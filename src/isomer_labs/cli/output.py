"""Shared output mode helpers for Isomer CLI commands."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import click

from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.rendering import render_diagnostics, render_json


@dataclass(frozen=True)
class OutputMode:
    """Root-selected CLI rendering mode."""

    print_json: bool = False

    @property
    def format_name(self) -> str:
        return "json" if self.print_json else "text"


def output_format(options: Any) -> str:
    output_mode = getattr(options, "output_mode", OutputMode())
    if isinstance(output_mode, OutputMode):
        return output_mode.format_name
    if bool(getattr(options, "json_output", False)):
        return "json"
    return str(getattr(options, "output_format", "text") or "text")


def emit_output(
    command: str,
    options: Any,
    payload: dict[str, Any],
    diagnostics: list[Diagnostic],
    text_lines: list[str],
) -> int:
    if output_format(options) == "json":
        click.echo(render_json(command, payload, diagnostics))
    else:
        lines = [*text_lines, *render_diagnostics(diagnostics)]
        if lines:
            click.echo("\n".join(lines))
    if payload.get("ok") is False:
        return 1
    return 1 if has_errors(diagnostics) else 0
