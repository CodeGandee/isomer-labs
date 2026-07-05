"""Click registration for Topic Workspace reset commands."""

from __future__ import annotations

import os
from typing import Any, Callable

import click

from isomer_labs.cli.handlers.shared import _context_for_options
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.cli.output import emit_output
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.workspace.reset import (
    apply_topic_reset,
    create_reset_checkpoint,
    list_reset_checkpoints,
    plan_topic_reset,
    show_reset_checkpoint,
    show_reset_plan,
    update_reset_checkpoint,
)


def register_topic_reset_commands(app: click.Group) -> None:
    @app.group(name="topic-reset", help="Topic Workspace reset checkpoint commands.")
    def topic_reset_group() -> None:
        pass

    @topic_reset_group.command(name="checkpoint", help="Create a reset checkpoint for the selected Topic Workspace.")
    @_common_options
    @_topic_selection_options
    @click.option("--actor", "actor_ref", default=None, help="Actor or operator ref to record.")
    @click.option("--id", "checkpoint_id", default=None, help="Explicit reset checkpoint id.")
    @click.option("--render", "render_format", default=None, help="Render a generated review view, for example markdown.")
    @click.pass_context
    def checkpoint_command(ctx: click.Context, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            kwargs,
            "project topic-reset checkpoint",
            lambda context: create_reset_checkpoint(
                context,
                env=os.environ,
                actor_ref=kwargs.get("actor_ref"),
                checkpoint_id=kwargs.get("checkpoint_id"),
                render_markdown=kwargs.get("render_format") == "markdown",
            ),
        )

    @topic_reset_group.command(name="update-checkpoint", help="Extend a reset checkpoint with preserved setup evidence.")
    @_common_options
    @_topic_selection_options
    @click.option("--actor", "actor_ref", default=None, help="Actor or operator ref to record.")
    @click.option("--source-label", default=None, help="Preparation workflow or skill label that owns this update.")
    @click.option("--preserve-record", "preserve_record_ids", multiple=True, help="Lifecycle record id to preserve. Repeatable.")
    @click.option("--preserve-structured-payload", "preserve_structured_payload_ids", multiple=True, help="Structured payload record id to preserve. Repeatable.")
    @click.option("--preserve-generated-view", "preserve_generated_view_paths", multiple=True, help="Generated view path to preserve. Repeatable.")
    @click.option("--preserve-semantic-label", "preserve_semantic_labels", multiple=True, help="Semantic label to preserve. Repeatable.")
    @click.option("--preserve-support-path", "preserve_support_paths", multiple=True, help="Support path to preserve. Repeatable.")
    @click.option("--provenance-ref", "provenance_refs", multiple=True, help="Provenance ref for this update. Repeatable.")
    @click.option("--render", "render_format", default=None, help="Render a generated review view, for example markdown.")
    @click.argument("checkpoint_id")
    @click.pass_context
    def update_checkpoint_command(ctx: click.Context, checkpoint_id: str, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            kwargs,
            "project topic-reset update-checkpoint",
            lambda context: update_reset_checkpoint(
                context,
                checkpoint_id,
                env=os.environ,
                actor_ref=kwargs.get("actor_ref"),
                preserve_record_ids=list(kwargs.get("preserve_record_ids") or []),
                preserve_structured_payload_ids=list(kwargs.get("preserve_structured_payload_ids") or []),
                preserve_generated_view_paths=list(kwargs.get("preserve_generated_view_paths") or []),
                preserve_semantic_labels=list(kwargs.get("preserve_semantic_labels") or []),
                preserve_support_paths=list(kwargs.get("preserve_support_paths") or []),
                provenance_refs=list(kwargs.get("provenance_refs") or []),
                source_label=kwargs.get("source_label"),
                render_markdown=kwargs.get("render_format") == "markdown",
            ),
        )

    @topic_reset_group.command(name="list", help="List reset checkpoints for the selected Topic Workspace.")
    @_common_options
    @_topic_selection_options
    @click.option("--include-payload", is_flag=True, help="Include structured checkpoint payloads.")
    @click.pass_context
    def list_command(ctx: click.Context, include_payload: bool = False, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            kwargs,
            "project topic-reset list",
            lambda context: list_reset_checkpoints(context, env=os.environ, include_payload=include_payload),
        )

    @topic_reset_group.command(name="show", help="Show a reset checkpoint.")
    @_common_options
    @_topic_selection_options
    @click.option("--include-payload", is_flag=True, help="Include structured checkpoint payload.")
    @click.option("--include-rendered-body", is_flag=True, help="Include rendered Markdown body when present.")
    @click.argument("checkpoint_id")
    @click.pass_context
    def show_command(ctx: click.Context, checkpoint_id: str, include_payload: bool = False, include_rendered_body: bool = False, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            kwargs,
            "project topic-reset show",
            lambda context: show_reset_checkpoint(
                context,
                checkpoint_id,
                env=os.environ,
                include_payload=include_payload,
                include_rendered_body=include_rendered_body,
            ),
        )

    @topic_reset_group.command(name="plan", help="Create a read-only reset plan from a checkpoint.")
    @_common_options
    @_topic_selection_options
    @click.option("--actor", "actor_ref", default=None, help="Actor or operator ref to record.")
    @click.option("--id", "plan_id", default=None, help="Explicit reset plan id.")
    @click.option("--render", "render_format", default=None, help="Render a generated review view, for example markdown.")
    @click.argument("checkpoint_id")
    @click.pass_context
    def plan_command(ctx: click.Context, checkpoint_id: str, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            kwargs,
            "project topic-reset plan",
            lambda context: plan_topic_reset(
                context,
                checkpoint_id,
                env=os.environ,
                actor_ref=kwargs.get("actor_ref"),
                plan_id=kwargs.get("plan_id"),
                render_markdown=kwargs.get("render_format") == "markdown",
            ),
        )

    @topic_reset_group.command(name="show-plan", help="Show a reset plan.")
    @_common_options
    @_topic_selection_options
    @click.option("--include-payload", is_flag=True, help="Include structured plan payload.")
    @click.option("--include-rendered-body", is_flag=True, help="Include rendered Markdown body when present.")
    @click.argument("plan_id")
    @click.pass_context
    def show_plan_command(ctx: click.Context, plan_id: str, include_payload: bool = False, include_rendered_body: bool = False, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            kwargs,
            "project topic-reset show-plan",
            lambda context: show_reset_plan(
                context,
                plan_id,
                env=os.environ,
                include_payload=include_payload,
                include_rendered_body=include_rendered_body,
            ),
        )

    @topic_reset_group.command(name="apply", help="Apply an approved destructive reset plan.")
    @_common_options
    @_topic_selection_options
    @click.option("--actor", "actor_ref", default=None, help="Actor or operator ref to record.")
    @click.option("--yes", is_flag=True, help="Apply the reviewed destructive reset plan.")
    @click.option("--render", "render_format", default=None, help="Render a generated outcome review view, for example markdown.")
    @click.argument("checkpoint_id")
    @click.argument("plan_id")
    @click.pass_context
    def apply_command(ctx: click.Context, checkpoint_id: str, plan_id: str, yes: bool = False, **kwargs: Any) -> int:
        return _with_context(
            ctx,
            kwargs,
            "project topic-reset apply",
            lambda context: apply_topic_reset(
                context,
                env=os.environ,
                checkpoint_id=checkpoint_id,
                plan_id=plan_id,
                actor_ref=kwargs.get("actor_ref"),
                yes=yes,
                render_markdown=kwargs.get("render_format") == "markdown",
            ),
        )


