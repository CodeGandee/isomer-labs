"""Versioned target-root receipts for installed Isomer system skills."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from pathlib import PurePosixPath
from typing import Literal

from packaging.version import InvalidVersion, Version

from isomer_labs.core.diagnostics import Diagnostic


SKILL_MANIFEST_FILENAME = "isomer-labs-skill-manifest.json"
SKILL_MANIFEST_SCHEMA = "isomer-labs-skill-manifest.v5"
LEGACY_SKILL_MANIFEST_SCHEMAS = (
    "isomer-labs-skill-manifest.v1",
    "isomer-labs-skill-manifest.v2",
    "isomer-labs-skill-manifest.v3",
    "isomer-labs-skill-manifest.v4",
)
ProjectionMode = Literal["copy", "symlink"]
SystemSkillScope = Literal["user", "project"]


@dataclass(frozen=True, order=True)
class SystemSkillManifestBinding:
    """One target and scope that resolves to a receipt-owned skill root."""

    target: str
    scope: SystemSkillScope

    def to_json(self) -> dict[str, str]:
        return {"target": self.target, "scope": self.scope}


@dataclass(frozen=True)
class SystemSkillManifestMemberRecord:
    """One protected member expected inside a receipt-owned public pack."""

    logical_id: str
    relative_path: str
    invocation_designator: str
    skill_version: str

    def to_json(self) -> dict[str, str]:
        return {
            "logical_id": self.logical_id,
            "relative_path": self.relative_path,
            "invocation_designator": self.invocation_designator,
            "skill_version": self.skill_version,
        }


@dataclass(frozen=True)
class SystemSkillManifestPublicRecord:
    """One receipt-owned public welcome or entrypoint projection."""

    name: str
    role: str
    source_path: str
    projection_mode: ProjectionMode
    skill_version: str

    def to_json(self) -> dict[str, str]:
        return {
            "name": self.name,
            "role": self.role,
            "source_path": self.source_path,
            "projection_mode": self.projection_mode,
            "skill_version": self.skill_version,
        }


@dataclass(frozen=True)
class SystemSkillManifestRecord:
    """One complete pack receipt, or one read-only legacy flat record."""

    name: str
    source_path: str
    projection_mode: ProjectionMode
    skill_version: str | None = None
    pack_id: str | None = None
    entry_skill: str | None = None
    package_version: str | None = None
    public_skills: tuple[SystemSkillManifestPublicRecord, ...] = ()
    protected_members: tuple[SystemSkillManifestMemberRecord, ...] = ()

    def to_json(self) -> dict[str, object]:
        data: dict[str, object] = {
            "name": self.name,
            "source_path": self.source_path,
            "projection_mode": self.projection_mode,
            "skill_version": self.skill_version,
        }
        if self.pack_id is not None:
            data.update(
                {
                    "pack_id": self.pack_id,
                    "entry_skill": self.entry_skill or self.name,
                    "package_version": self.package_version,
                    "public_skills": [skill.to_json() for skill in self.public_skills],
                    "protected_members": [member.to_json() for member in self.protected_members],
                }
            )
        return data


@dataclass(frozen=True)
class SystemSkillLegacyPathRecord:
    """One obsolete receipt-tracked top-level path retained for bounded cleanup."""

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
    skill_root: Path
    package_name: str
    package_version: str | None
    installed_by: str
    updated_at: str
    skills: tuple[SystemSkillManifestRecord, ...]
    bindings: tuple[SystemSkillManifestBinding, ...] = ()
    legacy_paths: tuple[SystemSkillLegacyPathRecord, ...] = ()
    legacy_target: str | None = None

    @property
    def target(self) -> str | None:
        """Return the legacy or unambiguous target label for compatibility output."""

        if self.legacy_target is not None:
            return self.legacy_target
        if len(self.bindings) == 1:
            return self.bindings[0].target
        if self.bindings:
            return "all"
        return None

    @property
    def path(self) -> Path:
        return self.skill_root / SKILL_MANIFEST_FILENAME

    def record_map(self) -> dict[str, SystemSkillManifestRecord]:
        return {record.name: record for record in self.skills}

    def pack_map(self) -> dict[str, SystemSkillManifestRecord]:
        """Return current or legacy pack records keyed by stable pack id when available."""

        return {record.pack_id or record.name: record for record in self.skills}

    def public_ownership_map(self) -> dict[str, tuple[SystemSkillManifestRecord, SystemSkillManifestPublicRecord]]:
        """Return v5 public projections keyed by canonical public name."""

        return {
            public.name: (record, public)
            for record in self.skills
            for public in record.public_skills
        }

    def to_json(self) -> dict[str, object]:
        return {
            "schema_version": self.schema_version,
            "target": self.target,
            "bindings": [binding.to_json() for binding in self.bindings],
            "skill_root": str(self.skill_root),
            "package_name": self.package_name,
            "package_version": self.package_version,
            "installed_by": self.installed_by,
            "updated_at": self.updated_at,
            "skills": [record.to_json() for record in self.skills],
            "skill_names": [record.name for record in self.skills],
            "legacy_paths": [record.to_json() for record in self.legacy_paths],
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
        if schema_version != "isomer-labs-skill-manifest.v1":
            if skill_version is not None and (not isinstance(skill_version, str) or not _is_pep440_version(skill_version)):
                return _malformed(
                    manifest_path,
                    f"Isomer skill manifest skill record {index} has an invalid skill_version.",
                )
        if schema_version == "isomer-labs-skill-manifest.v1":
            skill_version = None
        pack_id: str | None = None
        entry_skill: str | None = None
        record_package_version: str | None = None
        public_skills: list[SystemSkillManifestPublicRecord] = []
        protected_members: list[SystemSkillManifestMemberRecord] = []
        if schema_version == SKILL_MANIFEST_SCHEMA:
            pack_id = item.get("pack_id") if isinstance(item.get("pack_id"), str) else None
            entry_skill = item.get("entry_skill") if isinstance(item.get("entry_skill"), str) else None
            record_package_version = item.get("package_version") if isinstance(item.get("package_version"), str) else None
            raw_public_skills = item.get("public_skills")
            raw_members = item.get("protected_members")
            if (
                pack_id is None
                or not pack_id
                or entry_skill is None
                or not entry_skill
                or not isinstance(raw_public_skills, list)
                or not isinstance(raw_members, list)
            ):
                return _malformed(manifest_path, f"Isomer skill manifest pack record {index} is invalid.")
            for public_index, raw_public in enumerate(raw_public_skills):
                public = _parse_public_record(raw_public)
                if public is None:
                    return _malformed(
                        manifest_path,
                        f"Isomer skill manifest pack record {index} public skill {public_index} is invalid.",
                    )
                public_skills.append(public)
            if len(public_skills) != 2 or {public.role for public in public_skills} != {"welcome", "entrypoint"}:
                return _malformed(
                    manifest_path,
                    f"Isomer skill manifest pack record {index} must contain one welcome and one entrypoint.",
                )
            if len({public.name for public in public_skills}) != len(public_skills):
                return _malformed(manifest_path, f"Isomer skill manifest pack record {index} has duplicate public names.")
            entrypoints = [public for public in public_skills if public.role == "entrypoint"]
            if entrypoints[0].name != entry_skill or name != entry_skill:
                return _malformed(manifest_path, f"Isomer skill manifest pack record {index} entrypoint is inconsistent.")
            for member_index, raw_member in enumerate(raw_members):
                member = _parse_member_record(raw_member)
                if member is None:
                    return _malformed(
                        manifest_path,
                        f"Isomer skill manifest pack record {index} protected member {member_index} is invalid.",
                    )
                protected_members.append(member)
            if len({member.logical_id for member in protected_members}) != len(protected_members):
                return _malformed(manifest_path, f"Isomer skill manifest pack record {index} has duplicate logical ids.")
            if len({member.relative_path for member in protected_members}) != len(protected_members):
                return _malformed(manifest_path, f"Isomer skill manifest pack record {index} has duplicate member paths.")
        skills.append(
            SystemSkillManifestRecord(
                name=name,
                source_path=source_path,
                projection_mode=projection_mode,
                skill_version=skill_version if isinstance(skill_version, str) else None,
                pack_id=pack_id,
                entry_skill=entry_skill,
                package_version=record_package_version,
                public_skills=tuple(public_skills),
                protected_members=tuple(protected_members),
            )
        )
    if len({record.name for record in skills}) != len(skills):
        return _malformed(manifest_path, "Isomer skill manifest pack or skill names must be unique.")

    bindings: list[SystemSkillManifestBinding] = []
    manifest_target = raw.get("target")
    if schema_version in {
        SKILL_MANIFEST_SCHEMA,
        "isomer-labs-skill-manifest.v3",
        "isomer-labs-skill-manifest.v4",
    }:
        raw_bindings = raw.get("bindings")
        if not isinstance(raw_bindings, list) or not raw_bindings:
            return _malformed(manifest_path, "Isomer skill manifest `bindings` field must be a non-empty list.")
        for index, item in enumerate(raw_bindings):
            if not isinstance(item, dict):
                return _malformed(manifest_path, f"Isomer skill manifest binding {index} must be an object.")
            binding_target = item.get("target")
            binding_scope = item.get("scope")
            if not isinstance(binding_target, str) or not binding_target or binding_scope not in {"user", "project"}:
                return _malformed(manifest_path, f"Isomer skill manifest binding {index} is invalid.")
            bindings.append(SystemSkillManifestBinding(target=binding_target, scope=binding_scope))
        if len(set(bindings)) != len(bindings):
            return _malformed(manifest_path, "Isomer skill manifest bindings must be unique.")

    legacy_paths: list[SystemSkillLegacyPathRecord] = []
    if schema_version == SKILL_MANIFEST_SCHEMA:
        raw_legacy_paths = raw.get("legacy_paths", [])
        if not isinstance(raw_legacy_paths, list):
            return _malformed(manifest_path, "Isomer skill manifest `legacy_paths` field must be a list.")
        for index, item in enumerate(raw_legacy_paths):
            legacy = _parse_legacy_path_record(item)
            if legacy is None:
                return _malformed(manifest_path, f"Isomer skill manifest legacy path record {index} is invalid.")
            legacy_paths.append(legacy)
        if len({record.name for record in legacy_paths}) != len(legacy_paths):
            return _malformed(manifest_path, "Isomer skill manifest legacy path names must be unique.")
        if {record.name for record in skills} & {record.name for record in legacy_paths}:
            return _malformed(manifest_path, "Current pack and legacy path names must not overlap.")

    package_name = raw.get("package_name")
    package_version = raw.get("package_version")
    installed_by = raw.get("installed_by")
    updated_at = raw.get("updated_at")
    manifest = SystemSkillRootManifest(
        schema_version=str(schema_version),
        skill_root=skill_root,
        package_name=package_name if isinstance(package_name, str) else "isomer-labs",
        package_version=package_version if isinstance(package_version, str) else None,
        installed_by=installed_by if isinstance(installed_by, str) else "isomer-cli",
        updated_at=updated_at if isinstance(updated_at, str) else "",
        skills=tuple(skills),
        bindings=tuple(sorted(bindings)),
        legacy_paths=tuple(legacy_paths),
        legacy_target=(manifest_target if isinstance(manifest_target, str) else target_name)
        if schema_version in {"isomer-labs-skill-manifest.v1", "isomer-labs-skill-manifest.v2"}
        else None,
    )
    status: Literal["current", "legacy"] = "current" if schema_version == SKILL_MANIFEST_SCHEMA else "legacy"
    return SystemSkillManifestInspection(status, manifest_path, manifest, ())


def _parse_member_record(value: object) -> SystemSkillManifestMemberRecord | None:
    if not isinstance(value, dict):
        return None
    logical_id = value.get("logical_id")
    relative_path = value.get("relative_path")
    invocation_designator = value.get("invocation_designator")
    skill_version = value.get("skill_version")
    if (
        not isinstance(logical_id, str)
        or not logical_id
        or not isinstance(relative_path, str)
        or not _is_safe_relative_path(relative_path)
        or not relative_path.startswith("subskills/")
        or not isinstance(invocation_designator, str)
        or not invocation_designator
        or not isinstance(skill_version, str)
        or not _is_pep440_version(skill_version)
    ):
        return None
    return SystemSkillManifestMemberRecord(logical_id, relative_path, invocation_designator, skill_version)


def _parse_public_record(value: object) -> SystemSkillManifestPublicRecord | None:
    if not isinstance(value, dict):
        return None
    name = value.get("name")
    role = value.get("role")
    source_path = value.get("source_path")
    projection_mode = value.get("projection_mode")
    skill_version = value.get("skill_version")
    if (
        not isinstance(name, str)
        or not name
        or role not in {"welcome", "entrypoint"}
        or not isinstance(source_path, str)
        or not _is_safe_relative_path(source_path)
        or projection_mode not in {"copy", "symlink"}
        or not isinstance(skill_version, str)
        or not _is_pep440_version(skill_version)
    ):
        return None
    return SystemSkillManifestPublicRecord(
        name=name,
        role=role,
        source_path=source_path,
        projection_mode=projection_mode,
        skill_version=skill_version,
    )


def _parse_legacy_path_record(value: object) -> SystemSkillLegacyPathRecord | None:
    if not isinstance(value, dict):
        return None
    name = value.get("name")
    source_path = value.get("source_path")
    projection_mode = value.get("projection_mode")
    skill_version = value.get("skill_version")
    if (
        not isinstance(name, str)
        or not name
        or not isinstance(source_path, str)
        or projection_mode not in {"copy", "symlink"}
        or (skill_version is not None and (not isinstance(skill_version, str) or not _is_pep440_version(skill_version)))
    ):
        return None
    return SystemSkillLegacyPathRecord(
        name=name,
        source_path=source_path,
        projection_mode=projection_mode,
        skill_version=skill_version if isinstance(skill_version, str) else None,
    )


def _is_safe_relative_path(value: str) -> bool:
    path = PurePosixPath(value)
    return bool(value) and not path.is_absolute() and all(part not in {"", ".", ".."} for part in path.parts)


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
    "SystemSkillLegacyPathRecord",
    "SystemSkillManifestMemberRecord",
    "SystemSkillManifestPublicRecord",
    "SystemSkillManifestRecord",
    "SystemSkillRootManifest",
    "inspect_system_skill_receipt",
]
