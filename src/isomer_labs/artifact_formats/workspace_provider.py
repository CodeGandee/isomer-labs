"""Workspace Runtime-backed Artifact Format provider and registration helpers."""

from __future__ import annotations

import json
from pathlib import Path
import shutil
from typing import Literal

from jsonschema import SchemaError, validators  # type: ignore[import-untyped]

from isomer_labs.artifact_formats.models import (
    ArtifactFormatResolution,
    artifact_format_diagnostic,
    digest_bytes,
    validate_format_ref,
)
from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.identifiers import _provenance_ref, _slug
from isomer_labs.runtime.models import ArtifactFormatRegistrationRecord, utc_timestamp
from isomer_labs.runtime.store import WorkspaceRuntimeStore


class WorkspaceRuntimeArtifactFormatProvider:
    """Resolve topic-scoped custom Artifact Format refs from Workspace Runtime."""

    provider_id = "workspace-runtime.custom-artifact-formats"

    def __init__(self, store: WorkspaceRuntimeStore, *, topic_workspace_id: str) -> None:
        self.store = store
        self.topic_workspace_id = topic_workspace_id

    def resolve_profile(self, ref: str) -> ArtifactFormatResolution | None:
        registration = self.store.get_artifact_format_registration(
            topic_workspace_id=self.topic_workspace_id,
            format_profile_ref=ref,
        )
        if registration is None:
            return None
        content = json.dumps(registration.profile_json, indent=2, sort_keys=True)
        return ArtifactFormatResolution(
            ref=ref,
            kind="profile",
            source_kind=registration.source_kind,  # type: ignore[arg-type]
            content=content,
            digest=registration.profile_digest,
        )

    def resolve_schema(self, ref: str) -> ArtifactFormatResolution | None:
        registration = self._registration_for_ref(ref, "schema")
        if registration is None or registration.schema_snapshot_path is None:
            return None
        return _snapshot_resolution(ref, "schema", registration.schema_snapshot_path, registration.source_kind)

    def resolve_template(self, ref: str) -> ArtifactFormatResolution | None:
        registration = self._registration_for_ref(ref, "template")
        if registration is None or registration.template_snapshot_path is None:
            return None
        return _snapshot_resolution(ref, "template", registration.template_snapshot_path, registration.source_kind)

    def _registration_for_ref(
        self,
        ref: str,
        kind: Literal["schema", "template"],
    ) -> ArtifactFormatRegistrationRecord | None:
        for registration in self.store.list_artifact_format_registrations(topic_workspace_id=self.topic_workspace_id):
            if kind == "schema" and registration.schema_ref == ref:
                return registration
            if kind == "template" and registration.template_ref == ref:
                return registration
        return None


def register_custom_artifact_format(
    store: WorkspaceRuntimeStore,
    context: EffectiveTopicContext,
    *,
    format_profile_ref: str,
    schema_file: Path,
    template_file: Path | None,
    output_format: str = "markdown",
    actor_ref: str | None = None,
    provenance_refs: list[str] | None = None,
    replace: bool = False,
    source_kind: Literal["runtime_registration", "file_snapshot"] = "runtime_registration",
) -> tuple[ArtifactFormatRegistrationRecord | None, list[Diagnostic]]:
    """Copy custom format assets into managed runtime storage and persist refs."""

    diagnostics = _custom_profile_ref_diagnostics(format_profile_ref)
    existing = store.get_artifact_format_registration(
        topic_workspace_id=context.topic_workspace_id,
        format_profile_ref=format_profile_ref,
    )
    if existing is not None and not replace:
        diagnostics.append(
            artifact_format_diagnostic(
                "ISO206",
                "error",
                "Artifact Format Registration",
                f"Custom Artifact Format ref already exists in this Topic Workspace: {format_profile_ref}.",
                field="format_profile_ref",
            )
        )
    schema_content, schema_diagnostics = _read_schema_file(schema_file)
    diagnostics.extend(schema_diagnostics)
    template_content: str | None = None
    if template_file is not None:
        template_content, template_diagnostics = _read_text_file(
            template_file,
            concept="Artifact Format Template",
            field="template_file",
        )
        diagnostics.extend(template_diagnostics)
    if has_errors(diagnostics) or schema_content is None:
        return None, diagnostics

    schema_ref = related_custom_ref(format_profile_ref, "schema")
    template_ref = related_custom_ref(format_profile_ref, "template", output_format=output_format) if template_file is not None else None
    root = context.topic_workspace_path / "runtime" / "artifact-formats"
    schema_target = root / "schemas" / f"{_slug(format_profile_ref)}.schema.json"
    schema_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(schema_file, schema_target)
    template_target: Path | None = None
    if template_file is not None:
        template_target = root / "templates" / output_format / f"{_slug(format_profile_ref)}.{_template_extension(output_format)}.j2"
        template_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(template_file, template_target)
    now = utc_timestamp()
    profile: dict[str, object] = {
        "schema_ref": schema_ref,
        "templates": {output_format: template_ref} if template_ref is not None else {},
        "media_type": "application/json",
        "schema_version": "custom-structured-record.v1",
        "compatibility_version": "v1",
        "status": "active",
        "metadata": {
            "source_kind": source_kind,
            "original_schema_path": str(schema_file.resolve(strict=False)),
        },
    }
    if template_file is not None:
        metadata = profile["metadata"]
        if isinstance(metadata, dict):
            metadata["original_template_path"] = str(template_file.resolve(strict=False))
    profile_content = json.dumps(profile, sort_keys=True, separators=(",", ":"))
    record = ArtifactFormatRegistrationRecord(
        id=f"artifact-format-registration-{_slug(format_profile_ref)}",
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        format_profile_ref=format_profile_ref,
        schema_ref=schema_ref,
        template_ref=template_ref,
        output_format=output_format,
        source_kind=source_kind,
        profile_json=profile,
        schema_snapshot_path=str(schema_target.resolve(strict=False)),
        template_snapshot_path=str(template_target.resolve(strict=False)) if template_target is not None else None,
        original_schema_path=str(schema_file.resolve(strict=False)),
        original_template_path=str(template_file.resolve(strict=False)) if template_file is not None else None,
        profile_digest=digest_bytes(profile_content.encode("utf-8")),
        schema_digest=digest_bytes(schema_content.encode("utf-8")),
        template_digest=digest_bytes(template_content.encode("utf-8")) if template_content is not None else None,
        diagnostics=[],
        actor_ref=actor_ref,
        created_at=existing.created_at if existing is not None else now,
        updated_at=now,
        provenance_refs=provenance_refs or [_provenance_ref("artifact-format-registration", format_profile_ref)],
    )
    with store.connection:
        store.upsert_artifact_format_registration(record)
    stored = store.get_artifact_format_registration(
        topic_workspace_id=context.topic_workspace_id,
        format_profile_ref=format_profile_ref,
    )
    return stored or record, diagnostics


