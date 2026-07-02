"""Provider registry for Artifact Format Profiles, schemas, and templates."""

from __future__ import annotations

from typing import Mapping, Protocol

from isomer_labs.artifact_formats.models import (
    ArtifactFormatResolution,
    SourceKind,
    digest_bytes,
    validate_format_ref,
)
from isomer_labs.diagnostics import Diagnostic


class ArtifactFormatProvider(Protocol):
    """Provider interface for declarative Artifact Format material."""

    @property
    def provider_id(self) -> str:
        """Stable provider id."""

    def resolve_profile(self, ref: str) -> ArtifactFormatResolution | None:
        """Resolve an Artifact Format Profile ref."""

    def resolve_schema(self, ref: str) -> ArtifactFormatResolution | None:
        """Resolve a JSON Schema ref."""

    def resolve_template(self, ref: str) -> ArtifactFormatResolution | None:
        """Resolve a Jinja2 template ref."""


class StaticArtifactFormatProvider:
    """Small dictionary-backed provider used by tests and package assets."""

    def __init__(
        self,
        provider_id: str,
        *,
        profiles: Mapping[str, str] | None = None,
        schemas: Mapping[str, str] | None = None,
        templates: Mapping[str, str] | None = None,
        source_kind: SourceKind = "provider_asset",
    ) -> None:
        self.provider_id = provider_id
        self._profiles = dict(profiles or {})
        self._schemas = dict(schemas or {})
        self._templates = dict(templates or {})
        self._source_kind: SourceKind = source_kind

    def resolve_profile(self, ref: str) -> ArtifactFormatResolution | None:
        return self._resolve(ref, "profile", self._profiles)

    def resolve_schema(self, ref: str) -> ArtifactFormatResolution | None:
        return self._resolve(ref, "schema", self._schemas)

    def resolve_template(self, ref: str) -> ArtifactFormatResolution | None:
        return self._resolve(ref, "template", self._templates)

    def _resolve(
        self,
        ref: str,
        kind: str,
        values: Mapping[str, str],
    ) -> ArtifactFormatResolution | None:
        content = values.get(ref)
        if content is None:
            return None
        return ArtifactFormatResolution(
            ref=ref,
            kind=kind,  # type: ignore[arg-type]
            source_kind=self._source_kind,
            content=content,
            digest=digest_bytes(content.encode("utf-8")),
        )


class ArtifactFormatRegistry:
    """Ordered provider registry."""

    def __init__(self) -> None:
        self._providers: list[ArtifactFormatProvider] = []

    def register_provider(self, provider: ArtifactFormatProvider) -> None:
        self._providers = [existing for existing in self._providers if existing.provider_id != provider.provider_id]
        self._providers.append(provider)

    def providers(self) -> tuple[ArtifactFormatProvider, ...]:
        return tuple(self._providers)

    def clear(self) -> None:
        self._providers.clear()

    def validate_ref(self, ref: str, *, field: str = "format_ref") -> list[Diagnostic]:
        return validate_format_ref(ref, field=field)


default_registry = ArtifactFormatRegistry()


def register_provider(provider: ArtifactFormatProvider, registry: ArtifactFormatRegistry | None = None) -> None:
    """Register an Artifact Format provider with the selected registry."""

    selected_registry = registry or default_registry
    selected_registry.register_provider(provider)
