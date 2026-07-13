"""Read-only internal commands used by version-aligned Isomer system skills."""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

import click

from isomer_labs.cli.options import CliOptions
from isomer_labs.cli.output import emit_output
from isomer_labs.skills.inspection import (
    InventorySkillEntry,
    SystemSkillInspectionError,
    classify_system_skill_inventory,
    inspect_explicit_system_skill_root,
    inspection_error_result,
    parse_inventory_document,
)
from isomer_labs.skills.installer import SystemSkillInstallError


def register_internal_commands(app: click.Group) -> None:
    @app.group(name="internals", help="Versioned read-only primitives for Isomer system skills.")
    def internals_group() -> None:
        pass

    @internals_group.command(
        name="inspect-system-skill-root",
        help="Inspect exactly one explicit Isomer system-skill root.",
    )
    @click.option(
        "--skill-root",
        required=True,
        type=click.Path(path_type=Path, file_okay=True, dir_okay=True),
        help="Explicit agent-supplied skill root. No other roots are searched.",
    )
    @click.option("--category", type=click.Choice(("core", "extensions", "all")), default="all", show_default=True)
    @click.option("--extension", "extension_id", default=None, help="Packaged extension id filter.")
    @click.option("--group", "group_name", default=None, help="Packaged system-skill group filter.")
    @click.pass_context
    def inspect_system_skill_root_command(
        ctx: click.Context,
        skill_root: Path,
        category: str,
        extension_id: str | None,
        group_name: str | None,
    ) -> int:
        try:
            result = inspect_explicit_system_skill_root(
                skill_root,
                category=category,
                extension_id=extension_id,
                group_name=group_name,
            )
        except (SystemSkillInspectionError, SystemSkillInstallError) as exc:
            result = inspection_error_result(str(exc))
        payload = result.to_json()
        return emit_output(
            "internals inspect-system-skill-root",
            _root_options(ctx),
            payload,
            list(result.diagnostics),
            _render_root_inspection(payload),
        )

    @internals_group.command(
        name="classify-system-skill-inventory",
        help="Classify an explicit live skill inventory without filesystem discovery.",
    )
    @click.option("--skill-name", "skill_names", multiple=True, help="Host-visible skill name. Repeat as needed.")
    @click.option(
        "--inventory-json",
        default=None,
        help="Versioned inventory JSON file, or '-' for stdin.",
    )
    @click.pass_context
    def classify_system_skill_inventory_command(
        ctx: click.Context,
        skill_names: tuple[str, ...],
        inventory_json: str | None,
    ) -> int:
        try:
            entries = [InventorySkillEntry(name=name) for name in skill_names]
            if inventory_json is not None:
                entries.extend(parse_inventory_document(_read_inventory_json(inventory_json)))
            result = classify_system_skill_inventory(entries)
        except (OSError, SystemSkillInspectionError) as exc:
            result = inspection_error_result(str(exc))
        payload = result.to_json()
        return emit_output(
            "internals classify-system-skill-inventory",
            _root_options(ctx),
            payload,
            list(result.diagnostics),
            _render_inventory_classification(payload),
        )


def _read_inventory_json(source: str) -> str:
    if source == "-":
        return click.get_text_stream("stdin").read()
    path = Path(source).expanduser()
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SystemSkillInspectionError(f"Cannot read inventory JSON {path}: {exc}") from exc


def _root_options(ctx: click.Context) -> CliOptions:
    root_options = ctx.find_root().obj
    return root_options if isinstance(root_options, CliOptions) else CliOptions()


def _render_root_inspection(payload: dict[str, object]) -> list[str]:
    lines = [
        "Explicit Isomer system-skill root inspection",
        f"Root: {payload.get('skill_root', '(invalid request)')}",
        f"Root status: {payload.get('root_status', 'unknown')}",
        f"Evidence: {payload.get('evidence_basis', 'none')}",
    ]
    for row in _mapping_list(payload.get("groups")):
        lines.append(
            f"- {row.get('name')}: {row.get('coverage_status')} ({row.get('evidence_basis')})"
        )
        missing = _string_list(row.get("missing_members"))
        if missing:
            lines.append(f"  missing: {', '.join(missing)}")
    return lines


def _render_inventory_classification(payload: dict[str, object]) -> list[str]:
    lines = ["Isomer live skill inventory classification"]
    for row in _mapping_list(payload.get("groups")):
        lines.append(f"- {row.get('name')}: {row.get('coverage_status')}")
        missing = _string_list(row.get("missing_members"))
        if missing and row.get("coverage_status") == "partial":
            lines.append(f"  missing: {', '.join(missing)}")
    unmatched = _mapping_list(payload.get("unmatched_skills"))
    if unmatched:
        lines.append(f"Unmatched ambient skills: {', '.join(str(item.get('name')) for item in unmatched)}")
    return lines


def _mapping_list(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


__all__: Sequence[str] = ("register_internal_commands",)
