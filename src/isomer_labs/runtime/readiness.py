"""Readiness diagnostics helpers for Workspace Runtime commands."""

from __future__ import annotations

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.doctor import DoctorCheck
from isomer_labs.models import EffectiveTopicContext


def _readiness_diagnostic(check: DoctorCheck, context: EffectiveTopicContext) -> Diagnostic:
    return Diagnostic(
        code="ISO043",
        severity="error",
        concept=check.concept,
        path=context.project.manifest_path,
        field=check.id,
        message=f"{check.summary} Use a Service Request for environment setup or compatibility repair.",
    )
