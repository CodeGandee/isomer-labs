"""Click commands for packaged Isomer system skill installation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import click

from isomer_labs.cli.options import CliOptions
from isomer_labs.cli.output import output_format
from isomer_labs.core.rendering import render_json
from isomer_labs.skills.installer import (
    SUPPORTED_TARGETS,
    SystemSkillInstallError,
    inspect_system_skills,
    install_system_skills,
    list_packaged_system_skills,
    resolve_system_skill_selection,
    resolve_targets,
    uninstall_system_skills,
)
from isomer_labs.skills.system_assets import iter_system_skill_groups


def register_system_skill_commands(app: click.Group) -> None:
    @app.group(name="system-skills", help="Install and inspect packaged Isomer system skills.")
    def system_skills_group() -> None:
        pass

    @system_skills_group.command(name="list", help="List packaged Isomer system skills.")
    @click.pass_context
    def system_skills_list_command(ctx: click.Context) -> int:
        options = _root_options(ctx)
        groups = list(iter_system_skill_groups())
        skills = list_packaged_system_skills()
        payload = {
            "ok": True,
            "mutated": False,
            "groups": [
                {
                    "name": group.name,
                    "description": group.description,
                    "kind": group.kind,
                    "always_available": group.always_available,
                    "extension_id": group.extension_id,
                    "skills": [Path(skill_path).name for skill_path in group.skills],
                    "source_paths": list(group.skills),
                }
                for group in groups
            ],
            "extensions": [
                {
                    "extension_id": group.extension_id,
                    "group": group.name,
                    "description": group.description,
                    "skills": [Path(skill_path).name for skill_path in group.skills],
                }
                for group in groups
                if group.kind == "extension"
            ],
            "skills": [skill.to_json() for skill in skills],
            "supported_targets": list(SUPPORTED_TARGETS),
        }
        return _emit("system-skills list", options, payload, _render_list(payload))

    @system_skills_group.command(name="status", help="Show installed packaged Isomer system skills for one target.")
    @_target_options
    @_selection_options
    @click.pass_context
    def system_skills_status_command(
        ctx: click.Context,
        target: str,
        home: Path | None,
        groups: tuple[str, ...],
        extensions: tuple[str, ...],
        all_extensions: bool,
        skills: tuple[str, ...],
    ) -> int:
        options = _root_options(ctx)
        try:
            selection = _resolve_selection_for_read(
                groups=groups,
                extensions=extensions,
                all_extensions=all_extensions,
                skills=skills,
            )
            targets = resolve_targets(target, home=home)
            statuses = [inspect_system_skills(item, selection).to_json() for item in targets]
        except SystemSkillInstallError as exc:
            raise click.ClickException(str(exc)) from exc
        payload: dict[str, object] = {
            "ok": True,
            "mutated": False,
            "targets": statuses,
        }
        if len(statuses) == 1:
            payload.update(statuses[0])
        return _emit("system-skills status", options, payload, _render_statuses(statuses))

    @system_skills_group.command(name="install", help="Install packaged Isomer system skills into a target tool skill root.")
    @_target_options
    @_selection_options
    @click.option(
        "--mode",
        "projection_mode",
        type=click.Choice(["copy", "symlink"]),
        default="copy",
        show_default=True,
        help="Projection mode for installed skill directories.",
    )
    @click.pass_context
    def system_skills_install_command(
        ctx: click.Context,
        target: str,
        home: Path | None,
        groups: tuple[str, ...],
        extensions: tuple[str, ...],
        all_extensions: bool,
        skills: tuple[str, ...],
        projection_mode: str,
    ) -> int:
        options = _root_options(ctx)
        try:
            selection = resolve_system_skill_selection(
                groups=groups,
                extensions=extensions,
                all_extensions=all_extensions,
                skills=skills,
                default_core=True,
            )
            targets = resolve_targets(target, home=home)
            results = [
                install_system_skills(item, selection, projection_mode=projection_mode)  # type: ignore[arg-type]
                for item in targets
            ]
        except SystemSkillInstallError as exc:
            raise click.ClickException(str(exc)) from exc
        result_payloads = [result.to_json() for result in results]
        ok = all(result.ok for result in results)
        payload: dict[str, object] = {
            "ok": ok,
            "mutated": any(result.installed for result in results),
            "targets": result_payloads,
        }
        if len(result_payloads) == 1:
            payload.update(result_payloads[0])
        return _emit("system-skills install", options, payload, _render_installs(result_payloads))

    @system_skills_group.command(name="uninstall", help="Remove Isomer-owned packaged system skill projections.")
    @_target_options
    @_selection_options
    @click.pass_context
    def system_skills_uninstall_command(
        ctx: click.Context,
        target: str,
        home: Path | None,
        groups: tuple[str, ...],
        extensions: tuple[str, ...],
        all_extensions: bool,
        skills: tuple[str, ...],
    ) -> int:
        options = _root_options(ctx)
        try:
            selection = _resolve_selection_for_read(
                groups=groups,
                extensions=extensions,
                all_extensions=all_extensions,
                skills=skills,
            )
            targets = resolve_targets(target, home=home)
            results = [uninstall_system_skills(item, selection) for item in targets]
        except SystemSkillInstallError as exc:
            raise click.ClickException(str(exc)) from exc
        result_payloads = [result.to_json() for result in results]
        payload: dict[str, object] = {
            "ok": True,
            "mutated": any(result.removed for result in results),
            "targets": result_payloads,
        }
        if len(result_payloads) == 1:
            payload.update(result_payloads[0])
        return _emit("system-skills uninstall", options, payload, _render_uninstalls(result_payloads))


def _target_options(func: Any) -> Any:
    func = click.option(
        "--home",
        type=click.Path(path_type=Path, file_okay=False, dir_okay=True),
        help="Optional skill root override for one concrete target.",
    )(func)
    func = click.option(
        "--target",
        required=True,
        type=click.Choice(SUPPORTED_TARGETS),
        help=f"Install target ({', '.join(SUPPORTED_TARGETS)}).",
    )(func)
    return func


def _selection_options(func: Any) -> Any:
    func = click.option("--skill", "skills", multiple=True, help="Explicit packaged skill name to select.")(func)
    func = click.option("--all-extensions", is_flag=True, help="Include every packaged extension group.")(func)
    func = click.option("--extension", "extensions", multiple=True, help="Packaged extension id to include.")(func)
    func = click.option("--group", "groups", multiple=True, help="Packaged system-skill group to select.")(func)
    return func


def _root_options(ctx: click.Context) -> CliOptions:
    root_options = ctx.find_root().obj
    return root_options if isinstance(root_options, CliOptions) else CliOptions()


def _resolve_selection_for_read(
    *,
    groups: Sequence[str],
    extensions: Sequence[str],
    all_extensions: bool,
    skills: Sequence[str],
) -> Any:
    if groups or extensions or all_extensions or skills:
        return resolve_system_skill_selection(
            groups=groups,
            extensions=extensions,
            all_extensions=all_extensions,
            skills=skills,
            default_core=True,
        )
    return resolve_system_skill_selection(
        groups=tuple(group.name for group in iter_system_skill_groups()),
        default_core=False,
    )


def _emit(command: str, options: CliOptions, payload: dict[str, object], text_lines: list[str]) -> int:
    if output_format(options) == "json":
        click.echo(render_json(command, payload, []))
    else:
        click.echo("\n".join(text_lines))
    return 0 if payload.get("ok") is not False else 1


def _render_list(payload: dict[str, object]) -> list[str]:
    lines = ["Packaged Isomer system skills:"]
    for group in _mapping_list(payload.get("groups")):
        extension = group.get("extension_id")
        suffix = f" extension={extension}" if extension else ""
        lines.append(f"- {group.get('name')} ({group.get('kind')}{suffix})")
        for skill in _string_list(group.get("skills")):
            lines.append(f"  - {skill}")
    lines.append(f"Targets: {', '.join(_string_list(payload.get('supported_targets')))}")
    return lines


def _render_statuses(statuses: list[dict[str, object]]) -> list[str]:
    lines = ["Isomer system skill status:"]
    for status in statuses:
        lines.append(f"- {status.get('target')}: {status.get('skill_root')}")
        lines.append(f"  installed: {', '.join(_string_list(status.get('installed_skills'))) or '(none)'}")
        lines.append(f"  missing: {', '.join(_string_list(status.get('missing_skills'))) or '(none)'}")
        collisions = _mapping_list(status.get("unmanaged_collisions"))
        if collisions:
            lines.append("  unmanaged collisions:")
            for collision in collisions:
                lines.append(f"    - {collision.get('name')}: {collision.get('path')}")
    return lines


def _render_installs(results: list[dict[str, object]]) -> list[str]:
    lines = ["Installed Isomer system skills:"]
    for result in results:
        lines.append(f"- {result.get('target')}: {result.get('skill_root')}")
        installed = _string_list(result.get("installed_skills"))
        lines.append(f"  installed: {', '.join(installed) or '(none)'}")
        collisions = _mapping_list(result.get("unmanaged_collisions"))
        if collisions:
            lines.append("  unmanaged collisions:")
            for collision in collisions:
                lines.append(f"    - {collision.get('name')}: {collision.get('path')}")
    return lines


def _render_uninstalls(results: list[dict[str, object]]) -> list[str]:
    lines = ["Removed Isomer system skills:"]
    for result in results:
        lines.append(f"- {result.get('target')}: {result.get('skill_root')}")
        lines.append(f"  removed: {', '.join(_string_list(result.get('removed_skills'))) or '(none)'}")
        lines.append(f"  absent: {', '.join(_string_list(result.get('absent_skills'))) or '(none)'}")
        preserved = _mapping_list(result.get("preserved_unmanaged"))
        if preserved:
            lines.append("  preserved unmanaged:")
            for collision in preserved:
                lines.append(f"    - {collision.get('name')}: {collision.get('path')}")
    return lines


def _mapping_list(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


__all__ = ["register_system_skill_commands"]
