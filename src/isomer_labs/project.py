"""Project discovery and loading."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

from isomer_labs.diagnostics import Diagnostic
from isomer_labs.manifest import parse_project_manifest
from isomer_labs.models import Project
from isomer_labs.path_utils import canonicalize
from isomer_labs.toml_loader import load_toml


PROJECT_CONFIG_DIR_NAME = ".isomer-labs"
PROJECT_MANIFEST_NAME = "manifest.toml"


def discover_project(
    *,
    cwd: Path,
    env: Mapping[str, str],
    project_selector: str | None = None,
    manifest_selector: str | None = None,
) -> tuple[Project | None, list[Diagnostic]]:
    if manifest_selector is not None:
        return _load_project_from_manifest_path(
            canonicalize(Path(manifest_selector)),
            "explicit Project Manifest selector",
        )
    if project_selector is not None:
        return _load_project_from_project_selector(canonicalize(Path(project_selector)), "explicit Project selector")

    discovered = find_ancestor_manifest(canonicalize(cwd))
    if discovered is not None:
        return _load_project_from_manifest_path(discovered, "current directory")

    env_manifest = env.get("ISOMER_PROJECT_MANIFEST")
    if env_manifest:
        return _load_project_from_manifest_path(canonicalize(Path(env_manifest)), "env:ISOMER_PROJECT_MANIFEST")

    env_root = env.get("ISOMER_PROJECT_ROOT")
    if env_root:
        return _load_project_from_project_selector(canonicalize(Path(env_root)), "env:ISOMER_PROJECT_ROOT")

    env_config = env.get("ISOMER_PROJECT_CONFIG_DIR")
    if env_config:
        manifest_path = canonicalize(Path(env_config) / PROJECT_MANIFEST_NAME)
        return _load_project_from_manifest_path(manifest_path, "env:ISOMER_PROJECT_CONFIG_DIR")

    return None, [
        Diagnostic(
            code="ISO001",
            severity="error",
            concept="Project",
            message="No Project Manifest was found from selectors, current directory, or supported Project environment overrides.",
        )
    ]


def manifest_path_for_root(project_root: Path) -> Path:
    return canonicalize(project_root / PROJECT_CONFIG_DIR_NAME / PROJECT_MANIFEST_NAME)


def config_dir_for_root(project_root: Path) -> Path:
    return canonicalize(project_root / PROJECT_CONFIG_DIR_NAME)


def project_root_for_manifest(manifest_path: Path) -> Path:
    if manifest_path.parent.name == PROJECT_CONFIG_DIR_NAME:
        return canonicalize(manifest_path.parent.parent)
    return canonicalize(manifest_path.parent)


def _load_project_from_project_selector(path: Path, source: str) -> tuple[Project | None, list[Diagnostic]]:
    if path.name == PROJECT_MANIFEST_NAME:
        return _load_project_from_manifest_path(path, source)
    return _load_project_from_manifest_path(manifest_path_for_root(path), source)


def _load_project_from_manifest_path(manifest_path: Path, source: str) -> tuple[Project | None, list[Diagnostic]]:
    raw, diagnostics = load_toml(manifest_path, "Project Manifest")
    if raw is None:
        return None, diagnostics
    manifest, parse_diagnostics = parse_project_manifest(manifest_path, raw)
    diagnostics.extend(parse_diagnostics)
    project_root = project_root_for_manifest(manifest_path)
    project = Project(
        root=project_root,
        config_dir=canonicalize(manifest_path.parent),
        manifest_path=manifest_path,
        manifest=manifest,
        discovery_source=source,
    )
    return project, diagnostics


def find_ancestor_manifest(cwd: Path) -> Path | None:
    current = cwd
    if current.is_file():
        current = current.parent
    for directory in (current, *current.parents):
        manifest_path = manifest_path_for_root(directory)
        if manifest_path.exists():
            return manifest_path
    return None
