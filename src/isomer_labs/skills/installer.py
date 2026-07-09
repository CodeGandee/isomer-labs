"""Install packaged Isomer system skills into agent tool skill roots."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from importlib import metadata
from importlib.resources.abc import Traversable
import json
import os
from pathlib import Path
import shutil
from typing import Literal, Sequence

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.skills.system_assets import (
    SystemSkillAssetError,
    iter_system_skill_groups,
    resolve_system_skill,
)


SKILL_MANIFEST_FILENAME = "isomer-labs-skill-manifest.json"
SKILL_MANIFEST_SCHEMA = "isomer-labs-skill-manifest.v1"
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
    """One packaged system-skill projection in a target root."""

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
class ExistingSystemSkillPath:
    """One selected skill path preserved because force was not requested."""

    name: str
    path: Path
    path_kind: str

    def to_json(self) -> dict[str, str]:
        return {"name": self.name, "path": str(self.path), "path_kind": self.path_kind}


@dataclass(frozen=True)
class InvalidSystemSkillProjection:
    """One selected skill path that exists in an unsupported shape."""

    name: str
    path: Path
    path_kind: str
    message: str

    def to_json(self) -> dict[str, str]:
        return {
            "name": self.name,
            "path": str(self.path),
            "path_kind": self.path_kind,
            "message": self.message,
        }


@dataclass(frozen=True)
class SystemSkillManifestRecord:
    """One skill record tracked in the target-root manifest."""

    name: str
    source_path: str
    projection_mode: ProjectionMode

    def to_json(self) -> dict[str, str]:
        return {
            "name": self.name,
            "source_path": self.source_path,
            "projection_mode": self.projection_mode,
        }


@dataclass(frozen=True)
class SystemSkillRootManifest:
    """Target-root manifest for Isomer-managed system skill projections."""

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
    force: bool = False,
) -> SystemSkillInstallResult:
    """Install selected packaged skills into one target skill root."""

    _validate_projection_mode(projection_mode)
    target.skill_root.mkdir(parents=True, exist_ok=True)
    manifest, diagnostics = _read_manifest(target)
    manifest_records = manifest.record_map() if manifest is not None else {}

    installed: list[InstalledSystemSkill] = []
    preserved_existing: list[ExistingSystemSkillPath] = []
    replaced: list[ExistingSystemSkillPath] = []
    for record in selection.skills:
        destination = target.skill_root / record.name
        if destination.exists() or destination.is_symlink():
            existing = ExistingSystemSkillPath(record.name, destination, _path_kind(destination))
            if not force:
                preserved_existing.append(existing)
                continue
            _remove_path(destination)
            replaced.append(existing)
        _project_skill(record.source_path, destination, projection_mode=projection_mode)
        installed.append(_installed_record(record, destination, projection_mode))
        manifest_records[record.name] = SystemSkillManifestRecord(
            name=record.name,
            source_path=record.source_path,
            projection_mode=projection_mode,
        )

    updated_manifest = manifest
    if installed or replaced:
        updated_manifest = _write_manifest(target, manifest_records)
    return SystemSkillInstallResult(
        target=target,
        selection=selection,
        installed=tuple(installed),
        preserved_existing=tuple(preserved_existing),
        replaced=tuple(replaced),
        projection_mode=projection_mode,
        manifest=updated_manifest,
        diagnostics=diagnostics,
    )


def inspect_system_skills(target: SystemSkillTarget, selection: SystemSkillSelection) -> SystemSkillStatusResult:
    """Inspect selected packaged skill projections for one target skill root."""

    manifest, diagnostics = _read_manifest(target)
    installed: list[InstalledSystemSkill] = []
    missing: list[str] = []
    invalid: list[InvalidSystemSkillProjection] = []
    status_diagnostics = list(diagnostics)
    for record in selection.skills:
        destination = target.skill_root / record.name
        if destination.is_symlink():
            installed.append(_installed_record(record, destination, "symlink"))
        elif destination.is_dir():
            installed.append(_installed_record(record, destination, "copy"))
        elif destination.exists():
            issue = InvalidSystemSkillProjection(
                name=record.name,
                path=destination,
                path_kind=_path_kind(destination),
                message="Selected packaged system-skill path is not a directory or symlink projection.",
            )
            invalid.append(issue)
            status_diagnostics.append(_projection_diagnostic(issue))
        else:
            missing.append(record.name)
    return SystemSkillStatusResult(
        target=target,
        selection=selection,
        installed=tuple(installed),
        missing=tuple(missing),
        invalid_projections=tuple(invalid),
        manifest=manifest,
        diagnostics=tuple(status_diagnostics),
    )


def uninstall_system_skills(target: SystemSkillTarget, selection: SystemSkillSelection) -> SystemSkillUninstallResult:
    """Remove selected packaged skill projections from one target skill root."""

    manifest, diagnostics = _read_manifest(target)
    manifest_records = manifest.record_map() if manifest is not None else {}
    removed: list[InstalledSystemSkill] = []
    absent: list[str] = []
    changed_manifest = False
    for record in selection.skills:
        destination = target.skill_root / record.name
        if destination.exists() or destination.is_symlink():
            removed.append(_installed_record(record, destination, _detected_projection_mode(destination)))
            _remove_path(destination)
        else:
            absent.append(record.name)
        if manifest_records.pop(record.name, None) is not None:
            changed_manifest = True

    updated_manifest = manifest
    if removed or changed_manifest:
        target.skill_root.mkdir(parents=True, exist_ok=True)
        updated_manifest = _write_manifest(target, manifest_records)
    return SystemSkillUninstallResult(
        target=target,
        selection=selection,
        removed=tuple(removed),
        absent=tuple(absent),
        manifest=updated_manifest,
        diagnostics=diagnostics,
    )


def upgrade_system_skills(
    target: SystemSkillTarget,
    selection: SystemSkillSelection,
    *,
    projection_mode: ProjectionMode | None = None,
) -> SystemSkillUpgradeResult:
    """Refresh selected packaged skills and remove stale manifest-tracked skills."""

    if projection_mode is not None:
        _validate_projection_mode(projection_mode)
    target.skill_root.mkdir(parents=True, exist_ok=True)
    manifest, diagnostics = _read_manifest(target)
    manifest_records = manifest.record_map() if manifest is not None else {}
    selected_names = {record.name for record in selection.skills}

    stale_removed: list[InstalledSystemSkill] = []
    stale_absent: list[str] = []
    for name, tracked in sorted(manifest_records.items()):
        if name in selected_names:
            continue
        destination = target.skill_root / name
        if destination.exists() or destination.is_symlink():
            stale_removed.append(
                InstalledSystemSkill(
                    name=name,
                    path=destination,
                    source_path=tracked.source_path,
                    projection_mode=_detected_projection_mode(destination),
                )
            )
            _remove_path(destination)
        else:
            stale_absent.append(name)
        manifest_records.pop(name, None)

    refreshed: list[InstalledSystemSkill] = []
    for record in selection.skills:
        destination = target.skill_root / record.name
        mode = projection_mode or manifest_records.get(record.name, _manifest_record_for(record, "copy")).projection_mode
        if destination.exists() or destination.is_symlink():
            _remove_path(destination)
        _project_skill(record.source_path, destination, projection_mode=mode)
        refreshed.append(_installed_record(record, destination, mode))
        manifest_records[record.name] = _manifest_record_for(record, mode)

    updated_manifest = _write_manifest(target, manifest_records)
    return SystemSkillUpgradeResult(
        target=target,
        selection=selection,
        refreshed=tuple(refreshed),
        stale_removed=tuple(stale_removed),
        stale_absent=tuple(stale_absent),
        projection_mode_override=projection_mode,
        manifest=updated_manifest,
        diagnostics=diagnostics,
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


def _read_manifest(target: SystemSkillTarget) -> tuple[SystemSkillRootManifest | None, tuple[Diagnostic, ...]]:
    manifest_path = target.skill_root / SKILL_MANIFEST_FILENAME
    if not manifest_path.exists():
        return None, ()
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, (_manifest_diagnostic(manifest_path, f"Cannot read Isomer skill manifest: {exc}"),)
    if not isinstance(raw, dict):
        return None, (_manifest_diagnostic(manifest_path, "Isomer skill manifest must be a JSON object."),)
    if raw.get("schema_version") != SKILL_MANIFEST_SCHEMA:
        return None, (_manifest_diagnostic(manifest_path, "Unsupported Isomer skill manifest schema version."),)

    skills: list[SystemSkillManifestRecord] = []
    raw_skills = raw.get("skills", [])
    if not isinstance(raw_skills, list):
        return None, (_manifest_diagnostic(manifest_path, "Isomer skill manifest `skills` field must be a list."),)
    for index, item in enumerate(raw_skills):
        if not isinstance(item, dict):
            return None, (_manifest_diagnostic(manifest_path, f"Isomer skill manifest skill record {index} must be an object."),)
        name = item.get("name")
        source_path = item.get("source_path")
        projection_mode = item.get("projection_mode")
        if not isinstance(name, str) or not isinstance(source_path, str) or projection_mode not in {"copy", "symlink"}:
            return None, (_manifest_diagnostic(manifest_path, f"Isomer skill manifest skill record {index} is invalid."),)
        skills.append(
            SystemSkillManifestRecord(
                name=name,
                source_path=source_path,
                projection_mode=projection_mode,
            )
        )

    package_version = raw.get("package_version")
    updated_at = raw.get("updated_at")
    target_name = raw.get("target")
    installed_by = raw.get("installed_by")
    package_name = raw.get("package_name")
    return (
        SystemSkillRootManifest(
            schema_version=SKILL_MANIFEST_SCHEMA,
            target=target_name if isinstance(target_name, str) else target.target,
            skill_root=target.skill_root,
            package_name=package_name if isinstance(package_name, str) else "isomer-labs",
            package_version=package_version if isinstance(package_version, str) else None,
            installed_by=installed_by if isinstance(installed_by, str) else "isomer-cli",
            updated_at=updated_at if isinstance(updated_at, str) else "",
            skills=tuple(skills),
        ),
        (),
    )


def _write_manifest(
    target: SystemSkillTarget,
    records: dict[str, SystemSkillManifestRecord],
) -> SystemSkillRootManifest:
    manifest = SystemSkillRootManifest(
        schema_version=SKILL_MANIFEST_SCHEMA,
        target=target.target,
        skill_root=target.skill_root,
        package_name="isomer-labs",
        package_version=_package_version(),
        installed_by="isomer-cli",
        updated_at=datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        skills=tuple(records[name] for name in sorted(records)),
    )
    target.skill_root.mkdir(parents=True, exist_ok=True)
    manifest.path.write_text(json.dumps(_manifest_file_json(manifest), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest


def _manifest_file_json(manifest: SystemSkillRootManifest) -> dict[str, object]:
    data = manifest.to_json()
    data.pop("path", None)
    data.pop("skill_names", None)
    return data


def _manifest_record_for(record: SystemSkillRecord, projection_mode: ProjectionMode) -> SystemSkillManifestRecord:
    return SystemSkillManifestRecord(
        name=record.name,
        source_path=record.source_path,
        projection_mode=projection_mode,
    )


def _installed_record(record: SystemSkillRecord, destination: Path, projection_mode: str | None) -> InstalledSystemSkill:
    return InstalledSystemSkill(
        name=record.name,
        path=destination,
        source_path=record.source_path,
        projection_mode=projection_mode,
    )


def _detected_projection_mode(path: Path) -> str | None:
    if path.is_symlink():
        return "symlink"
    if path.is_dir():
        return "copy"
    return None


def _path_kind(path: Path) -> str:
    if path.is_symlink():
        return "symlink"
    if path.is_dir():
        return "directory"
    if path.is_file():
        return "file"
    if path.exists():
        return "other"
    return "missing"


def _manifest_diagnostic(path: Path, message: str) -> Diagnostic:
    return Diagnostic(
        code="ISOSKILL001",
        severity="warning",
        concept="system-skill-manifest",
        path=path,
        message=message,
    )


def _projection_diagnostic(issue: InvalidSystemSkillProjection) -> Diagnostic:
    return Diagnostic(
        code="ISOSKILL002",
        severity="warning",
        concept="system-skill-projection",
        path=issue.path,
        field=issue.name,
        message=issue.message,
    )


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
