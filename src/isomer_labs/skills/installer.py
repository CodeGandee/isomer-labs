"""Install packaged Isomer system skills into agent tool skill roots."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from functools import lru_cache
from importlib import metadata
from importlib.resources.abc import Traversable
import json
import os
from pathlib import Path
import shutil
from typing import Mapping, Sequence

from packaging.version import Version

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.skills.install_results import (
    SystemSkillInstallResult,
    SystemSkillStatusResult,
    SystemSkillUninstallResult,
    SystemSkillUpgradeResult,
)
from isomer_labs.skills.receipts import (
    ProjectionMode,
    SKILL_MANIFEST_FILENAME as SKILL_MANIFEST_FILENAME,
    SKILL_MANIFEST_SCHEMA,
    SystemSkillManifestInspection,
    SystemSkillManifestRecord,
    SystemSkillRootManifest,
    inspect_system_skill_receipt,
)
from isomer_labs.skills.system_assets import (
    SystemSkillAssetError,
    iter_system_skill_groups,
    minimum_compatible_system_skill_version,
    resolve_system_skill,
)
from isomer_labs.skills.versioning import inspect_skill_version, require_skill_version


CONCRETE_TARGETS = ("claude-code", "codex", "kimi-code", "generic")
SUPPORTED_TARGETS = (*CONCRETE_TARGETS, "all")


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
    skill_version: str
    minimum_compatible_version: str
    description: str | None = None

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "source_path": self.source_path,
            "group": self.group,
            "group_kind": self.group_kind,
            "extension_id": self.extension_id,
            "skill_version": self.skill_version,
            "minimum_compatible_version": self.minimum_compatible_version,
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
    skill_version: str | None = None
    receipt_skill_version: str | None = None
    minimum_compatible_version: str | None = None
    compatibility_status: str = "unversioned"
    installation_verified: bool = False

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "path": str(self.path),
            "source_path": self.source_path,
            "projection_mode": self.projection_mode,
            "skill_version": self.skill_version,
            "receipt_skill_version": self.receipt_skill_version,
            "minimum_compatible_version": self.minimum_compatible_version,
            "compatibility_status": self.compatibility_status,
            "installation_verified": self.installation_verified,
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


@lru_cache(maxsize=1)
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
                    skill_version=_packaged_skill_version(source_path),
                    minimum_compatible_version=minimum_compatible_system_skill_version(source_path),
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


def resolve_targets(
    target: str,
    *,
    home: Path | None = None,
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
) -> tuple[SystemSkillTarget, ...]:
    """Resolve a CLI target selector to concrete skill roots."""

    if target not in SUPPORTED_TARGETS:
        supported = ", ".join(SUPPORTED_TARGETS)
        raise SystemSkillInstallError(f"Unsupported system skill target {target!r}. Expected one of: {supported}.")
    if target == "all":
        if home is not None:
            raise SystemSkillInstallError("--home can only be used with one concrete --target, not --target all.")
        return tuple(resolve_targets(item, cwd=cwd, env=env)[0] for item in CONCRETE_TARGETS)

    root = _default_skill_root(target, cwd=cwd, env=env) if home is None else home.expanduser()
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
        receipt_record = _manifest_record_for(record, projection_mode)
        installed.append(_installed_record(record, destination, projection_mode, receipt_record))
        manifest_records[record.name] = SystemSkillManifestRecord(
            name=record.name,
            source_path=record.source_path,
            projection_mode=projection_mode,
            skill_version=record.skill_version,
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
    manifest_records = manifest.record_map() if manifest is not None else {}
    installed: list[InstalledSystemSkill] = []
    missing: list[str] = []
    invalid: list[InvalidSystemSkillProjection] = []
    status_diagnostics = list(diagnostics)
    for record in selection.skills:
        destination = target.skill_root / record.name
        if destination.is_symlink() and destination.is_dir():
            installed.append(_installed_record(record, destination, "symlink", manifest_records.get(record.name)))
        elif destination.is_symlink():
            issue = InvalidSystemSkillProjection(
                name=record.name,
                path=destination,
                path_kind="broken_symlink" if not destination.exists() else "symlink_to_non_directory",
                message="Selected packaged system-skill symlink does not resolve to a skill directory.",
            )
            invalid.append(issue)
            status_diagnostics.append(_projection_diagnostic(issue))
        elif destination.is_dir():
            installed.append(_installed_record(record, destination, "copy", manifest_records.get(record.name)))
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
            removed.append(
                _installed_record(
                    record,
                    destination,
                    _detected_projection_mode(destination),
                    manifest_records.get(record.name),
                )
            )
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
        refreshed_record = _manifest_record_for(record, mode)
        refreshed.append(_installed_record(record, destination, mode, refreshed_record))
        manifest_records[record.name] = refreshed_record

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


def _default_skill_root(
    target: str,
    *,
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
) -> Path:
    base = (cwd or Path.cwd()).resolve()
    if target == "claude-code":
        return base / ".claude" / "skills"
    if target == "codex":
        effective_env = os.environ if env is None else env
        codex_home = effective_env.get("CODEX_HOME", "").strip()
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


def inspect_system_skill_manifest(target: SystemSkillTarget) -> SystemSkillManifestInspection:
    """Inspect the Isomer receipt in exactly one supplied system-skill root."""

    return inspect_system_skill_receipt(target.skill_root, target.target)


def _read_manifest(target: SystemSkillTarget) -> tuple[SystemSkillRootManifest | None, tuple[Diagnostic, ...]]:
    inspection = inspect_system_skill_manifest(target)
    return inspection.manifest, inspection.diagnostics


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
        skill_version=record.skill_version,
    )


def _installed_record(
    record: SystemSkillRecord,
    destination: Path,
    projection_mode: str | None,
    receipt_record: SystemSkillManifestRecord | None = None,
) -> InstalledSystemSkill:
    observation = inspect_skill_version(destination)
    receipt_version = receipt_record.skill_version if receipt_record is not None else None
    return InstalledSystemSkill(
        name=record.name,
        path=destination,
        source_path=record.source_path,
        projection_mode=projection_mode,
        skill_version=observation.raw_version,
        receipt_skill_version=receipt_version,
        minimum_compatible_version=record.minimum_compatible_version,
        compatibility_status=_skill_compatibility_status(record, observation.raw_version, observation.status, receipt_record),
        installation_verified=(
            receipt_record is not None
            and receipt_version is not None
            and observation.status == "valid"
            and receipt_version == observation.raw_version
        ),
    )


def _skill_compatibility_status(
    record: SystemSkillRecord,
    observed_version: str | None,
    metadata_status: str,
    receipt_record: SystemSkillManifestRecord | None,
) -> str:
    if metadata_status != "valid" or observed_version is None:
        return metadata_status
    if receipt_record is not None and receipt_record.skill_version is None:
        return "unversioned"
    if receipt_record is not None and receipt_record.skill_version != observed_version:
        return "receipt_drift"
    observed = Version(observed_version)
    minimum = Version(record.minimum_compatible_version)
    current = Version(record.skill_version)
    if observed < minimum:
        return "obsolete_incompatible"
    if observed < current:
        return "compatible_older"
    if observed == current:
        return "current"
    return "newer_than_cli"


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


def _packaged_skill_version(source_path: str) -> str:
    try:
        return require_skill_version(resolve_system_skill(source_path))
    except (SystemSkillAssetError, ValueError) as exc:
        raise SystemSkillInstallError(f"Packaged system skill {source_path!r} has invalid version metadata: {exc}") from exc
