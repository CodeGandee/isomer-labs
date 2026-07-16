"""Mutable named Kaoju paper templates and non-canonical working copies."""

from __future__ import annotations

import builtins
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
from typing import Mapping, Sequence

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.content import DIRECTORY_MANIFEST_NAME
from isomer_labs.kaoju.template_state import KaojuTemplateStateService
from isomer_labs.kaoju.template_support import (
    DEFAULT_TEMPLATE_NAME,
    EXPORT_METADATA_NAME,
    EXPORT_METADATA_VERSION,
    TEMPLATE_EXCHANGE_LABEL,
    TEMPLATE_EXPORT_MANIFEST_SEMANTIC_ID,
    TEMPLATE_EXPORT_SEMANTIC_ID,
    TEMPLATE_PRODUCER,
    TEMPLATE_SEMANTIC_ID,
    TemplateState,
    _AUTHORED_METADATA_KEYS,
    _SERVICE_METADATA_KEYS,
    _atomic_write_json,
    _load_export_metadata,
    _nested_string,
    _prune_empty_parents,
    _replace_directory,
    _required_actor,
    _result_ref,
    _unique_strings,
    _utc_now,
    template_tree_digest,
    validate_template_name,
    validate_template_relative_path,
)
from isomer_labs.records.index import cleanup_query_index
from isomer_labs.runtime.records import RuntimeLifecycleRecord, utc_timestamp




