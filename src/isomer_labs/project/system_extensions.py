"""Project operator system-extension declarations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import tomlkit

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.models import Project
from isomer_labs.skills.system_assets import iter_system_skill_extensions


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


def list_project_system_extensions(project: Project) -> ProjectSystemExtensionResult:
    extensions = _project_extension_rows(project)
    return ProjectSystemExtensionResult(
        ok=True,
        mutated=False,
        project_root=project.root,
        diagnostics=(),
        extensions=extensions,
    )


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
