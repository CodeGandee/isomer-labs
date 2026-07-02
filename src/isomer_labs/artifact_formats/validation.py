"""JSON Schema validation for Artifact Format payloads."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import SchemaError, ValidationError, validators  # type: ignore[import-untyped]

from isomer_labs.artifact_formats.models import (
    ArtifactFormatResolution,
    ValidationResult,
    artifact_format_diagnostic,
    digest_bytes,
    digest_json,
)
from isomer_labs.artifact_formats.registry import ArtifactFormatRegistry
from isomer_labs.artifact_formats.resolver import ArtifactFormatResolver
from isomer_labs.diagnostics import Diagnostic


def validate_payload(
    payload: object,
    *,
    registry: ArtifactFormatRegistry | None = None,
    format_profile_ref: str | None = None,
    schema_ref: str | None = None,
    schema_file: Path | None = None,
) -> ValidationResult:
    """Validate a JSON-compatible payload against a resolved or path schema."""

    payload_digest = digest_json(payload)
    schema_resolution, profile_ref, schema_version, diagnostics = _resolve_schema(
        registry=registry,
        format_profile_ref=format_profile_ref,
        schema_ref=schema_ref,
        schema_file=schema_file,
    )
    if diagnostics:
        return ValidationResult(
            ok=False,
            status="error",
            payload_digest=payload_digest,
            schema_ref=schema_resolution.ref if schema_resolution is not None else schema_ref,
            schema_digest=schema_resolution.digest if schema_resolution is not None else None,
            schema_source_kind=schema_resolution.source_kind if schema_resolution is not None else None,
            diagnostics=diagnostics,
            profile_ref=profile_ref,
            schema_version=schema_version,
        )
    if schema_resolution is None:
        return ValidationResult(
            ok=False,
            status="error",
            payload_digest=payload_digest,
            schema_ref=schema_ref,
            schema_digest=None,
            schema_source_kind=None,
            diagnostics=[
                artifact_format_diagnostic(
                    "ISO203",
                    "error",
                    "Artifact Format Validation",
                    "Validation requires --format-profile, --schema-ref, or --schema-file.",
                    field="schema",
                )
            ],
            profile_ref=profile_ref,
        )
    schema, schema_diagnostics = _load_schema(schema_resolution)
    if schema_diagnostics:
        return ValidationResult(
            ok=False,
            status="error",
            payload_digest=payload_digest,
            schema_ref=schema_resolution.ref,
            schema_digest=schema_resolution.digest,
            schema_source_kind=schema_resolution.source_kind,
            diagnostics=schema_diagnostics,
            profile_ref=profile_ref,
            schema_version=schema_version,
        )
    assert schema is not None
    try:
        validator_class = validators.validator_for(schema)
        validator_class.check_schema(schema)
        errors = sorted(validator_class(schema).iter_errors(payload), key=lambda item: list(item.absolute_path))
    except SchemaError as exc:
        return ValidationResult(
            ok=False,
            status="error",
            payload_digest=payload_digest,
            schema_ref=schema_resolution.ref,
            schema_digest=schema_resolution.digest,
            schema_source_kind=schema_resolution.source_kind,
            diagnostics=[_schema_error_diagnostic(exc, schema_resolution)],
            profile_ref=profile_ref,
            schema_version=schema_version,
        )
    if errors:
        return ValidationResult(
            ok=False,
            status="invalid",
            payload_digest=payload_digest,
            schema_ref=schema_resolution.ref,
            schema_digest=schema_resolution.digest,
            schema_source_kind=schema_resolution.source_kind,
            diagnostics=[_validation_error_diagnostic(error, schema_resolution) for error in errors],
            profile_ref=profile_ref,
            schema_version=schema_version,
        )
    return ValidationResult(
        ok=True,
        status="valid",
        payload_digest=payload_digest,
        schema_ref=schema_resolution.ref,
        schema_digest=schema_resolution.digest,
        schema_source_kind=schema_resolution.source_kind,
        diagnostics=[],
        profile_ref=profile_ref,
        schema_version=schema_version,
    )


def load_payload_file(path: Path) -> tuple[object | None, list[Diagnostic]]:
    """Load JSON payload material from a file."""

    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except OSError as exc:
        return None, [
            artifact_format_diagnostic(
                "ISO203",
                "error",
                "Artifact Format Payload",
                f"Payload file could not be read: {exc}.",
                path=path,
            )
        ]
    except json.JSONDecodeError as exc:
        return None, [
            artifact_format_diagnostic(
                "ISO203",
                "error",
                "Artifact Format Payload",
                f"Payload file is not valid JSON: {exc.msg}.",
                path=path,
                field="payload_file",
            )
        ]


def load_schema_file(path: Path) -> tuple[ArtifactFormatResolution | None, list[Diagnostic]]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [
            artifact_format_diagnostic(
                "ISO203",
                "error",
                "Artifact Format Schema",
                f"Schema file could not be read: {exc}.",
                path=path,
                field="schema_file",
            )
        ]
    return (
        ArtifactFormatResolution(
            ref=str(path.resolve(strict=False)),
            kind="schema",
            source_kind="plain_file",
            content=content,
            digest=digest_bytes(content.encode("utf-8")),
            path=path.resolve(strict=False),
            media_type="application/schema+json",
        ),
        [],
    )


def _resolve_schema(
    *,
    registry: ArtifactFormatRegistry | None,
    format_profile_ref: str | None,
    schema_ref: str | None,
    schema_file: Path | None,
) -> tuple[ArtifactFormatResolution | None, str | None, str | None, list[Diagnostic]]:
    selector_count = sum(value is not None for value in (format_profile_ref, schema_ref, schema_file))
    if selector_count != 1:
        return None, format_profile_ref, None, [
            artifact_format_diagnostic(
                "ISO203",
                "error",
                "Artifact Format Validation",
                "Use exactly one schema selector: --format-profile, --schema-ref, or --schema-file.",
                field="schema",
            )
        ]
    if schema_file is not None:
        resolution, diagnostics = load_schema_file(schema_file)
        return resolution, format_profile_ref, None, diagnostics
    resolver = ArtifactFormatResolver(registry)
    if format_profile_ref is not None:
        profile, _profile_resolution, diagnostics = resolver.resolve_profile(format_profile_ref)
        if diagnostics or profile is None:
            return None, format_profile_ref, None, diagnostics
        schema_resolution, schema_diagnostics = resolver.resolve_schema(profile.schema_ref)
        return schema_resolution, profile.ref, profile.schema_version, schema_diagnostics
    assert schema_ref is not None
    schema_resolution, diagnostics = resolver.resolve_schema(schema_ref)
    return schema_resolution, format_profile_ref, None, diagnostics


def _load_schema(resolution: ArtifactFormatResolution) -> tuple[dict[str, Any] | None, list[Diagnostic]]:
    try:
        loaded = json.loads(resolution.content)
    except json.JSONDecodeError as exc:
        return None, [
            artifact_format_diagnostic(
                "ISO202",
                "error",
                "Artifact Format Schema",
                f"JSON Schema could not be loaded: {exc.msg}.",
                field="schema_ref",
                path=resolution.path,
            )
        ]
    if not isinstance(loaded, dict):
        return None, [
            artifact_format_diagnostic(
                "ISO202",
                "error",
                "Artifact Format Schema",
                "JSON Schema content must be a JSON object.",
                field="schema_ref",
                path=resolution.path,
            )
        ]
    return loaded, []


def _schema_error_diagnostic(error: SchemaError, resolution: ArtifactFormatResolution) -> Diagnostic:
    return artifact_format_diagnostic(
        "ISO202",
        "error",
        "Artifact Format Schema",
        f"JSON Schema is invalid at {_json_path(error.absolute_schema_path)}: {error.message}",
        field="schema_ref",
        path=resolution.path,
    )


def _validation_error_diagnostic(error: ValidationError, resolution: ArtifactFormatResolution) -> Diagnostic:
    keyword = str(error.validator) if error.validator else "unknown"
    return artifact_format_diagnostic(
        "ISO204",
        "error",
        "Artifact Format Payload",
        f"Payload does not satisfy schema at {_json_path(error.absolute_path)} (keyword: {keyword}): {error.message}",
        field="payload",
        path=resolution.path,
    )


def _json_path(parts: object) -> str:
    if isinstance(parts, (str, bytes)):
        values = []
    else:
        try:
            values = list(parts)  # type: ignore[call-overload]
        except TypeError:
            values = []
    if not values:
        return "$"
    return "$" + "".join(f"[{part!r}]" if isinstance(part, int) else f".{part}" for part in values)
