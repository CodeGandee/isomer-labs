"""Current-state publication snapshot planning and topology validation."""

from __future__ import annotations

import re
from typing import Iterable, Mapping

from isomer_labs.topic_git.models import (
    ComponentBinding,
    ComponentSelection,
    PrivacyDisposition,
    PublicationBinding,
    PublicationSnapshotMode,
    ReferenceRepositoryBinding,
)
from isomer_labs.topic_git.projection import (
    PUBLICATION_METADATA_ROOT,
    PUBLICATION_ROOT_GENERATED_PATHS,
    ProjectionEntry,
    validate_projection_entries,
)
from isomer_labs.topic_git.publication import (
    CANONICAL_PUBLICATION_BRANCH,
    BranchCompatibility,
    BranchCompatibilityState,
    SnapshotReplacementPlan,
    _COMPONENT_BRANCH_RE,
    _EXACT_GIT_COMMIT_RE,
    _publication_relative_path,
    validate_remote_locator,
)


_SAFE_REF_RE = re.compile(
    r"^(?!/)(?!.*(?:\.\.|@\{|//))[A-Za-z0-9._/-]+(?<![/.])$"
)


def classify_remote_branch(
    *,
    branch: str,
    local_commit: str | None,
    remote_commit: str | None,
    remote_is_ancestor: bool | None,
) -> BranchCompatibility:
    """Classify caller-supplied fetch and ancestry evidence."""

    if (
        branch != CANONICAL_PUBLICATION_BRANCH
        and _COMPONENT_BRANCH_RE.fullmatch(branch) is None
    ):
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
        return BranchCompatibility(
            branch,
            BranchCompatibilityState.ABSENT,
            local_commit,
            None,
            "remote ref is absent",
        )
    if remote_commit == local_commit:
        return BranchCompatibility(
            branch,
            BranchCompatibilityState.COMPATIBLE,
            local_commit,
            remote_commit,
            "remote ref already matches the exact current snapshot",
        )
    return BranchCompatibility(
        branch,
        BranchCompatibilityState.INCOMPATIBLE,
        local_commit,
        remote_commit,
        "remote ref requires current-snapshot replacement",
    )


def component_push_order(components: Iterable[ComponentBinding]) -> tuple[str, ...]:
    branches = sorted(
        {
            component.branch
            for component in components
            if component.selection is ComponentSelection.SELECTED
        }
    )
    return (*branches, CANONICAL_PUBLICATION_BRANCH)


def validate_exclusive_snapshot_authority(
    binding: PublicationBinding,
    *,
    remote_url: str,
    research_topic_id: str,
    topic_workspace_id: str,
    snapshot_mode: PublicationSnapshotMode = PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT,
) -> tuple[str, ...]:
    """Require the persistent authority to match the exact remote and Topic Workspace identity."""

    diagnostics: list[str] = []
    if binding.snapshot_mode is not snapshot_mode:
        diagnostics.append("Publication Binding does not grant exclusive-snapshot authority.")
    if binding.canonical_branch != CANONICAL_PUBLICATION_BRANCH:
        diagnostics.append("Publication Binding canonical branch is not main.")
    if binding.remote_url.strip() != remote_url.strip():
        diagnostics.append("Publication Binding remote identity changed.")
    if binding.research_topic_id != research_topic_id:
        diagnostics.append("Publication Binding Research Topic identity changed.")
    if binding.topic_workspace_id != topic_workspace_id:
        diagnostics.append("Publication Binding Topic Workspace identity changed.")
    if validate_remote_locator(binding.remote_url):
        diagnostics.append("Publication Binding remote locator is no longer credential-safe.")
    expected_payload = binding.to_json()
    if (
        binding.snapshot_mode is not None
        and expected_payload.get("authority_fingerprint")
        != binding.authority_fingerprint()
    ):
        diagnostics.append("Publication Binding authority fingerprint is invalid.")
    return tuple(diagnostics)


