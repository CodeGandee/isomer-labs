"""Workspace Runtime inspection and validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
import json
from pathlib import Path
import re
import subprocess
from typing import Iterable, Mapping

from isomer_labs.artifact_formats import digest_bytes, digest_json, register_builtin_artifact_format_providers, validate_payload
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.core.path_utils import canonicalize, is_within
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.records.index import query_index_diagnostics_for_store
from isomer_labs.runtime.records import (
    AdapterManifestRefRecord,
    AdapterPayloadRefRecord,
    AgentWorkspaceRecord,
    PathPlanRecord,
    RuntimeLifecycleRecord,
)
from isomer_labs.runtime.store import (
    WorkspaceRuntimeStore,
    open_workspace_runtime,
    validate_global_agent_instance_id_uniqueness as _validate_global_agent_instance_id_uniqueness,
)
from isomer_labs.workspace.manifest import EffectiveAgentContext, resolve_semantic_binding
from isomer_labs.workspace.path_resolution import preview_paths, resolve_semantic_path
from isomer_labs.workspace.path_resolution import validate_agent_name_value
from isomer_labs.workspace.surfaces import TmpSurfaceIgnorePolicy, tmp_surface_ignore_policy

@dataclass(frozen=True)
class SemanticFileLocator:
    record_kind: str
    record_id: str
    path_field: str
    semantic_label: str
    resolved_path: Path
    relative_path: str
    surface_path: Path
    path_plan_id: str | None = None
    scope_ref: str | None = None
    storage_profile: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "record_kind": self.record_kind,
            "record_id": self.record_id,
            "path_field": self.path_field,
            "semantic_label": self.semantic_label,
            "resolved_path": str(self.resolved_path),
            "relative_path": self.relative_path,
            "surface_path": str(self.surface_path),
        }
        if self.path_plan_id is not None:
            data["path_plan_id"] = self.path_plan_id
        if self.scope_ref is not None:
            data["scope_ref"] = self.scope_ref
        if self.storage_profile is not None:
            data["storage_profile"] = self.storage_profile
        return data


def locate_semantic_file(
    path: Path,
    path_plans: Iterable[PathPlanRecord],
    *,
    record_kind: str,
    record_id: str,
    path_field: str,
) -> SemanticFileLocator | None:
    resolved_path = canonicalize(path)
    candidates: list[tuple[int, PathPlanRecord, Path]] = []
    for plan in path_plans:
        if plan.semantic_label is None:
            continue
        surface_path = canonicalize(Path(plan.path))
        if resolved_path == surface_path or is_within(resolved_path, surface_path):
            candidates.append((len(surface_path.parts), plan, surface_path))
    if not candidates:
        return None
    _, plan, surface_path = sorted(candidates, key=lambda item: item[0], reverse=True)[0]
    semantic_label = plan.semantic_label
    if semantic_label is None:
        return None
    try:
        relative_path = resolved_path.relative_to(surface_path)
    except ValueError:
        return None
    relative_text = "." if str(relative_path) == "." else relative_path.as_posix()
    return SemanticFileLocator(
        record_kind=record_kind,
        record_id=record_id,
        path_field=path_field,
        semantic_label=semantic_label,
        resolved_path=resolved_path,
        relative_path=relative_text,
        surface_path=surface_path,
        path_plan_id=plan.id,
        scope_ref=plan.scope_ref,
        storage_profile=plan.storage_profile,
    )


def runtime_semantic_file_locators(
    *,
    path_plans: Iterable[PathPlanRecord],
    lifecycle_records: Iterable[RuntimeLifecycleRecord],
    adapter_manifest_refs: Iterable[AdapterManifestRefRecord],
    adapter_payload_refs: Iterable[AdapterPayloadRefRecord],
) -> list[SemanticFileLocator]:
    plans = list(path_plans)
    locators: list[SemanticFileLocator] = []
    for lifecycle_record in lifecycle_records:
        if lifecycle_record.content_path is None:
            continue
        locator = locate_semantic_file(
            Path(lifecycle_record.content_path),
            plans,
            record_kind=lifecycle_record.record_kind,
            record_id=lifecycle_record.id,
            path_field="content_path",
        )
        if locator is not None:
            locators.append(locator)
    for manifest_ref in adapter_manifest_refs:
        locator = locate_semantic_file(
            Path(manifest_ref.manifest_path),
            plans,
            record_kind="adapter_manifest_ref",
            record_id=manifest_ref.id,
            path_field="manifest_path",
        )
        if locator is not None:
            locators.append(locator)
    for payload_ref in adapter_payload_refs:
        locator = locate_semantic_file(
            Path(payload_ref.payload_path),
            plans,
            record_kind="adapter_payload_ref",
            record_id=payload_ref.id,
            path_field="payload_path",
        )
        if locator is not None:
            locators.append(locator)
    return locators

def owner_diagnostics(
    context: EffectiveTopicContext,
    path: Path,
    record_id: str,
    research_topic_id: str,
    topic_workspace_id: str,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if research_topic_id != context.research_topic.id:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Workspace Runtime record",
                path=path,
                field=record_id,
                message="Runtime record references another Research Topic.",
            )
        )
    if topic_workspace_id != context.topic_workspace_id:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Workspace Runtime record",
                path=path,
                field=record_id,
                message="Runtime record references another Topic Workspace.",
            )
        )
    return diagnostics


def missing_ref_diagnostics(
    path: Path,
    concept: str,
    record_id: str,
    ref_kind: str,
    refs: list[str],
    known: Mapping[str, object],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for ref in refs:
        if ref not in known:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept=concept,
                    path=path,
                    field=record_id,
                    message=f"Record points to a missing adapter {ref_kind} ref: {ref}.",
                )
            )
    return diagnostics

def workspace_isomer_managed_path(
    workspace: AgentWorkspaceRecord,
    path_plans: Mapping[str, PathPlanRecord],
    workspace_path: Path,
) -> Path:
    if workspace.isomer_managed_path_plan_id is not None:
        plan = path_plans.get(workspace.isomer_managed_path_plan_id)
        if plan is not None:
            return Path(plan.path)
    if workspace.support_root_path is not None and ".isomer-agent" not in Path(workspace.support_root_path).parts:
        return Path(workspace.support_root_path)
    return workspace_path / "isomer-managed"


def missing_isomer_managed_support_paths(isomer_managed_path: Path) -> list[Path]:
    required = (
        "agent-owned/runtime",
        "agent-owned/artifacts",
        "agent-owned/scratch",
        "agent-owned/logs",
        "agent-owned/public",
        "agent-owned/inbox",
        "topic-owned/readonly",
        "topic-owned/writable",
        "links",
    )
    return [isomer_managed_path / relative for relative in required if not (isomer_managed_path / relative).exists()]


def unsafe_generated_link_diagnostics(
    context: EffectiveTopicContext,
    workspace: AgentWorkspaceRecord,
    isomer_managed_path: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    links_root = isomer_managed_path / "links"
    if not links_root.exists():
        return diagnostics
    pending = [links_root]
    while pending:
        current = pending.pop()
        try:
            children = list(current.iterdir())
        except OSError as exc:
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="warning",
                    concept="Agent Workspace generated links",
                    path=current,
                    field=workspace.id,
                    message=f"Could not inspect generated links: {exc}.",
                )
            )
            continue
        for child in children:
            if child.is_symlink():
                target = child.resolve(strict=False)
                if not is_within(target, context.topic_workspace_path):
                    diagnostics.append(
                        Diagnostic(
                            code="ISO044",
                            severity="error",
                            concept="Agent Workspace generated links",
                            path=child,
                            field=workspace.id,
                            message=(
                                "Generated `isomer-managed/links/` target points outside the selected "
                                "Topic Workspace without an accepted external-root contract."
                            ),
                        )
                    )
                continue
            if child.is_dir():
                pending.append(child)
    return diagnostics


def is_unpromoted_isomer_managed_dependency(path: Path) -> bool:
    parts = path.parts
    return _contains_parts(parts, ("isomer-managed", "agent-owned")) or _contains_parts(
        parts,
        ("isomer-managed", "topic-owned"),
    )


def _contains_parts(parts: tuple[str, ...], needle: tuple[str, ...]) -> bool:
    if len(parts) < len(needle):
        return False
    return any(parts[index : index + len(needle)] == needle for index in range(len(parts) - len(needle) + 1))

_missing_ref_diagnostics = missing_ref_diagnostics
_owner_diagnostics = owner_diagnostics

_is_unpromoted_isomer_managed_dependency = is_unpromoted_isomer_managed_dependency
_missing_isomer_managed_support_paths = missing_isomer_managed_support_paths
_unsafe_generated_link_diagnostics = unsafe_generated_link_diagnostics
_workspace_isomer_managed_path = workspace_isomer_managed_path


def validate_topic_workspace_visibility_layout(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    current_entries, path_diagnostics = preview_paths(context, env=env)
    diagnostics.extend(path_diagnostics)
    current_by_surface = {entry.surface: entry for entry in current_entries}
    required_surfaces = (
        "topic_main_repo",
        "agents",
        "records_artifacts",
        "records_tasks",
        "records_runs",
        "records_views",
        "records_logs",
        "runtime",
    )
    for surface in required_surfaces:
        entry = current_by_surface.get(surface)
        if entry is not None and not entry.path.exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO042",
                    severity="warning",
                    concept="Topic Workspace visibility layout",
                    path=entry.path,
                    field=surface,
                    message="Standard Topic Workspace visibility path is missing.",
                )
            )

    for legacy_name in ("shared", "artifacts", "tasks", "runs", "views", "logs"):
        legacy_path = context.topic_workspace_path / legacy_name
        if legacy_path.exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO042",
                    severity="warning",
                    concept="Topic Workspace visibility layout",
                    path=legacy_path,
                    field=legacy_name,
                    message=(
                        "Legacy root collaboration directory exists. Move worker-visible material into "
                        "`repos/topic-main` or owner-preserved material into `records/*` through explicit operator action."
                    ),
                )
            )
    return diagnostics

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

@dataclass(frozen=True)
class _ResolvedTmpSurface:
    label: str
    path: Path
    policy: TmpSurfaceIgnorePolicy
    agent_name: str | None = None


def _validate_metadata(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    metadata = store.metadata()
    if metadata.research_topic_id != context.research_topic.id:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Workspace Runtime",
                path=store.db_path,
                field="research_topic_id",
                message="Workspace Runtime metadata references another Research Topic.",
            )
        )
    if metadata.topic_workspace_id != context.topic_workspace_id:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Workspace Runtime",
                path=store.db_path,
                field="topic_workspace_id",
                message="Workspace Runtime metadata references another Topic Workspace.",
            )
        )
    return diagnostics


def _validate_path_plans(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    env: Mapping[str, str],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    current_entries, path_diagnostics = preview_paths(context, env=env)
    diagnostics.extend(path_diagnostics)
    current_by_surface = {entry.surface: entry for entry in current_entries}
    for plan in store.list_path_plans():
        if plan.topic_workspace_id != context.topic_workspace_id:
            diagnostics.append(
                Diagnostic(
                    code="ISO042",
                    severity="error",
                    concept="Workspace Runtime path plan",
                    path=store.db_path,
                    field=plan.surface,
                    message="Path plan belongs to another Topic Workspace.",
                )
            )
        current_path: Path | None = None
        if plan.semantic_label is not None:
            agent_name = _agent_name_from_scope_ref(plan.scope_ref)
            semantic_current, semantic_diagnostics = resolve_semantic_path(
                context,
                plan.semantic_label,
                env=env,
                cwd=context.topic_workspace_path,
                agent_name=agent_name,
                use_path_plan=False,
            )
            diagnostics.extend(semantic_diagnostics)
            if semantic_current is not None:
                current_path = semantic_current.path
            else:
                diagnostics.append(
                    Diagnostic(
                        code="ISO042",
                        severity="warning",
                        concept="Workspace Runtime path plan",
                        path=store.db_path,
                        field=plan.semantic_label,
                        message="Historical path plan remains, but the current semantic binding is missing.",
                    )
                )
        if current_path is None:
            current = current_by_surface.get(plan.surface)
            if current is not None:
                current_path = current.path
        if current_path is not None and str(current_path) != plan.path:
            diagnostics.append(
                Diagnostic(
                    code="ISO042",
                    severity="warning",
                    concept="Workspace Runtime path plan",
                    path=store.db_path,
                    field=plan.surface,
                    message="Stored path plan differs from current Workspace Path Resolution output.",
                )
            )
        if not Path(plan.path).exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO042",
                    severity="warning",
                    concept="Workspace Runtime path plan",
                    path=Path(plan.path),
                    field=plan.surface,
                    message="Stored path-plan target does not exist.",
                )
            )
    return diagnostics


def _validate_local_tmp_surfaces(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    env: Mapping[str, str],
    tmp_surfaces: tuple[_ResolvedTmpSurface, ...] | None = None,
) -> list[Diagnostic]:
    if tmp_surfaces is None:
        resolved_tmp_surfaces, diagnostics = _resolved_tmp_surfaces(context, store, env)
    else:
        resolved_tmp_surfaces = list(tmp_surfaces)
        diagnostics = []
    for surface in resolved_tmp_surfaces:
        if not surface.path.exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="warning",
                    concept="Local Tmp Surface",
                    path=surface.path,
                    field=surface.label,
                    message="Local Tmp Surface directory is missing; setup can recreate this disposable path.",
                )
            )
        diagnostics.extend(_tmp_ignore_policy_diagnostics(surface))
        diagnostics.extend(_tracked_tmp_content_diagnostics(surface))
    return diagnostics


def _resolved_tmp_surfaces(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    env: Mapping[str, str],
) -> tuple[list[_ResolvedTmpSurface], list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    surfaces: list[_ResolvedTmpSurface] = []
    for label in ("topic.tmp", "topic.repos.main.tmp"):
        result, result_diagnostics = resolve_semantic_path(
            context,
            label,
            env=env,
            cwd=context.topic_workspace_path,
            use_path_plan=False,
        )
        diagnostics.extend(result_diagnostics)
        if result is None:
            continue
        policy, policy_diagnostics = tmp_surface_ignore_policy(context, label, result.path, env=env)
        diagnostics.extend(policy_diagnostics)
        if policy is not None:
            surfaces.append(_ResolvedTmpSurface(label=label, path=result.path, policy=policy))

    path_plans = {record.id: record for record in store.list_path_plans()}
    for workspace in store.list_agent_workspaces():
        if workspace.agent_name is None:
            continue
        workspace_path = _workspace_path_for_agent_tmp(workspace, path_plans)
        agent_context = EffectiveAgentContext(
            agent_name=workspace.agent_name,
            agent_workspace_path=workspace_path,
            source="runtime-validation",
            agent_instance_id=workspace.agent_instance_id,
        )
        result, result_diagnostics = resolve_semantic_binding(
            context,
            "agent.tmp",
            env=env,
            agent_context=agent_context,
        )
        diagnostics.extend(result_diagnostics)
        if result is None:
            continue
        policy, policy_diagnostics = tmp_surface_ignore_policy(
            context,
            "agent.tmp",
            result.path,
            env=env,
            agent_context=agent_context,
        )
        diagnostics.extend(policy_diagnostics)
        if policy is not None:
            surfaces.append(_ResolvedTmpSurface(label="agent.tmp", path=result.path, policy=policy, agent_name=workspace.agent_name))
    return surfaces, diagnostics


def _workspace_path_for_agent_tmp(
    workspace: AgentWorkspaceRecord,
    path_plans: Mapping[str, PathPlanRecord],
) -> Path:
    plan = path_plans.get(workspace.path_plan_id)
    if plan is not None:
        return Path(plan.path)
    return Path(workspace.agent_name or "agent-name-required")


def _tmp_ignore_policy_diagnostics(surface: _ResolvedTmpSurface) -> list[Diagnostic]:
    if not surface.policy.gitignore_path.exists():
        return [
            Diagnostic(
                code="ISO044",
                severity="error",
                concept="Local Tmp Surface",
                path=surface.policy.gitignore_path,
                field=surface.label,
                message="Local Tmp Surface ignore policy is missing.",
            )
        ]
    entries = {
        line.strip()
        for line in surface.policy.gitignore_path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }
    if surface.policy.entry in entries:
        return []
    return [
        Diagnostic(
            code="ISO044",
            severity="error",
            concept="Local Tmp Surface",
            path=surface.policy.gitignore_path,
            field=surface.label,
            message=f"Local Tmp Surface ignore policy does not include `{surface.policy.entry}`.",
        )
    ]


def _tracked_tmp_content_diagnostics(surface: _ResolvedTmpSurface) -> list[Diagnostic]:
    tracked_paths = _tracked_paths_under(surface.policy.relative_root, surface.path)
    return [
        Diagnostic(
            code="ISO044",
            severity="error",
            concept="Local Tmp Surface",
            path=path,
            field=surface.label,
            message="Git tracks content under a Local Tmp Surface; tmp material must stay ignored unless promoted elsewhere.",
        )
        for path in tracked_paths
    ]


def _tracked_paths_under(worktree_root: Path, tmp_path: Path) -> list[Path]:
    git_metadata = worktree_root / ".git"
    if not git_metadata.exists():
        return []
    try:
        relative = tmp_path.resolve(strict=False).relative_to(worktree_root.resolve(strict=False))
    except ValueError:
        return []
    result = subprocess.run(
        ["git", "-C", str(worktree_root), "ls-files", "--", relative.as_posix()],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [worktree_root / line for line in result.stdout.splitlines() if line]


def _tmp_dependency_diagnostic(
    context: EffectiveTopicContext,
    tmp_surfaces: tuple[_ResolvedTmpSurface, ...],
    path: Path,
    *,
    concept: str,
    field: str,
) -> Diagnostic | None:
    candidate = path.expanduser()
    if not candidate.is_absolute():
        candidate = context.project.root / candidate
    candidate = candidate.resolve(strict=False)
    for surface in tmp_surfaces:
        if is_within(candidate, surface.path):
            return Diagnostic(
                code="ISO045",
                severity="warning",
                concept=concept,
                path=candidate,
                field=field,
                message=(
                    f"Runtime record depends on Local Tmp Surface `{surface.label}`; "
                    "promote the material to a durable semantic surface before treating it as evidence."
                ),
            )
    return None


def _missing_semantic_file_evidence_diagnostic(
    context: EffectiveTopicContext,
    path_plans: Iterable[PathPlanRecord],
    path: Path,
    *,
    concept: str,
    field: str,
    path_field: str,
) -> Diagnostic | None:
    candidate = path.expanduser()
    if not candidate.is_absolute():
        candidate = context.project.root / candidate
    candidate = canonicalize(candidate)
    if not is_within(candidate, context.project.root):
        return None
    locator = locate_semantic_file(
        candidate,
        path_plans,
        record_kind=concept,
        record_id=field,
        path_field=path_field,
    )
    if locator is not None:
        return None
    return Diagnostic(
        code="ISO045",
        severity="warning",
        concept=concept,
        path=candidate,
        field=field,
        message=(
            "Project-local file ref has no semantic file locator evidence; "
            "preserving the historical path for compatibility."
        ),
    )


def _agent_name_from_scope_ref(scope_ref: str | None) -> str | None:
    if scope_ref is None:
        return None
    if scope_ref.startswith("agent_name:"):
        return scope_ref.split(":", 1)[1]
    return None


def _validate_readiness(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    *,
    require_ready: bool,
    tmp_surfaces: tuple[_ResolvedTmpSurface, ...],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    readiness_records = store.list_readiness_records()
    for record in readiness_records:
        if record.research_topic_id != context.research_topic.id:
            diagnostics.append(
                Diagnostic(
                    code="ISO043",
                    severity="error",
                    concept="Topic Environment Readiness",
                    path=store.db_path,
                    field=record.id,
                    message="Readiness record references another Research Topic.",
                )
            )
        if record.topic_workspace_id != context.topic_workspace_id:
            diagnostics.append(
                Diagnostic(
                    code="ISO043",
                    severity="error",
                    concept="Topic Environment Readiness",
                    path=store.db_path,
                    field=record.id,
                    message="Readiness record references another Topic Workspace.",
                )
            )
        for ref in (*record.project_pixi_environment_refs, *record.standalone_pixi_manifest_refs):
            diagnostic = _tmp_dependency_diagnostic(
                context,
                tmp_surfaces,
                Path(ref),
                concept="Topic Environment Readiness",
                field=record.id,
            )
            if diagnostic is not None:
                diagnostics.append(diagnostic)
    latest = store.latest_readiness()
    if latest is None:
        diagnostics.append(
            Diagnostic(
                code="ISO043",
                severity="error" if require_ready else "warning",
                concept="Topic Environment Readiness",
                path=store.db_path,
                message="No Topic Environment Readiness record exists for this Workspace Runtime.",
            )
        )
    elif latest.status != "ready":
        diagnostics.append(
            Diagnostic(
                code="ISO043",
                severity="error" if require_ready else "warning",
                concept="Topic Environment Readiness",
                path=store.db_path,
                field=latest.id,
                message=f"Latest Topic Environment Readiness record is {latest.status}, not ready.",
            )
        )
    return diagnostics


def _validate_lifecycle_records(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    tmp_surfaces: tuple[_ResolvedTmpSurface, ...],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    record_ids: dict[str, set[str]] = {}
    records = store.list_lifecycle_records()
    path_plans = store.list_path_plans()
    for record in records:
        record_ids.setdefault(record.record_kind, set()).add(record.id)
    for record in records:
        diagnostics.extend(_owner_diagnostics(context, store.db_path, record.id, record.research_topic_id, record.topic_workspace_id))
        if record.record_kind == "artifact" and record.content_path is not None and not Path(record.content_path).exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="error",
                    concept="Artifact",
                    path=Path(record.content_path),
                    field=record.id,
                    message="Artifact record points to a missing file.",
                )
            )
        if record.content_path is not None and _is_unpromoted_isomer_managed_dependency(Path(record.content_path)):
            diagnostics.append(
                Diagnostic(
                    code="ISO045",
                    severity="warning",
                    concept="Workspace Runtime unpromoted dependency",
                    path=Path(record.content_path),
                    field=record.id,
                    message=(
                        "Runtime record depends on untracked `isomer-managed/agent-owned/` or "
                        "`isomer-managed/topic-owned/` material; promote it to tracked Isomer material, "
                        "owner-preserved records, or a Provenance Record before treating it as durable."
                    ),
                )
            )
        if record.content_path is not None:
            missing_evidence = _missing_semantic_file_evidence_diagnostic(
                context,
                path_plans,
                Path(record.content_path),
                concept=record.record_kind.replace("_", " ").title(),
                field=record.id,
                path_field="content_path",
            )
            if missing_evidence is not None:
                diagnostics.append(missing_evidence)
            diagnostic = _tmp_dependency_diagnostic(
                context,
                tmp_surfaces,
                Path(record.content_path),
                concept=record.record_kind.replace("_", " ").title(),
                field=record.id,
            )
            if diagnostic is not None:
                diagnostics.append(diagnostic)
        if record.record_kind == "gate" and record.status in {"open", "pending", "unresolved", "blocked"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO045",
                    severity="warning",
                    concept="Gate",
                    path=store.db_path,
                    field=record.id,
                    message="Gate remains unresolved in Workspace Runtime.",
                )
            )
        if record.record_kind == "research_claim" and record.status == "supported":
            evidence_refs = [
                value
                for key, value in record.lifecycle_refs.items()
                if key.startswith("evidence_item")
            ]
            evidence_records = record_ids.get("evidence_item", set())
            if not evidence_refs or any(ref not in evidence_records for ref in evidence_refs):
                diagnostics.append(
                    Diagnostic(
                        code="ISO045",
                        severity="error",
                        concept="Research Claim",
                        path=store.db_path,
                        field=record.id,
                        message="Supported Research Claim lacks a valid Evidence Item ref.",
                    )
                )
        if record.record_kind == "provenance_record" and record.status == "stale":
            diagnostics.append(
                Diagnostic(
                    code="ISO045",
                    severity="warning",
                    concept="Provenance Record",
                    path=store.db_path,
                    field=record.id,
                    message="Provenance Record is stale.",
                )
            )
    return diagnostics


def _validate_structured_research_payloads(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    register_builtin_artifact_format_providers()
    lifecycle_records = {record.id: record for record in store.list_lifecycle_records()}
    for registration in store.list_artifact_format_registrations(topic_workspace_id=context.topic_workspace_id):
        if registration.research_topic_id != context.research_topic.id:
            diagnostics.append(
                Diagnostic(
                    code="ISO206",
                    severity="error",
                    concept="Artifact Format Registration",
                    path=store.db_path,
                    field=registration.format_profile_ref,
                    message="Artifact Format registration belongs to another Research Topic.",
                )
            )
        for path_field_name, snapshot_path in (
            ("schema_snapshot_path", registration.schema_snapshot_path),
            ("template_snapshot_path", registration.template_snapshot_path),
        ):
            if snapshot_path is not None and not Path(snapshot_path).exists():
                diagnostics.append(
                    Diagnostic(
                        code="ISO206",
                        severity="error",
                        concept="Artifact Format Registration",
                        path=Path(snapshot_path),
                        field=path_field_name,
                        message="Artifact Format managed snapshot is missing.",
                    )
                )
    for payload in store.list_structured_payloads(topic_workspace_id=context.topic_workspace_id):
        if payload.research_topic_id != context.research_topic.id:
            diagnostics.append(
                Diagnostic(
                    code="ISO207",
                    severity="error",
                    concept="Structured Research Payload",
                    path=store.db_path,
                    field=payload.record_id,
                    message="Structured payload belongs to another Research Topic.",
                )
            )
        lifecycle_record = lifecycle_records.get(payload.record_id)
        if lifecycle_record is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO207",
                    severity="error",
                    concept="Structured Research Payload",
                    path=store.db_path,
                    field=payload.record_id,
                    message="Structured payload points to a missing lifecycle record.",
                )
            )
        elif (
            lifecycle_record.research_topic_id != payload.research_topic_id
            or lifecycle_record.topic_workspace_id != payload.topic_workspace_id
        ):
            diagnostics.append(
                Diagnostic(
                    code="ISO207",
                    severity="error",
                    concept="Structured Research Payload",
                    path=store.db_path,
                    field=payload.record_id,
                    message="Structured payload owner does not match the linked lifecycle record.",
                )
            )
        payload_json = payload.payload_json
        payload_path = Path(payload.payload_file_path) if payload.payload_file_path is not None else None
        if payload_path is not None:
            if not payload_path.exists() or not payload_path.is_file():
                diagnostics.append(
                    Diagnostic(
                        code="ISO208",
                        severity="error",
                        concept="Structured Research Payload",
                        path=payload_path,
                        field=payload.record_id,
                        message="Structured payload file is missing.",
                    )
                )
                payload_json = {}
            else:
                try:
                    loaded_payload = json.loads(payload_path.read_text(encoding="utf-8"))
                except json.JSONDecodeError as exc:
                    diagnostics.append(
                        Diagnostic(
                            code="ISO208",
                            severity="error",
                            concept="Structured Research Payload",
                            path=payload_path,
                            field=payload.record_id,
                            message=f"Structured payload file is not valid JSON: {exc.msg}.",
                        )
                    )
                    payload_json = {}
                else:
                    if not isinstance(loaded_payload, dict):
                        diagnostics.append(
                            Diagnostic(
                                code="ISO208",
                                severity="error",
                                concept="Structured Research Payload",
                                path=payload_path,
                                field=payload.record_id,
                                message="Structured payload file must contain a JSON object.",
                            )
                        )
                        payload_json = {}
                    else:
                        payload_json = {str(key): value for key, value in loaded_payload.items()}
        observed_payload_digest = digest_json(payload_json)
        if payload_json and observed_payload_digest != payload.payload_digest:
            diagnostics.append(
                Diagnostic(
                    code="ISO208",
                    severity="error",
                    concept="Structured Research Payload",
                    path=payload_path or store.db_path,
                    field=payload.record_id,
                    message="Structured payload digest does not match the recorded payload digest.",
                )
            )
        if payload.payload_manifest_path is not None and not Path(payload.payload_manifest_path).exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO208",
                    severity="warning",
                    concept="Structured Research Payload",
                    path=Path(payload.payload_manifest_path),
                    field=payload.record_id,
                    message="Structured payload manifest file is missing.",
                )
            )
        for ref_field, ref_value in (
            ("revision_of_record_id", payload.revision_of_record_id),
            ("supersedes_record_id", payload.supersedes_record_id),
        ):
            if ref_value is not None and ref_value not in lifecycle_records:
                diagnostics.append(
                    Diagnostic(
                        code="ISO208",
                        severity="warning",
                        concept="Structured Research Payload",
                        path=store.db_path,
                        field=ref_field,
                        message=f"Structured payload revision ref points to a missing lifecycle record: {ref_value}.",
                    )
                )
        if payload.schema_ref.startswith("isomer:"):
            validation = validate_payload(payload_json, schema_ref=payload.schema_ref)
            if not validation.ok:
                diagnostics.append(
                    Diagnostic(
                        code="ISO208",
                        severity="error",
                        concept="Structured Research Payload",
                        path=store.db_path,
                        field=payload.record_id,
                        message="Stored structured payload no longer validates against its recorded schema ref.",
                    )
                )
                diagnostics.extend(validation.diagnostics)
        if payload.rendered_markdown_path is not None:
            rendered_path = Path(payload.rendered_markdown_path)
            if not rendered_path.exists():
                diagnostics.append(
                    Diagnostic(
                        code="ISO209",
                        severity="error",
                        concept="Structured Research Payload",
                        path=rendered_path,
                        field=payload.record_id,
                        message="Structured payload legacy rendered Markdown locator is missing.",
                    )
                )
            elif payload.rendered_markdown_digest is not None:
                observed_render_digest = digest_bytes(rendered_path.read_bytes())
                if observed_render_digest != payload.rendered_markdown_digest:
                    diagnostics.append(
                        Diagnostic(
                            code="ISO209",
                            severity="warning",
                            concept="Structured Research Payload",
                            path=rendered_path,
                            field=payload.record_id,
                            message="Generated Markdown digest is stale for the stored structured payload.",
                        )
                    )
    return diagnostics


def _validate_reset_records(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    lifecycle_records = {record.id: record for record in store.list_lifecycle_records()}
    structured_payloads = {record.record_id: record for record in store.list_structured_payloads()}
    artifact_format_registrations = {record.id: record for record in store.list_artifact_format_registrations()}
    readiness_records = {record.id: record for record in store.list_readiness_records()}
    checkpoints = {record.id: record for record in store.list_reset_checkpoints()}
    plans = {record.id: record for record in store.list_reset_plans()}

    for checkpoint in checkpoints.values():
        diagnostics.extend(
            _owner_diagnostics(context, store.db_path, checkpoint.id, checkpoint.research_topic_id, checkpoint.topic_workspace_id)
        )
        diagnostics.extend(
            _forbidden_git_payload_diagnostics(
                checkpoint.payload_json,
                concept="Topic Reset Checkpoint",
                record_id=checkpoint.id,
                path=store.db_path,
            )
        )
        payload = checkpoint.payload_json
        diagnostics.extend(
            _missing_preserved_targets(
                store,
                checkpoint.id,
                payload,
                lifecycle_records=lifecycle_records,
                structured_payloads=structured_payloads,
                artifact_format_registrations=artifact_format_registrations,
                readiness_records=readiness_records,
            )
        )
        for payload_field in ("preserved_generated_view_paths", "preserved_support_paths", "summary_paths"):
            for path_text in _payload_string_list(payload, payload_field):
                if not Path(path_text).exists():
                    diagnostics.append(
                        Diagnostic(
                            code="ISO220",
                            severity="warning",
                            concept="Topic Reset Checkpoint",
                            path=Path(path_text),
                            field=f"{checkpoint.id}.{payload_field}",
                            message="Reset checkpoint preserves a path that no longer exists; regenerate the checkpoint before applying a reset.",
                        )
                    )

    for plan in plans.values():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, plan.id, plan.research_topic_id, plan.topic_workspace_id))
        diagnostics.extend(
            _forbidden_git_payload_diagnostics(
                plan.payload_json,
                concept="Topic Reset Plan",
                record_id=plan.id,
                path=store.db_path,
            )
        )
        plan_checkpoint = checkpoints.get(plan.checkpoint_id)
        if plan_checkpoint is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO221",
                    severity="error",
                    concept="Topic Reset Plan",
                    path=store.db_path,
                    field=plan.id,
                    message="Reset plan references a missing checkpoint.",
                )
            )
        elif plan_checkpoint.checkpoint_digest != plan.checkpoint_digest:
            diagnostics.append(
                Diagnostic(
                    code="ISO221",
                    severity="error",
                    concept="Topic Reset Plan",
                    path=store.db_path,
                    field=plan.id,
                    message="Reset plan checkpoint digest is stale; generate a new reset plan.",
                )
            )
        for action in store.list_reset_plan_actions(plan_id=plan.id):
            diagnostics.extend(
                _forbidden_git_payload_diagnostics(
                    action.details,
                    concept="Topic Reset Plan Action",
                    record_id=action.id,
                    path=store.db_path,
                )
            )

    for outcome in store.list_reset_outcomes():
        diagnostics.extend(
            _owner_diagnostics(context, store.db_path, outcome.id, outcome.research_topic_id, outcome.topic_workspace_id)
        )
        diagnostics.extend(
            _forbidden_git_payload_diagnostics(
                outcome.payload_json,
                concept="Topic Reset Outcome",
                record_id=outcome.id,
                path=store.db_path,
            )
        )
        if outcome.checkpoint_id not in checkpoints:
            diagnostics.append(
                Diagnostic(
                    code="ISO222",
                    severity="error",
                    concept="Topic Reset Outcome",
                    path=store.db_path,
                    field=outcome.id,
                    message="Reset outcome references a missing checkpoint.",
                )
            )
        if outcome.plan_id not in plans:
            diagnostics.append(
                Diagnostic(
                    code="ISO222",
                    severity="error",
                    concept="Topic Reset Outcome",
                    path=store.db_path,
                    field=outcome.id,
                    message="Reset outcome references a missing reset plan.",
                )
            )
    return diagnostics


def _missing_preserved_targets(
    store: WorkspaceRuntimeStore,
    checkpoint_id: str,
    payload: dict[str, object],
    *,
    lifecycle_records: Mapping[str, object],
    structured_payloads: Mapping[str, object],
    artifact_format_registrations: Mapping[str, object],
    readiness_records: Mapping[str, object],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    target_sets = (
        ("preserved_record_ids", lifecycle_records, "lifecycle record"),
        ("preserved_structured_payload_ids", structured_payloads, "structured payload"),
        ("preserved_artifact_format_registration_ids", artifact_format_registrations, "Artifact Format registration"),
        ("preserved_readiness_record_ids", readiness_records, "Topic Environment Readiness record"),
    )
    for payload_field, existing, label in target_sets:
        for target_id in _payload_string_list(payload, payload_field):
            if target_id not in existing:
                diagnostics.append(
                    Diagnostic(
                        code="ISO220",
                        severity="error",
                        concept="Topic Reset Checkpoint",
                        path=store.db_path,
                        field=f"{checkpoint_id}.{payload_field}",
                        message=f"Reset checkpoint preserves a missing {label}: {target_id}.",
                    )
                )
    return diagnostics


def _payload_string_list(payload: dict[str, object], field: str) -> list[str]:
    value = payload.get(field)
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if isinstance(item, str)]


def _forbidden_git_payload_diagnostics(
    payload: object,
    *,
    concept: str,
    record_id: str,
    path: Path,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for field_path, value in _walk_payload(payload):
        key = field_path[-1] if field_path else ""
        key_text = str(key).lower().replace("-", "_")
        value_text = str(value)
        if key_text == "no_git_operations":
            continue
        if key_text in _FORBIDDEN_GIT_FIELDS or any(fragment in key_text for fragment in _FORBIDDEN_GIT_KEY_FRAGMENTS):
            diagnostics.append(
                Diagnostic(
                    code="ISO223",
                    severity="error",
                    concept=concept,
                    path=path,
                    field=f"{record_id}.{'.'.join(str(part) for part in field_path)}",
                    message="Reset payload contains forbidden Git operation metadata.",
                )
            )
        elif isinstance(value, str) and _GIT_COMMAND_RE.search(value_text):
            diagnostics.append(
                Diagnostic(
                    code="ISO223",
                    severity="error",
                    concept=concept,
                    path=path,
                    field=f"{record_id}.{'.'.join(str(part) for part in field_path)}",
                    message="Reset payload contains a command string that invokes Git.",
                )
            )
    return diagnostics


def _walk_payload(payload: object, prefix: tuple[object, ...] = ()) -> Iterable[tuple[tuple[object, ...], object]]:
    if isinstance(payload, dict):
        for key, value in payload.items():
            yield from _walk_payload(value, (*prefix, key))
    elif isinstance(payload, list):
        for index, value in enumerate(payload):
            yield from _walk_payload(value, (*prefix, index))
    else:
        yield prefix, payload


_FORBIDDEN_GIT_FIELDS = {
    "git_stash_id",
    "git_ref",
    "git_branch",
    "git_tag",
    "git_commit",
    "git_command",
    "git_operation",
    "project_root_git_tracking",
}
_FORBIDDEN_GIT_KEY_FRAGMENTS = ("git_stash", "git_ref", "git_branch", "git_commit", "git_command", "git_operation")
_GIT_COMMAND_RE = re.compile(r"(^|[;&|]\s*)git\s+[A-Za-z0-9_-]+")


def _validate_agent_team_instances(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    manifest_profile_ids = {
        profile.id
        for profile in context.project.manifest.topic_agent_team_profiles
        if profile.research_topic_id == context.research_topic.id
    }
    agent_instances = {record.id: record for record in store.list_agent_instances()}
    agent_workspaces = {record.id: record for record in store.list_agent_workspaces()}
    path_plans = {record.id: record for record in store.list_path_plans()}

    for team in store.list_agent_team_instances():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, team.id, team.research_topic_id, team.topic_workspace_id))
        if team.topic_agent_team_profile_id not in manifest_profile_ids:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Agent Team Instance",
                    path=store.db_path,
                    field=team.id,
                    message="Agent Team Instance references a missing or cross-topic Topic Agent Team Profile.",
                )
            )
        for agent_id in team.agent_instance_ids:
            if agent_id not in agent_instances:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Agent Instance",
                        path=store.db_path,
                        field=agent_id,
                        message="Agent Team Instance references a missing Agent Instance.",
                    )
                )
        for workspace_id in team.agent_workspace_ids:
            if workspace_id not in agent_workspaces:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Agent Workspace",
                        path=store.db_path,
                        field=workspace_id,
                        message="Agent Team Instance references a missing Agent Workspace.",
                    )
                )

    for agent in agent_instances.values():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, agent.id, agent.research_topic_id, agent.topic_workspace_id))
        if store.get_agent_team_instance(agent.agent_team_instance_id) is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Agent Instance",
                    path=store.db_path,
                    field=agent.id,
                    message="Agent Instance references a missing Agent Team Instance.",
                )
            )

    for workspace in agent_workspaces.values():
        if workspace.topic_workspace_id != context.topic_workspace_id:
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="error",
                    concept="Agent Workspace",
                    path=store.db_path,
                    field=workspace.id,
                    message="Agent Workspace belongs to another Topic Workspace.",
                )
            )
        diagnostics.extend(
            validate_agent_name_value(
                agent_name=workspace.agent_name,
                source_path=store.db_path,
                field=f"{workspace.id}.agent_name",
                concept="Agent Workspace",
            )
        )
        plan = path_plans.get(workspace.path_plan_id)
        if plan is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Agent Workspace",
                    path=store.db_path,
                    field=workspace.id,
                    message="Agent Workspace references a missing path plan.",
                )
            )
        elif not Path(plan.path).exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="error",
                    concept="Agent Workspace",
                    path=Path(plan.path),
                    field=workspace.id,
                    message="Agent Workspace directory is missing.",
                )
            )
        elif workspace.agent_name is not None:
            expected_path = context.topic_workspace_path / "agents" / workspace.agent_name
            if Path(plan.path).resolve(strict=False) != expected_path.resolve(strict=False):
                diagnostics.append(
                    Diagnostic(
                        code="ISO044",
                        severity="error",
                        concept="Agent Workspace",
                        path=Path(plan.path),
                        field=workspace.id,
                        message="Agent Workspace path plan does not match its topic-local agent name.",
                    )
                )
            workspace_path = Path(plan.path)
            legacy_support_root = workspace_path / ".isomer-agent"
            if legacy_support_root.exists() or (
                workspace.support_root_path is not None and ".isomer-agent" in Path(workspace.support_root_path).parts
            ):
                diagnostics.append(
                    Diagnostic(
                        code="ISO044",
                        severity="warning",
                        concept="Agent Workspace",
                        path=legacy_support_root,
                        field=workspace.id,
                        message=(
                            "Agent Workspace references legacy `.isomer-agent/` support material; "
                            "standard support boundaries now use `isomer-managed/`."
                        ),
                    )
                )
            isomer_managed_path = _workspace_isomer_managed_path(workspace, path_plans, workspace_path)
            if not isomer_managed_path.exists():
                diagnostics.append(
                    Diagnostic(
                        code="ISO044",
                        severity="error",
                        concept="Agent Workspace",
                        path=isomer_managed_path,
                        field=workspace.id,
                        message="Agent Workspace is missing its `isomer-managed/` support path.",
                    )
                )
            else:
                for missing_subpath in _missing_isomer_managed_support_paths(isomer_managed_path):
                    diagnostics.append(
                        Diagnostic(
                            code="ISO044",
                            severity="warning",
                            concept="Agent Workspace",
                            path=missing_subpath,
                            field=workspace.id,
                            message="Agent Workspace is missing a standard `isomer-managed/` support subpath.",
                        )
                    )
                diagnostics.extend(_unsafe_generated_link_diagnostics(context, workspace, isomer_managed_path))
    return diagnostics


def _validate_handoffs(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    tmp_surfaces: tuple[_ResolvedTmpSurface, ...],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    lifecycle_by_kind: dict[str, set[str]] = {}
    for record in store.list_lifecycle_records():
        lifecycle_by_kind.setdefault(record.record_kind, set()).add(record.id)
    for handoff in store.list_handoffs():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, handoff.id, handoff.research_topic_id, handoff.topic_workspace_id))
        if handoff.agent_team_instance_id is not None and store.get_agent_team_instance(handoff.agent_team_instance_id) is None:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Handoff",
                    path=store.db_path,
                    field=handoff.id,
                    message="Handoff references a missing Agent Team Instance.",
                )
            )
        if handoff.research_task_id is not None and handoff.research_task_id not in lifecycle_by_kind.get("research_task", set()):
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Handoff",
                    path=store.db_path,
                    field=handoff.id,
                    message="Handoff references a missing Research Task.",
                )
            )
        if handoff.run_id is not None and handoff.run_id not in lifecycle_by_kind.get("run", set()):
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Handoff",
                    path=store.db_path,
                    field=handoff.id,
                    message="Handoff references a missing Run.",
                )
            )
        if handoff.status in {"sent", "observing"} and handoff.stale_after is not None:
            stale_after = _parse_timestamp(handoff.stale_after)
            if stale_after is not None and stale_after < datetime.now(UTC):
                diagnostics.append(
                    Diagnostic(
                        code="ISO045",
                        severity="warning",
                        concept="Handoff",
                        path=store.db_path,
                        field=handoff.id,
                        message=(
                            "Handoff is stale; Signal Observations are not authoritative "
                            "completion until the Operator Agent records normalization."
                        ),
                    )
                )
        for output_ref in handoff.expected_output_refs:
            diagnostic = _tmp_dependency_diagnostic(
                context,
                tmp_surfaces,
                Path(output_ref),
                concept="Handoff",
                field=handoff.id,
            )
            if diagnostic is not None:
                diagnostics.append(diagnostic)
    return diagnostics


def _validate_adapter_records(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
    tmp_surfaces: tuple[_ResolvedTmpSurface, ...],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    teams = {record.id for record in store.list_agent_team_instances()}
    agents = {record.id for record in store.list_agent_instances()}
    handoffs = {record.id: record for record in store.list_handoffs()}
    lifecycle_by_kind: dict[str, set[str]] = {}
    for record in store.list_lifecycle_records():
        lifecycle_by_kind.setdefault(record.record_kind, set()).add(record.id)
    path_plans = {record.id: record for record in store.list_path_plans()}
    manifest_refs = {record.id: record for record in store.list_adapter_manifest_refs()}
    payload_refs = {record.id: record for record in store.list_adapter_payload_refs()}
    command_runs = {record.id: record for record in store.list_adapter_command_runs()}
    for manifest_ref in store.list_adapter_manifest_refs():
        diagnostics.extend(
            _owner_diagnostics(
                context,
                store.db_path,
                manifest_ref.id,
                manifest_ref.research_topic_id,
                manifest_ref.topic_workspace_id,
            )
        )
        if manifest_ref.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter manifest ref",
                    path=store.db_path,
                    field=manifest_ref.id,
                    message="Adapter manifest ref points to a missing Agent Team Instance.",
                )
            )
        if manifest_ref.path_plan_id is not None and manifest_ref.path_plan_id not in path_plans:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter manifest ref",
                    path=store.db_path,
                    field=manifest_ref.id,
                    message="Adapter manifest ref points to a missing path plan.",
                )
            )
        manifest_path = Path(manifest_ref.manifest_path)
        if manifest_ref.path_plan_id is None:
            missing_evidence = _missing_semantic_file_evidence_diagnostic(
                context,
                path_plans.values(),
                manifest_path,
                concept="Execution Adapter manifest ref",
                field=manifest_ref.id,
                path_field="manifest_path",
            )
            if missing_evidence is not None:
                diagnostics.append(missing_evidence)
        diagnostic = _tmp_dependency_diagnostic(
            context,
            tmp_surfaces,
            manifest_path,
            concept="Execution Adapter manifest ref",
            field=manifest_ref.id,
        )
        if diagnostic is not None:
            diagnostics.append(diagnostic)
        if not manifest_path.exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="warning",
                    concept="Execution Adapter manifest ref",
                    path=manifest_path,
                    field=manifest_ref.id,
                    message="Adapter manifest file is missing.",
                )
            )
    for reconciliation in store.list_adapter_reconciliation_records():
        diagnostics.extend(
            _owner_diagnostics(
                context,
                store.db_path,
                reconciliation.id,
                reconciliation.research_topic_id,
                reconciliation.topic_workspace_id,
            )
        )
        if reconciliation.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter reconciliation",
                    path=store.db_path,
                    field=reconciliation.id,
                    message="Reconciliation record points to a missing Agent Team Instance.",
                )
            )
    for payload_ref in store.list_adapter_payload_refs():
        diagnostics.extend(
            _owner_diagnostics(
                context,
                store.db_path,
                payload_ref.id,
                payload_ref.research_topic_id,
                payload_ref.topic_workspace_id,
            )
        )
        if payload_ref.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter payload ref",
                    path=store.db_path,
                    field=payload_ref.id,
                    message="Adapter payload ref points to a missing Agent Team Instance.",
                )
            )
        if payload_ref.agent_instance_id is not None and payload_ref.agent_instance_id not in agents:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter payload ref",
                    path=store.db_path,
                    field=payload_ref.id,
                    message="Adapter payload ref points to a missing Agent Instance.",
                )
            )
        if payload_ref.path_plan_id is not None and payload_ref.path_plan_id not in path_plans:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter payload ref",
                    path=store.db_path,
                    field=payload_ref.id,
                    message="Adapter payload ref points to a missing path plan.",
                )
            )
        payload_path = Path(payload_ref.payload_path)
        if payload_ref.path_plan_id is None:
            missing_evidence = _missing_semantic_file_evidence_diagnostic(
                context,
                path_plans.values(),
                payload_path,
                concept="Execution Adapter payload ref",
                field=payload_ref.id,
                path_field="payload_path",
            )
            if missing_evidence is not None:
                diagnostics.append(missing_evidence)
        diagnostic = _tmp_dependency_diagnostic(
            context,
            tmp_surfaces,
            payload_path,
            concept="Execution Adapter payload ref",
            field=payload_ref.id,
        )
        if diagnostic is not None:
            diagnostics.append(diagnostic)
        if not payload_path.exists():
            diagnostics.append(
                Diagnostic(
                    code="ISO044",
                    severity="warning",
                    concept="Execution Adapter payload ref",
                    path=payload_path,
                    field=payload_ref.id,
                    message="Adapter payload file is missing.",
                )
            )
    for command in store.list_adapter_command_runs():
        diagnostics.extend(
            _owner_diagnostics(
                context,
                store.db_path,
                command.id,
                command.research_topic_id,
                command.topic_workspace_id,
            )
        )
        if command.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter command run",
                    path=store.db_path,
                    field=command.id,
                    message="Adapter command run points to a missing Agent Team Instance.",
                )
            )
        if command.agent_instance_id is not None and command.agent_instance_id not in agents:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter command run",
                    path=store.db_path,
                    field=command.id,
                    message="Adapter command run points to a missing Agent Instance.",
                )
            )
        for payload_ref_id in command.payload_ref_ids:
            if payload_ref_id not in payload_refs:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Execution Adapter command run",
                        path=store.db_path,
                        field=command.id,
                        message=f"Adapter command run points to a missing payload ref: {payload_ref_id}.",
                    )
                )
        if command.status in {"timed_out", "invalid_json", "failed"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO075",
                    severity="warning",
                    concept="Execution Adapter command run",
                    path=store.db_path,
                    field=command.id,
                    message=f"Adapter command run is {command.status}; inspect or reconcile before treating the backend state as current.",
                )
            )
    diagnostics.extend(
        validate_adapter_handoff_records(
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
    for materialization in store.list_adapter_materializations():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, materialization.id, materialization.research_topic_id, materialization.topic_workspace_id))
        if materialization.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter materialization",
                    path=store.db_path,
                    field=materialization.id,
                    message="Adapter materialization points to a missing Agent Team Instance.",
                )
            )
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter materialization", materialization.id, "payload", materialization.material_ref_ids, payload_refs))
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter materialization", materialization.id, "manifest", materialization.manifest_ref_ids, manifest_refs))
    for launch_attempt in store.list_adapter_launch_attempts():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, launch_attempt.id, launch_attempt.research_topic_id, launch_attempt.topic_workspace_id))
        if launch_attempt.agent_team_instance_id not in teams:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter launch attempt",
                    path=store.db_path,
                    field=launch_attempt.id,
                    message="Adapter launch attempt points to a missing Agent Team Instance.",
                )
            )
        for agent_id in launch_attempt.agent_instance_ids:
            if agent_id not in agents:
                diagnostics.append(
                    Diagnostic(
                        code="ISO041",
                        severity="error",
                        concept="Execution Adapter launch attempt",
                        path=store.db_path,
                        field=launch_attempt.id,
                        message=f"Adapter launch attempt points to a missing Agent Instance: {agent_id}.",
                    )
                )
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter launch attempt", launch_attempt.id, "command", launch_attempt.command_run_ids, command_runs))
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter launch attempt", launch_attempt.id, "manifest", launch_attempt.manifest_ref_ids, manifest_refs))
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter launch attempt", launch_attempt.id, "payload", launch_attempt.payload_ref_ids, payload_refs))
        if launch_attempt.status in {"partial", "failed"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO075",
                    severity="warning",
                    concept="Execution Adapter launch attempt",
                    path=store.db_path,
                    field=launch_attempt.id,
                    message=f"Adapter launch attempt is {launch_attempt.status}; inspect-live or stop may be needed for recovery.",
                )
            )
    for snapshot in store.list_adapter_inspection_snapshots():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, snapshot.id, snapshot.research_topic_id, snapshot.topic_workspace_id))
        if snapshot.snapshot_payload_ref_id is not None and snapshot.snapshot_payload_ref_id not in payload_refs:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept="Execution Adapter inspection snapshot",
                    path=store.db_path,
                    field=snapshot.id,
                    message="Adapter inspection snapshot points to a missing payload ref.",
                )
            )
        if snapshot.status in {"failed", "stale"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO075",
                    severity="warning",
                    concept="Execution Adapter inspection snapshot",
                    path=store.db_path,
                    field=snapshot.id,
                    message=f"Adapter inspection snapshot is {snapshot.status}.",
                )
            )
    for stop_outcome in store.list_adapter_stop_outcomes():
        diagnostics.extend(_owner_diagnostics(context, store.db_path, stop_outcome.id, stop_outcome.research_topic_id, stop_outcome.topic_workspace_id))
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter stop outcome", stop_outcome.id, "command", stop_outcome.command_run_ids, command_runs))
        diagnostics.extend(_missing_ref_diagnostics(store.db_path, "Execution Adapter stop outcome", stop_outcome.id, "payload", stop_outcome.payload_ref_ids, payload_refs))
        if stop_outcome.status in {"partial", "failed", "stale"}:
            diagnostics.append(
                Diagnostic(
                    code="ISO075",
                    severity="warning",
                    concept="Execution Adapter stop outcome",
                    path=store.db_path,
                    field=stop_outcome.id,
                    message=f"Adapter stop outcome is {stop_outcome.status}; remaining live refs must be inspected before cleanup is complete.",
                )
            )
    return diagnostics


def _validate_lifecycle_transitions(store: WorkspaceRuntimeStore) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for transition in store.list_lifecycle_transitions():
        missing_fields = [
            field
            for field in ("record_kind", "record_id", "previous_status", "next_status", "actor_ref", "rationale", "created_at")
            if transition[field] in (None, "")
        ]
        if missing_fields:
            diagnostics.append(
                Diagnostic(
                    code="ISO045",
                    severity="error",
                    concept="Research Lifecycle State",
                    path=store.db_path,
                    field=transition["id"],
                    message=f"Lifecycle transition is missing required field(s): {', '.join(missing_fields)}.",
                )
            )
    return diagnostics


def _parse_timestamp(value: str) -> datetime | None:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None

@dataclass(frozen=True)
class RuntimeInspection:
    exists: bool
    runtime_path: Path | None
    metadata: dict[str, object] | None
    counts: dict[str, int]
    latest_readiness: dict[str, object] | None
    agent_team_instances: list[dict[str, object]]
    path_plans: list[dict[str, object]]
    semantic_file_locators: list[dict[str, object]] = field(default_factory=list)

    def to_json(self) -> dict[str, object]:
        return {
            "exists": self.exists,
            "runtime_path": str(self.runtime_path) if self.runtime_path is not None else None,
            "metadata": self.metadata,
            "counts": self.counts,
            "latest_readiness": self.latest_readiness,
            "agent_team_instances": self.agent_team_instances,
            "path_plans": self.path_plans,
            "semantic_file_locators": self.semantic_file_locators,
        }


def inspect_workspace_runtime(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> tuple[RuntimeInspection, list[Diagnostic]]:
    entries, diagnostics = preview_paths(context, env=env)
    runtime_path = None
    if not has_errors(diagnostics):
        runtime_path = next(entry.path for entry in entries if entry.surface == "workspace_runtime_db")
    store, open_diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    diagnostics.extend(open_diagnostics)
    if store is None:
        return RuntimeInspection(False, runtime_path, None, {}, None, [], []), diagnostics
    latest_readiness = store.latest_readiness()
    path_plans = store.list_path_plans()
    semantic_file_locators = runtime_semantic_file_locators(
        path_plans=path_plans,
        lifecycle_records=store.list_lifecycle_records(),
        adapter_manifest_refs=store.list_adapter_manifest_refs(),
        adapter_payload_refs=store.list_adapter_payload_refs(),
    )
    inspection = RuntimeInspection(
        exists=True,
        runtime_path=store.db_path,
        metadata=store.metadata().to_json(),
        counts=store.count_records(),
        latest_readiness=latest_readiness.to_json() if latest_readiness is not None else None,
        agent_team_instances=[
            record.to_json() for record in store.list_agent_team_instances()
        ],
        path_plans=[record.to_json() for record in path_plans],
        semantic_file_locators=[locator.to_json() for locator in semantic_file_locators],
    )
    store.close()
    return inspection, diagnostics


def validate_workspace_runtime(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    require_ready_readiness: bool = False,
) -> tuple[RuntimeInspection, list[Diagnostic]]:
    inspection, diagnostics = inspect_workspace_runtime(context, env=env)
    if not inspection.exists:
        return inspection, diagnostics

    store, open_diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    diagnostics.extend(open_diagnostics)
    if store is None:
        return inspection, diagnostics

    tmp_surfaces, tmp_surface_diagnostics = _resolved_tmp_surfaces(context, store, env)
    tmp_surfaces_tuple = tuple(tmp_surfaces)
    diagnostics.extend(tmp_surface_diagnostics)
    diagnostics.extend(_validate_metadata(context, store))
    diagnostics.extend(_validate_path_plans(context, store, env))
    diagnostics.extend(_validate_local_tmp_surfaces(context, store, env, tmp_surfaces=tmp_surfaces_tuple))
    diagnostics.extend(validate_topic_workspace_visibility_layout(context, env=env))
    diagnostics.extend(_validate_readiness(context, store, require_ready=require_ready_readiness, tmp_surfaces=tmp_surfaces_tuple))
    diagnostics.extend(_validate_lifecycle_records(context, store, tmp_surfaces_tuple))
    diagnostics.extend(_validate_agent_team_instances(context, store))
    diagnostics.extend(_validate_global_agent_instance_id_uniqueness(context, store.db_path))
    diagnostics.extend(_validate_adapter_records(context, store, tmp_surfaces_tuple))
    diagnostics.extend(_validate_handoffs(context, store, tmp_surfaces_tuple))
    diagnostics.extend(_validate_lifecycle_transitions(store))
    diagnostics.extend(_validate_structured_research_payloads(context, store))
    diagnostics.extend(_validate_research_record_query_index(context, store))
    diagnostics.extend(_validate_reset_records(context, store))
    store.close()
    return inspection, diagnostics


def _validate_research_record_query_index(
    context: EffectiveTopicContext,
    store: WorkspaceRuntimeStore,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for item in query_index_diagnostics_for_store(context, store):
        raw_severity = str(item.get("severity") or "warning")
        severity = "warning" if raw_severity == "warn" else raw_severity
        code = str(item.get("code") or "query_index_issue")
        message = str(item.get("message") or "Research record query index issue.")
        diagnostics.append(
            Diagnostic(
                code=f"ISOQ-{code}",
                severity="error" if severity == "error" else "warning",
                concept="Research Record Query Index",
                message=message,
                field=str(item.get("record_id")) if item.get("record_id") is not None else None,
            )
        )
    return diagnostics
