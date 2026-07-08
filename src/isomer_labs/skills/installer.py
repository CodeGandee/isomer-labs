"""Install packaged Isomer system skills into agent tool skill roots."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import metadata
from importlib.resources.abc import Traversable
import json
import os
from pathlib import Path
import shutil
from typing import Literal, Sequence

from isomer_labs.skills.system_assets import (
    SystemSkillAssetError,
    iter_system_skill_groups,
    resolve_system_skill,
)


INSTALL_MARKER_FILENAME = ".isomer-system-skill.json"
INSTALL_MARKER_SCHEMA = "isomer-system-skill-install.v1"
CONCRETE_TARGETS = ("claude-code", "codex", "kimi-code", "generic")
SUPPORTED_TARGETS = (*CONCRETE_TARGETS, "all")
ProjectionMode = Literal["copy", "symlink"]


class SystemSkillInstallError(RuntimeError):
    """Raised when packaged system-skill installation cannot proceed safely."""


@dataclass(frozen=True)
class SystemSkillRecord:
    """One installable packaged Isomer system skill."""

    name: str
    source_path: str
    group: str
    group_kind: str
    extension_id: str | None
    description: str | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "source_path": self.source_path,
            "group": self.group,
            "group_kind": self.group_kind,
            "extension_id": self.extension_id,
            "description": self.description,
        }


@dataclass(frozen=True)
class SystemSkillSelection:
    """Resolved packaged system-skill selection."""

    selected_groups: tuple[str, ...]
    selected_extensions: tuple[str, ...]
    explicit_skills: tuple[str, ...]
    skills: tuple[SystemSkillRecord, ...]

    def to_json(self) -> dict[str, object]:
        return {
            "selected_groups": list(self.selected_groups),
            "selected_extensions": list(self.selected_extensions),
            "explicit_skills": list(self.explicit_skills),
            "skills": [skill.to_json() for skill in self.skills],
            "skill_names": [skill.name for skill in self.skills],
        }


@dataclass(frozen=True)
class SystemSkillTarget:
    """Resolved concrete installation target."""

    target: str
    skill_root: Path

    def to_json(self) -> dict[str, str]:
        return {"target": self.target, "skill_root": str(self.skill_root)}


@dataclass(frozen=True)
class InstalledSystemSkill:
    """One Isomer-owned packaged system-skill projection."""

    name: str
    path: Path
    source_path: str | None
    projection_mode: str | None

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "path": str(self.path),
            "source_path": self.source_path,
            "projection_mode": self.projection_mode,
        }


@dataclass(frozen=True)
class UnmanagedSystemSkillCollision:
    """One skill-named directory not owned by Isomer."""

    name: str
    path: Path

    def to_json(self) -> dict[str, str]:
        return {"name": self.name, "path": str(self.path)}


@dataclass(frozen=True)
class SystemSkillStatusResult:
    """Status for one target skill root."""

    target: SystemSkillTarget
    installed: tuple[InstalledSystemSkill, ...]
    missing: tuple[str, ...]
    unmanaged_collisions: tuple[UnmanagedSystemSkillCollision, ...]
    selection: SystemSkillSelection

    def to_json(self) -> dict[str, object]:
        return {
            "target": self.target.target,
            "skill_root": str(self.target.skill_root),
            "installed": [record.to_json() for record in self.installed],
            "installed_skills": [record.name for record in self.installed],
            "missing_skills": list(self.missing),
            "unmanaged_collisions": [collision.to_json() for collision in self.unmanaged_collisions],
            "selection": self.selection.to_json(),
        }


@dataclass(frozen=True)
class SystemSkillInstallResult:
    """Install result for one target skill root."""

    target: SystemSkillTarget
    selection: SystemSkillSelection
    installed: tuple[InstalledSystemSkill, ...]
    unmanaged_collisions: tuple[UnmanagedSystemSkillCollision, ...]
    projection_mode: ProjectionMode

    @property
    def ok(self) -> bool:
        return not self.unmanaged_collisions

    def to_json(self) -> dict[str, object]:
        return {
            "target": self.target.target,
            "skill_root": str(self.target.skill_root),
            "projection_mode": self.projection_mode,
            "installed": [record.to_json() for record in self.installed],
            "installed_skills": [record.name for record in self.installed],
            "unmanaged_collisions": [collision.to_json() for collision in self.unmanaged_collisions],
            "selection": self.selection.to_json(),
        }


@dataclass(frozen=True)
class SystemSkillUninstallResult:
    """Uninstall result for one target skill root."""

    target: SystemSkillTarget
    removed: tuple[InstalledSystemSkill, ...]
    absent: tuple[str, ...]
    preserved_unmanaged: tuple[UnmanagedSystemSkillCollision, ...]
    selection: SystemSkillSelection

    @property
    def ok(self) -> bool:
        return True

    def to_json(self) -> dict[str, object]:
        return {
            "target": self.target.target,
            "skill_root": str(self.target.skill_root),
            "removed": [record.to_json() for record in self.removed],
            "removed_skills": [record.name for record in self.removed],
            "absent_skills": list(self.absent),
            "preserved_unmanaged": [collision.to_json() for collision in self.preserved_unmanaged],
            "selection": self.selection.to_json(),
        }


def list_packaged_system_skills() -> tuple[SystemSkillRecord, ...]:
    """Return installable packaged Isomer system skills in manifest order."""

    records: list[SystemSkillRecord] = []
    seen_names: set[str] = set()
    for group in iter_system_skill_groups():
        for source_path in group.skills:
            name = Path(source_path).name
            if name in seen_names:
                raise SystemSkillInstallError(f"Duplicate packaged system skill name: {name}")
            seen_names.add(name)
            records.append(
                SystemSkillRecord(
                    name=name,
                    source_path=source_path,
                    group=group.name,
                    group_kind=group.kind,
                    extension_id=group.extension_id,
                    description=_read_skill_description(source_path),
                )
            )
    return tuple(records)


def resolve_system_skill_selection(
    *,
    groups: Sequence[str] = (),
    extensions: Sequence[str] = (),
    all_extensions: bool = False,
    skills: Sequence[str] = (),
    default_core: bool = True,
) -> SystemSkillSelection:
    """Resolve user selectors to packaged Isomer system skills."""

    group_records = {group.name: group for group in iter_system_skill_groups()}
    extension_records = {
        group.extension_id: group
        for group in group_records.values()
        if group.kind == "extension" and group.extension_id is not None
    }
    skill_records = {record.name: record for record in list_packaged_system_skills()}
    selected_group_names: list[str] = []
    selected_extension_ids: list[str] = []
    selected_skill_names: list[str] = []

    for group_name in groups:
        if group_name not in group_records:
            raise SystemSkillInstallError(f"Unknown packaged system-skill group: {group_name}")
        selected_group_names.append(group_name)

    for extension_id in extensions:
        if extension_id not in extension_records:
            raise SystemSkillInstallError(f"Unknown packaged system-skill extension: {extension_id}")
        selected_extension_ids.append(extension_id)

    if all_extensions:
        selected_extension_ids.extend(extension_id for extension_id in extension_records if extension_id is not None)

    for skill_name in skills:
        if skill_name not in skill_records:
            raise SystemSkillInstallError(f"Unknown packaged system skill: {skill_name}")
        selected_skill_names.append(skill_name)

    has_selector = bool(selected_group_names or selected_extension_ids or selected_skill_names)
    if default_core and (not has_selector or selected_extension_ids or all_extensions):
        selected_group_names.insert(0, "core")

    resolved_names: list[str] = []
    for group_name in dict.fromkeys(selected_group_names):
        for source_path in group_records[group_name].skills:
            resolved_names.append(Path(source_path).name)
    for extension_id in dict.fromkeys(selected_extension_ids):
        group = extension_records[extension_id]
        for source_path in group.skills:
            resolved_names.append(Path(source_path).name)
    resolved_names.extend(selected_skill_names)

    unique_names = tuple(dict.fromkeys(resolved_names))
    if not unique_names:
        raise SystemSkillInstallError("At least one packaged system skill must be selected.")
    return SystemSkillSelection(
        selected_groups=tuple(dict.fromkeys(selected_group_names)),
        selected_extensions=tuple(dict.fromkeys(selected_extension_ids)),
        explicit_skills=tuple(dict.fromkeys(selected_skill_names)),
        skills=tuple(skill_records[name] for name in unique_names),
    )


def resolve_targets(target: str, *, home: Path | None = None, cwd: Path | None = None) -> tuple[SystemSkillTarget, ...]:
    """Resolve a CLI target selector to concrete skill roots."""

    if target not in SUPPORTED_TARGETS:
        supported = ", ".join(SUPPORTED_TARGETS)
        raise SystemSkillInstallError(f"Unsupported system skill target {target!r}. Expected one of: {supported}.")
    if target == "all":
        if home is not None:
            raise SystemSkillInstallError("--home can only be used with one concrete --target, not --target all.")
        return tuple(resolve_targets(item, cwd=cwd)[0] for item in CONCRETE_TARGETS)

    root = _default_skill_root(target, cwd=cwd) if home is None else home.expanduser()
    return (SystemSkillTarget(target=target, skill_root=root.resolve(strict=False)),)


def install_system_skills(
    target: SystemSkillTarget,
    selection: SystemSkillSelection,
    *,
    projection_mode: ProjectionMode = "copy",
) -> SystemSkillInstallResult:
    """Install selected packaged skills into one target skill root."""

    _validate_projection_mode(projection_mode)
    target.skill_root.mkdir(parents=True, exist_ok=True)
    collisions = _unmanaged_collisions(target, selection)
    if collisions:
        return SystemSkillInstallResult(
            target=target,
            selection=selection,
            installed=(),
            unmanaged_collisions=collisions,
            projection_mode=projection_mode,
        )

    installed: list[InstalledSystemSkill] = []
    for record in selection.skills:
        destination = target.skill_root / record.name
        _remove_path(destination)
        _project_skill(record.source_path, destination, projection_mode=projection_mode)
        _write_marker(destination, target=target.target, record=record, projection_mode=projection_mode)
        installed.append(
            InstalledSystemSkill(
                name=record.name,
                path=destination,
                source_path=record.source_path,
                projection_mode=projection_mode,
            )
        )
    return SystemSkillInstallResult(
        target=target,
        selection=selection,
        installed=tuple(installed),
        unmanaged_collisions=(),
        projection_mode=projection_mode,
    )


def inspect_system_skills(target: SystemSkillTarget, selection: SystemSkillSelection) -> SystemSkillStatusResult:
    """Inspect selected packaged skill projections for one target skill root."""

    installed: list[InstalledSystemSkill] = []
    missing: list[str] = []
    collisions: list[UnmanagedSystemSkillCollision] = []
    for record in selection.skills:
        destination = target.skill_root / record.name
        marker = _read_marker(destination)
        if marker is None:
            if destination.exists() or destination.is_symlink():
                collisions.append(UnmanagedSystemSkillCollision(name=record.name, path=destination))
            else:
                missing.append(record.name)
            continue
        installed.append(
            InstalledSystemSkill(
                name=record.name,
                path=destination,
                source_path=_marker_string(marker, "source_path"),
                projection_mode=_marker_string(marker, "projection_mode"),
            )
        )
    return SystemSkillStatusResult(
        target=target,
        selection=selection,
        installed=tuple(installed),
        missing=tuple(missing),
        unmanaged_collisions=tuple(collisions),
    )


def uninstall_system_skills(target: SystemSkillTarget, selection: SystemSkillSelection) -> SystemSkillUninstallResult:
    """Remove selected Isomer-owned packaged skill projections from one target skill root."""

    removed: list[InstalledSystemSkill] = []
    absent: list[str] = []
    preserved: list[UnmanagedSystemSkillCollision] = []
    for record in selection.skills:
        destination = target.skill_root / record.name
        marker = _read_marker(destination)
        if marker is None:
            if destination.exists() or destination.is_symlink():
                preserved.append(UnmanagedSystemSkillCollision(name=record.name, path=destination))
            else:
                absent.append(record.name)
            continue
        removed.append(
            InstalledSystemSkill(
                name=record.name,
                path=destination,
                source_path=_marker_string(marker, "source_path"),
                projection_mode=_marker_string(marker, "projection_mode"),
            )
        )
        _remove_path(destination)
    return SystemSkillUninstallResult(
        target=target,
        selection=selection,
        removed=tuple(removed),
        absent=tuple(absent),
        preserved_unmanaged=tuple(preserved),
    )


def _default_skill_root(target: str, *, cwd: Path | None = None) -> Path:
    base = (cwd or Path.cwd()).resolve()
    if target == "claude-code":
        return base / ".claude" / "skills"
    if target == "codex":
        codex_home = os.environ.get("CODEX_HOME", "").strip()
        if codex_home:
            return Path(codex_home).expanduser() / "skills"
        return Path.home() / ".codex" / "skills"
    if target == "kimi-code":
        return base / ".kimi-code" / "skills"
    if target == "generic":
        return base / ".agents" / "skills"
    raise SystemSkillInstallError(f"Unsupported concrete target: {target}")


def _validate_projection_mode(projection_mode: str) -> None:
    if projection_mode not in {"copy", "symlink"}:
        raise SystemSkillInstallError("Projection mode must be `copy` or `symlink`.")


def _unmanaged_collisions(
    target: SystemSkillTarget,
    selection: SystemSkillSelection,
) -> tuple[UnmanagedSystemSkillCollision, ...]:
    collisions: list[UnmanagedSystemSkillCollision] = []
    for record in selection.skills:
        destination = target.skill_root / record.name
        if (destination.exists() or destination.is_symlink()) and _read_marker(destination) is None:
            collisions.append(UnmanagedSystemSkillCollision(name=record.name, path=destination))
    return tuple(collisions)


def _project_skill(source_path: str, destination: Path, *, projection_mode: ProjectionMode) -> None:
    source = resolve_system_skill(source_path)
    if projection_mode == "symlink":
        if not isinstance(source, Path):
            raise SystemSkillInstallError(f"Packaged system skill is not filesystem-backed and cannot be symlinked: {source_path}")
        destination.symlink_to(source, target_is_directory=True)
        return
    _copy_resource_tree(source, destination)


def _copy_resource_tree(source: Traversable, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for child in source.iterdir():
        target = destination / child.name
        if child.is_dir():
            _copy_resource_tree(child, target)
        elif child.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(child.read_bytes())


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    if path.is_dir():
        shutil.rmtree(path)


def _write_marker(
    destination: Path,
    *,
    target: str,
    record: SystemSkillRecord,
    projection_mode: ProjectionMode,
) -> None:
    marker = {
        "schema_version": INSTALL_MARKER_SCHEMA,
        "package": "isomer-labs",
        "package_version": _package_version(),
        "installed_by": "isomer-cli",
        "target": target,
        "skill_name": record.name,
        "source_path": record.source_path,
        "projection_mode": projection_mode,
    }
    (destination / INSTALL_MARKER_FILENAME).write_text(json.dumps(marker, indent=2, sort_keys=True), encoding="utf-8")


def _read_marker(destination: Path) -> dict[str, object] | None:
    marker_path = destination / INSTALL_MARKER_FILENAME
    if not marker_path.is_file():
        return None
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(marker, dict):
        return None
    if marker.get("schema_version") != INSTALL_MARKER_SCHEMA:
        return None
    if marker.get("package") != "isomer-labs":
        return None
    return marker


def _marker_string(marker: dict[str, object], key: str) -> str | None:
    value = marker.get(key)
    return value if isinstance(value, str) else None


def _read_skill_description(source_path: str) -> str | None:
    try:
        skill_md = resolve_system_skill(source_path).joinpath("SKILL.md").read_text(encoding="utf-8")
    except (OSError, SystemSkillAssetError):
        return None
    if not skill_md.startswith("---"):
        return None
    frontmatter = skill_md.split("---", 2)
    if len(frontmatter) < 3:
        return None
    for line in frontmatter[1].splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip().strip('"')
    return None


def _package_version() -> str | None:
    try:
        return metadata.version("isomer-labs")
    except metadata.PackageNotFoundError:
        return None
