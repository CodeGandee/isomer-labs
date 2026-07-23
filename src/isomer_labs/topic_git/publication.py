"""Publication destination, binding, component, and remote-plan helpers."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
import hashlib
import json
from pathlib import Path
import re
from typing import Iterable, Mapping
from urllib.parse import urlsplit, urlunsplit

from isomer_labs.core.path_utils import canonicalize, is_within
from isomer_labs.topic_git.models import (
    ComponentBinding,
    ComponentSelection,
    PrivacyDisposition,
    PublicationBinding,
    PublicationState,
)
from isomer_labs.topic_git.projection import ProjectionFinding, classify_projection_file


PROJECT_IGNORE_BEGIN = "# BEGIN ISOMER TOPIC GIT PUBLICATION"
PROJECT_IGNORE_END = "# END ISOMER TOPIC GIT PUBLICATION"
PROJECT_PUBLICATION_IGNORE_RULE = "/tmp/topic-workspace-publish/"
_REMOTE_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")
_SCP_REMOTE_RE = re.compile(
    r"^(?P<user>[A-Za-z0-9._-]+)@(?P<host>[A-Za-z0-9.-]+):(?P<path>[A-Za-z0-9._~/-]+)$"
)
_BRANCH_RE = re.compile(r"^(?:topic-owner/main|topic-workspace/main|per-topic-actor/[^/]+/main|per-agent/[^/]+/main)$")


class BranchCompatibilityState(StrEnum):
    ABSENT = "absent"
    COMPATIBLE = "compatible"
    INCOMPATIBLE = "incompatible"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class TemporaryDirectoryEvidence:
    name: str
    path: Path
    exists: bool
    effectively_ignored: bool
    evidence: str


@dataclass(frozen=True)
class PublicationDestinationPlan:
    path: Path
    reason: str
    create_directory: bool
    update_project_ignore: bool


@dataclass(frozen=True)
class BranchCompatibility:
    branch: str
    state: BranchCompatibilityState
    local_commit: str | None
    remote_commit: str | None
    reason: str


@dataclass(frozen=True)
class DestructiveBranchReplacement:
    branch: str
    observed_remote_commit: str
    replacement_commit: str
    displaced_commits: tuple[str, ...]
    warning: str

    def to_json(self) -> dict[str, object]:
        return {
            "branch": self.branch,
            "observed_remote_commit": self.observed_remote_commit,
            "replacement_commit": self.replacement_commit,
            "displaced_commits": list(self.displaced_commits),
            "warning": self.warning,
        }


@dataclass(frozen=True)
class DestructiveChangePlan:
    plan_id: str
    binding_id: str
    replacements: tuple[DestructiveBranchReplacement, ...]
    push_order: tuple[str, ...]
    approved_branches: tuple[str, ...] = ()

    def to_json(self) -> dict[str, object]:
        return {
            "plan_id": self.plan_id,
            "binding_id": self.binding_id,
            "replacements": [replacement.to_json() for replacement in self.replacements],
            "push_order": list(self.push_order),
            "approved_branches": list(self.approved_branches),
        }


def validate_remote_locator(locator: str) -> tuple[str, ...]:
    """Reject locators that embed credentials, signatures, or ambiguous syntax."""

    value = locator.strip()
    if not value:
        return ("Publication remote is empty.",)
    if any(character.isspace() for character in value):
        return ("Publication remote contains whitespace.",)
    if _SCP_REMOTE_RE.fullmatch(value):
        return ()
    parsed = urlsplit(value)
    if parsed.scheme in {"http", "https"}:
        diagnostics: list[str] = []
        if parsed.hostname is None:
            diagnostics.append("HTTP publication remote has no host.")
        if parsed.username is not None or parsed.password is not None:
            diagnostics.append("HTTP publication remote embeds credentials.")
        if parsed.query:
            diagnostics.append("Publication remote contains query parameters or a signed locator.")
        if parsed.fragment:
            diagnostics.append("Publication remote contains a fragment.")
        return tuple(diagnostics)
    if parsed.scheme == "ssh":
        diagnostics = []
        if parsed.hostname is None:
            diagnostics.append("SSH publication remote has no host.")
        if parsed.password is not None:
            diagnostics.append("SSH publication remote embeds a password.")
        if parsed.query or parsed.fragment:
            diagnostics.append("SSH publication remote contains query parameters or a fragment.")
        return tuple(diagnostics)
    if parsed.scheme == "file":
        return ("File publication remote contains query parameters or a fragment.",) if parsed.query or parsed.fragment else ()
    if parsed.scheme:
        return (f"Unsupported publication remote scheme: {parsed.scheme}",)
    if value.startswith(("/", "./", "../")):
        return ()
    return ("Publication remote must be an HTTPS, SSH, scp-style, file, or explicit filesystem locator.",)


def redact_remote_locator(locator: str) -> str:
    """Return a credential-safe diagnostic rendering."""

    if not validate_remote_locator(locator):
        return locator.strip()
    parsed = urlsplit(locator.strip())
    if parsed.scheme and parsed.hostname:
        port = f":{parsed.port}" if parsed.port is not None else ""
        safe_netloc = f"{parsed.hostname}{port}"
        return urlunsplit((parsed.scheme, safe_netloc, parsed.path, "", ""))
    if "@" in locator and ":" in locator.rsplit("@", 1)[-1]:
        return locator.rsplit("@", 1)[-1]
    return "<redacted-invalid-publication-remote>"


def choose_publication_destination(
    *,
    project_root: Path,
    topic_id: str,
    candidates: Iterable[TemporaryDirectoryEvidence],
    forbidden_roots: Iterable[Path],
    existing_copy_path: Path | None = None,
) -> PublicationDestinationPlan:
    """Choose an existing binding, ignored tmp, ignored temp, or managed tmp."""

    root = canonicalize(project_root)
    forbidden = tuple(forbidden_roots)
    if existing_copy_path is not None:
        diagnostics = validate_publication_destination(
            existing_copy_path,
            project_root=root,
            forbidden_roots=forbidden,
        )
        if not diagnostics:
            return PublicationDestinationPlan(
                canonicalize(existing_copy_path),
                "reuse existing safe publication binding",
                not existing_copy_path.exists(),
                False,
            )

    by_name = {candidate.name: candidate for candidate in candidates if candidate.name in {"tmp", "temp"}}
    ordered = [
        candidate
        for name in ("tmp", "temp")
        if (candidate := by_name.get(name)) is not None and candidate.effectively_ignored
    ]
    if ordered:
        candidate = ordered[0]
        destination = canonicalize(candidate.path) / "topic-workspace-publish" / topic_id
        diagnostics = validate_publication_destination(
            destination,
            project_root=root,
            forbidden_roots=forbidden,
        )
        if diagnostics:
            raise ValueError("; ".join(diagnostics))
        return PublicationDestinationPlan(
            destination,
            f"use effectively ignored Project-root {candidate.name}/ ({candidate.evidence})",
            not destination.exists(),
            False,
        )

    destination = root / "tmp" / "topic-workspace-publish" / topic_id
    diagnostics = validate_publication_destination(
        destination,
        project_root=root,
        forbidden_roots=forbidden,
    )
    if diagnostics:
        raise ValueError("; ".join(diagnostics))
    return PublicationDestinationPlan(
        destination,
        "create managed ignored Project-root tmp/",
        not destination.exists(),
        True,
    )


def validate_publication_destination(
    destination: Path,
    *,
    project_root: Path,
    forbidden_roots: Iterable[Path],
) -> tuple[str, ...]:
    """Require a Project-local destination outside every canonical source root."""

    target = canonicalize(destination)
    root = canonicalize(project_root)
    diagnostics: list[str] = []
    if target == root or not is_within(target, root):
        diagnostics.append("Topic Publication Copy must stay below the Project root.")
    for forbidden_root in forbidden_roots:
        forbidden = canonicalize(forbidden_root)
        if target == forbidden or is_within(target, forbidden) or is_within(forbidden, target):
            diagnostics.append(f"Topic Publication Copy conflicts with protected root: {forbidden}")
    return tuple(diagnostics)


def update_project_publication_ignore(existing: str) -> str:
    """Add or refresh the bounded Project publication ignore block."""

    block = "\n".join((PROJECT_IGNORE_BEGIN, PROJECT_PUBLICATION_IGNORE_RULE, PROJECT_IGNORE_END))
    lines = existing.splitlines()
    starts = [index for index, line in enumerate(lines) if line == PROJECT_IGNORE_BEGIN]
    ends = [index for index, line in enumerate(lines) if line == PROJECT_IGNORE_END]
    if len(starts) > 1 or len(ends) > 1 or bool(starts) != bool(ends):
        raise ValueError("Project publication ignore block markers are invalid.")
    if starts:
        if ends[0] < starts[0]:
            raise ValueError("Project publication ignore block markers are out of order.")
        rendered = [*lines[: starts[0]], *block.splitlines(), *lines[ends[0] + 1 :]]
    else:
        rendered = list(lines)
        if rendered and rendered[-1] != "":
            rendered.append("")
        rendered.extend(block.splitlines())
    return "\n".join(rendered).rstrip() + "\n"


def classify_publication_path(
    relative_path: str,
    content: bytes,
    *,
    max_bytes: int,
    approved_license: bool = True,
) -> tuple[PrivacyDisposition, tuple[ProjectionFinding, ...]]:
    return classify_projection_file(
        relative_path,
        content,
        max_bytes=max_bytes,
        approved_license=approved_license,
    )


def select_publication_components(
    components: Iterable[ComponentBinding],
    *,
    explicit_exclusions: Iterable[str] = (),
) -> tuple[ComponentBinding, ...]:
    """Select every available Isomer-resolved component unless explicitly excluded."""

    exclusions = set(explicit_exclusions)
    selected: list[ComponentBinding] = []
    for component in components:
        if component.component_id in exclusions:
            selected.append(
                replace(
                    component,
                    selection=ComponentSelection.EXCLUDED,
                    reason="explicitly excluded from the current publication plan",
                )
            )
        elif component.selection is ComponentSelection.UNAVAILABLE:
            selected.append(component)
        elif component.selection is ComponentSelection.BLOCKED:
            selected.append(component)
        else:
            selected.append(replace(component, selection=ComponentSelection.SELECTED))
    return tuple(selected)


def publication_plan_fingerprint(
    *,
    source_fingerprints: Mapping[str, str],
    expected_output_fingerprints: Mapping[str, str],
    copy_fingerprints: Mapping[str, str],
    binding: PublicationBinding,
    components: Iterable[ComponentBinding],
    remote_refs: Mapping[str, str | None],
) -> str:
    """Bind approval to source, output, copy, binding, topology, and remote refs."""

    payload = {
        "source": sorted(source_fingerprints.items()),
        "expected_output": sorted(expected_output_fingerprints.items()),
        "copy": sorted(copy_fingerprints.items()),
        "binding": binding.to_json(),
        "components": [component.to_json() for component in sorted(components, key=lambda item: item.component_id)],
        "remote_refs": sorted(remote_refs.items()),
    }
    return hashlib.sha256(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()).hexdigest()


def classify_remote_branch(
    *,
    branch: str,
    local_commit: str | None,
    remote_commit: str | None,
    remote_is_ancestor: bool | None,
) -> BranchCompatibility:
    """Classify caller-supplied fetch and ancestry evidence."""

    if _BRANCH_RE.fullmatch(branch) is None:
        return BranchCompatibility(
            branch,
            BranchCompatibilityState.BLOCKED,
            local_commit,
            remote_commit,
            "branch is outside the deterministic publication namespace",
        )
    if local_commit is None:
        return BranchCompatibility(
            branch,
            BranchCompatibilityState.BLOCKED,
            local_commit,
            remote_commit,
            "local replacement commit is unavailable",
        )
    if remote_commit is None:
        return BranchCompatibility(branch, BranchCompatibilityState.ABSENT, local_commit, None, "remote ref is absent")
    if remote_commit == local_commit or remote_is_ancestor is True:
        return BranchCompatibility(
            branch,
            BranchCompatibilityState.COMPATIBLE,
            local_commit,
            remote_commit,
            "normal explicit-ref push is compatible",
        )
    return BranchCompatibility(
        branch,
        BranchCompatibilityState.INCOMPATIBLE,
        local_commit,
        remote_commit,
        "remote ref requires a separately approved branch replacement",
    )


def component_push_order(components: Iterable[ComponentBinding]) -> tuple[str, ...]:
    branches = sorted(
        {
            component.branch
            for component in components
            if component.selection is ComponentSelection.SELECTED
        }
    )
    return (*branches, "topic-workspace/main")


def validate_force_replacements(
    plan: DestructiveChangePlan,
    *,
    fetched_remote_refs: Mapping[str, str | None],
    requested_replacements: Mapping[str, str],
) -> tuple[str, ...]:
    """Require current refs, exact commits, listed branches, and separate approval."""

    diagnostics: list[str] = []
    planned = {replacement.branch: replacement for replacement in plan.replacements}
    approved = set(plan.approved_branches)
    for branch, requested_commit in requested_replacements.items():
        replacement = planned.get(branch)
        if replacement is None:
            diagnostics.append(f"force replacement branch is not listed in the destructive plan: {branch}")
            continue
        if branch not in approved:
            diagnostics.append(f"force replacement lacks separate branch approval: {branch}")
        if requested_commit != replacement.replacement_commit:
            diagnostics.append(f"force replacement commit differs from the approved plan: {branch}")
        if fetched_remote_refs.get(branch) != replacement.observed_remote_commit:
            diagnostics.append(f"force approval is stale because the fetched remote ref changed: {branch}")
    for branch in approved:
        if branch not in requested_replacements:
            diagnostics.append(f"approved force replacement is absent from the requested exact scope: {branch}")
    return tuple(diagnostics)


def derive_publication_status(
    *,
    binding_exists: bool,
    copy_exists: bool,
    synchronized: bool,
    stale: bool,
    blockers: Iterable[str],
) -> PublicationState:
    blocker_list = tuple(blockers)
    if blocker_list:
        return PublicationState.BLOCKED
    if not binding_exists:
        return PublicationState.DISABLED
    if not copy_exists:
        return PublicationState.COPY_MISSING
    if stale:
        return PublicationState.STALE
    if synchronized:
        return PublicationState.SYNCHRONIZED
    return PublicationState.PREPARED
