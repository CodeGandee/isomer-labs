"""Topic Actor topology and workspace management."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
from typing import Any, Mapping

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.workspace.path_resolution import materialize_semantic_path, resolve_semantic_path
from isomer_labs.runtime.records import _provenance_ref, _slug
from isomer_labs.runtime.records import RuntimeLifecycleRecord, utc_timestamp
from isomer_labs.runtime.store import open_workspace_runtime
from isomer_labs.workspace.manifest import (
    DEFAULT_TOPIC_ACTOR_WORKSPACE_LABEL,
    TopicActorBinding,
    archive_topic_actor_binding,
    load_topic_workspace_manifest,
    register_topic_actor_binding,
    update_topic_actor_binding,
)

TOPIC_ACTOR_WORKSPACE_LABELS = (
    "topic.actors.workspace",
    "topic.actors.tmp",
    "topic.actors.isomer_managed",
    "topic.actors.output_root",
    "topic.actors.private_artifacts",
    "topic.actors.logs",
    "topic.actors.links",
)


@dataclass(frozen=True)
class _GitWorktreeEntry:
    path: Path
    branch: str | None


@dataclass(frozen=True)
class _ActorWorktreeReadiness:
    source_repo_path: Path
    workspace_path: Path
    expected_branch: str
    status: str
    observed_branch: str | None = None
    observed_source_repo_path: Path | None = None
    matching_worktree_path: Path | None = None
    duplicate_branch_path: Path | None = None
    blocker: str | None = None
    next_action: str = "none"

    @property
    def ready(self) -> bool:
        return self.status == "ready"

    @property
    def can_create(self) -> bool:
        return self.status == "missing"

    def to_json(self) -> dict[str, object]:
        payload: dict[str, object] = {
            "source_repo_path": str(self.source_repo_path),
            "workspace_path": str(self.workspace_path),
            "expected_branch": self.expected_branch,
            "observed_branch": self.observed_branch,
            "status": self.status,
            "ready": self.ready,
            "can_create": self.can_create,
            "blocker": self.blocker,
            "next_action": self.next_action,
        }
        if self.observed_source_repo_path is not None:
            payload["observed_source_repo_path"] = str(self.observed_source_repo_path)
        if self.matching_worktree_path is not None:
            payload["matching_worktree_path"] = str(self.matching_worktree_path)
        if self.duplicate_branch_path is not None:
            payload["duplicate_branch_path"] = str(self.duplicate_branch_path)
        return payload


def list_topic_actors(context: EffectiveTopicContext) -> tuple[dict[str, Any], list[Diagnostic]]:
    manifest, diagnostics = load_topic_workspace_manifest(context)
    actors = [binding.to_json() for binding in manifest.topic_actor_bindings]
    return {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "topic_actors": actors,
        "manifest": manifest.to_json(),
    }, diagnostics


def show_topic_actor(context: EffectiveTopicContext, topic_actor_name: str) -> tuple[dict[str, Any], list[Diagnostic]]:
    manifest, diagnostics = load_topic_workspace_manifest(context)
    actor = manifest.topic_actor_binding_for(topic_actor_name)
    if actor is None:
        diagnostics.append(_missing_actor_diagnostic(topic_actor_name))
    return {
        "ok": actor is not None and not has_errors(diagnostics),
        "mutated": False,
        "topic_actor": actor.to_json() if actor is not None else None,
        "manifest": manifest.to_json(),
    }, diagnostics


def register_topic_actor(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    topic_actor_name: str,
    actor_kind: str | None = None,
    runtime_kind: str | None = None,
    role_kind: str | None = None,
    controller_kind: str | None = None,
    controller_ref: str | None = None,
    workspace_path: str | None = None,
    branch: str | None = None,
    adapter_ref: str | None = None,
    status: str = "ready",
    replace_existing: bool = False,
    materialize: bool = False,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    selected_actor_kind = actor_kind or ("operator" if topic_actor_name == "operator" else "manual_worker")
    selected_role_kind = role_kind or ("operator" if topic_actor_name == "operator" else "coder")
    manifest, actor, diagnostics = register_topic_actor_binding(
        context,
        topic_actor_name=topic_actor_name,
        actor_kind=selected_actor_kind,
        runtime_kind=runtime_kind or "human_cli",
        role_kind=selected_role_kind,
        controller_kind=controller_kind or "project_operator_session",
        controller_ref=controller_ref,
        default_cwd_label=DEFAULT_TOPIC_ACTOR_WORKSPACE_LABEL,
        workspace_label=DEFAULT_TOPIC_ACTOR_WORKSPACE_LABEL,
        workspace_path=workspace_path,
        branch=branch,
        adapter_ref=adapter_ref,
        status=status,
        replace_existing=replace_existing,
    )
    audit_record_id = None
    if actor is not None and not has_errors(diagnostics):
        audit_record_id, audit_diagnostics = _record_actor_audit(context, actor, "register", env=env)
        diagnostics.extend(audit_diagnostics)
    materialization = None
    if materialize and actor is not None and not has_errors(diagnostics):
        materialization, materialize_diagnostics = _materialize_actor_workspace(context, actor, env=env)
        diagnostics.extend(materialize_diagnostics)
    return {
        "ok": actor is not None and not has_errors(diagnostics),
        "mutated": actor is not None and not has_errors(diagnostics),
        "operation": "register",
        "topic_actor": actor.to_json() if actor is not None else None,
        "manifest": manifest.to_json() if manifest is not None else None,
        "materialization": materialization,
        "audit_record_id": audit_record_id,
    }, diagnostics


def update_topic_actor(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    topic_actor_name: str,
    actor_kind: str | None = None,
    runtime_kind: str | None = None,
    role_kind: str | None = None,
    controller_kind: str | None = None,
    controller_ref: str | None = None,
    workspace_path: str | None = None,
    branch: str | None = None,
    adapter_ref: str | None = None,
    status: str | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    manifest, actor, diagnostics = update_topic_actor_binding(
        context,
        topic_actor_name=topic_actor_name,
        actor_kind=actor_kind,
        runtime_kind=runtime_kind,
        role_kind=role_kind,
        controller_kind=controller_kind,
        controller_ref=controller_ref,
        workspace_path=workspace_path,
        branch=branch,
        adapter_ref=adapter_ref,
        status=status,
    )
    audit_record_id = None
    if actor is not None and not has_errors(diagnostics):
        audit_record_id, audit_diagnostics = _record_actor_audit(context, actor, "update", env=env)
        diagnostics.extend(audit_diagnostics)
    return {
        "ok": actor is not None and not has_errors(diagnostics),
        "mutated": actor is not None and not has_errors(diagnostics),
        "operation": "update",
        "topic_actor": actor.to_json() if actor is not None else None,
        "manifest": manifest.to_json() if manifest is not None else None,
        "audit_record_id": audit_record_id,
    }, diagnostics


def archive_topic_actor(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    topic_actor_name: str,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    manifest, actor, diagnostics = archive_topic_actor_binding(context, topic_actor_name=topic_actor_name)
    audit_record_id = None
    if actor is not None and not has_errors(diagnostics):
        audit_record_id, audit_diagnostics = _record_actor_audit(context, actor, "archive", env=env)
        diagnostics.extend(audit_diagnostics)
    return {
        "ok": actor is not None and not has_errors(diagnostics),
        "mutated": actor is not None and not has_errors(diagnostics),
        "operation": "archive",
        "topic_actor": actor.to_json() if actor is not None else None,
        "manifest": manifest.to_json() if manifest is not None else None,
        "audit_record_id": audit_record_id,
    }, diagnostics


def materialize_topic_actor_workspace(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    topic_actor_name: str,
    source_repo: str | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    manifest, diagnostics = load_topic_workspace_manifest(context)
    actor = manifest.topic_actor_binding_for(topic_actor_name)
    if actor is None:
        diagnostics.append(_missing_actor_diagnostic(topic_actor_name))
        return {"ok": False, "mutated": False, "operation": "materialize", "materialization": None}, diagnostics
    if source_repo is not None:
        topic_main, topic_main_diagnostics = resolve_semantic_path(context, "topic.repos.main", env=env, cwd=context.topic_workspace_path, use_path_plan=False)
        diagnostics.extend(topic_main_diagnostics)
        if topic_main is not None and Path(source_repo).expanduser().resolve(strict=False) != topic_main.path:
            diagnostics.append(
                Diagnostic(
                    code="ISO061",
                    severity="error",
                    concept="Topic Actor Workspace",
                    field="source_repo",
                    message="Alternate Topic Actor Workspace source repositories are unsupported in this change; use topic.repos.main.",
                )
            )
    materialization = None
    if not has_errors(diagnostics):
        materialization, materialize_diagnostics = _materialize_actor_workspace(context, actor, env=env)
        diagnostics.extend(materialize_diagnostics)
    return {
        "ok": materialization is not None and not has_errors(diagnostics),
        "mutated": materialization is not None and not has_errors(diagnostics),
        "operation": "materialize",
        "materialization": materialization,
    }, diagnostics


def diagnose_topic_actor(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    topic_actor_name: str | None = None,
) -> tuple[dict[str, Any], list[Diagnostic]]:
    manifest, diagnostics = load_topic_workspace_manifest(context)
    actors = [manifest.topic_actor_binding_for(topic_actor_name)] if topic_actor_name else list(manifest.active_topic_actor_bindings())
    selected_actors = [actor for actor in actors if actor is not None]
    if topic_actor_name is not None and not selected_actors:
        diagnostics.append(_missing_actor_diagnostic(topic_actor_name))
    actor_paths: list[dict[str, object]] = []
    worktree_status_by_actor: dict[str, dict[str, object]] = {}
    topic_main, topic_main_diagnostics = resolve_semantic_path(context, "topic.repos.main", env=env, cwd=context.topic_workspace_path, use_path_plan=False)
    diagnostics.extend(topic_main_diagnostics)
    for actor in selected_actors:
        workspace_result = None
        for label in TOPIC_ACTOR_WORKSPACE_LABELS:
            result, result_diagnostics = resolve_semantic_path(
                context,
                label,
                env=env,
                cwd=context.topic_workspace_path,
                topic_actor_name=actor.topic_actor_name,
                use_path_plan=False,
            )
            diagnostics.extend(result_diagnostics)
            if result is not None:
                actor_paths.append(result.to_json())
                if label == "topic.actors.workspace":
                    workspace_result = result
        if topic_main is not None and workspace_result is not None:
            readiness, readiness_diagnostics = _inspect_actor_worktree_readiness(topic_main.path, workspace_result.path, actor.effective_branch)
            diagnostics.extend(readiness_diagnostics)
            worktree_status_by_actor[actor.topic_actor_name] = readiness.to_json()
    return {
        "ok": not has_errors(diagnostics),
        "mutated": False,
        "topic_main": topic_main.to_json() if topic_main is not None else None,
        "topic_actors": [actor.to_json() for actor in selected_actors],
        "actor_paths": actor_paths,
        "worktree_status_by_actor": worktree_status_by_actor,
        "manifest": manifest.to_json(),
    }, diagnostics


def _materialize_actor_workspace(
    context: EffectiveTopicContext,
    actor: TopicActorBinding,
    *,
    env: Mapping[str, str],
) -> tuple[dict[str, Any] | None, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    topic_main, topic_main_diagnostics = resolve_semantic_path(context, "topic.repos.main", env=env, cwd=context.topic_workspace_path, use_path_plan=False)
    diagnostics.extend(topic_main_diagnostics)
    workspace, workspace_diagnostics = resolve_semantic_path(
        context,
        "topic.actors.workspace",
        env=env,
        cwd=context.topic_workspace_path,
        topic_actor_name=actor.topic_actor_name,
        use_path_plan=False,
    )
    diagnostics.extend(workspace_diagnostics)
    if topic_main is None or workspace is None or has_errors(diagnostics):
        return None, diagnostics

    created_paths: list[str] = []
    worktree_mode = "existing"
    readiness, readiness_diagnostics = _inspect_actor_worktree_readiness(topic_main.path, workspace.path, actor.effective_branch)
    diagnostics.extend(readiness_diagnostics)
    if readiness.can_create and not has_errors(diagnostics):
        if _git_branch_exists(topic_main.path, actor.effective_branch):
            command = ["git", "-C", str(topic_main.path), "worktree", "add", str(workspace.path), actor.effective_branch]
        else:
            command = ["git", "-C", str(topic_main.path), "worktree", "add", "-b", actor.effective_branch, str(workspace.path)]
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
        if completed.returncode != 0:
            diagnostics.append(
                Diagnostic(
                    code="ISO061",
                    severity="error",
                    concept="Topic Actor Workspace",
                    field="topic.repos.main",
                    message=f"Git worktree creation failed from topic.repos.main: {completed.stderr.strip() or completed.stdout.strip()}",
                )
            )
            return None, diagnostics
        created_paths.append(str(workspace.path))
        readiness, readiness_diagnostics = _inspect_actor_worktree_readiness(topic_main.path, workspace.path, actor.effective_branch)
        diagnostics.extend(readiness_diagnostics)
        worktree_mode = "git-worktree"
    elif readiness.ready:
        worktree_mode = "git-worktree"

    if not readiness.ready or has_errors(diagnostics):
        return None, diagnostics

    support_paths: list[dict[str, object]] = [workspace.to_json()]
    for label in TOPIC_ACTOR_WORKSPACE_LABELS[1:]:
        result, result_diagnostics = materialize_semantic_path(
            context,
            label,
            env=env,
            cwd=context.topic_workspace_path,
            topic_actor_name=actor.topic_actor_name,
        )
        diagnostics.extend(result_diagnostics)
        if result is not None:
            created_path_payload = result.get("created_paths", [])
            if isinstance(created_path_payload, list):
                created_paths.extend(str(path) for path in created_path_payload if isinstance(path, str))
            path_payload = result.get("path")
            if isinstance(path_payload, dict):
                support_paths.append(path_payload)

    audit_record_id = None
    if not has_errors(diagnostics):
        audit_record_id, audit_diagnostics = _record_actor_audit(context, actor, "materialize", env=env)
        diagnostics.extend(audit_diagnostics)
        path_plan_diagnostics = _record_actor_path_plans(context, actor, env=env)
        diagnostics.extend(path_plan_diagnostics)
    return {
        "topic_actor": actor.to_json(),
        "topic_main": topic_main.to_json(),
        "workspace": workspace.to_json(),
        "support_paths": support_paths,
        "created_paths": created_paths,
        "branch": actor.effective_branch,
        "worktree_mode": worktree_mode,
        "worktree_status": readiness.to_json(),
        "audit_record_id": audit_record_id,
    }, diagnostics


def _record_actor_audit(
    context: EffectiveTopicContext,
    actor: TopicActorBinding,
    operation: str,
    *,
    env: Mapping[str, str],
) -> tuple[str | None, list[Diagnostic]]:
    runtime_path, diagnostics = resolve_semantic_path(context, "topic.runtime.db", env=env, cwd=context.topic_workspace_path, use_path_plan=False)
    if runtime_path is None or not runtime_path.path.exists():
        return None, []
    store, open_diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    diagnostics.extend(open_diagnostics)
    if store is None or has_errors(diagnostics):
        return None, diagnostics
    now = utc_timestamp()
    record_id = f"topic-actor-{_slug(actor.topic_actor_name)}-{_slug(operation)}-{_slug(now)}"
    record = RuntimeLifecycleRecord(
        id=record_id,
        record_kind="provenance_record",
        research_topic_id=context.research_topic.id,
        topic_workspace_id=context.topic_workspace_id,
        status="ready",
        created_at=now,
        updated_at=now,
        lifecycle_refs={"topic_actor_name": actor.topic_actor_name},
        transition_metadata={
            "operation": f"topic_actor_{operation}",
            "topic_actor_name": actor.topic_actor_name,
            "actor_kind": actor.actor_kind,
            "runtime_kind": actor.runtime_kind,
            "role_kind": actor.role_kind,
            "controller_kind": actor.controller_kind,
            "branch": actor.effective_branch,
        },
        provenance_refs=[_provenance_ref("provenance_record", record_id)],
    )
    try:
        with store.connection:
            store.upsert_lifecycle_record(record)
    finally:
        store.close()
    return record_id, diagnostics


def _record_actor_path_plans(
    context: EffectiveTopicContext,
    actor: TopicActorBinding,
    *,
    env: Mapping[str, str],
) -> list[Diagnostic]:
    runtime_path, diagnostics = resolve_semantic_path(context, "topic.runtime.db", env=env, cwd=context.topic_workspace_path, use_path_plan=False)
    if runtime_path is None or not runtime_path.path.exists():
        return []
    store, open_diagnostics = open_workspace_runtime(context, env=env, read_only=False)
    diagnostics.extend(open_diagnostics)
    if store is None or has_errors(diagnostics):
        return diagnostics
    try:
        with store.connection:
            for label in TOPIC_ACTOR_WORKSPACE_LABELS:
                result, result_diagnostics = resolve_semantic_path(
                    context,
                    label,
                    env=env,
                    cwd=context.topic_workspace_path,
                    topic_actor_name=actor.topic_actor_name,
                    use_path_plan=False,
                )
                diagnostics.extend(result_diagnostics)
                if result is None or has_errors(result_diagnostics):
                    continue
                storage_profile_traits_payload = result.to_json().get("storage_profile_traits", {})
                storage_profile_traits = storage_profile_traits_payload if isinstance(storage_profile_traits_payload, dict) else {}
                store.record_path_plan(
                    topic_workspace_id=context.topic_workspace_id,
                    surface=result.compatibility_surface,
                    path=result.path,
                    source=result.source,
                    source_detail=result.source_detail,
                    semantic_label=result.label,
                    scope_ref=result.scope_ref,
                    compatibility_surface=result.compatibility_surface,
                    storage_profile=result.catalog.storage_profile,
                    storage_profile_traits=storage_profile_traits,
                )
    finally:
        store.close()
    return diagnostics


def _inspect_actor_worktree_readiness(topic_main_path: Path, workspace_path: Path, expected_branch: str) -> tuple[_ActorWorktreeReadiness, list[Diagnostic]]:
    diagnostics: list[Diagnostic] = []
    source_repo_path = topic_main_path.resolve(strict=False)
    resolved_workspace_path = workspace_path.resolve(strict=False)
    if not _looks_like_git_repo(source_repo_path):
        readiness = _ActorWorktreeReadiness(
            source_repo_path=source_repo_path,
            workspace_path=resolved_workspace_path,
            expected_branch=expected_branch,
            status="blocked_topic_main_not_git",
            blocker="topic.repos.main is missing or is not a Git repository.",
            next_action="Prepare topic.repos.main before materializing Topic Actor Workspaces.",
        )
        diagnostics.append(_worktree_blocker_diagnostic(readiness))
        return readiness, diagnostics

    entries, list_diagnostics = _list_git_worktrees(source_repo_path)
    diagnostics.extend(list_diagnostics)
    if has_errors(diagnostics):
        readiness = _ActorWorktreeReadiness(
            source_repo_path=source_repo_path,
            workspace_path=resolved_workspace_path,
            expected_branch=expected_branch,
            status="blocked_worktree_inspection_failed",
            blocker="Unable to inspect topic.repos.main worktrees.",
            next_action="Repair topic.repos.main Git metadata, then retry actor materialization.",
        )
        return readiness, diagnostics

    expected_branch_ref = f"refs/heads/{expected_branch}"
    matching_path_entry = next((entry for entry in entries if entry.path.resolve(strict=False) == resolved_workspace_path), None)
    duplicate_branch_entry = next(
        (
            entry
            for entry in entries
            if entry.branch in {expected_branch, expected_branch_ref} and entry.path.resolve(strict=False) != resolved_workspace_path
        ),
        None,
    )
    if matching_path_entry is not None and matching_path_entry.branch in {expected_branch, expected_branch_ref}:
        return (
            _ActorWorktreeReadiness(
                source_repo_path=source_repo_path,
                workspace_path=resolved_workspace_path,
                expected_branch=expected_branch,
                observed_branch=_short_branch(matching_path_entry.branch),
                observed_source_repo_path=source_repo_path,
                matching_worktree_path=matching_path_entry.path.resolve(strict=False),
                status="ready",
                next_action="none",
            ),
            diagnostics,
        )

    if matching_path_entry is not None:
        readiness = _ActorWorktreeReadiness(
            source_repo_path=source_repo_path,
            workspace_path=resolved_workspace_path,
            expected_branch=expected_branch,
            observed_branch=_short_branch(matching_path_entry.branch),
            observed_source_repo_path=source_repo_path,
            matching_worktree_path=matching_path_entry.path.resolve(strict=False),
            status="blocked_existing_nonmatching_path",
            blocker="The actor workspace path exists as a topic-main worktree, but not on the expected actor branch.",
            next_action="Move, archive, or repair the existing actor workspace path before retrying.",
        )
        diagnostics.append(_worktree_blocker_diagnostic(readiness))
        return readiness, diagnostics

    if resolved_workspace_path.exists():
        readiness = _ActorWorktreeReadiness(
            source_repo_path=source_repo_path,
            workspace_path=resolved_workspace_path,
            expected_branch=expected_branch,
            status="blocked_existing_nonmatching_path",
            blocker="The actor workspace path exists but is not a worktree of topic.repos.main.",
            next_action="Move or archive the existing path, then rerun actor materialization.",
        )
        diagnostics.append(_worktree_blocker_diagnostic(readiness))
        return readiness, diagnostics

    if duplicate_branch_entry is not None:
        readiness = _ActorWorktreeReadiness(
            source_repo_path=source_repo_path,
            workspace_path=resolved_workspace_path,
            expected_branch=expected_branch,
            observed_branch=_short_branch(duplicate_branch_entry.branch),
            observed_source_repo_path=source_repo_path,
            duplicate_branch_path=duplicate_branch_entry.path.resolve(strict=False),
            status="blocked_duplicate_branch_checkout",
            blocker="The expected actor branch is already checked out in another topic-main worktree.",
            next_action="Use that existing worktree or free the branch before creating this actor workspace.",
        )
        diagnostics.append(_worktree_blocker_diagnostic(readiness))
        return readiness, diagnostics

    return (
        _ActorWorktreeReadiness(
            source_repo_path=source_repo_path,
            workspace_path=resolved_workspace_path,
            expected_branch=expected_branch,
            status="missing",
            next_action="Create the actor workspace as a topic-main worktree.",
        ),
        diagnostics,
    )


def _list_git_worktrees(topic_main_path: Path) -> tuple[list[_GitWorktreeEntry], list[Diagnostic]]:
    completed = subprocess.run(
        ["git", "-C", str(topic_main_path), "worktree", "list", "--porcelain"],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        return [], [
            Diagnostic(
                code="ISO061",
                severity="error",
                concept="Topic Actor Workspace",
                field="topic.repos.main",
                message=f"Git worktree inspection failed from topic.repos.main: {completed.stderr.strip() or completed.stdout.strip()}",
            )
        ]
    entries: list[_GitWorktreeEntry] = []
    current_path: Path | None = None
    current_branch: str | None = None
    for line in completed.stdout.splitlines():
        if line.startswith("worktree "):
            if current_path is not None:
                entries.append(_GitWorktreeEntry(path=current_path, branch=current_branch))
            current_path = Path(line.removeprefix("worktree ")).resolve(strict=False)
            current_branch = None
        elif line.startswith("branch "):
            current_branch = line.removeprefix("branch ")
    if current_path is not None:
        entries.append(_GitWorktreeEntry(path=current_path, branch=current_branch))
    return entries, []


def _looks_like_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def _git_branch_exists(topic_main_path: Path, branch: str) -> bool:
    completed = subprocess.run(
        ["git", "-C", str(topic_main_path), "show-ref", "--verify", "--quiet", f"refs/heads/{branch}"],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed.returncode == 0


def _short_branch(branch: str | None) -> str | None:
    if branch is None:
        return None
    return branch.removeprefix("refs/heads/")


def _worktree_blocker_diagnostic(readiness: _ActorWorktreeReadiness) -> Diagnostic:
    detail = readiness.blocker or "Topic Actor Workspace worktree readiness is blocked."
    return Diagnostic(
        code="ISO061",
        severity="error",
        concept="Topic Actor Workspace",
        field="topic.actors.workspace",
        message=f"{detail} Expected {readiness.workspace_path} to be a worktree of {readiness.source_repo_path} on {readiness.expected_branch}.",
    )


def _missing_actor_diagnostic(topic_actor_name: str) -> Diagnostic:
    return Diagnostic(
        code="ISO061",
        severity="error",
        concept="Topic Actor Workspace",
        field="topic_actor_name",
        message=f"Selected Topic Actor is not registered in the Topic Workspace Manifest: {topic_actor_name}.",
    )
