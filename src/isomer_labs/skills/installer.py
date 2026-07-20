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
from pathlib import PurePosixPath
import shutil
import tempfile
from typing import Literal, Mapping, Sequence

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
    SystemSkillManifestBinding,
    SystemSkillLegacyPathRecord,
    SystemSkillManifestMemberRecord,
    SystemSkillManifestPublicRecord,
    SystemSkillManifestRecord,
    SystemSkillRootManifest,
    inspect_system_skill_receipt,
)
from isomer_labs.skills.system_assets import (
    SystemSkillAssetError,
    iter_system_skill_packs,
    normalize_system_skill_identity,
    resolve_system_skill,
    system_skill_catalog,
)
from isomer_labs.skills.versioning import inspect_skill_version, require_skill_version


CONCRETE_TARGETS = ("claude-code", "codex", "kimi-code", "generic")
SUPPORTED_TARGETS = (*CONCRETE_TARGETS, "all")
SUPPORTED_SCOPES = ("user", "project")
SystemSkillScope = Literal["user", "project"]


class SystemSkillInstallError(RuntimeError):
    """Raised when packaged system-skill installation cannot proceed safely."""


@dataclass(frozen=True)
class SystemSkillMemberRecord:
    """One protected member nested inside an installable public pack."""

    logical_id: str
    member_name: str
    relative_path: str
    source_path: str
    invocation_designator: str
    dependencies: tuple[str, ...]
    skill_version: str
    minimum_compatible_version: str

    def to_json(self) -> dict[str, object]:
        return {
            "logical_id": self.logical_id,
            "member_name": self.member_name,
            "relative_path": self.relative_path,
            "source_path": self.source_path,
            "invocation_designator": self.invocation_designator,
            "dependencies": list(self.dependencies),
            "skill_version": self.skill_version,
            "minimum_compatible_version": self.minimum_compatible_version,
        }


@dataclass(frozen=True)
class SystemSkillPublicRecord:
    """One public projection in an installable complete pack."""

    name: str
    role: str
    source_path: str
    skill_version: str
    minimum_compatible_version: str
    description: str | None = None
    public_commands: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "role": self.role,
            "source_path": self.source_path,
            "skill_version": self.skill_version,
            "minimum_compatible_version": self.minimum_compatible_version,
            "description": self.description,
            "public_commands": list(self.public_commands),
        }


@dataclass(frozen=True)
class SystemSkillRecord:
    """One installable complete Isomer pack."""

    name: str
    pack_id: str
    source_path: str
    group: str
    group_kind: str
    extension_id: str | None
    skill_version: str
    minimum_compatible_version: str
    description: str | None = None
    public_commands: tuple[str, ...] = ()
    public_skills: tuple[SystemSkillPublicRecord, ...] = ()
    protected_members: tuple[SystemSkillMemberRecord, ...] = ()

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "pack_id": self.pack_id,
            "source_path": self.source_path,
            "group": self.group,
            "group_kind": self.group_kind,
            "extension_id": self.extension_id,
            "skill_version": self.skill_version,
            "minimum_compatible_version": self.minimum_compatible_version,
            "description": self.description,
            "public_commands": list(self.public_commands),
            "public_skills": [skill.to_json() for skill in self.public_skills],
            "protected_members": [member.to_json() for member in self.protected_members],
        }


@dataclass(frozen=True)
class DeprecatedSystemSkillSelector:
    """One compatibility selector that resolved to a complete public pack."""

    requested: str
    canonical_public_skill: str
    selector_kind: str

    def to_json(self) -> dict[str, str]:
        return {
            "requested": self.requested,
            "canonical_public_skill": self.canonical_public_skill,
            "selector_kind": self.selector_kind,
            "message": (
                f"Selector {self.requested!r} is deprecated for ordinary installation; "
                f"the complete public pack {self.canonical_public_skill!r} is the projection unit."
            ),
        }


@dataclass(frozen=True)
class SystemSkillSelection:
    """Resolved packaged system-skill selection."""

    selected_groups: tuple[str, ...]
    selected_extensions: tuple[str, ...]
    explicit_skills: tuple[str, ...]
    skills: tuple[SystemSkillRecord, ...]
    deprecated_selectors: tuple[DeprecatedSystemSkillSelector, ...] = ()
    requested_skills: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        return {
            "selected_groups": list(self.selected_groups),
            "selected_extensions": list(self.selected_extensions),
            "explicit_skills": list(self.explicit_skills),
            "requested_skills": list(self.requested_skills),
            "skills": [skill.to_json() for skill in self.skills],
            "skill_names": [skill.name for skill in self.skills],
            "deprecated_selectors": [selector.to_json() for selector in self.deprecated_selectors],
        }


@dataclass(frozen=True)
class SystemSkillTargetBinding:
    """One agent-host target and installation-scope binding."""

    target: str
    scope: SystemSkillScope

    def to_json(self) -> dict[str, str]:
        return {"target": self.target, "scope": self.scope}


@dataclass(frozen=True)
class SystemSkillTarget:
    """One normalized physical system-skill destination."""

    target: str
    skill_root: Path
    scope: SystemSkillScope | None = None
    bindings: tuple[SystemSkillTargetBinding, ...] = ()

    def to_json(self) -> dict[str, object]:
        return {
            "target": self.target,
            "scope": self.scope,
            "skill_root": str(self.skill_root),
            "bindings": [binding.to_json() for binding in self.bindings],
        }


