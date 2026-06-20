"""Text and JSON render helpers shared by CLI commands."""

from __future__ import annotations

import json
from typing import Any

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.models import OUTPUT_SCHEMA_VERSION


def render_json(command: str, payload: dict[str, Any], diagnostics: list[Diagnostic]) -> str:
    body: dict[str, Any] = {
        "output_schema_version": OUTPUT_SCHEMA_VERSION,
        "command": command,
        **payload,
        "diagnostics": [diagnostic.to_json() for diagnostic in diagnostics],
    }
    return json.dumps(body, indent=2, sort_keys=True)


def render_diagnostics(diagnostics: list[Diagnostic]) -> list[str]:
    return [diagnostic.render() for diagnostic in diagnostics]


def render_key_values(rows: list[tuple[str, object]]) -> list[str]:
    return [f"{key}: {value}" for key, value in rows]
