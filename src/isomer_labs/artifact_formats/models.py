"""Models for generic Artifact Format processing."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Literal, Mapping

from isomer_labs.diagnostics import Diagnostic


FORMAT_REF_ORIGINS = ("isomer", "custom")
FORMAT_REF_SEGMENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
SourceKind = Literal["provider_asset", "runtime_registration", "plain_file", "file_snapshot"]


@dataclass(frozen=True)
class ArtifactFormatRef:
    """Origin-prefixed Artifact Format ref."""

    origin: Literal["isomer", "custom"]
    parts: tuple[str, ...]

    @property
    def text(self) -> str:
        return f"{self.origin}:{'/'.join(self.parts)}"

    @property
    def owner_slug(self) -> str:
        return self.parts[0]

    def __str__(self) -> str:
        return self.text


@dataclass(frozen=True)
class ArtifactFormatProfile:
    """Declarative content expectations for one Artifact format."""

    ref: str
    schema_ref: str
    templates: dict[str, str] = field(default_factory=dict)
    media_type: str | None = None
    schema_version: str | None = None
    compatibility_version: str | None = None
    status: str | None = None
    validation_hints: dict[str, object] = field(default_factory=dict)
    renderer_hints: dict[str, object] = field(default_factory=dict)
    metadata: dict[str, object] = field(default_factory=dict)

    @classmethod
    def from_mapping(cls, ref: str, raw: Mapping[str, Any]) -> tuple["ArtifactFormatProfile" | None, list[Diagnostic]]:
        diagnostics = validate_format_ref(ref, field="profile_ref")
        schema_ref = raw.get("schema_ref")
        if not isinstance(schema_ref, str) or not schema_ref.strip():
            diagnostics.append(
                artifact_format_diagnostic(
                    "ISO200",
                    "error",
                    "Artifact Format Profile",
                    "Artifact Format Profile requires a non-empty schema_ref.",
                    field="schema_ref",
                )
            )
            return None, diagnostics
        diagnostics.extend(validate_format_ref(schema_ref, field="schema_ref"))
        templates_raw = raw.get("templates", {})
        templates: dict[str, str] = {}
        if not isinstance(templates_raw, Mapping):
            diagnostics.append(
                artifact_format_diagnostic(
                    "ISO200",
                    "error",
                    "Artifact Format Profile",
                    "Artifact Format Profile templates must be an object keyed by output format.",
                    field="templates",
                )
            )
        else:
            for output_format, template_ref in templates_raw.items():
                if not isinstance(template_ref, str) or not template_ref.strip():
                    diagnostics.append(
                        artifact_format_diagnostic(
                            "ISO200",
                            "error",
                            "Artifact Format Profile",
                            "Artifact Format Profile template refs must be non-empty strings.",
                            field=f"templates.{output_format}",
                        )
                    )
                    continue
                diagnostics.extend(validate_format_ref(template_ref, field=f"templates.{output_format}"))
                templates[str(output_format)] = template_ref
        if any(diagnostic.is_error for diagnostic in diagnostics):
            return None, diagnostics
        return (
            cls(
                ref=ref,
                schema_ref=schema_ref,
                templates=templates,
                media_type=_optional_string(raw.get("media_type")),
                schema_version=_optional_string(raw.get("schema_version")),
                compatibility_version=_optional_string(raw.get("compatibility_version")),
                status=_optional_string(raw.get("status")),
                validation_hints=_object_dict(raw.get("validation_hints")),
                renderer_hints=_object_dict(raw.get("renderer_hints")),
                metadata=_object_dict(raw.get("metadata")),
            ),
            diagnostics,
        )

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "ref": self.ref,
            "schema_ref": self.schema_ref,
            "templates": dict(sorted(self.templates.items())),
        }
        for key, value in (
            ("media_type", self.media_type),
            ("schema_version", self.schema_version),
            ("compatibility_version", self.compatibility_version),
            ("status", self.status),
        ):
            if value is not None:
                data[key] = value
        if self.validation_hints:
            data["validation_hints"] = self.validation_hints
        if self.renderer_hints:
            data["renderer_hints"] = self.renderer_hints
        if self.metadata:
            data["metadata"] = self.metadata
        return data


@dataclass(frozen=True)
class ArtifactFormatResolution:
    """Resolved provider asset or path-backed material."""

    ref: str
    kind: Literal["profile", "schema", "template"]
    source_kind: SourceKind
    content: str
    digest: str
    path: Path | None = None
    media_type: str | None = None
    diagnostics: list[Diagnostic] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "ref": self.ref,
            "kind": self.kind,
            "source_kind": self.source_kind,
            "digest": self.digest,
        }
        if self.path is not None:
            data["path"] = str(self.path)
        if self.media_type is not None:
            data["media_type"] = self.media_type
        return data


@dataclass(frozen=True)
class ValidationResult:
    """Deterministic JSON Schema validation result."""

    ok: bool
    status: Literal["valid", "invalid", "error"]
    payload_digest: str
    schema_ref: str | None
    schema_digest: str | None
    schema_source_kind: SourceKind | None
    diagnostics: list[Diagnostic] = field(default_factory=list)
    profile_ref: str | None = None
    schema_version: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "ok": self.ok,
            "status": self.status,
            "payload_digest": self.payload_digest,
            "schema_ref": self.schema_ref,
            "schema_digest": self.schema_digest,
            "schema_source_kind": self.schema_source_kind,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }
        if self.profile_ref is not None:
            data["format_profile_ref"] = self.profile_ref
        if self.schema_version is not None:
            data["schema_version"] = self.schema_version
        return data


@dataclass(frozen=True)
class RenderResult:
    """Deterministic Jinja2 render result."""

    ok: bool
    status: Literal["rendered", "not_requested", "error"]
    payload_digest: str
    template_ref: str | None
    template_digest: str | None
    template_source_kind: SourceKind | None
    content: str | None
    diagnostics: list[Diagnostic] = field(default_factory=list)
    profile_ref: str | None = None
    schema_ref: str | None = None
    schema_digest: str | None = None
    schema_source_kind: SourceKind | None = None
    output_format: str | None = None

    def to_json(self, *, include_content: bool = True) -> dict[str, object]:
        data: dict[str, object] = {
            "ok": self.ok,
            "status": self.status,
            "payload_digest": self.payload_digest,
            "template_ref": self.template_ref,
            "template_digest": self.template_digest,
            "template_source_kind": self.template_source_kind,
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }
        if self.profile_ref is not None:
            data["format_profile_ref"] = self.profile_ref
        if self.schema_ref is not None:
            data["schema_ref"] = self.schema_ref
        if self.schema_digest is not None:
            data["schema_digest"] = self.schema_digest
        if self.schema_source_kind is not None:
            data["schema_source_kind"] = self.schema_source_kind
        if self.output_format is not None:
            data["format"] = self.output_format
        if include_content and self.content is not None:
            data["content"] = self.content
        return data


def parse_format_ref(value: str) -> ArtifactFormatRef:
    """Parse a canonical Artifact Format ref or raise ValueError."""

    diagnostics = validate_format_ref(value)
    if diagnostics:
        raise ValueError(diagnostics[0].message)
    origin, path = value.split(":", 1)
    return ArtifactFormatRef(origin=origin, parts=tuple(path.split("/")))  # type: ignore[arg-type]


def validate_format_ref(value: str | None, *, field: str = "format_ref") -> list[Diagnostic]:
    """Return deterministic diagnostics for a canonical Artifact Format ref."""

    raw = str(value or "")
    if not raw.strip():
        return [
            artifact_format_diagnostic(
                "ISO200",
                "error",
                "Artifact Format Ref",
                "Artifact Format ref is required.",
                field=field,
            )
        ]
    if ":" not in raw:
        return [
            artifact_format_diagnostic(
                "ISO200",
                "error",
                "Artifact Format Ref",
                "Artifact Format ref must include an origin prefix such as isomer: or custom:.",
                field=field,
            )
        ]
    origin, path = raw.split(":", 1)
    if origin not in FORMAT_REF_ORIGINS:
        return [
            artifact_format_diagnostic(
                "ISO200",
                "error",
                "Artifact Format Ref",
                "Artifact Format ref origin must be isomer or custom.",
                field=field,
            )
        ]
    parts = path.split("/")
    if len(parts) < 3:
        return [
            artifact_format_diagnostic(
                "ISO200",
                "error",
                "Artifact Format Ref",
                "Artifact Format ref path must include owner slug, primary group, and name segments.",
                field=field,
            )
        ]
    invalid_parts = [part for part in parts if part in {"", ".", ".."} or FORMAT_REF_SEGMENT_RE.fullmatch(part) is None]
    if invalid_parts:
        return [
            artifact_format_diagnostic(
                "ISO200",
                "error",
                "Artifact Format Ref",
                f"Artifact Format ref contains invalid path segment(s): {', '.join(invalid_parts)}.",
                field=field,
            )
        ]
    return []


def digest_bytes(content: bytes) -> str:
    return "sha256:" + hashlib.sha256(content).hexdigest()


def digest_json(value: object) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return digest_bytes(encoded)


def artifact_format_diagnostic(
    code: str,
    severity: Literal["error", "warning"],
    concept: str,
    message: str,
    *,
    field: str | None = None,
    path: Path | None = None,
    hint: str | None = None,
) -> Diagnostic:
    return Diagnostic(
        code=code,
        severity=severity,
        concept=concept,
        message=message,
        field=field,
        path=path,
        hint=hint,
    )


def _optional_string(value: object) -> str | None:
    return value if isinstance(value, str) and value.strip() else None


def _object_dict(value: object) -> dict[str, object]:
    if not isinstance(value, Mapping):
        return {}
    return {str(key): item for key, item in value.items()}
