"""Artifact Format provider resolution."""

from __future__ import annotations

import json
from typing import Literal

from isomer_labs.artifact_formats.models import (
    ArtifactFormatProfile,
    ArtifactFormatResolution,
    artifact_format_diagnostic,
    validate_format_ref,
)
from isomer_labs.artifact_formats.registry import ArtifactFormatRegistry, default_registry
from isomer_labs.diagnostics import Diagnostic


class ArtifactFormatResolver:
    """Resolve Artifact Format refs through registered providers."""

    def __init__(self, registry: ArtifactFormatRegistry | None = None) -> None:
        self.registry = registry or default_registry

    def resolve_profile(self, ref: str) -> tuple[ArtifactFormatProfile | None, ArtifactFormatResolution | None, list[Diagnostic]]:
        diagnostics = validate_format_ref(ref, field="format_profile_ref")
        if diagnostics:
            return None, None, diagnostics
        resolution, resolve_diagnostics = self._resolve(ref, "profile")
        if resolution is None:
            return None, None, resolve_diagnostics
        try:
            loaded = json.loads(resolution.content)
        except json.JSONDecodeError as exc:
            return None, resolution, [
                artifact_format_diagnostic(
                    "ISO202",
                    "error",
                    "Artifact Format Profile",
                    f"Artifact Format Profile JSON could not be loaded: {exc.msg}.",
                    field="format_profile_ref",
                    path=resolution.path,
                )
            ]
        if not isinstance(loaded, dict):
            return None, resolution, [
                artifact_format_diagnostic(
                    "ISO202",
                    "error",
                    "Artifact Format Profile",
                    "Artifact Format Profile content must be a JSON object.",
                    field="format_profile_ref",
                    path=resolution.path,
                )
            ]
        profile, profile_diagnostics = ArtifactFormatProfile.from_mapping(ref, loaded)
        return profile, resolution, profile_diagnostics

    def resolve_schema(self, ref: str) -> tuple[ArtifactFormatResolution | None, list[Diagnostic]]:
        diagnostics = validate_format_ref(ref, field="schema_ref")
        if diagnostics:
            return None, diagnostics
        return self._resolve(ref, "schema")

    def resolve_template(self, ref: str) -> tuple[ArtifactFormatResolution | None, list[Diagnostic]]:
        diagnostics = validate_format_ref(ref, field="template_ref")
        if diagnostics:
            return None, diagnostics
        return self._resolve(ref, "template")

    def _resolve(
        self,
        ref: str,
        kind: Literal["profile", "schema", "template"],
    ) -> tuple[ArtifactFormatResolution | None, list[Diagnostic]]:
        for provider in self.registry.providers():
            resolver = {
                "profile": provider.resolve_profile,
                "schema": provider.resolve_schema,
                "template": provider.resolve_template,
            }[kind]
            resolution = resolver(ref)
            if resolution is not None:
                return resolution, list(resolution.diagnostics)
        return None, [
            artifact_format_diagnostic(
                "ISO201",
                "error",
                "Artifact Format Resolution",
                f"No registered Artifact Format provider resolved {kind} ref: {ref}.",
                field=f"{kind}_ref",
            )
        ]
