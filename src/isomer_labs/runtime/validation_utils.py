"""Shared helpers for Workspace Runtime validation."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import EffectiveTopicContext


def owner_diagnostics(
    context: EffectiveTopicContext,
    path: Path,
    record_id: str,
    research_topic_id: str,
    topic_workspace_id: str,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    if research_topic_id != context.research_topic.id:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Workspace Runtime record",
                path=path,
                field=record_id,
                message="Runtime record references another Research Topic.",
            )
        )
    if topic_workspace_id != context.topic_workspace_id:
        diagnostics.append(
            Diagnostic(
                code="ISO041",
                severity="error",
                concept="Workspace Runtime record",
                path=path,
                field=record_id,
                message="Runtime record references another Topic Workspace.",
            )
        )
    return diagnostics


def missing_ref_diagnostics(
    path: Path,
    concept: str,
    record_id: str,
    ref_kind: str,
    refs: list[str],
    known: Mapping[str, object],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for ref in refs:
        if ref not in known:
            diagnostics.append(
                Diagnostic(
                    code="ISO041",
                    severity="error",
                    concept=concept,
                    path=path,
                    field=record_id,
                    message=f"Record points to a missing adapter {ref_kind} ref: {ref}.",
                )
            )
    return diagnostics
