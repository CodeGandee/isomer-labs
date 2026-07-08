"""User Skill Callback key validation helpers."""

from __future__ import annotations

import re


CALLBACK_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
CALLBACK_TOOLBOX_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
CALLBACK_TOOLBOX_KEY_RE = re.compile(r"^[A-Za-z0-9_/-]+$")


def valid_callback_id(callback_id: str) -> bool:
    parts = callback_id.split(":")
    if len(parts) == 1:
        return bool(CALLBACK_ID_RE.match(callback_id))
    if len(parts) != 2:
        return False
    toolbox_id, toolbox_key = parts
    return bool(CALLBACK_TOOLBOX_ID_RE.match(toolbox_id) and CALLBACK_TOOLBOX_KEY_RE.match(toolbox_key))
