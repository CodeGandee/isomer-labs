"""Mutable named Kaoju paper templates and non-canonical working copies."""

from __future__ import annotations

import builtins
import hashlib
import json
from pathlib import Path
import shutil
from typing import Mapping, Sequence

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.content import DIRECTORY_MANIFEST_NAME
from isomer_labs.kaoju.template_migration import (
    apply_exchange_root_migration,
    inspect_exchange_root_migration,
    inspect_latex_migration,
    legacy_content_export_paths,
    migrate_template,
)
from isomer_labs.kaoju.template_migration_support import migration_next_actions
from isomer_labs.kaoju.template_payloads import mutation_payload
from isomer_labs.kaoju.template_exchange import KaojuTemplateExchangeService
from isomer_labs.kaoju.template_support import (
    EXPORT_METADATA_NAME,
    TEMPLATE_EXCHANGE_LABEL,
    TEMPLATE_EXPORT_MANIFEST_SEMANTIC_ID,
    TEMPLATE_EXPORT_SEMANTIC_ID,
    TEMPLATE_KINDS,
    TEMPLATE_PRODUCER,
    TemplateSelection,
    _AUTHORED_METADATA_KEYS,
    _SERVICE_METADATA_KEYS,
    _atomic_write_json,
    _load_export_metadata,
    _nested_string,
    _prune_empty_parents,
    _result_ref,
    _unique_strings,
    template_tree_digest,
    validate_template_name,
    validate_template_relative_path,
)
from isomer_labs.records.index import cleanup_query_index
from isomer_labs.runtime.records import RuntimeLifecycleRecord, utc_timestamp


