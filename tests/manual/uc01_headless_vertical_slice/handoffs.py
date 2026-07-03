"""Simulated handoff helpers for the UC-01 manual harness."""

from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path

from isomer_labs.houmao.manifests import HOUMAO_ADAPTER_ID
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.records import _provenance_ref, _slug
from isomer_labs.runtime.records import (
    AdapterCommandRunRecord,
    AdapterHandoffDispatchRecord,
    AdapterPayloadRefRecord,
    HandoffNormalizationRecord,
    HandoffRecord,
    RuntimeLifecycleRecord,
    SignalObservationRecord,
    utc_timestamp,
)
from isomer_labs.runtime.store import WorkspaceRuntimeStore

from uc01_headless_vertical_slice.constants import UC01_RESEARCH_TASK_ID, UC01_SEED_INQUIRY_ID


def write_handoff_round(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    team_id: str,
    source_agent_id: str,
    target_agent_id: str,
    stage: str,
    actor_ref: str,
) -> dict[str, list[str]]:
    now = utc_timestamp()
    task_id = f"research-task-uc01-{_slug(stage)}"
    run_id = f"run-uc01-{_slug(stage)}"
    handoff_id = f"handoff-uc01-{_slug(stage)}"
    store.upsert_lifecycle_record(
        RuntimeLifecycleRecord(
            id=task_id,
            record_kind="research_task",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="complete",
            created_at=now,
            updated_at=now,
            lifecycle_refs={"research_inquiry_id": UC01_SEED_INQUIRY_ID, "parent_research_task_id": UC01_RESEARCH_TASK_ID},
            transition_metadata={"uc01": True, "workflow_stage": stage},
            provenance_refs=[_provenance_ref("research-task", task_id)],
        )
    )
    store.upsert_lifecycle_record(
        RuntimeLifecycleRecord(
            id=run_id,
            record_kind="run",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            status="complete",
            created_at=now,
            updated_at=now,
            lifecycle_refs={"research_task_id": task_id, "agent_team_instance_id": team_id, "handoff_id": handoff_id},
            transition_metadata={"uc01": True, "workflow_stage": stage, "normalization": "accepted"},
            provenance_refs=[_provenance_ref("run", run_id)],
        )
    )
    payload_path = context.topic_workspace_path / "logs" / "uc01" / f"{stage}-simulated-adapter-payload.json"
    payload: dict[str, object] = {
        "stage": stage,
        "status": "candidate_completion",
        "source_agent_instance_id": source_agent_id,
        "target_agent_instance_id": target_agent_id,
        "expected_output_refs": expected_outputs_for_stage(stage),
    }
    digest = _write_json(payload_path, payload)
    payload_ref = f"adapter-payload-uc01-{_slug(stage)}"
    command_ref = f"adapter-command-uc01-{_slug(stage)}"
    store.record_adapter_payload_ref(
        AdapterPayloadRefRecord(
            id=payload_ref,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            agent_team_instance_id=team_id,
            agent_instance_id=target_agent_id,
            adapter_id=HOUMAO_ADAPTER_ID,
            payload_kind="simulated_handoff_result",
            payload_path=str(payload_path),
            payload_digest=digest,
            source="uc01-adapter-simulated",
            command_run_id=command_ref,
            path_plan_id=None,
            created_at=now,
            provenance_refs=[_provenance_ref("adapter-payload", payload_ref)],
        )
    )
    store.record_adapter_command_run(
        AdapterCommandRunRecord(
            id=command_ref,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            agent_team_instance_id=team_id,
            agent_instance_id=target_agent_id,
            adapter_id=HOUMAO_ADAPTER_ID,
            operation_kind=f"uc01_simulated_{_slug(stage)}",
            argv=["isomer-simulated-houmao", "handoff", stage],
            cwd=str(context.topic_workspace_path),
            env_hints={"mode": "simulated"},
            status="succeeded",
            returncode=0,
            started_at=now,
            finished_at=now,
            duration_seconds=0.0,
            payload_ref_ids=[payload_ref],
            diagnostics=[],
            actor_ref=actor_ref,
            provenance_refs=[_provenance_ref("adapter-command", command_ref)],
        )
    )
    store.record_handoff(
        HandoffRecord(
            id=handoff_id,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            source_actor_ref=source_agent_id,
            target_actor_ref=target_agent_id,
            status="complete",
            research_task_id=task_id,
            run_id=run_id,
            agent_team_instance_id=team_id,
            completion_watcher_contract_refs=["completion-watcher:uc01-manual-normalization"],
            expected_output_refs=expected_outputs_for_stage(stage),
            created_at=now,
            updated_at=now,
            provenance_refs=[_provenance_ref("handoff", handoff_id)],
        )
    )
    store.record_adapter_handoff_dispatch(
        AdapterHandoffDispatchRecord(
            id=f"adapter-dispatch-uc01-{_slug(stage)}",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            handoff_id=handoff_id,
            agent_team_instance_id=team_id,
            source_agent_instance_id=source_agent_id,
            target_agent_instance_id=target_agent_id,
            adapter_id=HOUMAO_ADAPTER_ID,
            status="sent",
            research_task_id=task_id,
            run_id=run_id,
            command_run_ids=[command_ref],
            payload_ref_ids=[payload_ref],
            expected_output_refs=expected_outputs_for_stage(stage),
            completion_watcher_contract_refs=["completion-watcher:uc01-manual-normalization"],
            diagnostics=[],
            actor_ref=actor_ref,
            created_at=now,
            updated_at=now,
            provenance_refs=[_provenance_ref("adapter-dispatch", handoff_id)],
        )
    )
    store.record_signal_observation(
        SignalObservationRecord(
            id=f"signal-observation-uc01-{_slug(stage)}",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            handoff_id=handoff_id,
            run_id=run_id,
            agent_team_instance_id=team_id,
            source_agent_instance_id=source_agent_id,
            target_agent_instance_id=target_agent_id,
            adapter_id=HOUMAO_ADAPTER_ID,
            observation_kind="file",
            status="candidate_completion",
            summary=f"Simulated UC-01 {stage} handoff completed.",
            command_run_ids=[command_ref],
            payload_ref_ids=[payload_ref],
            diagnostics=[],
            actor_ref=actor_ref,
            observed_at=now,
            provenance_refs=[_provenance_ref("signal-observation", handoff_id)],
        )
    )
    store.record_handoff_normalization(
        HandoffNormalizationRecord(
            id=f"handoff-normalization-uc01-{_slug(stage)}",
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            handoff_id=handoff_id,
            run_id=run_id,
            status="accepted",
            rationale=f"Deterministic UC-01 {stage} output accepted for fixture validation.",
            signal_observation_ids=[f"signal-observation-uc01-{_slug(stage)}"],
            output_artifact_refs=artifact_outputs_for_stage(stage),
            corrective_refs=[],
            payload_ref_ids=[payload_ref],
            actor_ref=actor_ref,
            created_at=now,
            provenance_refs=[_provenance_ref("handoff-normalization", handoff_id)],
        )
    )
    return {"payload_refs": [payload_ref], "command_refs": [command_ref]}


def expected_outputs_for_stage(stage: str) -> list[str]:
    if stage == "scout":
        return [
            "artifact-uc01-seed-source-summary",
            "artifact-uc01-flash-attention-implementation-notes",
            "artifact-uc01-gb10-feature-notes",
            "evidence-uc01-gb10-feature-map",
        ]
    return [
        "artifact-uc01-review-notes",
        "artifact-uc01-follow-up-inquiry-options",
        "finding-uc01-memory-hierarchy-factor",
        "finding-uc01-tensor-core-precision-factor",
    ]


def artifact_outputs_for_stage(stage: str) -> list[str]:
    return [ref for ref in expected_outputs_for_stage(stage) if ref.startswith("artifact-")]


def _write_text(path: Path, content: str) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return sha256(content.encode("utf-8")).hexdigest()


def _write_json(path: Path, payload: dict[str, object]) -> str:
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    return _write_text(path, text)

