"""JSON serialization helpers for Workspace Runtime persistence."""

from __future__ import annotations

import json


def _dumps(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _loads_dict(value: str) -> dict[str, str]:
    loaded = json.loads(value)
    if not isinstance(loaded, dict):
        return {}
    return {str(key): str(item) for key, item in loaded.items() if isinstance(item, str)}


def _loads_object_dict(value: str) -> dict[str, object]:
    loaded = json.loads(value)
    if not isinstance(loaded, dict):
        return {}
    return {str(key): item for key, item in loaded.items()}


def _loads_json_list(value: str) -> list[dict[str, object]]:
    loaded = json.loads(value)
    if not isinstance(loaded, list):
        return []
    return [item for item in loaded if isinstance(item, dict)]


def _loads_list(value: str) -> list[str]:
    loaded = json.loads(value)
    if not isinstance(loaded, list):
        return []
    return [str(item) for item in loaded if isinstance(item, str)]
