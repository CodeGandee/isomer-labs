"""Project operator system-extension declarations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

import tomlkit

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import Project
from isomer_labs.skills.installer import (
    CONCRETE_TARGETS,
    InstalledSystemSkill,
    SystemSkillInstallError,
    inspect_system_skills,
    resolve_system_skill_selection,
    resolve_targets,
)
from isomer_labs.skills.system_assets import iter_system_skill_extensions


PROJECT_LOCAL_SYSTEM_SKILL_TARGETS = ("claude-code", "kimi-code", "generic")


@dataclass(frozen=True)
class ProjectSystemExtension:
    extension_id: str
    group: str
    description: str
    declared_installed: bool
    installation_verified: bool = False

    def to_json(self) -> dict[str, object]:
        return {
            "extension_id": self.extension_id,
            "group": self.group,
            "description": self.description,
            "declared_installed": self.declared_installed,
            "installation_verified": self.installation_verified,
            "availability_basis": "project_manifest_user_declared" if self.declared_installed else "catalog_known_not_declared",
        }


@dataclass(frozen=True)
class ProjectSystemExtensionResult:
    ok: bool
    mutated: bool
    project_root: Path
    diagnostics: tuple[Diagnostic, ...]
    extensions: tuple[ProjectSystemExtension, ...]
    extension_id: str | None = None

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "ok": self.ok,
            "mutated": self.mutated,
            "project_root": str(self.project_root),
            "extensions": [extension.to_json() for extension in self.extensions],
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
            "installation_verification": "optional system extension installation is user-declared and not filesystem-verified",
        }
        if self.extension_id is not None:
            data["extension_id"] = self.extension_id
        return data


@dataclass(frozen=True)
class ProjectSystemExtensionObservation:
    """Read-only extension installation observation for one agent target."""

    target: str
    skill_root: Path
    extension_id: str
    declared_installed: bool
    status: str
    version_status: str | None
    installed_skills: tuple[str, ...]
    missing_skills: tuple[str, ...]
    incompatible_skills: tuple[str, ...]
    skill_observations: tuple[InstalledSystemSkill, ...]
    receipt_path: Path | None
    advice: str | None

    def to_json(self) -> dict[str, object]:
        return {
            "target": self.target,
            "skill_root": str(self.skill_root),
            "extension_id": self.extension_id,
            "declared_installed": self.declared_installed,
            "status": self.status,
            "version_status": self.version_status,
            "installed_skills": list(self.installed_skills),
            "missing_skills": list(self.missing_skills),
            "incompatible_skills": list(self.incompatible_skills),
            "skill_observations": [observation.to_json() for observation in self.skill_observations],
            "receipt_path": str(self.receipt_path) if self.receipt_path is not None else None,
            "advice": self.advice,
        }


@dataclass(frozen=True)
class ProjectSystemExtensionDetectionResult:
    """Target-specific, non-mutating Project extension detection result."""

    ok: bool
    project_root: Path
    targets: tuple[str, ...]
    observations: tuple[ProjectSystemExtensionObservation, ...]
    diagnostics: tuple[Diagnostic, ...]

    @property
    def mutated(self) -> bool:
        return False

    def to_json(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "mutated": False,
            "project_root": str(self.project_root),
            "targets": list(self.targets),
            "observations": [observation.to_json() for observation in self.observations],
            "diagnostics": [diagnostic.to_json() for diagnostic in self.diagnostics],
            "declaration_mutation": "none; detection is advisory",
        }


def list_project_system_extensions(project: Project) -> ProjectSystemExtensionResult:
    extensions = _project_extension_rows(project)
    return ProjectSystemExtensionResult(
        ok=True,
        mutated=False,
        project_root=project.root,
        diagnostics=(),
        extensions=extensions,
    )


def detect_project_system_extensions(
    project: Project,
    *,
    targets: Sequence[str] = (),
    env: Mapping[str, str] | None = None,
) -> ProjectSystemExtensionDetectionResult:
    """Inspect extension installations without changing declarations or skill roots."""

    return detect_project_extension_installations(
        project.root,
        declared_extensions=project.manifest.operator_system_extensions,
        targets=targets,
        env=env,
    )


def detect_project_extension_installations(
    project_root: Path,
    *,
    declared_extensions: Sequence[str] = (),
    targets: Sequence[str] = (),
    env: Mapping[str, str] | None = None,
) -> ProjectSystemExtensionDetectionResult:
    """Inspect deterministic target roots and return bounded extension advice."""

    selected_targets = tuple(dict.fromkeys(targets or PROJECT_LOCAL_SYSTEM_SKILL_TARGETS))
    diagnostics: list[Diagnostic] = []
    unknown_targets = [target for target in selected_targets if target not in CONCRETE_TARGETS]
    if unknown_targets:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Project operator system extension detection",
                field="targets",
                message=f"Unknown system-skill target: {unknown_targets[0]}.",
            )
        )
        return ProjectSystemExtensionDetectionResult(False, project_root, selected_targets, (), tuple(diagnostics))

    declared = set(declared_extensions)
    observations: list[ProjectSystemExtensionObservation] = []
    try:
        for target_name in selected_targets:
            target = _resolve_detection_target(project_root, target_name, env)
            for extension in iter_system_skill_extensions():
                selection = resolve_system_skill_selection(extensions=(extension.extension_id,), default_core=False)
                status = inspect_system_skills(target, selection)
                observation = _extension_observation(
                    extension.extension_id,
                    extension.extension_id in declared,
                    status.installed,
                    status.missing,
                    bool(status.invalid_projections),
                    status.manifest.path if status.manifest is not None else None,
                    target.target,
                    target.skill_root,
                )
                if observation.status != "not_detected" or observation.declared_installed:
                    observations.append(observation)
    except SystemSkillInstallError as exc:
        diagnostics.append(
            Diagnostic(
                code="ISO103",
                severity="error",
                concept="Project operator system extension detection",
                message=str(exc),
            )
        )
    return ProjectSystemExtensionDetectionResult(not diagnostics, project_root, selected_targets, tuple(observations), tuple(diagnostics))


def _resolve_detection_target(project_root: Path, target_name: str, env: Mapping[str, str] | None):
    return resolve_targets(target_name, cwd=project_root, env=env)[0]


def _extension_observation(
    extension_id: str,
    declared: bool,
    installed: tuple[InstalledSystemSkill, ...],
    missing: tuple[str, ...],
    has_invalid_projection: bool,
    receipt_path: Path | None,
    target: str,
    skill_root: Path,
) -> ProjectSystemExtensionObservation:
    statuses = {record.compatibility_status for record in installed}
    installed_names = tuple(record.name for record in installed)
    incompatible_statuses = {
        "malformed_version",
        "newer_than_cli",
        "obsolete_incompatible",
        "receipt_drift",
        "unversioned",
    }
    incompatible = tuple(record.name for record in installed if record.compatibility_status in incompatible_statuses)
    version_status: str | None = None
    if has_invalid_projection:
        status = "invalid_projection"
    elif missing and installed:
        status = "partial"
    elif missing:
        status = "missing" if declared else "not_detected"
    elif incompatible:
        status = next(
            name
            for name in ("receipt_drift", "malformed_version", "unversioned", "obsolete_incompatible", "newer_than_cli")
            if name in statuses
        )
    elif receipt_path is None or not all(record.installation_verified for record in installed):
        status = "unverified"
    else:
        version_status = "compatible_older" if "compatible_older" in statuses else "current"
        status = "ready" if declared else "detected_undeclared"
    advice = _extension_advice(extension_id, target, status)
    return ProjectSystemExtensionObservation(
        target=target,
        skill_root=skill_root,
        extension_id=extension_id,
        declared_installed=declared,
        status=status,
        version_status=version_status,
        installed_skills=installed_names,
        missing_skills=missing,
        incompatible_skills=incompatible,
        skill_observations=installed,
        receipt_path=receipt_path,
        advice=advice,
    )


def _extension_advice(extension_id: str, target: str, status: str) -> str | None:
    if status == "detected_undeclared":
        return f"isomer-cli project system-extensions remember {extension_id}"
    if status == "newer_than_cli":
        return "Upgrade isomer-cli before using this newer extension installation."
    if status in {
        "invalid_projection",
        "malformed_version",
        "missing",
        "obsolete_incompatible",
        "partial",
        "receipt_drift",
        "unverified",
        "unversioned",
    }:
        return f"isomer-cli system-skills install --target {target} --extension {extension_id} --force"
    return None


def remember_project_system_extension(project: Project, extension_id: str) -> ProjectSystemExtensionResult:
    diagnostics = _extension_id_diagnostics(extension_id)
    if diagnostics:
        return ProjectSystemExtensionResult(False, False, project.root, tuple(diagnostics), _project_extension_rows(project), extension_id)
    declared = list(project.manifest.operator_system_extensions)
    mutated = extension_id not in declared
    if mutated:
        declared.append(extension_id)
        _write_project_operator_system_extensions(project.manifest_path, sorted(declared))
    next_project = project
    extensions = _extension_rows(sorted(declared))
    return ProjectSystemExtensionResult(True, mutated, next_project.root, (), extensions, extension_id)


def forget_project_system_extension(project: Project, extension_id: str) -> ProjectSystemExtensionResult:
    declared = [item for item in project.manifest.operator_system_extensions if item != extension_id]
    mutated = len(declared) != len(project.manifest.operator_system_extensions)
    if mutated:
        _write_project_operator_system_extensions(project.manifest_path, declared)
    extensions = _extension_rows(declared)
    return ProjectSystemExtensionResult(True, mutated, project.root, (), extensions, extension_id)


def _project_extension_rows(project: Project) -> tuple[ProjectSystemExtension, ...]:
    return _extension_rows(project.manifest.operator_system_extensions)


def _extension_rows(declared: list[str]) -> tuple[ProjectSystemExtension, ...]:
    declared_ids = set(declared)
    return tuple(
        ProjectSystemExtension(
            extension_id=extension.extension_id,
            group=extension.group,
            description=extension.description,
            declared_installed=extension.extension_id in declared_ids,
        )
        for extension in iter_system_skill_extensions()
    )


def _extension_id_diagnostics(extension_id: str) -> list[Diagnostic]:
    known = {extension.extension_id for extension in iter_system_skill_extensions()}
    if extension_id in known:
        return []
    return [
        Diagnostic(
            code="ISO103",
            severity="error",
            concept="Project operator system extension",
            field="extension_id",
            message=f"Unknown packaged system extension: {extension_id}.",
        )
    ]


def _write_project_operator_system_extensions(manifest_path: Path, installed: list[str]) -> None:
    document = tomlkit.parse(manifest_path.read_text(encoding="utf-8"))
    operator = document.get("operator")
    if not isinstance(operator, dict):
        operator = tomlkit.table()
        document["operator"] = operator
    system_extensions = operator.get("system_extensions")
    if not isinstance(system_extensions, dict):
        system_extensions = tomlkit.table()
        operator["system_extensions"] = system_extensions
    installed_array = tomlkit.array()
    installed_array.multiline(False)
    for extension_id in installed:
        installed_array.append(extension_id)
    system_extensions["installed"] = installed_array
    manifest_path.write_text(tomlkit.dumps(document), encoding="utf-8")
