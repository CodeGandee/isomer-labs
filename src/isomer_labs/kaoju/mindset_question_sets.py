"""Question-set contracts shared by Kaoju Mindset Sources and Records."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal, Mapping


SOURCE_SCHEMA_VERSION_V1 = "isomer-kaoju-mindset-source.v1"
SOURCE_SCHEMA_VERSION = "isomer-kaoju-mindset-source.v2"
SOURCE_SCHEMA_RESOURCES = {
    SOURCE_SCHEMA_VERSION_V1: "resources/mindset-source.v1.schema.json",
    SOURCE_SCHEMA_VERSION: "resources/mindset-source.v2.schema.json",
}
DEFAULT_QUESTION_SET_ID = "default"
DEFAULT_TRIGGERING_CONDITION = "Use when no specialized question set matches the task and active Run context."
LEGACY_SELECTION_RATIONALE = "The legacy v1 Mindset Source exposes one flat question list, which Kaoju treats as the implicit default question set."

QuestionSetSelectionKind = Literal["matched", "default-fallback", "legacy-default"]


@dataclass(frozen=True)
class MindsetDiagnostic:
    """One stable Mindset Source or Record diagnostic."""

    code: str
    message: str
    location: str
    severity: str = "error"

    def to_json(self) -> dict[str, str]:
        return {
            "code": self.code,
            "message": self.message,
            "location": self.location,
            "severity": self.severity,
        }


def question_sets_for_source(source: Mapping[str, Any]) -> list[dict[str, Any]]:
    """Return explicit v2 sets or one non-mutating implicit v1 default set."""

    if source.get("schema_version") == SOURCE_SCHEMA_VERSION_V1:
        return [
            {
                "question_set_id": DEFAULT_QUESTION_SET_ID,
                "triggering_condition": None,
                "question_ids": "all",
            }
        ]
    return [dict(item) for item in source.get("question_sets", []) if isinstance(item, dict)]


def expanded_question_ids(source: Mapping[str, Any], question_set: Mapping[str, Any]) -> list[str]:
    """Expand one set's `all` shorthand or return its explicit order."""

    references = question_set.get("question_ids")
    if references == "all":
        return [
            str(question["question_id"])
            for question in source.get("questions", [])
            if isinstance(question, dict) and isinstance(question.get("question_id"), str)
        ]
    return [str(item) for item in references] if isinstance(references, list) else []


def materialized_question(question: Mapping[str, Any]) -> dict[str, Any]:
    """Create one unanswered immutable question-contract row."""

    return {
        "question_id": question["question_id"],
        "prompt": question["prompt"],
        "additional_notes": question["additional_notes"],
        "answer_expectation": question["answer_expectation"],
        "required_posture": question["required_posture"],
        "evidence_expectation": question["evidence_expectation"],
        "answer_state": "unanswered",
        "answer": None,
        "rationale": None,
        "evidence_refs": [],
    }


def question_contract(row: Mapping[str, Any]) -> dict[str, Any]:
    """Return immutable Source-owned fields from one materialized row."""

    return {key: row.get(key) for key in ("question_id", "prompt", "additional_notes", "answer_expectation", "required_posture", "evidence_expectation")}


def validate_question_set_selection(
    source: Mapping[str, Any],
    *,
    question_set_id: str | None = None,
    selection_kind: QuestionSetSelectionKind | None = None,
    rationale: str | None = None,
) -> dict[str, Any]:
    """Validate one agent-selected v2 set or normalize one legacy v1 Source."""

    source_schema_version = source.get("schema_version")
    if source_schema_version == SOURCE_SCHEMA_VERSION_V1:
        if question_set_id not in {None, DEFAULT_QUESTION_SET_ID}:
            raise ValueError("Legacy v1 Mindset Sources can select only the implicit 'default' question set.")
        if selection_kind not in {None, "legacy-default"}:
            raise ValueError("Legacy v1 Mindset Sources require selection kind 'legacy-default'.")
        selected_rationale = rationale if isinstance(rationale, str) and rationale.strip() else LEGACY_SELECTION_RATIONALE
        return {
            "question_set_id": DEFAULT_QUESTION_SET_ID,
            "selection_kind": "legacy-default",
            "triggering_condition": None,
            "rationale": selected_rationale,
        }
    if source_schema_version != SOURCE_SCHEMA_VERSION:
        raise ValueError(f"Unsupported Mindset Source schema version: {source_schema_version!r}.")
    if question_set_id is None:
        raise ValueError("Mindset Source v2 materialization requires one selected question_set_id.")
    if selection_kind is None:
        raise ValueError("Mindset Source v2 materialization requires one question-set selection kind.")
    if not isinstance(rationale, str) or not rationale.strip():
        raise ValueError("Mindset Source v2 materialization requires a nonempty question-set selection rationale.")
    question_sets = {
        str(item.get("question_set_id")): item
        for item in question_sets_for_source(source)
        if isinstance(item.get("question_set_id"), str)
    }
    selected = question_sets.get(question_set_id)
    if selected is None:
        raise ValueError(f"Selected question set {question_set_id!r} does not exist in the Mindset Source.")
    if question_set_id == DEFAULT_QUESTION_SET_ID and selection_kind != "default-fallback":
        raise ValueError("Question set 'default' requires selection kind 'default-fallback'.")
    if question_set_id != DEFAULT_QUESTION_SET_ID and selection_kind != "matched":
        raise ValueError("A specialized question set requires selection kind 'matched'.")
    return {
        "question_set_id": question_set_id,
        "selection_kind": selection_kind,
        "triggering_condition": selected["triggering_condition"],
        "rationale": rationale,
    }


