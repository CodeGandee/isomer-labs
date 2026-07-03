"""Agent-readable failure output for the installed Isomer CLI."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import os
import sys
import traceback
from typing import Any

import click

from isomer_labs.cli.examples import COMMAND_EXAMPLES, examples_for_command
from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.core.rendering import render_diagnostics, render_json


VALUE_OPTIONS = {
    "--agent",
    "--agent-instance",
    "--agent-team-instance",
    "--content-dir",
    "--format",
    "--manifest",
    "--part",
    "--path",
    "--payload-json",
    "--project",
    "--research-inquiry",
    "--root",
    "--run",
    "--source",
    "--statement",
    "--storage-profile",
    "--task",
    "--to",
    "--topic",
    "--topic-agent-team-profile",
    "--topic-workspace",
    "--workspace-dir",
}

DEBUG_ENV = "ISOMER_CLI_DEBUG"
PROG_NAME = "isomer-cli"


def normalize_raw_args(argv: Sequence[str] | None) -> list[str]:
    if argv is not None:
        return list(argv)
    return list(sys.argv[1:])


def raw_print_json(argv: Sequence[str]) -> bool:
    return "--print-json" in argv


def raw_debug_enabled(argv: Sequence[str], env: Mapping[str, str] | None = None) -> bool:
    environment = os.environ if env is None else env
    return "--debug" in argv or environment.get(DEBUG_ENV) == "1"


def emit_click_exception(
    exc: click.ClickException,
    argv: Sequence[str],
    *,
    debug: bool,
) -> int:
    command = command_path_for_exception(exc, argv)
    diagnostic = diagnostic_for_click_exception(exc, command)
    return emit_cli_failure(
        command,
        argv,
        [diagnostic],
        {"ok": False, "mutated": False},
        exit_code=int(exc.exit_code),
        debug=debug,
    )


def emit_keyboard_interrupt(argv: Sequence[str], *, debug: bool) -> int:
    command = infer_command_path(argv)
    diagnostic = Diagnostic(
        code="ISOCLI130",
        severity="error",
        concept="CLI invocation",
        message="Command interrupted by user.",
    )
    return emit_cli_failure(
        command,
        argv,
        [diagnostic],
        {"ok": False, "mutation_state": "unknown"},
        exit_code=130,
        debug=debug,
    )


def emit_unexpected_exception(exc: BaseException, argv: Sequence[str], *, debug: bool) -> int:
    command = infer_command_path(argv)
    diagnostic = Diagnostic(
        code="ISOCLI500",
        severity="error",
        concept="CLI internal error",
        message="isomer-cli hit an unexpected internal error.",
        hint=f"Run again with --debug or {DEBUG_ENV}=1 to include traceback details.",
    )
    debug_payload: dict[str, object] | None = None
    if debug:
        debug_payload = {
            "exception_type": type(exc).__name__,
            "traceback": traceback.format_exception(type(exc), exc, exc.__traceback__),
        }
    return emit_cli_failure(
        command,
        argv,
        [diagnostic],
        {"ok": False, "mutation_state": "unknown"},
        exit_code=1,
        debug=debug,
        debug_payload=debug_payload,
    )


def emit_cli_failure(
    command: str,
    argv: Sequence[str],
    diagnostics: list[Diagnostic],
    payload: dict[str, Any],
    *,
    exit_code: int,
    debug: bool,
    debug_payload: dict[str, object] | None = None,
) -> int:
    if debug_payload is not None:
        payload = {**payload, "debug": debug_payload}
    if raw_print_json(argv):
        click.echo(render_json(command, payload, diagnostics))
        return exit_code
    lines = render_diagnostics(diagnostics)
    if "mutated" in payload:
        lines.append(f"Mutated: {str(payload['mutated']).lower()}")
    if "mutation_state" in payload:
        lines.append(f"Mutation state: {payload['mutation_state']}")
    if debug_payload is not None:
        lines.append("Debug traceback:")
        trace_lines = debug_payload.get("traceback", [])
        if isinstance(trace_lines, list):
            lines.extend(str(line).rstrip() for line in trace_lines)
    if lines:
        click.echo("\n".join(lines))
    return exit_code


def diagnostic_for_click_exception(exc: click.ClickException, command: str) -> Diagnostic:
    usage_error = isinstance(exc, click.UsageError)
    code = "ISOCLI001" if usage_error else "ISOCLI002"
    concept = "CLI invocation" if usage_error else "CLI execution"
    message = _click_message(exc)
    usage = _usage_for_exception(exc)
    examples = examples_for_command(command) if usage_error else ()
    return Diagnostic(
        code=code,
        severity="error",
        concept=concept,
        message=message,
        field=_field_for_exception(exc),
        hint=_hint_for_exception(exc),
        usage=usage,
        examples=examples,
    )


def command_path_for_exception(exc: click.ClickException, argv: Sequence[str]) -> str:
    ctx = getattr(exc, "ctx", None)
    if isinstance(ctx, click.Context):
        command_path = _strip_prog_name(ctx.command_path)
        if command_path:
            return nearest_registered_command(command_path)
    return infer_command_path(argv)


def infer_command_path(argv: Sequence[str]) -> str:
    positional = _positional_tokens(argv)
    while positional:
        candidate = " ".join(positional)
        nearest = nearest_registered_command(candidate)
        if nearest:
            return nearest
        positional = positional[:-1]
    return "project"


def nearest_registered_command(command_path: str) -> str:
    parts = command_path.split()
    while parts:
        candidate = " ".join(parts)
        if candidate in COMMAND_EXAMPLES:
            return candidate
        parts = parts[:-1]
    return "project"


def _positional_tokens(argv: Sequence[str]) -> list[str]:
    tokens: list[str] = []
    skip_next = False
    for value in argv:
        if skip_next:
            skip_next = False
            continue
        if value == "--":
            break
        if value.startswith("--"):
            option_name = value.split("=", 1)[0]
            skip_next = option_name in VALUE_OPTIONS and "=" not in value
            continue
        if value.startswith("-"):
            continue
        tokens.append(value)
    return tokens


def _strip_prog_name(command_path: str) -> str:
    parts = command_path.split()
    if parts and parts[0] == PROG_NAME:
        parts = parts[1:]
    return " ".join(parts)


def _click_message(exc: click.ClickException) -> str:
    formatter = getattr(exc, "format_message", None)
    if callable(formatter):
        return str(formatter())
    return str(exc)


def _usage_for_exception(exc: click.ClickException) -> str | None:
    ctx = getattr(exc, "ctx", None)
    if not isinstance(ctx, click.Context):
        return None
    try:
        usage = ctx.get_usage().strip()
    except click.ClickException:
        return None
    return usage.removeprefix("Usage: ").strip()


def _field_for_exception(exc: click.ClickException) -> str | None:
    param = getattr(exc, "param", None)
    name = getattr(param, "name", None)
    if isinstance(name, str):
        return name
    option_name = getattr(exc, "option_name", None)
    if isinstance(option_name, str):
        return option_name
    return None


def _hint_for_exception(exc: click.ClickException) -> str:
    if isinstance(exc, click.MissingParameter):
        return "Pass the required argument or option shown in Usage."
    if isinstance(exc, click.NoSuchOption):
        return "Remove the unsupported option or choose one of the command examples below."
    if isinstance(exc, click.BadParameter):
        return "Use one of the accepted values or formats shown by the selected command help."
    if isinstance(exc, click.UsageError):
        return "Use the expected command shape shown in Usage."
    return "Review the diagnostic and rerun the command after correcting the CLI invocation."
