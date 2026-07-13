"""Package-resource helpers for official Isomer system skills."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path, PurePosixPath
import re
from typing import Any, Sequence

from packaging.version import InvalidVersion, Version
import tomlkit


SYSTEM_SKILLS_RESOURCE = "assets/system_skills"
SYSTEM_SKILL_GROUP_KINDS = ("core", "extension")
SYSTEM_EXTENSION_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")
SYSTEM_EXTENSION_COMMAND_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class SystemSkillAssetError(ValueError):
    """Raised when packaged system-skill assets are invalid or unavailable."""


@dataclass(frozen=True)
class SystemSkillGroup:
    """Manifest-defined system-skill group."""

    name: str
    description: str
    skills: tuple[str, ...]
    kind: str
    always_available: bool
    minimum_compatible_skill_version: str
    extension_id: str | None = None
    entry_skill: str | None = None
    commands: tuple[str, ...] = ()


@dataclass(frozen=True)
class SystemSkillExtension:
    """Manifest-defined optional system-skill extension."""

    extension_id: str
    group: str
    description: str
    skills: tuple[str, ...]
    entry_skill: str
    commands: tuple[str, ...]
    minimum_compatible_skill_version: str


@dataclass(frozen=True)
class SystemSkillCatalogMetadata:
    """Package-owned metadata for one system skill."""

    callback_insertion_points: tuple[str, ...] = ()
    minimum_compatible_version: str | None = None


@dataclass(frozen=True)
class CallbackInsertionPointStage:
    """Manifest-defined callback insertion point stage."""

    stage: str
    label: str
    description: str


@dataclass(frozen=True)
class CallbackInsertionPoint:
    """Manifest-defined callback insertion point for one packaged system skill."""

    target_skill: str
    skill_path: str
    group: str
    group_kind: str
    extension_id: str | None
    stage: str
    stage_label: str
    description: str


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

    return _parse_system_skill_groups(load_system_skill_manifest())


def iter_system_skill_extensions() -> tuple[SystemSkillExtension, ...]:
    """Return manifest-defined optional system-skill extensions."""

    extensions: list[SystemSkillExtension] = []
    for group in iter_system_skill_groups():
        if group.kind != "extension" or group.extension_id is None:
            continue
        if group.entry_skill is None:
            raise SystemSkillAssetError(f"Extension system-skill group {group.name!r} is missing entry_skill.")
        extensions.append(
            SystemSkillExtension(
                extension_id=group.extension_id,
                group=group.name,
                description=group.description,
                skills=group.skills,
                entry_skill=group.entry_skill,
                commands=group.commands,
                minimum_compatible_skill_version=group.minimum_compatible_skill_version,
            )
        )
    return tuple(extensions)


def callback_insertion_point_stages() -> tuple[CallbackInsertionPointStage, ...]:
    """Return manifest-defined callback insertion point stages."""

    return _parse_callback_stages(load_system_skill_manifest())


def iter_system_skill_callback_insertion_points(
    *,
    include_core: bool = True,
    extension_ids: Sequence[str] | None = None,
    include_all_extensions: bool = False,
    skill: str | None = None,
    stage: str | None = None,
) -> tuple[CallbackInsertionPoint, ...]:
    """Return manifest-defined callback insertion points matching filters."""

    manifest = load_system_skill_manifest()
    groups = _parse_system_skill_groups(manifest)
    requested_extensions = tuple(dict.fromkeys(extension_ids or ()))
    if include_all_extensions and requested_extensions:
        raise SystemSkillAssetError("Cannot combine include_all_extensions with explicit extension ids.")
    available_extension_ids = {group.extension_id for group in groups if group.kind == "extension" and group.extension_id is not None}
    for extension_id in requested_extensions:
        if extension_id not in available_extension_ids:
            raise SystemSkillAssetError(f"Unknown packaged system extension: {extension_id}")
    stages = {item.stage: item for item in _parse_callback_stages(manifest)}
    skill_metadata = _parse_skill_metadata(manifest)
    points: list[CallbackInsertionPoint] = []
    seen_targets: set[tuple[str, str]] = set()
    for group in groups:
        include_group = group.kind == "core" and include_core
        if group.kind == "extension":
            include_group = include_all_extensions or (group.extension_id in requested_extensions)
        if not include_group:
            continue
        for skill_path in group.skills:
            metadata = skill_metadata.get(skill_path, SystemSkillCatalogMetadata())
            for point_stage in metadata.callback_insertion_points:
                if point_stage not in stages:
                    raise SystemSkillAssetError(f"Unknown callback insertion point stage {point_stage!r} for {skill_path}.")
                target_skill = Path(skill_path).name
                key = (target_skill, point_stage)
                if key in seen_targets:
                    raise SystemSkillAssetError(f"Duplicate callback insertion point target: {target_skill}/{point_stage}")
                seen_targets.add(key)
                stage_metadata = stages[point_stage]
                point = CallbackInsertionPoint(
                    target_skill=target_skill,
                    skill_path=skill_path,
                    group=group.name,
                    group_kind=group.kind,
                    extension_id=group.extension_id,
                    stage=point_stage,
                    stage_label=stage_metadata.label,
                    description=stage_metadata.description,
                )
                if skill is not None and point.target_skill != skill:
                    continue
                if stage is not None and point.stage != stage:
                    continue
                points.append(point)
    return tuple(points)


def has_system_skill_callback_insertion_point(skill: str | None, stage: str | None) -> bool:
    """Return whether the packaged catalog declares a callback insertion point."""

    if not skill or not stage:
        return False
    return any(
        True
        for _ in iter_system_skill_callback_insertion_points(
            include_core=True,
            include_all_extensions=True,
            skill=skill,
            stage=stage,
        )
    )


def callback_insertion_point_stage_names() -> tuple[str, ...]:
    """Return manifest-defined callback insertion point stage ids."""

    return tuple(stage.stage for stage in callback_insertion_point_stages())


def _parse_system_skill_groups(manifest: dict[str, Any]) -> tuple[SystemSkillGroup, ...]:
    groups = manifest.get("groups")
    if not isinstance(groups, dict):
        raise SystemSkillAssetError("Packaged system-skill manifest must define [groups].")
    parsed_groups: list[SystemSkillGroup] = []
    extension_ids: set[str] = set()
    for name, value in groups.items():
        if not isinstance(value, dict):
            raise SystemSkillAssetError(f"System-skill group {name!r} must be a table.")
        description = value.get("description", "")
        skills = value.get("skills")
        if not isinstance(skills, list) or not all(isinstance(item, str) for item in skills):
            raise SystemSkillAssetError(f"System-skill group {name!r} must define a string skills list.")
        kind = value.get("kind")
        if kind not in SYSTEM_SKILL_GROUP_KINDS:
            raise SystemSkillAssetError(f"System-skill group {name!r} must define kind as core or extension.")
        always_available = value.get("always_available")
        if not isinstance(always_available, bool):
            raise SystemSkillAssetError(f"System-skill group {name!r} must define boolean always_available.")
        extension_id = value.get("extension_id")
        entry_skill = value.get("entry_skill")
        commands = value.get("commands")
        minimum_compatible_skill_version = _required_pep440_version(
            value.get("minimum_compatible_skill_version"),
            f"System-skill group {name!r} minimum_compatible_skill_version",
        )
        if kind == "core":
            if extension_id is not None:
                raise SystemSkillAssetError(f"Core system-skill group {name!r} must not define extension_id.")
            if entry_skill is not None or commands is not None:
                raise SystemSkillAssetError(f"Core system-skill group {name!r} must not define extension entry metadata.")
            if not always_available:
                raise SystemSkillAssetError(f"Core system-skill group {name!r} must be always_available.")
        else:
            if not isinstance(extension_id, str) or not SYSTEM_EXTENSION_ID_RE.match(extension_id):
                raise SystemSkillAssetError(f"Extension system-skill group {name!r} must define a stable extension_id.")
            if always_available:
                raise SystemSkillAssetError(f"Extension system-skill group {name!r} must not be always_available.")
            if extension_id in extension_ids:
                raise SystemSkillAssetError(f"Duplicate packaged system extension id: {extension_id}")
            extension_ids.add(extension_id)
            skill_names = {PurePosixPath(item).name for item in skills}
            if not isinstance(entry_skill, str) or not entry_skill or entry_skill not in skill_names:
                raise SystemSkillAssetError(
                    f"Extension system-skill group {name!r} must define entry_skill as one of its packaged skill names."
                )
            if not isinstance(commands, list) or not all(
                isinstance(item, str) and SYSTEM_EXTENSION_COMMAND_RE.fullmatch(item) for item in commands
            ):
                raise SystemSkillAssetError(
                    f"Extension system-skill group {name!r} must define commands as a list of stable command ids."
                )
            if len(commands) != len(set(commands)):
                raise SystemSkillAssetError(f"Extension system-skill group {name!r} must not define duplicate commands.")
        parsed_groups.append(
            SystemSkillGroup(
                name=str(name),
                description=str(description),
                skills=tuple(_normalize_relative_path(item) for item in skills),
                kind=str(kind),
                always_available=always_available,
                minimum_compatible_skill_version=minimum_compatible_skill_version,
                extension_id=str(extension_id) if isinstance(extension_id, str) else None,
                entry_skill=str(entry_skill) if isinstance(entry_skill, str) else None,
                commands=tuple(str(item) for item in commands) if isinstance(commands, list) else (),
            )
        )
    return tuple(parsed_groups)


def _parse_callback_stages(manifest: dict[str, Any]) -> tuple[CallbackInsertionPointStage, ...]:
    raw_stages = manifest.get("callback_insertion_point_stages")
    if raw_stages is None:
        return ()
    if not isinstance(raw_stages, dict):
        raise SystemSkillAssetError("Packaged system-skill manifest callback insertion point stages must be a table.")
    stages: list[CallbackInsertionPointStage] = []
    for stage, value in raw_stages.items():
        if not isinstance(value, dict):
            raise SystemSkillAssetError(f"Callback insertion point stage {stage!r} must be a table.")
        label = value.get("label")
        description = value.get("description")
        if not isinstance(label, str) or not label:
            raise SystemSkillAssetError(f"Callback insertion point stage {stage!r} must define label.")
        if not isinstance(description, str) or not description:
            raise SystemSkillAssetError(f"Callback insertion point stage {stage!r} must define description.")
        stages.append(CallbackInsertionPointStage(stage=str(stage), label=label, description=description))
    return tuple(stages)


def _parse_skill_metadata(manifest: dict[str, Any]) -> dict[str, SystemSkillCatalogMetadata]:
    raw_metadata = manifest.get("skill_metadata")
    if raw_metadata is None:
        return {}
    if not isinstance(raw_metadata, dict):
        raise SystemSkillAssetError("Packaged system-skill manifest skill_metadata must be a table.")
    known_paths = set(iter_system_skill_paths())
    parsed: dict[str, SystemSkillCatalogMetadata] = {}
    for raw_path, value in raw_metadata.items():
        skill_path = _normalize_relative_path(str(raw_path))
        if skill_path not in known_paths:
            raise SystemSkillAssetError(f"Callback insertion point metadata references unknown packaged system skill: {skill_path}")
        if not isinstance(value, dict):
            raise SystemSkillAssetError(f"System-skill metadata {skill_path!r} must be a table.")
        raw_points = value.get("callback_insertion_points", ())
        if not isinstance(raw_points, list) or not all(isinstance(item, str) and item for item in raw_points):
            raise SystemSkillAssetError(f"System-skill metadata {skill_path!r} callback_insertion_points must be a string list.")
        minimum = value.get("minimum_compatible_version")
        if minimum is not None:
            minimum = _required_pep440_version(
                minimum,
                f"System-skill metadata {skill_path!r} minimum_compatible_version",
            )
        parsed[skill_path] = SystemSkillCatalogMetadata(
            callback_insertion_points=tuple(dict.fromkeys(str(item) for item in raw_points)),
            minimum_compatible_version=minimum,
        )
    return parsed


def system_skill_catalog_metadata() -> dict[str, SystemSkillCatalogMetadata]:
    """Return package-owned per-skill metadata keyed by manifest-relative path."""

    return _parse_skill_metadata(load_system_skill_manifest())


def minimum_compatible_system_skill_version(skill_path: str) -> str:
    """Resolve the package-owned compatibility floor for one packaged skill."""

    normalized = _normalize_relative_path(skill_path)
    metadata = system_skill_catalog_metadata().get(normalized)
    if metadata is not None and metadata.minimum_compatible_version is not None:
        return metadata.minimum_compatible_version
    for group in iter_system_skill_groups():
        if normalized in group.skills:
            return group.minimum_compatible_skill_version
    raise SystemSkillAssetError(f"Unknown packaged system skill: {normalized}")


def _required_pep440_version(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise SystemSkillAssetError(f"{field} must be a non-empty PEP 440 version.")
    try:
        Version(value)
    except InvalidVersion as exc:
        raise SystemSkillAssetError(f"{field} must be a valid PEP 440 version: {value!r}") from exc
    return value


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
