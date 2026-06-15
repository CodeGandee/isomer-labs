"""Common command-output envelope (see commands.toml [envelope])."""
from __future__ import annotations
import json
import sys


def envelope(command, *, ok=True, quest_id=None, plan_revision=None, data=None,
             diagnostics=None, warnings=None):
    return {
        "ok": bool(ok),
        "command": command,
        "quest_id": quest_id,
        "plan_revision": plan_revision,
        "data": data if data is not None else {},
        "diagnostics": diagnostics or [],
        "warnings": warnings or [],
    }


def emit(env: dict) -> None:
    json.dump(env, sys.stdout, indent=2, default=str)
    sys.stdout.write("\n")


def fail(command, message, **kw):
    env = envelope(command, ok=False, diagnostics=[message], **kw)
    emit(env)
    return env
