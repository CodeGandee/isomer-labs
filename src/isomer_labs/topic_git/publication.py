"""Publication destination, binding, component, and remote-plan helpers."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import StrEnum
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
from typing import Iterable, Mapping
from urllib.parse import urlsplit, urlunsplit

from isomer_labs.core.path_utils import canonicalize, is_within
from isomer_labs.topic_git.history_models import (
    PublicationHistoryDisposition,
    PublicationRefUpdate,
)
from isomer_labs.topic_git.models import (
    ComponentBinding,
    ComponentKind,
    ComponentSelection,
    PrivacyDisposition,
    PublicationBinding,
    PublicationContentClass,
    PublicationSelectionSettings,
    PublicationSnapshotMode,
    PublicationState,
    ReferenceRepositoryBinding,
    RemoteVisibility,
)
from isomer_labs.topic_git.projection import (
    ProjectionEntry,
    ProjectionFinding,
    classify_projection_file,
)


PROJECT_IGNORE_BEGIN = "# BEGIN ISOMER TOPIC GIT PUBLICATION"
PROJECT_IGNORE_END = "# END ISOMER TOPIC GIT PUBLICATION"
PROJECT_PUBLICATION_IGNORE_RULE = "/tmp/topic-workspace-publish/"
PUBLICATION_COPY_EXCLUDE_RULE = "/.isomer/"
CANONICAL_PUBLICATION_BRANCH = "main"
LEGACY_PUBLICATION_BRANCHES = (
    "topic-workspace/main",
    "topic-owner/main",
)
_REMOTE_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")
_SCP_REMOTE_RE = re.compile(
    r"^(?P<user>[A-Za-z0-9._-]+)@(?P<host>[A-Za-z0-9.-]+):(?P<path>[A-Za-z0-9._~/-]+)$"
)
_COMPONENT_BRANCH_RE = re.compile(
    r"^components/(?:topic-main|topic-actors/[A-Za-z0-9._-]+|agents/[A-Za-z0-9._-]+)$"
)
_COMPONENT_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")
_EXACT_GIT_COMMIT_RE = re.compile(r"^(?:[0-9a-f]{40}|[0-9a-f]{64})$")
_GITHUB_SCP_RE = re.compile(
    r"^git@github\.com:(?P<owner>[A-Za-z0-9_.-]+)/(?P<repo>[A-Za-z0-9_.-]+?)(?:\.git)?$"
)


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


@dataclass(frozen=True)
class SnapshotReplacementPlan:
    plan_id: str
    binding_id: str
    observed_refs: tuple[tuple[str, str], ...]
    expected_refs: tuple[tuple[str, str], ...]
    observed_tags: tuple[tuple[str, str], ...]
    expected_tags: tuple[tuple[str, str], ...]
    observed_remote_head: str | None
    push_order: tuple[str, ...]

    @property
    def ref_deletions(self) -> tuple[str, ...]:
        expected = {name for name, _ in self.expected_refs}
        return tuple(name for name, _ in self.observed_refs if name not in expected)

    @property
    def tag_deletions(self) -> tuple[str, ...]:
        expected = {name for name, _ in self.expected_tags}
        return tuple(name for name, _ in self.observed_tags if name not in expected)

    @property
    def provider_default_branch_action_required(self) -> bool:
        return self.observed_remote_head != CANONICAL_PUBLICATION_BRANCH

    @property
    def remote_head_ref_deletion(self) -> str | None:
        if self.observed_remote_head in self.ref_deletions:
            return self.observed_remote_head
        return None

    def to_json(self) -> dict[str, object]:
        return {
            "plan_id": self.plan_id,
            "binding_id": self.binding_id,
            "snapshot_mode": PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT.value,
            "canonical_branch": CANONICAL_PUBLICATION_BRANCH,
            "observed_remote_refs": dict(self.observed_refs),
            "expected_remote_refs": dict(self.expected_refs),
            "observed_remote_tags": dict(self.observed_tags),
            "expected_remote_tags": dict(self.expected_tags),
            "observed_remote_head": self.observed_remote_head,
            "expected_remote_head": CANONICAL_PUBLICATION_BRANCH,
            "provider_default_branch_action_required": self.provider_default_branch_action_required,
            "remote_head_ref_deletion": self.remote_head_ref_deletion,
            "ref_deletions": list(self.ref_deletions),
            "tag_deletions": list(self.tag_deletions),
            "push_order": list(self.push_order),
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


def update_publication_copy_exclude(existing: str) -> str:
    """Keep copy-local Topic Git support out of the publication index."""

    lines = existing.splitlines()
    if PUBLICATION_COPY_EXCLUDE_RULE not in lines:
        lines.append(PUBLICATION_COPY_EXCLUDE_RULE)
    return "\n".join(lines).rstrip() + "\n"


def classify_publication_path(
    relative_path: str,
    content: bytes,
    *,
    max_bytes: int,
    approved_license: bool = True,
    content_class: PublicationContentClass = PublicationContentClass.OTHER,
    selection: PublicationSelectionSettings = PublicationSelectionSettings(),
    approved_media_type: str | None = None,
) -> tuple[PrivacyDisposition, tuple[ProjectionFinding, ...]]:
    return classify_projection_file(
        relative_path,
        content,
        max_bytes=max_bytes,
        approved_license=approved_license,
        content_class=content_class,
        selection=selection,
        approved_media_type=approved_media_type,
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
    return normalize_publication_components(selected)


def publication_component_branch(kind: ComponentKind, name: str) -> str:
    """Return the deterministic current-snapshot branch for a topic-owned component."""

    if kind is ComponentKind.TOPIC_MAIN:
        return "components/topic-main"
    normalized = name.strip()
    if (
        _COMPONENT_NAME_RE.fullmatch(normalized) is None
        or normalized in {".", ".."}
        or normalized.startswith(".")
    ):
        raise ValueError(f"Component name is unsafe for publication: {name!r}")
    namespace = "topic-actors" if kind is ComponentKind.TOPIC_ACTOR else "agents"
    return f"components/{namespace}/{normalized}"


def normalize_publication_components(
    components: Iterable[ComponentBinding],
) -> tuple[ComponentBinding, ...]:
    """Assign deterministic branches and Topic Main anchors without source branch identity."""

    component_list = tuple(components)
    topic_main = tuple(
        component for component in component_list if component.kind is ComponentKind.TOPIC_MAIN
    )
    if len(topic_main) > 1:
        raise ValueError("Publication component topology contains multiple Topic Main components.")
    main_id = topic_main[0].component_id if topic_main else None
    normalized: list[ComponentBinding] = []
    for component in component_list:
        anchor = None
        if component.kind in {ComponentKind.TOPIC_ACTOR, ComponentKind.AGENT}:
            if main_id is None and component.selection is ComponentSelection.SELECTED:
                raise ValueError("Selected actor or agent snapshot requires a selected Topic Main anchor.")
            anchor = main_id
        normalized.append(
            replace(
                component,
                branch=publication_component_branch(component.kind, component.name),
                git_anchor_component_id=anchor,
            )
        )
    return tuple(normalized)


def validate_publication_component_topology(
    components: Iterable[ComponentBinding],
) -> tuple[str, ...]:
    """Validate deterministic branches, unique paths, and actor/agent anchor relationships."""

    component_list = tuple(components)
    diagnostics: list[str] = []
    selected = tuple(
        component
        for component in component_list
        if component.selection is ComponentSelection.SELECTED
    )
    main = tuple(component for component in selected if component.kind is ComponentKind.TOPIC_MAIN)
    if len(main) != 1 and any(
        component.kind in {ComponentKind.TOPIC_ACTOR, ComponentKind.AGENT}
        for component in selected
    ):
        diagnostics.append("Selected actor or agent snapshots require exactly one selected Topic Main component.")
    main_id = main[0].component_id if len(main) == 1 else None
    paths: set[str] = set()
    branches: set[str] = set()
    for component in selected:
        try:
            expected_branch = publication_component_branch(component.kind, component.name)
            path = _publication_relative_path(component.relative_path)
        except ValueError as error:
            diagnostics.append(str(error))
            continue
        if component.branch != expected_branch:
            diagnostics.append(
                f"component branch is not deterministic for {component.component_id}: {component.branch}"
            )
        if component.kind in {ComponentKind.TOPIC_ACTOR, ComponentKind.AGENT}:
            if component.git_anchor_component_id != main_id:
                diagnostics.append(
                    f"component does not record its Topic Main anchor: {component.component_id}"
                )
        elif component.git_anchor_component_id is not None:
            diagnostics.append("Topic Main component must not declare a Git anchor component.")
        if path in paths:
            diagnostics.append(f"duplicate topic-owned component path: {path}")
        if component.branch in branches:
            diagnostics.append(f"duplicate topic-owned component branch: {component.branch}")
        paths.add(path)
        branches.add(component.branch)
    return tuple(diagnostics)


def select_reference_repositories(
    references: Iterable[ReferenceRepositoryBinding],
    *,
    explicit_exclusions: Iterable[str] = (),
) -> tuple[ReferenceRepositoryBinding, ...]:
    """Select every registered GitHub reference unless explicitly excluded."""

    exclusions = set(explicit_exclusions)
    return tuple(
        replace(
            reference,
            selection=(
                ComponentSelection.EXCLUDED
                if reference.reference_id in exclusions
                else reference.selection
                if reference.selection in {ComponentSelection.UNAVAILABLE, ComponentSelection.BLOCKED}
                else ComponentSelection.SELECTED
            ),
        )
        for reference in references
    )


def normalize_github_repository_locator(locator: str) -> str:
    """Return a normalized credential-free GitHub repository locator."""

    value = locator.strip()
    scp_match = _GITHUB_SCP_RE.fullmatch(value)
    if scp_match is not None:
        return _canonical_github_locator(scp_match.group("owner"), scp_match.group("repo"))
    parsed = urlsplit(value)
    if parsed.scheme == "https" and parsed.hostname == "github.com":
        if (
            parsed.username is not None
            or parsed.password is not None
            or parsed.port is not None
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("GitHub repository locator must not contain authentication, ports, queries, or fragments.")
        parts = tuple(part for part in parsed.path.split("/") if part)
        if len(parts) != 2:
            raise ValueError("GitHub repository locator must identify exactly one owner and repository.")
        return _canonical_github_locator(parts[0], parts[1])
    if parsed.scheme == "ssh" and parsed.hostname == "github.com":
        if (
            parsed.username != "git"
            or parsed.password is not None
            or parsed.port is not None
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError("GitHub SSH locator must use the credential-free git service identity.")
        parts = tuple(part for part in parsed.path.split("/") if part)
        if len(parts) != 2:
            raise ValueError("GitHub repository locator must identify exactly one owner and repository.")
        return _canonical_github_locator(parts[0], parts[1])
    raise ValueError("Reference repository must use a credential-free github.com HTTPS, SSH, or scp-style locator.")


def validate_reference_repository(reference: ReferenceRepositoryBinding) -> tuple[str, ...]:
    """Validate one selected upstream GitHub reference without contacting it."""

    if reference.selection is not ComponentSelection.SELECTED:
        return ()
    diagnostics: list[str] = []
    if not reference.semantic_label.startswith("topic.repos.") or reference.semantic_label == "topic.repos.main":
        diagnostics.append("Reference repository semantic label must be a non-main topic.repos.* label.")
    try:
        _publication_relative_path(reference.relative_path)
    except ValueError as error:
        diagnostics.append(str(error))
    try:
        normalize_github_repository_locator(reference.remote_url)
    except ValueError as error:
        diagnostics.append(str(error))
    if _EXACT_GIT_COMMIT_RE.fullmatch(reference.commit_sha) is None:
        diagnostics.append("Reference repository commit must be an exact 40- or 64-character lowercase Git object id.")
    if reference.visibility is RemoteVisibility.UNKNOWN:
        diagnostics.append("Reference repository visibility is unknown.")
    if not reference.license_status or not reference.license_status.strip():
        diagnostics.append("Reference repository license posture is missing.")
    return tuple(diagnostics)


def render_publication_gitmodules(
    *,
    publication_remote: str,
    components: Iterable[ComponentBinding],
    references: Iterable[ReferenceRepositoryBinding] = (),
) -> str:
    """Render topic-owned same-remote and upstream-reference submodule configuration."""

    remote_diagnostics = validate_remote_locator(publication_remote)
    if remote_diagnostics:
        raise ValueError("; ".join(remote_diagnostics))
    component_list = tuple(components)
    topology_diagnostics = validate_publication_component_topology(component_list)
    if topology_diagnostics:
        raise ValueError("; ".join(topology_diagnostics))
    rows: list[tuple[str, str, str, str | None]] = []
    for component in component_list:
        if component.selection is not ComponentSelection.SELECTED:
            continue
        if _COMPONENT_BRANCH_RE.fullmatch(component.branch) is None:
            raise ValueError(f"Component branch is outside the publication namespace: {component.branch}")
        rows.append(
            (
                f"component:{component.component_id}",
                _publication_relative_path(component.relative_path),
                publication_remote.strip(),
                component.branch,
            )
        )
    for reference in references:
        if reference.selection is not ComponentSelection.SELECTED:
            continue
        diagnostics = validate_reference_repository(reference)
        if diagnostics:
            raise ValueError("; ".join(diagnostics))
        rows.append(
            (
                f"reference:{reference.reference_id}",
                _publication_relative_path(reference.relative_path),
                normalize_github_repository_locator(reference.remote_url),
                None,
            )
        )
    names = [row[0] for row in rows]
    paths = [row[1] for row in rows]
    if len(names) != len(set(names)):
        raise ValueError("Publication submodule names must be unique.")
    if len(paths) != len(set(paths)):
        raise ValueError("Publication submodule paths must be unique.")
    lines: list[str] = []
    for name, path, remote, branch in sorted(rows, key=lambda row: row[1]):
        if lines:
            lines.append("")
        lines.extend(
            (
                f'[submodule {json.dumps(name)}]',
                f"\tpath = {json.dumps(path)}",
                f"\turl = {json.dumps(remote)}",
            )
        )
        if branch is not None:
            lines.append(f"\tbranch = {json.dumps(branch)}")
    return "\n".join(lines) + ("\n" if lines else "")


def publication_plan_fingerprint(
    *,
    source_fingerprints: Mapping[str, str],
    expected_output_fingerprints: Mapping[str, str],
    copy_fingerprints: Mapping[str, str],
    binding: PublicationBinding,
    components: Iterable[ComponentBinding],
    remote_refs: Mapping[str, str | None],
    selection: PublicationSelectionSettings = PublicationSelectionSettings(),
    reference_repositories: Iterable[ReferenceRepositoryBinding] = (),
    generated_output_fingerprints: Mapping[str, str] | None = None,
    reproduction_limitations: Iterable[str] = (),
    projection_entries: Iterable[ProjectionEntry] = (),
    remote_tags: Mapping[str, str | None] | None = None,
    remote_head: str | None = None,
    expected_remote_refs: Mapping[str, str | None] | None = None,
    expected_remote_tags: Mapping[str, str | None] | None = None,
    ref_updates: Iterable[PublicationRefUpdate] = (),
    history_disposition: PublicationHistoryDisposition = PublicationHistoryDisposition.RETAIN,
) -> str:
    """Bind approval to source, output, copy, binding, topology, and remote refs."""

    payload = {
        "source": sorted(source_fingerprints.items()),
        "expected_output": sorted(expected_output_fingerprints.items()),
        "copy": sorted(copy_fingerprints.items()),
        "binding": binding.to_json(),
        "components": [component.to_json() for component in sorted(components, key=lambda item: item.component_id)],
        "selection": selection.to_json(),
        "reference_repositories": [
            reference.to_json()
            for reference in sorted(reference_repositories, key=lambda item: item.reference_id)
        ],
        "generated_output": sorted((generated_output_fingerprints or {}).items()),
        "projection_entries": [
            entry.to_json()
            for entry in sorted(
                projection_entries,
                key=lambda item: (
                    item.output_relative_path or "",
                    item.source_relative_path or "",
                ),
            )
        ],
        "reproduction_limitations": sorted(reproduction_limitations),
        "remote_refs": sorted(remote_refs.items()),
        "remote_tags": sorted((remote_tags or {}).items()),
        "remote_head": remote_head,
        "expected_remote_refs": sorted((expected_remote_refs or {}).items()),
        "expected_remote_tags": sorted((expected_remote_tags or {}).items()),
        "ref_updates": [
            update.to_json()
            for update in sorted(ref_updates, key=lambda item: item.ref)
        ],
        "history_disposition": history_disposition.value,
    }
    return hashlib.sha256(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()).hexdigest()


def _canonical_github_locator(owner: str, repository: str) -> str:
    normalized_repository = repository.removesuffix(".git")
    if (
        re.fullmatch(r"[A-Za-z0-9_.-]+", owner) is None
        or re.fullmatch(r"[A-Za-z0-9_.-]+", normalized_repository) is None
        or normalized_repository in {"", ".", ".."}
        or owner in {".", ".."}
    ):
        raise ValueError("GitHub repository owner or name is invalid.")
    return f"https://github.com/{owner}/{normalized_repository}.git"


def _publication_relative_path(value: str) -> str:
    path = PurePosixPath(value.replace("\\", "/"))
    normalized = path.as_posix()
    if (
        normalized in {"", ".", ".."}
        or normalized.startswith("../")
        or normalized.startswith("/")
        or any(part in {".", ".."} for part in path.parts)
        or "\n" in normalized
        or "\r" in normalized
    ):
        raise ValueError("Publication submodule path must be a non-root relative path.")
    return normalized


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
