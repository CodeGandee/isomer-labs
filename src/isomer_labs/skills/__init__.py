"""Packaged Isomer skill assets."""

from __future__ import annotations

from isomer_labs.skills.system_assets import (
    SystemSkillAssetError,
    SystemSkillGroup,
    SystemSkillMaterializationResult,
    iter_system_skill_groups,
    iter_system_skill_paths,
    load_system_skill_manifest,
    materialize_system_skills,
    resolve_system_skill,
    system_skills_root,
)
from isomer_labs.skills.installer import (
    CONCRETE_TARGETS,
    SKILL_MANIFEST_FILENAME,
    SUPPORTED_TARGETS,
    SystemSkillInstallError,
    inspect_system_skills,
    install_system_skills,
    list_packaged_system_skills,
    resolve_system_skill_selection,
    resolve_targets,
    uninstall_system_skills,
    upgrade_system_skills,
)

__all__ = [
    "CONCRETE_TARGETS",
    "SKILL_MANIFEST_FILENAME",
    "SUPPORTED_TARGETS",
    "SystemSkillAssetError",
    "SystemSkillGroup",
    "SystemSkillInstallError",
    "SystemSkillMaterializationResult",
    "inspect_system_skills",
    "install_system_skills",
    "iter_system_skill_groups",
    "iter_system_skill_paths",
    "list_packaged_system_skills",
    "load_system_skill_manifest",
    "materialize_system_skills",
    "resolve_system_skill_selection",
    "resolve_system_skill",
    "resolve_targets",
    "system_skills_root",
    "uninstall_system_skills",
    "upgrade_system_skills",
]