def plan_snapshot_replacement(
    *,
    plan_id: str,
    binding: PublicationBinding,
    observed_refs: Mapping[str, str],
    expected_refs: Mapping[str, str],
    observed_tags: Mapping[str, str] | None = None,
    expected_tags: Mapping[str, str] | None = None,
    observed_remote_head: str | None = None,
    push_order: Iterable[str],
) -> SnapshotReplacementPlan:
    """Create a complete current-state ref and tag replacement plan."""

    if binding.snapshot_mode is not PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT:
        raise ValueError("Whole-remote replacement requires exclusive-snapshot authority.")
    if binding.canonical_branch != CANONICAL_PUBLICATION_BRANCH:
        raise ValueError("Whole-remote replacement requires canonical branch main.")
    expected = dict(expected_refs)
    if CANONICAL_PUBLICATION_BRANCH not in expected:
        raise ValueError("Expected snapshot refs must include canonical main.")
    order = tuple(push_order)
    if not order or order[-1] != CANONICAL_PUBLICATION_BRANCH:
        raise ValueError("Snapshot push order must publish main last.")
    if set(order) != set(expected):
        raise ValueError("Snapshot push order must cover the complete expected branch set.")
    for ref, commit in observed_refs.items():
        _validate_git_ref(ref, commit)
    for ref, commit in expected.items():
        _validate_snapshot_ref(ref, commit)
    for tag, commit in (
        *(observed_tags or {}).items(),
        *(expected_tags or {}).items(),
    ):
        _validate_snapshot_tag(tag, commit)
    return SnapshotReplacementPlan(
        plan_id=plan_id,
        binding_id=binding.binding_id,
        observed_refs=tuple(sorted(observed_refs.items())),
        expected_refs=tuple(sorted(expected.items())),
        observed_tags=tuple(sorted((observed_tags or {}).items())),
        expected_tags=tuple(sorted((expected_tags or {}).items())),
        observed_remote_head=observed_remote_head,
        push_order=order,
    )


def validate_snapshot_replacement(
    plan: SnapshotReplacementPlan,
    *,
    binding: PublicationBinding,
    current_refs: Mapping[str, str],
    current_tags: Mapping[str, str],
    current_remote_head: str | None,
    requested_refs: Mapping[str, str],
    requested_tags: Mapping[str, str],
) -> tuple[str, ...]:
    """Reject stale or partial whole-snapshot replacement without repeated ref approvals."""

    diagnostics: list[str] = []
    if binding.binding_id != plan.binding_id:
        diagnostics.append("Snapshot plan binding identity changed.")
    if binding.snapshot_mode is not PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT:
        diagnostics.append("Snapshot replacement lacks exclusive-snapshot authority.")
    if dict(plan.observed_refs) != dict(current_refs):
        diagnostics.append(
            "Snapshot plan is stale because the complete remote ref set changed."
        )
    if dict(plan.observed_tags) != dict(current_tags):
        diagnostics.append(
            "Snapshot plan is stale because the complete remote tag set changed."
        )
    if plan.observed_remote_head != current_remote_head:
        diagnostics.append("Snapshot plan is stale because remote HEAD changed.")
    if dict(plan.expected_refs) != dict(requested_refs):
        diagnostics.append("Requested refs differ from the complete approved snapshot.")
    if dict(plan.expected_tags) != dict(requested_tags):
        diagnostics.append("Requested tags differ from the complete approved snapshot.")
    if plan.push_order[-1:] != (CANONICAL_PUBLICATION_BRANCH,):
        diagnostics.append("Snapshot plan does not publish canonical main last.")
    return tuple(diagnostics)


def validate_generated_publication_paths(
    *,
    source_paths: Iterable[str],
    generated_paths: Iterable[str],
) -> tuple[str, ...]:
    """Reject reserved-overlay collisions and generated paths outside the approved namespace."""

    sources = {_publication_relative_path(path) for path in source_paths}
    generated = {_publication_relative_path(path) for path in generated_paths}
    diagnostics: list[str] = []
    if any(
        path == PUBLICATION_METADATA_ROOT
        or path.startswith(f"{PUBLICATION_METADATA_ROOT}/")
        for path in sources
    ):
        diagnostics.append(
            "Source Topic Workspace collides with reserved .isomer-publication/ metadata."
        )
    if ".gitmodules" in sources:
        diagnostics.append(
            "Source Topic Workspace .gitmodules conflicts with generated submodule topology."
        )
    allowed_root = set(PUBLICATION_ROOT_GENERATED_PATHS)
    for path in sorted(generated):
        if path not in allowed_root and not path.startswith(
            f"{PUBLICATION_METADATA_ROOT}/"
        ):
            diagnostics.append(
                f"generated publication path is outside the reserved overlay: {path}"
            )
        if path in sources and path != "README.md":
            diagnostics.append(f"generated publication path shadows source content: {path}")
    return tuple(diagnostics)