def related_custom_ref(format_profile_ref: str, kind: str, *, output_format: str = "markdown") -> str:
    prefix = "custom:"
    if not format_profile_ref.startswith(prefix):
        raise ValueError("Custom Artifact Format ref must start with custom:.")
    origin, path = format_profile_ref.split(":", 1)
    parts = path.split("/")
    if len(parts) < 4 or parts[1] != "record-format" or parts[2] != "profile":
        raise ValueError("Custom profile ref must use custom:<topic-slug>/record-format/profile/.../v1.")
    if kind == "schema":
        next_parts = [parts[0], "record-format", "schema", *parts[3:]]
    elif kind == "template":
        next_parts = [parts[0], "record-format", "template", output_format, *parts[3:]]
    else:
        raise ValueError(f"Unsupported custom Artifact Format related ref kind: {kind}")
    return f"{origin}:{'/'.join(next_parts)}"


def _custom_profile_ref_diagnostics(format_profile_ref: str) -> list[Diagnostic]:
    diagnostics = validate_format_ref(format_profile_ref, field="format_profile_ref")
    if diagnostics:
        return diagnostics
    if not format_profile_ref.startswith("custom:"):
        return [
            artifact_format_diagnostic(
                "ISO206",
                "error",
                "Artifact Format Registration",
                "Custom Artifact Format registration requires a custom: format profile ref.",
                field="format_profile_ref",
            )
        ]
    parts = format_profile_ref.split(":", 1)[1].split("/")
    if len(parts) < 5 or parts[1] != "record-format" or parts[2] != "profile" or parts[-1] != "v1":
        return [
            artifact_format_diagnostic(
                "ISO206",
                "error",
                "Artifact Format Registration",
                "Custom format profile refs must use custom:<topic-slug>/record-format/profile/.../v1.",
                field="format_profile_ref",
            )
        ]
    return []


def _read_schema_file(path: Path) -> tuple[str | None, list[Diagnostic]]:
    content, diagnostics = _read_text_file(path, concept="Artifact Format Schema", field="schema_file")
    if content is None:
        return None, diagnostics
    try:
        schema = json.loads(content)
    except json.JSONDecodeError as exc:
        diagnostics.append(
            artifact_format_diagnostic(
                "ISO206",
                "error",
                "Artifact Format Schema",
                f"Custom schema file is not valid JSON: {exc.msg}.",
                path=path,
                field="schema_file",
            )
        )
        return None, diagnostics
    if not isinstance(schema, dict):
        diagnostics.append(
            artifact_format_diagnostic(
                "ISO206",
                "error",
                "Artifact Format Schema",
                "Custom schema file must contain a JSON object.",
                path=path,
                field="schema_file",
            )
        )
        return None, diagnostics
    try:
        validators.validator_for(schema).check_schema(schema)
    except SchemaError as exc:
        diagnostics.append(
            artifact_format_diagnostic(
                "ISO206",
                "error",
                "Artifact Format Schema",
                f"Custom schema file is not a valid JSON Schema: {exc.message}.",
                path=path,
                field="schema_file",
            )
        )
    return content, diagnostics


def _read_text_file(path: Path, *, concept: str, field: str) -> tuple[str | None, list[Diagnostic]]:
    try:
        return path.read_text(encoding="utf-8"), []
    except OSError as exc:
        return None, [
            artifact_format_diagnostic(
                "ISO206",
                "error",
                concept,
                f"File could not be read: {exc}.",
                path=path,
                field=field,
            )
        ]


def _snapshot_resolution(
    ref: str,
    kind: str,
    snapshot_path: str,
    source_kind: str,
) -> ArtifactFormatResolution | None:
    path = Path(snapshot_path)
    if not path.exists():
        return None
    content = path.read_text(encoding="utf-8")
    return ArtifactFormatResolution(
        ref=ref,
        kind=kind,  # type: ignore[arg-type]
        source_kind=source_kind,  # type: ignore[arg-type]
        content=content,
        digest=digest_bytes(content.encode("utf-8")),
        path=path,
    )


def _template_extension(output_format: str) -> str:
    if output_format == "markdown":
        return "md"
    return _slug(output_format)