def _with_context(
    ctx: click.Context,
    values: dict[str, Any],
    command: str,
    callback: Callable[[EffectiveTopicContext], tuple[dict[str, Any], list[Diagnostic]]],
) -> int:
    options = _merge_options(
        ctx,
        project=values.get("project"),
        manifest=values.get("manifest"),
        research_topic_id=values.get("research_topic_id"),
        topic_workspace_id=values.get("topic_workspace_id"),
        research_inquiry_id=values.get("research_inquiry_id"),
        research_task_id=values.get("research_task_id"),
        run_id=values.get("run_id"),
        agent_team_instance_id=values.get("agent_team_instance_id"),
        agent_instance_id=values.get("agent_instance_id"),
        topic_agent_team_profile_id=values.get("topic_agent_team_profile_id"),
    )
    context, diagnostics = _context_for_options(options)
    if context is None or has_errors(diagnostics):
        payload = {
            "ok": False,
            "mutated": False,
            "operation": command.rsplit(" ", 1)[-1],
            "error": {
                "code": "context_resolution_failed",
                "message": "Topic reset commands require a selected Isomer Topic Workspace.",
            },
        }
        return emit_output(command, options, payload, diagnostics, [])
    payload, call_diagnostics = callback(context)
    all_diagnostics = [*diagnostics, *call_diagnostics]
    return emit_output(command, options, payload, all_diagnostics, _text_lines(payload))


def _text_lines(payload: dict[str, Any]) -> list[str]:
    if payload.get("ok") is False:
        return []
    operation = str(payload.get("operation") or "topic-reset")
    lines = [f"Topic reset {operation}: ok"]
    for key in ("checkpoint_id", "plan_id", "outcome_id", "rendered_markdown_path"):
        value = payload.get(key)
        if value is not None:
            lines.append(f"{key}: {value}")
    blockers = payload.get("blockers")
    if isinstance(blockers, list) and blockers:
        lines.append(f"blockers: {len(blockers)}")
    return lines