class KaojuTemplateService(KaojuTemplateExchangeService):
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
            "template_kind": self.template_kind.kind,
            "template_label": self.template_kind.label,
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
            "template_kind": self.template_kind.kind,
            "template_label": self.template_kind.label,
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
        export_metadata = source / EXPORT_METADATA_NAME
        if export_metadata.is_file():
            metadata = _load_export_metadata(export_metadata, expected_kind=self.template_kind.kind)
            if metadata.get("template_name") != target.name or metadata.get("canonical_ref") != target.record.id:
                raise KaojuServiceError(
                    "template_export_identity_invalid",
                    f"Edited export does not target {self.template_kind.kind}/{target.name}.",
                )
            if metadata.get("state_token") != expected_state:
                raise KaojuServiceError(
                    "template_export_state_stale",
                    "Edited export was produced from a different template state; reconcile it before updating stock.",
                )
            with self._temporary_directory("template-export-update-") as temporary:
                candidate = temporary / "candidate"
                self._copy_canonical_tree(source, candidate, allow_exchange_metadata=True)
                return self._replace_tree(
                    target,
                    candidate,
                    expected_state=expected_state,
                    authored_metadata=target.authored_metadata,
                    actor=actor,
                    operation="update-from-export",
                    source_refs=_unique_strings(source_refs),
                    change_summary=change_summary,
                )
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
        return mutation_payload(
            self.template_kind,
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
            default_working_path=str(self._default_working_path(state.name, materialize=False)),
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
            if metadata.get("template_kind", "content") != self.template_kind.kind:
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
            "template_kind": self.template_kind.kind,
            "template_label": self.template_kind.label,
            "count": len(exports),
            "exports": exports,
            "diagnostics": [],
            "next_actions": [],
        }

    def export(
        self,
        name: str | None = None,
        *,
        target: Path | None = None,
        actor: str,
    ) -> dict[str, object]:
        selection = self.resolve_selection(name=name)
        selected_target = target.resolve(strict=False) if target is not None else self._default_working_path(selection.name, materialize=True)
        self._write_export(selection, selected_target, actor=actor)
        return self._register_export_observation(selection, selected_target, actor=actor, operation="export")

    def observe_export(self, name: str, target: Path, *, actor: str) -> dict[str, object]:
        state = self._read_state(validate_template_name(name))
        selection = TemplateSelection.from_state(self.template_kind, state)
        selected_target = target.resolve(strict=False)
        working_digest = template_tree_digest(selected_target, exclude_exchange_metadata=True)
        metadata = self._export_metadata(selection, selected_target, actor=actor, exported_tree_digest=working_digest)
        _atomic_write_json(selected_target / EXPORT_METADATA_NAME, metadata)
        return self._register_export_observation(selection, selected_target, actor=actor, operation="observe")

    def promote_export(
        self,
        target: Path,
        *,
        actor: str,
        change_summary: str | None = None,
    ) -> dict[str, object]:
        """Promote one assessed edited export through create or state-checked update."""

        selected_target = target.resolve(strict=False)
        metadata = _load_export_metadata(selected_target / EXPORT_METADATA_NAME, expected_kind=self.template_kind.kind)
        name = validate_template_name(str(metadata["template_name"]))
        working_digest = template_tree_digest(selected_target, exclude_exchange_metadata=True)
        if working_digest == metadata.get("exported_tree_digest"):
            return {
                "ok": True,
                "mutated": False,
                "operation": "paper.template.promote-export",
                "template_kind": self.template_kind.kind,
                "name": name,
                "posture": "unchanged",
                "working_tree_digest": working_digest,
                "diagnostics": [],
                "next_actions": [],
            }
        with self._temporary_directory("template-export-promotion-") as temporary:
            candidate = temporary / "candidate"
            self._copy_canonical_tree(selected_target, candidate, allow_exchange_metadata=True)
            if metadata.get("selection_source") == "packaged-default":
                try:
                    self._read_state(name)
                except KaojuServiceError as exc:
                    if exc.code != "template_not_found":
                        raise
                else:
                    raise KaojuServiceError(
                        "template_export_identity_conflict",
                        f"Packaged-default export targets {self.template_kind.kind}/{name}, but topic stock now exists.",
                        ("Re-export current topic stock and reconcile the edited tree against its state token.",),
                    )
                from isomer_labs.kaoju.template_defaults import load_packaged_template

                packaged = load_packaged_template(self.template_kind)
                if (
                    metadata.get("packaged_identity") != packaged.identity
                    or metadata.get("packaged_resource_version") != packaged.resource_version
                    or metadata.get("canonical_tree_digest") != packaged.tree_digest
                ):
                    raise KaojuServiceError(
                        "template_export_packaged_source_invalid",
                        "Edited export does not match the checked packaged source identity.",
                    )
                result = self.create(
                    name,
                    source=candidate,
                    authored_metadata=packaged.authored_metadata,
                    actor=actor,
                    source_refs=(packaged.identity,),
                    change_summary=change_summary or "Promote an edited packaged-default export into topic-owned stock.",
                )
                result["promotion_source"] = "packaged-default"
                return result
            state = self._read_state(name)
            if metadata.get("canonical_ref") != state.record.id:
                raise KaojuServiceError(
                    "template_export_identity_invalid",
                    f"Edited export does not target current {self.template_kind.kind}/{name} stock.",
                )
            recorded_state = metadata.get("state_token")
            if recorded_state != state.state_token or metadata.get("canonical_tree_digest") != state.tree_digest:
                raise KaojuServiceError(
                    "template_export_state_stale",
                    f"Edited export was based on {recorded_state!r}; current state is {state.state_token!r}.",
                    ("Re-export or agentically reconcile the working tree before promotion.",),
                )
            result = self.update(
                name,
                expected_state=state.state_token,
                source=selected_target,
                actor=actor,
                change_summary=change_summary or "Promote an assessed edited topic-stock export.",
            )
            result["promotion_source"] = "topic-stock"
            return result

    def inspect_migration(self) -> dict[str, object]:
        store = self._store(read_only=True)
        try:
            records = [
                record
                for record in store.list_lifecycle_records()
                if record.topic_workspace_id == self.context.topic_workspace_id
            ]
            legacy = [
                record
                for record in records
                if record.transition_metadata.get("semantic_id") == self.template_kind.semantic_id
                and not self._is_named_template_record(record)
            ]
        finally:
            store.close()
        if self.template_kind.kind == "latex":
            return inspect_latex_migration(self, records)
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
        content_records = [
            {
                "record_id": record.id,
                "template_name": record.transition_metadata.get("template_name"),
                "stable_ref": record.id,
                "state_token": record.transition_metadata.get("state_token"),
                "tree_digest": record.transition_metadata.get("tree_digest"),
                "contract_current": record.transition_metadata.get("template_kind") == "content",
            }
            for record in records
            if self._is_named_template_record(record)
        ]
        legacy_export_paths = legacy_content_export_paths(self)
        proposed_mutations = [
            {
                "operation": "annotate-content-template-kind",
                "record_id": str(item["record_id"]),
                "preserve_stable_ref": True,
                "preserve_tree_bytes": True,
            }
            for item in content_records
            if item["contract_current"] is False
        ]
        proposed_mutations.extend(
            {
                "operation": "adopt-legacy-content",
                "source_ref": str(item["record_id"]),
                "requires_explicit_name": len(candidates) > 1,
            }
            for item in candidates
        )
        return {
            "ok": True,
            "mutated": False,
            "operation": "paper.template.migrate.inspect",
            "template_kind": self.template_kind.kind,
            "template_label": self.template_kind.label,
            "content_records": content_records,
            "legacy_export_paths": legacy_export_paths,
            "legacy_export_compatibility": [
                {
                    "path": path,
                    "template_kind": "content",
                    "compatibility_source": "legacy-unqualified-content-export",
                }
                for path in legacy_export_paths
            ],
            "proposed_mutations": proposed_mutations,
            "active_candidates": candidates,
            "historical_record_ids": sorted(historical),
            "versioned_export_paths": versioned_exports,
            "legacy_latex_paths": self._legacy_latex_paths(),
            "diagnostics": [],
            "next_actions": migration_next_actions(candidates),
        }

    def inspect_exchange_root_migration(self) -> dict[str, object]:
        """Preview the singular-to-plural exchange-root migration."""

        return inspect_exchange_root_migration(self)

    def migrate_exchange_root(
        self,
        *,
        actor: str,
        expected_preview: str,
    ) -> dict[str, object]:
        """Apply one exact exchange-root migration preview."""

        return apply_exchange_root_migration(
            self,
            actor=actor,
            expected_preview=expected_preview,
        )

    def migrate(
        self,
        *,
        record_id: str | None = None,
        name: str | None = None,
        actor: str,
        authored_metadata: Mapping[str, object] | None = None,
        expected_state: str | None = None,
    ) -> dict[str, object]:
        return migrate_template(
            self,
            record_id=record_id,
            name=name,
            actor=actor,
            authored_metadata=authored_metadata,
            expected_state=expected_state,
        )

    def _register_export_observation(
        self,
        selection: TemplateSelection,
        target: Path,
        *,
        actor: str,
        operation: str,
    ) -> dict[str, object]:
        metadata = _load_export_metadata(target / EXPORT_METADATA_NAME, expected_kind=self.template_kind.kind)
        idempotency = hashlib.sha256(
            json.dumps(
                {
                    "operation": operation,
                    "template_kind": self.template_kind.kind,
                    "path": str(target),
                    "selection_source": selection.selection_source,
                    "source_identity": selection.stable_ref or selection.packaged_identity,
                    "state_token": selection.state_token,
                    "exported_tree_digest": metadata.get("exported_tree_digest"),
                },
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()
        export_result = self.artifacts.put(
            TEMPLATE_EXPORT_SEMANTIC_ID,
            target,
            producer=TEMPLATE_PRODUCER,
            scope_key=selection.name,
            relationships=[
                {
                    "role": "paper_template",
                    "target_ref": selection.stable_ref or str(selection.packaged_identity),
                }
            ],
            idempotency_key=f"paper-template-export:{self.template_kind.kind}:{idempotency}",
            external=True,
            metadata={**metadata, "observation_operation": operation},
        )
        export_ref = _result_ref(export_result)
        with self._temporary_directory("template-export-manifest-") as temporary:
            payload_path = temporary / "template-export-manifest.json"
            payload = {
                "title": f"{self.template_kind.label.title()} export {selection.name}",
                "summary": f"Registered non-canonical named {self.template_kind.label} working-copy observation.",
                "artifact_family": "kaoju",
                "semantic_id": TEMPLATE_EXPORT_MANIFEST_SEMANTIC_ID,
                "artifact_type": "paper-template-manifest",
                "sections": {
                    "export": {"ref": export_ref, "operation": operation, "canonical": False},
                    "source": selection.to_json(),
                    "tree": {
                        "canonical_digest": selection.tree_digest,
                        "exported_digest": metadata.get("exported_tree_digest"),
                    },
                    "actor": {"ref": actor, "observed_at": metadata.get("observed_at"), "path": str(target)},
                },
            }
            _atomic_write_json(payload_path, payload)
            manifest_result = self.artifacts.put(
                TEMPLATE_EXPORT_MANIFEST_SEMANTIC_ID,
                payload_path,
                producer=TEMPLATE_PRODUCER,
                scope_key=selection.name,
                relationships=[
                    {"role": "template_export", "target_ref": export_ref},
                    {
                        "role": "paper_template",
                        "target_ref": selection.stable_ref or str(selection.packaged_identity),
                    },
                ],
                idempotency_key=f"paper-template-export-manifest:{self.template_kind.kind}:{idempotency}",
                metadata={**metadata, "observation_operation": operation},
            )
        manifest_ref = _result_ref(manifest_result)
        return {
            "ok": True,
            "mutated": True,
            "operation": f"paper.template.{operation}",
            "template_kind": self.template_kind.kind,
            "template_label": self.template_kind.label,
            "name": selection.name,
            "selection_source": selection.selection_source,
            "stable_ref": selection.stable_ref,
            "state_token": selection.state_token,
            "packaged_identity": selection.packaged_identity,
            "packaged_resource_version": selection.packaged_resource_version,
            "tree_digest": selection.tree_digest,
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
        root = self._exchange_base_root(materialize=False)
        if not root.is_dir():
            return []
        reserved = {spec.exchange_subdirectory for spec in TEMPLATE_KINDS.values()}
        markers = ("template.tex", "main.tex", "latexmkrc")
        return sorted(
            str(path)
            for path in root.iterdir()
            if path.is_dir() and path.name not in reserved and any((path / marker).exists() for marker in markers)
        )
