"""Declarative Artifact Format profile extraction for the query index."""

from __future__ import annotations

import json
from typing import Mapping

from isomer_labs.artifact_formats import (
    ArtifactFormatRegistry,
    ArtifactFormatResolver,
    register_builtin_artifact_format_providers,
)
from isomer_labs.core.artifact_identity import valid_artifact_identity
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import RuntimeLifecycleRecord

from .index_schema import SOURCE_PAYLOAD


def semantic_index_identity(
    record_metadata: Mapping[str, object],
    payload_json: Mapping[str, object],
    profile_ref: str | None,
) -> dict[str, object]:
    """Resolve an exact authored or payload canonical semantic identity."""

    profile_metadata = resolved_profile_metadata(profile_ref)
    authored = _optional_string(record_metadata.get("semantic_id"))
    payload_semantic_id = _optional_string(payload_json.get("semantic_id"))
    valid_authored = authored if authored is not None and valid_artifact_identity(authored) else None
    valid_payload = payload_semantic_id if payload_semantic_id is not None and valid_artifact_identity(payload_semantic_id) else None
    semantic_id = valid_authored or valid_payload
    source = "authored" if valid_authored is not None else "payload" if valid_payload is not None else None
    artifact_family = _first_string(
        payload_json.get("artifact_family"),
        semantic_id.split(":", 1)[0].lower() if semantic_id is not None else None,
        profile_metadata.get("artifact_family"),
    )
    diagnostics: list[dict[str, object]] = []
    if authored is not None and not valid_artifact_identity(authored):
        diagnostics.append({"code": "query_index_invalid_authored_semantic_id", "semantic_id": authored})
    if payload_semantic_id is not None and not valid_artifact_identity(payload_semantic_id):
        diagnostics.append({"code": "query_index_invalid_payload_semantic_id", "semantic_id": payload_semantic_id})
    if authored is not None and payload_semantic_id is not None and authored != payload_semantic_id:
        diagnostics.append({"code": "query_index_semantic_id_mismatch", "metadata": authored, "payload": payload_semantic_id})
    payload_family = _optional_string(payload_json.get("artifact_family"))
    if payload_family is not None and semantic_id is not None and payload_family != semantic_id.split(":", 1)[0].lower():
        diagnostics.append({"code": "query_index_artifact_family_mismatch", "payload": payload_family, "semantic_id": semantic_id})
    return {
        "profile_metadata": profile_metadata,
        "artifact_family": artifact_family,
        "semantic_id": semantic_id,
        "semantic_id_source": source,
        "artifact_type": _first_string(payload_json.get("artifact_type"), profile_metadata.get("artifact_type")),
        "diagnostics": diagnostics,
    }


