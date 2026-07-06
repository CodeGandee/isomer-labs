"""Server entrypoint helpers for the local web GUI."""

from __future__ import annotations

import os
from pathlib import Path
import webbrowser

from fastapi import FastAPI

from .app import create_app


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


def run_server(
    *,
    project_root: Path,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    reload: bool = False,
    open_browser: bool = True,
) -> None:
    """Run the Project web GUI service."""

    import uvicorn

    os.environ["ISOMER_WEB_PROJECT_ROOT"] = str(project_root)
    if open_browser:
        webbrowser.open(f"http://{host}:{port}/")
    uvicorn.run(
        "isomer_labs.web.server:create_app_from_env",
        factory=True,
        host=host,
        port=port,
        reload=reload,
    )


def create_app_from_env() -> FastAPI:
    """Create an app from the project root selected by the server CLI."""

    project_root = os.environ.get("ISOMER_WEB_PROJECT_ROOT")
    if project_root is None:
        project_root = str(Path.cwd())
    return create_app(project_root)
