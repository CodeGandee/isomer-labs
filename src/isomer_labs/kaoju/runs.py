"""Research Task and Run checkpoint service for Kaoju procedures."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping
import uuid

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.store import ResearchRecordRequest, create_record, show_record, update_record


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
        return {**payload, "operation": "checkpoint", "run_ref": run_id, "checkpoint_sequence": sequence, "affected_refs": [run_id]}

    def status(self, run_id: str) -> dict[str, object]:
        payload, _ = show_record(self.context, run_id, env=self.env)
        return {**payload, "operation": "status", "run_ref": run_id}

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
        return {**payload, "operation": "complete", "run_ref": run_id, "terminal_status": terminal_status, "affected_refs": [run_id]}

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
