"""DeepScientist Artifact Format provider."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
import json

from isomer_labs.artifact_formats.models import ArtifactFormatResolution, digest_bytes
from isomer_labs.artifact_formats.registry import ArtifactFormatRegistry, default_registry


CATALOG_RESOURCE = "assets/record_formats/profiles/catalog.v1.json"
SCHEMA_RESOURCE = "assets/record_formats/schemas/structured-record.v1.schema.json"
TEMPLATE_RESOURCE = "assets/record_formats/templates/markdown/structured-record.v1.md.j2"
PROVIDER_ID = "isomer.deepsci.record-formats"


@dataclass(frozen=True)
class DeepScientistRecordFormatProvider:
    """Provider for active v2 DeepScientist record-format refs."""

    provider_id: str = PROVIDER_ID

    def resolve_profile(self, ref: str) -> ArtifactFormatResolution | None:
        legacy_profile = legacy_profile_from_ref(ref, expected_kind="profile")
        if legacy_profile is None or legacy_profile not in active_profile_names():
            return None
        profile = {
            "schema_ref": canonical_record_format_ref(legacy_profile, "schema"),
            "templates": {
                "markdown": canonical_record_format_ref(legacy_profile, "template"),
            },
            "media_type": "application/json",
            "schema_version": "deepsci-structured-record.v1",
            "compatibility_version": "v1",
            "status": "active",
            "metadata": {
                "provider": "deepsci",
                "legacy_profile": legacy_profile,
            },
        }
        content = json.dumps(profile, indent=2, sort_keys=True)
        return _resolution(ref, "profile", content)

    def resolve_schema(self, ref: str) -> ArtifactFormatResolution | None:
        legacy_profile = legacy_profile_from_ref(ref, expected_kind="schema")
        if legacy_profile is None or legacy_profile not in active_profile_names():
            return None
        return _resolution(ref, "schema", _resource_text(SCHEMA_RESOURCE), media_type="application/schema+json")

    def resolve_template(self, ref: str) -> ArtifactFormatResolution | None:
        legacy_profile = legacy_profile_from_ref(ref, expected_kind="template")
        if legacy_profile is None or legacy_profile not in active_profile_names():
            return None
        return _resolution(ref, "template", _resource_text(TEMPLATE_RESOURCE), media_type="text/markdown")


def register_deepsci_record_format_provider(registry: ArtifactFormatRegistry | None = None) -> DeepScientistRecordFormatProvider:
    """Register the DeepScientist record-format provider."""

    provider = DeepScientistRecordFormatProvider()
    selected_registry = registry or default_registry
    selected_registry.register_provider(provider)
    return provider


def active_profile_names() -> tuple[str, ...]:
    """Return active v2 legacy profile names covered by this provider."""

    catalog = json.loads(_resource_text(CATALOG_RESOURCE))
    profiles = catalog.get("profiles", [])
    return tuple(str(profile) for profile in profiles)


def canonical_record_format_ref(legacy_profile: str, kind: str) -> str:
    """Convert a legacy binding profile name to a canonical DeepScientist ref."""

    parts = [part for part in legacy_profile.split(".") if part]
    if not parts:
        raise ValueError("DeepScientist legacy profile name is required.")
    if kind == "template":
        return f"isomer:deepsci/record-format/template/markdown/{'/'.join(parts)}/v1"
    if kind in {"profile", "schema"}:
        return f"isomer:deepsci/record-format/{kind}/{'/'.join(parts)}/v1"
    raise ValueError(f"Unsupported DeepScientist record-format ref kind: {kind}")


def legacy_profile_from_ref(ref: str, *, expected_kind: str) -> str | None:
    prefix = "isomer:deepsci/record-format/"
    if not ref.startswith(prefix):
        return None
    tail = ref[len(prefix):]
    parts = tail.split("/")
    if expected_kind == "template":
        if len(parts) < 5 or parts[0] != "template" or parts[1] != "markdown" or parts[-1] != "v1":
            return None
        return ".".join(parts[2:-1])
    if len(parts) < 4 or parts[0] != expected_kind or parts[-1] != "v1":
        return None
    return ".".join(parts[1:-1])


def _resolution(
    ref: str,
    kind: str,
    content: str,
    *,
    media_type: str | None = None,
) -> ArtifactFormatResolution:
    return ArtifactFormatResolution(
        ref=ref,
        kind=kind,  # type: ignore[arg-type]
        source_kind="provider_asset",
        content=content,
        digest=digest_bytes(content.encode("utf-8")),
        media_type=media_type,
    )


def _resource_text(resource: str) -> str:
    package_root = resources.files("isomer_labs.deepsci_ext")
    return package_root.joinpath(resource).read_text(encoding="utf-8")
