"""Semantic file locator helpers for project-local runtime files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from isomer_labs.path_utils import canonicalize, is_within
from isomer_labs.runtime.models import (
    AdapterManifestRefRecord,
    AdapterPayloadRefRecord,
    PathPlanRecord,
    RuntimeLifecycleRecord,
)


@dataclass(frozen=True)
class SemanticFileLocator:
    record_kind: str
    record_id: str
    path_field: str
    semantic_label: str
    resolved_path: Path
    relative_path: str
    surface_path: Path
    path_plan_id: str | None = None
    scope_ref: str | None = None
    storage_profile: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "record_kind": self.record_kind,
            "record_id": self.record_id,
            "path_field": self.path_field,
            "semantic_label": self.semantic_label,
            "resolved_path": str(self.resolved_path),
            "relative_path": self.relative_path,
            "surface_path": str(self.surface_path),
        }
        if self.path_plan_id is not None:
            data["path_plan_id"] = self.path_plan_id
        if self.scope_ref is not None:
            data["scope_ref"] = self.scope_ref
        if self.storage_profile is not None:
            data["storage_profile"] = self.storage_profile
        return data


def locate_semantic_file(
    path: Path,
    path_plans: Iterable[PathPlanRecord],
    *,
    record_kind: str,
    record_id: str,
    path_field: str,
) -> SemanticFileLocator | None:
    resolved_path = canonicalize(path)
    candidates: list[tuple[int, PathPlanRecord, Path]] = []
    for plan in path_plans:
        if plan.semantic_label is None:
            continue
        surface_path = canonicalize(Path(plan.path))
        if resolved_path == surface_path or is_within(resolved_path, surface_path):
            candidates.append((len(surface_path.parts), plan, surface_path))
    if not candidates:
        return None
    _, plan, surface_path = sorted(candidates, key=lambda item: item[0], reverse=True)[0]
    semantic_label = plan.semantic_label
    if semantic_label is None:
        return None
    try:
        relative_path = resolved_path.relative_to(surface_path)
    except ValueError:
        return None
    relative_text = "." if str(relative_path) == "." else relative_path.as_posix()
    return SemanticFileLocator(
        record_kind=record_kind,
        record_id=record_id,
        path_field=path_field,
        semantic_label=semantic_label,
        resolved_path=resolved_path,
        relative_path=relative_text,
        surface_path=surface_path,
        path_plan_id=plan.id,
        scope_ref=plan.scope_ref,
        storage_profile=plan.storage_profile,
    )


def runtime_semantic_file_locators(
    *,
    path_plans: Iterable[PathPlanRecord],
    lifecycle_records: Iterable[RuntimeLifecycleRecord],
    adapter_manifest_refs: Iterable[AdapterManifestRefRecord],
    adapter_payload_refs: Iterable[AdapterPayloadRefRecord],
) -> list[SemanticFileLocator]:
    plans = list(path_plans)
    locators: list[SemanticFileLocator] = []
    for lifecycle_record in lifecycle_records:
        if lifecycle_record.content_path is None:
            continue
        locator = locate_semantic_file(
            Path(lifecycle_record.content_path),
            plans,
            record_kind=lifecycle_record.record_kind,
            record_id=lifecycle_record.id,
            path_field="content_path",
        )
        if locator is not None:
            locators.append(locator)
    for manifest_ref in adapter_manifest_refs:
        locator = locate_semantic_file(
            Path(manifest_ref.manifest_path),
            plans,
            record_kind="adapter_manifest_ref",
            record_id=manifest_ref.id,
            path_field="manifest_path",
        )
        if locator is not None:
            locators.append(locator)
    for payload_ref in adapter_payload_refs:
        locator = locate_semantic_file(
            Path(payload_ref.payload_path),
            plans,
            record_kind="adapter_payload_ref",
            record_id=payload_ref.id,
            path_field="payload_path",
        )
        if locator is not None:
            locators.append(locator)
    return locators
