"""DeepScientist-flavored compatibility mocks for Isomer Labs."""

from __future__ import annotations

from isomer_labs.deepsci_ext.registry import (
    ARTIFACT_TOOLS,
    BASH_EXEC_TOOLS,
    MEMORY_TOOLS,
    SUPPORTED_TOOLS,
)
from isomer_labs.deepsci_ext.service import DeepSciCompatError, call_tool

__all__ = [
    "ARTIFACT_TOOLS",
    "BASH_EXEC_TOOLS",
    "DeepSciCompatError",
    "MEMORY_TOOLS",
    "SUPPORTED_TOOLS",
    "call_tool",
]
