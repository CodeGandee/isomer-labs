"""Record-to-query-index extraction helpers."""

from __future__ import annotations

import json
import mimetypes
from pathlib import Path
from typing import Any, Iterable, Mapping

from sqlalchemy import Table, delete, insert

from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import RuntimeLifecycleRecord, StructuredResearchPayloadRecord, utc_timestamp

from .index_schema import (
    IndexedRecordParts,
    RELATION_KINDS,
    SOURCE_AUTHORED,
    SOURCE_PAYLOAD,
    record_claims,
    record_edges,
    record_files,
    record_ideas,
    record_index,
    record_json_facts,
    record_metrics,
    record_routes,
)

def _build_index_parts(
    context: EffectiveTopicContext,
    record: RuntimeLifecycleRecord,
    payload: StructuredResearchPayloadRecord | None,
) -> IndexedRecordParts:
    now = utc_timestamp()
    record_metadata = dict(record.transition_metadata)
    payload_json = payload.payload_json if payload is not None else {}
    title = _first_string(payload_json.get("title"), record_metadata.get("title"), record.id)
    summary = _first_string(payload_json.get("summary"), record_metadata.get("summary"))
    format_profile_ref = payload.format_profile_ref if payload is not None else _optional_string(record_metadata.get("format_profile_ref"))
    profile_family, profile_name = _profile_parts(format_profile_ref or _optional_string(record_metadata.get("profile")))
    source = SOURCE_PAYLOAD if payload is not None else SOURCE_AUTHORED
    index_row: dict[str, object] = {
        "record_id": record.id,
        "research_topic_id": record.research_topic_id,
        "topic_workspace_id": record.topic_workspace_id,
        "record_kind": record.record_kind,
        "status": record.status,
        "placeholder": _optional_string(record_metadata.get("placeholder")),
        "profile": _optional_string(record_metadata.get("profile")),
        "skill": _optional_string(record_metadata.get("skill")),
        "producer": _optional_string(record_metadata.get("producer")),
        "consumer": _optional_string(record_metadata.get("consumer")),
        "format_profile_ref": format_profile_ref,
        "profile_family": profile_family,
        "profile_name": profile_name,
        "title": title,
        "summary": summary,
        "content_path": record.content_path,
        "rendered_markdown_path": payload.rendered_markdown_path if payload is not None else _optional_string(record_metadata.get("rendered_markdown_path")),
        "validation_status": payload.validation_status if payload is not None else _optional_string(record_metadata.get("validation_status")),
        "render_status": payload.render_status if payload is not None else _optional_string(record_metadata.get("render_status")),
        "payload_digest": payload.payload_digest if payload is not None else _optional_string(record_metadata.get("payload_digest")),
        "source_classification": source,
        "stale": 0,
        "created_at": record.created_at,
        "updated_at": record.updated_at,
        "indexed_at": now,
        "metadata_json": _dumps({"lifecycle_refs": record.lifecycle_refs, "transition_metadata": record_metadata}),
    }
    return IndexedRecordParts(
        index_row=index_row,
        edge_rows=_edge_rows(context, record, payload_json, record_metadata, now),
        file_rows=_file_rows(context, record, payload, payload_json, record_metadata, now),
        idea_rows=_idea_rows(context, record, payload_json, now),
        route_rows=_route_rows(context, record, payload_json, now),
        metric_rows=_metric_rows(context, record, payload_json, now),
        claim_rows=_claim_rows(context, record, payload_json, now),
        fact_rows=_fact_rows(context, record, payload_json, now),
    )


def _replace_record_rows(connection: Any, record_id: str, parts: IndexedRecordParts) -> None:
    for table in (record_edges,):
        connection.execute(delete(table).where(table.c.source_record_id == record_id))
    for table in (record_files, record_ideas, record_routes, record_metrics, record_claims, record_json_facts):
        connection.execute(delete(table).where(table.c.record_id == record_id))
    connection.execute(delete(record_index).where(record_index.c.record_id == record_id))
    connection.execute(insert(record_index).values(parts.index_row))
    _bulk_insert(connection, record_edges, parts.edge_rows)
    _bulk_insert(connection, record_files, parts.file_rows)
    _bulk_insert(connection, record_ideas, parts.idea_rows)
    _bulk_insert(connection, record_routes, parts.route_rows)
    _bulk_insert(connection, record_metrics, parts.metric_rows)
    _bulk_insert(connection, record_claims, parts.claim_rows)
    _bulk_insert(connection, record_json_facts, parts.fact_rows)


