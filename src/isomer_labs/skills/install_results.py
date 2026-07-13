"""Result models for packaged system-skill operations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from isomer_labs.core.diagnostics import Diagnostic
    from isomer_labs.skills.installer import (
        ExistingSystemSkillPath,
        InstalledSystemSkill,
        InvalidSystemSkillProjection,
        SystemSkillSelection,
        SystemSkillTarget,
    )
    from isomer_labs.skills.receipts import ProjectionMode, SystemSkillRootManifest


@dataclass(frozen=True)
class SystemSkillStatusResult:
    """Status for one target skill root."""

    target: SystemSkillTarget
    installed: tuple[InstalledSystemSkill, ...]
    missing: tuple[str, ...]
    invalid_projections: tuple[InvalidSystemSkillProjection, ...]
    selection: SystemSkillSelection
    manifest: SystemSkillRootManifest | None
    diagnostics: tuple[Diagnostic, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "target": self.target.target,
            "skill_root": str(self.target.skill_root),
            "manifest": self.manifest.to_json() if self.manifest is not None else None,
            "installed": [record.to_json() for record in self.installed],
            "installed_skills": [record.name for record in self.installed],
            "missing_skills": list(self.missing),
            "invalid_projections": [projection.to_json() for projection in self.invalid_projections],
            "selection": self.selection.to_json(),
        }


@dataclass(frozen=True)
class SystemSkillInstallResult:
    """Install result for one target skill root."""

    target: SystemSkillTarget
    selection: SystemSkillSelection
    installed: tuple[InstalledSystemSkill, ...]
    preserved_existing: tuple[ExistingSystemSkillPath, ...]
    replaced: tuple[ExistingSystemSkillPath, ...]
    projection_mode: ProjectionMode
    manifest: SystemSkillRootManifest | None
    diagnostics: tuple[Diagnostic, ...]

    @property
    def ok(self) -> bool:
        return True

    @property
    def mutated(self) -> bool:
        return bool(self.installed or self.replaced)

    def to_json(self) -> dict[str, object]:
        return {
            "target": self.target.target,
            "skill_root": str(self.target.skill_root),
            "projection_mode": self.projection_mode,
            "manifest": self.manifest.to_json() if self.manifest is not None else None,
            "installed": [record.to_json() for record in self.installed],
            "installed_skills": [record.name for record in self.installed],
            "preserved_existing": [record.to_json() for record in self.preserved_existing],
            "replaced": [record.to_json() for record in self.replaced],
            "replaced_skills": [record.name for record in self.replaced],
            "selection": self.selection.to_json(),
        }


@dataclass(frozen=True)
class SystemSkillUninstallResult:
    """Uninstall result for one target skill root."""

    target: SystemSkillTarget
    removed: tuple[InstalledSystemSkill, ...]
    absent: tuple[str, ...]
    selection: SystemSkillSelection
    manifest: SystemSkillRootManifest | None
    diagnostics: tuple[Diagnostic, ...]

    @property
    def ok(self) -> bool:
        return True

    @property
    def mutated(self) -> bool:
        return bool(self.removed)

    def to_json(self) -> dict[str, object]:
        return {
            "target": self.target.target,
            "skill_root": str(self.target.skill_root),
            "manifest": self.manifest.to_json() if self.manifest is not None else None,
            "removed": [record.to_json() for record in self.removed],
            "removed_skills": [record.name for record in self.removed],
            "absent_skills": list(self.absent),
            "selection": self.selection.to_json(),
        }


@dataclass(frozen=True)
class SystemSkillUpgradeResult:
    """Upgrade result for one target skill root."""

    target: SystemSkillTarget
    selection: SystemSkillSelection
    refreshed: tuple[InstalledSystemSkill, ...]
    stale_removed: tuple[InstalledSystemSkill, ...]
    stale_absent: tuple[str, ...]
    projection_mode_override: ProjectionMode | None
    manifest: SystemSkillRootManifest | None
    diagnostics: tuple[Diagnostic, ...]

    @property
    def ok(self) -> bool:
        return True

    @property
    def mutated(self) -> bool:
        return bool(self.refreshed or self.stale_removed or self.stale_absent)

    def to_json(self) -> dict[str, object]:
        return {
            "target": self.target.target,
            "skill_root": str(self.target.skill_root),
            "projection_mode_override": self.projection_mode_override,
            "manifest": self.manifest.to_json() if self.manifest is not None else None,
            "refreshed": [record.to_json() for record in self.refreshed],
            "refreshed_skills": [record.name for record in self.refreshed],
            "stale_removed": [record.to_json() for record in self.stale_removed],
            "stale_removed_skills": [record.name for record in self.stale_removed],
            "stale_absent_skills": list(self.stale_absent),
            "selection": self.selection.to_json(),
        }
