"""Canonical Project Artifact and Run commands."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Callable

import click

from isomer_labs.cli.handlers.shared import _context_for_options
from isomer_labs.cli.options import common_options, merge_options, topic_selection_options
from isomer_labs.cli.output import emit_output
from isomer_labs.kaoju.artifacts import KaojuArtifactService, KaojuServiceError
from isomer_labs.kaoju.repositories import KaojuRepositoryService
from isomer_labs.kaoju.runs import KaojuRunService
from isomer_labs.kaoju.service_requests import KaojuServiceRequestService


def register_kaoju_project_commands(project: click.Group) -> None:
    """Register typed Artifact and Run services below ``project``."""

    @project.group(name="artifacts", help="Resolve and manage typed project Artifacts through Workspace Runtime.")
    def artifacts_group() -> None:
        pass

    @artifacts_group.command(name="describe", help="Describe one semantic binding without exposing a physical subpath template.")
    @common_options
    @topic_selection_options
    @click.argument("semantic_id")
    @click.pass_context
    def artifacts_describe(ctx: click.Context, semantic_id: str, **values: Any) -> int:
        return _with_artifact_service(ctx, values, lambda service: service.describe(semantic_id))

    @artifacts_group.command(name="put", help="Create a typed Artifact using binding inference.")
    @common_options
    @topic_selection_options
    @click.option("--producer", required=True, help="Canonical producer skill or service id.")
    @click.option("--scope-key", default=None, help="Binding-defined current-state scope key.")
    @click.option("--id", "record_id", default=None, help="Explicit stable record id.")
    @click.option("--status", default="ready", show_default=True, help="Initial lifecycle status.")
    @click.option("--relationships-json", default=None, help="Relationship objects with binding role fields.")
    @click.option("--idempotency-key", default=None, help="Retry-safe mutation key.")
    @click.option("--external", is_flag=True, help="Register an authorized external path without copying it.")
    @click.option("--repository-remote", default=None, help="Canonical repository remote URL.")
    @click.option("--repository-commit", default=None, help="Canonical repository immutable commit.")
    @click.option("--repository-depth", type=int, default=None, help="Recorded clone depth posture.")
    @click.argument("semantic_id")
    @click.argument("content", type=click.Path(path_type=Path))
    @click.pass_context
    def artifacts_put(ctx: click.Context, semantic_id: str, content: Path, **values: Any) -> int:
        return _with_artifact_service(
            ctx,
            values,
            lambda service: service.put(
                semantic_id,
                content,
                producer=str(values["producer"]),
                scope_key=values.get("scope_key"),
                record_id=values.get("record_id"),
                status=str(values.get("status") or "ready"),
                relationships=_object_list(values.get("relationships_json")),
                idempotency_key=values.get("idempotency_key"),
                external=bool(values.get("external")),
                repository_remote=values.get("repository_remote"),
                repository_commit=values.get("repository_commit"),
                repository_depth=values.get("repository_depth"),
            ),
        )

    @artifacts_group.command(name="revise", help="Create a current-state Artifact revision.")
    @common_options
    @topic_selection_options
    @click.option("--producer", required=True, help="Canonical producer skill or service id.")
    @click.option("--scope-key", default=None, help="Binding-defined current-state scope key.")
    @click.option("--id", "new_record_id", default=None, help="Explicit descendant record id.")
    @click.option("--relationships-json", default=None, help="Relationship objects with binding role fields.")
    @click.option("--idempotency-key", default=None, help="Retry-safe mutation key.")
    @click.argument("record_id")
    @click.argument("content", type=click.Path(path_type=Path))
    @click.pass_context
    def artifacts_revise(ctx: click.Context, record_id: str, content: Path, **values: Any) -> int:
        return _with_artifact_service(
            ctx,
            values,
            lambda service: service.revise(
                record_id,
                content,
                producer=str(values["producer"]),
                scope_key=values.get("scope_key"),
                new_record_id=values.get("new_record_id"),
                relationships=_object_list(values.get("relationships_json")),
                idempotency_key=values.get("idempotency_key"),
            ),
        )

    @artifacts_group.command(name="latest", help="Resolve one deterministic scoped current Artifact.")
    @common_options
    @topic_selection_options
    @click.option("--scope-key", default=None, help="Binding-defined current-state scope key.")
    @click.argument("semantic_id")
    @click.pass_context
    def artifacts_latest(ctx: click.Context, semantic_id: str, **values: Any) -> int:
        return _with_artifact_service(ctx, values, lambda service: service.latest(semantic_id, scope_key=values.get("scope_key")))

    @artifacts_group.command(name="list", help="List Artifacts from state DB metadata.")
    @common_options
    @topic_selection_options
    @click.option("--semantic-id", default=None, help="Exact semantic id filter.")
    @click.option("--scope-key", default=None, help="Exact scope key filter.")
    @click.option("--status", default=None, help="Lifecycle status filter.")
    @click.pass_context
    def artifacts_list(ctx: click.Context, **values: Any) -> int:
        return _with_artifact_service(ctx, values, lambda service: service.list(semantic_id=values.get("semantic_id"), scope_key=values.get("scope_key"), status=values.get("status")))

    @artifacts_group.command(name="show", help="Show one Artifact and locator-integrity diagnostics.")
    @common_options
    @topic_selection_options
    @click.option("--include-content", is_flag=True, help="Include structured JSON or readable file content.")
    @click.argument("record_id")
    @click.pass_context
    def artifacts_show(ctx: click.Context, record_id: str, **values: Any) -> int:
        return _with_artifact_service(ctx, values, lambda service: service.show(record_id, include_content=bool(values.get("include_content"))))

    @artifacts_group.command(name="archive", help="Archive one Artifact without deleting externally owned content.")
    @common_options
    @topic_selection_options
    @click.option("--reason", default=None, help="Archive rationale.")
    @click.argument("record_id")
    @click.pass_context
    def artifacts_archive(ctx: click.Context, record_id: str, **values: Any) -> int:
        return _with_artifact_service(ctx, values, lambda service: service.archive(record_id, reason=values.get("reason")))

    @artifacts_group.command(name="migrate-scope", help="Preview or apply unambiguous legacy scope-key backfill.")
    @common_options
    @topic_selection_options
    @click.option("--apply", is_flag=True, help="Apply the reported backfill plan.")
    @click.pass_context
    def artifacts_migrate_scope(ctx: click.Context, **values: Any) -> int:
        return _with_artifact_service(ctx, values, lambda service: service.backfill_scope_keys(apply=bool(values.get("apply"))))

    repos_group = project.commands.get("repos")
    if not isinstance(repos_group, click.Group):
        raise RuntimeError("Project repository command group must be registered before Kaoju services.")

    @repos_group.command(name="acquire", help="Acquire, validate, and then register a canonical external repository.")
    @common_options
    @topic_selection_options
    @click.option("--semantic-label", required=True, help="Exact non-main topic.repos.* target label.")
    @click.option("--history-depth", type=int, default=1, show_default=True, help="Required history depth after the depth-one clone.")
    @click.option("--timeout", "timeout_seconds", type=float, default=120.0, show_default=True, help="Synchronous command timeout in seconds.")
    @click.argument("remote_url")
    @click.pass_context
    def repos_acquire(ctx: click.Context, remote_url: str, **values: Any) -> int:
        return _with_repository_service(ctx, values, lambda service: service.acquire(remote_url, semantic_label=str(values["semantic_label"]), history_depth=int(values["history_depth"]), timeout_seconds=float(values["timeout_seconds"])))

    @project.group(name="service-requests", help="Create, synchronously dispatch, and inspect Service Requests.")
    def service_requests_group() -> None:
        pass

    @service_requests_group.command(name="create", help="Record one bounded operational support request.")
    @common_options
    @topic_selection_options
    @click.option("--task-description", required=True, help="Specific operational support task.")
    @click.option("--scope-kind", required=True, help="Supported domain scope kind.")
    @click.option("--scope-ref", required=True, help="Supported scope stable ref.")
    @click.option("--expected-output-ref", "expected_output_refs", multiple=True, help="Expected support output ref.")
    @click.option("--authorization", required=True, help="Recorded support authorization scope.")
    @click.option("--dispatch-form", type=click.Choice(["tool_native_subagent", "launched_service_agent"]), required=True)
    @click.option("--completion-observation", "completion_observations", multiple=True, help="Terminal completion observation rule.")
    @click.option("--command-request-json", default=None, help="Provider-neutral command request object for synchronous dispatch.")
    @click.option("--actor-ref", required=True, help="Requesting Project Operator Session or Operator Agent ref.")
    @click.option("--id", "request_id", default=None, help="Explicit Service Request id.")
    @click.pass_context
    def service_requests_create(ctx: click.Context, **values: Any) -> int:
        return _with_service_request_service(
            ctx,
            values,
            lambda service: service.create(
                task=str(values["task_description"]),
                scope_kind=str(values["scope_kind"]),
                scope_ref=str(values["scope_ref"]),
                expected_output_refs=list(values["expected_output_refs"]),
                authorization=str(values["authorization"]),
                dispatch_form=str(values["dispatch_form"]),
                completion_observations=list(values["completion_observations"]),
                command_request=_object(values.get("command_request_json")),
                research_task_ref=values.get("research_task_id"),
                run_ref=values.get("run_id"),
                actor_ref=str(values["actor_ref"]),
                request_id=values.get("request_id"),
            ),
        )

    @service_requests_group.command(name="dispatch", help="Dispatch synchronously and wait for a terminal observation.")
    @common_options
    @topic_selection_options
    @click.option("--service-actor-ref", required=True, help="Handling Service Agent Instance or tool-native service actor ref.")
    @click.option("--timeout", "timeout_seconds", type=float, default=120.0, show_default=True)
    @click.option("--no-wait", is_flag=True, help="Rejected in the synchronous-only first release.")
    @click.argument("request_id")
    @click.pass_context
    def service_requests_dispatch(ctx: click.Context, request_id: str, **values: Any) -> int:
        return _with_service_request_service(ctx, values, lambda service: service.dispatch(request_id, service_actor_ref=str(values["service_actor_ref"]), timeout_seconds=float(values["timeout_seconds"]), no_wait=bool(values["no_wait"])))

    @service_requests_group.command(name="status", help="Inspect Service Request recovery and terminal observations.")
    @common_options
    @topic_selection_options
    @click.argument("request_id")
    @click.pass_context
    def service_requests_status(ctx: click.Context, request_id: str, **values: Any) -> int:
        return _with_service_request_service(ctx, values, lambda service: service.status(request_id))

    @project.group(name="runs", help="Create and checkpoint durable Kaoju procedure Runs.")
    def runs_group() -> None:
        pass

    @runs_group.command(name="begin", help="Begin a Research Task and Run.")
    @common_options
    @topic_selection_options
    @click.option("--procedure-id", required=True, help="Survey intent or compatibility procedure id.")
    @click.option("--control-mode", default="interactive", show_default=True, help="Run control mode.")
    @click.option("--input-ref", "input_refs", multiple=True, help="Input Artifact ref. Repeat as needed.")
    @click.option("--expected-output-ref", "expected_output_refs", multiple=True, help="Expected output ref. Repeat as needed.")
    @click.option("--stage-id", required=True, help="Initial workflow stage id.")
    @click.option("--id", "new_run_id", default=None, help="Explicit new Run id.")
    @click.option("--resume-hint", default=None, help="Exact resume instruction.")
    @click.pass_context
    def runs_begin(ctx: click.Context, **values: Any) -> int:
        return _with_run_service(ctx, values, lambda service: service.begin(procedure_id=str(values["procedure_id"]), control_mode=str(values["control_mode"]), input_refs=list(values["input_refs"]), expected_output_refs=list(values["expected_output_refs"]), stage_id=str(values["stage_id"]), research_task_id=values.get("research_task_id"), run_id=values.get("new_run_id"), resume_hint=values.get("resume_hint")))

    @runs_group.command(name="checkpoint", help="Record one resumable Run checkpoint.")
    @common_options
    @topic_selection_options
    @click.option("--stage-id", required=True, help="Current workflow stage id.")
    @click.option("--completed-ref", "completed_refs", multiple=True, help="Completed Artifact ref.")
    @click.option("--pending-gate-ref", default=None, help="Pending Gate ref.")
    @click.option("--blocker-ref", "blocker_refs", multiple=True, help="Blocker ref.")
    @click.option("--service-request-ref", "service_request_refs", multiple=True, help="Service Request ref.")
    @click.option("--resume-hint", default=None, help="Exact resume instruction.")
    @click.option("--status", type=click.Choice(["running", "blocked"]), default="running")
    @click.argument("run_id")
    @click.pass_context
    def runs_checkpoint(ctx: click.Context, run_id: str, **values: Any) -> int:
        return _with_run_service(ctx, values, lambda service: service.checkpoint(run_id, stage_id=str(values["stage_id"]), completed_refs=list(values["completed_refs"]), pending_gate_ref=values.get("pending_gate_ref"), blocker_refs=list(values["blocker_refs"]), service_request_refs=list(values["service_request_refs"]), resume_hint=values.get("resume_hint"), status=str(values["status"])))

    @runs_group.command(name="status", help="Show current Run checkpoint state.")
    @common_options
    @topic_selection_options
    @click.argument("run_id")
    @click.pass_context
    def runs_status(ctx: click.Context, run_id: str, **values: Any) -> int:
        return _with_run_service(ctx, values, lambda service: service.status(run_id))

    @runs_group.command(name="complete", help="Seal a Run with an immutable terminal state.")
    @common_options
    @topic_selection_options
    @click.option("--terminal-status", type=click.Choice(["complete", "failed", "stopped", "cancelled"]), required=True)
    @click.option("--completed-ref", "completed_refs", multiple=True, help="Completed Artifact ref.")
    @click.option("--blocker-ref", "blocker_refs", multiple=True, help="Blocker ref.")
    @click.option("--resume-hint", default=None, help="Exact resume instruction for non-success terminal states.")
    @click.argument("run_id")
    @click.pass_context
    def runs_complete(ctx: click.Context, run_id: str, **values: Any) -> int:
        return _with_run_service(ctx, values, lambda service: service.complete(run_id, terminal_status=str(values["terminal_status"]), completed_refs=list(values["completed_refs"]), blocker_refs=list(values["blocker_refs"]), resume_hint=values.get("resume_hint")))


def _with_artifact_service(ctx: click.Context, values: dict[str, Any], callback: Callable[[KaojuArtifactService], dict[str, object]]) -> int:
    return _with_service(ctx, values, lambda context: callback(KaojuArtifactService(context, env=os.environ, cwd=Path.cwd())))


def _with_run_service(ctx: click.Context, values: dict[str, Any], callback: Callable[[KaojuRunService], dict[str, object]]) -> int:
    return _with_service(ctx, values, lambda context: callback(KaojuRunService(context, env=os.environ, cwd=Path.cwd())))


def _with_repository_service(ctx: click.Context, values: dict[str, Any], callback: Callable[[KaojuRepositoryService], dict[str, object]]) -> int:
    return _with_service(ctx, values, lambda context: callback(KaojuRepositoryService(context, env=os.environ, cwd=Path.cwd())))


def _with_service_request_service(ctx: click.Context, values: dict[str, Any], callback: Callable[[KaojuServiceRequestService], dict[str, object]]) -> int:
    return _with_service(ctx, values, lambda context: callback(KaojuServiceRequestService(context, env=os.environ, cwd=Path.cwd())))


def _with_service(ctx: click.Context, values: dict[str, Any], callback: Callable[[Any], dict[str, object]]) -> int:
    options = merge_options(ctx, project=values.get("project"), manifest=values.get("manifest"), research_topic_id=values.get("research_topic_id"), topic_workspace_id=values.get("topic_workspace_id"), research_inquiry_id=values.get("research_inquiry_id"), research_task_id=values.get("research_task_id"), run_id=values.get("run_id"), agent_team_instance_id=values.get("agent_team_instance_id"), agent_instance_id=values.get("agent_instance_id"), topic_agent_team_profile_id=values.get("topic_agent_team_profile_id"))
    context, diagnostics = _context_for_options(options)
    if context is None:
        payload: dict[str, object] = {"ok": False, "mutated": False, "error": {"code": "context_resolution_failed", "message": "Select one Topic Workspace."}}
    else:
        try:
            payload = callback(context)
        except KaojuServiceError as exc:
            payload = exc.payload()
        except (json.JSONDecodeError, ValueError) as exc:
            payload = {"ok": False, "mutated": False, "error": {"code": "invalid_request", "message": str(exc)}, "recovery_actions": []}
    operation = str(payload.get("operation") or "error")
    lines = _human_lines(operation, payload)
    return emit_output(f"project.{operation}", options, payload, diagnostics, lines)


def _object_list(value: object) -> list[dict[str, object]]:
    if value is None:
        return []
    loaded = json.loads(str(value))
    if not isinstance(loaded, list) or any(not isinstance(item, dict) for item in loaded):
        raise ValueError("relationships-json must be an array of objects.")
    return [{str(key): item for key, item in entry.items()} for entry in loaded]


def _object(value: object) -> dict[str, object] | None:
    if value is None:
        return None
    loaded = json.loads(str(value))
    if not isinstance(loaded, dict):
        raise ValueError("command-request-json must be an object.")
    return {str(key): item for key, item in loaded.items()}


def _human_lines(operation: str, payload: dict[str, object]) -> list[str]:
    if payload.get("ok") is False:
        error = payload.get("error")
        return [str(error.get("message"))] if isinstance(error, dict) else ["Kaoju service command failed."]
    refs = payload.get("affected_refs")
    suffix = f": {', '.join(str(value) for value in refs)}" if isinstance(refs, list) and refs else ""
    return [f"{operation} succeeded{suffix}"]
