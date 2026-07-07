"""Research Idea query-index export helpers."""

from __future__ import annotations

from typing import Any

from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.idea_sources import (
    SOURCE_CLASSIFICATION_LEGACY,
    SOURCE_STATUS_LEGACY_FALLBACK,
    resolve_structured_source_fragment,
)
from isomer_labs.runtime.records import ResearchIdea, ResearchIdeaRealization


def legacy_idea_facet(row: dict[str, object], *, has_canonical: bool) -> dict[str, object]:
    if not has_canonical:
        return {**row, "facet_role": "heuristic_fallback"}
    return {**row, "facet_role": "legacy_fallback"}


def canonical_ideas_with_source_status(
    context: EffectiveTopicContext,
    store: Any,
    ideas: list[ResearchIdea],
    realizations: list[ResearchIdeaRealization],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    diagnostics: list[dict[str, object]] = []
    by_idea: dict[str, list[ResearchIdeaRealization]] = {}
    for realization in realizations:
        by_idea.setdefault(realization.idea_id, []).append(realization)
    rows: list[dict[str, object]] = []
    for idea in ideas:
        latest = next((item for item in by_idea.get(idea.idea_id, []) if item.latest), by_idea.get(idea.idea_id, [None])[0])
        status_payload = _source_status_payload(context, store, idea, latest)
        diagnostics.extend(status_payload.pop("_diagnostics", []))  # type: ignore[arg-type]
        rows.append({**idea.to_json(), **status_payload})
    return rows, diagnostics


def canonical_realizations_with_source_status(
    context: EffectiveTopicContext,
    store: Any,
    ideas: list[ResearchIdea],
    realizations: list[ResearchIdeaRealization],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    diagnostics: list[dict[str, object]] = []
    idea_by_id = {idea.idea_id: idea for idea in ideas}
    rows: list[dict[str, object]] = []
    for realization in realizations:
        idea = idea_by_id.get(realization.idea_id)
        status_payload = _source_status_payload(context, store, idea, realization)
        diagnostics.extend(status_payload.pop("_diagnostics", []))  # type: ignore[arg-type]
        rows.append({**realization.to_json(), **status_payload})
    return rows, diagnostics


def idea_export_diagnostics(legacy_ideas: list[dict[str, object]], canonical_ideas: list[dict[str, object]]) -> list[dict[str, object]]:
    diagnostics: list[dict[str, object]] = []
    if canonical_ideas and legacy_ideas:
        diagnostics.append(
            _diag(
                "info",
                "research_record_ideas_legacy_fallback",
                "Extracted research_record_ideas facets are legacy fallback data because canonical Research Idea rows exist.",
                legacy_count=len(legacy_ideas),
                canonical_count=len(canonical_ideas),
            )
        )
    if not canonical_ideas:
        return diagnostics

    seen: set[tuple[str, str]] = set()
    duplicate_count = 0
    for row in legacy_ideas:
        key = (str(row.get("record_id") or ""), str(row.get("idea_id") or row.get("idea_title") or ""))
        if not key[0] or not key[1]:
            continue
        if key in seen:
            duplicate_count += 1
        seen.add(key)
    if duplicate_count:
        diagnostics.append(
            _diag(
                "warning",
                "duplicate_extracted_idea_facets",
                "Extracted idea facets contain duplicate record/title pairs.",
                duplicate_count=duplicate_count,
            )
        )
    return diagnostics


def _diag(severity: str, code: str, message: str, **details: object) -> dict[str, object]:
    payload: dict[str, object] = {"severity": severity, "code": code, "message": message}
    payload.update(details)
    return payload


def _source_status_payload(
    context: EffectiveTopicContext,
    store: Any,
    idea: ResearchIdea | None,
    realization: ResearchIdeaRealization | None,
) -> dict[str, object]:
    if realization is None:
        return {
            "source_fragment_status": SOURCE_STATUS_LEGACY_FALLBACK,
            "source_classification": SOURCE_CLASSIFICATION_LEGACY,
            "source_record_id": idea.source_record_id if idea is not None else None,
            "source_json_path": idea.source_json_path if idea is not None else None,
            "_diagnostics": [],
        }
    structured = store.get_structured_payload(realization.record_id)
    latest_primary = idea is not None and idea.visibility == "primary" and realization.latest and structured is not None
    resolution = resolve_structured_source_fragment(
        context,
        structured,
        realization.source_json_path,
        idea_id=realization.idea_id,
        record_id=realization.record_id,
        severity="error" if latest_primary else "warning",
    )
    payload: dict[str, object] = {
        "source_fragment_status": resolution.status,
        "source_classification": resolution.classification,
        "source_record_id": realization.record_id,
        "source_json_path": realization.source_json_path,
        "_diagnostics": resolution.diagnostics,
    }
    if structured is not None:
        payload["payload_digest"] = structured.payload_digest
    return payload
