"""Built-in family-neutral research record Artifact Format provider."""

from __future__ import annotations

from dataclasses import dataclass, field
from importlib import resources
import json
import re
from typing import Any, Iterable, Mapping

from isomer_labs.core.artifact_identity import parse_artifact_identity
from isomer_labs.artifact_formats.models import ArtifactFormatResolution, digest_bytes
from isomer_labs.artifact_formats.registry import ArtifactFormatRegistry, default_registry


PROVIDER_ID = "isomer.research.record-formats"
CATALOG_RESOURCES = ("assets/research_record_formats/profiles/kaoju.v1.json",)
SCHEMA_RESOURCE = "assets/research_record_formats/schemas/research-structured-record.v1.schema.json"
TEMPLATE_RESOURCE = "assets/research_record_formats/templates/markdown/research-structured-record.v1.md.j2"
SCHEMA_REF = "isomer:research/record-format/schema/research-structured-record/v1"
TEMPLATE_REF = "isomer:research/record-format/template/markdown/research-structured-record/v1"
MINDSET_RECORD_SCHEMA_RESOURCE = "assets/research_record_formats/schemas/mindset-record.v1.schema.json"
MINDSET_RECORD_TEMPLATE_RESOURCE = "assets/research_record_formats/templates/markdown/mindset-record.v1.md.j2"
MINDSET_RECORD_SCHEMA_REF = "isomer:research/record-format/schema/mindset-record/v1"
MINDSET_RECORD_TEMPLATE_REF = "isomer:research/record-format/template/markdown/mindset-record/v1"
LITERATURE_OBSERVATION_PROFILE_RESOURCE = (
    "assets/research_record_formats/profiles/literature-provider-observation.v1.json"
)
LITERATURE_OBSERVATION_SCHEMA_RESOURCE = (
    "assets/research_record_formats/schemas/literature-provider-observation.v1.schema.json"
)
LITERATURE_OBSERVATION_PROFILE_REF = (
    "isomer:research/record-format/profile/literature/provider-output/provider-observation/v1"
)
LITERATURE_OBSERVATION_SCHEMA_REF = (
    "isomer:research/record-format/schema/literature-provider-observation/v1"
)
SUPPORTED_CATALOG_VERSION = "isomer-research-record-format-catalog.v1"
SUPPORTED_PROFILE_VERSIONS = ("v1", "v2")
SEGMENT_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


@dataclass(frozen=True)
class ResearchProfileRef:
    """Parsed family-neutral research profile ref."""

    family: str
    artifact_class: str
    semantic_id: str
    version: str

    @property
    def text(self) -> str:
        return research_profile_ref(self.family, self.artifact_class, self.semantic_id, version=self.version)


def research_profile_ref(family: str, artifact_class: str, semantic_id: str, *, version: str = "v1") -> str:
    """Build a canonical family-neutral research profile ref."""

    values = (family, artifact_class, semantic_id)
    if any(SEGMENT_RE.fullmatch(value) is None for value in values) or version not in SUPPORTED_PROFILE_VERSIONS:
        raise ValueError("Research profile family, class, and semantic id must be lowercase slug segments and version must be v1 or v2.")
    return f"isomer:research/record-format/profile/{family}/{artifact_class}/{semantic_id}/{version}"


def parse_research_profile_ref(ref: str) -> ResearchProfileRef | None:
    """Parse a canonical neutral research profile ref, or return ``None``."""

    prefix = "isomer:research/record-format/profile/"
    if not ref.startswith(prefix):
        return None
    parts = ref[len(prefix) :].split("/")
    if len(parts) != 4 or parts[-1] not in SUPPORTED_PROFILE_VERSIONS:
        return None
    if any(SEGMENT_RE.fullmatch(value) is None for value in parts[:-1]):
        return None
    return ResearchProfileRef(parts[0], parts[1], parts[2], parts[3])


