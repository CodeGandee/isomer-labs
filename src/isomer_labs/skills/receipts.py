"""Versioned target-root receipts for installed Isomer system skills."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Literal

from packaging.version import InvalidVersion, Version

from isomer_labs.core.diagnostics import Diagnostic


SKILL_MANIFEST_FILENAME = "isomer-labs-skill-manifest.json"
SKILL_MANIFEST_SCHEMA = "isomer-labs-skill-manifest.v2"
LEGACY_SKILL_MANIFEST_SCHEMAS = ("isomer-labs-skill-manifest.v1",)
ProjectionMode = Literal["copy", "symlink"]


@dataclass(frozen=True)
class SystemSkillManifestRecord:
    """One skill record tracked in the target-root receipt."""

    name: str
    source_path: str
    projection_mode: ProjectionMode
    skill_version: str | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "source_path": self.source_path,
            "projection_mode": self.projection_mode,
            "skill_version": self.skill_version,
        }


@dataclass(frozen=True)
class SystemSkillRootManifest:
    """Target-root receipt for Isomer-managed system-skill projections."""

    schema_version: str
    target: str
    skill_root: Path
    package_name: str
    package_version: str | None
    installed_by: str
    updated_at: str
    skills: tuple[SystemSkillManifestRecord, ...]

    @property
    def path(self) -> Path:
        return self.skill_root / SKILL_MANIFEST_FILENAME

    def record_map(self) -> dict[str, SystemSkillManifestRecord]:
        return {record.name: record for record in self.skills}

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "target": self.target,
            "skill_root": str(self.skill_root),
            "package_name": self.package_name,
            "package_version": self.package_version,
            "installed_by": self.installed_by,
            "updated_at": self.updated_at,
            "skills": [record.to_json() for record in self.skills],
            "skill_names": [record.name for record in self.skills],
            "path": str(self.path),
        }


@dataclass(frozen=True)
class SystemSkillManifestInspection:
    """Read-only parse result for one Isomer target-root receipt."""

    status: Literal["absent", "current", "legacy", "unsupported_schema", "malformed_receipt"]
    path: Path
    manifest: SystemSkillRootManifest | None
    diagnostics: tuple[Diagnostic, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "status": self.status,
            "path": str(self.path),
            "schema_version": self.manifest.schema_version if self.manifest is not None else None,
            "legacy": self.status == "legacy",
            "manifest": self.manifest.to_json() if self.manifest is not None else None,
        }


def inspect_system_skill_receipt(skill_root: Path, target_name: str) -> SystemSkillManifestInspection:
    """Inspect the Isomer receipt in exactly one supplied system-skill root."""

    manifest_path = skill_root / SKILL_MANIFEST_FILENAME
    if not manifest_path.exists():
        return SystemSkillManifestInspection("absent", manifest_path, None, ())
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return _malformed(manifest_path, f"Cannot read Isomer skill manifest: {exc}")
    if not isinstance(raw, dict):
        return _malformed(manifest_path, "Isomer skill manifest must be a JSON object.")
    schema_version = raw.get("schema_version")
    if schema_version not in (SKILL_MANIFEST_SCHEMA, *LEGACY_SKILL_MANIFEST_SCHEMAS):
        diagnostics = (_manifest_diagnostic(manifest_path, "Unsupported Isomer skill manifest schema version."),)
        return SystemSkillManifestInspection("unsupported_schema", manifest_path, None, diagnostics)

    raw_skills = raw.get("skills", [])
    if not isinstance(raw_skills, list):
        return _malformed(manifest_path, "Isomer skill manifest `skills` field must be a list.")
    skills: list[SystemSkillManifestRecord] = []
    for index, item in enumerate(raw_skills):
        if not isinstance(item, dict):
            return _malformed(manifest_path, f"Isomer skill manifest skill record {index} must be an object.")
        name = item.get("name")
        source_path = item.get("source_path")
        projection_mode = item.get("projection_mode")
        skill_version = item.get("skill_version")
        if not isinstance(name, str) or not isinstance(source_path, str) or projection_mode not in {"copy", "symlink"}:
            return _malformed(manifest_path, f"Isomer skill manifest skill record {index} is invalid.")
        if schema_version == SKILL_MANIFEST_SCHEMA:
            if skill_version is not None and (not isinstance(skill_version, str) or not _is_pep440_version(skill_version)):
                return _malformed(
                    manifest_path,
                    f"Isomer skill manifest skill record {index} has an invalid skill_version.",
                )
        else:
            skill_version = None
        skills.append(
            SystemSkillManifestRecord(
                name=name,
                source_path=source_path,
                projection_mode=projection_mode,
                skill_version=skill_version if isinstance(skill_version, str) else None,
            )
        )

    manifest_target = raw.get("target")
    package_name = raw.get("package_name")
    package_version = raw.get("package_version")
    installed_by = raw.get("installed_by")
    updated_at = raw.get("updated_at")
    manifest = SystemSkillRootManifest(
        schema_version=str(schema_version),
        target=manifest_target if isinstance(manifest_target, str) else target_name,
        skill_root=skill_root,
        package_name=package_name if isinstance(package_name, str) else "isomer-labs",
        package_version=package_version if isinstance(package_version, str) else None,
        installed_by=installed_by if isinstance(installed_by, str) else "isomer-cli",
        updated_at=updated_at if isinstance(updated_at, str) else "",
        skills=tuple(skills),
    )
    status: Literal["current", "legacy"] = "current" if schema_version == SKILL_MANIFEST_SCHEMA else "legacy"
    return SystemSkillManifestInspection(status, manifest_path, manifest, ())


def _malformed(path: Path, message: str) -> SystemSkillManifestInspection:
    diagnostics = (_manifest_diagnostic(path, message),)
    return SystemSkillManifestInspection("malformed_receipt", path, None, diagnostics)


def _manifest_diagnostic(path: Path, message: str) -> Diagnostic:
    return Diagnostic(
        code="ISOSKILL001",
        severity="warning",
        concept="system-skill-manifest",
        path=path,
        message=message,
    )


def _is_pep440_version(value: str) -> bool:
    try:
        Version(value)
    except InvalidVersion:
        return False
    return True


__all__ = [
    "LEGACY_SKILL_MANIFEST_SCHEMAS",
    "ProjectionMode",
    "SKILL_MANIFEST_FILENAME",
    "SKILL_MANIFEST_SCHEMA",
    "SystemSkillManifestInspection",
    "SystemSkillManifestRecord",
    "SystemSkillRootManifest",
    "inspect_system_skill_receipt",
]
