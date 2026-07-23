"""Deterministic local-tracking planning that never executes Git."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Iterable

from isomer_labs.core.path_utils import canonicalize


LOCAL_IGNORE_BEGIN = "# BEGIN ISOMER TOPIC GIT LOCAL"
LOCAL_IGNORE_END = "# END ISOMER TOPIC GIT LOCAL"
LOCAL_DEFAULT_IGNORE_RULES = (
    "/.pixi/",
    "/.venv/",
    "/__pycache__/",
    "/runtime/",
    "/tmp/",
    "/temp/",
    "state.sqlite",
    "*.log",
    "*.pem",
    "*.key",
    ".env",
    ".env.*",
)
_SECRET_KEY_RE = re.compile(
    rb"(?i)(?:api[_-]?key|client[_-]?secret|password|access[_-]?token)\s*[:=]\s*[\"']?[^\s\"']{8,}"
)
_PRIVATE_KEY_RE = re.compile(rb"-----BEGIN (?:[A-Z0-9 ]+ )?PRIVATE KEY-----")


class LocalCandidateDisposition(StrEnum):
    TRACK = "track"
    IGNORE = "ignore"
    WARN = "warn"
    BLOCK = "block"


@dataclass(frozen=True)
class AncestorRepositoryEvidence:
    """Read-only evidence collected by direct, path-scoped Git commands."""

    top_level: Path
    source_tracked: bool
    tracked_paths: tuple[str, ...]
    source_ignored: bool
    ignore_evidence: str | None = None


@dataclass(frozen=True)
class LocalRepositoryEvidence:
    """A caller-supplied snapshot of the Source Topic Workspace root repository."""

    top_level: Path | None
    git_dir_valid: bool
    head_sha: str | None
    index_paths: tuple[str, ...]
    working_tree_fingerprint: str
    ignore_fingerprint: str

    def repository_identity(self, source_topic_workspace: Path) -> str:
        source = canonicalize(source_topic_workspace)
        if self.top_level is None:
            return "absent"
        top_level = canonicalize(self.top_level)
        if top_level != source:
            return f"ancestor:{top_level}"
        return f"root:{top_level}" if self.git_dir_valid else f"invalid:{top_level}"

    def local_state(self, source_topic_workspace: Path) -> str:
        source = canonicalize(source_topic_workspace)
        if self.top_level is None or canonicalize(self.top_level) != source:
            return "disabled"
        return "enabled" if self.git_dir_valid else "invalid"


@dataclass(frozen=True)
class LocalCandidate:
    relative_path: str
    disposition: LocalCandidateDisposition
    reasons: tuple[str, ...] = ()


@dataclass(frozen=True)
class NestedWorkspacePointer:
    label: str
    relative_path: str
    branch: str
    commit_sha: str
    dirty: bool


@dataclass(frozen=True)
class LocalPlanFingerprint:
    value: str

    @classmethod
    def from_evidence(
        cls,
        evidence: LocalRepositoryEvidence,
        *,
        approved_paths: Iterable[str],
    ) -> LocalPlanFingerprint:
        payload = {
            "repository": str(canonicalize(evidence.top_level)) if evidence.top_level else None,
            "git_dir_valid": evidence.git_dir_valid,
            "head_sha": evidence.head_sha,
            "index_paths": sorted(evidence.index_paths),
            "working_tree_fingerprint": evidence.working_tree_fingerprint,
            "ignore_fingerprint": evidence.ignore_fingerprint,
            "approved_paths": sorted(_normalize_relative_path(path) for path in approved_paths),
        }
        encoded = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
        return cls(hashlib.sha256(encoded).hexdigest())


def evaluate_ancestor_repositories(
    source_topic_workspace: Path,
    evidence: Iterable[AncestorRepositoryEvidence],
) -> tuple[str, ...]:
    """Return blockers from caller-collected ancestor repository evidence."""

    source = canonicalize(source_topic_workspace)
    blockers: list[str] = []
    observed: set[Path] = set()
    for item in evidence:
        top_level = canonicalize(item.top_level)
        if top_level in observed:
            blockers.append(f"duplicate ancestor repository evidence: {top_level}")
            continue
        observed.add(top_level)
        try:
            source.relative_to(top_level)
        except ValueError:
            blockers.append(f"reported repository is not an ancestor of the Source Topic Workspace: {top_level}")
            continue
        if top_level == source:
            blockers.append(f"reported ancestor evidence points at the Source Topic Workspace itself: {top_level}")
            continue
        if item.source_tracked or item.tracked_paths:
            blockers.append(f"ancestor repository tracks Source Topic Workspace material: {top_level}")
        if not item.source_ignored:
            blockers.append(f"ancestor repository does not effectively ignore the Source Topic Workspace: {top_level}")
    return tuple(blockers)


def classify_local_candidate(relative_path: str, content: bytes | None = None) -> LocalCandidate:
    """Classify one root-owned whole-file candidate without consulting Git."""

    normalized = _normalize_relative_path(relative_path)
    parts = PurePosixPath(normalized).parts
    lower_parts = tuple(part.lower() for part in parts)
    name = lower_parts[-1] if lower_parts else ""
    reasons: list[str] = []

    if ".git" in lower_parts:
        return LocalCandidate(normalized, LocalCandidateDisposition.BLOCK, ("Git control material is never staged.",))
    if any(part in {"runtime", "tmp", "temp", ".pixi", ".venv", "__pycache__"} for part in lower_parts):
        return LocalCandidate(normalized, LocalCandidateDisposition.IGNORE, ("Known local-only support surface.",))
    if any(part in {"actors", "agents"} for part in lower_parts) or lower_parts[:2] == ("repos", "topic-main"):
        return LocalCandidate(normalized, LocalCandidateDisposition.IGNORE, ("Nested workspace topology stays independent.",))
    if name == "state.sqlite" or name.endswith((".log", ".pyc", ".pem", ".key")) or name.startswith(".env"):
        return LocalCandidate(normalized, LocalCandidateDisposition.IGNORE, ("Sensitive or disposable local surface.",))
    if content is not None and (_SECRET_KEY_RE.search(content) or _PRIVATE_KEY_RE.search(content)):
        reasons.append("Secret-like content requires explicit local-history approval.")
        return LocalCandidate(normalized, LocalCandidateDisposition.WARN, tuple(reasons))
    return LocalCandidate(normalized, LocalCandidateDisposition.TRACK)


def update_local_managed_ignore(
    existing: str,
    *,
    nested_workspace_paths: Iterable[str] = (),
    extra_rules: Iterable[str] = (),
) -> str:
    """Render the idempotent local managed block while preserving user rules."""

    rules = set(LOCAL_DEFAULT_IGNORE_RULES)
    rules.update(_ignore_rule(path) for path in nested_workspace_paths)
    rules.update(rule.strip() for rule in extra_rules if rule.strip())
    block = "\n".join((LOCAL_IGNORE_BEGIN, *sorted(rules), LOCAL_IGNORE_END))
    return _replace_managed_block(existing, LOCAL_IGNORE_BEGIN, LOCAL_IGNORE_END, block)


def verify_exact_index(actual_index_paths: Iterable[str], approved_paths: Iterable[str]) -> tuple[str, ...]:
    """Require the index to equal the approved exact path set."""

    actual = {_normalize_relative_path(path) for path in actual_index_paths}
    approved = {_normalize_relative_path(path) for path in approved_paths}
    diagnostics = [f"unexpected staged path: {path}" for path in sorted(actual - approved)]
    diagnostics.extend(f"approved path is not staged: {path}" for path in sorted(approved - actual))
    return tuple(diagnostics)


def render_local_version_manifest(pointers: Iterable[NestedWorkspacePointer]) -> str:
    """Render a pointer-only TOML summary of nested workspace state."""

    lines = [
        'schema_version = "isomer-topic-workspace-local-version.v1"',
        'limitation = "Pointers only; uncommitted nested workspace content is not preserved by this root commit."',
    ]
    for pointer in sorted(pointers, key=lambda item: (item.label, item.relative_path)):
        lines.extend(
            (
                "",
                "[[nested_workspaces]]",
                f"label = {_toml_string(pointer.label)}",
                f"path = {_toml_string(_normalize_relative_path(pointer.relative_path))}",
                f"branch = {_toml_string(pointer.branch)}",
                f"commit_sha = {_toml_string(pointer.commit_sha)}",
                f"dirty = {'true' if pointer.dirty else 'false'}",
            )
        )
    return "\n".join(lines) + "\n"


def _replace_managed_block(existing: str, begin: str, end: str, block: str) -> str:
    lines = existing.splitlines()
    begin_indexes = [index for index, line in enumerate(lines) if line == begin]
    end_indexes = [index for index, line in enumerate(lines) if line == end]
    if len(begin_indexes) > 1 or len(end_indexes) > 1:
        raise ValueError("Managed ignore markers are duplicated.")
    if bool(begin_indexes) != bool(end_indexes):
        raise ValueError("Managed ignore block is incomplete.")
    if begin_indexes:
        start = begin_indexes[0]
        finish = end_indexes[0]
        if finish < start:
            raise ValueError("Managed ignore block markers are out of order.")
        new_lines = [*lines[:start], *block.splitlines(), *lines[finish + 1 :]]
    else:
        new_lines = list(lines)
        if new_lines and new_lines[-1] != "":
            new_lines.append("")
        new_lines.extend(block.splitlines())
    return "\n".join(new_lines).rstrip() + "\n"


def _normalize_relative_path(value: str) -> str:
    normalized = PurePosixPath(value.replace("\\", "/")).as_posix()
    if normalized in {"", ".", ".."} or normalized.startswith("../") or normalized.startswith("/"):
        raise ValueError(f"Topic Git path must be a non-root relative path: {value!r}")
    return normalized


def _ignore_rule(value: str) -> str:
    return f"/{_normalize_relative_path(value).rstrip('/')}/"


def _toml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)