def validate_latest_paper_mapping(
    latest_paper_path: str | None,
    *,
    approved_artifact_paths: Iterable[str],
) -> tuple[str, ...]:
    """Require README navigation to target one approved path-preserved paper Artifact."""

    if latest_paper_path is None:
        return ()
    normalized = _publication_relative_path(latest_paper_path)
    approved = {_publication_relative_path(path) for path in approved_artifact_paths}
    if normalized not in approved:
        return (
            "Latest paper path is not an approved path-preserved Artifact; relocated aliases are forbidden.",
        )
    return ()


def validate_staged_publication_topology(
    actual_index: Mapping[str, str],
    *,
    entries: Iterable[ProjectionEntry],
    components: Iterable[ComponentBinding],
    references: Iterable[ReferenceRepositoryBinding] = (),
    generated_paths: Iterable[str] = (),
) -> tuple[str, ...]:
    """Verify the complete staged path set and exact gitlink modes."""

    entry_list = tuple(entries)
    diagnostics = [
        finding.message for finding in validate_projection_entries(entry_list)
    ]
    expected_regular = {
        entry.output_relative_path
        for entry in entry_list
        if entry.output_relative_path is not None
        and entry.disposition
        in {PrivacyDisposition.TRACK, PrivacyDisposition.TEMPLATE}
    }
    expected_gitlinks = {
        component.relative_path
        for component in components
        if component.selection is ComponentSelection.SELECTED
    } | {
        reference.relative_path
        for reference in references
        if reference.selection is ComponentSelection.SELECTED
    }
    expected = {
        *(path for path in expected_regular if path is not None),
        *(_publication_relative_path(path) for path in generated_paths),
        *(_publication_relative_path(path) for path in expected_gitlinks),
    }
    actual = set(actual_index)
    diagnostics.extend(
        f"unexpected staged path: {path}" for path in sorted(actual - expected)
    )
    diagnostics.extend(
        f"approved path is not staged: {path}" for path in sorted(expected - actual)
    )
    for path in sorted(expected_gitlinks):
        normalized = _publication_relative_path(path)
        if actual_index.get(normalized) != "160000":
            diagnostics.append(
                "publication component is not an exact mode 160000 gitlink: "
                f"{normalized}"
            )
    for path in sorted(expected_regular):
        if path is not None and actual_index.get(path) == "160000":
            diagnostics.append(
                f"ordinary publication path unexpectedly became a gitlink: {path}"
            )
    for component_path in sorted(expected_gitlinks):
        prefix = f"{_publication_relative_path(component_path)}/"
        for path in sorted(actual):
            if path.startswith(prefix):
                diagnostics.append(
                    f"component files were flattened into the superproject: {path}"
                )
    return tuple(diagnostics)


def legacy_publication_refs(
    remote_refs: Mapping[str, str],
    *,
    expected_refs: Iterable[str],
) -> tuple[str, ...]:
    """Return every current remote branch outside the approved current snapshot."""

    expected = set(expected_refs)
    return tuple(sorted(ref for ref in remote_refs if ref not in expected))


def remote_head_action_required(observed_remote_head: str | None) -> bool:
    """Report provider default-branch work without mutating provider state."""

    return observed_remote_head != CANONICAL_PUBLICATION_BRANCH


def _validate_git_ref(ref: str, commit: str) -> None:
    if _SAFE_REF_RE.fullmatch(ref) is None:
        raise ValueError(f"Remote ref name is invalid: {ref!r}")
    if _EXACT_GIT_COMMIT_RE.fullmatch(commit) is None:
        raise ValueError(f"Remote ref commit is invalid: {ref}")


def _validate_snapshot_ref(ref: str, commit: str) -> None:
    _validate_git_ref(ref, commit)
    if (
        ref != CANONICAL_PUBLICATION_BRANCH
        and _COMPONENT_BRANCH_RE.fullmatch(ref) is None
    ):
        raise ValueError(
            f"Expected snapshot ref is outside the publication namespace: {ref}"
        )


def _validate_snapshot_tag(tag: str, commit: str) -> None:
    _validate_git_ref(tag, commit)
