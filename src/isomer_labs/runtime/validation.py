"""Workspace Runtime inspection and validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from isomer_labs.diagnostics import Diagnostic, has_errors
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.paths import preview_paths
from isomer_labs.runtime.store import open_workspace_runtime
from isomer_labs.runtime.validation_checks import (
    _validate_adapter_records,
    _validate_agent_team_instances,
    _validate_handoffs,
    _validate_lifecycle_records,
    _validate_lifecycle_transitions,
    _validate_metadata,
    _validate_path_plans,
    _validate_readiness,
)


@dataclass(frozen=True)
class RuntimeInspection:
    exists: bool
    runtime_path: Path | None
    metadata: dict[str, object] | None
    counts: dict[str, int]
    latest_readiness: dict[str, object] | None
    agent_team_instances: list[dict[str, object]]

    def to_json(self) -> dict[str, object]:
        return {
            "exists": self.exists,
            "runtime_path": str(self.runtime_path) if self.runtime_path is not None else None,
            "metadata": self.metadata,
            "counts": self.counts,
            "latest_readiness": self.latest_readiness,
            "agent_team_instances": self.agent_team_instances,
        }


def inspect_workspace_runtime(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
) -> tuple[RuntimeInspection, list[Diagnostic]]:
    entries, diagnostics = preview_paths(context, env=env)
    runtime_path = None
    if not has_errors(diagnostics):
        runtime_path = next(entry.path for entry in entries if entry.surface == "workspace_runtime_db")
    store, open_diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    diagnostics.extend(open_diagnostics)
    if store is None:
        return RuntimeInspection(False, runtime_path, None, {}, None, []), diagnostics
    latest_readiness = store.latest_readiness()
    inspection = RuntimeInspection(
        exists=True,
        runtime_path=store.db_path,
        metadata=store.metadata().to_json(),
        counts=store.count_records(),
        latest_readiness=latest_readiness.to_json() if latest_readiness is not None else None,
        agent_team_instances=[
            record.to_json() for record in store.list_agent_team_instances()
        ],
    )
    store.close()
    return inspection, diagnostics


def validate_workspace_runtime(
    context: EffectiveTopicContext,
    *,
    env: Mapping[str, str],
    require_ready_readiness: bool = False,
) -> tuple[RuntimeInspection, list[Diagnostic]]:
    inspection, diagnostics = inspect_workspace_runtime(context, env=env)
    if not inspection.exists:
        return inspection, diagnostics

    store, open_diagnostics = open_workspace_runtime(context, env=env, read_only=True)
    diagnostics.extend(open_diagnostics)
    if store is None:
        return inspection, diagnostics

    diagnostics.extend(_validate_metadata(context, store))
    diagnostics.extend(_validate_path_plans(context, store, env))
    diagnostics.extend(_validate_readiness(context, store, require_ready=require_ready_readiness))
    diagnostics.extend(_validate_lifecycle_records(context, store))
    diagnostics.extend(_validate_agent_team_instances(context, store))
    diagnostics.extend(_validate_adapter_records(context, store))
    diagnostics.extend(_validate_handoffs(context, store))
    diagnostics.extend(_validate_lifecycle_transitions(store))
    store.close()
    return inspection, diagnostics