def question_set_selection_diagnostics(source_snapshot: Mapping[str, Any]) -> list[MindsetDiagnostic]:
    """Validate additive question-set selection fields in a Record snapshot."""

    diagnostics: list[MindsetDiagnostic] = []
    source_schema_version = source_snapshot.get("source_schema_version")
    selection = source_snapshot.get("question_set_selection")
    if source_schema_version is None and selection is None:
        return diagnostics
    if source_schema_version not in SOURCE_SCHEMA_RESOURCES:
        diagnostics.append(
            MindsetDiagnostic(
                "mindset_record_source_schema_version_invalid",
                "Record Source schema version must identify a supported Mindset Source version.",
                "sections/source_snapshot/source_schema_version",
            )
        )
    if not isinstance(selection, dict):
        diagnostics.append(
            MindsetDiagnostic(
                "mindset_record_question_set_selection_missing",
                "Record Source snapshot with a schema version requires question_set_selection.",
                "sections/source_snapshot/question_set_selection",
            )
        )
        return diagnostics
    question_set_id = selection.get("question_set_id")
    selection_kind = selection.get("selection_kind")
    triggering_condition = selection.get("triggering_condition")
    rationale = selection.get("rationale")
    if not isinstance(rationale, str) or not rationale.strip():
        diagnostics.append(
            MindsetDiagnostic(
                "mindset_record_question_set_rationale_missing",
                "Question-set selection requires a nonempty rationale.",
                "sections/source_snapshot/question_set_selection/rationale",
            )
        )
    if source_schema_version == SOURCE_SCHEMA_VERSION_V1:
        if question_set_id != DEFAULT_QUESTION_SET_ID or selection_kind != "legacy-default" or triggering_condition is not None:
            diagnostics.append(
                MindsetDiagnostic(
                    "mindset_record_legacy_question_set_selection_invalid",
                    "Legacy v1 Source selection must use implicit set 'default', kind 'legacy-default', and a null triggering condition.",
                    "sections/source_snapshot/question_set_selection",
                )
            )
    elif source_schema_version == SOURCE_SCHEMA_VERSION:
        if not isinstance(triggering_condition, str) or not triggering_condition.strip():
            diagnostics.append(
                MindsetDiagnostic(
                    "mindset_record_question_set_condition_invalid",
                    "V2 Source selection must preserve a nonempty triggering condition.",
                    "sections/source_snapshot/question_set_selection/triggering_condition",
                )
            )
        if question_set_id == DEFAULT_QUESTION_SET_ID and selection_kind != "default-fallback":
            diagnostics.append(
                MindsetDiagnostic(
                    "mindset_record_question_set_selection_invalid",
                    "Question set 'default' requires selection kind 'default-fallback'.",
                    "sections/source_snapshot/question_set_selection",
                )
            )
        if isinstance(question_set_id, str) and question_set_id != DEFAULT_QUESTION_SET_ID and selection_kind != "matched":
            diagnostics.append(
                MindsetDiagnostic(
                    "mindset_record_question_set_selection_invalid",
                    "A specialized question set requires selection kind 'matched'.",
                    "sections/source_snapshot/question_set_selection",
                )
            )
    return diagnostics