@dataclass(frozen=True)
class ResearchRecordFormatProvider:
    """Provider backed by declarative built-in research-family catalogs."""

    catalog_resources: tuple[str, ...] = CATALOG_RESOURCES
    provider_id: str = PROVIDER_ID
    _profiles: Mapping[str, Mapping[str, object]] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_profiles", _load_catalogs(self.catalog_resources))

    def resolve_profile(self, ref: str) -> ArtifactFormatResolution | None:
        if ref == LITERATURE_OBSERVATION_PROFILE_REF:
            return _resolution(
                ref,
                "profile",
                _resource_text(LITERATURE_OBSERVATION_PROFILE_RESOURCE),
                media_type="application/json",
            )
        parsed = parse_research_profile_ref(ref)
        if parsed is None:
            return None
        raw = self._profiles.get(ref)
        if raw is None:
            return None
        is_mindset_record = raw["semantic_id"] == "KAOJU:MINDSET-RECORD"
        profile = {
            "schema_ref": MINDSET_RECORD_SCHEMA_REF if is_mindset_record else SCHEMA_REF,
            "templates": {"markdown": MINDSET_RECORD_TEMPLATE_REF if is_mindset_record else TEMPLATE_REF},
            "media_type": "application/json",
            "schema_version": "research-structured-record.v1",
            "compatibility_version": raw["version"],
            "status": raw["status"],
            "validation_hints": {"required_paths": raw["required_payload_paths"]},
            "renderer_hints": {"renderer": raw["renderer"]},
            "metadata": {
                "provider": "research",
                "artifact_family": raw["family"],
                "semantic_id": raw["semantic_id"],
                "artifact_type": raw["artifact_type"],
                "artifact_class": raw["artifact_class"],
                "compatible_record_kinds": raw["compatible_record_kinds"],
                "relationship_paths": raw["relationship_paths"],
                "file_paths": raw["file_paths"],
                "facet_paths": raw["facet_paths"],
                "idea_effects": raw["idea_effects"],
                "catalog_source": raw["catalog_source"],
            },
        }
        return _resolution(ref, "profile", json.dumps(profile, indent=2, sort_keys=True))

    def resolve_schema(self, ref: str) -> ArtifactFormatResolution | None:
        if ref == LITERATURE_OBSERVATION_SCHEMA_REF:
            return _resolution(
                ref,
                "schema",
                _resource_text(LITERATURE_OBSERVATION_SCHEMA_RESOURCE),
                media_type="application/schema+json",
            )
        if ref == MINDSET_RECORD_SCHEMA_REF:
            return _resolution(ref, "schema", _resource_text(MINDSET_RECORD_SCHEMA_RESOURCE), media_type="application/schema+json")
        if ref != SCHEMA_REF:
            return None
        return _resolution(ref, "schema", _resource_text(SCHEMA_RESOURCE), media_type="application/schema+json")

    def resolve_template(self, ref: str) -> ArtifactFormatResolution | None:
        if ref == MINDSET_RECORD_TEMPLATE_REF:
            return _resolution(ref, "template", _resource_text(MINDSET_RECORD_TEMPLATE_RESOURCE), media_type="text/markdown")
        if ref != TEMPLATE_REF:
            return None
        return _resolution(ref, "template", _resource_text(TEMPLATE_RESOURCE), media_type="text/markdown")

    def profile_refs(self) -> tuple[str, ...]:
        """Return catalog refs in deterministic order."""

        return tuple(sorted((*self._profiles, LITERATURE_OBSERVATION_PROFILE_REF)))


def register_research_record_format_provider(
    registry: ArtifactFormatRegistry | None = None,
) -> ResearchRecordFormatProvider:
    """Register the family-neutral research record provider."""

    provider = ResearchRecordFormatProvider()
    (registry or default_registry).register_provider(provider)
    return provider


def register_builtin_artifact_format_providers(registry: ArtifactFormatRegistry | None = None) -> None:
    """Register all built-in providers while preserving their distinct identities."""

    from isomer_labs.deepsci_ext.record_formats import register_deepsci_record_format_provider

    selected = registry or default_registry
    register_deepsci_record_format_provider(selected)
    register_research_record_format_provider(selected)


def _load_catalogs(catalog_resources: Iterable[str]) -> dict[str, Mapping[str, object]]:
    profiles: dict[str, Mapping[str, object]] = {}
    sources: dict[str, str] = {}
    for resource in sorted(catalog_resources):
        try:
            raw = json.loads(_resource_text(resource))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"Research format catalog {resource} could not be loaded: {exc}") from exc
        if not isinstance(raw, dict) or raw.get("schema_version") != SUPPORTED_CATALOG_VERSION:
            raise ValueError(f"Research format catalog {resource} uses an unsupported catalog version.")
        family = _slug_field(raw, "family", resource)
        entries = raw.get("profiles")
        if not isinstance(entries, list):
            raise ValueError(f"Research format catalog {resource} profiles must be an array.")
        for index, entry in enumerate(entries):
            location = f"{resource}#profiles[{index}]"
            if not isinstance(entry, dict):
                raise ValueError(f"Research format catalog entry {location} must be an object.")
            normalized = _validate_catalog_entry(entry, family=family, source=location)
            ref = str(normalized["ref"])
            if ref in profiles:
                raise ValueError(f"Duplicate research format profile ref {ref} in {sources[ref]} and {location}.")
            profiles[ref] = normalized
            sources[ref] = location
    return profiles


