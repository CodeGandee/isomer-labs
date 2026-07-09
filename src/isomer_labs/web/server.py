"""Server entrypoint helpers for the local web GUI."""

from __future__ import annotations

import os
from pathlib import Path
import webbrowser

from fastapi import FastAPI

from .app import WebCacheMode, create_app


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_CACHE_MODE: WebCacheMode = "normal"


def run_server(
    *,
    project_root: Path,
    host: str = DEFAULT_HOST,
    port: int = DEFAULT_PORT,
    reload: bool = False,
    open_browser: bool = True,
    cache_mode: WebCacheMode = DEFAULT_CACHE_MODE,
) -> None:
    """Run the Project web GUI service."""

    import uvicorn

    os.environ["ISOMER_WEB_PROJECT_ROOT"] = str(project_root)
    os.environ["ISOMER_WEB_CACHE_MODE"] = cache_mode
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
    cache_mode = _cache_mode_from_env(os.environ.get("ISOMER_WEB_CACHE_MODE"))
    return create_app(project_root, cache_mode=cache_mode)


def _cache_mode_from_env(value: str | None) -> WebCacheMode:
    if value == "debug":
        return "debug"
    return DEFAULT_CACHE_MODE
