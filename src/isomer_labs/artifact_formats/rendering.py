"""Jinja2 rendering for Artifact Format payloads."""

from __future__ import annotations

from pathlib import Path

from jinja2 import Environment, StrictUndefined, TemplateError

from isomer_labs.artifact_formats.models import (
    ArtifactFormatResolution,
    RenderResult,
    artifact_format_diagnostic,
    digest_bytes,
)
from isomer_labs.artifact_formats.registry import ArtifactFormatRegistry
from isomer_labs.artifact_formats.resolver import ArtifactFormatResolver
from isomer_labs.artifact_formats.validation import validate_payload
from isomer_labs.core.diagnostics import Diagnostic


def render_artifact(
    payload: object,
    *,
    registry: ArtifactFormatRegistry | None = None,
    output_format: str = "markdown",
    format_profile_ref: str | None = None,
    schema_ref: str | None = None,
    template_ref: str | None = None,
    schema_file: Path | None = None,
    template_file: Path | None = None,
) -> RenderResult:
    """Validate and render a JSON-compatible payload through Jinja2."""

    validation = validate_payload(
        payload,
        registry=registry,
        format_profile_ref=format_profile_ref,
        schema_ref=schema_ref,
        schema_file=schema_file,
    )
    if not validation.ok:
        return RenderResult(
            ok=False,
            status="error",
            payload_digest=validation.payload_digest,
            template_ref=template_ref,
            template_digest=None,
            template_source_kind=None,
            content=None,
            diagnostics=validation.diagnostics,
            profile_ref=validation.profile_ref,
            schema_ref=validation.schema_ref,
            schema_digest=validation.schema_digest,
            schema_source_kind=validation.schema_source_kind,
            output_format=output_format,
        )
    template_resolution, selected_template_ref, diagnostics = _resolve_template(
        registry=registry,
        output_format=output_format,
        format_profile_ref=format_profile_ref,
        template_ref=template_ref,
        template_file=template_file,
    )
    if diagnostics or template_resolution is None:
        return RenderResult(
            ok=False,
            status="error",
            payload_digest=validation.payload_digest,
            template_ref=selected_template_ref,
            template_digest=template_resolution.digest if template_resolution is not None else None,
            template_source_kind=template_resolution.source_kind if template_resolution is not None else None,
            content=None,
            diagnostics=diagnostics,
            profile_ref=validation.profile_ref,
            schema_ref=validation.schema_ref,
            schema_digest=validation.schema_digest,
            schema_source_kind=validation.schema_source_kind,
            output_format=output_format,
        )
    try:
        rendered = Environment(undefined=StrictUndefined, autoescape=False).from_string(template_resolution.content).render(
            payload=payload
        )
    except TemplateError as exc:
        return RenderResult(
            ok=False,
            status="error",
            payload_digest=validation.payload_digest,
            template_ref=template_resolution.ref,
            template_digest=template_resolution.digest,
            template_source_kind=template_resolution.source_kind,
            content=None,
            diagnostics=[
                artifact_format_diagnostic(
                    "ISO205",
                    "error",
                    "Artifact Format Rendering",
                    f"Jinja2 rendering failed: {exc}.",
                    field="template_ref",
                    path=template_resolution.path,
                )
            ],
            profile_ref=validation.profile_ref,
            schema_ref=validation.schema_ref,
            schema_digest=validation.schema_digest,
            schema_source_kind=validation.schema_source_kind,
            output_format=output_format,
        )
    return RenderResult(
        ok=True,
        status="rendered",
        payload_digest=validation.payload_digest,
        template_ref=template_resolution.ref,
        template_digest=template_resolution.digest,
        template_source_kind=template_resolution.source_kind,
        content=rendered,
        diagnostics=[],
        profile_ref=validation.profile_ref,
        schema_ref=validation.schema_ref,
        schema_digest=validation.schema_digest,
        schema_source_kind=validation.schema_source_kind,
        output_format=output_format,
    )


def load_template_file(path: Path) -> tuple[ArtifactFormatResolution | None, list[Diagnostic]]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, [
            artifact_format_diagnostic(
                "ISO205",
                "error",
                "Artifact Format Template",
                f"Template file could not be read: {exc}.",
                path=path,
                field="template_file",
            )
        ]
    return (
        ArtifactFormatResolution(
            ref=str(path.resolve(strict=False)),
            kind="template",
            source_kind="plain_file",
            content=content,
            digest=digest_bytes(content.encode("utf-8")),
            path=path.resolve(strict=False),
            media_type="text/markdown",
        ),
        [],
    )


def _resolve_template(
    *,
    registry: ArtifactFormatRegistry | None,
    output_format: str,
    format_profile_ref: str | None,
    template_ref: str | None,
    template_file: Path | None,
) -> tuple[ArtifactFormatResolution | None, str | None, list[Diagnostic]]:
    selector_count = sum(value is not None for value in (format_profile_ref, template_ref, template_file))
    if selector_count != 1:
        return None, template_ref, [
            artifact_format_diagnostic(
                "ISO205",
                "error",
                "Artifact Format Rendering",
                "Use exactly one template selector: --format-profile, --template-ref, or --template-file.",
                field="template",
            )
        ]
    if template_file is not None:
        resolution, diagnostics = load_template_file(template_file)
        return resolution, resolution.ref if resolution is not None else None, diagnostics
    resolver = ArtifactFormatResolver(registry)
    if format_profile_ref is not None:
        profile, _profile_resolution, profile_diagnostics = resolver.resolve_profile(format_profile_ref)
        if profile_diagnostics or profile is None:
            return None, format_profile_ref, profile_diagnostics
        selected_ref = profile.templates.get(output_format)
        if selected_ref is None:
            return None, None, [
                artifact_format_diagnostic(
                    "ISO205",
                    "error",
                    "Artifact Format Rendering",
                    f"Artifact Format Profile has no template for output format: {output_format}.",
                    field="format",
                )
            ]
        resolution, diagnostics = resolver.resolve_template(selected_ref)
        return resolution, selected_ref, diagnostics
    assert template_ref is not None
    resolution, diagnostics = resolver.resolve_template(template_ref)
    return resolution, template_ref, diagnostics