def _validate_catalog_entry(entry: Mapping[str, Any], *, family: str, source: str) -> dict[str, object]:
    entry_family = _slug_field(entry, "family", source)
    artifact_class = _slug_field(entry, "artifact_class", source)
    profile_slug = _slug_field(entry, "profile_slug", source)
    semantic_id = str(entry.get("semantic_id") or "")
    try:
        identity = parse_artifact_identity(semantic_id, expected_extension=family)
    except ValueError as exc:
        raise ValueError(f"Research format profile at {source} has invalid semantic_id {semantic_id!r}: {exc}") from exc
    if identity.what != profile_slug.upper():
        raise ValueError(
            f"Research format profile at {source} semantic_id {semantic_id!r} does not match profile_slug {profile_slug!r}."
        )
    artifact_type = _slug_field(entry, "artifact_type", source)
    version = str(entry.get("version") or "")
    status = str(entry.get("status") or "")
    if entry_family != family:
        raise ValueError(f"Research format catalog family mismatch at {source}: {entry_family!r} != {family!r}.")
    if version not in SUPPORTED_PROFILE_VERSIONS:
        raise ValueError(f"Research format profile at {source} uses unsupported version {version!r}.")
    if status not in {"active", "disabled"}:
        raise ValueError(f"Research format profile at {source} has unsupported status {status!r}.")
    expected_ref = research_profile_ref(family, artifact_class, profile_slug, version=version)
    declared_ref = str(entry.get("ref") or expected_ref)
    parsed = parse_research_profile_ref(declared_ref)
    if parsed is None:
        raise ValueError(f"Research format profile at {source} has invalid ref {declared_ref!r}.")
    if parsed.family != family or parsed.artifact_class != artifact_class or parsed.semantic_id != profile_slug:
        raise ValueError(f"Research format profile semantic-id mismatch at {source}: {declared_ref!r}.")
    if declared_ref != expected_ref:
        raise ValueError(f"Research format profile ref mismatch at {source}: expected {expected_ref!r}.")
    compatible_record_kinds = _string_list(entry, "compatible_record_kinds", source, allow_empty=False)
    required_payload_paths = _string_list(entry, "required_payload_paths", source, allow_empty=False)
    relationship_paths = _string_list(entry, "relationship_paths", source)
    file_paths = _string_list(entry, "file_paths", source)
    facet_paths = _path_map(entry, "facet_paths", source)
    idea_effects_raw = entry.get("idea_effects", {})
    if not isinstance(idea_effects_raw, Mapping):
        raise ValueError(f"Research format profile at {source} idea_effects must be an object.")
    renderer = str(entry.get("renderer") or "")
    if renderer != "markdown":
        raise ValueError(f"Research format profile at {source} has unsupported renderer {renderer!r}.")
    return {
        "ref": declared_ref,
        "family": family,
        "profile_slug": profile_slug,
        "semantic_id": semantic_id,
        "artifact_class": artifact_class,
        "artifact_type": artifact_type,
        "compatible_record_kinds": compatible_record_kinds,
        "required_payload_paths": required_payload_paths,
        "relationship_paths": relationship_paths,
        "file_paths": file_paths,
        "facet_paths": facet_paths,
        "idea_effects": {str(key): value for key, value in idea_effects_raw.items()},
        "renderer": renderer,
        "version": version,
        "status": status,
        "catalog_source": source,
    }


def _slug_field(raw: Mapping[str, Any], field_name: str, source: str) -> str:
    value = str(raw.get(field_name) or "")
    if SEGMENT_RE.fullmatch(value) is None:
        raise ValueError(f"Research format catalog {source} requires lowercase slug field {field_name}.")
    return value


def _string_list(raw: Mapping[str, Any], field_name: str, source: str, *, allow_empty: bool = True) -> list[str]:
    value = raw.get(field_name)
    if not isinstance(value, list) or (not allow_empty and not value) or any(not isinstance(item, str) or not item for item in value):
        raise ValueError(f"Research format catalog {source} requires {field_name} as a string array.")
    return list(value)


def _path_map(raw: Mapping[str, Any], field_name: str, source: str) -> dict[str, list[str]]:
    value = raw.get(field_name)
    if not isinstance(value, dict):
        raise ValueError(f"Research format catalog {source} requires {field_name} as an object.")
    result: dict[str, list[str]] = {}
    for key, paths in value.items():
        if not isinstance(key, str) or not isinstance(paths, list) or any(not isinstance(path, str) or not path for path in paths):
            raise ValueError(f"Research format catalog {source} has invalid {field_name}.{key} paths.")
        result[key] = list(paths)
    return result


def _resolution(ref: str, kind: str, content: str, *, media_type: str | None = None) -> ArtifactFormatResolution:
    return ArtifactFormatResolution(
        ref=ref,
        kind=kind,  # type: ignore[arg-type]
        source_kind="provider_asset",
        content=content,
        digest=digest_bytes(content.encode("utf-8")),
        media_type=media_type,
    )


def _resource_text(resource: str) -> str:
    return resources.files("isomer_labs.artifact_formats").joinpath(resource).read_text(encoding="utf-8")
