"""DeepScientist-flavored compatibility mocks for Isomer Labs."""

from __future__ import annotations

from isomer_labs.deepsci_ext.tools import (
    ARTIFACT_TOOLS,
    BASH_EXEC_TOOLS,
    DeepSciCompatError,
    MEMORY_TOOLS,
    SUPPORTED_TOOLS,
    call_tool,
)
from isomer_labs.deepsci_ext.record_formats import (
    DeepScientistRecordFormatProvider,
    active_profile_names,
    canonical_record_format_ref,
    register_deepsci_record_format_provider,
)
__all__ = [
    "ARTIFACT_TOOLS",
    "BASH_EXEC_TOOLS",
    "DeepSciCompatError",
    "DeepScientistRecordFormatProvider",
    "MEMORY_TOOLS",
    "SUPPORTED_TOOLS",
    "active_profile_names",
    "call_tool",
    "canonical_record_format_ref",
    "register_deepsci_record_format_provider",
]
