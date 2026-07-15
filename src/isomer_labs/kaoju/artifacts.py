"""Typed Kaoju Artifact service over Workspace Runtime research records."""

from __future__ import annotations

import builtins
from dataclasses import dataclass
from pathlib import Path
import shutil
from typing import Mapping, Sequence
import uuid

from isomer_labs.core.artifact_identity import ArtifactIdentityError, parse_artifact_identity
from isomer_labs.kaoju.content import (
    ArtifactContent,
    checksum_file,
    create_managed_directory_artifact,
    directory_manifest,
    manifest_checksum,
    register_canonical_repository,
    register_external_path,
    register_ordinary_file,
    register_structured_file,
    validate_directory_manifest,
)
from isomer_labs.kaoju.contracts import KaojuBinding, describe_binding, load_binding_registry
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.index import query_index_list, refresh_query_index_for_record
from isomer_labs.records.store import (
    ResearchRecordError,
    ResearchRecordRequest,
    archive_record,
    create_record,
    list_records,
    revise_record,
    show_record,
)
from isomer_labs.runtime.records import RuntimeLifecycleRecord, utc_timestamp
from isomer_labs.runtime.store import open_workspace_runtime
from isomer_labs.kaoju.survey import ContractDiagnostic, diagnostic_errors, validate_structured_artifact


@dataclass(frozen=True)
class KaojuServiceError(Exception):
    """Stable service error with recovery actions."""

    code: str
    message: str
    recovery_actions: tuple[str, ...] = ()

    def __str__(self) -> str:
        return self.message

    def payload(self) -> dict[str, object]:
        return {
            "ok": False,
            "mutated": False,
            "error": {"code": self.code, "message": self.message},
            "recovery_actions": list(self.recovery_actions),
        }


