"""TOML loading with source-aware diagnostics."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import tomllib

from isomer_labs.core.diagnostics import Diagnostic


def load_toml(path: Path, concept: str) -> tuple[dict[str, Any] | None, list[Diagnostic]]:
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except FileNotFoundError:
        return None, [
            Diagnostic(
                code="ISO001",
                severity="error",
                concept=concept,
                path=path,
                message=f"{concept} file does not exist.",
            )
        ]
    except tomllib.TOMLDecodeError as exc:
        return None, [
            Diagnostic(
                code="ISO002",
                severity="error",
                concept=concept,
                path=path,
                message=f"{concept} TOML is malformed: {exc}",
            )
        ]
    except OSError as exc:
        return None, [
            Diagnostic(
                code="ISO001",
                severity="error",
                concept=concept,
                path=path,
                message=f"{concept} file could not be read: {exc}",
            )
        ]
    return data, []
