"""Focused validation checks for Workspace Runtime records."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import subprocess
from typing import Iterable, Mapping

from isomer_labs.artifact_formats import digest_bytes, digest_json, validate_payload
from isomer_labs.deepsci_ext.record_formats import register_deepsci_record_format_provider
from isomer_labs.diagnostics import Diagnostic
from isomer_labs.local_tmp_surfaces import TmpSurfaceIgnorePolicy, tmp_surface_ignore_policy
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.path_utils import canonicalize, is_within
from isomer_labs.paths import preview_paths, resolve_semantic_path
from isomer_labs.runtime.semantic_file_locator import locate_semantic_file
from isomer_labs.runtime.adapter_handoff_validation import validate_adapter_handoff_records
from isomer_labs.runtime.models import AgentWorkspaceRecord, PathPlanRecord
from isomer_labs.runtime.store import WorkspaceRuntimeStore
from isomer_labs.runtime.validation_utils import (
    missing_ref_diagnostics as _missing_ref_diagnostics,
    owner_diagnostics as _owner_diagnostics,
)
from isomer_labs.runtime.workspace_layout_validation import (
    is_unpromoted_isomer_managed_dependency as _is_unpromoted_isomer_managed_dependency,
    missing_isomer_managed_support_paths as _missing_isomer_managed_support_paths,
    unsafe_generated_link_diagnostics as _unsafe_generated_link_diagnostics,
    workspace_isomer_managed_path as _workspace_isomer_managed_path,
)
from isomer_labs.topic_workspace_manifest import (
    EffectiveAgentContext,
    resolve_semantic_binding,
)
from isomer_labs.workspace_refs import validate_agent_name_value


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
    register_deepsci_record_format_provider()
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
        for field, snapshot_path in (
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
                        field=field,
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
        observed_payload_digest = digest_json(payload.payload_json)
        if observed_payload_digest != payload.payload_digest:
            diagnostics.append(
                Diagnostic(
                    code="ISO208",
                    severity="error",
                    concept="Structured Research Payload",
                    path=store.db_path,
                    field=payload.record_id,
                    message="Structured payload digest does not match stored payload JSON.",
                )
            )
        if payload.schema_ref.startswith("isomer:"):
            validation = validate_payload(payload.payload_json, schema_ref=payload.schema_ref)
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
                        message="Structured payload generated Markdown locator is missing.",
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
