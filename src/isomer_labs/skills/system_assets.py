"""Package-resource helpers for official Isomer system skills."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path, PurePosixPath
from typing import Any, Sequence

import tomlkit


SYSTEM_SKILLS_RESOURCE = "assets/system_skills"


class SystemSkillAssetError(ValueError):
    """Raised when packaged system-skill assets are invalid or unavailable."""


@dataclass(frozen=True)
class SystemSkillGroup:
    """Manifest-defined system-skill group."""

    name: str
    description: str
    skills: tuple[str, ...]


@dataclass(frozen=True)
class SystemSkillMaterializationResult:
    """Result from copying packaged system skills to a target directory."""

    target: Path
    groups: tuple[str, ...]
    copied_paths: tuple[Path, ...]


def system_skills_root() -> Traversable:
    """Return the package resource root for official system skills."""

    root = resources.files("isomer_labs").joinpath(SYSTEM_SKILLS_RESOURCE)
    if not root.is_dir():
        raise SystemSkillAssetError(f"Packaged system-skill root is missing: {SYSTEM_SKILLS_RESOURCE}")
    return root


def load_system_skill_manifest() -> dict[str, Any]:
    """Load the packaged system-skill manifest."""

    manifest = system_skills_root().joinpath("manifest.toml")
    if not manifest.is_file():
        raise SystemSkillAssetError("Packaged system-skill manifest is missing.")
    parsed = tomlkit.parse(manifest.read_text(encoding="utf-8"))
    return dict(parsed)


def iter_system_skill_groups() -> tuple[SystemSkillGroup, ...]:
    """Return manifest-defined system-skill groups."""

    manifest = load_system_skill_manifest()
    groups = manifest.get("groups")
    if not isinstance(groups, dict):
        raise SystemSkillAssetError("Packaged system-skill manifest must define [groups].")
    parsed_groups: list[SystemSkillGroup] = []
    for name, value in groups.items():
        if not isinstance(value, dict):
            raise SystemSkillAssetError(f"System-skill group {name!r} must be a table.")
        description = value.get("description", "")
        skills = value.get("skills")
        if not isinstance(skills, list) or not all(isinstance(item, str) for item in skills):
            raise SystemSkillAssetError(f"System-skill group {name!r} must define a string skills list.")
        parsed_groups.append(
            SystemSkillGroup(
                name=str(name),
                description=str(description),
                skills=tuple(_normalize_relative_path(item) for item in skills),
            )
        )
    return tuple(parsed_groups)


def iter_system_skill_paths(groups: Sequence[str] | None = None) -> tuple[str, ...]:
    """Return manifest-relative skill paths for selected groups."""

    selected = _selected_groups(groups)
    seen: set[str] = set()
    paths: list[str] = []
    for group in selected:
        for skill_path in group.skills:
            if skill_path not in seen:
                resolve_system_skill(skill_path)
                seen.add(skill_path)
                paths.append(skill_path)
    return tuple(paths)


def resolve_system_skill(skill_path: str) -> Traversable:
    """Resolve one manifest-relative system-skill path below the packaged root."""

    normalized = _normalize_relative_path(skill_path)
    target = _join_resource(system_skills_root(), normalized)
    if not target.is_dir():
        raise SystemSkillAssetError(f"Packaged system skill is missing: {normalized}")
    skill_md = target.joinpath("SKILL.md")
    if not skill_md.is_file():
        raise SystemSkillAssetError(f"Packaged system skill is missing SKILL.md: {normalized}")
    return target


def materialize_system_skills(
    target: Path,
    *,
    groups: Sequence[str] | None = None,
) -> SystemSkillMaterializationResult:
    """Copy selected packaged system skills to an empty or new filesystem target."""

    selected_groups = _selected_groups(groups)
    selected_names = tuple(group.name for group in selected_groups)
    target = target.expanduser().resolve(strict=False)
    _ensure_empty_or_new_directory(target)
    root = system_skills_root()
    copied_paths: list[Path] = []
    copied_paths.append(_copy_resource_file(root.joinpath("manifest.toml"), target / "manifest.toml"))
    for skill_path in iter_system_skill_paths(selected_names):
        destination = target / Path(skill_path)
        _copy_resource_tree(resolve_system_skill(skill_path), destination, copied_paths)
    return SystemSkillMaterializationResult(
        target=target,
        groups=selected_names,
        copied_paths=tuple(copied_paths),
    )


def _selected_groups(groups: Sequence[str] | None) -> tuple[SystemSkillGroup, ...]:
    available = {group.name: group for group in iter_system_skill_groups()}
    if groups is None:
        return tuple(available.values())
    selected: list[SystemSkillGroup] = []
    for name in groups:
        if name not in available:
            raise SystemSkillAssetError(f"Unknown packaged system-skill group: {name}")
        selected.append(available[name])
    return tuple(selected)


def _normalize_relative_path(value: str) -> str:
    path = PurePosixPath(value)
    if value == "" or path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise SystemSkillAssetError(f"System-skill path must be a safe relative path: {value!r}")
    return path.as_posix()


def _join_resource(root: Traversable, relative_path: str) -> Traversable:
    target = root
    for part in PurePosixPath(relative_path).parts:
        target = target.joinpath(part)
    return target


def _ensure_empty_or_new_directory(target: Path) -> None:
    if target.exists():
        if not target.is_dir():
            raise SystemSkillAssetError(f"System-skill materialization target is not a directory: {target}")
        if any(target.iterdir()):
            raise SystemSkillAssetError(f"System-skill materialization target must be empty: {target}")
    else:
        target.mkdir(parents=True)


def _copy_resource_tree(source: Traversable, destination: Path, copied_paths: list[Path]) -> None:
    if destination.exists():
        raise SystemSkillAssetError(f"Refusing to overwrite existing path: {destination}")
    destination.mkdir(parents=True)
    copied_paths.append(destination)
    for child in source.iterdir():
        child_destination = destination / child.name
        if child.is_dir():
            _copy_resource_tree(child, child_destination, copied_paths)
        elif child.is_file():
            copied_paths.append(_copy_resource_file(child, child_destination))


def _copy_resource_file(source: Traversable, destination: Path) -> Path:
    if destination.exists():
        raise SystemSkillAssetError(f"Refusing to overwrite existing file: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(source.read_bytes())
    return destination
