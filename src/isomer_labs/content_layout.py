"""Shared defaults for Isomer-generated Project content."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from isomer_labs.path_utils import display_path, resolve_project_path


ISOMER_CONTENT_ROOT_DIR = "isomer-content"
TOPIC_WORKSPACE_BASE_DIR = f"{ISOMER_CONTENT_ROOT_DIR}/topic-ws"
TOPIC_WORKSPACE_BASE_NAME = "topic-ws"

CONTENT_ROOT_README_TEXT = """# Isomer Content

This directory is the default Project-local home for Isomer-generated content.

Fresh Projects ignore generated content under this root by default. The generated `.gitignore` keeps this `README.md` and the `.gitignore` policy file trackable, while Topic Workspaces and other generated files stay local unless you intentionally track selected files.

Default Topic Workspaces live under `topic-ws/<topic-id>/`.
"""

CONTENT_ROOT_GITIGNORE_TEXT = """*
!.gitignore
!/README.md
"""


def content_path_defaults_for_init(project_root: Path, content_dir: str | None = None) -> dict[str, str]:
    content_root = selected_content_root_path(project_root, content_dir)
    content_root_input = display_path(content_root, project_root)
    return {
        "isomer_content_root": content_root_input,
        "topic_workspace_base_dir": f"{content_root_input}/{TOPIC_WORKSPACE_BASE_NAME}",
    }


def selected_content_root_path(project_root: Path, content_dir: str | None = None) -> Path:
    if content_dir is not None and content_dir:
        return resolve_project_path(project_root, content_dir)
    return project_root / ISOMER_CONTENT_ROOT_DIR


def content_root_path(project_root: Path, path_defaults: Mapping[str, object] | None = None) -> Path:
    value = _path_default(path_defaults, "isomer_content_root")
    if value is not None:
        return resolve_project_path(project_root, value)
    return project_root / ISOMER_CONTENT_ROOT_DIR


def topic_workspace_base_path(project_root: Path, path_defaults: Mapping[str, object] | None = None) -> Path:
    value = _path_default(path_defaults, "topic_workspace_base_dir")
    if value is not None:
        return resolve_project_path(project_root, value)
    return content_root_path(project_root, path_defaults) / TOPIC_WORKSPACE_BASE_NAME


def topic_workspace_path(
    project_root: Path,
    topic_id: str,
    path_defaults: Mapping[str, object] | None = None,
) -> Path:
    return topic_workspace_base_path(project_root, path_defaults) / topic_id


def topic_workspace_path_input(topic_id: str) -> str:
    return f"{TOPIC_WORKSPACE_BASE_DIR}/{topic_id}"


def topic_workspace_path_input_from_defaults(topic_id: str, path_defaults: Mapping[str, object]) -> str:
    base = _path_default(path_defaults, "topic_workspace_base_dir") or TOPIC_WORKSPACE_BASE_DIR
    return f"{base}/{topic_id}"


def _path_default(path_defaults: Mapping[str, object] | None, key: str) -> str | None:
    if path_defaults is None:
        return None
    value = path_defaults.get(key)
    if isinstance(value, str) and value:
        return value
    return None