def profile_metric_rows(
    context: EffectiveTopicContext,
    record: RuntimeLifecycleRecord,
    payload: Mapping[str, object],
    created_at: str,
    profile_metadata: Mapping[str, object],
    profile_ref: str | None,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for declared_path in _facet_paths(profile_metadata, "metric"):
        for actual_path, value in _declared_path_values(payload, declared_path):
            values = value.items() if isinstance(value, Mapping) else [(actual_path.rsplit(".", 1)[-1], value)]
            for metric_key, metric_value in values:
                if not _is_scalar(metric_value):
                    continue
                rows.append(
                    {
                        "id": _row_id("profile-metric", record.id, actual_path, metric_key),
                        "research_topic_id": context.research_topic.id,
                        "topic_workspace_id": context.topic_workspace_id,
                        "record_id": record.id,
                        "metric_key": str(metric_key),
                        "metric_value": _stringify_scalar(metric_value),
                        "unit": None,
                        "comparator": None,
                        "scope": None,
                        "source_json_path": actual_path,
                        "metadata_json": _dumps({"profile_ref": profile_ref, "declared_path": declared_path}),
                        "created_at": created_at,
                    }
                )
    return rows


def profile_claim_rows(
    context: EffectiveTopicContext,
    record: RuntimeLifecycleRecord,
    payload: Mapping[str, object],
    created_at: str,
    profile_metadata: Mapping[str, object],
    profile_ref: str | None,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for declared_path in _facet_paths(profile_metadata, "claim"):
        for actual_path, value in _declared_path_values(payload, declared_path):
            item = dict(value) if isinstance(value, Mapping) else {"claim": value}
            claim = _optional_string(item.get("claim") or item.get("text") or item.get("statement"))
            if claim is None:
                continue
            rows.append(
                {
                    "id": _row_id("profile-claim", record.id, actual_path, claim),
                    "research_topic_id": context.research_topic.id,
                    "topic_workspace_id": context.topic_workspace_id,
                    "record_id": record.id,
                    "claim": claim,
                    "metric_key": _optional_string(item.get("metric_key")),
                    "observed_value": _stringify_scalar(item.get("observed_value")),
                    "expected": _stringify_scalar(item.get("expected")),
                    "verdict": _optional_string(item.get("verdict") or item.get("status")),
                    "caveat": _optional_string(item.get("caveat")),
                    "source_json_path": actual_path,
                    "metadata_json": _dumps({**item, "profile_ref": profile_ref, "declared_path": declared_path}),
                    "created_at": created_at,
                }
            )
    return rows


def profile_fact_rows(
    context: EffectiveTopicContext,
    record: RuntimeLifecycleRecord,
    payload: Mapping[str, object],
    created_at: str,
    profile_metadata: Mapping[str, object],
    profile_ref: str | None,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    facets = profile_metadata.get("facet_paths")
    if not isinstance(facets, Mapping):
        return rows
    for facet, paths in sorted(facets.items()):
        if not isinstance(paths, list):
            continue
        for declared_path in paths:
            if not isinstance(declared_path, str):
                continue
            for actual_path, value in _declared_path_values(payload, declared_path):
                rows.append(
                    {
                        "id": _row_id("profile-fact", record.id, facet, actual_path),
                        "research_topic_id": context.research_topic.id,
                        "topic_workspace_id": context.topic_workspace_id,
                        "record_id": record.id,
                        "json_path": actual_path,
                        "value_type": type(value).__name__,
                        "value_text": _stringify_scalar(value) if _is_scalar(value) else _dumps(value),
                        "source_classification": SOURCE_PAYLOAD,
                        "metadata_json": _dumps({"facet": str(facet), "profile_ref": profile_ref, "declared_path": declared_path}),
                        "created_at": created_at,
                    }
                )
    return rows


def resolved_profile_metadata(profile_ref: str | None) -> dict[str, object]:
    if profile_ref is None:
        return {}
    registry = ArtifactFormatRegistry()
    register_builtin_artifact_format_providers(registry)
    profile, _resolution, diagnostics = ArtifactFormatResolver(registry).resolve_profile(profile_ref)
    return {} if diagnostics or profile is None else dict(profile.metadata)


def profile_parts(profile_ref: str | None) -> tuple[str | None, str | None]:
    """Return family and first profile-name segment for legacy projections."""

    if not profile_ref:
        return None, None
    parts = [part for part in profile_ref.strip("/").split("/") if part]
    if "profile" in parts:
        index = parts.index("profile")
        if len(parts) > index + 2:
            return parts[index + 1], parts[index + 2]
    return (parts[-2], parts[-1]) if len(parts) >= 2 else (None, profile_ref)


def _facet_paths(profile_metadata: Mapping[str, object], facet: str) -> list[str]:
    facets = profile_metadata.get("facet_paths")
    paths = facets.get(facet, []) if isinstance(facets, Mapping) else []
    return [path for path in paths if isinstance(path, str)] if isinstance(paths, list) else []


def _declared_path_values(payload: object, declared_path: str) -> list[tuple[str, object]]:
    current: list[tuple[str, object]] = [("$", payload)]
    for part in declared_path.removeprefix("$.").split("."):
        next_values: list[tuple[str, object]] = []
        for path, value in current:
            if part == "*" and isinstance(value, list):
                next_values.extend((f"{path}[{index}]", item) for index, item in enumerate(value))
            elif isinstance(value, Mapping) and part in value:
                next_values.append((f"{path}.{part}", value[part]))
        current = next_values
        if not current:
            break
    return current


def _optional_string(value: object) -> str | None:
    if value is None or isinstance(value, Mapping | list):
        return None
    return str(value).strip() or None


def _first_string(*values: object) -> str | None:
    return next((text for value in values if (text := _optional_string(value)) is not None), None)


def _is_scalar(value: object) -> bool:
    return value is None or isinstance(value, str | int | float | bool)


def _stringify_scalar(value: object) -> str | None:
    return None if value is None else str(value) if isinstance(value, str | int | float | bool) else None


def _row_id(*parts: object) -> str:
    value = "::".join(str(part) for part in parts)
    return "".join(character if character.isalnum() or character in "._-" else "-" for character in value)[:220]


def _dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))
