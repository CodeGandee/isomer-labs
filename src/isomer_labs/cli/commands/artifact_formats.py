"""Click registration for generic Artifact Format commands."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import click

from isomer_labs.artifact_formats import (
    ArtifactFormatRegistry,
    WorkspaceRuntimeArtifactFormatProvider,
    register_custom_artifact_format,
    render_artifact,
    validate_payload,
)
from isomer_labs.artifact_formats.validation import load_payload_file
from isomer_labs.cli.handlers.shared import _context_for_options
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.cli.output import emit_output, output_format
from isomer_labs.deepsci_ext.record_formats import register_deepsci_record_format_provider
from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.runtime.store import open_workspace_runtime


def register_artifact_format_commands(app: click.Group) -> None:
    @app.group(name="artifact-formats", help="Validate, render, and register Artifact Formats.")
    def artifact_formats_group() -> None:
        pass

    @artifact_formats_group.command(name="validate", help="Validate a JSON payload against an Artifact Format.")
    @_common_options
    @_topic_selection_options
    @_schema_selector_options
    @click.option("--payload-file", type=click.Path(path_type=Path), required=True, help="JSON payload file to validate.")
    @click.pass_context
    def validate_command(ctx: click.Context, **kwargs: Any) -> int:
        return _run_validate(ctx, kwargs)

    @artifact_formats_group.command(name="render", help="Render a JSON payload through an Artifact Format template.")
    @_common_options
    @_topic_selection_options
    @_schema_selector_options
    @_template_selector_options
    @click.option("--payload-file", type=click.Path(path_type=Path), required=True, help="JSON payload file to render.")
    @click.option("--format", "render_format", default="markdown", show_default=True, help="Output format to render.")
    @click.option("--output-file", type=click.Path(path_type=Path), default=None, help="Optional file path for rendered content.")
    @click.pass_context
    def render_command(ctx: click.Context, **kwargs: Any) -> int:
        return _run_render(ctx, kwargs)

    @artifact_formats_group.command(name="register", help="Register a custom Topic Workspace Artifact Format.")
    @_common_options
    @_topic_selection_options
    @click.option("--format-profile", "format_profile_ref", required=True, help="custom: Artifact Format Profile ref.")
    @click.option("--schema-file", type=click.Path(path_type=Path), required=True, help="JSON Schema file to snapshot.")
    @click.option("--template-file", type=click.Path(path_type=Path), required=True, help="Jinja2 template file to snapshot.")
    @click.option("--format", "output_format_name", default="markdown", show_default=True, help="Template output format.")
    @click.option("--replace", is_flag=True, help="Replace an existing custom registration.")
    @click.pass_context
    def register_command(ctx: click.Context, **kwargs: Any) -> int:
        return _run_register(ctx, kwargs)


def _schema_selector_options(command: Any) -> Any:
    command = click.option("--schema-file", type=click.Path(path_type=Path), default=None, help="Plain JSON Schema file.")(command)
    command = click.option("--schema-ref", default=None, help="Artifact Format schema ref.")(command)
    command = click.option("--format-profile", "format_profile_ref", default=None, help="Artifact Format Profile ref.")(command)
    return command


def _template_selector_options(command: Any) -> Any:
    command = click.option("--template-file", type=click.Path(path_type=Path), default=None, help="Plain Jinja2 template file.")(command)
    command = click.option("--template-ref", default=None, help="Artifact Format template ref.")(command)
    return command


def _run_validate(ctx: click.Context, values: dict[str, Any]) -> int:
    options, context, diagnostics = _resolve_context(ctx, values, read_only=True)
    registry = ArtifactFormatRegistry()
    register_deepsci_record_format_provider(registry)
    runtime_store = None
    if context is not None:
        runtime_store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=True)
        diagnostics.extend(runtime_diagnostics)
        if runtime_store is not None:
            registry.register_provider(
                WorkspaceRuntimeArtifactFormatProvider(runtime_store, topic_workspace_id=context.topic_workspace_id)
            )
    payload, payload_diagnostics = load_payload_file(values["payload_file"])
    diagnostics.extend(payload_diagnostics)
    validation = None
    if payload is not None and not has_errors(diagnostics):
        validation = validate_payload(
            payload,
            registry=registry,
            format_profile_ref=values.get("format_profile_ref"),
            schema_ref=values.get("schema_ref"),
            schema_file=values.get("schema_file"),
        )
        diagnostics.extend(validation.diagnostics)
    if runtime_store is not None:
        runtime_store.close()
    payload_json: dict[str, Any] = {
        "ok": validation.ok if validation is not None else False,
        "mutated": False,
        "operation": "artifact-formats validate",
    }
    if validation is not None:
        payload_json["validation"] = validation.to_json()
    return _emit_artifact_format("artifact-formats validate", options, payload_json, diagnostics, [])


def _run_render(ctx: click.Context, values: dict[str, Any]) -> int:
    options, context, diagnostics = _resolve_context(ctx, values, read_only=True)
    registry = ArtifactFormatRegistry()
    register_deepsci_record_format_provider(registry)
    runtime_store = None
    if context is not None:
        runtime_store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=True)
        diagnostics.extend(runtime_diagnostics)
        if runtime_store is not None:
            registry.register_provider(
                WorkspaceRuntimeArtifactFormatProvider(runtime_store, topic_workspace_id=context.topic_workspace_id)
            )
    payload, payload_diagnostics = load_payload_file(values["payload_file"])
    diagnostics.extend(payload_diagnostics)
    render = None
    output_file = values.get("output_file")
    if payload is not None and not has_errors(diagnostics):
        render = render_artifact(
            payload,
            registry=registry,
            output_format=str(values.get("render_format") or "markdown"),
            format_profile_ref=values.get("format_profile_ref"),
            schema_ref=values.get("schema_ref"),
            template_ref=values.get("template_ref"),
            schema_file=values.get("schema_file"),
            template_file=values.get("template_file"),
        )
        diagnostics.extend(render.diagnostics)
        if render.ok and output_file is not None and render.content is not None:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(render.content, encoding="utf-8")
    if runtime_store is not None:
        runtime_store.close()
    payload_json: dict[str, Any] = {
        "ok": render.ok if render is not None else False,
        "mutated": False,
        "operation": "artifact-formats render",
    }
    if render is not None:
        payload_json["render"] = render.to_json(include_content=True)
    if output_file is not None:
        payload_json["output_file"] = str(output_file)
    text_lines: list[str] = []
    if render is not None and render.ok and render.content is not None:
        text_lines = [f"Rendered Artifact Format to {output_file}"] if output_file is not None else [render.content]
    return _emit_artifact_format("artifact-formats render", options, payload_json, diagnostics, text_lines)


def _run_register(ctx: click.Context, values: dict[str, Any]) -> int:
    options, context, diagnostics = _resolve_context(ctx, values, read_only=False)
    registration = None
    if context is not None and not has_errors(diagnostics):
        runtime_store, runtime_diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
        diagnostics.extend(runtime_diagnostics)
        if runtime_store is not None:
            try:
                registration, register_diagnostics = register_custom_artifact_format(
                    runtime_store,
                    context,
                    format_profile_ref=values["format_profile_ref"],
                    schema_file=values["schema_file"],
                    template_file=values["template_file"],
                    output_format=str(values.get("output_format_name") or "markdown"),
                    replace=bool(values.get("replace")),
                )
                diagnostics.extend(register_diagnostics)
            finally:
                runtime_store.close()
    payload_json: dict[str, Any] = {
        "ok": registration is not None and not has_errors(diagnostics),
        "mutated": registration is not None and not has_errors(diagnostics),
        "operation": "artifact-formats register",
        "registration": registration.to_json() if registration is not None else None,
    }
    lines = [f"Registered Artifact Format: {registration.format_profile_ref}"] if registration is not None else []
    return _emit_artifact_format("artifact-formats register", options, payload_json, diagnostics, lines)


def _resolve_context(
    ctx: click.Context,
    values: dict[str, Any],
    *,
    read_only: bool,
) -> tuple[Any, Any, list[Diagnostic]]:
    options = _merge_options(
        ctx,
        project=values.get("project"),
        manifest=values.get("manifest"),
        output_format=values.get("output_format"),
        json_output=bool(values.get("json_output", False)),
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
    if context is None:
        diagnostics.append(
            Diagnostic(
                code="ISO203" if read_only else "ISO206",
                severity="error",
                concept="Effective Topic Context",
                message="Artifact Format commands require a selected Isomer Topic Workspace.",
            )
        )
    return options, context, diagnostics


def _emit_artifact_format(
    command: str,
    options: Any,
    payload: dict[str, Any],
    diagnostics: list[Diagnostic],
    text_lines: list[str],
) -> int:
    if output_format(options) == "json":
        return emit_output(f"project {command}", options, payload, diagnostics, text_lines)
    return emit_output(command, options, payload, diagnostics, text_lines)
