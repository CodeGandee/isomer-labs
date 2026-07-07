"""Shared Research Idea source-fragment resolution helpers."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path

from isomer_labs.artifact_formats import digest_json
from isomer_labs.artifact_formats.processing import load_payload_file
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import StructuredResearchPayloadRecord


SOURCE_STATUS_EXACT = "exact"
SOURCE_STATUS_MISSING_PAYLOAD = "missing_payload"
SOURCE_STATUS_MISSING_PATH = "missing_path"
SOURCE_STATUS_UNRESOLVED_PATH = "unresolved_path"
SOURCE_STATUS_BROAD_PATH = "broad_path"
SOURCE_STATUS_NON_OBJECT = "non_object"
SOURCE_STATUS_LEGACY_FALLBACK = "legacy_fallback"

SOURCE_CLASSIFICATION_CANONICAL = "canonical_idea_source"
SOURCE_CLASSIFICATION_RECORD_CONTEXT = "record_context"
SOURCE_CLASSIFICATION_LEGACY = "legacy_heuristic"

SOURCE_FRAGMENT_STATUSES = {
    SOURCE_STATUS_EXACT,
    SOURCE_STATUS_MISSING_PAYLOAD,
    SOURCE_STATUS_MISSING_PATH,
    SOURCE_STATUS_UNRESOLVED_PATH,
    SOURCE_STATUS_BROAD_PATH,
    SOURCE_STATUS_NON_OBJECT,
    SOURCE_STATUS_LEGACY_FALLBACK,
}
SOURCE_CLASSIFICATIONS = {
    SOURCE_CLASSIFICATION_CANONICAL,
    SOURCE_CLASSIFICATION_RECORD_CONTEXT,
    SOURCE_CLASSIFICATION_LEGACY,
}


@dataclass(frozen=True)
class SourceFragmentResolution:
    status: str
    classification: str
    source_json_path: str | None
    source_json: object | None
    diagnostics: list[dict[str, object]]

    @property
    def exact(self) -> bool:
        return self.status == SOURCE_STATUS_EXACT and isinstance(self.source_json, Mapping)


@dataclass(frozen=True)
class IdeaEntryFragment:
    source_json_path: str
    source_json: Mapping[str, object]


def load_structured_payload(
    context: EffectiveTopicContext,
    structured: StructuredResearchPayloadRecord,
) -> tuple[object | None, list[dict[str, object]]]:
    diagnostics: list[dict[str, object]] = []
    if structured.payload_file_path:
        path = Path(structured.payload_file_path)
        if not path.is_absolute():
            path = context.topic_workspace_path / path
        payload, load_diagnostics = load_payload_file(path)
        diagnostics.extend(
            _diag("warning", "payload_file_unreadable", diagnostic.message, record_id=structured.record_id)
            for diagnostic in load_diagnostics
        )
        if payload is not None:
            observed_digest = digest_json(payload)
            if observed_digest != structured.payload_digest:
                diagnostics.append(
                    _diag(
                        "warning",
                        "payload_digest_mismatch",
                        "Payload file digest does not match the stored structured payload digest.",
                        record_id=structured.record_id,
                    )
                )
            return payload, diagnostics
    if structured.payload_json is not None:
        if structured.payload_file_path:
            diagnostics.append(
                _diag(
                    "warning",
                    "payload_file_fallback",
                    "Using inline structured payload JSON because the payload file was unavailable.",
                    record_id=structured.record_id,
                )
            )
        return structured.payload_json, diagnostics
    diagnostics.append(
        _diag(
            "warning",
            "source_payload_missing",
            f"Structured payload for record {structured.record_id} does not contain JSON content.",
            record_id=structured.record_id,
        )
    )
    return None, diagnostics


def resolve_payload_source_fragment(
    payload: object | None,
    source_json_path: str | None,
    *,
    format_profile_ref: str | None = None,
    idea_id: str | None = None,
    record_id: str | None = None,
    severity: str = "warning",
) -> SourceFragmentResolution:
    if payload is None:
        return _resolution(
            SOURCE_STATUS_MISSING_PAYLOAD,
            SOURCE_CLASSIFICATION_LEGACY,
            source_json_path,
            None,
            severity,
            "source_payload_missing",
            "Structured source payload is not available.",
            idea_id=idea_id,
            record_id=record_id,
        )
    if not source_json_path:
        return _resolution(
            SOURCE_STATUS_MISSING_PATH,
            SOURCE_CLASSIFICATION_LEGACY,
            source_json_path,
            None,
            severity,
            "source_json_path_missing",
            "Idea realization does not name a source JSON path.",
            idea_id=idea_id,
            record_id=record_id,
        )
    if _is_root_path(source_json_path):
        return _resolution(
            SOURCE_STATUS_BROAD_PATH,
            SOURCE_CLASSIFICATION_RECORD_CONTEXT,
            source_json_path,
            payload,
            severity,
            "source_json_path_broad",
            f"Source JSON path is too broad for a Primary Idea preview: {source_json_path}",
            idea_id=idea_id,
            record_id=record_id,
        )
    extracted, unresolved = extract_json_path(payload, source_json_path)
    if unresolved:
        return _resolution(
            SOURCE_STATUS_UNRESOLVED_PATH,
            SOURCE_CLASSIFICATION_LEGACY,
            source_json_path,
            None,
            severity,
            "source_json_path_unresolved",
            f"Source JSON path could not be resolved: {source_json_path}",
            idea_id=idea_id,
            record_id=record_id,
        )
    if _is_context_path(format_profile_ref, source_json_path):
        return _resolution(
            SOURCE_STATUS_BROAD_PATH,
            SOURCE_CLASSIFICATION_RECORD_CONTEXT,
            source_json_path,
            extracted,
            severity,
            "source_json_path_context_section",
            f"Source JSON path points at record context, not idea content: {source_json_path}",
            idea_id=idea_id,
            record_id=record_id,
        )
    if not isinstance(extracted, Mapping):
        return _resolution(
            SOURCE_STATUS_NON_OBJECT,
            SOURCE_CLASSIFICATION_RECORD_CONTEXT if isinstance(extracted, list) else SOURCE_CLASSIFICATION_LEGACY,
            source_json_path,
            extracted,
            severity,
            "source_json_fragment_non_object",
            f"Source JSON path must resolve to one idea object: {source_json_path}",
            idea_id=idea_id,
            record_id=record_id,
        )
    return SourceFragmentResolution(
        status=SOURCE_STATUS_EXACT,
        classification=SOURCE_CLASSIFICATION_CANONICAL,
        source_json_path=source_json_path,
        source_json=dict(extracted),
        diagnostics=[],
    )


def resolve_structured_source_fragment(
    context: EffectiveTopicContext,
    structured: StructuredResearchPayloadRecord | None,
    source_json_path: str | None,
    *,
    idea_id: str | None = None,
    record_id: str | None = None,
    severity: str = "warning",
) -> SourceFragmentResolution:
    if structured is None:
        return _resolution(
            SOURCE_STATUS_MISSING_PAYLOAD,
            SOURCE_CLASSIFICATION_LEGACY,
            source_json_path,
            None,
            severity,
            "source_record_payload_missing",
            "Structured payload is not available for the source record.",
            idea_id=idea_id,
            record_id=record_id,
        )
    payload, payload_diagnostics = load_structured_payload(context, structured)
    resolution = resolve_payload_source_fragment(
        payload,
        source_json_path,
        format_profile_ref=structured.format_profile_ref,
        idea_id=idea_id,
        record_id=record_id or structured.record_id,
        severity=severity,
    )
    return SourceFragmentResolution(
        status=resolution.status,
        classification=resolution.classification,
        source_json_path=resolution.source_json_path,
        source_json=resolution.source_json,
        diagnostics=[*payload_diagnostics, *resolution.diagnostics],
    )


def extract_json_path(payload: object, path: str) -> tuple[object | None, bool]:
    if path in {"", "$"}:
        return payload, False
    normalized = path
    if normalized.startswith("$."):
        normalized = normalized[2:]
    elif normalized.startswith("$"):
        normalized = normalized[1:]
    if normalized.startswith("."):
        normalized = normalized[1:]
    if not normalized:
        return payload, False
    current = payload
    for token in _json_path_tokens(normalized):
        if isinstance(token, int):
            if isinstance(current, list) and 0 <= token < len(current):
                current = current[token]
                continue
            return None, True
        if isinstance(current, Mapping) and token in current:
            current = current[token]
            continue
        return None, True
    return current, False


def profile_idea_entry_fragments(
    payload: Mapping[str, object],
    format_profile_ref: str | None,
    *,
    record_id: str | None = None,
) -> tuple[list[IdeaEntryFragment], list[dict[str, object]]]:
    profile_key = _profile_key(format_profile_ref)
    if profile_key is None:
        return legacy_idea_entry_fragments(payload), [
            _diag(
                "warning",
                "idea_source_legacy_heuristic",
                "No format profile was available; using legacy idea-entry key heuristics.",
                record_id=record_id,
            )
        ]
    section_paths = IDEA_ENTRY_SECTION_PATHS.get(profile_key)
    if section_paths is None:
        return [], [
            _diag(
                "warning",
                "idea_source_profile_mapping_missing",
                f"No idea-bearing section mapping is declared for profile: {format_profile_ref}",
                record_id=record_id,
                format_profile_ref=format_profile_ref,
            )
        ]
    fragments: list[IdeaEntryFragment] = []
    diagnostics: list[dict[str, object]] = []
    for section_path in section_paths:
        section, unresolved = extract_json_path(payload, section_path)
        if unresolved:
            continue
        if isinstance(section, list):
            for index, item in enumerate(section):
                if isinstance(item, Mapping):
                    fragments.append(IdeaEntryFragment(source_json_path=f"{section_path}[{index}]", source_json=dict(item)))
        elif isinstance(section, Mapping):
            fragments.append(IdeaEntryFragment(source_json_path=section_path, source_json=dict(section)))
    if not fragments:
        diagnostics.append(
            _diag(
                "warning",
                "idea_source_entries_missing",
                "No idea entries were found in the declared profile idea-bearing sections.",
                record_id=record_id,
                format_profile_ref=format_profile_ref,
            )
        )
    return fragments, diagnostics


def legacy_idea_entry_fragments(payload: Mapping[str, object]) -> list[IdeaEntryFragment]:
    fragments: list[IdeaEntryFragment] = []
    for path, value in _walk_mapping(payload):
        key = path.rsplit(".", 1)[-1].replace("[]", "")
        if key not in {"raw_ideas", "candidate_ideas", "ideas", "selected_hypothesis", "hypotheses"}:
            continue
        items = value if isinstance(value, list) else [value]
        for index, item in enumerate(items):
            if isinstance(item, Mapping):
                source_path = f"{path}[{index}]" if isinstance(value, list) else path
                fragments.append(IdeaEntryFragment(source_json_path=source_path, source_json=dict(item)))
    return fragments


IDEA_ENTRY_SECTION_PATHS: dict[str, tuple[str, ...]] = {
    "report/raw-idea-slate": ("$.sections.raw_ideas",),
    "report/candidate-idea-frontier": ("$.sections.serious_candidates", "$.sections.candidate_ideas"),
    "decision/rejected-and-deferred-ideas": (
        "$.sections.rejected_ideas",
        "$.sections.deferred_ideas",
        "$.sections.rejected_and_deferred_ideas",
    ),
    "draft/pre-idea-draft": ("$.sections",),
    "handoff/selected-hypothesis": ("$.sections",),
    "draft/selected-idea-draft": ("$.sections",),
    "decision/idea-route-decision": ("$.sections.selected_idea", "$.sections.idea"),
    "draft/paper-outline-seed": ("$.sections",),
    "report/research-outline-note": ("$.sections",),
    "paper/outline/idea": ("$.sections",),
}

CONTEXT_SECTION_PATHS: dict[str, tuple[str, ...]] = {
    "report/raw-idea-slate": ("$.sections.filter_notes",),
    "report/candidate-idea-frontier": ("$.sections.collapse_rationale",),
    "decision/rejected-and-deferred-ideas": ("$.sections.filter_notes", "$.sections.rationale"),
    "decision/idea-route-decision": ("$.sections.route_context", "$.sections.rationale"),
}


def _profile_key(format_profile_ref: str | None) -> str | None:
    if not format_profile_ref:
        return None
    if "/record-format/profile/" in format_profile_ref:
        suffix = format_profile_ref.split("/record-format/profile/", 1)[1]
    elif "profile/" in format_profile_ref:
        suffix = format_profile_ref.split("profile/", 1)[1]
    else:
        suffix = format_profile_ref
    if suffix.endswith("/v1"):
        suffix = suffix[:-3]
    return suffix


def _is_context_path(format_profile_ref: str | None, source_json_path: str) -> bool:
    profile_key = _profile_key(format_profile_ref)
    if profile_key is None:
        return False
    prefixes = CONTEXT_SECTION_PATHS.get(profile_key, ())
    normalized = source_json_path.rstrip("]")
    return any(source_json_path == prefix or source_json_path.startswith(f"{prefix}.") or normalized.startswith(f"{prefix}[") for prefix in prefixes)


def _is_root_path(path: str | None) -> bool:
    return path in {None, "", "$"}


def _json_path_tokens(path: str) -> list[str | int]:
    tokens: list[str | int] = []
    for part in [item for item in path.split(".") if item]:
        head = re.match(r"^[^\[]+", part)
        if head:
            tokens.append(head.group(0))
        for index in re.findall(r"\[(\d+)\]", part):
            tokens.append(int(index))
    return tokens


def _walk_mapping(value: object, prefix: str = "$") -> list[tuple[str, object]]:
    result: list[tuple[str, object]] = [(prefix, value)]
    if isinstance(value, Mapping):
        for key, item in value.items():
            result.extend(_walk_mapping(item, f"{prefix}.{key}"))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            result.extend(_walk_mapping(item, f"{prefix}[{index}]"))
    return result


def _resolution(
    status: str,
    classification: str,
    source_json_path: str | None,
    source_json: object | None,
    severity: str,
    code: str,
    message: str,
    **details: object,
) -> SourceFragmentResolution:
    return SourceFragmentResolution(
        status=status,
        classification=classification,
        source_json_path=source_json_path,
        source_json=source_json,
        diagnostics=[_diag(severity, code, message, source_json_path=source_json_path, **details)],
    )


def _diag(severity: str, code: str, message: str, **details: object) -> dict[str, object]:
    payload: dict[str, object] = {
        "severity": severity,
        "code": code,
        "concept": "Research Idea Source JSON",
        "message": message,
    }
    payload.update({key: value for key, value in details.items() if value is not None})
    return payload
