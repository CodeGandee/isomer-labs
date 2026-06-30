"""Rendering and JSON input helpers for DeepScientist compatibility calls."""

from __future__ import annotations

import json
import sys
from typing import Any


def dumps_raw_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=2, sort_keys=True)


def load_input_json(value: str | None) -> dict[str, Any]:
    raw = ""
    if value == "-":
        raw = sys.stdin.read()
    elif value is not None:
        raw = value
    elif not sys.stdin.isatty():
        raw = sys.stdin.read()
    if not raw.strip():
        return {}
    loaded = json.loads(raw)
    if not isinstance(loaded, dict):
        raise ValueError("DeepScientist compatibility input JSON must be an object.")
    return loaded


def unsupported_tool_payload(tool_name: str) -> dict[str, Any]:
    return {
        "ok": False,
        "tool_name": tool_name,
        "error": {
            "code": "unsupported_tool",
            "message": f"Unsupported DeepScientist compatibility tool: {tool_name}",
            "tool_name": tool_name,
        },
    }
