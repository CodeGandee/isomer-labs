"""Load and validate extension-owned Kaoju process and artifact resources."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from importlib.resources import files
import json
from typing import Any, Literal, Mapping

from jsonschema import Draft202012Validator  # type: ignore[import-untyped]

from isomer_labs.core.artifact_identity import ArtifactIdentityError, parse_artifact_identity


CONTRACT_RESOURCE = "resources/survey-process.v2.json"
BINDING_RESOURCE = "resources/bindings.v2.json"
BINDING_SCHEMA_RESOURCE = "resources/bindings.v2.schema.json"
SEMANTIC_RESOURCE = "resources/artifact-semantics.v1.json"
SEMANTIC_SCHEMA_RESOURCE = "resources/artifact-semantics.v1.schema.json"
KAOJU_NAMESPACE = "KAOJU"

ContentMode = Literal[
    "structured_file",
    "ordinary_file",
    "directory_manifest",
    "external_path",
    "canonical_repository",
]


@dataclass(frozen=True)
class KaojuContract:
    """Checked public process inventory and implementation decisions for Kaoju."""

    schema_version: str
    entry_skill: str
    skills: tuple[str, ...]
    protected_members: tuple["KaojuProtectedMember", ...]
    survey_intents: tuple[str, ...]
    compatibility_procedures: tuple[str, ...]
    exploration_procedures: tuple[str, ...]
    manager_actions: dict[str, tuple[str, ...]]
    binding_queries: dict[str, str]
    raw: dict[str, Any]


@dataclass(frozen=True)
class KaojuProtectedMember:
    """One stable protected Kaoju capability reported by the process contract."""

    logical_id: str
    member_name: str
    invocation_designator: str


@dataclass(frozen=True)
class KaojuArtifactSemantic:
    """Storage-neutral meaning and ownership for one canonical Kaoju artifact."""

    semantic_id: str
    category: str
    meaning: str
    minimum_content: tuple[str, ...]
    producer: str
    consumers: tuple[str, ...]
    update_intent: str


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
    path = files("isomer_labs.kaoju").joinpath(resource)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Packaged Kaoju resource must contain a JSON object: {resource}")
    return value


@lru_cache(maxsize=1)
def load_contract() -> KaojuContract:
    """Return the checked Kaoju public process contract."""

    raw = _load_json(CONTRACT_RESOURCE)
    required = (
        "schema_version",
        "entry_skill",
        "protected_members",
        "skills",
        "survey_intents",
        "compatibility_procedures",
        "exploration_procedures",
        "manager_actions",
        "binding_queries",
    )
    missing = [name for name in required if name not in raw]
    if missing:
        raise ValueError(f"Kaoju survey-process contract is missing: {', '.join(missing)}")
    skills = _unique_strings(raw["skills"], "skills")
    entry_skill = str(raw["entry_skill"])
    if entry_skill != "isomer-ext-kaoju-entrypoint" or not skills or skills[0] != entry_skill:
        raise ValueError("Kaoju contract entry_skill must be the first public skill and use the extension entrypoint name.")
    raw_members = raw["protected_members"]
    if not isinstance(raw_members, list):
        raise ValueError("Kaoju protected_members must be a list.")
    protected_members: list[KaojuProtectedMember] = []
    for index, item in enumerate(raw_members):
        if not isinstance(item, dict):
            raise ValueError(f"Kaoju protected_members[{index}] must be an object.")
        logical_id = str(item.get("logical_id", ""))
        member_name = str(item.get("member_name", ""))
        invocation_designator = str(item.get("invocation_designator", ""))
        if not logical_id or not member_name:
            raise ValueError(f"Kaoju protected_members[{index}] must define logical_id and member_name.")
        if invocation_designator != f"{entry_skill}->{member_name}":
            raise ValueError(f"Kaoju protected member {logical_id!r} has a noncanonical invocation designator.")
        protected_members.append(KaojuProtectedMember(logical_id, member_name, invocation_designator))
    if len(protected_members) != 14:
        raise ValueError(f"Kaoju contract must declare fourteen protected members, found {len(protected_members)}.")
    if len({item.logical_id for item in protected_members}) != len(protected_members):
        raise ValueError("Kaoju protected member logical ids must be unique.")
    if len({item.member_name for item in protected_members}) != len(protected_members):
        raise ValueError("Kaoju protected member names must be unique within the public pack.")
    if tuple(item.logical_id for item in protected_members) != skills[1:]:
        raise ValueError("Kaoju protected member mapping must match the ordered protected skill inventory.")
    intents = _unique_strings(raw["survey_intents"], "survey_intents")
    compatibility = _unique_strings(raw["compatibility_procedures"], "compatibility_procedures")
    exploration = _unique_strings(raw["exploration_procedures"], "exploration_procedures")
    if len(skills) != 15:
        raise ValueError(f"Kaoju contract must declare fifteen skills, found {len(skills)}.")
    if len(intents) != 10:
        raise ValueError(f"Kaoju contract must declare ten survey intents, found {len(intents)}.")
    raw_managers = raw["manager_actions"]
    if not isinstance(raw_managers, dict):
        raise ValueError("Kaoju manager_actions must be an object.")
    managers = {
        str(name): _unique_strings(actions, f"manager_actions.{name}")
        for name, actions in raw_managers.items()
    }
    raw_queries = raw["binding_queries"]
    if not isinstance(raw_queries, dict) or set(raw_queries) != {"list", "describe"}:
        raise ValueError("Kaoju binding_queries must contain only list and describe commands.")
    queries = {str(name): str(command) for name, command in raw_queries.items()}
    expected_queries = {
        "list": "isomer-cli --print-json ext kaoju bindings list",
        "describe": "isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT",
    }
    if queries != expected_queries:
        raise ValueError("Kaoju binding_queries must use the canonical context-free ext kaoju commands.")
    if "semantic_aliases" in raw or "binding_registry_resource" in raw:
        raise ValueError("Kaoju process resources cannot expose artifact aliases or physical registry paths.")
    return KaojuContract(
        schema_version=str(raw["schema_version"]),
        entry_skill=entry_skill,
        skills=skills,
        protected_members=tuple(protected_members),
        survey_intents=intents,
        compatibility_procedures=compatibility,
        exploration_procedures=exploration,
        manager_actions=managers,
        binding_queries=queries,
        raw=raw,
    )


@lru_cache(maxsize=1)
def _load_binding_registry() -> dict[str, KaojuBinding]:
    raw = _load_json(BINDING_RESOURCE)
    schema = _load_json(BINDING_SCHEMA_RESOURCE)
    errors = validate_binding_registry_document(raw, schema=schema)
    if errors:
        raise ValueError(f"Invalid Kaoju binding registry: {'; '.join(errors)}")
    resolved: dict[str, KaojuBinding] = {}
    for raw_binding in raw["bindings"]:
        semantic_id = str(raw_binding["semantic_id"])
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


@lru_cache(maxsize=1)
def _load_semantic_registry() -> dict[str, KaojuArtifactSemantic]:
    raw = _load_json(SEMANTIC_RESOURCE)
    schema = _load_json(SEMANTIC_SCHEMA_RESOURCE)
    errors = validate_semantic_registry_document(raw, schema=schema)
    if errors:
        raise ValueError(f"Invalid Kaoju semantic registry: {'; '.join(errors)}")
    resolved: dict[str, KaojuArtifactSemantic] = {}
    for raw_semantic in raw["artifacts"]:
        semantic_id = str(raw_semantic["semantic_id"])
        resolved[semantic_id] = KaojuArtifactSemantic(
            semantic_id=semantic_id,
            category=str(raw_semantic["category"]),
            meaning=str(raw_semantic["meaning"]),
            minimum_content=tuple(str(value) for value in raw_semantic["minimum_content"]),
            producer=str(raw_semantic["producer"]),
            consumers=tuple(str(value) for value in raw_semantic["consumers"]),
            update_intent=str(raw_semantic["update_intent"]),
        )
    return resolved


@lru_cache(maxsize=1)
def resource_coverage_diagnostics() -> tuple[str, ...]:
    """Return deterministic semantic-to-binding coverage and ownership diagnostics."""

    bindings = _load_binding_registry()
    semantics = _load_semantic_registry()
    diagnostics: list[str] = []
    for semantic_id in sorted(set(semantics) - set(bindings)):
        diagnostics.append(f"semantic registry id has no binding: {semantic_id}")
    for semantic_id in sorted(set(bindings) - set(semantics)):
        diagnostics.append(f"binding id has no semantic definition: {semantic_id}")
    for semantic_id in sorted(set(bindings) & set(semantics)):
        binding = bindings[semantic_id]
        semantic = semantics[semantic_id]
        if semantic.producer != binding.producer:
            diagnostics.append(
                f"producer mismatch for {semantic_id}: semantics={semantic.producer!r}, binding={binding.producer!r}"
            )
        if semantic.consumers != binding.consumers:
            diagnostics.append(
                f"consumer mismatch for {semantic_id}: semantics={semantic.consumers!r}, binding={binding.consumers!r}"
            )
    return tuple(diagnostics)


@lru_cache(maxsize=1)
def load_binding_registry() -> dict[str, KaojuBinding]:
    """Return bindings keyed by exact uppercase semantic id."""

    diagnostics = resource_coverage_diagnostics()
    if diagnostics:
        raise ValueError(f"Invalid Kaoju resource coverage: {'; '.join(diagnostics)}")
    return _load_binding_registry()


@lru_cache(maxsize=1)
def load_semantic_registry() -> dict[str, KaojuArtifactSemantic]:
    """Return storage-neutral meanings keyed by exact uppercase semantic id."""

    diagnostics = resource_coverage_diagnostics()
    if diagnostics:
        raise ValueError(f"Invalid Kaoju resource coverage: {'; '.join(diagnostics)}")
    return _load_semantic_registry()


def validate_binding_registry_document(raw: object, *, schema: dict[str, Any] | None = None) -> list[str]:
    """Return stable structural, identity, duplicate, and successor diagnostics."""

    selected_schema = schema or _load_json(BINDING_SCHEMA_RESOURCE)
    diagnostics = _schema_diagnostics(raw, selected_schema)
    if isinstance(raw, dict) and isinstance(raw.get("bindings"), list):
        seen: dict[str, int] = {}
        successors: list[tuple[int, str]] = []
        for index, binding in enumerate(raw["bindings"]):
            if not isinstance(binding, dict) or not isinstance(binding.get("semantic_id"), str):
                continue
            semantic_id = binding["semantic_id"]
            diagnostics.extend(_identity_diagnostics(semantic_id, f"bindings/{index}/semantic_id"))
            artifact_type = binding.get("artifact_type")
            try:
                identity = parse_artifact_identity(semantic_id, expected_extension="kaoju")
            except ArtifactIdentityError:
                identity = None
            if identity is not None and isinstance(artifact_type, str) and identity.what != artifact_type.upper():
                diagnostics.append(
                    f"bindings/{index}/semantic_id: {semantic_id} does not match artifact_type {artifact_type!r}"
                )
            if semantic_id in seen:
                diagnostics.append(
                    f"bindings/{index}/semantic_id: duplicate {semantic_id}; first declared at bindings/{seen[semantic_id]}"
                )
            else:
                seen[semantic_id] = index
            migration = binding.get("migration")
            if isinstance(migration, dict) and isinstance(migration.get("canonical_successor"), str):
                successor = migration["canonical_successor"]
                diagnostics.extend(
                    _identity_diagnostics(successor, f"bindings/{index}/migration/canonical_successor")
                )
                successors.append((index, successor))
        for index, successor in successors:
            if successor not in seen:
                diagnostics.append(
                    f"bindings/{index}/migration/canonical_successor: unregistered {successor}"
                )
    return sorted(set(diagnostics))


def validate_semantic_registry_document(raw: object, *, schema: dict[str, Any] | None = None) -> list[str]:
    """Return stable structural, identity, and duplicate diagnostics for semantics."""

    selected_schema = schema or _load_json(SEMANTIC_SCHEMA_RESOURCE)
    diagnostics = _schema_diagnostics(raw, selected_schema)
    if isinstance(raw, dict) and isinstance(raw.get("artifacts"), list):
        seen: dict[str, int] = {}
        for index, semantic in enumerate(raw["artifacts"]):
            if not isinstance(semantic, dict) or not isinstance(semantic.get("semantic_id"), str):
                continue
            semantic_id = semantic["semantic_id"]
            diagnostics.extend(_identity_diagnostics(semantic_id, f"artifacts/{index}/semantic_id"))
            if semantic_id in seen:
                diagnostics.append(
                    f"artifacts/{index}/semantic_id: duplicate {semantic_id}; first declared at artifacts/{seen[semantic_id]}"
                )
            else:
                seen[semantic_id] = index
    return sorted(set(diagnostics))


def describe_binding(semantic_id: str) -> dict[str, Any]:
    """Return one joined semantic and storage binding description."""

    parse_artifact_identity(semantic_id, expected_extension="kaoju")
    binding = load_binding_registry().get(semantic_id)
    semantic = load_semantic_registry().get(semantic_id)
    if binding is None or semantic is None:
        raise KeyError(f"Unknown Kaoju semantic id: {semantic_id}")
    return {
        "semantic_id": binding.semantic_id,
        "category": semantic.category,
        "meaning": semantic.meaning,
        "minimum_content": list(semantic.minimum_content),
        "update_intent": semantic.update_intent,
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


def list_binding_summaries() -> list[dict[str, Any]]:
    """Return canonical-identifier-sorted joined binding summaries."""

    return [
        {
            "semantic_id": semantic_id,
            "meaning": semantic.meaning,
            "artifact_type": binding.artifact_type,
            "record_kind": binding.record_kind,
            "producer": binding.producer,
            "status": binding.status,
        }
        for semantic_id in sorted(load_binding_registry())
        for binding in (load_binding_registry()[semantic_id],)
        for semantic in (load_semantic_registry()[semantic_id],)
    ]


def resource_versions() -> dict[str, str]:
    """Return the declared versions of the extension-owned Kaoju resources."""

    return {
        "process": str(_load_json(CONTRACT_RESOURCE)["schema_version"]),
        "bindings": str(_load_json(BINDING_RESOURCE)["schema_version"]),
        "semantics": str(_load_json(SEMANTIC_RESOURCE)["schema_version"]),
    }


def _identity_diagnostics(value: str, path: str) -> list[str]:
    try:
        parse_artifact_identity(value, expected_extension="kaoju")
    except ArtifactIdentityError as exc:
        return [f"{path}: {exc}"]
    return []


def _schema_diagnostics(raw: object, schema: Mapping[str, Any]) -> list[str]:
    errors = sorted(
        Draft202012Validator(schema).iter_errors(raw),
        key=lambda error: (tuple(str(part) for part in error.path), error.message),
    )
    return [
        f"{'/'.join(str(part) for part in error.path) or '<root>'}: {error.message}"
        for error in errors
    ]


def _unique_strings(value: object, field: str) -> tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"Kaoju contract field {field} must be a non-empty string list.")
    values = tuple(value)
    if len(values) != len(set(values)):
        raise ValueError(f"Kaoju contract field {field} contains duplicates.")
    return values
