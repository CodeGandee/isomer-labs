"""Project-facing callback insertion point discovery."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from isomer_labs.core.diagnostics import Diagnostic, has_errors
from isomer_labs.models import ProjectState
from isomer_labs.skills.system_assets import (
    CallbackInsertionPoint,
    SystemSkillAssetError,
    iter_system_skill_callback_insertion_points,
)


@dataclass(frozen=True)
class CallbackInsertionPointRecord:
    point: CallbackInsertionPoint
    availability_basis: str
    installation_verified: bool

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "id": f"{self.point.target_skill}/{self.point.stage}",
            "target_skill": self.point.target_skill,
            "skill_path": self.point.skill_path,
            "group": self.point.group,
            "group_kind": self.point.group_kind,
            "stage": self.point.stage,
            "stage_label": self.point.stage_label,
            "description": self.point.description,
            "availability_basis": self.availability_basis,
            "installation_verified": self.installation_verified,
        }
        if self.point.extension_id is not None:
            data["extension_id"] = self.point.extension_id
        return data


@dataclass(frozen=True)
class CallbackInsertionPointCommandResult:
    ok: bool
    project_root: Path
    insertion_points: tuple[CallbackInsertionPointRecord, ...]
    diagnostics: tuple[Diagnostic, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "mutated": False,
            "project_root": str(self.project_root),
            "insertion_points": [point.to_json() for point in self.insertion_points],
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
        }


def list_callback_insertion_points(
    state: ProjectState,
    *,
    extension_ids: tuple[str, ...],
    include_all_catalog_extensions: bool,
    core_only: bool,
    skill: str | None,
    stage: str | None,
) -> CallbackInsertionPointCommandResult:
    project = state.project
    diagnostics: list[Diagnostic] = []
    if core_only and (extension_ids or include_all_catalog_extensions):
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Callback insertion point",
                field="extensions",
                message="Use --core-only without --extension or --all-catalog-extensions.",
            )
        )
    selected_extensions = () if core_only or include_all_catalog_extensions else extension_ids or tuple(project.manifest.operator_system_extensions)
    try:
        points = iter_system_skill_callback_insertion_points(
            include_core=True,
            extension_ids=selected_extensions,
            include_all_extensions=include_all_catalog_extensions and not core_only,
            skill=skill,
            stage=stage,
        )
    except SystemSkillAssetError as exc:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Callback insertion point",
                field="extensions",
                message=str(exc),
            )
        )
        points = ()
    declared_extensions = set(project.manifest.operator_system_extensions)
    records = tuple(_callback_insertion_point_record(point, declared_extensions, include_all_catalog_extensions or bool(extension_ids)) for point in points)
    return CallbackInsertionPointCommandResult(
        ok=not has_errors(diagnostics),
        project_root=project.root,
        insertion_points=records,
        diagnostics=tuple(diagnostics),
    )


def _callback_insertion_point_record(
    point: CallbackInsertionPoint,
    declared_extensions: set[str],
    explicit_catalog_request: bool,
) -> CallbackInsertionPointRecord:
    if point.group_kind == "core":
        return CallbackInsertionPointRecord(point, "core_always_available", True)
    if point.extension_id in declared_extensions:
        return CallbackInsertionPointRecord(point, "project_manifest_user_declared", False)
    basis = "catalog_requested_not_verified" if explicit_catalog_request else "catalog_known_not_declared"
    return CallbackInsertionPointRecord(point, basis, False)
