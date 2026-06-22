"""Validation checks for Execution Adapter handoff records."""

from __future__ import annotations

from typing import Mapping

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.runtime.store import WorkspaceRuntimeStore
from isomer_labs.runtime.validation_utils import missing_ref_diagnostics, owner_diagnostics


def validate_adapter_handoff_records(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    handoffs: Mapping[str, object],
    teams: set[str],
    agents: set[str],
    command_runs: Mapping[str, object],
    payload_refs: Mapping[str, object],
    lifecycle_by_kind: Mapping[str, set[str]],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    signal_observations = {record.id: record for record in store.list_signal_observations()}
    diagnostics.extend(
        _validate_dispatches(
            context,
            store,
            handoffs=handoffs,
            teams=teams,
            agents=agents,
            command_runs=command_runs,
            payload_refs=payload_refs,
            lifecycle_by_kind=lifecycle_by_kind,
        )
    )
    diagnostics.extend(
        _validate_signal_observations(
            context,
            store,
            handoffs=handoffs,
            teams=teams,
            agents=agents,
            command_runs=command_runs,
            payload_refs=payload_refs,
            lifecycle_by_kind=lifecycle_by_kind,
        )
    )
    diagnostics.extend(
        _validate_normalizations(
            context,
            store,
            handoffs=handoffs,
            signal_observations=signal_observations,
            payload_refs=payload_refs,
            lifecycle_by_kind=lifecycle_by_kind,
        )
    )
    return diagnostics


def _validate_dispatches(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    handoffs: Mapping[str, object],
    teams: set[str],
    agents: set[str],
    command_runs: Mapping[str, object],
    payload_refs: Mapping[str, object],
    lifecycle_by_kind: Mapping[str, set[str]],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for dispatch in store.list_adapter_handoff_dispatches():
        diagnostics.extend(owner_diagnostics(context, store.db_path, dispatch.id, dispatch.research_topic_id, dispatch.topic_workspace_id))
        if dispatch.handoff_id not in handoffs:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter handoff dispatch",
                    path=store.db_path,
                    field=dispatch.id,
                    message="Adapter handoff dispatch points to a missing handoff.",
                )
            )
        if dispatch.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter handoff dispatch",
                    path=store.db_path,
                    field=dispatch.id,
                    message="Adapter handoff dispatch points to a missing Agent Team Instance.",
                )
            )
        for agent_id, label in (
            (dispatch.source_agent_instance_id, "source Agent Instance"),
            (dispatch.target_agent_instance_id, "target Agent Instance"),
        ):
            if agent_id not in agents:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Execution Adapter handoff dispatch",
                        path=store.db_path,
                        field=dispatch.id,
                        message=f"Adapter handoff dispatch points to a missing {label}: {agent_id}.",
                    )
                )
        diagnostics.extend(missing_ref_diagnostics(store.db_path, "Execution Adapter handoff dispatch", dispatch.id, "command", dispatch.command_run_ids, command_runs))
        diagnostics.extend(missing_ref_diagnostics(store.db_path, "Execution Adapter handoff dispatch", dispatch.id, "payload", dispatch.payload_ref_ids, payload_refs))
        if dispatch.run_id is not None and dispatch.run_id not in lifecycle_by_kind.get("run", set()):
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter handoff dispatch",
                    path=store.db_path,
                    field=dispatch.id,
                    message="Adapter handoff dispatch points to a missing Run.",
                )
            )
        if dispatch.research_task_id is not None and dispatch.research_task_id not in lifecycle_by_kind.get("research_task", set()):
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter handoff dispatch",
                    path=store.db_path,
                    field=dispatch.id,
                    message="Adapter handoff dispatch points to a missing Research Task.",
                )
            )
        if dispatch.status in {"failed", "blocked"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO075",
                    severity="warning",
                    concept="Execution Adapter handoff dispatch",
                    path=store.db_path,
                    field=dispatch.id,
                    message=f"Adapter handoff dispatch is {dispatch.status}; observe or repair before treating it as current.",
                )
            )
    return diagnostics


def _validate_signal_observations(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    handoffs: Mapping[str, object],
    teams: set[str],
    agents: set[str],
    command_runs: Mapping[str, object],
    payload_refs: Mapping[str, object],
    lifecycle_by_kind: Mapping[str, set[str]],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for observation in store.list_signal_observations():
        diagnostics.extend(owner_diagnostics(context, store.db_path, observation.id, observation.research_topic_id, observation.topic_workspace_id))
        if observation.handoff_id not in handoffs:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Signal Observation",
                    path=store.db_path,
                    field=observation.id,
                    message="Signal Observation points to a missing handoff.",
                )
            )
        if observation.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Signal Observation",
                    path=store.db_path,
                    field=observation.id,
                    message="Signal Observation points to a missing Agent Team Instance.",
                )
            )
        for observed_agent_id in (observation.source_agent_instance_id, observation.target_agent_instance_id):
            if observed_agent_id is not None and observed_agent_id not in agents:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Signal Observation",
                        path=store.db_path,
                        field=observation.id,
                        message=f"Signal Observation points to a missing Agent Instance: {observed_agent_id}.",
                    )
                )
        diagnostics.extend(missing_ref_diagnostics(store.db_path, "Signal Observation", observation.id, "command", observation.command_run_ids, command_runs))
        diagnostics.extend(missing_ref_diagnostics(store.db_path, "Signal Observation", observation.id, "payload", observation.payload_ref_ids, payload_refs))
        if observation.run_id is not None and observation.run_id not in lifecycle_by_kind.get("run", set()):
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Signal Observation",
                    path=store.db_path,
                    field=observation.id,
                    message="Signal Observation points to a missing Run.",
                )
            )
        if observation.status in {"failed", "stale"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO075",
                    severity="warning",
                    concept="Signal Observation",
                    path=store.db_path,
                    field=observation.id,
                    message=f"Signal Observation is {observation.status}; normalization should not treat it as accepted completion.",
                )
            )
    return diagnostics


def _validate_normalizations(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    handoffs: Mapping[str, object],
    signal_observations: Mapping[str, object],
    payload_refs: Mapping[str, object],
    lifecycle_by_kind: Mapping[str, set[str]],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for normalization in store.list_handoff_normalizations():
        diagnostics.extend(owner_diagnostics(context, store.db_path, normalization.id, normalization.research_topic_id, normalization.topic_workspace_id))
        if normalization.handoff_id not in handoffs:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Handoff normalization",
                    path=store.db_path,
                    field=normalization.id,
                    message="Handoff normalization points to a missing handoff.",
                )
            )
        diagnostics.extend(missing_ref_diagnostics(store.db_path, "Handoff normalization", normalization.id, "Signal Observation", normalization.signal_observation_ids, signal_observations))
        diagnostics.extend(missing_ref_diagnostics(store.db_path, "Handoff normalization", normalization.id, "payload", normalization.payload_ref_ids, payload_refs))
        if normalization.run_id is not None and normalization.run_id not in lifecycle_by_kind.get("run", set()):
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Handoff normalization",
                    path=store.db_path,
                    field=normalization.id,
                    message="Handoff normalization points to a missing Run.",
                )
            )
        known_artifacts = lifecycle_by_kind.get("artifact", set())
        for artifact_ref in normalization.output_artifact_refs:
            if artifact_ref.startswith("artifact:") or artifact_ref in known_artifacts:
                continue
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="warning",
                    concept="Handoff normalization",
                    path=store.db_path,
                    field=normalization.id,
                    message=f"Handoff normalization output Artifact ref is not recorded as a lifecycle Artifact: {artifact_ref}.",
                )
            )
    return diagnostics
