"""Compatibility re-exports for CLI command handlers."""

# ruff: noqa: F403
from __future__ import annotations

from isomer_labs.cli.handlers.project import *
from isomer_labs.cli.handlers.runtime import *
from isomer_labs.cli.handlers.schemas import *
from isomer_labs.cli.handlers.self import *
from isomer_labs.cli.handlers.team_instances import *
from isomer_labs.cli.handlers.teams import *
from isomer_labs.cli.handlers.workspace import *
from isomer_labs.cli.handlers.workspace_paths import *

__all__ = [name for name in globals() if name.startswith("_cmd_")]
