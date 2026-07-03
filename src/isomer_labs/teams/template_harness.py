"""Domain Agent Team Template harness and workspace-contract checks."""

from __future__ import annotations

from pathlib import Path
import subprocess
from typing import Any

from isomer_labs.core.diagnostics import Diagnostic


def validate_workspace_contract(source_path: Path, raw: dict[str, Any], diagnostics: list[Diagnostic]) -> None:
    rules = _dict_items(raw.get("read_write_rules"))
    if "no-workspace-local-teams" not in {_string(item.get("id")) for item in rules}:
        diagnostics.append(
            Diagnostic(
                code="ISO017",
                severity="error",
                concept="Domain Agent Team Template workspace contract",
                path=source_path / "specs/workspace/workspace.toml",
                field="read_write_rules",
                message="Workspace contract must prohibit a workspace-local teams directory.",
            )
        )


def harness_diagnostics(source_path: Path) -> list[Diagnostic]:
    harness = source_path / "harness/bin/deepsci-org"
    if not harness.exists():
        return []
    try:
        result = subprocess.run(
            [str(harness), "validate"],
            cwd=source_path,
            text=True,
            capture_output=True,
            timeout=15,
            check=False,
        )
    except OSError as exc:
        return [
            Diagnostic(
                code="ISO021",
                severity="warning",
                concept="Domain Agent Team Template harness",
                path=harness,
                message=f"Generated harness validation could not be run: {exc}.",
            )
        ]
    except subprocess.TimeoutExpired:
        return [
            Diagnostic(
                code="ISO021",
                severity="warning",
                concept="Domain Agent Team Template harness",
                path=harness,
                message="Generated harness validation timed out.",
            )
        ]
    if result.returncode == 0:
        return []
    message = (result.stderr or result.stdout or "Generated harness validation failed.").strip().splitlines()[0]
    return [
        Diagnostic(
            code="ISO021",
            severity="error",
            concept="Domain Agent Team Template harness",
            path=harness,
            message=message,
        )
    ]


def _dict_items(value: object) -> list[dict[str, Any]]:
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    if isinstance(value, dict):
        return [value]
    return []


def _string(value: object) -> str | None:
    if isinstance(value, str) and value:
        return value
    return None
