"""Click registration for DeepScientist compatibility extension commands."""

from __future__ import annotations

import json
import os
from typing import Any

import click

from isomer_labs.cli.handlers.shared import _context_for_options
from isomer_labs.cli.options import (
    common_options as _common_options,
    merge_options as _merge_options,
    topic_selection_options as _topic_selection_options,
)
from isomer_labs.deepsci_ext.tools import (
    DeepSciCompatError,
    call_tool,
    dumps_raw_json,
    load_input_json,
    split_tool_name,
    tool_listing,
    unsupported_tool_payload,
)
from isomer_labs.core.diagnostics import has_errors


def register_deepsci_ext_commands(app: click.Group) -> None:
    @app.group(name="ext", help="Use extension command surfaces for research records, ideas, and compatibility tooling.")
    def ext_group() -> None:
        pass

    @ext_group.group(name="deepsci", help="DeepScientist compatibility extension.")
    def deepsci_group() -> None:
        pass

    @deepsci_group.command(name="tools", help="List DeepScientist compatibility tools.")
    @click.argument("namespace", required=False)
    def deepsci_tools_command(namespace: str | None = None) -> int:
        click.echo(dumps_raw_json(tool_listing(namespace)))
        return 0

    @deepsci_group.command(name="call", help="Call a mocked DeepScientist-compatible tool.")
    @_common_options
    @_topic_selection_options
    @click.option("--input-json", default=None, help="JSON object to pass as DeepScientist tool arguments. Use '-' for stdin.")
    @click.argument("tool_name")
    @click.pass_context
    def deepsci_call_command(
        ctx: click.Context,
        tool_name: str,
        input_json: str | None = None,
        project: str | None = None,
        manifest: str | None = None,
        output_format: str | None = None,
        json_output: bool = False,
        research_topic_id: str | None = None,
        topic_workspace_id: str | None = None,
        research_inquiry_id: str | None = None,
        research_task_id: str | None = None,
        run_id: str | None = None,
        agent_team_instance_id: str | None = None,
        agent_instance_id: str | None = None,
        topic_agent_team_profile_id: str | None = None,
    ) -> int:
        if split_tool_name(tool_name) is None:
            click.echo(dumps_raw_json(unsupported_tool_payload(tool_name)))
            return 1
        try:
            arguments = load_input_json(input_json)
        except (ValueError, json.JSONDecodeError) as exc:
            click.echo(
                dumps_raw_json(
                    {
                        "ok": False,
                        "tool_name": tool_name,
                        "error": {
                            "code": "invalid_input_json",
                            "message": str(exc),
                        },
                    }
                )
            )
            return 1
        options = _merge_options(
            ctx,
            project=project,
            manifest=manifest,
            output_format=output_format,
            json_output=json_output,
            research_topic_id=research_topic_id,
            topic_workspace_id=topic_workspace_id,
            research_inquiry_id=research_inquiry_id,
            research_task_id=research_task_id,
            run_id=run_id,
            agent_team_instance_id=agent_team_instance_id,
            agent_instance_id=agent_instance_id,
            topic_agent_team_profile_id=topic_agent_team_profile_id,
        )
        context, diagnostics = _context_for_options(options)
        if context is None or has_errors(diagnostics):
            click.echo(
                dumps_raw_json(
                    {
                        "ok": False,
                        "tool_name": tool_name,
                        "error": {
                            "code": "context_resolution_failed",
                            "message": "DeepScientist compatibility call requires a selected Isomer Topic Workspace.",
                        },
                        "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
                    }
                )
            )
            return 1
        try:
            payload, call_diagnostics = call_tool(context, tool_name, arguments, env=os.environ)
        except DeepSciCompatError as exc:
            click.echo(dumps_raw_json(exc.to_payload(tool_name=tool_name)))
            return 1
        if call_diagnostics and has_errors(call_diagnostics):
            payload = {
                **payload,
                "diagnostics": [diagnostic.to_json() for diagnostic in call_diagnostics],
            }
        click.echo(dumps_raw_json(_ensure_tool_payload(payload, tool_name=tool_name)))
        return 0 if payload.get("ok") is not False and not has_errors(call_diagnostics) else 1


def _ensure_tool_payload(payload: dict[str, Any], *, tool_name: str) -> dict[str, Any]:
    if "tool_name" in payload:
        return payload
    return {
        "tool_name": tool_name,
        **payload,
    }