def _bulk_insert(connection: Any, table: Table, rows: list[dict[str, object]]) -> None:
    if rows:
        connection.execute(insert(table), rows)


def _edge_rows(
    context: EffectiveTopicContext,
    record: RuntimeLifecycleRecord,
    payload_json: Mapping[str, object],
    record_metadata: Mapping[str, object],
    created_at: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    query_index = _dict_value(record_metadata.get("query_index"))
    for index, item in enumerate(_list_of_dicts(query_index.get("relationships"))):
        target = _optional_string(item.get("target_record_id") or item.get("target") or item.get("record_id") or item.get("ref"))
        relation = _relation_kind(item.get("relation_kind") or item.get("kind") or item.get("relation"))
        if target is None or relation is None:
            continue
        rows.append(
            _edge_row(
                context,
                record,
                target_record_id=target,
                relation_kind=relation,
                relation_role=_optional_string(item.get("relation_role") or item.get("role")),
                source_field=f"transition_metadata.query_index.relationships[{index}]",
                source_classification=SOURCE_AUTHORED,
                confidence=_float_or_none(item.get("confidence")) or 1.0,
                status=_optional_string(item.get("status")) or "ready",
                rationale=_optional_string(item.get("rationale")),
                metadata=item,
                created_at=created_at,
            )
        )
    derived_specs = (
        ("evidence_refs", "evidence_basis"),
        ("evidence_ref", "evidence_basis"),
        ("artifact_refs", "uses_input"),
        ("artifact_ref", "uses_input"),
        ("input_refs", "uses_input"),
        ("source_refs", "derived_from"),
        ("source_ref", "derived_from"),
        ("claim_refs", "supports_claim"),
        ("provenance_refs", "cites"),
        ("parent_record_id", "derived_from"),
        ("supersedes", "supersedes"),
        ("blocked_by", "blocks"),
    )
    for path, value in _walk_json(payload_json):
        key = path.rsplit(".", 1)[-1].replace("[]", "")
        relation = next((relation for candidate, relation in derived_specs if key == candidate), None)
        if relation is None:
            continue
        for target in _refs_from_value(value):
            rows.append(
                _edge_row(
                    context,
                    record,
                    target_record_id=target,
                    relation_kind=relation,
                    relation_role=None,
                    source_field=path,
                    source_classification=SOURCE_PAYLOAD,
                    confidence=0.8,
                    status="ready",
                    rationale=None,
                    metadata={},
                    created_at=created_at,
                )
            )
    return _dedupe_rows(rows)


def _edge_row(
    context: EffectiveTopicContext,
    record: RuntimeLifecycleRecord,
    *,
    target_record_id: str,
    relation_kind: str,
    relation_role: str | None,
    source_field: str,
    source_classification: str,
    confidence: float,
    status: str,
    rationale: str | None,
    metadata: Mapping[str, object],
    created_at: str,
) -> dict[str, object]:
    row_id = _row_id("edge", record.id, target_record_id, relation_kind, relation_role or "", source_field)
    return {
        "id": row_id,
        "research_topic_id": context.research_topic.id,
        "topic_workspace_id": context.topic_workspace_id,
        "source_record_id": record.id,
        "target_record_id": target_record_id,
        "relation_kind": relation_kind,
        "relation_role": relation_role,
        "source_field": source_field,
        "source_classification": source_classification,
        "confidence": confidence,
        "status": status,
        "rationale": rationale,
        "metadata_json": _dumps(dict(metadata)),
        "created_at": created_at,
        "updated_at": created_at,
    }


def _file_rows(
    context: EffectiveTopicContext,
    record: RuntimeLifecycleRecord,
    payload: StructuredResearchPayloadRecord | None,
    payload_json: Mapping[str, object],
    record_metadata: Mapping[str, object],
    created_at: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    semantic_label = _optional_string(record_metadata.get("semantic_label"))
    if record.content_path is not None:
        rows.append(_file_row(context, record, record.content_path, "body", semantic_label, None, None, SOURCE_AUTHORED, {}, created_at))
    if payload is not None and payload.rendered_markdown_path is not None:
        rows.append(
            _file_row(
                context,
                record,
                payload.rendered_markdown_path,
                "rendered_markdown",
                semantic_label,
                None,
                "structured_payload.rendered_markdown_path",
                SOURCE_PAYLOAD,
                {"payload_digest": payload.payload_digest},
                created_at,
            )
        )
    query_index = _dict_value(record_metadata.get("query_index"))
    for index, item in enumerate(_list_of_dicts(query_index.get("files"))):
        path = _optional_string(item.get("path") or item.get("locator") or item.get("file"))
        if path is None:
            continue
        rows.append(
            _file_row(
                context,
                record,
                path,
                _optional_string(item.get("file_role") or item.get("role")) or "attachment",
                _optional_string(item.get("semantic_label")) or semantic_label,
                _optional_string(item.get("operation_set_id")),
                f"transition_metadata.query_index.files[{index}]",
                SOURCE_AUTHORED,
                item,
                created_at,
            )
        )
    file_keys = {"path", "file_path", "artifact_path", "output_path", "locator"}
    for path, value in _walk_json(payload_json):
        if not isinstance(value, Mapping):
            continue
        path_value = next((_optional_string(value.get(key)) for key in file_keys if _optional_string(value.get(key)) is not None), None)
        if path_value is None:
            continue
        rows.append(
            _file_row(
                context,
                record,
                path_value,
                _optional_string(value.get("file_role") or value.get("role") or value.get("kind")) or "payload_ref",
                _optional_string(value.get("semantic_label")) or semantic_label,
                _optional_string(value.get("operation_set_id")),
                path,
                SOURCE_PAYLOAD,
                dict(value),
                created_at,
            )
        )
    return _dedupe_rows(rows)


def _file_row(
    context: EffectiveTopicContext,
    record: RuntimeLifecycleRecord,
    path_text: str,
    file_role: str,
    semantic_label: str | None,
    operation_set_id: str | None,
    source_field: str | None,
    source_classification: str,
    metadata: Mapping[str, object],
    created_at: str,
) -> dict[str, object]:
    local_path = _resolve_local_path(context, path_text)
    exists = bool(local_path is not None and local_path.exists())
    size_bytes = local_path.stat().st_size if exists and local_path is not None and local_path.is_file() else None
    media_type = mimetypes.guess_type(str(path_text))[0]
    return {
        "id": _row_id("file", record.id, path_text, file_role, source_field or ""),
        "research_topic_id": context.research_topic.id,
        "topic_workspace_id": context.topic_workspace_id,
        "record_id": record.id,
        "path": path_text,
        "file_role": file_role,
        "semantic_label": semantic_label,
        "operation_set_id": operation_set_id,
        "digest": _optional_string(metadata.get("digest")),
        "size_bytes": size_bytes,
        "media_type": _optional_string(metadata.get("media_type")) or media_type,
        "exists_flag": 1 if exists else 0,
        "status": "ready" if exists else "missing",
        "source_field": source_field,
        "source_classification": source_classification,
        "metadata_json": _dumps(dict(metadata)),
        "created_at": created_at,
        "updated_at": created_at,
    }


def _idea_rows(context: EffectiveTopicContext, record: RuntimeLifecycleRecord, payload_json: Mapping[str, object], created_at: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path, value in _walk_json(payload_json):
        key = path.rsplit(".", 1)[-1].replace("[]", "")
        if key not in {"raw_ideas", "candidate_ideas", "ideas", "selected_hypothesis", "hypotheses"}:
            continue
        items = value if isinstance(value, list) else [value]
        for index, item in enumerate(items):
            item_map = dict(item) if isinstance(item, Mapping) else {"one_liner": str(item)}
            one_liner = _first_string(item_map.get("one_liner"), item_map.get("summary"), item_map.get("title"), item_map.get("idea"), item_map.get("text"))
            if one_liner is None:
                continue
            idea_id = _optional_string(item_map.get("idea_id") or item_map.get("id"))
            source_path = f"{path}[{index}]" if isinstance(value, list) else path
            rows.append(
                {
                    "id": _row_id("idea", record.id, idea_id or one_liner, source_path),
                    "research_topic_id": context.research_topic.id,
                    "topic_workspace_id": context.topic_workspace_id,
                    "record_id": record.id,
                    "idea_id": idea_id,
                    "family": _optional_string(item_map.get("family")) or key,
                    "one_liner": one_liner,
                    "status": _optional_string(item_map.get("status")) or ("selected" if key == "selected_hypothesis" else None),
                    "selected": 1 if key == "selected_hypothesis" or bool(item_map.get("selected")) else 0,
                    "source_json_path": source_path,
                    "metadata_json": _dumps(item_map),
                    "created_at": created_at,
                }
            )
    return _dedupe_rows(rows)


def _route_rows(context: EffectiveTopicContext, record: RuntimeLifecycleRecord, payload_json: Mapping[str, object], created_at: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path, value in _walk_json(payload_json):
        if not isinstance(value, Mapping):
            continue
        if not any(key in value for key in ("decision", "next_route", "reason", "selected_hypothesis_id")):
            continue
        decision = _first_string(value.get("decision"), value.get("selected_option"))
        next_route = _first_string(value.get("next_route"), value.get("route"))
        reason = _first_string(value.get("reason"), value.get("rationale"))
        selected = _optional_string(value.get("selected_hypothesis_id"))
        if decision is None and next_route is None and reason is None and selected is None:
            continue
        rows.append(
            {
                "id": _row_id("route", record.id, path, decision or "", next_route or "", selected or ""),
                "research_topic_id": context.research_topic.id,
                "topic_workspace_id": context.topic_workspace_id,
                "record_id": record.id,
                "decision": decision,
                "next_route": next_route,
                "reason": reason,
                "selected_hypothesis_id": selected,
                "source_json_path": path,
                "metadata_json": _dumps(dict(value)),
                "created_at": created_at,
            }
        )
    return _dedupe_rows(rows)


def _metric_rows(context: EffectiveTopicContext, record: RuntimeLifecycleRecord, payload_json: Mapping[str, object], created_at: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path, value in _walk_json(payload_json):
        key = path.rsplit(".", 1)[-1].replace("[]", "")
        if "metric" not in key or not isinstance(value, Mapping):
            continue
        for metric_key, metric_value in value.items():
            if isinstance(metric_value, Mapping):
                observed = metric_value.get("value") or metric_value.get("observed_value")
                unit = _optional_string(metric_value.get("unit"))
                comparator = _optional_string(metric_value.get("comparator") or metric_value.get("expected"))
                metadata = dict(metric_value)
            elif _is_scalar(metric_value):
                observed = metric_value
                unit = None
                comparator = None
                metadata = {}
            else:
                continue
            rows.append(
                {
                    "id": _row_id("metric", record.id, path, str(metric_key)),
                    "research_topic_id": context.research_topic.id,
                    "topic_workspace_id": context.topic_workspace_id,
                    "record_id": record.id,
                    "metric_key": str(metric_key),
                    "metric_value": _stringify_scalar(observed),
                    "unit": unit,
                    "comparator": comparator,
                    "scope": _optional_string(metadata.get("scope")),
                    "source_json_path": f"{path}.{metric_key}",
                    "metadata_json": _dumps(metadata),
                    "created_at": created_at,
                }
            )
    return _dedupe_rows(rows)


def _claim_rows(context: EffectiveTopicContext, record: RuntimeLifecycleRecord, payload_json: Mapping[str, object], created_at: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path, value in _walk_json(payload_json):
        key = path.rsplit(".", 1)[-1].replace("[]", "")
        if key not in {"claims", "claim_validation", "validated_claims"}:
            continue
        items = value if isinstance(value, list) else [value]
        for index, item in enumerate(items):
            item_map = dict(item) if isinstance(item, Mapping) else {"claim": str(item)}
            claim = _first_string(item_map.get("claim"), item_map.get("text"), item_map.get("summary"))
            if claim is None:
                continue
            source_path = f"{path}[{index}]" if isinstance(value, list) else path
            rows.append(
                {
                    "id": _row_id("claim", record.id, source_path, claim),
                    "research_topic_id": context.research_topic.id,
                    "topic_workspace_id": context.topic_workspace_id,
                    "record_id": record.id,
                    "claim": claim,
                    "metric_key": _optional_string(item_map.get("metric_key")),
                    "observed_value": _stringify_scalar(item_map.get("observed_value")),
                    "expected": _stringify_scalar(item_map.get("expected") or item_map.get("expected_value") or item_map.get("expected_direction")),
                    "verdict": _optional_string(item_map.get("verdict") or item_map.get("status")),
                    "caveat": _first_string(item_map.get("caveat"), item_map.get("notes")),
                    "source_json_path": source_path,
                    "metadata_json": _dumps(item_map),
                    "created_at": created_at,
                }
            )
    return _dedupe_rows(rows)


def _fact_rows(context: EffectiveTopicContext, record: RuntimeLifecycleRecord, payload_json: Mapping[str, object], created_at: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path, value in _walk_json(payload_json):
        if len(rows) >= 200:
            break
        if not _is_scalar(value):
            continue
        rows.append(
            {
                "id": _row_id("fact", record.id, path),
                "research_topic_id": context.research_topic.id,
                "topic_workspace_id": context.topic_workspace_id,
                "record_id": record.id,
                "json_path": path,
                "value_type": type(value).__name__,
                "value_text": _stringify_scalar(value),
                "source_classification": SOURCE_PAYLOAD,
                "metadata_json": "{}",
                "created_at": created_at,
            }
        )
    return rows


def _parts_counts(parts: IndexedRecordParts) -> dict[str, int]:
    return {
        "records": 1,
        "edges": len(parts.edge_rows),
        "files": len(parts.file_rows),
        "ideas": len(parts.idea_rows),
        "routes": len(parts.route_rows),
        "metrics": len(parts.metric_rows),
        "claims": len(parts.claim_rows),
        "facts": len(parts.fact_rows),
    }


def _sum_counts(counts: Iterable[dict[str, int]]) -> dict[str, int]:
    total = {"records": 0, "edges": 0, "files": 0, "ideas": 0, "routes": 0, "metrics": 0, "claims": 0, "facts": 0}
    for item in counts:
        for key, value in item.items():
            total[key] = total.get(key, 0) + value
    return total


def _belongs_to_context(record: RuntimeLifecycleRecord, context: EffectiveTopicContext) -> bool:
    return record.research_topic_id == context.research_topic.id and record.topic_workspace_id == context.topic_workspace_id


def _profile_parts(profile_ref: str | None) -> tuple[str | None, str | None]:
    if not profile_ref:
        return None, None
    parts = [part for part in profile_ref.strip("/").split("/") if part]
    if "profile" in parts:
        index = parts.index("profile")
        if len(parts) > index + 2:
            return parts[index + 1], parts[index + 2]
    if len(parts) >= 2:
        return parts[-2], parts[-1]
    return None, profile_ref


def _relation_kind(value: object) -> str | None:
    relation = _optional_string(value)
    if relation is None:
        return None
    if relation in RELATION_KINDS or relation.startswith("custom."):
        return relation
    return None


def _dict_value(value: object) -> dict[str, object]:
    return dict(value) if isinstance(value, Mapping) else {}


def _list_of_dicts(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, Mapping)]


def _optional_string(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, Mapping | list):
        return None
    text_value = str(value).strip()
    return text_value or None


def _first_string(*values: object) -> str | None:
    for value in values:
        result = _optional_string(value)
        if result is not None:
            return result
    return None


def _float_or_none(value: object) -> float | None:
    if value is None:
        return None
    if not isinstance(value, str | int | float) or isinstance(value, bool):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _is_scalar(value: object) -> bool:
    return value is None or isinstance(value, str | int | float | bool)


def _stringify_scalar(value: object) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, bool | int | float):
        return str(value)
    return None


def _walk_json(value: object, path: str = "$") -> Iterable[tuple[str, object]]:
    yield path, value
    if isinstance(value, Mapping):
        for key, item in value.items():
            yield from _walk_json(item, f"{path}.{key}")
    elif isinstance(value, list):
        for item in value:
            yield from _walk_json(item, f"{path}[]")


def _refs_from_value(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, Mapping):
        result = _optional_string(value.get("record_id") or value.get("ref") or value.get("id") or value.get("source_ref"))
        return [result] if result is not None else []
    if isinstance(value, list):
        refs: list[str] = []
        for item in value:
            refs.extend(_refs_from_value(item))
        return refs
    return []


def _resolve_local_path(context: EffectiveTopicContext, path_text: str) -> Path | None:
    if "://" in path_text:
        return None
    path = Path(path_text)
    if not path.is_absolute():
        path = context.topic_workspace_path / path
    return path


def _row_id(*parts: object) -> str:
    text_value = "::".join(str(part) for part in parts)
    safe = "".join(char if char.isalnum() or char in "._-" else "-" for char in text_value)
    return safe[:220]


def _dedupe_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    seen: set[str] = set()
    result: list[dict[str, object]] = []
    for row in rows:
        row_id = str(row["id"])
        if row_id in seen:
            continue
        seen.add(row_id)
        result.append(row)
    return result


def _dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))
