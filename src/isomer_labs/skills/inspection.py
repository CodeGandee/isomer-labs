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
from isomer_labs.skills.system_assets import SystemSkillGroup, iter_system_skill_groups


INTERNAL_INSPECTION_SCHEMA = "isomer-internal-system-skill-inspection.v1"
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
    groups = _select_groups(category=category, extension_id=extension_id, group_name=group_name)
    selection = resolve_system_skill_selection(groups=tuple(group.name for group in groups), default_core=False)
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
    skill_rows: list[dict[str, object]] = []
    managed_names: set[str] = set()
    observed_names: set[str] = set()
    version_statuses: dict[str, str] = {}

    for record in selection.skills:
        installed_item = installed.get(record.name)
        invalid_item = invalid.get(record.name)
        receipt_record = manifest_records.get(record.name)
        row, row_diagnostics = _root_skill_row(
            record,
            installed_item=installed_item,
            invalid_item=invalid_item,
            receipt_record=receipt_record,
            receipt_status=receipt.status,
        )
        diagnostics.extend(row_diagnostics)
        skill_rows.append(row)
        if row["projection_status"] in {"valid", "unmanaged"}:
            observed_names.add(record.name)
        if row["managed"] is True:
            managed_names.add(record.name)
        compatibility = row.get("compatibility_status")
        if isinstance(compatibility, str):
            version_statuses[record.name] = compatibility

    group_rows = [
        _root_group_row(
            group,
            records=records,
            managed_names=managed_names,
            observed_names=observed_names,
            version_statuses=version_statuses,
            receipt_status=receipt.status,
        )
        for group in groups
    ]
    evidence_basis = "none"
    if managed_names:
        evidence_basis = "managed_legacy_receipt" if receipt.status == "legacy" else "managed_receipt"
    elif observed_names:
        evidence_basis = "unmanaged_projection"

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
            "skills": skill_rows,
            "groups": group_rows,
            "extensions": [row for row in group_rows if row["kind"] == "extension"],
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
    """Classify only the host-supplied live inventory; never inspect its paths."""

    unique_entries: dict[str, InventorySkillEntry] = {}
    for entry in entries:
        normalized = _inventory_entry(entry.name, entry.path)
        existing = unique_entries.get(normalized.name)
        if existing is None or (existing.path is None and normalized.path is not None):
            unique_entries[normalized.name] = normalized

    catalog_records = {record.name: record for record in list_packaged_system_skills()}
    matched_names = set(unique_entries).intersection(catalog_records)
    unmatched_names = set(unique_entries).difference(catalog_records)
    ordered_matched = [record.name for record in list_packaged_system_skills() if record.name in matched_names]
    ordered_unmatched = sorted(unmatched_names)
    group_rows = [_inventory_group_row(group, matched_names) for group in iter_system_skill_groups()]

    return InternalSystemSkillInspectionResult(
        kind="live_inventory",
        data={
            "evidence_basis": "live_inventory",
            "input_schema_version": INVENTORY_INPUT_SCHEMA,
            "inventory": [unique_entries[name].to_json() for name in sorted(unique_entries)],
            "matched_skills": [
                {
                    **catalog_records[name].to_json(),
                    "inventory_path": unique_entries[name].path,
                    "evidence_basis": "live_inventory",
                }
                for name in ordered_matched
            ],
            "unmatched_skills": [unique_entries[name].to_json() for name in ordered_unmatched],
            "groups": group_rows,
            "extensions": [row for row in group_rows if row["kind"] == "extension"],
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


def _select_groups(
    *,
    category: str,
    extension_id: str | None,
    group_name: str | None,
) -> tuple[SystemSkillGroup, ...]:
    if category not in {"core", "extensions", "all"}:
        raise SystemSkillInspectionError(f"Unknown system-skill category: {category}")
    all_groups = iter_system_skill_groups()
    known_groups = {group.name: group for group in all_groups}
    known_extensions = {
        group.extension_id: group
        for group in all_groups
        if group.kind == "extension" and group.extension_id is not None
    }
    if group_name is not None and group_name not in known_groups:
        raise SystemSkillInspectionError(f"Unknown packaged system-skill group: {group_name}")
    if extension_id is not None and extension_id not in known_extensions:
        raise SystemSkillInspectionError(f"Unknown packaged system extension: {extension_id}")

    selected = list(all_groups)
    if category == "core":
        selected = [group for group in selected if group.kind == "core"]
    elif category == "extensions":
        selected = [group for group in selected if group.kind == "extension"]
    if group_name is not None:
        selected = [group for group in selected if group.name == group_name]
    if extension_id is not None:
        selected = [group for group in selected if group.extension_id == extension_id]
    if not selected:
        raise SystemSkillInspectionError("System-skill filters select no catalog groups.")
    return tuple(selected)


def _root_skill_row(
    record: SystemSkillRecord,
    *,
    installed_item: InstalledSystemSkill | None,
    invalid_item: InvalidSystemSkillProjection | None,
    receipt_record: Any,
    receipt_status: str,
) -> tuple[dict[str, object], tuple[Diagnostic, ...]]:
    diagnostics: list[Diagnostic] = []
    tracked = receipt_record is not None and receipt_status in {"current", "legacy"}
    projection_status = "missing"
    projection_mode: str | None = None
    path: str | None = None
    compatibility_status: str | None = None

    if invalid_item is not None:
        projection_status = invalid_item.path_kind
        path = str(invalid_item.path)
    elif installed_item is not None:
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
        else:
            projection_status = "valid" if tracked else "unmanaged"

    managed = tracked and projection_status == "valid"
    evidence_basis = "none"
    if managed:
        evidence_basis = "managed_legacy_receipt" if receipt_status == "legacy" else "managed_receipt"
    elif projection_status == "unmanaged":
        evidence_basis = "unmanaged_projection"
    return (
        {
            **record.to_json(),
            "tracked_by_receipt": tracked,
            "managed": managed,
            "path": path,
            "projection_mode": projection_mode,
            "projection_status": projection_status,
            "compatibility_status": compatibility_status,
            "evidence_basis": evidence_basis,
        },
        tuple(diagnostics),
    )


def _root_group_row(
    group: SystemSkillGroup,
    *,
    records: Mapping[str, SystemSkillRecord],
    managed_names: set[str],
    observed_names: set[str],
    version_statuses: Mapping[str, str],
    receipt_status: str,
) -> dict[str, object]:
    members = tuple(Path(path).name for path in group.skills)
    managed = tuple(name for name in members if name in managed_names)
    observed = tuple(name for name in members if name in observed_names)
    missing = tuple(name for name in members if name not in observed_names)
    unmanaged = tuple(name for name in observed if name not in managed_names)
    if len(managed) == len(members):
        coverage_status = "complete"
    elif len(observed) == len(members):
        coverage_status = "unmanaged_complete"
    elif observed:
        coverage_status = "partial"
    else:
        coverage_status = "missing"
    evidence_basis = "none"
    if managed:
        evidence_basis = "managed_legacy_receipt" if receipt_status == "legacy" else "managed_receipt"
    elif observed:
        evidence_basis = "unmanaged_projection"
    return {
        "name": group.name,
        "kind": group.kind,
        "extension_id": group.extension_id,
        "entry_skill": group.entry_skill,
        "members": list(members),
        "installed_members": list(managed),
        "observed_members": list(observed),
        "unmanaged_members": list(unmanaged),
        "missing_members": list(missing),
        "coverage_status": coverage_status,
        "evidence_basis": evidence_basis,
        "version_status": _aggregate_version_status(members, version_statuses),
        "minimum_compatible_skill_version": group.minimum_compatible_skill_version,
        "catalog_records": [records[name].to_json() for name in members],
    }


def _inventory_group_row(group: SystemSkillGroup, matched_names: set[str]) -> dict[str, object]:
    members = tuple(Path(path).name for path in group.skills)
    installed = tuple(name for name in members if name in matched_names)
    missing = tuple(name for name in members if name not in matched_names)
    coverage_status = "complete" if not missing else "partial" if installed else "missing"
    return {
        "name": group.name,
        "kind": group.kind,
        "extension_id": group.extension_id,
        "entry_skill": group.entry_skill,
        "members": list(members),
        "installed_members": list(installed),
        "missing_members": list(missing),
        "coverage_status": coverage_status,
        "evidence_basis": "live_inventory" if installed else "none",
    }


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
