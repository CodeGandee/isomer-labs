"""Filesystem path helpers for project-scoped validation."""

from __future__ import annotations

from pathlib import Path


def canonicalize(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def resolve_project_path(project_root: Path, value: str) -> Path:
    candidate = Path(value).expanduser()
    if candidate.is_absolute():
        return canonicalize(candidate)
    return canonicalize(project_root / candidate)


def is_within(path: Path, root: Path) -> bool:
    try:
        canonicalize(path).relative_to(canonicalize(root))
    except ValueError:
        return False
    return True


def display_path(path: Path, root: Path) -> str:
    try:
        return str(canonicalize(path).relative_to(canonicalize(root)))
    except ValueError:
        return str(canonicalize(path))
