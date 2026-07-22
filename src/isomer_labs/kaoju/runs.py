"""Research Task and Run checkpoint service for Kaoju procedures."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping
import uuid

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.mindsets import (
    DEFAULT_KEYS,
    RECORD_SEMANTIC_ID,
    SOURCE_SEMANTIC_LABEL,
    mindset_source_child,
    validate_mindset_record,
)
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.store import ResearchRecordError, ResearchRecordRequest, create_record, show_record, update_record
from isomer_labs.workspace.path_resolution import resolve_semantic_path


TERMINAL_RUN_STATUSES = {"complete", "failed", "stopped", "cancelled"}


class KaojuRunService:
    """Create and transition durable procedure Runs."""

    def __init__(self, context: EffectiveTopicContext, *, env: Mapping[str, str], cwd: Path) -> None:
        self.context = context
        self.env = env
        self.cwd = cwd

    def begin(
        self,
        *,
        procedure_id: str,
        control_mode: str,
        input_refs: list[str],
        expected_output_refs: list[str],
        stage_id: str,
        research_task_id: str | None = None,
        run_id: str | None = None,
        resume_hint: str | None = None,
    ) -> dict[str, object]:
        task_id = research_task_id or f"research-task-{uuid.uuid4().hex[:12]}"
        if research_task_id is None:
            task_payload, _ = create_record(
                self.context,
                ResearchRecordRequest(
                    record_kind="research_task",
                    record_id=task_id,
                    status="active",
                    metadata={"procedure_id": procedure_id, "control_mode": control_mode, "expected_output_refs": expected_output_refs},
                ),
                env=self.env,
                cwd=self.cwd,
            )
            if task_payload.get("ok") is False:
                raise KaojuServiceError("research_task_begin_failed", "Research Task creation failed.")
        selected_run_id = run_id or f"run-{uuid.uuid4().hex[:12]}"
        metadata: dict[str, object] = {
            "procedure_id": procedure_id,
            "control_mode": control_mode,
            "input_refs": input_refs,
            "expected_output_refs": expected_output_refs,
            "stage_id": stage_id,
            "completed_refs": [],
            "pending_gate_ref": None,
            "blocker_refs": [],
            "service_request_refs": [],
            "terminal_status": "running",
            "resume_hint": resume_hint,
            "checkpoint_sequence": 0,
        }
        payload, _ = create_record(
            self.context,
            ResearchRecordRequest(
                record_kind="run",
                record_id=selected_run_id,
                status="running",
                lifecycle_refs={"research_task_id": task_id},
                metadata=metadata,
            ),
            env=self.env,
            cwd=self.cwd,
        )
        if payload.get("ok") is False:
            raise KaojuServiceError("run_begin_failed", "Run creation failed.")
        return {**payload, "operation": "begin", "research_task_ref": task_id, "run_ref": selected_run_id, "affected_refs": [task_id, selected_run_id]}

    def resolve_mindset(
        self,
        run_id: str,
        *,
        mindset_key: str,
        record_ref: str | None,
        source_missing: bool,
    ) -> dict[str, object]:
        """Persist one verified, immutable mindset posture on an active Run."""

        if mindset_key not in DEFAULT_KEYS:
            raise KaojuServiceError(
                "mindset_key_invalid",
                f"Mindset key must be one of: {', '.join(DEFAULT_KEYS)}.",
            )
        if (record_ref is not None) == source_missing:
            raise KaojuServiceError(
                "mindset_resolution_mode_invalid",
                "Select exactly one mindset resolution mode: --record-ref or --source-missing.",
            )
        run = self._run_record(run_id)
        if run["status"] in TERMINAL_RUN_STATUSES:
            raise KaojuServiceError("run_terminal", f"Run {run_id} is terminal and immutable.")
        metadata = run["transition_metadata"]
        assert isinstance(metadata, dict)
        existing = metadata.get("mindset_resolution")
        if existing is not None:
            if not self._resolution_request_matches(
                existing,
                mindset_key=mindset_key,
                record_ref=record_ref,
                source_missing=source_missing,
            ):
                raise KaojuServiceError(
                    "mindset_resolution_conflict",
                    f"Run {run_id} already has a different immutable mindset resolution.",
                )
            return {
                "ok": True,
                "mutated": False,
                "operation": "resolve-mindset",
                "run_ref": run_id,
                "record": run,
                "mindset_resolution": existing,
                "affected_refs": [run_id],
            }
        resolution = (
            self._missing_mindset_resolution(mindset_key)
            if source_missing
            else self._recorded_mindset_resolution(run_id, mindset_key, str(record_ref))
        )
        input_refs = [str(value) for value in metadata.get("input_refs", [])] if isinstance(metadata.get("input_refs"), list) else []
        if record_ref is not None and record_ref not in input_refs:
            input_refs.append(record_ref)
        payload, _ = update_record(
            self.context,
            run_id,
            ResearchRecordRequest(
                record_kind="run",
                status=str(run["status"]),
                metadata={"mindset_resolution": resolution, "input_refs": input_refs},
            ),
            env=self.env,
            cwd=self.cwd,
        )
        if payload.get("ok") is False:
            raise KaojuServiceError("mindset_resolution_failed", f"Mindset resolution could not be persisted for Run {run_id}.")
        affected_refs = [run_id, record_ref] if record_ref is not None else [run_id]
        return {
            **payload,
            "operation": "resolve-mindset",
            "run_ref": run_id,
            "mindset_resolution": resolution,
            "affected_refs": affected_refs,
        }

    def checkpoint(
        self,
        run_id: str,
        *,
        stage_id: str,
        completed_refs: list[str],
        pending_gate_ref: str | None,
        blocker_refs: list[str],
        service_request_refs: list[str],
        resume_hint: str | None,
        status: str = "running",
    ) -> dict[str, object]:
        record = self._run_record(run_id)
        if record["status"] in TERMINAL_RUN_STATUSES:
            raise KaojuServiceError("run_terminal", f"Run {run_id} is terminal and immutable.")
        metadata = record["transition_metadata"]
        assert isinstance(metadata, dict)
        sequence = int(metadata.get("checkpoint_sequence", 0)) + 1
        payload, _ = update_record(
            self.context,
            run_id,
            ResearchRecordRequest(
                record_kind="run",
                status=status,
                metadata={
                    "stage_id": stage_id,
                    "completed_refs": completed_refs,
                    "pending_gate_ref": pending_gate_ref,
                    "blocker_refs": blocker_refs,
                    "service_request_refs": service_request_refs,
                    "terminal_status": status,
                    "resume_hint": resume_hint,
                    "checkpoint_sequence": sequence,
                },
            ),
            env=self.env,
            cwd=self.cwd,
        )
        if payload.get("ok") is False:
            raise KaojuServiceError("run_checkpoint_failed", f"Run checkpoint failed: {run_id}")
        return self._with_mindset_resolution({**payload, "operation": "checkpoint", "run_ref": run_id, "checkpoint_sequence": sequence, "affected_refs": [run_id]})

    def status(self, run_id: str) -> dict[str, object]:
        payload, _ = show_record(self.context, run_id, env=self.env)
        return self._with_mindset_resolution({**payload, "operation": "status", "run_ref": run_id})

    def complete(
        self,
        run_id: str,
        *,
        terminal_status: str,
        completed_refs: list[str],
        blocker_refs: list[str],
        resume_hint: str | None,
    ) -> dict[str, object]:
        if terminal_status not in TERMINAL_RUN_STATUSES:
            raise KaojuServiceError("run_terminal_status_invalid", f"Unsupported terminal Run status: {terminal_status}")
        record = self._run_record(run_id)
        if record["status"] in TERMINAL_RUN_STATUSES:
            raise KaojuServiceError("run_terminal", f"Run {run_id} is already terminal and immutable.")
        payload, _ = update_record(
            self.context,
            run_id,
            ResearchRecordRequest(
                record_kind="run",
                status=terminal_status,
                metadata={
                    "completed_refs": completed_refs,
                    "blocker_refs": blocker_refs,
                    "terminal_status": terminal_status,
                    "resume_hint": resume_hint,
                    "checkpoint_sequence": _checkpoint_sequence(record) + 1,
                },
            ),
            env=self.env,
            cwd=self.cwd,
        )
        if payload.get("ok") is False:
            raise KaojuServiceError("run_complete_failed", f"Run completion failed: {run_id}")
        return self._with_mindset_resolution({**payload, "operation": "complete", "run_ref": run_id, "terminal_status": terminal_status, "affected_refs": [run_id]})

    def _missing_mindset_resolution(self, mindset_key: str) -> dict[str, str]:
        root, diagnostics = resolve_semantic_path(self.context, SOURCE_SEMANTIC_LABEL, env=self.env, cwd=self.cwd)
        if root is None:
            detail = "; ".join(item.message for item in diagnostics) or "semantic path could not be resolved"
            raise KaojuServiceError(
                "mindset_source_resolution_failed",
                f"Mindset Source root could not be resolved: {detail}",
            )
        source_path = mindset_source_child(root.path, mindset_key)
        if source_path.exists() or source_path.is_symlink():
            raise KaojuServiceError(
                "mindset_source_not_missing",
                f"Mindset Source path exists and cannot be recorded as missing: {source_path}",
                ("Validate or repair the existing Source through Kaoju create-topic.",),
            )
        return {
            "disposition": "skipped_source_missing",
            "mindset_key": mindset_key,
            "source_semantic_label": SOURCE_SEMANTIC_LABEL,
            "source_relative_path": f"{mindset_key}.json",
            "source_status": "missing",
            "record_status": "absent",
            "reason": "source_missing",
        }

    def _recorded_mindset_resolution(self, run_id: str, mindset_key: str, record_ref: str) -> dict[str, str]:
        try:
            payload, _ = show_record(self.context, record_ref, env=self.env, include_payload=True)
        except ResearchRecordError as exc:
            raise KaojuServiceError("mindset_record_not_found", f"Mindset Record not found: {record_ref}") from exc
        record = payload.get("record")
        if not isinstance(record, dict):
            raise KaojuServiceError("mindset_record_not_found", f"Mindset Record not found: {record_ref}")
        metadata = record.get("transition_metadata")
        if (
            record.get("record_kind") != "artifact"
            or not isinstance(metadata, dict)
            or metadata.get("semantic_id") != RECORD_SEMANTIC_ID
            or metadata.get("scope_key") != run_id
        ):
            raise KaojuServiceError(
                "mindset_record_identity_mismatch",
                f"Record {record_ref!r} must be a {RECORD_SEMANTIC_ID} Artifact scoped to Run {run_id!r}.",
            )
        structured = payload.get("structured_payload")
        document = structured.get("payload") if isinstance(structured, dict) else None
        sections = document.get("sections") if isinstance(document, dict) else None
        source_snapshot = sections.get("source_snapshot") if isinstance(sections, dict) else None
        survey_context = sections.get("survey_context") if isinstance(sections, dict) else None
        if (
            not isinstance(document, dict)
            or not isinstance(source_snapshot, dict)
            or source_snapshot.get("mindset_key") != mindset_key
            or source_snapshot.get("semantic_label") != SOURCE_SEMANTIC_LABEL
            or source_snapshot.get("relative_path") != f"{mindset_key}.json"
            or not isinstance(survey_context, dict)
            or survey_context.get("run_ref") != run_id
        ):
            raise KaojuServiceError(
                "mindset_record_snapshot_mismatch",
                f"Mindset Record {record_ref!r} does not snapshot key {mindset_key!r} for Run {run_id!r}.",
            )
        record_diagnostics = validate_mindset_record(document)
        if record_diagnostics:
            detail = "; ".join(item.message for item in record_diagnostics)
            raise KaojuServiceError("mindset_record_invalid", f"Mindset Record {record_ref!r} is invalid: {detail}")
        return {
            "disposition": "recorded",
            "mindset_key": mindset_key,
            "source_semantic_label": SOURCE_SEMANTIC_LABEL,
            "source_relative_path": f"{mindset_key}.json",
            "source_status": "present",
            "record_status": "available",
            "record_ref": record_ref,
        }

    @staticmethod
    def _with_mindset_resolution(payload: dict[str, object]) -> dict[str, object]:
        record = payload.get("record")
        metadata = record.get("transition_metadata") if isinstance(record, dict) else None
        resolution = metadata.get("mindset_resolution") if isinstance(metadata, dict) else None
        if isinstance(resolution, dict):
            payload["mindset_resolution"] = resolution
        return payload

    @staticmethod
    def _resolution_request_matches(
        existing: object,
        *,
        mindset_key: str,
        record_ref: str | None,
        source_missing: bool,
    ) -> bool:
        if not isinstance(existing, dict) or existing.get("mindset_key") != mindset_key:
            return False
        if source_missing:
            return existing.get("disposition") == "skipped_source_missing" and existing.get("record_status") == "absent"
        return (
            existing.get("disposition") == "recorded"
            and existing.get("record_status") == "available"
            and existing.get("record_ref") == record_ref
        )

    def _run_record(self, run_id: str) -> dict[str, object]:
        payload, _ = show_record(self.context, run_id, env=self.env)
        record = payload.get("record")
        if not isinstance(record, dict) or record.get("record_kind") != "run":
            raise KaojuServiceError("run_not_found", f"Run not found: {run_id}")
        metadata = record.get("transition_metadata")
        if not isinstance(metadata, dict):
            record["transition_metadata"] = {}
        return record


def _checkpoint_sequence(record: dict[str, object]) -> int:
    metadata = record.get("transition_metadata")
    if not isinstance(metadata, dict):
        return 0
    return int(metadata.get("checkpoint_sequence", 0))
