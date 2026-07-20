"""Provider-neutral inspection of explicit system-skill roots and inventories."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.skills.installer import (
    InstalledSystemSkill,
    InvalidSystemSkillProjection,
    SystemSkillRecord,
    SystemSkillTarget,
    inspect_system_skill_manifest,
    inspect_system_skills,
    list_packaged_system_skills,
    resolve_system_skill_selection,
)
from isomer_labs.skills.receipts import SKILL_MANIFEST_FILENAME, SystemSkillManifestRecord
from isomer_labs.skills.system_assets import (
    SystemSkillAssetError,
    SystemSkillPack,
    iter_system_skill_packs,
    system_skill_catalog,
)


INTERNAL_INSPECTION_SCHEMA = "isomer-internal-system-skill-inspection.v3"
INVENTORY_INPUT_SCHEMA = "isomer-system-skill-inventory.v1"


class SystemSkillInspectionError(ValueError):
    """Raised when an explicit inspection request is invalid."""


@dataclass(frozen=True)
class InventorySkillEntry:
    """One skill entry supplied by the current agent host."""

    name: str
    path: str | None = None

    def to_json(self) -> dict[str, object]:
        return {"name": self.name, "path": self.path}


@dataclass(frozen=True)
class InternalSystemSkillInspectionResult:
    """Versioned read-only payload returned by an internal inspector."""

    kind: str
    data: Mapping[str, object]
    diagnostics: tuple[Diagnostic, ...] = ()
    ok: bool = True

    @property
    def mutated(self) -> bool:
        return False

    def to_json(self) -> dict[str, object]:
        return {
            "ok": self.ok,
            "mutated": False,
            "internal_schema_version": INTERNAL_INSPECTION_SCHEMA,
            "inspection_kind": self.kind,
            **self.data,
        }


def inspect_explicit_system_skill_root(
    skill_root: Path,
    *,
    category: str = "all",
    extension_id: str | None = None,
    group_name: str | None = None,
) -> InternalSystemSkillInspectionResult:
    """Inspect exactly one caller-supplied root against the packaged catalog."""

    root = skill_root.expanduser().resolve(strict=False)
    packs = _select_packs(category=category, extension_id=extension_id, group_name=group_name)
    selection = resolve_system_skill_selection(groups=tuple(pack.pack_id for pack in packs), default_core=False)
    target = SystemSkillTarget(target="explicit", skill_root=root)
    receipt = inspect_system_skill_manifest(target)
    status = inspect_system_skills(target, selection)
    diagnostics = list(status.diagnostics)

    root_status = "present"
    if not root.exists():
        root_status = "absent"
    elif not root.is_dir():
        root_status = "invalid"
        diagnostics.append(
            Diagnostic(
                code="ISOSKILL010",
                severity="warning",
                concept="system-skill-root-inspection",
                path=root,
                message="The supplied system-skill root is not a directory.",
            )
        )

    manifest_records = receipt.manifest.record_map() if receipt.manifest is not None else {}
    installed = {item.name: item for item in status.installed}
    invalid = {item.name: item for item in status.invalid_projections}
    records = {item.name: item for item in selection.skills}
    pack_rows: list[dict[str, object]] = []
    managed_names: set[str] = set()
    observed_names: set[str] = set()

    for record in selection.skills:
        installed_item = installed.get(record.name)
        receipt_record = manifest_records.get(record.name)
        row, row_diagnostics = _root_pack_row(
            record,
            installed_item=installed_item,
            invalid_items={
                public.name: invalid[public.name]
                for public in record.public_skills
                if public.name in invalid
            },
            receipt_record=receipt_record,
            receipt_status=receipt.status,
        )
        diagnostics.extend(row_diagnostics)
        pack_rows.append(row)
        public_skill_status = row["public_skill_status"]
        if not isinstance(public_skill_status, list):
            raise AssertionError("Root pack rows must expose a public_skill_status list.")
        if any(isinstance(public, dict) and public.get("status") != "missing" for public in public_skill_status):
            observed_names.add(record.name)
        if row["managed"] is True:
            managed_names.add(record.name)
    group_rows = [
        _root_pack_coverage_row(
            pack,
            record=records[pack.entry_skill],
            row=next(row for row in pack_rows if row["name"] == pack.entry_skill),
            receipt_status=receipt.status,
        )
        for pack in packs
    ]
    legacy_rows = _legacy_receipt_rows(receipt.manifest, receipt.status)
    tracked_names = set(manifest_records)
    if receipt.manifest is not None:
        tracked_names.update(receipt.manifest.public_ownership_map())
        tracked_names.update(record.name for record in receipt.manifest.legacy_paths)
    ambient_paths = _ambient_root_paths(root, tracked_names)
    evidence_basis = "none"
    if managed_names:
        evidence_basis = "managed_receipt"
    elif any(row["coverage_status"] == "unmanaged_complete" for row in group_rows):
        evidence_basis = "explicit_root_verified"
    elif legacy_rows:
        evidence_basis = "managed_legacy_receipt"
    elif observed_names:
        evidence_basis = "explicit_root_partial"

    return InternalSystemSkillInspectionResult(
        kind="explicit_root",
        data={
            "skill_root": str(root),
            "root_status": root_status,
            "evidence_basis": evidence_basis,
            "filters": {
                "category": category,
                "extension": extension_id,
                "group": group_name,
            },
            "receipt": receipt.to_json(),
            "skills": pack_rows,
            "packs": pack_rows,
            "groups": group_rows,
            "extensions": [row for row in group_rows if row["kind"] == "extension"],
            "legacy_flat_paths": legacy_rows,
            "ambient_paths": ambient_paths,
        },
        diagnostics=tuple(_deduplicate_diagnostics(diagnostics)),
    )


def parse_inventory_document(raw: str) -> tuple[InventorySkillEntry, ...]:
    """Parse the versioned structured live-inventory input contract."""

    try:
        document = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemSkillInspectionError(f"Inventory JSON is malformed: {exc.msg}.") from exc
    if not isinstance(document, dict):
        raise SystemSkillInspectionError("Inventory JSON must be an object.")
    if document.get("schema_version") != INVENTORY_INPUT_SCHEMA:
        raise SystemSkillInspectionError(
            f"Unsupported inventory schema; expected {INVENTORY_INPUT_SCHEMA!r}."
        )
    raw_skills = document.get("skills")
    if not isinstance(raw_skills, list):
        raise SystemSkillInspectionError("Inventory JSON `skills` must be a list.")
    entries: list[InventorySkillEntry] = []
    for index, item in enumerate(raw_skills):
        if isinstance(item, str):
            entries.append(_inventory_entry(item, None, index=index))
            continue
        if not isinstance(item, dict):
            raise SystemSkillInspectionError(f"Inventory skill entry {index} must be a string or object.")
        name = item.get("name")
        path = item.get("path")
        if path is not None and not isinstance(path, str):
            raise SystemSkillInspectionError(f"Inventory skill entry {index} path must be a string or null.")
        entries.append(_inventory_entry(name, path, index=index))
    return tuple(entries)


def classify_system_skill_inventory(
    entries: Sequence[InventorySkillEntry],
) -> InternalSystemSkillInspectionResult:
    """Classify host names as entrypoints, legacy members, aliases, or ambient entries."""

    unique_entries: dict[str, InventorySkillEntry] = {}
    for entry in entries:
        normalized = _inventory_entry(entry.name, entry.path)
        existing = unique_entries.get(normalized.name)
        if existing is None or (existing.path is None and normalized.path is not None):
            unique_entries[normalized.name] = normalized

    catalog = system_skill_catalog()
    pack_records = {record.name: record for record in list_packaged_system_skills()}
    public_skills: dict[str, dict[str, object]] = {}
    legacy_members: dict[str, dict[str, object]] = {}
    legacy_aliases: dict[str, dict[str, object]] = {}
    unmatched: dict[str, InventorySkillEntry] = {}
    for name, entry in unique_entries.items():
        try:
            public = catalog.public_skill_by_name(name)
        except SystemSkillAssetError:
            public = None
        if public is not None:
            pack = catalog.pack_for_public_skill(public.name)
            public_skills[name] = {
                "name": name,
                "canonical_public_skill": public.name,
                "public_role": public.role,
                "pack_id": pack.pack_id,
                "extension_id": pack.extension_id,
                "inventory_path": entry.path,
                "observation_kind": f"public_{public.role}",
                "protected_integrity_status": "unverified",
            }
            continue
        try:
            kind, canonical_id, deprecated = catalog.normalize_identity(name)
        except SystemSkillAssetError:
            unmatched[name] = entry
            continue
        if kind == "pack":
            pack = catalog.pack_for_public_skill(canonical_id)
            row: dict[str, object] = {
                "name": name,
                "canonical_public_skill": pack.entry_skill,
                "public_role": "entrypoint",
                "pack_id": pack.pack_id,
                "extension_id": pack.extension_id,
                "inventory_path": entry.path,
                "observation_kind": "legacy_public_alias",
                "protected_integrity_status": "unverified",
            }
            legacy_aliases[name] = row
            continue
        capability = catalog.capability_by_logical_id(canonical_id)
        pack = catalog.pack_by_id(capability.pack_id)
        legacy_members[name] = {
            "name": name,
            "logical_id": capability.logical_id,
            "pack_id": pack.pack_id,
            "public_skill": pack.entry_skill,
            "member_name": capability.member_name,
            "invocation_designator": capability.invocation_designator,
            "inventory_path": entry.path,
            "observation_kind": "legacy_member",
            "protected_integrity_status": "unverified",
        }
    group_rows = [
        _inventory_pack_row(
            pack,
            public_skill_names=set(public_skills),
            legacy_members=legacy_members,
            legacy_aliases=legacy_aliases,
        )
        for pack in catalog.packs
    ]
    capability_order = {
        capability.logical_id: index for index, capability in enumerate(catalog.capabilities)
    }
    ordered_legacy_members = sorted(
        legacy_members.values(),
        key=lambda row: (capability_order.get(str(row["logical_id"]), len(capability_order)), str(row["name"])),
    )
    matched_rows = [
        *(
            public_skills[public.name]
            for pack in catalog.packs
            for public in pack.public_skills
            if public.name in public_skills
        ),
        *ordered_legacy_members,
        *(legacy_aliases[name] for name in sorted(legacy_aliases)),
    ]

    return InternalSystemSkillInspectionResult(
        kind="live_inventory",
        data={
            "evidence_basis": "live_inventory_limited",
            "input_schema_version": INVENTORY_INPUT_SCHEMA,
            "inventory": [unique_entries[name].to_json() for name in sorted(unique_entries)],
            "matched_skills": matched_rows,
            "public_skill_observations": [public_skills[name] for name in sorted(public_skills)],
            "welcome_observations": [
                public_skills[name]
                for name in sorted(public_skills)
                if public_skills[name]["public_role"] == "welcome"
            ],
            "entrypoint_observations": [
                public_skills[name]
                for name in sorted(public_skills)
                if public_skills[name]["public_role"] == "entrypoint"
            ],
            "legacy_member_observations": [
                legacy_members[name] for name in sorted(legacy_members)
            ],
            "legacy_alias_observations": [legacy_aliases[name] for name in sorted(legacy_aliases)],
            "unmatched_skills": [unmatched[name].to_json() for name in sorted(unmatched)],
            "groups": group_rows,
            "extensions": [row for row in group_rows if row["kind"] == "extension"],
            "catalog_packs": [record.to_json() for record in pack_records.values()],
        },
    )


def inspection_error_result(message: str) -> InternalSystemSkillInspectionResult:
    """Return a deterministic non-mutating validation failure."""

    diagnostic = Diagnostic(
        code="ISOSKILL010",
        severity="error",
        concept="system-skill-internal-inspection",
        message=message,
    )
    return InternalSystemSkillInspectionResult(
        kind="invalid_request",
        data={"evidence_basis": "none"},
        diagnostics=(diagnostic,),
        ok=False,
    )


def _select_packs(
    *,
    category: str,
    extension_id: str | None,
    group_name: str | None,
) -> tuple[SystemSkillPack, ...]:
    if category not in {"core", "extensions", "all"}:
        raise SystemSkillInspectionError(f"Unknown system-skill category: {category}")
    all_packs = iter_system_skill_packs()
    known_groups = {pack.pack_id: pack for pack in all_packs}
    known_extensions = {
        pack.extension_id: pack
        for pack in all_packs
        if pack.kind == "extension" and pack.extension_id is not None
    }
    if group_name is not None and group_name not in known_groups:
        raise SystemSkillInspectionError(f"Unknown packaged system-skill group: {group_name}")
    if extension_id is not None and extension_id not in known_extensions:
        raise SystemSkillInspectionError(f"Unknown packaged system extension: {extension_id}")

    selected = list(all_packs)
    if category == "core":
        selected = [pack for pack in selected if pack.kind == "core"]
    elif category == "extensions":
        selected = [pack for pack in selected if pack.kind == "extension"]
    if group_name is not None:
        selected = [pack for pack in selected if pack.pack_id == group_name]
    if extension_id is not None:
        selected = [pack for pack in selected if pack.extension_id == extension_id]
    if not selected:
        raise SystemSkillInspectionError("System-skill filters select no catalog groups.")
    return tuple(selected)


def _root_pack_row(
    record: SystemSkillRecord,
    *,
    installed_item: InstalledSystemSkill | None,
    invalid_items: Mapping[str, InvalidSystemSkillProjection],
    receipt_record: Any,
    receipt_status: str,
) -> tuple[dict[str, object], tuple[Diagnostic, ...]]:
    diagnostics: list[Diagnostic] = []
    tracked = receipt_record is not None and receipt_status == "current"
    legacy_tracked = receipt_record is not None and receipt_status == "legacy"
    projection_status = "missing"
    projection_mode: str | None = None
    path: str | None = None
    compatibility_status: str | None = None

    if installed_item is not None:
        projection_mode = installed_item.projection_mode
        path = str(installed_item.path)
        compatibility_status = installed_item.compatibility_status
        if not (installed_item.path / "SKILL.md").is_file():
            projection_status = "missing_skill_material"
            diagnostics.append(
                Diagnostic(
                    code="ISOSKILL012",
                    severity="warning",
                    concept="system-skill-projection",
                    path=installed_item.path,
                    field=record.name,
                    message="Projected skill directory is missing SKILL.md.",
                )
            )
        elif tracked and receipt_record.source_path != record.source_path:
            projection_status = "receipt_source_mismatch"
            diagnostics.append(
                Diagnostic(
                    code="ISOSKILL012",
                    severity="warning",
                    concept="system-skill-projection",
                    path=installed_item.path,
                    field=record.name,
                    message="Receipt source_path does not match the packaged catalog.",
                )
            )
        elif tracked and receipt_record.projection_mode != installed_item.projection_mode:
            projection_status = "receipt_projection_mismatch"
            diagnostics.append(
                Diagnostic(
                    code="ISOSKILL012",
                    severity="warning",
                    concept="system-skill-projection",
                    path=installed_item.path,
                    field=record.name,
                    message="Receipt projection_mode does not match the observed projection.",
                )
            )
        elif tracked and installed_item.installation_verified:
            projection_status = "valid"
        elif installed_item.pack_status == "incomplete":
            projection_status = "incomplete"
        elif tracked:
            projection_status = installed_item.pack_status
        elif _explicit_pack_material_complete(installed_item):
            projection_status = "unmanaged_valid"
        else:
            projection_status = "unmanaged_incomplete"

    public_rows: list[dict[str, object]] = []
    installed_public = {
        public.name: public for public in (installed_item.public_skills if installed_item is not None else ())
    }
    for public in record.public_skills:
        observation = installed_public.get(public.name)
        invalid = invalid_items.get(public.name)
        if invalid is not None:
            public_rows.append(
                {
                    **public.to_json(),
                    "path": str(invalid.path),
                    "status": invalid.path_kind,
                    "identity_status": invalid.path_kind,
                    "projection_mode": None,
                    "skill_version": None,
                    "receipt_skill_version": None,
                    "compatibility_status": "invalid",
                    "receipt_owned": False,
                    "installation_verified": False,
                }
            )
        elif observation is not None:
            public_rows.append({**public.to_json(), **observation.to_json(), "status": observation.identity_status})
        else:
            public_rows.append(
                {
                    **public.to_json(),
                    "path": None,
                    "status": "missing",
                    "identity_status": "missing",
                    "projection_mode": None,
                    "skill_version": None,
                    "receipt_skill_version": None,
                    "compatibility_status": "missing",
                    "receipt_owned": False,
                    "installation_verified": False,
                }
            )
    role_status = {str(public["role"]): str(public["status"]) for public in public_rows}
    entrypoint_invalid = next(
        (invalid for public_name, invalid in invalid_items.items() if public_name == record.name),
        None,
    )
    if entrypoint_invalid is not None:
        projection_status = entrypoint_invalid.path_kind
        path = str(entrypoint_invalid.path)
    managed = tracked and installed_item is not None and installed_item.installation_verified
    evidence_basis = "none"
    if managed:
        evidence_basis = "managed_receipt"
    elif projection_status == "unmanaged_valid":
        evidence_basis = "explicit_root_verified"
    elif installed_item is not None:
        evidence_basis = "explicit_root_partial"
    elif legacy_tracked:
        evidence_basis = "managed_legacy_receipt"
    return (
        {
            **record.to_json(),
            "tracked_by_receipt": tracked,
            "tracked_by_legacy_receipt": legacy_tracked,
            "managed": managed,
            "path": path,
            "projection_mode": projection_mode,
            "projection_status": projection_status,
            "public_skill_status": public_rows,
            "welcome_status": role_status.get("welcome", "missing"),
            "entrypoint_status": role_status.get("entrypoint", "missing"),
            "compatibility_status": compatibility_status,
            "evidence_basis": evidence_basis,
            "pack_status": installed_item.pack_status if installed_item is not None else "missing",
            "installation_verified": installed_item.installation_verified if installed_item is not None else False,
            "protected_member_status": (
                [member.to_json() for member in installed_item.protected_members]
                if installed_item is not None
                else []
            ),
            "missing_protected_members": (
                list(installed_item.missing_protected_members) if installed_item is not None else [
                    member.logical_id for member in record.protected_members
                ]
            ),
            "extra_protected_paths": list(installed_item.extra_protected_paths) if installed_item is not None else [],
        },
        tuple(diagnostics),
    )


def _explicit_pack_material_complete(installed: InstalledSystemSkill) -> bool:
    return (
        installed.pack_status in {"unmanaged", "receipt_mismatch"}
        and all(
            public.identity_status == "valid" and public.skill_version is not None
            for public in installed.public_skills
        )
        and not installed.missing_protected_members
        and not installed.extra_protected_paths
        and all(
            member.identity_status == "valid" and member.skill_version is not None
            for member in installed.protected_members
        )
    )


def _root_pack_coverage_row(
    pack: SystemSkillPack,
    *,
    record: SystemSkillRecord,
    row: Mapping[str, object],
    receipt_status: str,
) -> dict[str, object]:
    members = tuple(member.logical_id for member in record.protected_members)
    member_rows = row.get("protected_member_status")
    valid_members = tuple(
        str(member.get("logical_id"))
        for member in member_rows
        if isinstance(member_rows, list) and isinstance(member, dict) and member.get("identity_status") == "valid"
    ) if isinstance(member_rows, list) else ()
    missing = tuple(member for member in members if member not in valid_members)
    projection_status = row.get("projection_status")
    public_rows = row.get("public_skill_status")
    public_complete = isinstance(public_rows, list) and len(public_rows) == len(pack.public_skills) and all(
        isinstance(public, dict) and public.get("identity_status") == "valid"
        for public in public_rows
    )
    if projection_status == "valid" and public_complete and not missing:
        coverage_status = "complete"
    elif projection_status == "unmanaged_valid" and public_complete and not missing:
        coverage_status = "unmanaged_complete"
    elif (
        row.get("entrypoint_status") != "missing"
        or row.get("welcome_status") != "missing"
        or valid_members
    ):
        coverage_status = "partial"
    else:
        coverage_status = "missing"
    return {
        "name": pack.pack_id,
        "pack_id": pack.pack_id,
        "kind": pack.kind,
        "extension_id": pack.extension_id,
        "entry_skill": pack.entry_skill,
        "public_skills": [public.to_json() for public in pack.public_skills],
        "members": list(members),
        "installed_members": list(valid_members),
        "observed_members": list(valid_members),
        "missing_members": list(missing),
        "coverage_status": coverage_status,
        "entrypoint_status": row.get("entrypoint_status"),
        "welcome_status": row.get("welcome_status"),
        "protected_integrity_status": "verified" if coverage_status in {"complete", "unmanaged_complete"} else "incomplete",
        "evidence_basis": row.get("evidence_basis"),
        "receipt_status": receipt_status,
        "projection_status": projection_status,
        "version_status": row.get("compatibility_status"),
        "minimum_compatible_skill_version": pack.minimum_compatible_skill_version,
        "catalog_records": [member.to_json() for member in record.protected_members],
        "extra_protected_paths": row.get("extra_protected_paths", []),
    }


def _inventory_pack_row(
    pack: SystemSkillPack,
    *,
    public_skill_names: set[str],
    legacy_members: Mapping[str, Mapping[str, object]],
    legacy_aliases: Mapping[str, Mapping[str, object]],
) -> dict[str, object]:
    catalog = system_skill_catalog()
    members = tuple(
        capability.logical_id for capability in catalog.capabilities if capability.pack_id == pack.pack_id
    )
    observed_members = tuple(
        sorted(
            {
                str(row["logical_id"])
                for row in legacy_members.values()
                if row.get("pack_id") == pack.pack_id
            }
        )
    )
    aliases = tuple(
        sorted(name for name, row in legacy_aliases.items() if row.get("pack_id") == pack.pack_id)
    )
    welcome_seen = pack.welcome is not None and pack.welcome.name in public_skill_names
    entrypoint_seen = pack.entry_skill in public_skill_names
    if welcome_seen and entrypoint_seen:
        coverage_status = "public_pair_seen"
        evidence_basis = "public_pair_seen"
    elif entrypoint_seen:
        coverage_status = "entrypoint_seen"
        evidence_basis = "entrypoint_seen"
    elif welcome_seen:
        coverage_status = "welcome_seen"
        evidence_basis = "welcome_seen"
    elif observed_members or aliases:
        coverage_status = "legacy_observed"
        evidence_basis = "legacy_member_observation"
    else:
        coverage_status = "missing"
        evidence_basis = "none"
    return {
        "name": pack.pack_id,
        "pack_id": pack.pack_id,
        "kind": pack.kind,
        "extension_id": pack.extension_id,
        "entry_skill": pack.entry_skill,
        "public_skills": [public.to_json() for public in pack.public_skills],
        "members": list(members),
        "entrypoint_status": "seen" if entrypoint_seen else "not_seen",
        "entrypoint_seen": entrypoint_seen,
        "welcome_status": "seen" if welcome_seen else "not_seen",
        "welcome_seen": welcome_seen,
        "installed_members": list(observed_members),
        "observed_members": list(observed_members),
        "legacy_aliases_seen": list(aliases),
        "missing_members": [member for member in members if member not in observed_members],
        "coverage_status": coverage_status,
        "protected_integrity_status": "unverified",
        "evidence_basis": evidence_basis,
    }


def _legacy_receipt_rows(manifest: object, receipt_status: str) -> list[dict[str, object]]:
    if manifest is None:
        return []
    raw_records: list[SystemSkillManifestRecord | object] = []
    if receipt_status == "legacy":
        raw_records.extend(getattr(manifest, "skills", ()))
    raw_records.extend(getattr(manifest, "legacy_paths", ()))
    catalog = system_skill_catalog()
    rows: list[dict[str, object]] = []
    for record in raw_records:
        name = getattr(record, "name", None)
        if not isinstance(name, str):
            continue
        candidate_pack: str | None = None
        candidate_public_skill: str | None = None
        logical_id: str | None = None
        try:
            kind, canonical_id, _deprecated = catalog.normalize_identity(name)
            if kind == "pack":
                pack = catalog.pack_for_public_skill(canonical_id)
            else:
                capability = catalog.capability_by_logical_id(canonical_id)
                pack = catalog.pack_by_id(capability.pack_id)
                logical_id = capability.logical_id
            candidate_pack = pack.pack_id
            candidate_public_skill = pack.entry_skill
        except SystemSkillAssetError:
            pass
        rows.append(
            {
                "name": name,
                "source_path": getattr(record, "source_path", None),
                "projection_mode": getattr(record, "projection_mode", None),
                "skill_version": getattr(record, "skill_version", None),
                "logical_id": logical_id,
                "candidate_pack_id": candidate_pack,
                "candidate_public_skill": candidate_public_skill,
                "evidence_basis": "managed_legacy_receipt",
                "nested_integrity_status": "unverified",
            }
        )
    return sorted(rows, key=lambda row: str(row["name"]))


def _ambient_root_paths(root: Path, tracked_names: set[str]) -> list[dict[str, str]]:
    if not root.is_dir():
        return []
    rows: list[dict[str, str]] = []
    for path in sorted(root.iterdir(), key=lambda item: item.name):
        if path.name == SKILL_MANIFEST_FILENAME or path.name in tracked_names:
            continue
        if path.is_symlink():
            path_kind = "symlink"
        elif path.is_dir():
            path_kind = "directory"
        elif path.is_file():
            path_kind = "file"
        else:
            path_kind = "other"
        rows.append({"name": path.name, "path": str(path), "path_kind": path_kind})
    return rows


def _aggregate_version_status(members: Sequence[str], statuses: Mapping[str, str]) -> str | None:
    observed = {statuses[name] for name in members if name in statuses}
    for value in (
        "receipt_drift",
        "malformed_version",
        "missing_version",
        "obsolete_incompatible",
        "newer_than_cli",
        "unversioned",
        "compatible_older",
        "current",
    ):
        if value in observed:
            return value
    return None


def _inventory_entry(name: object, path: str | None, *, index: int | None = None) -> InventorySkillEntry:
    label = f"Inventory skill entry {index}" if index is not None else "Inventory skill entry"
    if not isinstance(name, str) or not name.strip():
        raise SystemSkillInspectionError(f"{label} name must be a non-empty string.")
    return InventorySkillEntry(name=name.strip(), path=path)


def _deduplicate_diagnostics(diagnostics: Sequence[Diagnostic]) -> list[Diagnostic]:
    seen: set[tuple[object, ...]] = set()
    result: list[Diagnostic] = []
    for diagnostic in diagnostics:
        key = (
            diagnostic.code,
            diagnostic.severity,
            diagnostic.concept,
            str(diagnostic.path) if diagnostic.path is not None else None,
            diagnostic.field,
            diagnostic.message,
        )
        if key in seen:
            continue
        seen.add(key)
        result.append(diagnostic)
    return result


__all__ = [
    "INTERNAL_INSPECTION_SCHEMA",
    "INVENTORY_INPUT_SCHEMA",
    "InternalSystemSkillInspectionResult",
    "InventorySkillEntry",
    "SystemSkillInspectionError",
    "classify_system_skill_inventory",
    "inspect_explicit_system_skill_root",
    "inspection_error_result",
    "parse_inventory_document",
]
