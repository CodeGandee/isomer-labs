"""Persistence and concurrency boundary for mutable named Kaoju templates."""

from __future__ import annotations

import builtins
from contextlib import contextmanager
import json
from pathlib import Path
import shutil
import tempfile
from typing import Iterator, Mapping, Sequence
import uuid

from isomer_labs.kaoju.artifacts import KaojuArtifactService, KaojuServiceError
from isomer_labs.kaoju.content import (
    DIRECTORY_MANIFEST_NAME,
    ArtifactContent,
    create_managed_directory_artifact,
    register_ordinary_file,
    validate_directory_manifest,
)
from isomer_labs.kaoju.contracts import KaojuBinding, load_binding_registry
from isomer_labs.kaoju.template_support import (
    AUDIT_VERSION,
    EXPORT_METADATA_NAME,
    TEMPLATE_AUDIT_SEMANTIC_ID,
    TEMPLATE_EXCHANGE_LABEL,
    TEMPLATE_EXPORT_MANIFEST_SEMANTIC_ID,
    TEMPLATE_EXPORT_SEMANTIC_ID,
    TEMPLATE_SEMANTIC_ID,
    TemplateState,
    _AUTHORED_METADATA_KEYS,
    _atomic_write_json,
    _contains_exact,
    _new_state_token,
    _required_actor,
    template_tree_digest,
    validate_template_name,
    validate_template_relative_path,
)
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.index import refresh_query_index_for_record
from isomer_labs.runtime.records import RuntimeLifecycleRecord, _provenance_ref, utc_timestamp
from isomer_labs.runtime.store import WorkspaceRuntimeStore, open_workspace_runtime
from isomer_labs.workspace.path_resolution import materialize_semantic_path, resolve_semantic_path