class KaojuArtifactService:
    """Resolve binding inference and persist one topic's Kaoju Artifacts."""

    def __init__(self, context: EffectiveTopicContext, *, env: Mapping[str, str], cwd: Path) -> None:
        self.context = context
        self.env = env
        self.cwd = cwd

    def describe(self, semantic_id: str) -> dict[str, object]:
        try:
            binding = describe_binding(semantic_id)
        except ArtifactIdentityError as exc:
            raise KaojuServiceError(exc.code, str(exc)) from exc
        except KeyError as exc:
            raise KaojuServiceError("unknown_semantic_id", str(exc), ("List the packaged Kaoju binding registry.",)) from exc
        return {"ok": True, "mutated": False, "operation": "describe", "binding": binding}

    def put(
        self,
        semantic_id: str,
        content: Path,
        *,
        producer: str,
        scope_key: str | None = None,
        record_id: str | None = None,
        status: str = "ready",
        relationships: list[dict[str, object]] | None = None,
        idempotency_key: str | None = None,
        external: bool = False,
        repository_remote: str | None = None,
        repository_commit: str | None = None,
        repository_depth: int | None = None,
    ) -> dict[str, object]:
        binding = self._binding(semantic_id)
        self._authorize(binding, producer)
        self._validate_status(binding, status)
        self._validate_scope(binding, scope_key)
        self._validate_relationships(binding, relationships or [])
        contract_diagnostics = self._validate_content_contract(binding, content)
        if idempotency_key is not None:
            existing = self._idempotent_record(idempotency_key)
            if existing is not None:
                return {"ok": True, "mutated": False, "operation": "put", "idempotent_replay": True, "record": existing.to_json(), "affected_refs": [existing.id]}
        selected_id = record_id or f"artifact-{binding.artifact_type}-{uuid.uuid4().hex[:12]}"
        prepared = self._prepare_content(
            binding,
            content,
            record_id=selected_id,
            external=external,
            repository_remote=repository_remote,
            repository_commit=repository_commit,
            repository_depth=repository_depth,
        )
        request = self._request(
            binding,
            prepared,
            producer=producer,
            scope_key=scope_key,
            record_id=selected_id,
            status=status,
            relationships=relationships or [],
            idempotency_key=idempotency_key,
            contract_diagnostics=contract_diagnostics,
        )
        try:
            payload, diagnostics = create_record(self.context, request, env=self.env, cwd=self.cwd)
        except ResearchRecordError as exc:
            cleanup = _discard_uncommitted_managed_directory(prepared)
            raise KaojuServiceError(exc.code, exc.message, tuple(_string_values(exc.payload.get("recovery_actions"))) + cleanup) from exc
        if payload.get("ok") is False:
            _discard_uncommitted_managed_directory(prepared)
            raise KaojuServiceError("artifact_put_failed", "Artifact creation failed validation.", tuple(item.message for item in diagnostics))
        return {
            **payload,
            "operation": "put",
            "semantic_id": semantic_id,
            "scope_key": scope_key,
            "content_mode": binding.content_mode,
            "affected_refs": [selected_id],
            "contract_diagnostics": [diagnostic.to_json() for diagnostic in contract_diagnostics],
            "recovery_actions": [],
        }

    def revise(
        self,
        record_id: str,
        content: Path,
        *,
        producer: str,
        scope_key: str | None = None,
        new_record_id: str | None = None,
        relationships: list[dict[str, object]] | None = None,
        idempotency_key: str | None = None,
    ) -> dict[str, object]:
        shown, _diagnostics = show_record(self.context, record_id, env=self.env)
        record = shown.get("record")
        if not isinstance(record, dict):
            raise KaojuServiceError("artifact_not_found", f"Artifact record not found: {record_id}")
        metadata = record.get("transition_metadata")
        semantic_id = metadata.get("semantic_id") if isinstance(metadata, dict) else None
        if not isinstance(semantic_id, str):
            raise KaojuServiceError("artifact_binding_missing", f"Record {record_id} has no semantic binding.")
        binding = self._binding(semantic_id)
        if binding.revision_mode in {"append_only", "immutable"}:
            raise KaojuServiceError("artifact_revision_forbidden", f"{semantic_id} uses {binding.revision_mode} behavior; create a distinct record instead.")
        self._authorize(binding, producer)
        self._validate_relationships(binding, relationships or [])
        contract_diagnostics = self._validate_content_contract(binding, content)
        inherited_scope = metadata.get("scope_key") if isinstance(metadata, dict) else None
        selected_scope = scope_key or (inherited_scope if isinstance(inherited_scope, str) else None)
        self._validate_scope(binding, selected_scope)
        selected_id = new_record_id or f"artifact-{binding.artifact_type}-{uuid.uuid4().hex[:12]}"
        prepared = self._prepare_content(binding, content, record_id=selected_id, external=False, repository_remote=None, repository_commit=None, repository_depth=None)
        request = self._request(
            binding,
            prepared,
            producer=producer,
            scope_key=selected_scope,
            record_id=selected_id,
            status="ready",
            relationships=relationships or [],
            idempotency_key=idempotency_key,
            contract_diagnostics=contract_diagnostics,
        )
        payload, diagnostics = revise_record(self.context, record_id, request, env=self.env, cwd=self.cwd)
        if payload.get("ok") is False:
            raise KaojuServiceError("artifact_revise_failed", "Artifact revision failed validation.", tuple(item.message for item in diagnostics))
        return {**payload, "operation": "revise", "semantic_id": semantic_id, "scope_key": selected_scope, "content_mode": binding.content_mode, "affected_refs": [selected_id], "contract_diagnostics": [diagnostic.to_json() for diagnostic in contract_diagnostics]}

    def latest(self, semantic_id: str, *, scope_key: str | None = None) -> dict[str, object]:
        binding = self._binding(semantic_id)
        self._validate_scope(binding, scope_key, for_query=True)
        payload, _diagnostics = query_index_list(
            self.context,
            env=self.env,
            artifact_family="kaoju",
            semantic_id=semantic_id,
            scope_key=scope_key,
            unscoped_only=scope_key is None,
            latest_only=True,
        )
        ambiguous = [item for item in _dict_list(payload.get("diagnostics")) if item.get("code") == "query_index_latest_ambiguous"]
        if ambiguous:
            record_ids = [str(record.get("record_id")) for record in _dict_list(payload.get("records"))]
            raise KaojuServiceError("artifact_latest_ambiguous", f"Current Artifact selection is ambiguous for {semantic_id} in scope {scope_key or '<legacy-unscoped>'}: {', '.join(record_ids)}.", ("Supply a scope key.", "Archive or supersede the competing record."))
        return {**payload, "operation": "latest", "scope_key": scope_key, "binding_revision_mode": binding.revision_mode}

    def list(self, *, semantic_id: str | None = None, scope_key: str | None = None, status: str | None = None) -> dict[str, object]:
        payload, _diagnostics = list_records(self.context, env=self.env, semantic_id=semantic_id, scope_key=scope_key, status=status)
        return payload

    def show(self, record_id: str, *, include_content: bool = False) -> dict[str, object]:
        payload, _diagnostics = show_record(self.context, record_id, env=self.env, include_body=include_content, include_payload=include_content)
        payload["content_diagnostics"] = self.content_diagnostics(payload)
        return payload

    def archive(self, record_id: str, *, reason: str | None = None) -> dict[str, object]:
        payload, _diagnostics = archive_record(self.context, record_id, env=self.env, reason=reason)
        return payload

    def content_diagnostics(self, shown: dict[str, object]) -> builtins.list[dict[str, object]]:
        record = shown.get("record")
        if not isinstance(record, dict):
            return []
        content_path = record.get("content_path")
        metadata = record.get("transition_metadata")
        artifact_content = metadata.get("artifact_content") if isinstance(metadata, dict) else None
        if not isinstance(content_path, str) or not isinstance(artifact_content, dict):
            return []
        path = Path(content_path)
        if not path.exists():
            return [{"severity": "error", "code": "artifact_content_missing", "message": "Recorded Artifact content is missing.", "record_id": record.get("id")}]
        locator_kind = artifact_content.get("locator_kind")
        if locator_kind == "managed_directory_manifest":
            return validate_directory_manifest(path)
        if locator_kind == "external_directory" and path.is_dir():
            try:
                current = manifest_checksum(directory_manifest(path, locator_posture="external"))
            except ValueError as exc:
                return [{"severity": "error", "code": "artifact_content_corrupt", "message": str(exc), "record_id": record.get("id")}]
            if artifact_content.get("checksum") != current:
                return [{"severity": "error", "code": "artifact_content_stale", "message": "External Artifact directory changed after registration.", "record_id": record.get("id")}]
        if path.is_file() and artifact_content.get("checksum") != checksum_file(path):
            return [{"severity": "error", "code": "artifact_content_corrupt", "message": "Recorded Artifact checksum does not match content.", "record_id": record.get("id")}]
        return []

    def backfill_scope_keys(self, *, apply: bool = False) -> dict[str, object]:
        """Backfill only unambiguous legacy scope values from explicit metadata fields."""

        store, diagnostics = open_workspace_runtime(self.context, env=self.env, read_only=not apply)
        if store is None:
            raise KaojuServiceError("workspace_runtime_missing", "Workspace Runtime is unavailable.", tuple(item.message for item in diagnostics))
        changes: builtins.list[dict[str, str]] = []
        skipped: builtins.list[dict[str, object]] = []
        fields = ("direction_id", "source_id", "paper_line", "export_target", "environment_id", "trial_id", "survey_id")
        try:
            for record in store.list_lifecycle_records():
                if record.topic_workspace_id != self.context.topic_workspace_id or record.transition_metadata.get("scope_key"):
                    continue
                semantic_id = record.transition_metadata.get("semantic_id")
                binding = load_binding_registry().get(str(semantic_id))
                if binding is None or binding.scope_key_policy["mode"] == "none":
                    continue
                candidates = {str(record.transition_metadata[field]) for field in fields if isinstance(record.transition_metadata.get(field), str) and record.transition_metadata[field]}
                if len(candidates) != 1:
                    skipped.append({"record_id": record.id, "reason": "scope_not_unambiguous", "candidates": sorted(candidates)})
                    continue
                scope_key = next(iter(candidates))
                changes.append({"record_id": record.id, "scope_key": scope_key})
                if apply:
                    updated = RuntimeLifecycleRecord(**{**record.__dict__, "updated_at": utc_timestamp(), "transition_metadata": {**record.transition_metadata, "scope_key": scope_key, "scope_backfill": "explicit_metadata"}})
                    with store.connection:
                        store.upsert_lifecycle_record(updated)
                    refresh_query_index_for_record(self.context, store, record.id)
        finally:
            store.close()
        return {"ok": True, "mutated": apply and bool(changes), "operation": "migrate-scope", "apply": apply, "changes": changes, "skipped": skipped}

    def _binding(self, semantic_id: str) -> KaojuBinding:
        try:
            parse_artifact_identity(semantic_id, expected_extension="kaoju")
        except ArtifactIdentityError as exc:
            raise KaojuServiceError(exc.code, str(exc)) from exc
        binding = load_binding_registry().get(semantic_id)
        if binding is None:
            raise KaojuServiceError("unknown_semantic_id", f"Unknown Kaoju semantic id: {semantic_id}")
        return binding

    def _authorize(self, binding: KaojuBinding, producer: str) -> None:
        if producer != binding.producer:
            raise KaojuServiceError("artifact_producer_rejected", f"Producer {producer!r} is not authorized for {binding.semantic_id}; expected {binding.producer!r}.")

    def _validate_scope(self, binding: KaojuBinding, scope_key: str | None, *, for_query: bool = False) -> None:
        mode = binding.scope_key_policy["mode"]
        if mode == "required" and not scope_key and not for_query:
            raise KaojuServiceError("artifact_scope_required", f"{binding.semantic_id} requires a {binding.scope_key_policy['dimension']} scope key.")
        if mode == "none" and scope_key and not for_query:
            raise KaojuServiceError("artifact_scope_forbidden", f"{binding.semantic_id} is topic-scoped and does not accept a scope key.")

    def _validate_relationships(self, binding: KaojuBinding, relationships: Sequence[dict[str, object]]) -> None:
        supplied = {str(item.get("role")) for item in relationships if item.get("role")}
        missing = sorted(set(binding.relationships) - supplied)
        if missing:
            raise KaojuServiceError("artifact_relationship_missing", f"{binding.semantic_id} requires relationship roles: {', '.join(missing)}.")
        unknown = sorted(supplied - set(binding.relationships))
        if unknown:
            raise KaojuServiceError("artifact_relationship_unknown", f"{binding.semantic_id} does not define relationship roles: {', '.join(unknown)}.")
        for index, relationship in enumerate(relationships):
            targets = [relationship.get(field) for field in ("target_record_id", "target_ref", "record_id")]
            if not any(isinstance(value, str) and value.strip() for value in targets):
                raise KaojuServiceError("artifact_relationship_ref_invalid", f"Relationship {index} for {binding.semantic_id} requires a non-empty target ref.")

    def _validate_status(self, binding: KaojuBinding, status: str) -> None:
        accepted = tuple(str(value) for value in binding.acceptance.get("statuses", ()))
        if status not in accepted:
            raise KaojuServiceError("artifact_status_invalid", f"Status {status!r} is not accepted for {binding.semantic_id}; expected one of: {', '.join(accepted)}.")

    def _validate_content_contract(self, binding: KaojuBinding, content: Path) -> builtins.list[ContractDiagnostic]:
        contract_path = content
        if binding.semantic_id == "KAOJU:GENERATED-DATASET" and binding.content_mode == "directory_manifest":
            contract_path = content / "generated-dataset.json"
            if not contract_path.is_file():
                raise KaojuServiceError(
                    "artifact_contract_invalid",
                    "KAOJU:GENERATED-DATASET requires generated-dataset.json at the directory root.",
                    ("Write the capability-probe manifest and retry registration.",),
                )
        elif binding.content_mode != "structured_file":
            return []
        _payload, diagnostics = validate_structured_artifact(contract_path, binding.semantic_id)
        errors = diagnostic_errors(diagnostics)
        if errors:
            detail = "; ".join(f"{diagnostic.location}: {diagnostic.message}" for diagnostic in errors)
            raise KaojuServiceError("artifact_contract_invalid", f"{binding.semantic_id} content violates its semantic contract: {detail}")
        return diagnostics

    def _prepare_content(
        self,
        binding: KaojuBinding,
        content: Path,
        *,
        record_id: str,
        external: bool,
        repository_remote: str | None,
        repository_commit: str | None,
        repository_depth: int | None,
    ) -> ArtifactContent:
        try:
            if binding.content_mode == "structured_file":
                return register_structured_file(content)
            if binding.content_mode == "ordinary_file":
                return register_external_path(content) if external else register_ordinary_file(content)
            if binding.content_mode == "directory_manifest":
                return register_external_path(content) if external else create_managed_directory_artifact(self.context, content, semantic_label=binding.semantic_label, record_kind=binding.record_kind, record_id=record_id, env=self.env, cwd=self.cwd)
            if binding.content_mode == "external_path":
                return register_external_path(content)
            if repository_remote is None or repository_commit is None:
                raise ValueError("Canonical repository content requires remote URL and immutable commit.")
            return register_canonical_repository(content, remote_url=repository_remote, commit=repository_commit, depth=repository_depth)
        except ValueError as exc:
            raise KaojuServiceError("artifact_content_invalid", str(exc)) from exc

    def _request(
        self,
        binding: KaojuBinding,
        content: ArtifactContent,
        *,
        producer: str,
        scope_key: str | None,
        record_id: str,
        status: str,
        relationships: Sequence[dict[str, object]],
        idempotency_key: str | None,
        contract_diagnostics: Sequence[ContractDiagnostic],
    ) -> ResearchRecordRequest:
        metadata: dict[str, object] = {
            "artifact_type": binding.artifact_type,
            "content_mode": binding.content_mode,
            "artifact_content": content.metadata(),
            "binding_schema_version": "isomer-kaoju-binding-registry.v2",
            "accepted_statuses": list(binding.acceptance["statuses"]),
            "contract_diagnostics": [diagnostic.to_json() for diagnostic in contract_diagnostics],
            "relationships": [dict(relationship) for relationship in relationships],
        }
        if idempotency_key is not None:
            metadata["idempotency_key"] = idempotency_key
        if binding.content_mode == "structured_file":
            return ResearchRecordRequest(record_kind=binding.record_kind, record_id=record_id, status=status, semantic_id=binding.semantic_id, scope_key=scope_key, skill=producer, producer=producer, consumer=",".join(binding.consumers), semantic_label=binding.semantic_label, metadata=metadata, relationships=list(relationships), payload_file=content.content_path, format_profile_ref=binding.profile_ref)
        if content.managed and binding.content_mode == "ordinary_file":
            return ResearchRecordRequest(record_kind=binding.record_kind, record_id=record_id, status=status, semantic_id=binding.semantic_id, scope_key=scope_key, skill=producer, producer=producer, consumer=",".join(binding.consumers), semantic_label=binding.semantic_label, metadata=metadata, relationships=list(relationships), body_file=content.content_path, content_name=content.content_path.name)
        return ResearchRecordRequest(record_kind=binding.record_kind, record_id=record_id, status=status, semantic_id=binding.semantic_id, scope_key=scope_key, skill=producer, producer=producer, consumer=",".join(binding.consumers), semantic_label=binding.semantic_label, metadata=metadata, relationships=list(relationships), registered_content_path=content.content_path)

    def _idempotent_record(self, key: str) -> RuntimeLifecycleRecord | None:
        store, diagnostics = open_workspace_runtime(self.context, env=self.env, read_only=True)
        if store is None:
            raise KaojuServiceError("workspace_runtime_missing", "Workspace Runtime is unavailable.", tuple(item.message for item in diagnostics))
        try:
            matches = [record for record in store.list_lifecycle_records() if record.topic_workspace_id == self.context.topic_workspace_id and record.transition_metadata.get("idempotency_key") == key]
        finally:
            store.close()
        if len(matches) > 1:
            raise KaojuServiceError("artifact_idempotency_conflict", f"Idempotency key {key!r} resolves to multiple records.")
        return matches[0] if matches else None


def _dict_list(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _discard_uncommitted_managed_directory(content: ArtifactContent) -> tuple[str, ...]:
    if content.locator_kind != "managed_directory_manifest":
        return ()
    owner = content.content_path.parent.parent
    try:
        shutil.rmtree(owner)
        return (f"Removed uncommitted managed content at {owner}.",)
    except OSError as exc:
        return (f"Uncommitted managed content may remain at {owner}: {exc}",)


def _string_values(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value]
