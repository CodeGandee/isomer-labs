"""Click commands for packaged Isomer system skill installation."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

import click

from isomer_labs.cli.options import CliOptions
from isomer_labs.cli.output import output_format
from isomer_labs.core.diagnostics import Diagnostic
from isomer_labs.core.rendering import render_json
from isomer_labs.skills.installer import (
    SUPPORTED_SCOPES,
    SUPPORTED_TARGETS,
    SystemSkillInstallError,
    SystemSkillScope,
    inspect_system_skills,
    install_system_skills,
    list_packaged_system_skills,
    resolve_system_skill_selection,
    resolve_targets,
    uninstall_system_skills,
    upgrade_system_skills,
)
from isomer_labs.skills.system_assets import (
    SystemSkillExtension,
    iter_system_skill_extensions,
    iter_system_skill_groups,
    system_skill_catalog,
)


def register_system_skill_commands(app: click.Group) -> None:
    @app.group(name="system-skills", help="Discover, install, and inspect packaged Isomer system skills.")
    def system_skills_group() -> None:
        pass

    @system_skills_group.group(name="extensions", help="Discover optional packaged agent-skill extensions.")
    def system_skill_extensions_group() -> None:
        pass

    @system_skill_extensions_group.command(name="list", help="List packaged agent-skill extensions.")
    @click.pass_context
    def system_skill_extensions_list_command(ctx: click.Context) -> int:
        options = _root_options(ctx)
        extensions = [_extension_payload(extension) for extension in iter_system_skill_extensions()]
        payload: dict[str, object] = {
            "ok": True,
            "mutated": False,
            "extensions": extensions,
        }
        return _emit("system-skills extensions list", options, payload, _render_extension_list(extensions))

    @system_skill_extensions_group.command(name="show", help="Show one packaged agent-skill extension.")
    @click.argument("extension_id")
    @click.pass_context
    def system_skill_extensions_show_command(ctx: click.Context, extension_id: str) -> int:
        options = _root_options(ctx)
        extension = next(
            (item for item in iter_system_skill_extensions() if item.extension_id == extension_id),
            None,
        )
        if extension is None:
            raise click.ClickException(f"Unknown packaged system extension: {extension_id}")
        extension_payload = _extension_payload(extension)
        payload: dict[str, object] = {
            "ok": True,
            "mutated": False,
            "extension": extension_payload,
        }
        return _emit("system-skills extensions show", options, payload, _render_extension_show(extension_payload))

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
                    "entry_skill": group.entry_skill,
                    "commands": list(group.commands),
                    "skills": [Path(skill_path).name for skill_path in group.skills],
                    "source_paths": list(group.skills),
                }
                for group in groups
            ],
            "extensions": [
                _extension_payload(extension)
                for extension in iter_system_skill_extensions()
            ],
            "skills": [skill.to_json() for skill in skills],
            "supported_targets": list(SUPPORTED_TARGETS),
            "supported_scopes": list(SUPPORTED_SCOPES),
        }
        return _emit("system-skills list", options, payload, _render_list(payload))

    @system_skills_group.command(name="status", help="Show installed packaged Isomer system skills for one target.")
    @_target_options
    @_selection_options
    @click.pass_context
    def system_skills_status_command(
        ctx: click.Context,
        target: str,
        scope: SystemSkillScope,
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
            targets = resolve_targets(target, scope=scope)
            results = [inspect_system_skills(item, selection) for item in targets]
        except SystemSkillInstallError as exc:
            raise click.ClickException(str(exc)) from exc
        statuses = [result.to_json() for result in results]
        diagnostics = _result_diagnostics(results)
        payload: dict[str, object] = {
            "ok": True,
            "mutated": False,
            "targets": statuses,
        }
        if len(statuses) == 1:
            payload.update(statuses[0])
        return _emit("system-skills status", options, payload, _render_statuses(statuses), diagnostics)

    @system_skills_group.command(name="install", help="Install packaged Isomer system skills into a target tool skill root.")
    @_install_target_options
    @_selection_options
    @click.option(
        "--mode",
        "projection_mode",
        type=click.Choice(["copy", "symlink"]),
        default="copy",
        show_default=True,
        help="Projection mode for installed skill directories.",
    )
    @click.option("--force", is_flag=True, help="Replace existing selected skill paths before installing.")
    @click.pass_context
    def system_skills_install_command(
        ctx: click.Context,
        target: str,
        scope: SystemSkillScope,
        groups: tuple[str, ...],
        extensions: tuple[str, ...],
        all_extensions: bool,
        skills: tuple[str, ...],
        projection_mode: str,
        force: bool,
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
            targets = resolve_targets(target, scope=scope)
            results = [
                install_system_skills(item, selection, projection_mode=projection_mode, force=force)  # type: ignore[arg-type]
                for item in targets
            ]
        except SystemSkillInstallError as exc:
            raise click.ClickException(str(exc)) from exc
        result_payloads = [result.to_json() for result in results]
        diagnostics = _result_diagnostics(results)
        ok = all(result.ok for result in results)
        payload: dict[str, object] = {
            "ok": ok,
            "mutated": any(result.mutated for result in results),
            "targets": result_payloads,
        }
        if len(result_payloads) == 1:
            payload.update(result_payloads[0])
        return _emit("system-skills install", options, payload, _render_installs(result_payloads), diagnostics)

    @system_skills_group.command(name="upgrade", help="Refresh packaged system skills and remove stale manifest-tracked projections.")
    @_target_options
    @_selection_options
    @click.option(
        "--mode",
        "projection_mode",
        type=click.Choice(["copy", "symlink"]),
        default=None,
        help="Projection mode override for refreshed skill directories.",
    )
    @click.pass_context
    def system_skills_upgrade_command(
        ctx: click.Context,
        target: str,
        scope: SystemSkillScope,
        groups: tuple[str, ...],
        extensions: tuple[str, ...],
        all_extensions: bool,
        skills: tuple[str, ...],
        projection_mode: str | None,
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
            targets = resolve_targets(target, scope=scope)
            results = [
                upgrade_system_skills(item, selection, projection_mode=projection_mode)  # type: ignore[arg-type]
                for item in targets
            ]
        except SystemSkillInstallError as exc:
            raise click.ClickException(str(exc)) from exc
        result_payloads = [result.to_json() for result in results]
        diagnostics = _result_diagnostics(results)
        payload: dict[str, object] = {
            "ok": all(result.ok for result in results),
            "mutated": any(result.mutated for result in results),
            "targets": result_payloads,
        }
        if len(result_payloads) == 1:
            payload.update(result_payloads[0])
        return _emit("system-skills upgrade", options, payload, _render_upgrades(result_payloads), diagnostics)

    @system_skills_group.command(name="uninstall", help="Remove Isomer-owned packaged system skill projections.")
    @_target_options
    @_selection_options
    @click.pass_context
    def system_skills_uninstall_command(
        ctx: click.Context,
        target: str,
        scope: SystemSkillScope,
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
            targets = resolve_targets(target, scope=scope)
            results = [uninstall_system_skills(item, selection) for item in targets]
        except SystemSkillInstallError as exc:
            raise click.ClickException(str(exc)) from exc
        result_payloads = [result.to_json() for result in results]
        diagnostics = _result_diagnostics(results)
        payload: dict[str, object] = {
            "ok": True,
            "mutated": any(result.mutated for result in results),
            "targets": result_payloads,
        }
        if len(result_payloads) == 1:
            payload.update(result_payloads[0])
        return _emit("system-skills uninstall", options, payload, _render_uninstalls(result_payloads), diagnostics)


def _target_options(func: Any) -> Any:
    func = click.option(
        "--scope",
        required=True,
        type=click.Choice(SUPPORTED_SCOPES),
        help="Installation scope: current user or current working directory project.",
    )(func)
    func = click.option(
        "--target",
        required=True,
        type=click.Choice(SUPPORTED_TARGETS),
        help=f"Install target ({', '.join(SUPPORTED_TARGETS)}).",
    )(func)
    return func


def _install_target_options(func: Any) -> Any:
    func = click.option(
        "--scope",
        default="project",
        show_default=True,
        type=click.Choice(SUPPORTED_SCOPES),
        help="Installation scope: current user or current working directory project.",
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
    func = click.option(
        "--extension",
        "extensions",
        multiple=True,
        type=click.Choice(tuple(extension.extension_id for extension in iter_system_skill_extensions())),
        help="Packaged agent-skill extension id to include.",
    )(func)
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


def _emit(
    command: str,
    options: CliOptions,
    payload: dict[str, object],
    text_lines: list[str],
    diagnostics: Sequence[Diagnostic] = (),
) -> int:
    if output_format(options) == "json":
        click.echo(render_json(command, payload, list(diagnostics)))
    else:
        click.echo("\n".join(text_lines))
        for diagnostic in diagnostics:
            click.echo(diagnostic.render())
    return 0 if payload.get("ok") is not False else 1


def _result_diagnostics(results: Sequence[Any]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for result in results:
        diagnostics.extend(getattr(result, "diagnostics", ()))
    return diagnostics


def _render_list(payload: dict[str, object]) -> list[str]:
    lines = ["Packaged Isomer public skill packs:"]
    for pack in _mapping_list(payload.get("skills")):
        extension = pack.get("extension_id")
        suffix = f", extension={extension}" if extension else ""
        lines.append(f"- {pack.get('name')} (pack={pack.get('pack_id')}, {pack.get('group_kind')}{suffix})")
        commands = _string_list(pack.get("public_commands"))
        lines.append(f"  public commands: {', '.join(commands) or '(none)'}")
        lines.append("  protected members:")
        for member in _mapping_list(pack.get("protected_members")):
            lines.append(
                f"    - {member.get('logical_id')} ({member.get('member_name')}): "
                f"{member.get('invocation_designator')} [{member.get('relative_path')}]"
            )
    lines.append(f"Targets: {', '.join(_string_list(payload.get('supported_targets')))}")
    lines.append(f"Scopes: {', '.join(_string_list(payload.get('supported_scopes')))}")
    return lines


def _extension_payload(extension: SystemSkillExtension) -> dict[str, object]:
    extension_id = extension.extension_id
    entry_skill = extension.entry_skill
    catalog = system_skill_catalog()
    pack = catalog.pack_for_extension(extension_id)
    protected_members = [
        {
            "logical_id": capability.logical_id,
            "member_name": capability.member_name,
            "invocation_designator": capability.invocation_designator,
            "source_path": capability.source_path,
            "dependencies": list(capability.dependencies),
        }
        for capability in catalog.capabilities
        if capability.pack_id == pack.pack_id
    ]
    return {
        "extension_id": extension_id,
        "group": extension.group,
        "pack_id": pack.pack_id,
        "description": extension.description,
        "entry_skill": entry_skill,
        "commands": list(extension.commands),
        "skills": [Path(skill_path).name for skill_path in extension.skills],
        "protected_members": protected_members,
        "install_command": (
            f"isomer-cli system-skills install --target <target> --extension {extension_id}"
        ),
        "status_command": (
            f"isomer-cli system-skills status --target <target> --scope <scope> --extension {extension_id}"
        ),
        "invocation": f"${entry_skill}",
    }


def _render_extension_list(extensions: list[dict[str, object]]) -> list[str]:
    lines = ["Packaged Isomer agent-skill extensions:"]
    for extension in extensions:
        lines.append(f"- {extension.get('extension_id')}: {extension.get('description')}")
        lines.append(f"  entry skill: {extension.get('invocation')}")
        lines.append(f"  inspect: isomer-cli system-skills extensions show {extension.get('extension_id')}")
    lines.append("Runtime and compatibility CLI commands are listed under: isomer-cli ext --help")
    return lines


def _render_extension_show(extension: dict[str, object]) -> list[str]:
    lines = [
        f"Packaged Isomer agent-skill extension: {extension.get('extension_id')}",
        f"Description: {extension.get('description')}",
        f"Entry skill: {extension.get('invocation')}",
        "Commands:",
    ]
    invocation = extension.get("invocation")
    for command in _string_list(extension.get("commands")):
        lines.append(f"- {invocation} use {command} to <task>")
    lines.extend(
        (
            "Public packs:",
            *[f"- {skill}" for skill in _string_list(extension.get("skills"))],
            "Protected members:",
            *[
                f"- {member.get('logical_id')}: {member.get('invocation_designator')}"
                for member in _mapping_list(extension.get("protected_members"))
            ],
            f"Install: {extension.get('install_command')}",
            f"Status: {extension.get('status_command')}",
            "This is an agent-skill extension; runtime and compatibility CLI commands are listed under isomer-cli ext --help.",
        )
    )
    return lines


def _render_statuses(statuses: list[dict[str, object]]) -> list[str]:
    lines = ["Isomer system skill status:"]
    for status in statuses:
        lines.append(_render_destination_heading(status))
        lines.append(f"  installed: {', '.join(_string_list(status.get('installed_skills'))) or '(none)'}")
        lines.append(f"  missing: {', '.join(_string_list(status.get('missing_skills'))) or '(none)'}")
        invalid = _mapping_list(status.get("invalid_projections"))
        if invalid:
            lines.append("  invalid projections:")
            for projection in invalid:
                lines.append(f"    - {projection.get('name')}: {projection.get('path')} ({projection.get('path_kind')})")
        for pack in _mapping_list(status.get("installed")):
            lines.append(
                f"  pack {pack.get('name')}: {pack.get('pack_status')} "
                f"({len(_mapping_list(pack.get('protected_members')))} protected members)"
            )
            missing_members = _string_list(pack.get("missing_protected_members"))
            if missing_members:
                lines.append(f"    missing protected members: {', '.join(missing_members)}")
        manifest = status.get("manifest")
        if isinstance(manifest, dict):
            lines.append(f"  manifest: {manifest.get('path')}")
            lines.append(f"  manifest package version: {manifest.get('package_version') or '(unknown)'}")
    return lines


def _render_installs(results: list[dict[str, object]]) -> list[str]:
    lines = ["Installed Isomer system skills:"]
    for result in results:
        lines.append(_render_destination_heading(result))
        installed = _string_list(result.get("installed_skills"))
        lines.append(f"  installed: {', '.join(installed) or '(none)'}")
        replaced = _string_list(result.get("replaced_skills"))
        if replaced:
            lines.append(f"  replaced: {', '.join(replaced)}")
        preserved = _mapping_list(result.get("preserved_existing"))
        if preserved:
            lines.append("  preserved existing:")
            for item in preserved:
                lines.append(f"    - {item.get('name')}: {item.get('path')} ({item.get('path_kind')})")
        manifest = result.get("manifest")
        if isinstance(manifest, dict):
            lines.append(f"  manifest: {manifest.get('path')}")
    return lines


def _render_upgrades(results: list[dict[str, object]]) -> list[str]:
    lines = ["Upgraded Isomer system skills:"]
    for result in results:
        lines.append(_render_destination_heading(result))
        lines.append(f"  refreshed: {', '.join(_string_list(result.get('refreshed_skills'))) or '(none)'}")
        lines.append(f"  stale removed: {', '.join(_string_list(result.get('stale_removed_skills'))) or '(none)'}")
        stale_absent = _string_list(result.get("stale_absent_skills"))
        if stale_absent:
            lines.append(f"  stale absent: {', '.join(stale_absent)}")
        retained = _mapping_list(result.get("stale_retained"))
        if retained:
            lines.append("  stale retained for repair:")
            for item in retained:
                lines.append(f"    - {item.get('name')}: {item.get('path')}")
        manifest = result.get("manifest")
        if isinstance(manifest, dict):
            lines.append(f"  manifest: {manifest.get('path')}")
    return lines


def _render_uninstalls(results: list[dict[str, object]]) -> list[str]:
    lines = ["Removed Isomer system skills:"]
    for result in results:
        lines.append(_render_destination_heading(result))
        lines.append(f"  removed: {', '.join(_string_list(result.get('removed_skills'))) or '(none)'}")
        lines.append(f"  absent: {', '.join(_string_list(result.get('absent_skills'))) or '(none)'}")
        manifest = result.get("manifest")
        if isinstance(manifest, dict):
            lines.append(f"  manifest: {manifest.get('path')}")
    return lines


def _mapping_list(value: object) -> list[dict[str, object]]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, dict)]


def _render_destination_heading(payload: dict[str, object]) -> str:
    bindings = _mapping_list(payload.get("bindings"))
    labels = [f"{binding.get('target')}/{binding.get('scope')}" for binding in bindings]
    label = ", ".join(labels) or f"{payload.get('target')}/{payload.get('scope') or 'unknown'}"
    return f"- {label}: {payload.get('skill_root')}"


def _string_list(value: object) -> list[str]:
    if not isinstance(value, list):
        return []
    return [item for item in value if isinstance(item, str)]


__all__ = ["register_system_skill_commands"]