@dataclass(frozen=True)
class InstalledSystemSkillMember:
    """Observed integrity and version state for one protected pack member."""

    logical_id: str
    member_name: str
    relative_path: str
    path: Path
    invocation_designator: str
    skill_version: str | None
    receipt_skill_version: str | None
    minimum_compatible_version: str
    identity_status: str
    compatibility_status: str
    installation_verified: bool

    def to_json(self) -> dict[str, object]:
        return {
            "logical_id": self.logical_id,
            "member_name": self.member_name,
            "relative_path": self.relative_path,
            "path": str(self.path),
            "invocation_designator": self.invocation_designator,
            "skill_version": self.skill_version,
            "receipt_skill_version": self.receipt_skill_version,
            "minimum_compatible_version": self.minimum_compatible_version,
            "identity_status": self.identity_status,
            "compatibility_status": self.compatibility_status,
            "installation_verified": self.installation_verified,
        }


@dataclass(frozen=True)
class InstalledSystemSkillPublic:
    """Observed state for one welcome or entrypoint projection."""

    name: str
    role: str
    path: Path
    source_path: str
    projection_mode: str | None
    skill_version: str | None
    receipt_skill_version: str | None
    minimum_compatible_version: str
    identity_status: str
    compatibility_status: str
    receipt_owned: bool
    installation_verified: bool

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "role": self.role,
            "path": str(self.path),
            "source_path": self.source_path,
            "projection_mode": self.projection_mode,
            "skill_version": self.skill_version,
            "receipt_skill_version": self.receipt_skill_version,
            "minimum_compatible_version": self.minimum_compatible_version,
            "identity_status": self.identity_status,
            "compatibility_status": self.compatibility_status,
            "receipt_owned": self.receipt_owned,
            "installation_verified": self.installation_verified,
        }