class KaojuTemplateService(KaojuTemplateStateService):
    """Own low-level named-template state and working-copy exchange."""


    def list(self) -> dict[str, object]:
        store = self._store(read_only=True)
        try:
            root = self._exchange_root(materialize=False)
            records = [
                record
                for record in store.list_lifecycle_records()
                if self._is_named_template_record(record)
            ]
            templates = [self._summary(self._state_from_record(record), exchange_root=root) for record in records]
        finally:
            store.close()
        templates.sort(key=lambda item: str(item["name"]))
        return {
            "ok": True,
            "mutated": False,
            "operation": "paper.template.list",
            "count": len(templates),
            "templates": templates,
            "diagnostics": [],
            "next_actions": [],
        }

    def show(self, name: str) -> dict[str, object]:
        state = self._read_state(validate_template_name(name))
        return {
            "ok": True,
            "mutated": False,
            "operation": "paper.template.show",
            "template": self._summary(state),
            "diagnostics": [],
            "next_actions": [],
        }

    def create(
        self,
        name: str,
        *,
        source: Path | None = None,
        from_template: str | None = None,
        authored_metadata: Mapping[str, object] | None = None,
        actor: str,
        source_refs: Sequence[str] = (),
        change_summary: str | None = None,
    ) -> dict[str, object]:
        selected_name = validate_template_name(name)
        if (source is None) == (from_template is None):
            raise KaojuServiceError("template_source_conflict", "Template create requires exactly one of a prepared directory or an existing template name.")
        copied_from: str | None = None
        inherited_metadata: dict[str, object] = {}
        if from_template is not None:
            source_state = self._read_state(validate_template_name(from_template))
            copied_from = source_state.record.id
            inherited_metadata = dict(source_state.authored_metadata)
            with self._temporary_directory("template-copy-") as temporary:
                candidate = temporary / "candidate"
                self._copy_canonical_tree(source_state.root, candidate)
                return self._create_from_directory(
                    selected_name,
                    candidate,
                    authored_metadata=self._validated_authored_metadata(authored_metadata or inherited_metadata, root=candidate),
                    actor=actor,
                    source_refs=_unique_strings((*source_refs, copied_from)),
                    operation="create-from-template",
                    change_summary=change_summary,
                )
        assert source is not None
        return self._create_from_directory(
            selected_name,
            source,
            authored_metadata=self._validated_authored_metadata(authored_metadata or {}, root=source),
            actor=actor,
            source_refs=_unique_strings(source_refs),
            operation="create",
            change_summary=change_summary,
        )

    def update(
        self,
        name: str,
        *,
        expected_state: str,
        source: Path | None = None,
        from_template: str | None = None,
        actor: str,
        source_refs: Sequence[str] = (),
        change_summary: str | None = None,
    ) -> dict[str, object]:
        selected_name = validate_template_name(name)
        if (source is None) == (from_template is None):
            raise KaojuServiceError("template_source_conflict", "Template update requires exactly one of a prepared directory or an existing template name.")
        target = self._read_state(selected_name)
        self._require_expected_state(target, expected_state)
        if from_template is not None:
            source_state = self._read_state(validate_template_name(from_template))
            with self._temporary_directory("template-replace-") as temporary:
                candidate = temporary / "candidate"
                self._copy_canonical_tree(source_state.root, candidate)
                return self._replace_tree(
                    target,
                    candidate,
                    expected_state=expected_state,
                    authored_metadata=source_state.authored_metadata,
                    actor=actor,
                    operation="update-from-template",
                    source_refs=_unique_strings((*source_refs, source_state.record.id)),
                    change_summary=change_summary,
                )
        assert source is not None
        return self._replace_tree(
            target,
            source,
            expected_state=expected_state,
            authored_metadata=target.authored_metadata,
            actor=actor,
            operation="update",
            source_refs=_unique_strings(source_refs),
            change_summary=change_summary,
        )

    def file_put(
        self,
        name: str,
        relative_path: str,
        source: Path,
        *,
        expected_state: str,
        actor: str,
        source_refs: Sequence[str] = (),
        change_summary: str | None = None,
    ) -> dict[str, object]:
        state = self._read_state(validate_template_name(name))
        self._require_expected_state(state, expected_state)
        relative = validate_template_relative_path(relative_path)
        selected_source = source.resolve(strict=False)
        if selected_source.is_symlink() or not selected_source.is_file():
            raise KaojuServiceError("template_file_source_invalid", f"Template file source is not a regular file: {selected_source}")
        with self._temporary_directory("template-file-put-") as temporary:
            candidate = temporary / "candidate"
            self._copy_canonical_tree(state.root, candidate)
            target = candidate.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(selected_source, target)
            return self._replace_tree(
                state,
                candidate,
                expected_state=expected_state,
                authored_metadata=state.authored_metadata,
                actor=actor,
                operation="file-put",
                source_refs=_unique_strings(source_refs),
                change_summary=change_summary or f"Put {relative.as_posix()}.",
            )

    def file_remove(
        self,
        name: str,
        relative_path: str,
        *,
        expected_state: str,
        actor: str,
        source_refs: Sequence[str] = (),
        change_summary: str | None = None,
    ) -> dict[str, object]:
        state = self._read_state(validate_template_name(name))
        self._require_expected_state(state, expected_state)
        relative = validate_template_relative_path(relative_path)
        with self._temporary_directory("template-file-remove-") as temporary:
            candidate = temporary / "candidate"
            self._copy_canonical_tree(state.root, candidate)
            target = candidate.joinpath(*relative.parts)
            if not target.is_file() or target.is_symlink():
                raise KaojuServiceError("template_file_missing", f"Template file does not exist: {relative.as_posix()}")
            target.unlink()
            _prune_empty_parents(target.parent, candidate)
            return self._replace_tree(
                state,
                candidate,
                expected_state=expected_state,
                authored_metadata=state.authored_metadata,
                actor=actor,
                operation="file-remove",
                source_refs=_unique_strings(source_refs),
                change_summary=change_summary or f"Removed {relative.as_posix()}.",
            )

    def metadata_patch(
        self,
        name: str,
        patch: Mapping[str, object],
        *,
        expected_state: str,
        actor: str,
        source_refs: Sequence[str] = (),
        change_summary: str | None = None,
    ) -> dict[str, object]:
        state = self._read_state(validate_template_name(name))
        self._require_expected_state(state, expected_state)
        unknown = sorted(set(patch) - _AUTHORED_METADATA_KEYS)
        protected = sorted(set(patch) & _SERVICE_METADATA_KEYS)
        if protected:
            raise KaojuServiceError("template_metadata_protected", f"Template metadata patch cannot change service-controlled fields: {', '.join(protected)}")
        if unknown:
            raise KaojuServiceError("template_metadata_unknown", f"Template metadata patch contains unsupported fields: {', '.join(unknown)}")
        next_metadata = dict(state.authored_metadata)
        for key, value in patch.items():
            if value is None:
                next_metadata.pop(key, None)
            else:
                next_metadata[key] = value
        validated = self._validated_authored_metadata(next_metadata, root=state.root, allow_internal_manifest=True)
        return self._replace_metadata(
            state,
            expected_state=expected_state,
            authored_metadata=validated,
            actor=actor,
            operation="metadata-patch",
            source_refs=_unique_strings(source_refs),
            change_summary=change_summary,
        )

    def archive(
        self,
        name: str,
        *,
        expected_state: str,
        actor: str,
        reason: str | None = None,
    ) -> dict[str, object]:
        state = self._read_state(validate_template_name(name))
        self._require_expected_state(state, expected_state)
        dependents = self._dependent_paper_records(state)
        if dependents:
            raise KaojuServiceError(
                "template_referenced",
                f"Template {state.name!r} is referenced by durable paper state: {', '.join(dependents)}.",
                ("Update or archive the dependent paper state before archiving this template.",),
            )
        return self._replace_metadata(
            state,
            expected_state=expected_state,
            authored_metadata=state.authored_metadata,
            actor=actor,
            operation="archive",
            source_refs=(),
            change_summary=reason,
            status="archived",
        )

    def delete(self, name: str, *, expected_state: str, actor: str) -> dict[str, object]:
        state = self._read_state(validate_template_name(name))
        self._require_expected_state(state, expected_state, allow_archived=True)
        dependents = self._dependent_paper_records(state)
        if dependents:
            raise KaojuServiceError(
                "template_referenced",
                f"Template {state.name!r} is referenced by durable paper state: {', '.join(dependents)}.",
                ("Update or archive the dependent paper state before deleting this template.",),
            )
        now = utc_timestamp()
        audit_id = self._audit_id(state.name)
        event = self._audit_event(
            audit_id=audit_id,
            state=state,
            operation="delete",
            actor=actor,
            source_refs=(),
            occurred_at=now,
            prior_state_token=state.state_token,
            state_token=None,
            prior_tree_digest=state.tree_digest,
            tree_digest=None,
            change_summary=None,
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
            self._require_locked_state(current, state, expected_state, allow_archived=True)
            store.delete_lifecycle_record(state.record.id)
            store.upsert_lifecycle_record(audit_record)
            store.connection.commit()
            index_diagnostics = self._refresh_index_after_commit(store, (audit_id,))
        except Exception:
            store.connection.rollback()
            shutil.rmtree(audit_owner, ignore_errors=True)
            raise
        finally:
            store.close()
        try:
            cleanup_query_index(self.context, env=self.env, orphaned=True, apply=True)
        except Exception as exc:
            index_diagnostics.append(self._index_warning("query_index_cleanup_failed", exc))
        self._discard_managed_tree(state.record.content_path)
        return self._mutation_payload(
            operation="delete",
            name=state.name,
            stable_ref=state.record.id,
            prior_state_token=state.state_token,
            state_token=None,
            prior_tree_digest=state.tree_digest,
            tree_digest=None,
            audit_ref=audit_id,
            authored_metadata=state.authored_metadata,
            status="deleted",
            diagnostics=index_diagnostics,
        )

    def exports(self) -> dict[str, object]:
        payload = self.artifacts.list(semantic_id=TEMPLATE_EXPORT_SEMANTIC_ID)
        raw_records = payload.get("records")
        records = [record for record in raw_records if isinstance(record, dict)] if isinstance(raw_records, list) else []
        latest_by_path: dict[str, dict[str, object]] = {}
        for record in records:
            metadata = record.get("transition_metadata")
            if not isinstance(metadata, dict) or not isinstance(metadata.get("observed_path"), str):
                continue
            observed_path = str(metadata["observed_path"])
            previous = latest_by_path.get(observed_path)
            if previous is None or str(record.get("updated_at") or record.get("created_at") or "") > str(previous.get("updated_at") or previous.get("created_at") or ""):
                latest_by_path[observed_path] = record
        exports = [self._export_status(record) for record in latest_by_path.values()]
        exports.sort(key=lambda item: (str(item.get("name")), str(item.get("path"))))
        return {
            "ok": True,
            "mutated": False,
            "operation": "paper.template.exports",
            "count": len(exports),
            "exports": exports,
            "diagnostics": [],
            "next_actions": [],
        }

    def export(
        self,
        name: str = DEFAULT_TEMPLATE_NAME,
        *,
        target: Path | None = None,
        actor: str,
    ) -> dict[str, object]:
        state = self._read_state(validate_template_name(name))
        if state.record.status != "ready":
            raise KaojuServiceError("template_not_active", f"Template {state.name!r} is not active and cannot be exported.")
        selected_target = target.resolve(strict=False) if target is not None else self._default_working_path(state.name, materialize=True)
        self._write_export(state, selected_target, actor=actor)
        return self._register_export_observation(state, selected_target, actor=actor, operation="export")

    def observe_export(self, name: str, target: Path, *, actor: str) -> dict[str, object]:
        state = self._read_state(validate_template_name(name))
        selected_target = target.resolve(strict=False)
        working_digest = template_tree_digest(selected_target, exclude_exchange_metadata=True)
        metadata = self._export_metadata(state, selected_target, actor=actor, exported_tree_digest=working_digest)
        _atomic_write_json(selected_target / EXPORT_METADATA_NAME, metadata)
        return self._register_export_observation(state, selected_target, actor=actor, operation="observe")

    def inspect_migration(self) -> dict[str, object]:
        store = self._store(read_only=True)
        try:
            legacy = [
                record
                for record in store.list_lifecycle_records()
                if record.topic_workspace_id == self.context.topic_workspace_id
                and record.transition_metadata.get("semantic_id") == TEMPLATE_SEMANTIC_ID
                and not self._is_named_template_record(record)
            ]
        finally:
            store.close()
        candidates: list[dict[str, object]] = []
        historical: list[str] = []
        for record in legacy:
            metadata = record.transition_metadata
            item = {
                "record_id": record.id,
                "status": record.status,
                "paper_line": metadata.get("scope_key") or metadata.get("paper_line"),
                "content_path": record.content_path,
                "content_mode": metadata.get("content_mode"),
                "digest": self._legacy_content_digest(record),
                "entrypoint_ambiguous": self._legacy_entrypoint_ambiguous(record),
            }
            if record.status in {"archived", "superseded", "stale"} or metadata.get("revision_of_record_id") or metadata.get("supersedes_record_id"):
                historical.append(record.id)
            else:
                candidates.append(item)
        old_export_root = self.context.topic_workspace_path / "exports" / "kaoju-paper"
        versioned_exports = sorted(str(path) for path in old_export_root.glob("**/v[0-9][0-9][0-9][0-9]") if path.is_dir()) if old_export_root.is_dir() else []
        return {
            "ok": True,
            "mutated": False,
            "operation": "paper.template.migrate.inspect",
            "active_candidates": candidates,
            "historical_record_ids": sorted(historical),
            "versioned_export_paths": versioned_exports,
            "legacy_latex_paths": self._legacy_latex_paths(),
            "diagnostics": [],
            "next_actions": self._migration_next_actions(candidates),
        }

    def migrate(
        self,
        *,
        record_id: str | None = None,
        name: str | None = None,
        actor: str,
    ) -> dict[str, object]:
        inspection = self.inspect_migration()
        candidates = inspection["active_candidates"]
        assert isinstance(candidates, list)
        selected: dict[str, object] | None = None
        if record_id is not None:
            selected = next((item for item in candidates if isinstance(item, dict) and item.get("record_id") == record_id), None)
            if selected is None:
                raise KaojuServiceError("template_migration_candidate_missing", f"Legacy template migration candidate not found: {record_id}")
        elif len(candidates) == 1:
            item = candidates[0]
            selected = item if isinstance(item, dict) else None
        elif len(candidates) > 1:
            raise KaojuServiceError("template_migration_ambiguous", "Several active legacy templates require explicit record ids and names.", tuple(str(item) for item in candidates))
        if selected is None:
            raise KaojuServiceError("template_migration_candidate_missing", "No active legacy paper template is available to migrate.")
        selected_name = validate_template_name(name or (DEFAULT_TEMPLATE_NAME if len(candidates) == 1 else ""))
        if selected.get("entrypoint_ambiguous") is True:
            raise KaojuServiceError("template_migration_entrypoint_ambiguous", "Legacy template content has an ambiguous entrypoint; agent review and an explicit prepared tree are required.")
        legacy_record = self._read_record(str(selected["record_id"]))
        with self._temporary_directory("template-migration-") as temporary:
            candidate = temporary / "candidate"
            candidate.mkdir()
            content_path = Path(str(legacy_record.content_path)) if legacy_record.content_path else None
            if content_path is None or not content_path.exists():
                raise KaojuServiceError("template_migration_content_missing", f"Legacy template content is missing for {legacy_record.id}.")
            if content_path.name == DIRECTORY_MANIFEST_NAME:
                self._copy_canonical_tree(content_path.parent, candidate)
            elif content_path.is_file():
                shutil.copyfile(content_path, candidate / content_path.name)
            else:
                raise KaojuServiceError("template_migration_content_invalid", f"Legacy template content is unsupported: {content_path}")
            result = self.create(
                selected_name,
                source=candidate,
                actor=actor,
                source_refs=(legacy_record.id,),
                change_summary="Wrap one unambiguous active legacy template in the mutable named-template tree without semantic rewriting.",
            )
        result["operation"] = "paper.template.migrate"
        result["legacy_record_id"] = legacy_record.id
        result["preserved_historical_record_ids"] = inspection["historical_record_ids"]
        result["preserved_versioned_export_paths"] = inspection["versioned_export_paths"]
        return result


    def _write_export(self, state: TemplateState, target: Path, *, actor: str) -> None:
        if target.exists() and not target.is_dir():
            raise KaojuServiceError("template_export_target_invalid", f"Template export target is not a directory: {target}")
        if target.exists():
            entries = list(target.iterdir())
            metadata_path = target / EXPORT_METADATA_NAME
            if entries and not metadata_path.is_file():
                raise KaojuServiceError(
                    "template_export_target_unrecognized",
                    f"Template export target contains unrecognized or legacy content: {target}",
                    ("Move or archive the existing directory outside Isomer, then export again.",),
                )
            if metadata_path.is_file():
                metadata = _load_export_metadata(metadata_path)
                if metadata.get("template_name") != state.name or metadata.get("canonical_ref") != state.record.id:
                    raise KaojuServiceError("template_export_identity_invalid", f"Template export target claims a different canonical identity: {target}")
                observed = template_tree_digest(target, exclude_exchange_metadata=True)
                if observed != metadata.get("exported_tree_digest"):
                    raise KaojuServiceError(
                        "template_export_edited",
                        f"Template export target contains edits and will not be overwritten: {target}",
                        ("Use the Kaoju agent to reconcile the working tree, then update or observe it explicitly.",),
                    )
        metadata = self._export_metadata(state, target, actor=actor, exported_tree_digest=state.tree_digest)
        target.parent.mkdir(parents=True, exist_ok=True)
        staged = Path(tempfile.mkdtemp(prefix=f".{target.name}.template-export-", dir=target.parent))
        try:
            self._copy_canonical_tree(state.root, staged)
            _atomic_write_json(staged / EXPORT_METADATA_NAME, metadata)
            _replace_directory(staged, target)
        finally:
            if staged.exists():
                shutil.rmtree(staged)

    def _export_metadata(
        self,
        state: TemplateState,
        target: Path,
        *,
        actor: str,
        exported_tree_digest: str,
    ) -> dict[str, object]:
        return {
            "schema_version": EXPORT_METADATA_VERSION,
            "template_name": state.name,
            "canonical_ref": state.record.id,
            "state_token": state.state_token,
            "canonical_tree_digest": state.tree_digest,
            "exported_tree_digest": exported_tree_digest,
            "observed_path": str(target.resolve(strict=False)),
            "observed_at": _utc_now(),
            "actor": _required_actor(actor),
            "exchange_root_label": TEMPLATE_EXCHANGE_LABEL,
            "canonical": False,
        }

    def _register_export_observation(
        self,
        state: TemplateState,
        target: Path,
        *,
        actor: str,
        operation: str,
    ) -> dict[str, object]:
        metadata = _load_export_metadata(target / EXPORT_METADATA_NAME)
        idempotency = hashlib.sha256(
            json.dumps(
                {
                    "operation": operation,
                    "path": str(target),
                    "state_token": state.state_token,
                    "exported_tree_digest": metadata.get("exported_tree_digest"),
                },
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        export_result = self.artifacts.put(
            TEMPLATE_EXPORT_SEMANTIC_ID,
            target,
            producer=TEMPLATE_PRODUCER,
            scope_key=state.name,
            relationships=[{"role": "paper_template", "target_ref": state.record.id}],
            idempotency_key=f"paper-template-export:{idempotency}",
            external=True,
            metadata={**metadata, "observation_operation": operation},
        )
        export_ref = _result_ref(export_result)
        with self._temporary_directory("template-export-manifest-") as temporary:
            payload_path = temporary / "template-export-manifest.json"
            payload = {
                "title": f"Template export {state.name}",
                "summary": "Registered non-canonical named-template working-copy observation.",
                "artifact_family": "kaoju",
                "semantic_id": TEMPLATE_EXPORT_MANIFEST_SEMANTIC_ID,
                "artifact_type": "paper-template-manifest",
                "sections": {
                    "export": {"ref": export_ref, "operation": operation, "canonical": False},
                    "source": {"template_name": state.name, "stable_ref": state.record.id, "state_token": state.state_token},
                    "tree": {"canonical_digest": state.tree_digest, "exported_digest": metadata.get("exported_tree_digest")},
                    "actor": {"ref": actor, "observed_at": metadata.get("observed_at"), "path": str(target)},
                },
            }
            _atomic_write_json(payload_path, payload)
            manifest_result = self.artifacts.put(
                TEMPLATE_EXPORT_MANIFEST_SEMANTIC_ID,
                payload_path,
                producer=TEMPLATE_PRODUCER,
                scope_key=state.name,
                relationships=[
                    {"role": "template_export", "target_ref": export_ref},
                    {"role": "paper_template", "target_ref": state.record.id},
                ],
                idempotency_key=f"paper-template-export-manifest:{idempotency}",
                metadata={**metadata, "observation_operation": operation},
            )
        manifest_ref = _result_ref(manifest_result)
        return {
            "ok": True,
            "mutated": True,
            "operation": f"paper.template.{operation}",
            "name": state.name,
            "stable_ref": state.record.id,
            "state_token": state.state_token,
            "tree_digest": state.tree_digest,
            "exported_tree_digest": metadata.get("exported_tree_digest"),
            "target": str(target),
            "exchange_root_label": TEMPLATE_EXCHANGE_LABEL,
            "canonical": False,
            "export_ref": export_ref,
            "manifest_ref": manifest_ref,
            "affected_refs": [export_ref, manifest_ref],
            "diagnostics": [],
            "next_actions": ["Edit the working copy, then use the Kaoju agent to prepare and apply an explicit named-template update."],
        }

    def _export_status(self, record: Mapping[str, object]) -> dict[str, object]:
        metadata_value = record.get("transition_metadata")
        metadata = metadata_value if isinstance(metadata_value, dict) else {}
        name = str(metadata.get("template_name") or metadata.get("scope_key") or "")
        observed_path = str(metadata.get("observed_path") or record.get("content_path") or "")
        path = Path(observed_path)
        posture = "missing"
        working_digest: str | None = None
        identity_valid = False
        canonical_changed = False
        if path.is_dir():
            metadata_path = path / EXPORT_METADATA_NAME
            if metadata_path.is_file():
                try:
                    disk_metadata = _load_export_metadata(metadata_path)
                    identity_valid = (
                        disk_metadata.get("template_name") == name
                        and disk_metadata.get("canonical_ref") == metadata.get("canonical_ref")
                        and disk_metadata.get("observed_path") == str(path.resolve(strict=False))
                    )
                    working_digest = template_tree_digest(path, exclude_exchange_metadata=True)
                    if identity_valid:
                        posture = "edited" if working_digest != disk_metadata.get("exported_tree_digest") else "unchanged"
                        try:
                            current = self._read_state(name)
                        except KaojuServiceError:
                            current = None
                        canonical_changed = current is None or current.record.id != disk_metadata.get("canonical_ref") or current.state_token != disk_metadata.get("state_token") or current.tree_digest != disk_metadata.get("canonical_tree_digest")
                        if posture == "unchanged" and canonical_changed:
                            posture = "canonical-changed"
                    else:
                        posture = "identity-invalid"
                except (KaojuServiceError, OSError, json.JSONDecodeError):
                    posture = "identity-invalid"
            else:
                posture = "identity-invalid"
        return {
            "name": name,
            "path": observed_path,
            "export_ref": record.get("id"),
            "canonical_ref": metadata.get("canonical_ref"),
            "recorded_state_token": metadata.get("state_token"),
            "recorded_canonical_tree_digest": metadata.get("canonical_tree_digest"),
            "recorded_exported_tree_digest": metadata.get("exported_tree_digest"),
            "working_tree_digest": working_digest,
            "posture": posture,
            "identity_valid": identity_valid,
            "canonical_changed": canonical_changed,
        }
    def _legacy_entrypoint_ambiguous(self, record: RuntimeLifecycleRecord) -> bool:
        if record.content_path is None:
            return True
        path = Path(record.content_path)
        if path.name != DIRECTORY_MANIFEST_NAME:
            return not path.is_file()
        candidates = [item for item in path.parent.rglob("*") if item.is_file() and item.name != DIRECTORY_MANIFEST_NAME and item.suffix.casefold() in {".md", ".myst"}]
        return len(candidates) > 1

    def _legacy_content_digest(self, record: RuntimeLifecycleRecord) -> str | None:
        recorded = _nested_string(record.transition_metadata, "artifact_content", "checksum")
        if recorded is not None:
            return recorded
        if record.content_path is None:
            return None
        path = Path(record.content_path)
        if not path.is_file():
            return None
        if path.name == DIRECTORY_MANIFEST_NAME:
            try:
                return template_tree_digest(path.parent, allow_internal_manifest=True)
            except KaojuServiceError:
                return None
        digest = hashlib.sha256()
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
        return f"sha256:{digest.hexdigest()}"

    def _legacy_latex_paths(self) -> builtins.list[str]:
        root = self._exchange_root(materialize=False)
        if not root.is_dir():
            return []
        markers = ("template.tex", "main.tex", "latexmkrc")
        return sorted(str(path) for path in root.iterdir() if path.is_dir() and any((path / marker).exists() for marker in markers))

    def _migration_next_actions(self, candidates: Sequence[object]) -> builtins.list[str]:
        if len(candidates) == 1:
            return ["Review the selected content and run template migrate to create mutable named template main."]
        if len(candidates) > 1:
            return ["Assign an explicit name to each distinct active legacy template before migration."]
        return []
