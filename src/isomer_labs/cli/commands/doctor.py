"""Click registration for doctor diagnostics commands."""

from __future__ import annotations

import click

from isomer_labs.cli.handlers.project import _cmd_doctor
from isomer_labs.cli.options import (
    merge_options as _merge_options,
)


def register_doctor_commands(app: click.Group) -> None:
    @app.command(name="doctor", help="Run read-only dependency, Project, and topic diagnostics.")
    @click.option("--root", "project_root", default=None, help="Explicit Project root selector.")
    @click.option("--project", "project_alias", default=None, hidden=True, help="Compatibility alias for --root.")
    @click.option("--manifest", default=None, help="Explicit Project Manifest selector.")
    @click.option(
        "--with-topic",
        "doctor_topics",
        multiple=True,
        metavar="<research-topic-id>",
        help="Limit topic diagnostics to a Research Topic id. May be repeated.",
    )
    @click.pass_context
    def doctor_command(
        ctx: click.Context,
        project_root: str | None = None,
        project_alias: str | None = None,
        manifest: str | None = None,
        doctor_topics: tuple[str, ...] = (),
    ) -> int:
        selected_root = project_root if project_root is not None else project_alias
        return _cmd_doctor(
            _merge_options(
                ctx,
                project=selected_root,
                manifest=manifest,
                doctor_topics=doctor_topics,
            )
        )