@dataclass(frozen=True)
class InstalledSystemSkill:
    """One packaged public-pack projection in a target root."""

    name: str
    pack_id: str | None
    path: Path
    source_path: str | None
    projection_mode: str | None
    skill_version: str | None = None
    receipt_skill_version: str | None = None
    minimum_compatible_version: str | None = None
    compatibility_status: str = "unversioned"
    installation_verified: bool = False
    receipt_owned: bool = False
    pack_status: str = "unverified"
    public_skills: tuple[InstalledSystemSkillPublic, ...] = ()
    protected_members: tuple[InstalledSystemSkillMember, ...] = ()
    missing_protected_members: tuple[str, ...] = ()
    extra_protected_paths: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "pack_id": self.pack_id,
            "path": str(self.path),
            "source_path": self.source_path,
            "projection_mode": self.projection_mode,
            "skill_version": self.skill_version,
            "receipt_skill_version": self.receipt_skill_version,
            "minimum_compatible_version": self.minimum_compatible_version,
            "compatibility_status": self.compatibility_status,
            "installation_verified": self.installation_verified,
            "receipt_owned": self.receipt_owned,
            "pack_status": self.pack_status,
            "public_skills": [skill.to_json() for skill in self.public_skills],
            "protected_members": [member.to_json() for member in self.protected_members],
            "missing_protected_members": list(self.missing_protected_members),
            "extra_protected_paths": list(self.extra_protected_paths),
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
    """Return installable public packs with their protected inventories."""

    records: list[SystemSkillRecord] = []
    seen_names: set[str] = set()
    catalog = system_skill_catalog()
    for pack in iter_system_skill_packs():
        if pack.entry_skill in seen_names:
            raise SystemSkillInstallError(f"Duplicate packaged public pack name: {pack.entry_skill}")
        seen_names.add(pack.entry_skill)
        members: list[SystemSkillMemberRecord] = []
        for capability in catalog.capabilities:
            if capability.pack_id != pack.pack_id:
                continue
            relative_path = PurePosixPath(capability.source_path).relative_to(PurePosixPath(pack.source_path)).as_posix()
            members.append(
                SystemSkillMemberRecord(
                    logical_id=capability.logical_id,
                    member_name=capability.member_name,
                    relative_path=relative_path,
                    source_path=capability.source_path,
                    invocation_designator=capability.invocation_designator,
                    dependencies=capability.dependencies,
                    skill_version=_packaged_skill_version(capability.source_path),
                    minimum_compatible_version=capability.minimum_compatible_version,
                )
            )
        public_skills = tuple(
            SystemSkillPublicRecord(
                name=public.name,
                role=public.role,
                source_path=public.source_path,
                skill_version=_packaged_skill_version(public.source_path),
                minimum_compatible_version=public.minimum_compatible_version,
                description=_read_skill_description(public.source_path),
                public_commands=public.public_commands,
            )
            for public in pack.public_skills
        )
        records.append(
            SystemSkillRecord(
                name=pack.entry_skill,
                pack_id=pack.pack_id,
                source_path=pack.source_path,
                group=pack.pack_id,
                group_kind=pack.kind,
                extension_id=pack.extension_id,
                skill_version=_packaged_skill_version(pack.source_path),
                minimum_compatible_version=pack.minimum_compatible_skill_version,
                description=_read_skill_description(pack.source_path),
                public_commands=pack.public_commands,
                public_skills=public_skills,
                protected_members=tuple(members),
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

    catalog = system_skill_catalog()
    group_records = {pack.pack_id: pack for pack in iter_system_skill_packs()}
    extension_records = {
        pack.extension_id: pack
        for pack in group_records.values()
        if pack.kind == "extension" and pack.extension_id is not None
    }
    skill_records = {record.name: record for record in list_packaged_system_skills()}
    selected_group_names: list[str] = []
    selected_extension_ids: list[str] = []
    selected_skill_names: list[str] = []
    deprecated_selectors: list[DeprecatedSystemSkillSelector] = []

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
        try:
            requested_public = catalog.public_skill_by_name(skill_name)
        except SystemSkillAssetError:
            requested_public = None
        if requested_public is not None:
            public_skill = catalog.pack_for_public_skill(requested_public.name).entry_skill
            selector_kind = f"public_{requested_public.role}"
            deprecated = False
        else:
            try:
                identity_kind, canonical_id, deprecated = normalize_system_skill_identity(skill_name)
            except SystemSkillAssetError as exc:
                raise SystemSkillInstallError(f"Unknown packaged system skill selector {skill_name!r}: {exc}") from exc
            if identity_kind == "pack":
                public_skill = canonical_id
                selector_kind = "legacy_public_alias" if deprecated else "public_pack"
            else:
                capability = catalog.capability_by_logical_id(canonical_id)
                public_skill = catalog.pack_by_id(capability.pack_id).entry_skill
                selector_kind = "protected_logical_id"
                deprecated = True
        selected_skill_names.append(public_skill)
        if deprecated:
            deprecated_selectors.append(
                DeprecatedSystemSkillSelector(
                    requested=skill_name,
                    canonical_public_skill=public_skill,
                    selector_kind=selector_kind,
                )
            )

    has_selector = bool(selected_group_names or selected_extension_ids or selected_skill_names)
    explicit_extension_pack = any(skill_records[name].group_kind == "extension" for name in selected_skill_names)
    if default_core and (not has_selector or selected_extension_ids or all_extensions or explicit_extension_pack):
        selected_group_names.insert(0, "core")

    resolved_names: list[str] = []
    for group_name in dict.fromkeys(selected_group_names):
        resolved_names.append(group_records[group_name].entry_skill)
    for extension_id in dict.fromkeys(selected_extension_ids):
        resolved_names.append(extension_records[extension_id].entry_skill)
    resolved_names.extend(selected_skill_names)

    unique_names = tuple(dict.fromkeys(resolved_names))
    if not unique_names:
        raise SystemSkillInstallError("At least one packaged system skill must be selected.")
    return SystemSkillSelection(
        selected_groups=tuple(dict.fromkeys(selected_group_names)),
        selected_extensions=tuple(dict.fromkeys(selected_extension_ids)),
        explicit_skills=tuple(dict.fromkeys(selected_skill_names)),
        skills=tuple(skill_records[name] for name in unique_names),
        deprecated_selectors=tuple(dict.fromkeys(deprecated_selectors)),
        requested_skills=tuple(dict.fromkeys(skills)),
    )


def resolve_targets(
    target: str,
    *,
    scope: SystemSkillScope,
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
) -> tuple[SystemSkillTarget, ...]:
    """Resolve target and scope selectors to unique physical skill roots."""

    if target not in SUPPORTED_TARGETS:
        supported = ", ".join(SUPPORTED_TARGETS)
        raise SystemSkillInstallError(f"Unsupported system skill target {target!r}. Expected one of: {supported}.")
    if scope not in SUPPORTED_SCOPES:
        supported = ", ".join(SUPPORTED_SCOPES)
        raise SystemSkillInstallError(f"Unsupported system skill scope {scope!r}. Expected one of: {supported}.")

    selected_targets = CONCRETE_TARGETS if target == "all" else (target,)
    grouped: dict[Path, list[SystemSkillTargetBinding]] = {}
    for concrete_target in selected_targets:
        root = _scoped_skill_root(concrete_target, scope=scope, cwd=cwd, env=env).resolve(strict=False)
        grouped.setdefault(root, []).append(SystemSkillTargetBinding(target=concrete_target, scope=scope))

    destinations: list[SystemSkillTarget] = []
    for root, bindings in grouped.items():
        resolved_bindings = tuple(bindings)
        result_target = resolved_bindings[0].target if len(resolved_bindings) == 1 else "all"
        destinations.append(
            SystemSkillTarget(
                target=result_target,
                scope=scope,
                skill_root=root,
                bindings=resolved_bindings,
            )
        )
    return tuple(destinations)


def install_system_skills(
    target: SystemSkillTarget,
    selection: SystemSkillSelection,
    *,
    projection_mode: ProjectionMode = "copy",
    force: bool = False,
) -> SystemSkillInstallResult:
    """Install selected complete public packs into one target skill root."""

    _validate_projection_mode(projection_mode)
    target.skill_root.mkdir(parents=True, exist_ok=True)
    manifest, diagnostics = _read_manifest(target, mutation=True)
    manifest_records = (
        manifest.record_map() if manifest is not None and manifest.schema_version == SKILL_MANIFEST_SCHEMA else {}
    )
    result_diagnostics = [*diagnostics, *_selection_diagnostics(selection)]

    installed: list[InstalledSystemSkill] = []
    preserved_existing: list[ExistingSystemSkillPath] = []
    replaced: list[ExistingSystemSkillPath] = []
    records_to_install: list[SystemSkillRecord] = []
    for record in selection.skills:
        existing_public = [
            ExistingSystemSkillPath(public.name, target.skill_root / public.name, _path_kind(target.skill_root / public.name))
            for public in record.public_skills
            if (target.skill_root / public.name).exists() or (target.skill_root / public.name).is_symlink()
        ]
        if existing_public and not force:
            preserved_existing.extend(existing_public)
            continue
        replaced.extend(existing_public)
        records_to_install.append(record)

    updated_manifest = manifest
    if records_to_install:
        staging_root, staged_paths = _stage_pack_projections(
            target.skill_root,
            records_to_install,
            {
                public.name: projection_mode
                for record in records_to_install
                for public in record.public_skills
            },
        )
        committed: list[tuple[Path, Path | None]] = []
        try:
            backup_root = staging_root / ".backups"
            backup_root.mkdir()
            for record in records_to_install:
                modes = {public.name: projection_mode for public in record.public_skills}
                for public in record.public_skills:
                    destination = target.skill_root / public.name
                    backup_path: Path | None = None
                    if destination.exists() or destination.is_symlink():
                        backup_path = backup_root / public.name
                        destination.rename(backup_path)
                    staged_paths[public.name].rename(destination)
                    committed.append((destination, backup_path))
                receipt_record = _manifest_record_for(record, modes)
                manifest_records[record.name] = receipt_record
                installed.append(
                    _installed_record(
                        record,
                        target.skill_root / record.name,
                        projection_mode,
                        receipt_record,
                    )
                )
            updated_manifest = _write_manifest(target, manifest_records, existing_manifest=manifest)
        except (OSError, SystemSkillInstallError):
            for destination, backup_path in reversed(committed):
                _remove_path(destination)
                if backup_path is not None and (backup_path.exists() or backup_path.is_symlink()):
                    backup_path.rename(destination)
            raise
        finally:
            _remove_path(staging_root)
    return SystemSkillInstallResult(
        target=target,
        selection=selection,
        installed=tuple(installed),
        preserved_existing=tuple(preserved_existing),
        replaced=tuple(replaced),
        projection_mode=projection_mode,
        manifest=updated_manifest,
        diagnostics=tuple(result_diagnostics),
    )


def inspect_system_skills(target: SystemSkillTarget, selection: SystemSkillSelection) -> SystemSkillStatusResult:
    """Inspect selected packaged skill projections for one target skill root."""

    manifest, diagnostics = _read_manifest(target)
    manifest_records = manifest.record_map() if manifest is not None else {}
    installed: list[InstalledSystemSkill] = []
    missing: list[str] = []
    invalid: list[InvalidSystemSkillProjection] = []
    status_diagnostics = [*diagnostics, *_selection_diagnostics(selection)]
    for record in selection.skills:
        any_public = False
        for public in record.public_skills:
            destination = target.skill_root / public.name
            if destination.is_symlink() and not destination.is_dir():
                issue = InvalidSystemSkillProjection(
                    name=public.name,
                    path=destination,
                    path_kind="broken_symlink" if not destination.exists() else "symlink_to_non_directory",
                    message=f"Selected public {public.role} symlink does not resolve to a skill directory.",
                )
                invalid.append(issue)
                status_diagnostics.append(_projection_diagnostic(issue))
                any_public = True
            elif destination.is_dir():
                any_public = True
            elif destination.exists():
                issue = InvalidSystemSkillProjection(
                    name=public.name,
                    path=destination,
                    path_kind=_path_kind(destination),
                    message=f"Selected public {public.role} path is not a directory or symlink projection.",
                )
                invalid.append(issue)
                status_diagnostics.append(_projection_diagnostic(issue))
                any_public = True
            else:
                missing.append(public.name)
        if any_public:
            entrypoint_path = target.skill_root / record.name
            installed.append(
                _installed_record(
                    record,
                    entrypoint_path,
                    _detected_projection_mode(entrypoint_path),
                    manifest_records.get(record.name),
                )
            )
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
    """Remove selected receipt-owned public pack projections as complete units."""

    protected_selectors = [
        selector for selector in selection.deprecated_selectors if selector.selector_kind == "protected_logical_id"
    ]
    if protected_selectors:
        selector = protected_selectors[0]
        raise SystemSkillInstallError(
            f"Cannot uninstall protected member selector {selector.requested!r} independently. "
            f"Select owning public pack {selector.canonical_public_skill!r} explicitly."
        )

    manifest, diagnostics = _read_manifest(target, mutation=True)
    manifest_records = (
        manifest.record_map() if manifest is not None and manifest.schema_version == SKILL_MANIFEST_SCHEMA else {}
    )
    for record in selection.skills:
        tracked = manifest_records.get(record.name)
        tracked_public = {public.name: public for public in tracked.public_skills} if tracked is not None else {}
        for public in record.public_skills:
            destination = target.skill_root / public.name
            if (destination.exists() or destination.is_symlink()) and (
                tracked is None
                or tracked.pack_id != record.pack_id
                or public.name not in tracked_public
            ):
                raise SystemSkillInstallError(
                    f"Refusing to uninstall untracked or legacy-only public {public.role} path: {destination}. "
                    "Run a managed upgrade first."
                )
    removed: list[InstalledSystemSkill] = []
    absent: list[str] = []
    changed_manifest = False
    for record in selection.skills:
        tracked = manifest_records.get(record.name)
        observed = _installed_record(
            record,
            target.skill_root / record.name,
            _detected_projection_mode(target.skill_root / record.name),
            tracked,
        )
        removed_any = False
        for public in record.public_skills:
            destination = target.skill_root / public.name
            if tracked is not None and (destination.exists() or destination.is_symlink()):
                _remove_path(destination)
                removed_any = True
            else:
                absent.append(public.name)
        if removed_any:
            removed.append(
                observed
            )
        if manifest_records.pop(record.name, None) is not None:
            changed_manifest = True

    updated_manifest = manifest
    if removed or changed_manifest:
        target.skill_root.mkdir(parents=True, exist_ok=True)
        updated_manifest = _write_manifest(target, manifest_records, existing_manifest=manifest)
    return SystemSkillUninstallResult(
        target=target,
        selection=selection,
        removed=tuple(removed),
        absent=tuple(absent),
        manifest=updated_manifest,
        diagnostics=tuple([*diagnostics, *_selection_diagnostics(selection)]),
    )


def upgrade_system_skills(
    target: SystemSkillTarget,
    selection: SystemSkillSelection,
    *,
    projection_mode: ProjectionMode | None = None,
) -> SystemSkillUpgradeResult:
    """Stage complete public packs, commit receipt v5, then clean tracked stale paths."""

    if projection_mode is not None:
        _validate_projection_mode(projection_mode)
    target.skill_root.mkdir(parents=True, exist_ok=True)
    manifest, diagnostics = _read_manifest(target, mutation=True)
    result_diagnostics = [*diagnostics, *_selection_diagnostics(selection)]
    current_records = (
        manifest.record_map() if manifest is not None and manifest.schema_version == SKILL_MANIFEST_SCHEMA else {}
    )
    legacy_records = (
        manifest.record_map() if manifest is not None and manifest.schema_version != SKILL_MANIFEST_SCHEMA else {}
    )
    existing_legacy_paths = {
        record.name: record for record in (manifest.legacy_paths if manifest is not None else ())
    }
    selected_public_names = {public.name for record in selection.skills for public in record.public_skills}
    current_public = manifest.public_ownership_map() if manifest is not None and manifest.schema_version == SKILL_MANIFEST_SCHEMA else {}
    tracked_names = set(current_public) | set(legacy_records) | set(existing_legacy_paths)
    for record in selection.skills:
        for public in record.public_skills:
            destination = target.skill_root / public.name
            if (destination.exists() or destination.is_symlink()) and public.name not in tracked_names:
                raise SystemSkillInstallError(
                    f"Upgrade destination conflicts with an untracked path for public {public.role}: {destination}. "
                    "Preserve or relocate that path before retrying."
                )

    modes: dict[str, ProjectionMode] = {}
    for record in selection.skills:
        current_pack = current_records.get(record.name)
        current_pack_public = {
            public.name: public for public in (current_pack.public_skills if current_pack is not None else ())
        }
        for public in record.public_skills:
            prior_public = current_pack_public.get(public.name)
            prior_legacy = legacy_records.get(public.name) or existing_legacy_paths.get(public.name)
            prior_mode = (
                prior_public.projection_mode
                if prior_public is not None
                else prior_legacy.projection_mode if prior_legacy is not None else "copy"
            )
            modes[public.name] = projection_mode or prior_mode

    stale_candidates: dict[str, SystemSkillLegacyPathRecord] = dict(existing_legacy_paths)
    for tracked in current_records.values():
        for tracked_public in tracked.public_skills:
            if tracked_public.name in selected_public_names:
                stale_candidates.pop(tracked_public.name, None)
                continue
            stale_candidates[tracked_public.name] = SystemSkillLegacyPathRecord(
                name=tracked_public.name,
                source_path=tracked_public.source_path,
                projection_mode=tracked_public.projection_mode,
                skill_version=tracked_public.skill_version,
            )
    for tracked in legacy_records.values():
        if tracked.name in selected_public_names:
            stale_candidates.pop(tracked.name, None)
            continue
        stale_candidates[tracked.name] = SystemSkillLegacyPathRecord(
            name=tracked.name,
            source_path=tracked.source_path,
            projection_mode=tracked.projection_mode,
            skill_version=tracked.skill_version,
        )

    known_legacy_names = {capability.logical_id for capability in system_skill_catalog().capabilities}
    known_legacy_names.update(alias for pack in system_skill_catalog().packs for alias in pack.legacy_aliases)
    for name in sorted(known_legacy_names - set(stale_candidates) - selected_public_names):
        path = target.skill_root / name
        if path.exists() or path.is_symlink():
            result_diagnostics.append(
                Diagnostic(
                    code="ISOSKILL014",
                    severity="warning",
                    concept="system-skill-upgrade",
                    path=path,
                    field=name,
                    message="Preserved legacy-looking top-level path because no supported receipt tracks it.",
                )
            )

    staging_root, staged_paths = _stage_pack_projections(target.skill_root, selection.skills, modes)
    committed: list[tuple[Path, Path | None]] = []
    refreshed: list[InstalledSystemSkill] = []
    new_records: dict[str, SystemSkillManifestRecord] = {}
    try:
        backup_root = staging_root / ".backups"
        backup_root.mkdir()
        for record in selection.skills:
            for public in record.public_skills:
                destination = target.skill_root / public.name
                backup_path: Path | None = None
                if destination.exists() or destination.is_symlink():
                    backup_path = backup_root / public.name
                    destination.rename(backup_path)
                staged_paths[public.name].rename(destination)
                committed.append((destination, backup_path))
            receipt_record = _manifest_record_for(record, modes)
            new_records[record.name] = receipt_record
            refreshed.append(
                _installed_record(
                    record,
                    target.skill_root / record.name,
                    modes[record.name],
                    receipt_record,
                )
            )
        try:
            updated_manifest = _write_manifest(
                target,
                new_records,
                existing_manifest=manifest,
                legacy_paths=stale_candidates,
            )
        except (OSError, SystemSkillInstallError):
            for destination, backup_path in reversed(committed):
                _remove_path(destination)
                if backup_path is not None and (backup_path.exists() or backup_path.is_symlink()):
                    backup_path.rename(destination)
            raise

        stale_removed: list[InstalledSystemSkill] = []
        stale_absent: list[str] = []
        stale_retained: list[ExistingSystemSkillPath] = []
        retained_candidates = dict(stale_candidates)
        for name, legacy_path in sorted(stale_candidates.items()):
            destination = target.skill_root / name
            if not destination.exists() and not destination.is_symlink():
                stale_absent.append(name)
                retained_candidates.pop(name, None)
                continue
            try:
                _remove_stale_path(destination)
            except OSError as exc:
                stale_retained.append(ExistingSystemSkillPath(name, destination, _path_kind(destination)))
                result_diagnostics.append(
                    Diagnostic(
                        code="ISOSKILL015",
                        severity="warning",
                        concept="system-skill-upgrade",
                        path=destination,
                        field=name,
                        message=f"Retained receipt-tracked stale path after cleanup failed: {exc}",
                        hint="Repair or remove only this exact retained path, then rerun system-skills upgrade.",
                    )
                )
                continue
            stale_removed.append(
                InstalledSystemSkill(
                    name=name,
                    pack_id=None,
                    path=destination,
                    source_path=legacy_path.source_path,
                    projection_mode=legacy_path.projection_mode,
                )
            )
            retained_candidates.pop(name, None)
        if retained_candidates != stale_candidates:
            try:
                updated_manifest = _write_manifest(
                    target,
                    new_records,
                    existing_manifest=updated_manifest,
                    legacy_paths=retained_candidates,
                )
            except OSError as exc:
                result_diagnostics.append(
                    Diagnostic(
                        code="ISOSKILL015",
                        severity="warning",
                        concept="system-skill-upgrade",
                        path=updated_manifest.path,
                        message=f"Cleanup completed but the receipt could not drop cleared legacy paths: {exc}",
                        hint="Rerun system-skills upgrade to reconcile stale receipt evidence.",
                    )
                )
    finally:
        _remove_path(staging_root)
    return SystemSkillUpgradeResult(
        target=target,
        selection=selection,
        refreshed=tuple(refreshed),
        stale_removed=tuple(stale_removed),
        stale_absent=tuple(stale_absent),
        stale_retained=tuple(stale_retained),
        projection_mode_override=projection_mode,
        manifest=updated_manifest,
        diagnostics=tuple(result_diagnostics),
    )


def _scoped_skill_root(
    target: str,
    *,
    scope: SystemSkillScope,
    cwd: Path | None = None,
    env: Mapping[str, str] | None = None,
) -> Path:
    base = (cwd or Path.cwd()).resolve()
    if scope == "project":
        if target == "claude-code":
            return base / ".claude" / "skills"
        if target in {"codex", "generic"}:
            return base / ".agents" / "skills"
        if target == "kimi-code":
            return base / ".kimi-code" / "skills"
        raise SystemSkillInstallError(f"Unsupported concrete target: {target}")

    effective_env = os.environ if env is None else env
    user_home_value = effective_env.get("HOME", "").strip()
    user_home = Path(user_home_value).expanduser() if user_home_value else Path.home()
    if target == "claude-code":
        claude_config_dir = effective_env.get("CLAUDE_CONFIG_DIR", "").strip()
        config_root = _expand_user_path(claude_config_dir, user_home) if claude_config_dir else user_home / ".claude"
        return config_root / "skills"
    if target == "codex":
        codex_home = effective_env.get("CODEX_HOME", "").strip()
        if codex_home:
            return _expand_user_path(codex_home, user_home) / "skills"
        return user_home / ".codex" / "skills"
    if target == "kimi-code":
        kimi_code_home = effective_env.get("KIMI_CODE_HOME", "").strip()
        config_root = _expand_user_path(kimi_code_home, user_home) if kimi_code_home else user_home / ".kimi-code"
        return config_root / "skills"
    if target == "generic":
        return user_home / ".agents" / "skills"
    raise SystemSkillInstallError(f"Unsupported concrete target: {target}")


def _expand_user_path(value: str, user_home: Path) -> Path:
    if value == "~":
        return user_home
    if value.startswith("~/"):
        return user_home / value[2:]
    return Path(value).expanduser()


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


def _stage_pack_projections(
    skill_root: Path,
    records: Sequence[SystemSkillRecord],
    modes: Mapping[str, ProjectionMode],
) -> tuple[Path, dict[str, Path]]:
    """Project and validate complete packs before changing live destinations."""

    staging_root = Path(tempfile.mkdtemp(prefix=".isomer-system-skills-staging-", dir=skill_root))
    staged_paths: dict[str, Path] = {}
    try:
        for record in records:
            for public in record.public_skills:
                staged = staging_root / public.name
                _project_skill(public.source_path, staged, projection_mode=modes[public.name])
                errors = _public_projection_errors(public, staged)
                if public.role == "entrypoint":
                    errors = (*errors, *_pack_projection_errors(record, staged))
                if errors:
                    raise SystemSkillInstallError(
                        f"Staged public skill {public.name!r} in pack {record.pack_id!r} failed validation: "
                        f"{'; '.join(dict.fromkeys(errors))}"
                    )
                staged_paths[public.name] = staged
    except (OSError, SystemSkillAssetError, SystemSkillInstallError):
        _remove_path(staging_root)
        raise
    return staging_root, staged_paths


def _pack_projection_errors(record: SystemSkillRecord, path: Path) -> tuple[str, ...]:
    errors: list[str] = []
    if not path.is_dir():
        return ("projection is not a directory",)
    if _skill_identity(path) != record.name:
        errors.append(f"entrypoint identity does not match {record.name}")
    pack_version = inspect_skill_version(path)
    if pack_version.status != "valid" or pack_version.raw_version != record.skill_version:
        errors.append(f"entrypoint version does not match {record.skill_version}")
    expected_paths = {member.relative_path for member in record.protected_members}
    for member in record.protected_members:
        member_path = path / member.relative_path
        if _skill_identity(member_path) != member.logical_id:
            errors.append(f"protected member identity is invalid: {member.logical_id}")
            continue
        observation = inspect_skill_version(member_path)
        if observation.status != "valid" or observation.raw_version != member.skill_version:
            errors.append(f"protected member version is invalid: {member.logical_id}")
    subskills_root = path / "subskills"
    observed_paths = {
        child.relative_to(path).as_posix() for child in subskills_root.iterdir()
    } if subskills_root.is_dir() else set()
    for extra in sorted(observed_paths - expected_paths):
        errors.append(f"undeclared protected member path: {extra}")
    return tuple(errors)


def _public_projection_errors(record: SystemSkillPublicRecord, path: Path) -> tuple[str, ...]:
    errors: list[str] = []
    if not path.is_dir():
        return ("projection is not a directory",)
    if _skill_identity(path) != record.name:
        errors.append(f"public {record.role} identity does not match {record.name}")
    observation = inspect_skill_version(path)
    if observation.status != "valid" or observation.raw_version != record.skill_version:
        errors.append(f"public {record.role} version does not match {record.skill_version}")
    if record.role == "welcome" and (path / "subskills").exists():
        errors.append("public welcome must not contain a protected subskills tree")
    return tuple(errors)


def _selection_diagnostics(selection: SystemSkillSelection) -> tuple[Diagnostic, ...]:
    return tuple(
        Diagnostic(
            code="ISOSKILL013",
            severity="warning",
            concept="system-skill-selector",
            field=selector.requested,
            message=(
                f"Selector {selector.requested!r} is deprecated for ordinary installation; "
                f"selected complete public pack {selector.canonical_public_skill!r}."
            ),
        )
        for selector in selection.deprecated_selectors
    )


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


def _remove_stale_path(path: Path) -> None:
    """Remove one exact receipt-tracked stale path after v5 commit."""

    _remove_path(path)


def inspect_system_skill_manifest(target: SystemSkillTarget) -> SystemSkillManifestInspection:
    """Inspect the Isomer receipt in exactly one supplied system-skill root."""

    return inspect_system_skill_receipt(target.skill_root, target.target)


def _read_manifest(
    target: SystemSkillTarget,
    *,
    mutation: bool = False,
) -> tuple[SystemSkillRootManifest | None, tuple[Diagnostic, ...]]:
    inspection = inspect_system_skill_manifest(target)
    if mutation and inspection.status in {"unsupported_schema", "malformed_receipt"}:
        raise SystemSkillInstallError(
            f"Refusing to mutate system skills with {inspection.status} at {inspection.path}. "
            "Repair or preserve the receipt before retrying."
        )
    return inspection.manifest, inspection.diagnostics


def _write_manifest(
    target: SystemSkillTarget,
    records: dict[str, SystemSkillManifestRecord],
    *,
    existing_manifest: SystemSkillRootManifest | None = None,
    legacy_paths: dict[str, SystemSkillLegacyPathRecord] | None = None,
) -> SystemSkillRootManifest:
    bindings = set(existing_manifest.bindings if existing_manifest is not None else ())
    bindings.update(
        SystemSkillManifestBinding(target=binding.target, scope=binding.scope) for binding in target.bindings
    )
    if not bindings:
        raise SystemSkillInstallError("Cannot write a system-skill receipt without a target-scope binding.")
    resolved_legacy_paths = legacy_paths
    if resolved_legacy_paths is None:
        resolved_legacy_paths = {
            record.name: record for record in (existing_manifest.legacy_paths if existing_manifest is not None else ())
        }
        if existing_manifest is not None and existing_manifest.schema_version != SKILL_MANIFEST_SCHEMA:
            for record in existing_manifest.skills:
                if record.name in records:
                    continue
                resolved_legacy_paths[record.name] = SystemSkillLegacyPathRecord(
                    name=record.name,
                    source_path=record.source_path,
                    projection_mode=record.projection_mode,
                    skill_version=record.skill_version,
                )
    catalog_order = [record.name for record in list_packaged_system_skills() if record.name in records]
    ordered_names = [*catalog_order, *sorted(set(records) - set(catalog_order))]
    manifest = SystemSkillRootManifest(
        schema_version=SKILL_MANIFEST_SCHEMA,
        skill_root=target.skill_root,
        package_name="isomer-labs",
        package_version=_package_version(),
        installed_by="isomer-cli",
        updated_at=datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        skills=tuple(records[name] for name in ordered_names),
        bindings=tuple(sorted(bindings)),
        legacy_paths=tuple(resolved_legacy_paths[name] for name in sorted(resolved_legacy_paths)),
    )
    target.skill_root.mkdir(parents=True, exist_ok=True)
    manifest_temp = manifest.path.with_name(f".{manifest.path.name}.staging")
    manifest_temp.write_text(json.dumps(_manifest_file_json(manifest), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_temp.replace(manifest.path)
    return manifest


def _manifest_file_json(manifest: SystemSkillRootManifest) -> dict[str, object]:
    data = manifest.to_json()
    data.pop("path", None)
    data.pop("skill_names", None)
    data.pop("target", None)
    return data


def _manifest_record_for(
    record: SystemSkillRecord, projection_modes: Mapping[str, ProjectionMode]
) -> SystemSkillManifestRecord:
    entrypoint = next(public for public in record.public_skills if public.role == "entrypoint")
    return SystemSkillManifestRecord(
        name=record.name,
        source_path=record.source_path,
        projection_mode=projection_modes[entrypoint.name],
        skill_version=record.skill_version,
        pack_id=record.pack_id,
        entry_skill=record.name,
        package_version=_package_version(),
        public_skills=tuple(
            SystemSkillManifestPublicRecord(
                name=public.name,
                role=public.role,
                source_path=public.source_path,
                projection_mode=projection_modes[public.name],
                skill_version=public.skill_version,
            )
            for public in record.public_skills
        ),
        protected_members=tuple(
            SystemSkillManifestMemberRecord(
                logical_id=member.logical_id,
                relative_path=member.relative_path,
                invocation_designator=member.invocation_designator,
                skill_version=member.skill_version,
            )
            for member in record.protected_members
        ),
    )


def _installed_record(
    record: SystemSkillRecord,
    destination: Path,
    projection_mode: str | None,
    receipt_record: SystemSkillManifestRecord | None = None,
) -> InstalledSystemSkill:
    observation = inspect_skill_version(destination)
    receipt_version = receipt_record.skill_version if receipt_record is not None else None
    pack_receipt_owned = (
        receipt_record is not None
        and receipt_record.pack_id == record.pack_id
        and receipt_record.source_path == record.source_path
        and receipt_record.projection_mode == projection_mode
    )
    receipt_public = {
        public.name: public for public in (receipt_record.public_skills if receipt_record is not None else ())
    }
    installed_public: list[InstalledSystemSkillPublic] = []
    for public in record.public_skills:
        public_path = destination.parent / public.name
        public_observation = inspect_skill_version(public_path)
        public_receipt = receipt_public.get(public.name)
        public_mode = _detected_projection_mode(public_path)
        public_identity = _skill_identity(public_path)
        if not public_path.is_dir():
            identity_status = "missing"
        elif public_identity != public.name:
            identity_status = "identity_mismatch"
        else:
            identity_status = "valid"
        public_owned = (
            pack_receipt_owned
            and public_receipt is not None
            and public_receipt.role == public.role
            and public_receipt.source_path == public.source_path
            and public_receipt.projection_mode == public_mode
        )
        compatibility_status = _public_compatibility_status(public, public_observation, public_receipt)
        public_verified = (
            public_owned
            and identity_status == "valid"
            and public_observation.status == "valid"
            and public_receipt is not None
            and public_receipt.skill_version == public_observation.raw_version
            and compatibility_status in {"current", "compatible_older", "newer_than_cli"}
        )
        installed_public.append(
            InstalledSystemSkillPublic(
                name=public.name,
                role=public.role,
                path=public_path,
                source_path=public.source_path,
                projection_mode=public_mode,
                skill_version=public_observation.raw_version,
                receipt_skill_version=public_receipt.skill_version if public_receipt is not None else None,
                minimum_compatible_version=public.minimum_compatible_version,
                identity_status=identity_status,
                compatibility_status=compatibility_status,
                receipt_owned=public_owned,
                installation_verified=public_verified,
            )
        )
    receipt_owned = pack_receipt_owned and len(receipt_public) == len(record.public_skills) and all(
        public.receipt_owned for public in installed_public
    )
    receipt_members = {
        member.logical_id: member for member in (receipt_record.protected_members if receipt_record is not None else ())
    }
    installed_members: list[InstalledSystemSkillMember] = []
    missing_members: list[str] = []
    expected_relative_paths = {member.relative_path for member in record.protected_members}
    for member in record.protected_members:
        member_path = destination / member.relative_path
        member_observation = inspect_skill_version(member_path)
        identity = _skill_identity(member_path)
        if not member_path.is_dir():
            identity_status = "missing"
            missing_members.append(member.logical_id)
        elif identity != member.logical_id:
            identity_status = "identity_mismatch"
        else:
            identity_status = "valid"
        receipt_member = receipt_members.get(member.logical_id)
        receipt_member_valid = (
            receipt_member is not None
            and receipt_member.relative_path == member.relative_path
            and receipt_member.invocation_designator == member.invocation_designator
        )
        compatibility_status = _member_compatibility_status(member, member_observation, receipt_member)
        member_verified = (
            receipt_owned
            and receipt_member_valid
            and identity_status == "valid"
            and member_observation.status == "valid"
            and receipt_member is not None
            and receipt_member.skill_version == member_observation.raw_version
            and compatibility_status in {"current", "compatible_older", "newer_than_cli"}
        )
        installed_members.append(
            InstalledSystemSkillMember(
                logical_id=member.logical_id,
                member_name=member.member_name,
                relative_path=member.relative_path,
                path=member_path,
                invocation_designator=member.invocation_designator,
                skill_version=member_observation.raw_version,
                receipt_skill_version=receipt_member.skill_version if receipt_member is not None else None,
                minimum_compatible_version=member.minimum_compatible_version,
                identity_status=identity_status,
                compatibility_status=compatibility_status,
                installation_verified=member_verified,
            )
        )
    subskills_root = destination / "subskills"
    observed_relative_paths = {
        path.relative_to(destination).as_posix()
        for path in subskills_root.iterdir()
    } if subskills_root.is_dir() else set()
    extra_paths = tuple(sorted(observed_relative_paths - expected_relative_paths))
    pack_compatibility = _skill_compatibility_status(record, observation.raw_version, observation.status, receipt_record)
    pack_identity_valid = _skill_identity(destination) == record.name
    pack_verified = (
        receipt_owned
        and pack_identity_valid
        and observation.status == "valid"
        and receipt_version == observation.raw_version
        and not missing_members
        and not extra_paths
        and all(member.installation_verified for member in installed_members)
        and all(public.installation_verified for public in installed_public)
    )
    if missing_members or extra_paths or not pack_identity_valid or any(
        member.identity_status != "valid" for member in installed_members
    ) or any(public.identity_status != "valid" for public in installed_public):
        pack_status = "incomplete"
    elif not receipt_owned:
        pack_status = "unmanaged" if receipt_record is None else "receipt_mismatch"
    elif pack_verified:
        pack_status = "verified"
    else:
        pack_status = "version_or_receipt_drift"
    return InstalledSystemSkill(
        name=record.name,
        pack_id=record.pack_id,
        path=destination,
        source_path=record.source_path,
        projection_mode=projection_mode,
        skill_version=observation.raw_version,
        receipt_skill_version=receipt_version,
        minimum_compatible_version=record.minimum_compatible_version,
        compatibility_status=pack_compatibility,
        installation_verified=pack_verified,
        receipt_owned=receipt_owned,
        pack_status=pack_status,
        public_skills=tuple(installed_public),
        protected_members=tuple(installed_members),
        missing_protected_members=tuple(missing_members),
        extra_protected_paths=extra_paths,
    )


def _public_compatibility_status(
    record: SystemSkillPublicRecord,
    observation: object,
    receipt_record: SystemSkillManifestPublicRecord | None,
) -> str:
    metadata_status = getattr(observation, "status", "invalid")
    observed_version = getattr(observation, "raw_version", None)
    if metadata_status != "valid" or not isinstance(observed_version, str):
        return str(metadata_status)
    if receipt_record is None:
        return "unversioned"
    if receipt_record.skill_version != observed_version:
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


def _member_compatibility_status(
    record: SystemSkillMemberRecord,
    observation: object,
    receipt_record: SystemSkillManifestMemberRecord | None,
) -> str:
    metadata_status = getattr(observation, "status", "invalid")
    observed_version = getattr(observation, "raw_version", None)
    if metadata_status != "valid" or not isinstance(observed_version, str):
        return str(metadata_status)
    if receipt_record is None:
        return "unversioned"
    if receipt_record.skill_version != observed_version:
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


def _skill_identity(skill_path: Path) -> str | None:
    skill_md = skill_path / "SKILL.md"
    try:
        text = skill_md.read_text(encoding="utf-8")
    except OSError:
        return None
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    for line in parts[1].splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip('"\'')
    return None


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
