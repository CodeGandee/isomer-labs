"""Load and validate the packaged Kaoju survey-process contracts."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files
import json
from typing import Any, Literal

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]


CONTRACT_RESOURCE = "assets/system_skills/research-paradigm/kaoju/contracts/survey-process.v2.json"
BINDING_RESOURCE = "assets/system_skills/research-paradigm/kaoju/contracts/bindings.v2.json"
BINDING_SCHEMA_RESOURCE = "assets/system_skills/research-paradigm/kaoju/contracts/bindings.v2.schema.json"

ContentMode = Literal[
    "structured_file",
    "ordinary_file",
    "directory_manifest",
    "external_path",
    "canonical_repository",
]


@dataclass(frozen=True)
class KaojuContract:
    """Checked public inventory and implementation decisions for Kaoju."""

    schema_version: str
    skills: tuple[str, ...]
    survey_intents: tuple[str, ...]
    compatibility_procedures: tuple[str, ...]
    manager_actions: dict[str, tuple[str, ...]]
    semantic_aliases: dict[str, dict[str, Any]]
    raw: dict[str, Any]


@dataclass(frozen=True)
class KaojuBinding:
    """One resolved declarative Artifact binding."""

    semantic_id: str
    artifact_type: str
    record_kind: str
    profile_ref: str | None
    semantic_label: str
    content_mode: ContentMode
    producer: str
    consumers: tuple[str, ...]
    relationships: tuple[str, ...]
    revision_mode: str
    scope_key_policy: dict[str, Any]
    latest_selection_policy: str
    validation: dict[str, Any]
    acceptance: dict[str, Any]
    status: str
    migration: dict[str, Any]


def _load_json(resource: str) -> dict[str, Any]:
    path = files("isomer_labs").joinpath(resource)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Packaged Kaoju resource must contain a JSON object: {resource}")
    return value


@lru_cache(maxsize=1)
def load_contract() -> KaojuContract:
    """Return the checked Kaoju public contract, failing on inventory drift."""

    raw = _load_json(CONTRACT_RESOURCE)
    required = ("schema_version", "skills", "survey_intents", "compatibility_procedures", "manager_actions")
    missing = [name for name in required if name not in raw]
    if missing:
        raise ValueError(f"Kaoju survey-process contract is missing: {', '.join(missing)}")
    skills = _unique_strings(raw["skills"], "skills")
    intents = _unique_strings(raw["survey_intents"], "survey_intents")
    compatibility = _unique_strings(raw["compatibility_procedures"], "compatibility_procedures")
    if len(skills) != 14:
        raise ValueError(f"Kaoju contract must declare fourteen skills, found {len(skills)}.")
    if len(intents) != 10:
        raise ValueError(f"Kaoju contract must declare ten survey intents, found {len(intents)}.")
    raw_managers = raw["manager_actions"]
    if not isinstance(raw_managers, dict):
        raise ValueError("Kaoju manager_actions must be an object.")
    managers = {str(name): _unique_strings(actions, f"manager_actions.{name}") for name, actions in raw_managers.items()}
    raw_aliases = raw.get("semantic_aliases", {})
    if not isinstance(raw_aliases, dict):
        raise ValueError("Kaoju semantic_aliases must be an object.")
    aliases: dict[str, dict[str, Any]] = {}
    for alias, disposition in raw_aliases.items():
        if not isinstance(alias, str) or not alias.startswith("kaoju:") or not isinstance(disposition, dict):
            raise ValueError("Kaoju semantic aliases require kaoju:* keys and object dispositions.")
        target = disposition.get("canonical_semantic_id")
        if not isinstance(target, str) or not target.startswith("kaoju:"):
            raise ValueError(f"Kaoju semantic alias {alias} has no canonical semantic id.")
        aliases[alias] = dict(disposition)
    return KaojuContract(
        schema_version=str(raw["schema_version"]),
        skills=skills,
        survey_intents=intents,
        compatibility_procedures=compatibility,
        manager_actions=managers,
        semantic_aliases=aliases,
        raw=raw,
    )


@lru_cache(maxsize=1)
def load_binding_registry() -> dict[str, KaojuBinding]:
    """Return bindings keyed by semantic id with deterministic schema diagnostics."""

    raw = _load_json(BINDING_RESOURCE)
    schema = _load_json(BINDING_SCHEMA_RESOURCE)
    errors = validate_binding_registry_document(raw, schema=schema)
    if errors:
        details = "; ".join(errors)
        raise ValueError(f"Invalid Kaoju binding registry: {details}")
    resolved: dict[str, KaojuBinding] = {}
    for index, raw_binding in enumerate(raw["bindings"]):
        semantic_id = str(raw_binding["semantic_id"])
        if semantic_id in resolved:
            raise ValueError(f"Duplicate Kaoju binding at bindings/{index}: {semantic_id}")
        resolved[semantic_id] = KaojuBinding(
            semantic_id=semantic_id,
            artifact_type=str(raw_binding["artifact_type"]),
            record_kind=str(raw_binding["record_kind"]),
            profile_ref=str(raw_binding["profile_ref"]) if raw_binding["profile_ref"] is not None else None,
            semantic_label=str(raw_binding["semantic_label"]),
            content_mode=raw_binding["content_mode"],
            producer=str(raw_binding["producer"]),
            consumers=tuple(str(value) for value in raw_binding["consumers"]),
            relationships=tuple(str(value) for value in raw_binding["relationships"]),
            revision_mode=str(raw_binding["revision_mode"]),
            scope_key_policy=dict(raw_binding["scope_key_policy"]),
            latest_selection_policy=str(raw_binding["latest_selection_policy"]),
            validation=dict(raw_binding["validation"]),
            acceptance=dict(raw_binding["acceptance"]),
            status=str(raw_binding["status"]),
            migration=dict(raw_binding.get("migration", {})),
        )
    return resolved


def validate_binding_registry_document(raw: object, *, schema: dict[str, Any] | None = None) -> list[str]:
    """Return stable structural and duplicate diagnostics for a candidate registry."""

    selected_schema = schema or _load_json(BINDING_SCHEMA_RESOURCE)
    errors = sorted(Draft202012Validator(selected_schema).iter_errors(raw), key=lambda error: tuple(str(part) for part in error.path))
    diagnostics = [f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}" for error in errors]
    if isinstance(raw, dict) and isinstance(raw.get("bindings"), list):
        seen: dict[str, int] = {}
        for index, binding in enumerate(raw["bindings"]):
            if not isinstance(binding, dict) or not isinstance(binding.get("semantic_id"), str):
                continue
            semantic_id = binding["semantic_id"]
            if semantic_id in seen:
                diagnostics.append(f"bindings/{index}/semantic_id: duplicate {semantic_id}; first declared at bindings/{seen[semantic_id]}")
            else:
                seen[semantic_id] = index
    return diagnostics


def describe_binding(semantic_id: str) -> dict[str, Any]:
    """Return one binding as a stable JSON-ready value."""

    binding = load_binding_registry().get(semantic_id)
    if binding is None:
        raise KeyError(f"Unknown Kaoju semantic id: {semantic_id}")
    return {
        "semantic_id": binding.semantic_id,
        "artifact_type": binding.artifact_type,
        "record_kind": binding.record_kind,
        "profile_ref": binding.profile_ref,
        "semantic_label": binding.semantic_label,
        "content_mode": binding.content_mode,
        "producer": binding.producer,
        "consumers": list(binding.consumers),
        "relationships": list(binding.relationships),
        "revision_mode": binding.revision_mode,
        "scope_key_policy": binding.scope_key_policy,
        "latest_selection_policy": binding.latest_selection_policy,
        "validation": binding.validation,
        "acceptance": binding.acceptance,
        "status": binding.status,
        "migration": binding.migration,
    }


def resolve_semantic_id(semantic_id: str) -> tuple[str, dict[str, Any] | None]:
    """Resolve an ADR-declared use-case alias without treating it as canonical state."""

    contract = load_contract()
    disposition = contract.semantic_aliases.get(semantic_id)
    if disposition is None:
        return semantic_id, None
    return str(disposition["canonical_semantic_id"]), dict(disposition)


def _unique_strings(value: object, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"Kaoju contract field {field} must be a non-empty string list.")
    values = tuple(value)
    if len(values) != len(set(values)):
        raise ValueError(f"Kaoju contract field {field} contains duplicates.")
    return values
