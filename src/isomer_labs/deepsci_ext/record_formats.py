"""DeepScientist Artifact Format provider."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
import json

from isomer_labs.artifact_formats.models import ArtifactFormatResolution, digest_bytes
from isomer_labs.artifact_formats.registry import ArtifactFormatRegistry, default_registry


CATALOG_RESOURCE = "assets/record_formats/profiles/catalog.v1.json"
SCHEMA_RESOURCE_V1 = "assets/record_formats/schemas/structured-record.v1.schema.json"
SCHEMA_RESOURCE_V2 = "assets/record_formats/schemas/structured-record.v2.schema.json"
TEMPLATE_RESOURCE_V1 = "assets/record_formats/templates/markdown/structured-record.v1.md.j2"
TEMPLATE_RESOURCE_V2 = "assets/record_formats/templates/markdown/structured-record.v2.md.j2"
PROVIDER_ID = "isomer.deepsci.record-formats"
SUPPORTED_STRUCTURED_RECORD_VERSION = "v2"
UNSUPPORTED_STRUCTURED_RECORD_VERSION = "v1"
PROFILE_ASSETS = {
    "control.topic-reset-checkpoint": (
        "assets/record_formats/schemas/topic-reset-checkpoint.v1.schema.json",
        "assets/record_formats/templates/markdown/topic-reset-checkpoint.v1.md.j2",
    ),
    "control.topic-reset-plan": (
        "assets/record_formats/schemas/topic-reset-plan.v1.schema.json",
        "assets/record_formats/templates/markdown/topic-reset-plan.v1.md.j2",
    ),
    "report.topic-reset-outcome": (
        "assets/record_formats/schemas/topic-reset-outcome.v1.schema.json",
        "assets/record_formats/templates/markdown/topic-reset-outcome.v1.md.j2",
    ),
}


@dataclass(frozen=True)
class DeepScientistRecordFormatProvider:
    """Provider for active DeepSci record-format refs."""

    provider_id: str = PROVIDER_ID

    def resolve_profile(self, ref: str) -> ArtifactFormatResolution | None:
        parsed = parse_record_format_ref(ref, expected_kind="profile")
        if parsed is None:
            return None
        legacy_profile, version = parsed
        if legacy_profile not in active_profile_names():
            return None
        if legacy_profile in PROFILE_ASSETS and version != "v1":
            return None
        if legacy_profile not in PROFILE_ASSETS and version not in {"v1", "v2"}:
            return None
        profile = {
            "schema_ref": canonical_record_format_ref(legacy_profile, "schema", version=version),
            "templates": {
                "markdown": canonical_record_format_ref(legacy_profile, "template", version=version),
            },
            "media_type": "application/json",
            "schema_version": "topic-reset.v1" if legacy_profile in PROFILE_ASSETS else f"deepsci-structured-record.{version}",
            "compatibility_version": version,
            "status": "active" if version == "v2" or legacy_profile in PROFILE_ASSETS else "legacy_unsupported",
            "metadata": {
                "provider": "deepsci",
                "legacy_profile": legacy_profile,
                "record_format_version": version,
            },
        }
        content = json.dumps(profile, indent=2, sort_keys=True)
        return _resolution(ref, "profile", content)

    def resolve_schema(self, ref: str) -> ArtifactFormatResolution | None:
        parsed = parse_record_format_ref(ref, expected_kind="schema")
        if parsed is None:
            return None
        legacy_profile, version = parsed
        if legacy_profile not in active_profile_names():
            return None
        if legacy_profile in PROFILE_ASSETS and version != "v1":
            return None
        if legacy_profile not in PROFILE_ASSETS and version not in {"v1", "v2"}:
            return None
        resource = PROFILE_ASSETS.get(legacy_profile, _shared_resources(version))[0]
        return _resolution(ref, "schema", _resource_text(resource), media_type="application/schema+json")

    def resolve_template(self, ref: str) -> ArtifactFormatResolution | None:
        parsed = parse_record_format_ref(ref, expected_kind="template")
        if parsed is None:
            return None
        legacy_profile, version = parsed
        if legacy_profile not in active_profile_names():
            return None
        if legacy_profile in PROFILE_ASSETS and version != "v1":
            return None
        if legacy_profile not in PROFILE_ASSETS and version not in {"v1", "v2"}:
            return None
        resource = PROFILE_ASSETS.get(legacy_profile, _shared_resources(version))[1]
        return _resolution(ref, "template", _resource_text(resource), media_type="text/markdown")


def register_deepsci_record_format_provider(registry: ArtifactFormatRegistry | None = None) -> DeepScientistRecordFormatProvider:
    """Register the DeepScientist record-format provider."""

    provider = DeepScientistRecordFormatProvider()
    selected_registry = registry or default_registry
    selected_registry.register_provider(provider)
    return provider


def active_profile_names() -> tuple[str, ...]:
    """Return active legacy profile names covered by this provider."""

    catalog = json.loads(_resource_text(CATALOG_RESOURCE))
    profiles = catalog.get("profiles", [])
    return tuple(str(profile) for profile in profiles)


def active_deepsci_binding_profile_names() -> tuple[str, ...]:
    """Return active profile names expected in DeepSci placeholder bindings."""

    return tuple(profile for profile in active_profile_names() if profile not in PROFILE_ASSETS)


def canonical_record_format_ref(legacy_profile: str, kind: str, *, version: str | None = None) -> str:
    """Convert a legacy binding profile name to a canonical DeepScientist ref."""

    parts = [part for part in legacy_profile.split(".") if part]
    if not parts:
        raise ValueError("DeepScientist legacy profile name is required.")
    selected_version = version or ("v1" if legacy_profile in PROFILE_ASSETS else SUPPORTED_STRUCTURED_RECORD_VERSION)
    if kind == "template":
        return f"isomer:deepsci/record-format/template/markdown/{'/'.join(parts)}/{selected_version}"
    if kind in {"profile", "schema"}:
        return f"isomer:deepsci/record-format/{kind}/{'/'.join(parts)}/{selected_version}"
    raise ValueError(f"Unsupported DeepScientist record-format ref kind: {kind}")


def legacy_profile_from_ref(ref: str, *, expected_kind: str) -> str | None:
    parsed = parse_record_format_ref(ref, expected_kind=expected_kind)
    return parsed[0] if parsed is not None else None


def parse_record_format_ref(ref: str, *, expected_kind: str) -> tuple[str, str] | None:
    prefix = "isomer:deepsci/record-format/"
    if not ref.startswith(prefix):
        return None
    tail = ref[len(prefix):]
    parts = tail.split("/")
    if expected_kind == "template":
        if len(parts) < 5 or parts[0] != "template" or parts[1] != "markdown" or not _version_tail(parts[-1]):
            return None
        return ".".join(parts[2:-1]), parts[-1]
    if len(parts) < 4 or parts[0] != expected_kind or not _version_tail(parts[-1]):
        return None
    return ".".join(parts[1:-1]), parts[-1]


def is_unsupported_deepsci_v1_ref(ref: str | None) -> bool:
    """Return whether a ref names an unsupported generic DeepSci v1 structured record."""

    if not ref:
        return False
    for kind in ("profile", "schema", "template"):
        parsed = parse_record_format_ref(ref, expected_kind=kind)
        if parsed is None:
            continue
        legacy_profile, version = parsed
        return version == UNSUPPORTED_STRUCTURED_RECORD_VERSION and legacy_profile not in PROFILE_ASSETS
    return False


def _shared_resources(version: str) -> tuple[str, str]:
    if version == "v2":
        return SCHEMA_RESOURCE_V2, TEMPLATE_RESOURCE_V2
    return SCHEMA_RESOURCE_V1, TEMPLATE_RESOURCE_V1


def _version_tail(value: str) -> bool:
    return value in {"v1", "v2"}


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
