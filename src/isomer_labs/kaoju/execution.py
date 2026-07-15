"""Provider-neutral Execution Adapter Command Requests for Kaoju services."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import subprocess
import time
from typing import Mapping, Sequence
import uuid


KAOJU_EXTENSION_POINTS = {
    "pixi_mutation",
    "smoke_run",
    "code_trial",
    "document_build",
    "viewer_launch",
    "service_dispatch",
}


@dataclass(frozen=True)
class ExecutionAdapterCommandRequest:
    """Canonical provider-neutral request for one bounded executable operation."""

    id: str
    extension_point: str
    argv: tuple[str, ...]
    cwd: Path
    timeout_seconds: float
    recording_refs: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        *,
        extension_point: str,
        argv: Sequence[str],
        cwd: Path,
        timeout_seconds: float,
        recording_refs: Sequence[str] = (),
    ) -> ExecutionAdapterCommandRequest:
        if extension_point not in KAOJU_EXTENSION_POINTS:
            raise ValueError(f"Unsupported Research Operation Extension Point: {extension_point}")
        if not argv or any(not value for value in argv):
            raise ValueError("Execution Adapter Command Request argv must be non-empty.")
        if extension_point in {"smoke_run", "code_trial"} and not uses_explicit_pixi_environment(argv):
            raise ValueError(f"{extension_point} must run through an explicit Pixi environment, not the ambient process environment.")
        if timeout_seconds <= 0:
            raise ValueError("Execution Adapter Command Request timeout must be positive.")
        return cls(
            id=f"command-request-{uuid.uuid4().hex[:12]}",
            extension_point=extension_point,
            argv=tuple(argv),
            cwd=cwd.resolve(strict=False),
            timeout_seconds=timeout_seconds,
            recording_refs=tuple(recording_refs),
        )

    def to_json(self) -> dict[str, object]:
        return {
            "id": self.id,
            "schema_version": "isomer-execution-adapter-command-request.v1",
            "extension_point": self.extension_point,
            "argv": list(self.argv),
            "cwd": str(self.cwd),
            "timeout_seconds": self.timeout_seconds,
            "recording_refs": list(self.recording_refs),
        }


def execute_command_request(
    request: ExecutionAdapterCommandRequest,
    *,
    env: Mapping[str, str],
) -> dict[str, object]:
    """Execute synchronously and return a stable terminal observation."""

    started = time.monotonic()
    selected_env = {str(key): str(value) for key, value in env.items()}
    try:
        completed = subprocess.run(
            list(request.argv),
            cwd=request.cwd,
            env=selected_env,
            text=True,
            capture_output=True,
            check=False,
            timeout=request.timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "request": request.to_json(),
            "status": "timed_out",
            "returncode": None,
            "stdout": _text(exc.stdout),
            "stderr": _text(exc.stderr),
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "recovery": "Inspect the stable command request ref and retry synchronously after resolving the timeout.",
        }
    except OSError as exc:
        return {
            "request": request.to_json(),
            "status": "failed",
            "returncode": None,
            "stdout": "",
            "stderr": str(exc),
            "elapsed_seconds": round(time.monotonic() - started, 6),
            "recovery": "Repair command availability or working-directory access, then retry the same recorded request.",
        }
    return {
        "request": request.to_json(),
        "status": "succeeded" if completed.returncode == 0 else "failed",
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "elapsed_seconds": round(time.monotonic() - started, 6),
    }


def command_environment(env: Mapping[str, str], additions: Mapping[str, str] | None = None) -> dict[str, str]:
    """Build a child environment without exposing values in the recorded envelope."""

    selected = {str(key): str(value) for key, value in env.items()}
    selected.update({str(key): str(value) for key, value in (additions or {}).items()})
    selected.setdefault("PATH", os.defpath)
    return selected


def uses_explicit_pixi_environment(argv: Sequence[str]) -> bool:
    """Return whether a command pins a named Pixi environment for execution."""

    if len(argv) < 4 or Path(argv[0]).name != "pixi" or argv[1] != "run":
        return False
    return any(value in {"--environment", "-e"} and index + 1 < len(argv) and bool(argv[index + 1]) for index, value in enumerate(argv[2:], start=2))


def _text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return str(value)
