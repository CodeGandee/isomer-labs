"""Click registration for the local Project web GUI."""

from __future__ import annotations

import os
from pathlib import Path

import click

from isomer_labs.cli.options import CliOptions
from isomer_labs.web.server import DEFAULT_HOST, DEFAULT_PORT, run_server


def register_web_commands(app: click.Group) -> None:
    @app.group(name="web", help="Local Project web GUI commands.")
    def web_group() -> None:
        pass

    @web_group.command(name="serve", help="Serve the local Project web GUI.")
    @click.option("--root", "project_root", default=None, help="Explicit Project root selector.")
    @click.option("--host", default=DEFAULT_HOST, show_default=True, help="Host interface to bind.")
    @click.option("--port", default=DEFAULT_PORT, show_default=True, type=int, help="Port to bind.")
    @click.option("--reload", is_flag=True, help="Reload the web service when Python files change.")
    @click.option("--no-browser", is_flag=True, help="Do not open a browser after starting.")
    @click.pass_context
    def serve_command(
        ctx: click.Context,
        project_root: str | None = None,
        host: str = DEFAULT_HOST,
        port: int = DEFAULT_PORT,
        reload: bool = False,
        no_browser: bool = False,
    ) -> int:
        parent_options = ctx.obj if isinstance(ctx.obj, CliOptions) else None
        selected_root = project_root or (parent_options.project if parent_options is not None else None) or os.getcwd()
        run_server(
            project_root=Path(str(selected_root)).expanduser().resolve(strict=False),
            host=host,
            port=port,
            reload=reload,
            open_browser=not no_browser,
        )
        return 0
