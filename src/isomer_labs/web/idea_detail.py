"""Idea-detail read helpers for the local Project web API."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from urllib.parse import quote

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.idea_sources import (
    SOURCE_CLASSIFICATION_LEGACY,
    SOURCE_STATUS_LEGACY_FALLBACK,
    resolve_structured_source_fragment,
)
from isomer_labs.runtime.records import StructuredResearchPayloadRecord
from isomer_labs.runtime.store import open_workspace_runtime


SOURCE_JSON_DEFAULT_CAP_BYTES = 1024 * 1024


@dataclass(frozen=True)
class _SourceCandidate:
    kind: str
    record_id: str | None
    json_path: str | None


def idea_detail_payload(
    context: EffectiveTopicContext,
    idea_id: str,
    *,
    env: Mapping[str, str],
    include_source_json: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    """Build the topic-scoped read-only payload for one canonical Research Idea."""

    store, runtime_diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    if store is None:
        return {
            "ok": False,
            "mutated": False,
            "topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "idea_id": idea_id,
            "diagnostics": [],
        }, runtime_diagnostics

    try:
        idea = store.get_research_idea(idea_id, topic_workspace_id=context.topic_workspace_id)
        if idea is None:
            return {
                "ok": False,
                "mutated": False,
                "topic_id": context.research_topic.id,
                "topic_workspace_id": context.topic_workspace_id,
                "idea_id": idea_id,
                "idea": None,
                "realizations": [],
                "generation_groups": [],
                "incoming_edges": [],
                "outgoing_edges": [],
                "source": _missing_source("idea_not_found", "Research Idea is not available in this topic."),
                "exists": False,
                "error": {"code": "idea_not_found", "message": f"Research Idea is not available: {idea_id}"},
                "diagnostics": [
                    _payload_diagnostic("idea_not_found", "warning", f"Research Idea is not available: {idea_id}")
                ],
            }, runtime_diagnostics

        realizations = store.list_research_idea_realizations(
            topic_workspace_id=context.topic_workspace_id,
            idea_id=idea.idea_id,
        )
        latest_realization = next((item for item in realizations if item.latest), realizations[0] if realizations else None)
        incoming_edges = store.list_research_idea_lineage_edges(
            topic_workspace_id=context.topic_workspace_id,
            child_idea_id=idea.idea_id,
        )
        outgoing_edges = store.list_research_idea_lineage_edges(
            topic_workspace_id=context.topic_workspace_id,
            parent_idea_id=idea.idea_id,
        )
        generation_ids = {
            edge.generation_id
            for edge in [*incoming_edges, *outgoing_edges]
            if edge.generation_id is not None
        }
        generation_groups = [
            group
            for group in store.list_research_idea_generation_groups(topic_workspace_id=context.topic_workspace_id)
            if group.id in generation_ids
        ]
        idea_content, source, source_provenance, source_diagnostics = _resolve_source(
            context,
            store,
            idea.to_json(),
            latest_realization.to_json() if latest_realization is not None else None,
            idea_id=idea.idea_id,
            candidates=_source_candidates(idea.to_json(), latest_realization.to_json() if latest_realization is not None else None),
            include_source_json=include_source_json,
        )
        latest_record = None
        if latest_realization is not None:
            latest_record = store.get_lifecycle_record(latest_realization.record_id)
        return {
            "ok": True,
            "mutated": False,
            "topic_id": context.research_topic.id,
            "topic_workspace_id": context.topic_workspace_id,
            "idea_id": idea.idea_id,
            "exists": True,
            "idea": idea.to_json(),
            "realizations": [item.to_json() for item in realizations],
            "latest_realization": latest_realization.to_json() if latest_realization is not None else None,
            "latest_record": latest_record.to_json() if latest_record is not None else None,
            "generation_groups": [item.to_json() for item in generation_groups],
            "incoming_edges": [item.to_json() for item in incoming_edges],
            "outgoing_edges": [item.to_json() for item in outgoing_edges],
            "idea_content": idea_content,
            "source": source,
            "source_provenance": source_provenance,
            "diagnostics": source_diagnostics,
        }, runtime_diagnostics
    finally:
        store.close()


def _source_candidates(idea: Mapping[str, object], latest_realization: Mapping[str, object] | None) -> list[_SourceCandidate]:
    candidates: list[_SourceCandidate] = []
    if latest_realization is not None:
        latest_path = _string_or_none(latest_realization.get("source_json_path"))
        candidates.append(
            _SourceCandidate(
                kind="latest_realization_source_path",
                record_id=_string_or_none(latest_realization.get("record_id")),
                json_path=latest_path,
            )
        )
    if latest_realization is None:
        candidates.append(
            _SourceCandidate(
                kind="idea_source_path",
                record_id=_string_or_none(idea.get("source_record_id")),
                json_path=_string_or_none(idea.get("source_json_path")),
            )
        )
    return candidates


def _resolve_source(
    context: EffectiveTopicContext,
    store: Any,
    idea: Mapping[str, object],
    latest_realization: Mapping[str, object] | None,
    *,
    idea_id: str,
    candidates: list[_SourceCandidate],
    include_source_json: bool,
) -> tuple[dict[str, object], dict[str, object], dict[str, object], list[dict[str, object]]]:
    diagnostics: list[dict[str, object]] = []
    for candidate in candidates:
        if candidate.record_id is None:
            continue
        structured = store.get_structured_payload(candidate.record_id)
        resolution = resolve_structured_source_fragment(
            context,
            idea_id=idea_id,
            structured=structured,
            source_json_path=candidate.json_path,
            record_id=candidate.record_id,
            severity="warning",
        )
        diagnostics.extend(resolution.diagnostics)
        if not resolution.exact:
            break
        idea_content = _idea_content(idea, resolution.source_json, resolution=resolution)
        source, source_diagnostics = _source_response(
            context,
            idea_id=idea_id,
            source_kind=candidate.kind,
            record_id=candidate.record_id,
            json_path=resolution.source_json_path,
            structured=structured,
            source_json=idea_content,
            source_fragment_status=resolution.status,
            source_classification=resolution.classification,
            include_source_json=include_source_json,
        )
        diagnostics.extend(source_diagnostics)
        provenance = _source_provenance(source, diagnostics)
        return idea_content, source, provenance, diagnostics

    metadata_source = _idea_content(idea, None, resolution=None)
    diagnostics.append(
        _payload_diagnostic(
            "source_json_unavailable",
            "warning",
            "No managed structured payload JSON was available; using canonical idea metadata.",
        )
    )
    source, source_diagnostics = _source_response(
        context,
        idea_id=idea_id,
        source_kind="idea_metadata",
        record_id=_string_or_none(idea.get("source_record_id")),
        json_path=_string_or_none(idea.get("source_json_path")),
        structured=None,
        source_json=metadata_source,
        source_fragment_status=SOURCE_STATUS_LEGACY_FALLBACK,
        source_classification=SOURCE_CLASSIFICATION_LEGACY,
        include_source_json=include_source_json,
    )
    diagnostics.extend(source_diagnostics)
    provenance = _source_provenance(source, diagnostics)
    return metadata_source, source, provenance, diagnostics


def _source_response(
    context: EffectiveTopicContext,
    *,
    idea_id: str,
    source_kind: str,
    record_id: str | None,
    json_path: str | None,
    structured: StructuredResearchPayloadRecord | None,
    source_json: object,
    source_fragment_status: str,
    source_classification: str,
    include_source_json: bool,
) -> tuple[dict[str, object], list[dict[str, object]]]:
    encoded = json.dumps(source_json, ensure_ascii=False, sort_keys=True, indent=2)
    size = len(encoded.encode("utf-8"))
    truncated = size > SOURCE_JSON_DEFAULT_CAP_BYTES and not include_source_json
    diagnostics: list[dict[str, object]] = []
    if truncated:
        diagnostics.append(
            _payload_diagnostic(
                "source_json_truncated",
                "warning",
                f"Source JSON is {size} bytes, above the default {SOURCE_JSON_DEFAULT_CAP_BYTES} byte response cap.",
            )
        )
    response: dict[str, object] = {
        "source_kind": source_kind,
        "source_record_id": record_id,
        "source_json_path": json_path,
        "source_json_available": True,
        "source_json_truncated": truncated,
        "source_json_bytes": size,
        "source_json_cap_bytes": SOURCE_JSON_DEFAULT_CAP_BYTES,
        "source_fragment_status": source_fragment_status,
        "source_classification": source_classification,
        "full_source_url": f"/api/topics/{context.research_topic.id}/ideas/{_quote_path_segment(idea_id)}?include_source_json=true",
    }
    if structured is not None:
        response.update(
            {
                "payload_digest": structured.payload_digest,
                "payload_file_path": structured.payload_file_path,
                "payload_media_type": structured.payload_media_type,
            }
        )
    if not truncated:
        response["source_json"] = source_json
    return response, diagnostics


def _idea_content(
    idea: Mapping[str, object],
    source_json: object | None,
    *,
    resolution: object | None,
) -> dict[str, object]:
    content: dict[str, object] = dict(source_json) if isinstance(source_json, Mapping) else {}
    for key in ("idea_id", "title", "one_liner", "family", "status", "visibility", "aliases"):
        if key in idea and key not in content:
            content[key] = idea[key]  # type: ignore[index]
    if "source_label" not in content:
        source_label = content.get("id") or content.get("label")
        if source_label is not None:
            content["source_label"] = source_label
    if resolution is not None and getattr(resolution, "source_json_path", None) is not None:
        content["source_json_path"] = getattr(resolution, "source_json_path")
    return content


def _source_provenance(source: Mapping[str, object], diagnostics: list[dict[str, object]]) -> dict[str, object]:
    keys = (
        "source_kind",
        "source_record_id",
        "source_json_path",
        "source_fragment_status",
        "source_classification",
        "payload_digest",
        "payload_file_path",
        "payload_media_type",
        "source_json_bytes",
    )
    data = {key: source[key] for key in keys if key in source}
    data["diagnostics"] = diagnostics
    return data


def _missing_source(code: str, message: str) -> dict[str, object]:
    return {
        "source_kind": "missing",
        "source_record_id": None,
        "source_json_path": None,
        "source_json_available": False,
        "source_json_truncated": False,
        "source_json_bytes": 0,
        "error": {"code": code, "message": message},
    }


def _payload_diagnostic(code: str, severity: str, message: str) -> dict[str, object]:
    return {
        "code": code,
        "severity": severity,
        "concept": "Research Idea Source JSON",
        "message": message,
    }


def _string_or_none(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _quote_path_segment(value: str) -> str:
    return quote(value, safe="")
