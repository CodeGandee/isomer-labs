"""Package-resource helpers for official Isomer system-skill packs."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from functools import lru_cache
from importlib import resources
from importlib.resources.abc import Traversable
from pathlib import Path, PurePosixPath
import re
from typing import Any, Sequence

from packaging.version import InvalidVersion, Version
import tomlkit


SYSTEM_SKILLS_RESOURCE = "assets/system_skills"
SYSTEM_SKILL_MANIFEST_V2 = "isomer-skillset-manifest.v2"
SYSTEM_SKILL_MANIFEST_V3 = "isomer-skillset-manifest.v3"
SYSTEM_SKILL_MANIFEST_V4 = "isomer-skillset-manifest.v4"
SYSTEM_SKILL_GROUP_KINDS = ("core", "extension")
SYSTEM_SKILL_PUBLIC_ROLES = ("welcome", "entrypoint")
SYSTEM_EXTENSION_ID_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SYSTEM_EXTENSION_ENTRYPOINT_RE = re.compile(r"^isomer-ext-([a-z0-9][a-z0-9-]*)-entrypoint$")
SYSTEM_EXTENSION_WELCOME_RE = re.compile(r"^isomer-ext-([a-z0-9][a-z0-9-]*)-welcome$")
SYSTEM_EXTENSION_COMMAND_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SYSTEM_SKILL_MEMBER_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
SYSTEM_SKILL_AREA_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


class SystemSkillAssetError(ValueError):
    """Raised when packaged system-skill assets are invalid or unavailable."""


@dataclass(frozen=True)
class SystemSkillPublicSkill:
    """One public welcome or execution entrypoint in a complete pack."""

    name: str
    pack_id: str
    role: str
    source_path: str
    public_commands: tuple[str, ...] = ()
    legacy_aliases: tuple[str, ...] = ()
    callback_insertion_points: tuple[str, ...] = ()
    minimum_compatible_version: str = ""

    def to_json(self) -> dict[str, object]:
        return {
            "name": self.name,
            "pack_id": self.pack_id,
            "role": self.role,
            "source_path": self.source_path,
            "public_commands": list(self.public_commands),
            "legacy_aliases": list(self.legacy_aliases),
            "callback_insertion_points": list(self.callback_insertion_points),
            "minimum_compatible_version": self.minimum_compatible_version,
        }


@dataclass(frozen=True)
class SystemSkillPack:
    """One atomically installed system-skill pack with ordered public roles."""

    pack_id: str
    description: str
    kind: str
    entry_skill: str
    always_available: bool
    minimum_compatible_skill_version: str
    public_skills: tuple[SystemSkillPublicSkill, ...]
    extension_id: str | None = None
    protected_members: tuple[str, ...] = ()

    @property
    def entrypoint(self) -> SystemSkillPublicSkill:
        """Return the designated execution entrypoint record."""

        for public_skill in self.public_skills:
            if public_skill.name == self.entry_skill:
                return public_skill
        raise SystemSkillAssetError(f"Pack {self.pack_id!r} has no entrypoint record for {self.entry_skill!r}.")

    @property
    def welcome(self) -> SystemSkillPublicSkill | None:
        """Return the independent welcome record when declared."""

        return next((skill for skill in self.public_skills if skill.role == "welcome"), None)

    @property
    def source_path(self) -> str:
        """Return the entrypoint source path for compatibility callers."""

        return self.entrypoint.source_path

    @property
    def public_commands(self) -> tuple[str, ...]:
        """Return the entrypoint command inventory for compatibility callers."""

        return self.entrypoint.public_commands

    @property
    def legacy_aliases(self) -> tuple[str, ...]:
        """Return entrypoint aliases for compatibility lookup."""

        return self.entrypoint.legacy_aliases

    @property
    def callback_insertion_points(self) -> tuple[str, ...]:
        """Return entrypoint callback stages for compatibility callers."""

        return self.entrypoint.callback_insertion_points


@dataclass(frozen=True)
class SystemSkillCapability:
    """One stable protected capability nested below a public pack."""

    logical_id: str
    pack_id: str
    area: str
    member_name: str
    source_path: str
    invocation_designator: str
    dependencies: tuple[str, ...]
    legacy_aliases: tuple[str, ...]
    callback_insertion_points: tuple[str, ...]
    minimum_compatible_version: str


@dataclass(frozen=True)
class SystemSkillPrivateProjection:
    """Catalog-owned source metadata for one protected private projection."""

    logical_id: str
    pack_id: str
    public_skill: str
    source_path: str
    projected_path: str
    invocation_designator: str
    dependencies: tuple[str, ...]
    minimum_compatible_version: str


@dataclass(frozen=True)
class SystemSkillGroup:
    """Compatibility view of one manifest-defined pack or legacy flat group."""

    name: str
    description: str
    skills: tuple[str, ...]
    kind: str
    always_available: bool
    minimum_compatible_skill_version: str
    extension_id: str | None = None
    entry_skill: str | None = None
    commands: tuple[str, ...] = ()
    protected_members: tuple[str, ...] = ()
    legacy_aliases: tuple[str, ...] = ()


@dataclass(frozen=True)
class SystemSkillExtension:
    """Manifest-defined optional system-skill extension pack."""

    extension_id: str
    group: str
    description: str
    skills: tuple[str, ...]
    entry_skill: str
    commands: tuple[str, ...]
    minimum_compatible_skill_version: str
    protected_members: tuple[str, ...] = ()
    source_path: str = ""
    legacy_aliases: tuple[str, ...] = ()
    public_skills: tuple[SystemSkillPublicSkill, ...] = ()


@dataclass(frozen=True)
class SystemSkillCatalogMetadata:
    """Package-owned callback and compatibility metadata for one skill bundle."""

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
    """Manifest-defined callback insertion point for one packaged capability."""

    target_skill: str
    skill_path: str
    group: str
    group_kind: str
    extension_id: str | None
    stage: str
    stage_label: str
    description: str
    pack_id: str
    public_skill: str
    public_role: str
    member_name: str | None
    invocation_designator: str


@dataclass(frozen=True)
class SystemSkillMaterializationResult:
    """Result from copying packaged system-skill packs to a target directory."""

    target: Path
    groups: tuple[str, ...]
    copied_paths: tuple[Path, ...]


@dataclass(frozen=True)
class SystemSkillPrivateProjectionMaterializationResult:
    """Result from projecting dependency-closed protected bundles as flat siblings."""

    target: Path
    projections: tuple[SystemSkillPrivateProjection, ...]
    copied_paths: tuple[Path, ...]


@dataclass(frozen=True)
class SystemSkillCatalog:
    """Parsed public-pack and protected-capability catalog."""

    schema_version: str
    packs: tuple[SystemSkillPack, ...] = ()
    capabilities: tuple[SystemSkillCapability, ...] = ()
    legacy_groups: tuple[SystemSkillGroup, ...] = ()

    @property
    def is_legacy(self) -> bool:
        """Return whether this is a read-only flat-manifest catalog."""

        return self.schema_version == SYSTEM_SKILL_MANIFEST_V2

    def pack_by_id(self, pack_id: str) -> SystemSkillPack:
        """Return a pack by stable pack id."""

        for pack in self.packs:
            if pack.pack_id == pack_id:
                return pack
        raise SystemSkillAssetError(f"Unknown system-skill pack id: {pack_id}")

    def pack_for_public_skill(self, public_skill: str) -> SystemSkillPack:
        """Return a pack by either canonical public skill name."""

        for pack in self.packs:
            if any(skill.name == public_skill for skill in pack.public_skills):
                return pack
        raise SystemSkillAssetError(f"Unknown public system-skill pack: {public_skill}")

    def public_skill_by_name(self, public_skill: str) -> SystemSkillPublicSkill:
        """Return one public role record by canonical name."""

        for pack in self.packs:
            for record in pack.public_skills:
                if record.name == public_skill:
                    return record
        raise SystemSkillAssetError(f"Unknown public system skill: {public_skill}")

    def pack_for_extension(self, extension_id: str) -> SystemSkillPack:
        """Return an optional pack by extension id."""

        for pack in self.packs:
            if pack.extension_id == extension_id:
                return pack
        raise SystemSkillAssetError(f"Unknown packaged system extension: {extension_id}")

    def capability_by_logical_id(self, logical_id: str) -> SystemSkillCapability:
        """Return a protected capability by stable logical id."""

        for capability in self.capabilities:
            if capability.logical_id == logical_id:
                return capability
        raise SystemSkillAssetError(f"Unknown protected system-skill logical id: {logical_id}")

    def capability_for_member(self, pack_id: str, member_name: str) -> SystemSkillCapability:
        """Return a protected capability by pack-scoped member name."""

        for capability in self.capabilities:
            if capability.pack_id == pack_id and capability.member_name == member_name:
                return capability
        raise SystemSkillAssetError(f"Unknown protected member {member_name!r} for pack {pack_id!r}.")

    def capability_for_invocation(self, invocation_designator: str) -> SystemSkillCapability:
        """Return a protected capability by canonical parent-owned designator."""

        for capability in self.capabilities:
            if capability.invocation_designator == invocation_designator:
                return capability
        raise SystemSkillAssetError(f"Unknown protected invocation designator: {invocation_designator}")

    def normalize_identity(self, identifier: str) -> tuple[str, str, bool]:
        """Return ``(kind, canonical_id, deprecated)`` for a catalog identifier."""

        for pack in self.packs:
            if identifier in {pack.pack_id, pack.extension_id}:
                return ("pack", pack.entry_skill, False)
            for public_skill in pack.public_skills:
                if identifier == public_skill.name:
                    return ("pack", pack.entry_skill, False)
                if identifier in public_skill.legacy_aliases:
                    return ("pack", pack.entry_skill, True)
        for capability in self.capabilities:
            if identifier == capability.logical_id:
                return ("capability", capability.logical_id, False)
            if identifier == capability.invocation_designator:
                return ("capability", capability.logical_id, False)
            if identifier in capability.legacy_aliases:
                return ("capability", capability.logical_id, True)
        raise SystemSkillAssetError(f"Unknown system-skill catalog identifier: {identifier}")

    def dependency_closure(self, logical_ids: Sequence[str]) -> tuple[SystemSkillCapability, ...]:
        """Resolve dependencies before dependents in deterministic request order."""

        ordered: list[SystemSkillCapability] = []
        visited: set[str] = set()

        def visit(logical_id: str) -> None:
            if logical_id in visited:
                return
            capability = self.capability_by_logical_id(logical_id)
            for dependency in capability.dependencies:
                visit(dependency)
            visited.add(logical_id)
            ordered.append(capability)

        for logical_id in dict.fromkeys(logical_ids):
            visit(logical_id)
        return tuple(ordered)

    def private_projection(self, logical_ids: Sequence[str]) -> tuple[SystemSkillPrivateProjection, ...]:
        """Return dependency-closed private-projection source metadata."""

        projections: list[SystemSkillPrivateProjection] = []
        for capability in self.dependency_closure(logical_ids):
            pack = self.pack_by_id(capability.pack_id)
            projections.append(
                SystemSkillPrivateProjection(
                    logical_id=capability.logical_id,
                    pack_id=pack.pack_id,
                    public_skill=pack.entry_skill,
                    source_path=capability.source_path,
                    projected_path=capability.logical_id,
                    invocation_designator=capability.invocation_designator,
                    dependencies=capability.dependencies,
                    minimum_compatible_version=capability.minimum_compatible_version,
                )
            )
        return tuple(projections)


def system_skills_root() -> Traversable:
    """Return the package resource root for official system skills."""

    root = resources.files("isomer_labs").joinpath(SYSTEM_SKILLS_RESOURCE)
    if not root.is_dir():
        raise SystemSkillAssetError(f"Packaged system-skill root is missing: {SYSTEM_SKILLS_RESOURCE}")
    return root


@lru_cache(maxsize=1)
def _load_system_skill_manifest_cached() -> dict[str, Any]:
    """Parse the process-immutable packaged system-skill manifest once."""

    manifest = system_skills_root().joinpath("manifest.toml")
    if not manifest.is_file():
        raise SystemSkillAssetError("Packaged system-skill manifest is missing.")
    parsed = tomlkit.parse(manifest.read_text(encoding="utf-8"))
    return dict(parsed)


def load_system_skill_manifest() -> dict[str, Any]:
    """Load an isolated copy of the packaged system-skill manifest."""

    return deepcopy(_load_system_skill_manifest_cached())


def parse_system_skill_manifest(manifest: dict[str, Any]) -> SystemSkillCatalog:
    """Parse the current catalog or a supported read-only legacy manifest."""

    schema_version = manifest.get("schema_version")
    if schema_version == SYSTEM_SKILL_MANIFEST_V2:
        return SystemSkillCatalog(
            schema_version=SYSTEM_SKILL_MANIFEST_V2,
            legacy_groups=_parse_legacy_system_skill_groups(manifest),
        )
    if schema_version not in {SYSTEM_SKILL_MANIFEST_V3, SYSTEM_SKILL_MANIFEST_V4}:
        raise SystemSkillAssetError(f"Unsupported packaged system-skill manifest schema: {schema_version!r}")
    stages = {stage.stage for stage in _parse_callback_stages(manifest)}
    packs = (
        _parse_system_skill_packs_v4(manifest, stages)
        if schema_version == SYSTEM_SKILL_MANIFEST_V4
        else _parse_system_skill_packs_v3(manifest, stages)
    )
    _require_unique((pack.pack_id for pack in packs), "pack ids")
    _require_unique((skill.name for pack in packs for skill in pack.public_skills), "public skill names")
    _require_unique((skill.source_path for pack in packs for skill in pack.public_skills), "public skill source paths")
    _require_unique((pack.extension_id for pack in packs if pack.extension_id is not None), "extension ids")
    capabilities = _parse_system_skill_capabilities(manifest, packs, stages)
    _validate_catalog_identities(packs, capabilities)
    _validate_capability_dependencies(capabilities)
    return SystemSkillCatalog(
        schema_version=str(schema_version),
        packs=packs,
        capabilities=capabilities,
    )


@lru_cache(maxsize=1)
def system_skill_catalog() -> SystemSkillCatalog:
    """Return the immutable packaged system-skill catalog for this process."""

    catalog = parse_system_skill_manifest(_load_system_skill_manifest_cached())
    if catalog.is_legacy:
        raise SystemSkillAssetError("The packaged system-skill manifest must use the current pack schema.")
    if catalog.schema_version != SYSTEM_SKILL_MANIFEST_V4:
        raise SystemSkillAssetError("The packaged system-skill manifest must use schema v4.")
    return catalog


def iter_system_skill_packs() -> tuple[SystemSkillPack, ...]:
    """Return manifest-defined public packs."""

    return parse_system_skill_manifest(load_system_skill_manifest()).packs


def iter_system_skill_capabilities(pack_id: str | None = None) -> tuple[SystemSkillCapability, ...]:
    """Return protected capabilities, optionally filtered by owning pack."""

    capabilities = parse_system_skill_manifest(load_system_skill_manifest()).capabilities
    if pack_id is None:
        return capabilities
    return tuple(capability for capability in capabilities if capability.pack_id == pack_id)


def iter_system_skill_groups() -> tuple[SystemSkillGroup, ...]:
    """Return compatibility group views for current packs or legacy fixtures."""

    return _parse_system_skill_groups(load_system_skill_manifest())


def iter_system_skill_extensions() -> tuple[SystemSkillExtension, ...]:
    """Return manifest-defined optional system-skill extension packs."""

    extensions: list[SystemSkillExtension] = []
    catalog = parse_system_skill_manifest(load_system_skill_manifest())
    if catalog.is_legacy:
        for group in catalog.legacy_groups:
            if group.kind != "extension" or group.extension_id is None or group.entry_skill is None:
                continue
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
    for pack in catalog.packs:
        if pack.kind != "extension" or pack.extension_id is None:
            continue
        extensions.append(
            SystemSkillExtension(
                extension_id=pack.extension_id,
                group=pack.pack_id,
                description=pack.description,
                skills=tuple(skill.source_path for skill in pack.public_skills),
                entry_skill=pack.entry_skill,
                commands=pack.public_commands,
                minimum_compatible_skill_version=pack.minimum_compatible_skill_version,
                protected_members=pack.protected_members,
                source_path=pack.source_path,
                legacy_aliases=pack.legacy_aliases,
                public_skills=pack.public_skills,
            )
        )
    return tuple(extensions)


def lookup_system_skill_pack(identifier: str) -> SystemSkillPack:
    """Look up a pack by pack id, public name, extension id, or legacy alias."""

    catalog = system_skill_catalog()
    kind, canonical_id, _deprecated = catalog.normalize_identity(identifier)
    if kind != "pack":
        raise SystemSkillAssetError(f"System-skill identifier is protected, not a public pack: {identifier}")
    return catalog.pack_for_public_skill(canonical_id)


def lookup_system_skill_capability(identifier: str, *, pack_id: str | None = None) -> SystemSkillCapability:
    """Look up a capability by logical id, invocation, alias, or scoped member."""

    catalog = system_skill_catalog()
    if pack_id is not None and SYSTEM_SKILL_MEMBER_RE.fullmatch(identifier):
        return catalog.capability_for_member(pack_id, identifier)
    kind, canonical_id, _deprecated = catalog.normalize_identity(identifier)
    if kind != "capability":
        raise SystemSkillAssetError(f"System-skill identifier is public, not protected: {identifier}")
    return catalog.capability_by_logical_id(canonical_id)


def normalize_system_skill_identity(identifier: str) -> tuple[str, str, bool]:
    """Normalize a public, protected, scoped, invocation, or alias identity."""

    return system_skill_catalog().normalize_identity(identifier)


def resolve_system_skill_dependency_closure(logical_ids: Sequence[str]) -> tuple[SystemSkillCapability, ...]:
    """Return deterministic protected dependency closure."""

    return system_skill_catalog().dependency_closure(logical_ids)


def resolve_system_skill_private_projection(logical_ids: Sequence[str]) -> tuple[SystemSkillPrivateProjection, ...]:
    """Return dependency-closed protected private-projection metadata."""

    return system_skill_catalog().private_projection(logical_ids)


def resolve_system_skill_binding_projection(identifiers: Sequence[str]) -> tuple[SystemSkillPrivateProjection, ...]:
    """Resolve provider-neutral protected binding identities through the catalog."""

    catalog = system_skill_catalog()
    logical_ids: list[str] = []
    for identifier in identifiers:
        kind, canonical_id, _deprecated = catalog.normalize_identity(identifier)
        if kind != "capability":
            raise SystemSkillAssetError(
                f"Skill Binding Projection must reference a protected logical id, not public pack {identifier!r}."
            )
        logical_ids.append(canonical_id)
    return catalog.private_projection(tuple(logical_ids))


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

    requested_extensions = tuple(dict.fromkeys(extension_ids or ()))
    if include_all_extensions and requested_extensions:
        raise SystemSkillAssetError("Cannot combine include_all_extensions with explicit extension ids.")
    catalog = system_skill_catalog()
    for extension_id in requested_extensions:
        catalog.pack_for_extension(extension_id)
    canonical_skill = skill
    if skill is not None:
        try:
            canonical_skill = catalog.public_skill_by_name(skill).name
        except SystemSkillAssetError:
            _kind, canonical_skill, _deprecated = catalog.normalize_identity(skill)
    selected: list[CallbackInsertionPoint] = []
    for point in _all_system_skill_callback_insertion_points():
        include_point = point.group_kind == "core" and include_core
        if point.group_kind == "extension":
            include_point = include_all_extensions or point.extension_id in requested_extensions
        if not include_point:
            continue
        if canonical_skill is not None and point.target_skill != canonical_skill:
            continue
        if stage is not None and point.stage != stage:
            continue
        selected.append(point)
    return tuple(selected)


@lru_cache(maxsize=1)
def _all_system_skill_callback_insertion_points() -> tuple[CallbackInsertionPoint, ...]:
    """Return the immutable callback insertion-point catalog for this process."""

    manifest = _load_system_skill_manifest_cached()
    catalog = parse_system_skill_manifest(manifest)
    if catalog.is_legacy:
        return _legacy_callback_insertion_points(manifest, catalog.legacy_groups)
    stages = {item.stage: item for item in _parse_callback_stages(manifest)}
    points: list[CallbackInsertionPoint] = []
    seen_targets: set[tuple[str, str]] = set()
    for pack in catalog.packs:
        targets: list[tuple[str, str, str, str | None, str, tuple[str, ...]]] = [
            (
                public_skill.name,
                public_skill.source_path,
                public_skill.role,
                None,
                public_skill.name,
                public_skill.callback_insertion_points,
            )
            for public_skill in pack.public_skills
        ]
        targets.extend(
            (
                capability.logical_id,
                capability.source_path,
                "protected",
                capability.member_name,
                capability.invocation_designator,
                capability.callback_insertion_points,
            )
            for capability in catalog.capabilities
            if capability.pack_id == pack.pack_id
        )
        for target_skill, skill_path, public_role, member_name, invocation_designator, target_stages in targets:
            for point_stage in target_stages:
                key = (target_skill, point_stage)
                if key in seen_targets:
                    raise SystemSkillAssetError(f"Duplicate callback insertion point target: {target_skill}/{point_stage}")
                seen_targets.add(key)
                stage_metadata = stages[point_stage]
                points.append(
                    CallbackInsertionPoint(
                        target_skill=target_skill,
                        skill_path=skill_path,
                        group=pack.pack_id,
                        group_kind=pack.kind,
                        extension_id=pack.extension_id,
                        stage=point_stage,
                        stage_label=stage_metadata.label,
                        description=stage_metadata.description,
                        pack_id=pack.pack_id,
                        public_skill=pack.entry_skill,
                        public_role=public_role,
                        member_name=member_name,
                        invocation_designator=invocation_designator,
                    )
                )
    return tuple(points)


def _legacy_callback_insertion_points(
    manifest: dict[str, Any], groups: tuple[SystemSkillGroup, ...]
) -> tuple[CallbackInsertionPoint, ...]:
    stages = {item.stage: item for item in _parse_callback_stages(manifest)}
    metadata = _parse_legacy_skill_metadata(manifest, groups)
    points: list[CallbackInsertionPoint] = []
    for group in groups:
        for skill_path in group.skills:
            target_skill = PurePosixPath(skill_path).name
            for point_stage in metadata.get(skill_path, SystemSkillCatalogMetadata()).callback_insertion_points:
                stage_metadata = stages[point_stage]
                points.append(
                    CallbackInsertionPoint(
                        target_skill=target_skill,
                        skill_path=skill_path,
                        group=group.name,
                        group_kind=group.kind,
                        extension_id=group.extension_id,
                        stage=point_stage,
                        stage_label=stage_metadata.label,
                        description=stage_metadata.description,
                        pack_id=group.name,
                        public_skill=group.entry_skill or target_skill,
                        public_role="entrypoint",
                        member_name=None,
                        invocation_designator=target_skill,
                    )
                )
    return tuple(points)


@lru_cache(maxsize=1)
def _system_skill_callback_insertion_point_keys() -> frozenset[tuple[str, str]]:
    """Return constant-time canonical lookup keys for callback validation."""

    return frozenset((point.target_skill, point.stage) for point in _all_system_skill_callback_insertion_points())


def has_system_skill_callback_insertion_point(skill: str | None, stage: str | None) -> bool:
    """Return whether the packaged catalog declares a callback insertion point."""

    if not skill or not stage:
        return False
    try:
        catalog = system_skill_catalog()
        try:
            canonical = catalog.public_skill_by_name(skill).name
        except SystemSkillAssetError:
            _kind, canonical, _deprecated = catalog.normalize_identity(skill)
    except SystemSkillAssetError:
        return False
    return (canonical, stage) in _system_skill_callback_insertion_point_keys()


def callback_insertion_point_stage_names() -> tuple[str, ...]:
    """Return manifest-defined callback insertion point stage ids."""

    return tuple(stage.stage for stage in callback_insertion_point_stages())


def _parse_system_skill_groups(manifest: dict[str, Any]) -> tuple[SystemSkillGroup, ...]:
    catalog = parse_system_skill_manifest(manifest)
    if catalog.is_legacy:
        return catalog.legacy_groups
    return tuple(
        SystemSkillGroup(
            name=pack.pack_id,
            description=pack.description,
            skills=tuple(skill.source_path for skill in pack.public_skills),
            kind=pack.kind,
            always_available=pack.always_available,
            minimum_compatible_skill_version=pack.minimum_compatible_skill_version,
            extension_id=pack.extension_id,
            entry_skill=pack.entry_skill,
            commands=pack.public_commands,
            protected_members=pack.protected_members,
            legacy_aliases=pack.legacy_aliases,
        )
        for pack in catalog.packs
    )


def _parse_system_skill_packs_v3(
    manifest: dict[str, Any], callback_stages: set[str]
) -> tuple[SystemSkillPack, ...]:
    raw_packs = manifest.get("packs")
    if not isinstance(raw_packs, list) or not raw_packs:
        raise SystemSkillAssetError("Packaged system-skill manifest v3 must define a non-empty [[packs]] list.")
    packs: list[SystemSkillPack] = []
    for index, value in enumerate(raw_packs):
        if not isinstance(value, dict):
            raise SystemSkillAssetError(f"System-skill pack at index {index} must be a table.")
        field = f"System-skill pack at index {index}"
        pack_id = _required_identifier(value.get("pack_id"), f"{field} pack_id", SYSTEM_SKILL_MEMBER_RE)
        description = _required_string(value.get("description"), f"{field} description")
        kind = value.get("kind")
        if kind not in SYSTEM_SKILL_GROUP_KINDS:
            raise SystemSkillAssetError(f"{field} must define kind as core or extension.")
        source_path = _normalize_relative_path(_required_string(value.get("source_path"), f"{field} source_path"))
        entry_skill = _required_string(value.get("entry_skill"), f"{field} entry_skill")
        if PurePosixPath(source_path).name != entry_skill:
            raise SystemSkillAssetError(f"Pack {pack_id!r} source_path must end with entry_skill {entry_skill!r}.")
        always_available = value.get("always_available")
        if not isinstance(always_available, bool):
            raise SystemSkillAssetError(f"Pack {pack_id!r} must define boolean always_available.")
        extension_id = value.get("extension_id")
        if kind == "core":
            if extension_id is not None:
                raise SystemSkillAssetError(f"Core system-skill pack {pack_id!r} must not define extension_id.")
            if not always_available:
                raise SystemSkillAssetError(f"Core system-skill pack {pack_id!r} must be always_available.")
        else:
            extension_id = _required_identifier(extension_id, f"Pack {pack_id!r} extension_id", SYSTEM_EXTENSION_ID_RE)
            match = SYSTEM_EXTENSION_ENTRYPOINT_RE.fullmatch(entry_skill)
            if match is None or match.group(1) != extension_id:
                raise SystemSkillAssetError(
                    f"Extension pack {pack_id!r} entry_skill must be isomer-ext-{extension_id}-entrypoint."
                )
            if always_available:
                raise SystemSkillAssetError(f"Extension system-skill pack {pack_id!r} must not be always_available.")
        public_commands = _string_list(value.get("public_commands", ()), f"Pack {pack_id!r} public_commands")
        if any(SYSTEM_EXTENSION_COMMAND_RE.fullmatch(command) is None for command in public_commands):
            raise SystemSkillAssetError(f"Pack {pack_id!r} public_commands contains an invalid command id.")
        if len(public_commands) != len(set(public_commands)):
            raise SystemSkillAssetError(f"Pack {pack_id!r} must not define duplicate public commands.")
        protected_members = _string_list(value.get("protected_members", ()), f"Pack {pack_id!r} protected_members")
        legacy_aliases = _string_list(value.get("legacy_aliases", ()), f"Pack {pack_id!r} legacy_aliases")
        points = _string_list(value.get("callback_insertion_points", ()), f"Pack {pack_id!r} callback insertion points")
        _validate_callback_stages(points, callback_stages, f"pack {pack_id!r}")
        packs.append(
            SystemSkillPack(
                pack_id=pack_id,
                description=description,
                kind=str(kind),
                entry_skill=entry_skill,
                always_available=always_available,
                minimum_compatible_skill_version=_required_pep440_version(
                    value.get("minimum_compatible_skill_version"),
                    f"Pack {pack_id!r} minimum_compatible_skill_version",
                ),
                public_skills=(
                    SystemSkillPublicSkill(
                        name=entry_skill,
                        pack_id=pack_id,
                        role="entrypoint",
                        source_path=source_path,
                        public_commands=public_commands,
                        legacy_aliases=legacy_aliases,
                        callback_insertion_points=points,
                        minimum_compatible_version=_required_pep440_version(
                            value.get("minimum_compatible_skill_version"),
                            f"Pack {pack_id!r} minimum_compatible_skill_version",
                        ),
                    ),
                ),
                extension_id=str(extension_id) if isinstance(extension_id, str) else None,
                protected_members=protected_members,
            )
        )
    return tuple(packs)


def _parse_system_skill_packs_v4(
    manifest: dict[str, Any], callback_stages: set[str]
) -> tuple[SystemSkillPack, ...]:
    raw_packs = manifest.get("packs")
    raw_public_skills = manifest.get("public_skills")
    if not isinstance(raw_packs, list) or not raw_packs:
        raise SystemSkillAssetError("Packaged system-skill manifest v4 must define a non-empty [[packs]] list.")
    if not isinstance(raw_public_skills, list) or not raw_public_skills:
        raise SystemSkillAssetError("Packaged system-skill manifest v4 must define a non-empty [[public_skills]] list.")

    raw_pack_map: dict[str, dict[str, Any]] = {}
    for index, value in enumerate(raw_packs):
        if not isinstance(value, dict):
            raise SystemSkillAssetError(f"System-skill pack at index {index} must be a table.")
        pack_id = _required_identifier(value.get("pack_id"), f"System-skill pack at index {index} pack_id", SYSTEM_SKILL_MEMBER_RE)
        if pack_id in raw_pack_map:
            raise SystemSkillAssetError(f"Duplicate pack ids: {pack_id}")
        raw_pack_map[pack_id] = value

    public_by_pack: dict[str, list[SystemSkillPublicSkill]] = {pack_id: [] for pack_id in raw_pack_map}
    for index, value in enumerate(raw_public_skills):
        if not isinstance(value, dict):
            raise SystemSkillAssetError(f"Public skill at index {index} must be a table.")
        field = f"Public skill at index {index}"
        name = _required_string(value.get("name"), f"{field} name")
        pack_id = _required_identifier(value.get("pack_id"), f"Public skill {name!r} pack_id", SYSTEM_SKILL_MEMBER_RE)
        if pack_id not in raw_pack_map:
            raise SystemSkillAssetError(f"Public skill {name!r} references unknown pack {pack_id!r}.")
        role = value.get("role")
        if role not in SYSTEM_SKILL_PUBLIC_ROLES:
            raise SystemSkillAssetError(f"Public skill {name!r} role must be welcome or entrypoint.")
        source_path = _normalize_relative_path(_required_string(value.get("source_path"), f"Public skill {name!r} source_path"))
        if PurePosixPath(source_path).name != name:
            raise SystemSkillAssetError(f"Public skill {name!r} source_path must end with its canonical name.")
        commands = _string_list(value.get("public_commands", ()), f"Public skill {name!r} public_commands")
        if any(SYSTEM_EXTENSION_COMMAND_RE.fullmatch(command) is None for command in commands):
            raise SystemSkillAssetError(f"Public skill {name!r} contains an invalid command id.")
        if len(commands) != len(set(commands)):
            raise SystemSkillAssetError(f"Public skill {name!r} must not define duplicate public commands.")
        aliases = _string_list(value.get("legacy_aliases", ()), f"Public skill {name!r} legacy_aliases")
        points = _string_list(value.get("callback_insertion_points", ()), f"Public skill {name!r} callback insertion points")
        _validate_callback_stages(points, callback_stages, f"public skill {name!r}")
        if role == "welcome" and points:
            raise SystemSkillAssetError(f"Public welcome skill {name!r} must not declare callback insertion points.")
        minimum_value = value.get("minimum_compatible_version")
        pack_floor = raw_pack_map[pack_id].get("minimum_compatible_skill_version")
        minimum = _required_pep440_version(
            pack_floor if minimum_value is None else minimum_value,
            f"Public skill {name!r} minimum_compatible_version",
        )
        public_by_pack[pack_id].append(
            SystemSkillPublicSkill(
                name=name,
                pack_id=pack_id,
                role=str(role),
                source_path=source_path,
                public_commands=commands,
                legacy_aliases=aliases,
                callback_insertion_points=points,
                minimum_compatible_version=minimum,
            )
        )

    packs: list[SystemSkillPack] = []
    for index, value in enumerate(raw_packs):
        assert isinstance(value, dict)
        field = f"System-skill pack at index {index}"
        pack_id = _required_identifier(value.get("pack_id"), f"{field} pack_id", SYSTEM_SKILL_MEMBER_RE)
        description = _required_string(value.get("description"), f"{field} description")
        kind = value.get("kind")
        if kind not in SYSTEM_SKILL_GROUP_KINDS:
            raise SystemSkillAssetError(f"{field} must define kind as core or extension.")
        entry_skill = _required_string(value.get("entry_skill"), f"{field} entry_skill")
        always_available = value.get("always_available")
        if not isinstance(always_available, bool):
            raise SystemSkillAssetError(f"Pack {pack_id!r} must define boolean always_available.")
        extension_id = value.get("extension_id")
        if kind == "core":
            if extension_id is not None or not always_available:
                raise SystemSkillAssetError(f"Core system-skill pack {pack_id!r} must be always available and omit extension_id.")
        else:
            extension_id = _required_identifier(extension_id, f"Pack {pack_id!r} extension_id", SYSTEM_EXTENSION_ID_RE)
            if always_available:
                raise SystemSkillAssetError(f"Extension system-skill pack {pack_id!r} must not be always_available.")
        public_skills = tuple(public_by_pack[pack_id])
        roles = tuple(skill.role for skill in public_skills)
        if roles.count("welcome") != 1 or roles.count("entrypoint") != 1 or len(public_skills) != 2:
            raise SystemSkillAssetError(f"Pack {pack_id!r} must declare exactly one welcome and one entrypoint public skill.")
        entrypoint = next(skill for skill in public_skills if skill.role == "entrypoint")
        welcome = next(skill for skill in public_skills if skill.role == "welcome")
        if entry_skill != entrypoint.name:
            raise SystemSkillAssetError(f"Pack {pack_id!r} entry_skill must resolve to its entrypoint-role record.")
        if kind == "core":
            if entrypoint.name != "isomer-op-entrypoint" or welcome.name != "isomer-op-welcome":
                raise SystemSkillAssetError("Core pack public roles must be isomer-op-welcome and isomer-op-entrypoint.")
        else:
            entry_match = SYSTEM_EXTENSION_ENTRYPOINT_RE.fullmatch(entrypoint.name)
            welcome_match = SYSTEM_EXTENSION_WELCOME_RE.fullmatch(welcome.name)
            if entry_match is None or entry_match.group(1) != extension_id:
                raise SystemSkillAssetError(f"Extension pack {pack_id!r} entry_skill must be isomer-ext-{extension_id}-entrypoint.")
            if welcome_match is None or welcome_match.group(1) != extension_id:
                raise SystemSkillAssetError(f"Extension pack {pack_id!r} welcome skill must be isomer-ext-{extension_id}-welcome.")
        declared_public = _string_list(value.get("public_skills"), f"Pack {pack_id!r} public_skills")
        if declared_public != tuple(skill.name for skill in public_skills):
            raise SystemSkillAssetError(
                f"Pack {pack_id!r} public skill order does not match declared public records: expected {declared_public!r}."
            )
        packs.append(
            SystemSkillPack(
                pack_id=pack_id,
                description=description,
                kind=str(kind),
                entry_skill=entry_skill,
                always_available=always_available,
                minimum_compatible_skill_version=_required_pep440_version(
                    value.get("minimum_compatible_skill_version"), f"Pack {pack_id!r} minimum_compatible_skill_version"
                ),
                public_skills=public_skills,
                extension_id=str(extension_id) if isinstance(extension_id, str) else None,
                protected_members=_string_list(value.get("protected_members", ()), f"Pack {pack_id!r} protected_members"),
            )
        )
    return tuple(packs)


def _parse_system_skill_capabilities(
    manifest: dict[str, Any],
    packs: tuple[SystemSkillPack, ...],
    callback_stages: set[str],
) -> tuple[SystemSkillCapability, ...]:
    raw_capabilities = manifest.get("capabilities")
    if not isinstance(raw_capabilities, list):
        raise SystemSkillAssetError("Packaged system-skill manifest v3 must define [[capabilities]].")
    packs_by_id = {pack.pack_id: pack for pack in packs}
    parsed: list[SystemSkillCapability] = []
    for index, value in enumerate(raw_capabilities):
        if not isinstance(value, dict):
            raise SystemSkillAssetError(f"Protected capability at index {index} must be a table.")
        field = f"Protected capability at index {index}"
        logical_id = _required_string(value.get("logical_id"), f"{field} logical_id")
        pack_id = _required_identifier(value.get("pack_id"), f"Capability {logical_id!r} pack_id", SYSTEM_SKILL_MEMBER_RE)
        pack = packs_by_id.get(pack_id)
        if pack is None:
            raise SystemSkillAssetError(f"Protected capability {logical_id!r} references unknown pack {pack_id!r}.")
        area = _required_identifier(value.get("area"), f"Capability {logical_id!r} area", SYSTEM_SKILL_AREA_RE)
        member_name = _required_identifier(
            value.get("member_name"), f"Capability {logical_id!r} member_name", SYSTEM_SKILL_MEMBER_RE
        )
        source_path = _normalize_relative_path(
            _required_string(value.get("source_path"), f"Capability {logical_id!r} source_path")
        )
        expected_path = (PurePosixPath(pack.source_path) / "subskills" / logical_id).as_posix()
        if source_path != expected_path:
            raise SystemSkillAssetError(
                f"Protected capability {logical_id!r} source_path must be {expected_path!r}, got {source_path!r}."
            )
        invocation_designator = _required_string(
            value.get("invocation_designator"), f"Capability {logical_id!r} invocation_designator"
        )
        expected_designator = f"{pack.entry_skill}->{member_name}"
        if invocation_designator != expected_designator or "(" in invocation_designator or ")" in invocation_designator:
            raise SystemSkillAssetError(
                f"Protected capability {logical_id!r} invocation_designator must be bare canonical path {expected_designator!r}."
            )
        dependencies = _string_list(value.get("dependencies", ()), f"Capability {logical_id!r} dependencies")
        legacy_aliases = _string_list(value.get("legacy_aliases", ()), f"Capability {logical_id!r} legacy_aliases")
        points = _string_list(
            value.get("callback_insertion_points", ()), f"Capability {logical_id!r} callback insertion points"
        )
        _validate_callback_stages(points, callback_stages, f"capability {logical_id!r}")
        minimum_value = value.get("minimum_compatible_version")
        minimum = (
            pack.minimum_compatible_skill_version
            if minimum_value is None
            else _required_pep440_version(minimum_value, f"Capability {logical_id!r} minimum_compatible_version")
        )
        parsed.append(
            SystemSkillCapability(
                logical_id=logical_id,
                pack_id=pack_id,
                area=area,
                member_name=member_name,
                source_path=source_path,
                invocation_designator=invocation_designator,
                dependencies=dependencies,
                legacy_aliases=legacy_aliases,
                callback_insertion_points=points,
                minimum_compatible_version=minimum,
            )
        )
    by_id = {capability.logical_id: capability for capability in parsed}
    if len(by_id) != len(parsed):
        duplicates = _duplicates(capability.logical_id for capability in parsed)
        raise SystemSkillAssetError(f"Duplicate protected logical ids: {', '.join(duplicates)}")
    expected_all: list[str] = []
    for pack in packs:
        if len(pack.protected_members) != len(set(pack.protected_members)):
            raise SystemSkillAssetError(f"Pack {pack.pack_id!r} contains duplicate protected member ids.")
        expected_all.extend(pack.protected_members)
        actual = tuple(capability.logical_id for capability in parsed if capability.pack_id == pack.pack_id)
        if actual != pack.protected_members:
            raise SystemSkillAssetError(
                f"Pack {pack.pack_id!r} protected member order does not match declared capability records: "
                f"expected {pack.protected_members!r}, got {actual!r}."
            )
    if len(expected_all) != len(set(expected_all)):
        raise SystemSkillAssetError("A protected logical id is declared by more than one pack.")
    if set(expected_all) != set(by_id):
        missing = sorted(set(expected_all) - set(by_id))
        extra = sorted(set(by_id) - set(expected_all))
        raise SystemSkillAssetError(f"Protected capability inventory mismatch; missing={missing!r}, extra={extra!r}.")
    return tuple(parsed)


def _validate_catalog_identities(
    packs: tuple[SystemSkillPack, ...], capabilities: tuple[SystemSkillCapability, ...]
) -> None:
    _require_unique((pack.pack_id for pack in packs), "pack ids")
    _require_unique((skill.name for pack in packs for skill in pack.public_skills), "public skill names")
    _require_unique((skill.source_path for pack in packs for skill in pack.public_skills), "public skill source paths")
    _require_unique((pack.extension_id for pack in packs if pack.extension_id is not None), "extension ids")
    _require_unique((capability.source_path for capability in capabilities), "protected source paths")
    _require_unique((capability.invocation_designator for capability in capabilities), "protected invocation designators")
    for pack in packs:
        members = [capability.member_name for capability in capabilities if capability.pack_id == pack.pack_id]
        _require_unique(members, f"scoped member names in pack {pack.pack_id!r}")

    identities: dict[str, tuple[str, str]] = {}

    def register(identity: str | None, kind: str, canonical: str) -> None:
        if identity is None:
            return
        existing = identities.get(identity)
        if existing is not None and existing != (kind, canonical):
            raise SystemSkillAssetError(
                f"System-skill identity or alias conflict for {identity!r}: {existing[0]} {existing[1]!r} and {kind} {canonical!r}."
            )
        identities[identity] = (kind, canonical)

    for pack in packs:
        register(pack.pack_id, "pack", pack.entry_skill)
        register(pack.extension_id, "pack", pack.entry_skill)
        for public_skill in pack.public_skills:
            register(public_skill.name, "pack", pack.entry_skill)
            for alias in public_skill.legacy_aliases:
                register(alias, "pack", pack.entry_skill)
    for capability in capabilities:
        register(capability.logical_id, "capability", capability.logical_id)
        register(capability.invocation_designator, "capability", capability.logical_id)
        for alias in capability.legacy_aliases:
            register(alias, "capability", capability.logical_id)


def _validate_capability_dependencies(capabilities: tuple[SystemSkillCapability, ...]) -> None:
    by_id = {capability.logical_id: capability for capability in capabilities}
    for capability in capabilities:
        if len(capability.dependencies) != len(set(capability.dependencies)):
            raise SystemSkillAssetError(f"Capability {capability.logical_id!r} declares duplicate dependencies.")
        for dependency in capability.dependencies:
            if dependency not in by_id:
                raise SystemSkillAssetError(
                    f"Capability {capability.logical_id!r} references unknown dependency {dependency!r}."
                )
    state: dict[str, int] = {}
    stack: list[str] = []

    def visit(logical_id: str) -> None:
        status = state.get(logical_id, 0)
        if status == 2:
            return
        if status == 1:
            start = stack.index(logical_id)
            cycle = (*stack[start:], logical_id)
            raise SystemSkillAssetError(f"Protected dependency cycle: {' -> '.join(cycle)}")
        state[logical_id] = 1
        stack.append(logical_id)
        for dependency in by_id[logical_id].dependencies:
            visit(dependency)
        stack.pop()
        state[logical_id] = 2

    for capability in capabilities:
        visit(capability.logical_id)


def _parse_legacy_system_skill_groups(manifest: dict[str, Any]) -> tuple[SystemSkillGroup, ...]:
    groups = manifest.get("groups")
    if not isinstance(groups, dict):
        raise SystemSkillAssetError("Legacy packaged system-skill manifest must define [groups].")
    parsed_groups: list[SystemSkillGroup] = []
    extension_ids: set[str] = set()
    for name, value in groups.items():
        if not isinstance(value, dict):
            raise SystemSkillAssetError(f"System-skill group {name!r} must be a table.")
        skills = _string_list(value.get("skills"), f"System-skill group {name!r} skills")
        kind = value.get("kind")
        if kind not in SYSTEM_SKILL_GROUP_KINDS:
            raise SystemSkillAssetError(f"System-skill group {name!r} must define kind as core or extension.")
        always_available = value.get("always_available")
        if not isinstance(always_available, bool):
            raise SystemSkillAssetError(f"System-skill group {name!r} must define boolean always_available.")
        extension_id = value.get("extension_id")
        entry_skill = value.get("entry_skill")
        commands = value.get("commands")
        if kind == "core":
            if extension_id is not None:
                raise SystemSkillAssetError(f"Core system-skill group {name!r} must not define extension_id.")
            if entry_skill is not None or commands is not None:
                raise SystemSkillAssetError(f"Core system-skill group {name!r} must not define extension entry metadata.")
            if not always_available:
                raise SystemSkillAssetError(f"Core system-skill group {name!r} must be always_available.")
        else:
            extension_id = _required_identifier(
                extension_id, f"Extension system-skill group {name!r} extension_id", SYSTEM_EXTENSION_ID_RE
            )
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
            commands = _string_list(commands, f"Extension system-skill group {name!r} commands")
            if any(SYSTEM_EXTENSION_COMMAND_RE.fullmatch(item) is None for item in commands):
                raise SystemSkillAssetError(
                    f"Extension system-skill group {name!r} must define commands as stable command ids."
                )
            if len(commands) != len(set(commands)):
                raise SystemSkillAssetError(f"Extension system-skill group {name!r} must not define duplicate commands.")
        parsed_groups.append(
            SystemSkillGroup(
                name=str(name),
                description=str(value.get("description", "")),
                skills=tuple(_normalize_relative_path(item) for item in skills),
                kind=str(kind),
                always_available=always_available,
                minimum_compatible_skill_version=_required_pep440_version(
                    value.get("minimum_compatible_skill_version"),
                    f"System-skill group {name!r} minimum_compatible_skill_version",
                ),
                extension_id=str(extension_id) if isinstance(extension_id, str) else None,
                entry_skill=str(entry_skill) if isinstance(entry_skill, str) else None,
                commands=tuple(str(item) for item in commands) if isinstance(commands, tuple) else (),
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
        label = _required_string(value.get("label"), f"Callback insertion point stage {stage!r} label")
        description = _required_string(
            value.get("description"), f"Callback insertion point stage {stage!r} description"
        )
        stages.append(CallbackInsertionPointStage(stage=str(stage), label=label, description=description))
    return tuple(stages)


def _parse_legacy_skill_metadata(
    manifest: dict[str, Any], groups: tuple[SystemSkillGroup, ...]
) -> dict[str, SystemSkillCatalogMetadata]:
    raw_metadata = manifest.get("skill_metadata")
    if raw_metadata is None:
        return {}
    if not isinstance(raw_metadata, dict):
        raise SystemSkillAssetError("Packaged system-skill manifest skill_metadata must be a table.")
    known_paths = {path for group in groups for path in group.skills}
    parsed: dict[str, SystemSkillCatalogMetadata] = {}
    for raw_path, value in raw_metadata.items():
        skill_path = _normalize_relative_path(str(raw_path))
        if skill_path not in known_paths:
            raise SystemSkillAssetError(f"Callback metadata references unknown packaged system skill: {skill_path}")
        if not isinstance(value, dict):
            raise SystemSkillAssetError(f"System-skill metadata {skill_path!r} must be a table.")
        raw_points = _string_list(
            value.get("callback_insertion_points", ()), f"System-skill metadata {skill_path!r} callback insertion points"
        )
        minimum = value.get("minimum_compatible_version")
        parsed[skill_path] = SystemSkillCatalogMetadata(
            callback_insertion_points=raw_points,
            minimum_compatible_version=(
                _required_pep440_version(minimum, f"System-skill metadata {skill_path!r} minimum_compatible_version")
                if minimum is not None
                else None
            ),
        )
    return parsed


def system_skill_catalog_metadata() -> dict[str, SystemSkillCatalogMetadata]:
    """Return callback and compatibility metadata keyed by manifest-relative path."""

    manifest = load_system_skill_manifest()
    catalog = parse_system_skill_manifest(manifest)
    if catalog.is_legacy:
        return _parse_legacy_skill_metadata(manifest, catalog.legacy_groups)
    metadata: dict[str, SystemSkillCatalogMetadata] = {}
    for pack in catalog.packs:
        for public_skill in pack.public_skills:
            metadata[public_skill.source_path] = SystemSkillCatalogMetadata(
                callback_insertion_points=public_skill.callback_insertion_points,
                minimum_compatible_version=public_skill.minimum_compatible_version,
            )
    for capability in catalog.capabilities:
        metadata[capability.source_path] = SystemSkillCatalogMetadata(
            callback_insertion_points=capability.callback_insertion_points,
            minimum_compatible_version=capability.minimum_compatible_version,
        )
    return metadata


def minimum_compatible_system_skill_version(identifier: str) -> str:
    """Resolve the package-owned compatibility floor for a public or protected skill."""

    catalog = system_skill_catalog()
    for pack in catalog.packs:
        if identifier in {pack.pack_id, pack.extension_id}:
            return pack.minimum_compatible_skill_version
        for public_skill in pack.public_skills:
            if identifier in {public_skill.name, public_skill.source_path, *public_skill.legacy_aliases}:
                return public_skill.minimum_compatible_version
    for capability in catalog.capabilities:
        if identifier in {
            capability.logical_id,
            capability.source_path,
            capability.invocation_designator,
            *capability.legacy_aliases,
        }:
            return capability.minimum_compatible_version
    raise SystemSkillAssetError(f"Unknown packaged system skill: {identifier}")


def _required_pep440_version(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise SystemSkillAssetError(f"{field} must be a non-empty PEP 440 version.")
    try:
        Version(value)
    except InvalidVersion as exc:
        raise SystemSkillAssetError(f"{field} must be a valid PEP 440 version: {value!r}") from exc
    return value


def iter_system_skill_paths(groups: Sequence[str] | None = None) -> tuple[str, ...]:
    """Return ordered public-skill paths or flat legacy skill paths."""

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
    """Resolve one manifest-relative public pack or protected bundle path."""

    normalized = _normalize_relative_path(skill_path)
    target = _join_resource(system_skills_root(), normalized)
    if not target.is_dir():
        raise SystemSkillAssetError(f"Packaged system skill is missing: {normalized}")
    skill_md = target.joinpath("SKILL.md")
    if not skill_md.is_file():
        raise SystemSkillAssetError(f"Packaged system skill is missing SKILL.md: {normalized}")
    return target


def resolve_system_skill_capability(logical_id: str) -> Traversable:
    """Resolve one protected logical capability to its nested package resource."""

    capability = system_skill_catalog().capability_by_logical_id(logical_id)
    return resolve_system_skill(capability.source_path)


def materialize_system_skills(
    target: Path,
    *,
    groups: Sequence[str] | None = None,
) -> SystemSkillMaterializationResult:
    """Copy selected public packs to top-level host-discoverable directories."""

    selected_groups = _selected_groups(groups)
    selected_names = tuple(group.name for group in selected_groups)
    target = target.expanduser().resolve(strict=False)
    _ensure_empty_or_new_directory(target)
    root = system_skills_root()
    copied_paths: list[Path] = []
    copied_paths.append(_copy_resource_file(root.joinpath("manifest.toml"), target / "manifest.toml"))
    for group in selected_groups:
        if group.entry_skill is None:
            for skill_path in group.skills:
                destination = target / Path(skill_path)
                _copy_resource_tree(resolve_system_skill(skill_path), destination, copied_paths)
            continue
        for skill_path in group.skills:
            public_name = PurePosixPath(skill_path).name
            destination = target / public_name
            _copy_resource_tree(resolve_system_skill(skill_path), destination, copied_paths)
    return SystemSkillMaterializationResult(
        target=target,
        groups=selected_names,
        copied_paths=tuple(copied_paths),
    )


def materialize_system_skill_private_projection(
    target: Path,
    identifiers: Sequence[str],
) -> SystemSkillPrivateProjectionMaterializationResult:
    """Copy a protected binding and dependency closure into a flat private root."""

    projections = resolve_system_skill_binding_projection(identifiers)
    target = target.expanduser().resolve(strict=False)
    _ensure_empty_or_new_directory(target)
    copied_paths: list[Path] = []
    for projection in projections:
        destination = target / projection.projected_path
        _copy_resource_tree(resolve_system_skill(projection.source_path), destination, copied_paths)
    return SystemSkillPrivateProjectionMaterializationResult(
        target=target,
        projections=projections,
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


def _required_string(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise SystemSkillAssetError(f"{field} must be a non-empty string.")
    return value


def _required_identifier(value: object, field: str, pattern: re.Pattern[str]) -> str:
    identifier = _required_string(value, field)
    if pattern.fullmatch(identifier) is None:
        raise SystemSkillAssetError(f"{field} has invalid value {identifier!r}.")
    return identifier


def _string_list(value: object, field: str) -> tuple[str, ...]:
    if not isinstance(value, (list, tuple)) or not all(isinstance(item, str) and item for item in value):
        raise SystemSkillAssetError(f"{field} must be a string list.")
    return tuple(str(item) for item in value)


def _validate_callback_stages(values: tuple[str, ...], stages: set[str], owner: str) -> None:
    if len(values) != len(set(values)):
        raise SystemSkillAssetError(f"Duplicate callback insertion point stage for {owner}.")
    for value in values:
        if value not in stages:
            raise SystemSkillAssetError(f"Unknown callback insertion point stage {value!r} for {owner}.")


def _require_unique(values: Sequence[str] | Any, label: str) -> None:
    duplicates = _duplicates(values)
    if duplicates:
        raise SystemSkillAssetError(f"Duplicate {label}: {', '.join(duplicates)}")


def _duplicates(values: Sequence[str] | Any) -> tuple[str, ...]:
    seen: set[str] = set()
    duplicates: list[str] = []
    for value in values:
        if value in seen and value not in duplicates:
            duplicates.append(value)
        seen.add(value)
    return tuple(duplicates)


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
