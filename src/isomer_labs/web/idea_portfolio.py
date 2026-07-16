"""Producer-neutral Research Idea portfolio predicates and read metadata."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from isomer_labs.runtime.records import (
    RESEARCH_IDEA_ARCHIVE_STATES,
    RESEARCH_IDEA_DECISION_STATES,
    RESEARCH_IDEA_EVIDENCE_STATES,
    RESEARCH_IDEA_EXPLORATION_STATES,
    RESEARCH_IDEA_VISIBILITIES,
)


PORTFOLIO_PRESET_REGISTRY: tuple[dict[str, object], ...] = (
    {
        "id": "current",
        "label": "Current",
        "description": "Active Primary Ideas whose decision remains unknown, open, shortlisted, or selected.",
        "predicate": {
            "archive_state": ["active"],
            "visibility": ["primary"],
            "decision_state": ["unknown", "open", "shortlisted", "selected"],
        },
    },
    {
        "id": "all-proposed",
        "label": "All proposed",
        "description": "Every non-hidden canonical Research Idea, including supporting and archived ideas.",
        "predicate": {"visibility": ["primary", "supporting"]},
    },
    {
        "id": "open-for-exploration",
        "label": "Open for exploration",
        "description": "Active non-hidden ideas explicitly open, shortlisted, or selected.",
        "predicate": {
            "archive_state": ["active"],
            "visibility": ["primary", "supporting"],
            "decision_state": ["open", "shortlisted", "selected"],
        },
    },
    {
        "id": "unexplored",
        "label": "Unexplored",
        "description": "Non-hidden ideas whose exploration has not started.",
        "predicate": {"visibility": ["primary", "supporting"], "exploration_state": ["unexplored"]},
    },
    {
        "id": "exploring",
        "label": "Exploring",
        "description": "Non-hidden ideas under active exploration.",
        "predicate": {"visibility": ["primary", "supporting"], "exploration_state": ["exploring"]},
    },
    {
        "id": "explored",
        "label": "Explored",
        "description": "Non-hidden ideas whose exploration pass is complete.",
        "predicate": {"visibility": ["primary", "supporting"], "exploration_state": ["explored"]},
    },
    {
        "id": "selected",
        "label": "Selected",
        "description": "Non-hidden ideas selected for further development.",
        "predicate": {"visibility": ["primary", "supporting"], "decision_state": ["selected"]},
    },
    {
        "id": "deferred",
        "label": "Deferred",
        "description": "Non-hidden ideas deferred for possible later reconsideration.",
        "predicate": {"visibility": ["primary", "supporting"], "decision_state": ["deferred"]},
    },
    {
        "id": "closed",
        "label": "Closed",
        "description": "Non-hidden ideas closed with a recorded reason when available.",
        "predicate": {"visibility": ["primary", "supporting"], "decision_state": ["closed"]},
    },
    {
        "id": "needs-classification",
        "label": "Needs classification",
        "description": "Non-hidden ideas with an unknown exploration, decision, or evidence facet.",
        "predicate": {
            "visibility": ["primary", "supporting"],
            "needs_classification": ["exploration_state", "decision_state", "evidence_state"],
        },
    },
)

PORTFOLIO_PRESETS = {str(item["id"]): item for item in PORTFOLIO_PRESET_REGISTRY}
PORTFOLIO_FACETS: tuple[str, ...] = (
    "exploration_state",
    "decision_state",
    "evidence_state",
    "archive_state",
    "visibility",
)
PORTFOLIO_FILTER_VALUES: dict[str, tuple[str, ...]] = {
    "exploration_state": RESEARCH_IDEA_EXPLORATION_STATES,
    "decision_state": RESEARCH_IDEA_DECISION_STATES,
    "evidence_state": RESEARCH_IDEA_EVIDENCE_STATES,
    "archive_state": RESEARCH_IDEA_ARCHIVE_STATES,
    "visibility": RESEARCH_IDEA_VISIBILITIES,
}


def apply_portfolio_predicate(
    nodes: list[dict[str, Any]],
    *,
    preset: str,
    exploration_state: str | None = None,
    decision_state: str | None = None,
    evidence_state: str | None = None,
    archive_state: str | None = None,
    visibility: str | None = None,
    generation_id: str | None = None,
    decision_record_id: str | None = None,
    include_secondary: bool = False,
) -> dict[str, Any]:
    """Apply a fixed preset and explicit filters to canonical idea nodes."""

    selected_preset = PORTFOLIO_PRESETS.get(preset)
    if selected_preset is None:
        message = f"Unsupported Research Idea portfolio preset: {preset}"
        return {
            "ok": False,
            "nodes": [],
            "preset": None,
            "explicit_filters": {},
            "applied_predicate": {},
            "diagnostics": [_diag("error", "portfolio_preset_unsupported", message, preset=preset)],
            "error": {"code": "portfolio_preset_unsupported", "message": message},
        }

    explicit_raw = {
        "exploration_state": exploration_state,
        "decision_state": decision_state,
        "evidence_state": evidence_state,
        "archive_state": archive_state,
        "visibility": visibility,
    }
    explicit_filters: dict[str, list[str]] = {}
    diagnostics: list[dict[str, Any]] = []
    for facet, raw_value in explicit_raw.items():
        values = sorted(_split_filter(raw_value))
        invalid = [value for value in values if value not in PORTFOLIO_FILTER_VALUES[facet]]
        if invalid:
            message = f"Unsupported {facet} filter value: {', '.join(invalid)}"
            return {
                "ok": False,
                "nodes": [],
                "preset": dict(selected_preset),
                "explicit_filters": {**explicit_filters, facet: values},
                "applied_predicate": {},
                "diagnostics": [_diag("error", "portfolio_filter_value_unsupported", message, facet=facet, values=invalid)],
                "error": {"code": "portfolio_filter_value_unsupported", "message": message},
            }
        if values:
            explicit_filters[facet] = values
    generation_values = sorted(_split_filter(generation_id))
    decision_values = sorted(_split_filter(decision_record_id))
    if generation_values:
        explicit_filters["generation_id"] = generation_values
    if decision_values:
        explicit_filters["decision_record_id"] = decision_values

    preset_predicate = {
        key: list(value) if isinstance(value, list) else value
        for key, value in _mapping(selected_preset.get("predicate")).items()
    }
    if preset == "current" and include_secondary and "visibility" not in explicit_filters:
        preset_predicate["visibility"] = ["primary", "supporting"]
    for facet in PORTFOLIO_FACETS:
        preset_values = set(_string_list(preset_predicate.get(facet)))
        explicit_values = set(explicit_filters.get(facet, []))
        if preset_values and explicit_values and not preset_values.intersection(explicit_values):
            diagnostics.append(
                _diag(
                    "warning",
                    "portfolio_filter_contradiction",
                    f"Preset {preset} and the explicit {facet} filter have no values in common.",
                    preset=preset,
                    facet=facet,
                    preset_values=sorted(preset_values),
                    explicit_values=sorted(explicit_values),
                )
            )

    selected = [
        node
        for node in nodes
        if _matches_predicate(node, preset_predicate)
        and _matches_explicit(node, explicit_filters)
    ]
    applied_predicate = {
        "composition": "preset AND explicit_filters",
        "composition_order": ["preset", "explicit_filters", "relation_filter", "text_filter", "paging"],
        "preset": preset_predicate,
        "explicit_filters": explicit_filters,
        "include_secondary_compatibility": include_secondary,
    }
    return {
        "ok": True,
        "nodes": selected,
        "preset": {**dict(selected_preset), "predicate": preset_predicate},
        "explicit_filters": explicit_filters,
        "applied_predicate": applied_predicate,
        "diagnostics": diagnostics,
        "error": None,
    }


def facet_counts(nodes: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    """Return deterministic counts for every canonical facet value."""

    counts: dict[str, dict[str, int]] = {}
    for facet in PORTFOLIO_FACETS:
        values = PORTFOLIO_FILTER_VALUES[facet]
        facet_count = {value: 0 for value in values}
        for node in nodes:
            value = str(node.get(facet) or "unknown")
            facet_count[value] = facet_count.get(value, 0) + 1
        counts[facet] = facet_count
    return counts


def portfolio_metadata(
    *,
    result: Mapping[str, Any],
    source_nodes: list[dict[str, Any]],
    visible_nodes: list[dict[str, Any]],
    source_edge_count: int,
    visible_edge_count: int,
    omitted_cross_boundary_edge_count: int,
    topology_complete: bool,
) -> dict[str, Any]:
    return {
        "preset": result.get("preset"),
        "available_presets": [dict(item) for item in PORTFOLIO_PRESET_REGISTRY],
        "explicit_filters": result.get("explicit_filters") or {},
        "applied_predicate": result.get("applied_predicate") or {},
        "source_counts": {
            "ideas": len(source_nodes),
            "edges": source_edge_count,
            "facets": facet_counts(source_nodes),
        },
        "visible_counts": {
            "ideas": len(visible_nodes),
            "edges": visible_edge_count,
            "facets": facet_counts(visible_nodes),
        },
        "omitted_cross_boundary_edge_count": omitted_cross_boundary_edge_count,
        "source_topology_complete": topology_complete,
    }


def classification_fields(node: Mapping[str, Any]) -> list[str]:
    return [facet for facet in ("exploration_state", "decision_state", "evidence_state") if str(node.get(facet) or "unknown") == "unknown"]


def _matches_predicate(node: Mapping[str, Any], predicate: Mapping[str, Any]) -> bool:
    for facet in PORTFOLIO_FACETS:
        accepted = set(_string_list(predicate.get(facet)))
        if accepted and str(node.get(facet) or "unknown") not in accepted:
            return False
    if predicate.get("needs_classification") and not classification_fields(node):
        return False
    return True


def _matches_explicit(node: Mapping[str, Any], filters: Mapping[str, list[str]]) -> bool:
    for facet in PORTFOLIO_FACETS:
        accepted = set(filters.get(facet, []))
        if accepted and str(node.get(facet) or "unknown") not in accepted:
            return False
    generation_ids = set(_string_list(node.get("generation_ids")))
    if filters.get("generation_id") and not generation_ids.intersection(filters["generation_id"]):
        return False
    decision_ids = set(_string_list(node.get("decision_record_ids")))
    if filters.get("decision_record_id") and not decision_ids.intersection(filters["decision_record_id"]):
        return False
    return True


def _mapping(value: object) -> Mapping[str, object]:
    return value if isinstance(value, Mapping) else {}


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item)]


def _split_filter(value: str | None) -> set[str]:
    if value is None or not value.strip():
        return set()
    return {item.strip() for item in value.split(",") if item.strip()}


def _diag(severity: str, code: str, message: str, **details: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {"severity": severity, "code": code, "message": message}
    payload.update(details)
    return payload
