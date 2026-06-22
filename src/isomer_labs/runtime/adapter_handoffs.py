"""Execution Adapter handoff runtime records."""

from __future__ import annotations

from dataclasses import dataclass, field


ADAPTER_HANDOFF_DISPATCH_STATUSES = ("sent", "failed", "blocked")
SIGNAL_OBSERVATION_STATUSES = ("observed", "candidate_completion", "failed", "stale")
HANDOFF_NORMALIZATION_STATUSES = ("accepted", "rejected", "blocked", "superseded", "repair_routed", "follow_up")


@dataclass(frozen=True)
class AdapterHandoffDispatchRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    handoff_id: str
    agent_team_instance_id: str
    source_agent_instance_id: str
    target_agent_instance_id: str
    adapter_id: str
    status: str
    command_run_ids: list[str]
    payload_ref_ids: list[str]
    diagnostics: list[dict[str, object]]
    created_at: str
    updated_at: str
    research_task_id: str | None = None
    run_id: str | None = None
    actor_ref: str | None = None
    expected_output_refs: list[str] = field(default_factory=list)
    completion_watcher_contract_refs: list[str] = field(default_factory=list)
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "handoff_id": self.handoff_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "source_agent_instance_id": self.source_agent_instance_id,
            "target_agent_instance_id": self.target_agent_instance_id,
            "adapter_id": self.adapter_id,
            "status": self.status,
            "command_run_ids": self.command_run_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "diagnostics": self.diagnostics,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "expected_output_refs": self.expected_output_refs,
            "completion_watcher_contract_refs": self.completion_watcher_contract_refs,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("research_task_id", self.research_task_id),
            ("run_id", self.run_id),
            ("actor_ref", self.actor_ref),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class SignalObservationRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    handoff_id: str
    agent_team_instance_id: str
    adapter_id: str
    observation_kind: str
    status: str
    summary: str
    command_run_ids: list[str]
    payload_ref_ids: list[str]
    diagnostics: list[dict[str, object]]
    observed_at: str
    run_id: str | None = None
    source_agent_instance_id: str | None = None
    target_agent_instance_id: str | None = None
    actor_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "handoff_id": self.handoff_id,
            "agent_team_instance_id": self.agent_team_instance_id,
            "adapter_id": self.adapter_id,
            "observation_kind": self.observation_kind,
            "status": self.status,
            "summary": self.summary,
            "command_run_ids": self.command_run_ids,
            "payload_ref_ids": self.payload_ref_ids,
            "diagnostics": self.diagnostics,
            "observed_at": self.observed_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (
            ("run_id", self.run_id),
            ("source_agent_instance_id", self.source_agent_instance_id),
            ("target_agent_instance_id", self.target_agent_instance_id),
            ("actor_ref", self.actor_ref),
        ):
            if value is not None:
                data[key] = value
        return data


@dataclass(frozen=True)
class HandoffNormalizationRecord:
    id: str
    research_topic_id: str
    topic_workspace_id: str
    handoff_id: str
    status: str
    rationale: str
    signal_observation_ids: list[str]
    output_artifact_refs: list[str]
    corrective_refs: list[str]
    payload_ref_ids: list[str]
    created_at: str
    run_id: str | None = None
    actor_ref: str | None = None
    provenance_refs: list[str] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": self.id,
            "research_topic_id": self.research_topic_id,
            "topic_workspace_id": self.topic_workspace_id,
            "handoff_id": self.handoff_id,
            "status": self.status,
            "rationale": self.rationale,
            "signal_observation_ids": self.signal_observation_ids,
            "output_artifact_refs": self.output_artifact_refs,
            "corrective_refs": self.corrective_refs,
            "payload_ref_ids": self.payload_ref_ids,
            "created_at": self.created_at,
            "provenance_refs": self.provenance_refs,
        }
        for key, value in (("run_id", self.run_id), ("actor_ref", self.actor_ref)):
            if value is not None:
                data[key] = value
        return data
