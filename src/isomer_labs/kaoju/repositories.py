"""Verified canonical repository acquisition for Topic Workspaces."""

from __future__ import annotations

import os
from pathlib import Path
import re
import shutil
from typing import Mapping
import uuid

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.execution import ExecutionAdapterCommandRequest, command_environment, execute_command_request
from isomer_labs.models import EffectiveTopicContext
from isomer_labs.workspace.manifest import register_manifest_binding


REPO_LABEL_RE = re.compile(r"^topic\.repos\.[a-z0-9][a-z0-9_.-]*$")


class KaojuRepositoryService:
    """Acquire one immutable repository before making its semantic registration visible."""

    def __init__(self, context: EffectiveTopicContext, *, env: Mapping[str, str], cwd: Path) -> None:
        self.context = context
        self.env = env
        self.cwd = cwd

    def acquire(
        self,
        remote_url: str,
        *,
        semantic_label: str,
        history_depth: int = 1,
        timeout_seconds: float = 120.0,
    ) -> dict[str, object]:
        if not REPO_LABEL_RE.fullmatch(semantic_label) or semantic_label == "topic.repos.main":
            raise KaojuServiceError("repository_label_invalid", "Repository acquisition requires an exact non-main topic.repos.* semantic label.")
        if history_depth < 1:
            raise KaojuServiceError("repository_depth_invalid", "Repository history depth must be at least one.")
        suffix = semantic_label.removeprefix("topic.repos.")
        relative = Path("repos/extern").joinpath(*suffix.split("."))
        target = (self.context.topic_workspace_path / relative).resolve(strict=False)
        if target.exists():
            raise KaojuServiceError("repository_target_exists", f"Repository target already exists: {target}", ("Choose another semantic label.", "Inspect and explicitly register the existing checkout if it is authoritative."))
        target.parent.mkdir(parents=True, exist_ok=True)
        staged = target.parent / f".{target.name}.acquire-{uuid.uuid4().hex[:8]}"
        child_env = command_environment(self.env, {"GIT_TERMINAL_PROMPT": "0"})
        command_requests: list[dict[str, object]] = []
        preflight = ExecutionAdapterCommandRequest.create(
            extension_point="repository_acquisition",
            argv=("git", "ls-remote", "--exit-code", remote_url, "HEAD"),
            cwd=target.parent,
            timeout_seconds=timeout_seconds,
        )
        preflight_result = execute_command_request(preflight, env=child_env)
        command_requests.append(preflight_result)
        if preflight_result["status"] != "succeeded":
            raise self._acquisition_error("repository_remote_unreachable", remote_url, preflight_result)
        try:
            clone = ExecutionAdapterCommandRequest.create(
                extension_point="repository_acquisition",
                argv=("git", "clone", "--depth", "1", "--no-tags", "--", remote_url, str(staged)),
                cwd=target.parent,
                timeout_seconds=timeout_seconds,
            )
            clone_result = execute_command_request(clone, env=child_env)
            command_requests.append(clone_result)
            if clone_result["status"] != "succeeded":
                raise self._acquisition_error("repository_clone_failed", remote_url, clone_result)
            if history_depth > 1:
                deepen = ExecutionAdapterCommandRequest.create(
                    extension_point="repository_acquisition",
                    argv=("git", "fetch", "--deepen", str(history_depth - 1), "origin"),
                    cwd=staged,
                    timeout_seconds=timeout_seconds,
                )
                deepen_result = execute_command_request(deepen, env=child_env)
                command_requests.append(deepen_result)
                if deepen_result["status"] != "succeeded":
                    raise self._acquisition_error("repository_deepen_failed", remote_url, deepen_result)
            commit_result = self._git(staged, ("rev-parse", "HEAD"), timeout_seconds)
            command_requests.append(commit_result)
            validation_result = self._git(staged, ("fsck", "--connectivity-only"), timeout_seconds)
            command_requests.append(validation_result)
            if commit_result["status"] != "succeeded" or validation_result["status"] != "succeeded":
                raise KaojuServiceError("repository_validation_failed", "Cloned repository failed immutable-commit or connectivity validation.")
            commit = str(commit_result["stdout"]).strip().lower()
            if len(commit) != 40 or any(character not in "0123456789abcdef" for character in commit):
                raise KaojuServiceError("repository_commit_invalid", "Cloned repository did not resolve to a full immutable commit id.")
            os.replace(staged, target)
            manifest, _created, diagnostics = register_manifest_binding(
                self.context,
                label=semantic_label,
                path_template=relative.as_posix(),
                storage_profile="topic_repo",
                create=False,
            )
            if manifest is None or any(diagnostic.is_error for diagnostic in diagnostics):
                shutil.rmtree(target)
                messages = "; ".join(diagnostic.message for diagnostic in diagnostics)
                raise KaojuServiceError("repository_registration_failed", f"Repository validation succeeded but semantic registration failed: {messages}")
        finally:
            if staged.exists():
                shutil.rmtree(staged)
        return {
            "ok": True,
            "mutated": True,
            "operation": "repos.acquire",
            "repository": {
                "semantic_label": semantic_label,
                "remote_url": remote_url,
                "commit": commit,
                "depth": history_depth,
                "shallow": _is_shallow(target),
                "path": str(target),
            },
            "command_requests": command_requests,
            "affected_refs": [semantic_label, f"git:{commit}"],
            "recovery_actions": [],
        }

    def _git(self, cwd: Path, arguments: tuple[str, ...], timeout_seconds: float) -> dict[str, object]:
        request = ExecutionAdapterCommandRequest.create(extension_point="repository_acquisition", argv=("git", *arguments), cwd=cwd, timeout_seconds=timeout_seconds)
        return execute_command_request(request, env=command_environment(self.env, {"GIT_TERMINAL_PROMPT": "0"}))

    def _acquisition_error(self, code: str, remote_url: str, result: dict[str, object]) -> KaojuServiceError:
        stderr = str(result.get("stderr") or "")
        selected_code = "repository_authentication_failed" if any(marker in stderr.lower() for marker in ("authentication", "permission denied", "could not read username")) else code
        request = result.get("request")
        request_ref = request.get("id") if isinstance(request, dict) else None
        return KaojuServiceError(selected_code, f"Repository acquisition failed for {remote_url}. Command request: {request_ref or 'unavailable'}.", (str(result.get("recovery") or "Inspect the recorded stderr and retry."),))


def _is_shallow(path: Path) -> bool:
    common = path / ".git" / "shallow"
    return common.is_file() and bool(common.read_text(encoding="utf-8", errors="replace").strip())