class KaojuTemplateStateService:
    """Own stable records, managed trees, audits, and optimistic concurrency."""

    def __init__(self, context: EffectiveTopicContext, *, env: Mapping[str, str], cwd: Path) -> None:
        self.context = context
        self.env = env
        self.cwd = cwd
        self.artifacts = KaojuArtifactService(context, env=env, cwd=cwd)

    def _create_from_directory(
        self,
        name: str,
        source: Path,
        *,
        authored_metadata: Mapping[str, object],
        actor: str,
        source_refs: Sequence[str],
        operation: str,
        change_summary: str | None,
    ) -> dict[str, object]:
        tree_digest = template_tree_digest(source)
        stable_ref = f"artifact-paper-template-myst-{name}"
        state_token = _new_state_token()
        now = utc_timestamp()
        audit_id = self._audit_id(name)
        prepared = create_managed_directory_artifact(
            self.context,
            source,
            semantic_label="topic.records.artifacts",
            record_kind="artifact",
            record_id=f"{stable_ref}-state-{uuid.uuid4().hex[:12]}",
            env=self.env,
            cwd=self.cwd,
        )
        metadata = self._template_metadata(
            name=name,
            content=prepared,
            state_token=state_token,
            tree_digest=tree_digest,
            authored_metadata=authored_metadata,
            audit_ref=audit_id,
            actor=actor,
            operation=operation,
            change_summary=change_summary,
        )
        record = RuntimeLifecycleRecord(
            id=stable_ref,
            record_kind="artifact",
            research_topic_id=self.context.research_topic.id,
            topic_workspace_id=self.context.topic_workspace_id,
            status="ready",
            created_at=now,
            updated_at=now,
            lifecycle_refs={},
            transition_metadata=metadata,
            content_path=str(prepared.content_path),
            provenance_refs=[_provenance_ref("artifact", stable_ref), _provenance_ref("template-mutation-audit", audit_id)],
        )
        provisional = TemplateState(record, name, state_token, tree_digest, dict(authored_metadata), prepared.content_path.parent)
        event = self._audit_event(
            audit_id=audit_id,
            state=provisional,
            operation=operation,
            actor=actor,
            source_refs=source_refs,
            occurred_at=now,
            prior_state_token=None,
            state_token=state_token,
            prior_tree_digest=None,
            tree_digest=tree_digest,
            change_summary=change_summary,
        )
        audit_owner: Path | None = None
        try:
            audit_record, audit_owner = self._prepare_audit_record(event, audit_id=audit_id, template_ref=stable_ref, name=name, now=now)
            store = self._store(read_only=False)
        except Exception:
            self._discard_managed_tree(str(prepared.content_path))
            if audit_owner is not None:
                shutil.rmtree(audit_owner, ignore_errors=True)
            raise
        index_diagnostics: list[dict[str, object]] = []
        try:
            store.connection.execute("BEGIN IMMEDIATE")
            if self._find_named_record(store, name) is not None or store.get_lifecycle_record(stable_ref) is not None:
                raise KaojuServiceError("template_already_exists", f"A named template already exists: {name}")
            store.upsert_lifecycle_record(record)
            store.upsert_lifecycle_record(audit_record)
            store.connection.commit()
            index_diagnostics = self._refresh_index_after_commit(store, (stable_ref, audit_id))
        except Exception:
            store.connection.rollback()
            self._discard_managed_tree(str(prepared.content_path))
            shutil.rmtree(audit_owner, ignore_errors=True)
            raise
        finally:
            store.close()
        return self._mutation_payload(
            operation=operation,
            name=name,
            stable_ref=stable_ref,
            prior_state_token=None,
            state_token=state_token,
            prior_tree_digest=None,
            tree_digest=tree_digest,
            audit_ref=audit_id,
            authored_metadata=authored_metadata,
            status="ready",
            diagnostics=index_diagnostics,
        )

    def _replace_tree(
        self,
        state: TemplateState,
        source: Path,
        *,
        expected_state: str,
        authored_metadata: Mapping[str, object],
        actor: str,
        operation: str,
        source_refs: Sequence[str],
        change_summary: str | None,
    ) -> dict[str, object]:
        tree_digest = template_tree_digest(source)
        validated_metadata = self._validated_authored_metadata(authored_metadata, root=source)
        if tree_digest == state.tree_digest and validated_metadata == state.authored_metadata:
            self._require_expected_state(self._read_state(state.name), expected_state)
            return self._no_change_payload(state, operation=operation)
        next_token = _new_state_token()
        now = utc_timestamp()
        audit_id = self._audit_id(state.name)
        prepared = create_managed_directory_artifact(
            self.context,
            source,
            semantic_label="topic.records.artifacts",
            record_kind="artifact",
            record_id=f"{state.record.id}-state-{uuid.uuid4().hex[:12]}",
            env=self.env,
            cwd=self.cwd,
        )
        event = self._audit_event(
            audit_id=audit_id,
            state=state,
            operation=operation,
            actor=actor,
            source_refs=source_refs,
            occurred_at=now,
            prior_state_token=state.state_token,
            state_token=next_token,
            prior_tree_digest=state.tree_digest,
            tree_digest=tree_digest,
            change_summary=change_summary,
        )
        audit_owner: Path | None = None
        try:
            audit_record, audit_owner = self._prepare_audit_record(event, audit_id=audit_id, template_ref=state.record.id, name=state.name, now=now)
            store = self._store(read_only=False)
        except Exception:
            self._discard_managed_tree(str(prepared.content_path))
            if audit_owner is not None:
                shutil.rmtree(audit_owner, ignore_errors=True)
            raise
        index_diagnostics: list[dict[str, object]] = []
        try:
            store.connection.execute("BEGIN IMMEDIATE")
            current = store.get_lifecycle_record(state.record.id)
            self._require_locked_state(current, state, expected_state)
            assert current is not None
            metadata = dict(current.transition_metadata)
            metadata.update(
                {
                    "artifact_content": prepared.metadata(),
                    "tree_digest": tree_digest,
                    "state_token": next_token,
                    "authored_metadata": dict(validated_metadata),
                    "last_audit_ref": audit_id,
                    "last_mutation": self._mutation_summary(operation, actor, now, source_refs, change_summary),
                }
            )
            updated = RuntimeLifecycleRecord(
                **{
                    **current.__dict__,
                    "updated_at": now,
                    "transition_metadata": metadata,
                    "content_path": str(prepared.content_path),
                    "provenance_refs": [*current.provenance_refs, _provenance_ref("template-mutation-audit", audit_id)],
                }
            )
            store.upsert_lifecycle_record(updated)
            store.upsert_lifecycle_record(audit_record)
            store.connection.commit()
            index_diagnostics = self._refresh_index_after_commit(store, (state.record.id, audit_id))
        except Exception:
            store.connection.rollback()
            self._discard_managed_tree(str(prepared.content_path))
            shutil.rmtree(audit_owner, ignore_errors=True)
            raise
        finally:
            store.close()
        self._discard_managed_tree(state.record.content_path)
        return self._mutation_payload(
            operation=operation,
            name=state.name,
            stable_ref=state.record.id,
            prior_state_token=state.state_token,
            state_token=next_token,
            prior_tree_digest=state.tree_digest,
            tree_digest=tree_digest,
            audit_ref=audit_id,
            authored_metadata=validated_metadata,
            status="ready",
            diagnostics=index_diagnostics,
        )

    def _replace_metadata(
        self,
        state: TemplateState,
        *,
        expected_state: str,
        authored_metadata: Mapping[str, object],
        actor: str,
        operation: str,
        source_refs: Sequence[str],
        change_summary: str | None,
        status: str | None = None,
    ) -> dict[str, object]:
        next_status = status or state.record.status
        if dict(authored_metadata) == state.authored_metadata and next_status == state.record.status:
            self._require_expected_state(self._read_state(state.name), expected_state)
            return self._no_change_payload(state, operation=operation)
        next_token = _new_state_token()
        now = utc_timestamp()
        audit_id = self._audit_id(state.name)
        event = self._audit_event(
            audit_id=audit_id,
            state=state,
            operation=operation,
            actor=actor,
            source_refs=source_refs,
            occurred_at=now,
            prior_state_token=state.state_token,
            state_token=next_token,
            prior_tree_digest=state.tree_digest,
            tree_digest=state.tree_digest,
            change_summary=change_summary,
        )
        audit_record, audit_owner = self._prepare_audit_record(event, audit_id=audit_id, template_ref=state.record.id, name=state.name, now=now)
        try:
            store = self._store(read_only=False)
        except Exception:
            shutil.rmtree(audit_owner, ignore_errors=True)
            raise
        index_diagnostics: list[dict[str, object]] = []
        try:
            store.connection.execute("BEGIN IMMEDIATE")
            current = store.get_lifecycle_record(state.record.id)
            self._require_locked_state(current, state, expected_state)
            assert current is not None
            metadata = dict(current.transition_metadata)
            metadata.update(
                {
                    "state_token": next_token,
                    "authored_metadata": dict(authored_metadata),
                    "last_audit_ref": audit_id,
                    "last_mutation": self._mutation_summary(operation, actor, now, source_refs, change_summary),
                }
            )
            updated = RuntimeLifecycleRecord(
                **{
                    **current.__dict__,
                    "status": next_status,
                    "updated_at": now,
                    "transition_metadata": metadata,
                    "provenance_refs": [*current.provenance_refs, _provenance_ref("template-mutation-audit", audit_id)],
                }
            )
            store.upsert_lifecycle_record(updated)
            store.upsert_lifecycle_record(audit_record)
            store.connection.commit()
            index_diagnostics = self._refresh_index_after_commit(store, (state.record.id, audit_id))
        except Exception:
            store.connection.rollback()
            shutil.rmtree(audit_owner, ignore_errors=True)
            raise
        finally:
            store.close()
        return self._mutation_payload(
            operation=operation,
            name=state.name,
            stable_ref=state.record.id,
            prior_state_token=state.state_token,
            state_token=next_token,
            prior_tree_digest=state.tree_digest,
            tree_digest=state.tree_digest,
            audit_ref=audit_id,
            authored_metadata=authored_metadata,
            status=next_status,
            diagnostics=index_diagnostics,
        )

    def _read_state(self, name: str) -> TemplateState:
        store = self._store(read_only=True)
        try:
            record = self._find_named_record(store, name)
        finally:
            store.close()
        if record is None:
            raise KaojuServiceError("template_not_found", f"Named template not found: {name}")
        return self._state_from_record(record)

    def _read_record(self, record_id: str) -> RuntimeLifecycleRecord:
        store = self._store(read_only=True)
        try:
            record = store.get_lifecycle_record(record_id)
        finally:
            store.close()
        if record is None or record.topic_workspace_id != self.context.topic_workspace_id:
            raise KaojuServiceError("template_record_not_found", f"Template record not found: {record_id}")
        return record

    def _state_from_record(self, record: RuntimeLifecycleRecord) -> TemplateState:
        metadata = record.transition_metadata
        name = metadata.get("template_name")
        state_token = metadata.get("state_token")
        tree_digest = metadata.get("tree_digest")
        authored = metadata.get("authored_metadata")
        if not isinstance(name, str) or not isinstance(state_token, str) or not isinstance(tree_digest, str) or not isinstance(authored, dict):
            raise KaojuServiceError("template_state_invalid", f"Named template record has incomplete mutable state: {record.id}")
        if record.content_path is None:
            raise KaojuServiceError("template_content_missing", f"Named template has no managed content: {record.id}")
        manifest_path = Path(record.content_path)
        if manifest_path.name != DIRECTORY_MANIFEST_NAME or not manifest_path.is_file():
            raise KaojuServiceError("template_content_invalid", f"Named template does not resolve to a managed directory manifest: {record.id}")
        diagnostics = validate_directory_manifest(manifest_path)
        if any(item.get("severity") == "error" for item in diagnostics):
            raise KaojuServiceError("template_content_corrupt", f"Named template content failed manifest validation: {record.id}", tuple(str(item.get("message")) for item in diagnostics))
        root = manifest_path.parent
        observed_digest = template_tree_digest(root, allow_internal_manifest=True)
        if observed_digest != tree_digest:
            raise KaojuServiceError("template_digest_mismatch", f"Named template tree digest does not match its stable record: {record.id}")
        return TemplateState(record, validate_template_name(name), state_token, tree_digest, dict(authored), root)

    def _find_named_record(self, store: WorkspaceRuntimeStore, name: str) -> RuntimeLifecycleRecord | None:
        matches = [
            record
            for record in store.list_lifecycle_records()
            if self._is_named_template_record(record) and record.transition_metadata.get("template_name") == name
        ]
        if len(matches) > 1:
            raise KaojuServiceError("template_identity_conflict", f"Template name {name!r} resolves to several stable records: {', '.join(record.id for record in matches)}")
        return matches[0] if matches else None

    def _is_named_template_record(self, record: RuntimeLifecycleRecord) -> bool:
        metadata = record.transition_metadata
        return (
            record.topic_workspace_id == self.context.topic_workspace_id
            and metadata.get("semantic_id") == TEMPLATE_SEMANTIC_ID
            and isinstance(metadata.get("template_name"), str)
            and isinstance(metadata.get("state_token"), str)
        )

    def _summary(self, state: TemplateState, *, exchange_root: Path | None = None) -> dict[str, object]:
        root = exchange_root or self._exchange_root(materialize=False)
        working_path = self._safe_named_child(root, state.name)
        return {
            "name": state.name,
            "stable_ref": state.record.id,
            "semantic_id": TEMPLATE_SEMANTIC_ID,
            "status": state.record.status,
            "state_token": state.state_token,
            "tree_digest": state.tree_digest,
            "authored_metadata": state.authored_metadata,
            "default_working_path": str(working_path),
            "exchange_root_label": TEMPLATE_EXCHANGE_LABEL,
            "content_path": state.record.content_path,
            "updated_at": state.record.updated_at,
        }

    def _require_expected_state(self, state: TemplateState, expected_state: str, *, allow_archived: bool = False) -> None:
        if not expected_state:
            raise KaojuServiceError("template_expected_state_required", "A current expected state token is required for this template mutation.")
        if state.state_token != expected_state:
            raise KaojuServiceError(
                "template_state_stale",
                f"Template {state.name!r} changed; expected {expected_state!r}, current state is {state.state_token!r} with digest {state.tree_digest}.",
                ("Read the current template state and reconcile before retrying.",),
            )
        allowed_statuses = {"ready", "archived"} if allow_archived else {"ready"}
        if state.record.status not in allowed_statuses:
            raise KaojuServiceError("template_not_active", f"Template {state.name!r} is {state.record.status!r} and cannot be mutated.")

    def _require_locked_state(self, current: RuntimeLifecycleRecord | None, prior: TemplateState, expected_state: str, *, allow_archived: bool = False) -> None:
        if current is None or not self._is_named_template_record(current):
            raise KaojuServiceError("template_not_found", f"Named template no longer exists: {prior.name}")
        current_token = current.transition_metadata.get("state_token")
        current_digest = current.transition_metadata.get("tree_digest")
        if current.id != prior.record.id or current_token != expected_state:
            raise KaojuServiceError(
                "template_state_stale",
                f"Template {prior.name!r} changed before commit; current state is {current_token!r} with digest {current_digest!r}.",
                ("Read the current template state and reconcile before retrying.",),
            )
        allowed_statuses = {"ready", "archived"} if allow_archived else {"ready"}
        if current.status not in allowed_statuses:
            raise KaojuServiceError("template_not_active", f"Template {prior.name!r} is {current.status!r} and cannot be mutated.")

    def _template_metadata(
        self,
        *,
        name: str,
        content: ArtifactContent,
        state_token: str,
        tree_digest: str,
        authored_metadata: Mapping[str, object],
        audit_ref: str,
        actor: str,
        operation: str,
        change_summary: str | None,
    ) -> dict[str, object]:
        binding = load_binding_registry()[TEMPLATE_SEMANTIC_ID]
        now = utc_timestamp()
        return {
            **self._binding_metadata(binding, content, scope_key=name, relationships=[]),
            "template_name": name,
            "state_token": state_token,
            "tree_digest": tree_digest,
            "authored_metadata": dict(authored_metadata),
            "last_audit_ref": audit_ref,
            "last_mutation": self._mutation_summary(operation, actor, now, (), change_summary),
        }

    def _binding_metadata(
        self,
        binding: KaojuBinding,
        content: ArtifactContent,
        *,
        scope_key: str,
        relationships: Sequence[dict[str, object]],
    ) -> dict[str, object]:
        return {
            "artifact_type": binding.artifact_type,
            "content_mode": binding.content_mode,
            "artifact_content": content.metadata(),
            "binding_schema_version": "isomer-kaoju-binding-registry.v2",
            "accepted_statuses": list(binding.acceptance["statuses"]),
            "contract_diagnostics": [],
            "relationships": [dict(item) for item in relationships],
            "semantic_id": binding.semantic_id,
            "scope_key": scope_key,
            "skill": binding.producer,
            "producer": binding.producer,
            "consumer": ",".join(binding.consumers),
            "semantic_label": binding.semantic_label,
            "query_index": {"relationships": [dict(item) for item in relationships]},
        }

    def _validated_authored_metadata(
        self,
        value: Mapping[str, object],
        *,
        root: Path,
        allow_internal_manifest: bool = False,
    ) -> dict[str, object]:
        unknown = sorted(set(value) - _AUTHORED_METADATA_KEYS)
        if unknown:
            raise KaojuServiceError("template_metadata_unknown", f"Template authored metadata contains unsupported fields: {', '.join(unknown)}")
        result: dict[str, object] = {}
        entrypoint = value.get("entrypoint")
        if entrypoint is not None:
            if not isinstance(entrypoint, str):
                raise KaojuServiceError("template_entrypoint_invalid", "Template entrypoint metadata must be a safe relative file path.")
            relative = validate_template_relative_path(entrypoint)
            candidate = root.joinpath(*relative.parts)
            if not candidate.is_file() or candidate.is_symlink():
                raise KaojuServiceError("template_entrypoint_missing", f"Template entrypoint does not exist in the prepared tree: {entrypoint}")
            result["entrypoint"] = relative.as_posix()
        guidance = value.get("use_guidance")
        if guidance is not None:
            if not isinstance(guidance, str) or not guidance.strip() or len(guidance) > 20_000:
                raise KaojuServiceError("template_use_guidance_invalid", "Template use guidance must be a non-empty string of at most 20,000 characters.")
            result["use_guidance"] = guidance
        extensions = value.get("extensions")
        if extensions is not None:
            if not isinstance(extensions, dict):
                raise KaojuServiceError("template_extensions_invalid", "Template extension metadata must be a JSON object.")
            encoded = json.dumps(extensions, sort_keys=True, ensure_ascii=False)
            if len(encoded.encode("utf-8")) > 64 * 1024:
                raise KaojuServiceError("template_extensions_too_large", "Template extension metadata exceeds 64 KiB.")
            result["extensions"] = dict(extensions)
        if allow_internal_manifest:
            template_tree_digest(root, allow_internal_manifest=True)
        return result

    def _audit_event(
        self,
        *,
        audit_id: str,
        state: TemplateState,
        operation: str,
        actor: str,
        source_refs: Sequence[str],
        occurred_at: str,
        prior_state_token: str | None,
        state_token: str | None,
        prior_tree_digest: str | None,
        tree_digest: str | None,
        change_summary: str | None,
    ) -> dict[str, object]:
        return {
            "schema_version": AUDIT_VERSION,
            "audit_ref": audit_id,
            "template_ref": state.record.id,
            "template_name": state.name,
            "actor": _required_actor(actor),
            "operation": operation,
            "source_refs": list(source_refs),
            "occurred_at": occurred_at,
            "prior_state_token": prior_state_token,
            "state_token": state_token,
            "prior_tree_digest": prior_tree_digest,
            "tree_digest": tree_digest,
            "change_summary": change_summary,
        }

    def _prepare_audit_record(
        self,
        event: Mapping[str, object],
        *,
        audit_id: str,
        template_ref: str,
        name: str,
        now: str,
    ) -> tuple[RuntimeLifecycleRecord, Path]:
        resolution, diagnostics = resolve_semantic_path(self.context, "topic.records.views", env=self.env, cwd=self.cwd)
        if resolution is None:
            raise KaojuServiceError("template_audit_path_unavailable", "Template mutation audit path could not be resolved.", tuple(item.message for item in diagnostics))
        owner = resolution.path / "research-records" / "view_manifest" / audit_id
        path = owner / "template-mutation-audit.json"
        owner.mkdir(parents=True, exist_ok=False)
        try:
            _atomic_write_json(path, event)
            content = register_ordinary_file(path)
            binding = load_binding_registry()[TEMPLATE_AUDIT_SEMANTIC_ID]
            relationships: Sequence[dict[str, object]] = [{"role": "paper_template", "target_ref": template_ref}]
            metadata = self._binding_metadata(binding, content, scope_key=name, relationships=relationships)
            metadata.update({"template_name": name, "mutation": dict(event)})
        except Exception:
            shutil.rmtree(owner, ignore_errors=True)
            raise
        return (
            RuntimeLifecycleRecord(
                id=audit_id,
                record_kind="view_manifest",
                research_topic_id=self.context.research_topic.id,
                topic_workspace_id=self.context.topic_workspace_id,
                status="ready",
                created_at=now,
                updated_at=now,
                lifecycle_refs={},
                transition_metadata=metadata,
                content_path=str(path.resolve(strict=False)),
                provenance_refs=[_provenance_ref("view_manifest", audit_id)],
            ),
            owner,
        )

    def _dependent_paper_records(self, state: TemplateState) -> builtins.list[str]:
        store = self._store(read_only=True)
        try:
            records = store.list_lifecycle_records()
        finally:
            store.close()
        ignored = {TEMPLATE_SEMANTIC_ID, TEMPLATE_AUDIT_SEMANTIC_ID, TEMPLATE_EXPORT_SEMANTIC_ID, TEMPLATE_EXPORT_MANIFEST_SEMANTIC_ID}
        dependents: list[str] = []
        for record in records:
            semantic_id = record.transition_metadata.get("semantic_id")
            if record.id == state.record.id or semantic_id in ignored or record.status in {"archived", "superseded"}:
                continue
            if isinstance(semantic_id, str) and semantic_id.startswith("KAOJU:PAPER") and _contains_exact(record.transition_metadata, state.record.id):
                dependents.append(record.id)
        return sorted(dependents)

    def _exchange_root(self, *, materialize: bool) -> Path:
        if materialize:
            payload, diagnostics = materialize_semantic_path(self.context, TEMPLATE_EXCHANGE_LABEL, env=self.env, cwd=self.cwd)
            if payload is None:
                raise KaojuServiceError("template_exchange_root_unavailable", "Template exchange root could not be materialized.", tuple(item.message for item in diagnostics))
        resolution, diagnostics = resolve_semantic_path(self.context, TEMPLATE_EXCHANGE_LABEL, env=self.env, cwd=self.cwd, use_path_plan=False)
        if resolution is None:
            raise KaojuServiceError("template_exchange_root_unavailable", "Template exchange root could not be resolved.", tuple(item.message for item in diagnostics))
        return resolution.path.resolve(strict=False)

    def _default_working_path(self, name: str, *, materialize: bool) -> Path:
        return self._safe_named_child(self._exchange_root(materialize=materialize), validate_template_name(name))

    def _safe_named_child(self, root: Path, name: str) -> Path:
        child = (root / validate_template_name(name)).resolve(strict=False)
        try:
            child.relative_to(root.resolve(strict=False))
        except ValueError as exc:
            raise KaojuServiceError("template_path_escape", f"Template working path escapes the exchange root: {child}") from exc
        return child

    def _copy_canonical_tree(self, source: Path, target: Path) -> None:
        template_tree_digest(source, allow_internal_manifest=True)
        target.mkdir(parents=True, exist_ok=True)
        for path in sorted(source.rglob("*"), key=lambda item: item.relative_to(source).as_posix()):
            relative = path.relative_to(source)
            if path.is_symlink():
                raise KaojuServiceError("template_symlink_forbidden", f"Template trees cannot contain symbolic links: {relative.as_posix()}")
            if relative.as_posix() in {DIRECTORY_MANIFEST_NAME, EXPORT_METADATA_NAME}:
                continue
            destination = target / relative
            if path.is_dir():
                destination.mkdir(parents=True, exist_ok=True)
            elif path.is_file():
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(path, destination)

    def _store(self, *, read_only: bool) -> WorkspaceRuntimeStore:
        store, diagnostics = open_workspace_runtime(self.context, env=self.env, read_only=read_only)
        if store is None:
            raise KaojuServiceError("workspace_runtime_missing", "Workspace Runtime is unavailable.", tuple(item.message for item in diagnostics))
        return store

    def _refresh_index_after_commit(
        self,
        store: WorkspaceRuntimeStore,
        record_ids: Sequence[str],
    ) -> builtins.list[dict[str, object]]:
        diagnostics: list[dict[str, object]] = []
        for record_id in record_ids:
            try:
                payload = refresh_query_index_for_record(self.context, store, record_id)
            except Exception as exc:
                diagnostics.append(self._index_warning("query_index_refresh_failed", exc, record_id=record_id))
                continue
            if payload.get("ok") is False:
                diagnostics.append(
                    {
                        "severity": "warning",
                        "code": "query_index_refresh_failed",
                        "message": f"Canonical template state committed, but query-index refresh failed for {record_id}.",
                        "record_id": record_id,
                    }
                )
        return diagnostics

    def _index_warning(self, code: str, exc: Exception, *, record_id: str | None = None) -> dict[str, object]:
        payload: dict[str, object] = {
            "severity": "warning",
            "code": code,
            "message": f"Canonical template state committed, but index maintenance failed: {exc}",
        }
        if record_id is not None:
            payload["record_id"] = record_id
        return payload

    def _discard_managed_tree(self, content_path: str | None) -> None:
        if content_path is None:
            return
        path = Path(content_path)
        if path.name != DIRECTORY_MANIFEST_NAME or path.parent.name != "content":
            return
        owner = path.parent.parent
        shutil.rmtree(owner, ignore_errors=True)

    def _mutation_payload(
        self,
        *,
        operation: str,
        name: str,
        stable_ref: str,
        prior_state_token: str | None,
        state_token: str | None,
        prior_tree_digest: str | None,
        tree_digest: str | None,
        audit_ref: str,
        authored_metadata: Mapping[str, object],
        status: str,
        diagnostics: Sequence[Mapping[str, object]] = (),
    ) -> dict[str, object]:
        next_actions = ["Run 'isomer-cli ext research records index rebuild' to repair query-index state."] if diagnostics else []
        return {
            "ok": True,
            "mutated": True,
            "operation": f"paper.template.{operation}",
            "name": name,
            "stable_ref": stable_ref,
            "status": status,
            "prior_state_token": prior_state_token,
            "state_token": state_token,
            "prior_tree_digest": prior_tree_digest,
            "tree_digest": tree_digest,
            "authored_metadata": dict(authored_metadata),
            "audit_ref": audit_ref,
            "affected_refs": [stable_ref, audit_ref],
            "diagnostics": [dict(item) for item in diagnostics],
            "next_actions": next_actions,
        }

    def _no_change_payload(self, state: TemplateState, *, operation: str) -> dict[str, object]:
        return {
            "ok": True,
            "mutated": False,
            "operation": f"paper.template.{operation}",
            "name": state.name,
            "stable_ref": state.record.id,
            "status": state.record.status,
            "prior_state_token": state.state_token,
            "state_token": state.state_token,
            "prior_tree_digest": state.tree_digest,
            "tree_digest": state.tree_digest,
            "authored_metadata": state.authored_metadata,
            "audit_ref": None,
            "affected_refs": [],
            "diagnostics": [],
            "next_actions": [],
        }

    def _mutation_summary(
        self,
        operation: str,
        actor: str,
        occurred_at: str,
        source_refs: Sequence[str],
        change_summary: str | None,
    ) -> dict[str, object]:
        return {
            "operation": operation,
            "actor": _required_actor(actor),
            "occurred_at": occurred_at,
            "source_refs": list(source_refs),
            "change_summary": change_summary,
        }

    def _audit_id(self, name: str) -> str:
        return f"artifact-paper-template-mutation-audit-{name}-{uuid.uuid4().hex[:12]}"

    @contextmanager
    def _temporary_directory(self, prefix: str) -> Iterator[Path]:
        root = self.context.topic_workspace_path / "tmp" / "kaoju-template-service"
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=prefix, dir=root) as raw:
            yield Path(raw)
