"""Current-state publication snapshot planning and topology validation."""

from __future__ import annotations

import re
from typing import Iterable, Mapping

from isomer_labs.topic_git.history_models import (
    HistoryAwarePublicationPlan,
    PublicationHistoryCompatibility,
    PublicationHistoryDisposition,
    PublicationRefUpdate,
    PublicationRefUpdateStrategy,
)
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
_SAFE_REMOTE_NAME_RE = re.compile(r"^[A-Za-z0-9._-]+$")


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
    if remote_is_ancestor is True:
        return BranchCompatibility(
            branch,
            BranchCompatibilityState.COMPATIBLE,
            local_commit,
            remote_commit,
            "remote ref is the verified direct publication-history base",
        )
    if remote_is_ancestor is None:
        return BranchCompatibility(
            branch,
            BranchCompatibilityState.BLOCKED,
            local_commit,
            remote_commit,
            "remote ancestry evidence is unavailable",
        )
    return BranchCompatibility(
        branch,
        BranchCompatibilityState.INCOMPATIBLE,
        local_commit,
        remote_commit,
        "remote ref is not an ancestor of the planned publication commit",
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


def history_withdrawal_replacement_scope(
    affected_refs: Iterable[str],
) -> tuple[str, ...]:
    """Expand a history-purge fallback to canonical main when a component is affected."""

    affected = set(affected_refs)
    for ref in affected:
        if ref != CANONICAL_PUBLICATION_BRANCH and _COMPONENT_BRANCH_RE.fullmatch(ref) is None:
            raise ValueError(f"History-withdrawal ref is outside the publication namespace: {ref}")
    if any(ref != CANONICAL_PUBLICATION_BRANCH for ref in affected):
        affected.add(CANONICAL_PUBLICATION_BRANCH)
    return tuple(sorted(affected - {CANONICAL_PUBLICATION_BRANCH})) + (
        ((CANONICAL_PUBLICATION_BRANCH,) if CANONICAL_PUBLICATION_BRANCH in affected else ())
    )


def plan_history_aware_publication(
    *,
    plan_id: str,
    binding: PublicationBinding,
    observed_refs: Mapping[str, str],
    expected_refs: Mapping[str, str],
    compatibility_by_ref: Mapping[str, PublicationHistoryCompatibility],
    observed_tags: Mapping[str, str] | None = None,
    expected_tags: Mapping[str, str] | None = None,
    observed_remote_head: str | None = None,
    push_order: Iterable[str],
    history_disposition: PublicationHistoryDisposition = PublicationHistoryDisposition.RETAIN,
    force_replacement_refs: Iterable[str] = (),
    history_withdrawal_refs: Iterable[str] = (),
    fallback_reasons: Mapping[str, str] | None = None,
    conflicted_refs: Iterable[str] = (),
) -> HistoryAwarePublicationPlan:
    """Plan complete ref synchronization while preferring sanitized fast-forwards."""

    if binding.canonical_branch != CANONICAL_PUBLICATION_BRANCH:
        raise ValueError("Publication synchronization requires canonical branch main.")
    expected = dict(expected_refs)
    observed = dict(observed_refs)
    if CANONICAL_PUBLICATION_BRANCH not in expected:
        raise ValueError("Expected publication refs must include canonical main.")
    order = tuple(push_order)
    if not order or order[-1] != CANONICAL_PUBLICATION_BRANCH:
        raise ValueError("Publication push order must publish main last.")
    if set(order) != set(expected):
        raise ValueError("Publication push order must cover the complete expected branch set.")
    for ref, commit in observed.items():
        _validate_git_ref(ref, commit)
    for ref, commit in expected.items():
        _validate_snapshot_ref(ref, commit)
    for tag, commit in (
        *(observed_tags or {}).items(),
        *(expected_tags or {}).items(),
    ):
        _validate_snapshot_tag(tag, commit)

    forced = set(force_replacement_refs)
    withdrawals = set(history_withdrawal_refs)
    forced.update(history_withdrawal_replacement_scope(withdrawals))
    if history_disposition is PublicationHistoryDisposition.PURGE:
        forced.update(ref for ref in expected if ref in observed)
    conflicts = set(conflicted_refs)
    unknown_conflicts = conflicts - set(expected)
    if unknown_conflicts:
        raise ValueError(
            "Conflicted refs are outside the expected publication scope: "
            + ", ".join(sorted(unknown_conflicts))
        )
    reasons = dict(fallback_reasons or {})
    blockers = [
        f"publication destination conflict blocks mutation for {ref}"
        for ref in sorted(conflicts)
    ]
    updates: list[PublicationRefUpdate] = []
    for ref in order:
        planned_commit = expected[ref]
        observed_commit = observed.get(ref)
        compatibility = compatibility_by_ref.get(
            ref,
            PublicationHistoryCompatibility(
                compatible=False,
                evidence=(),
                reason="publication-history compatibility evidence is unavailable",
            ),
        )
        fallback_reason: str | None = None
        if observed_commit is None:
            strategy = PublicationRefUpdateStrategy.CREATE
            base_commit = None
        elif ref in forced:
            strategy = PublicationRefUpdateStrategy.FORCE_REPLACEMENT
            base_commit = None
            fallback_reason = reasons.get(ref)
            if fallback_reason is None:
                fallback_reason = (
                    "current privacy plan requires prior publication history to be purged"
                    if ref in history_withdrawal_replacement_scope(withdrawals)
                    or history_disposition is PublicationHistoryDisposition.PURGE
                    else compatibility.reason
                )
        elif observed_commit == planned_commit:
            strategy = PublicationRefUpdateStrategy.NO_OP
            base_commit = observed_commit
        elif compatibility.compatible:
            strategy = PublicationRefUpdateStrategy.FAST_FORWARD
            base_commit = observed_commit
        else:
            strategy = PublicationRefUpdateStrategy.FORCE_REPLACEMENT
            base_commit = None
            fallback_reason = reasons.get(ref) or compatibility.reason
        if strategy is PublicationRefUpdateStrategy.FORCE_REPLACEMENT:
            if binding.snapshot_mode is not PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT:
                blockers.append(f"force replacement lacks exclusive_snapshot authority for {ref}")
            if not fallback_reason:
                blockers.append(f"force replacement lacks an exact fallback reason for {ref}")
        updates.append(
            PublicationRefUpdate(
                ref=ref,
                strategy=strategy,
                observed_commit=observed_commit,
                base_commit=base_commit,
                planned_commit=planned_commit,
                compatibility=compatibility,
                fallback_reason=fallback_reason,
            )
        )
    deletions_exist = bool(set(observed) - set(expected)) or bool(
        set(observed_tags or {}) - set(expected_tags or {})
    )
    if (
        deletions_exist
        and binding.snapshot_mode is not PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT
    ):
        blockers.append("obsolete ref or tag deletion lacks exclusive_snapshot authority")
    return HistoryAwarePublicationPlan(
        plan_id=plan_id,
        binding_id=binding.binding_id,
        observed_refs=tuple(sorted(observed.items())),
        expected_refs=tuple(sorted(expected.items())),
        observed_tags=tuple(sorted((observed_tags or {}).items())),
        expected_tags=tuple(sorted((expected_tags or {}).items())),
        observed_remote_head=observed_remote_head,
        history_disposition=history_disposition,
        ref_updates=tuple(updates),
        push_order=order,
        blockers=tuple(blockers),
    )


def validate_history_aware_publication(
    plan: HistoryAwarePublicationPlan,
    *,
    binding: PublicationBinding,
    current_refs: Mapping[str, str],
    current_tags: Mapping[str, str],
    current_remote_head: str | None,
    requested_refs: Mapping[str, str],
    requested_tags: Mapping[str, str],
) -> tuple[str, ...]:
    """Reject stale, partial, blocked, or internally inconsistent synchronization."""

    diagnostics = list(plan.blockers)
    if binding.binding_id != plan.binding_id:
        diagnostics.append("Publication plan binding identity changed.")
    if binding.canonical_branch != CANONICAL_PUBLICATION_BRANCH:
        diagnostics.append("Publication Binding canonical branch is not main.")
    if dict(plan.observed_refs) != dict(current_refs):
        diagnostics.append("Publication plan is stale because the complete remote ref set changed.")
    if dict(plan.observed_tags) != dict(current_tags):
        diagnostics.append("Publication plan is stale because the complete remote tag set changed.")
    if plan.observed_remote_head != current_remote_head:
        diagnostics.append("Publication plan is stale because remote HEAD changed.")
    if dict(plan.expected_refs) != dict(requested_refs):
        diagnostics.append("Requested refs differ from the complete approved publication.")
    if dict(plan.expected_tags) != dict(requested_tags):
        diagnostics.append("Requested tags differ from the complete approved publication.")
    if plan.push_order[-1:] != (CANONICAL_PUBLICATION_BRANCH,):
        diagnostics.append("Publication plan does not publish canonical main last.")
    expected_updates = {ref for ref, _ in plan.expected_refs}
    actual_updates = {update.ref for update in plan.ref_updates}
    if actual_updates != expected_updates or len(actual_updates) != len(plan.ref_updates):
        diagnostics.append("Publication plan does not contain exactly one strategy per expected ref.")
    observed = dict(plan.observed_refs)
    expected = dict(plan.expected_refs)
    for update in plan.ref_updates:
        if update.observed_commit != observed.get(update.ref):
            diagnostics.append(f"Planned observed commit differs for {update.ref}.")
        if update.planned_commit != expected.get(update.ref):
            diagnostics.append(f"Planned result commit differs for {update.ref}.")
        if update.strategy is PublicationRefUpdateStrategy.CREATE:
            if update.observed_commit is not None or update.base_commit is not None:
                diagnostics.append(f"Create strategy has a remote base for {update.ref}.")
        elif update.strategy is PublicationRefUpdateStrategy.NO_OP:
            if update.observed_commit != update.planned_commit:
                diagnostics.append(f"No-op strategy is not already exact for {update.ref}.")
        elif update.strategy is PublicationRefUpdateStrategy.FAST_FORWARD:
            if (
                update.base_commit != update.observed_commit
                or not update.compatibility.compatible
            ):
                diagnostics.append(f"Fast-forward strategy lacks a compatible exact base for {update.ref}.")
        elif update.strategy is PublicationRefUpdateStrategy.FORCE_REPLACEMENT:
            if (
                binding.snapshot_mode is not PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT
                or update.observed_commit is None
                or update.fallback_reason is None
            ):
                diagnostics.append(f"Force replacement lacks authority, lease, or reason for {update.ref}.")
    return tuple(diagnostics)


def publication_push_arguments(
    update: PublicationRefUpdate,
    *,
    remote_name: str,
) -> tuple[str, ...]:
    """Return an exact Git push argument vector for one approved branch strategy."""

    if _SAFE_REMOTE_NAME_RE.fullmatch(remote_name) is None:
        raise ValueError("Publication remote name is unsafe.")
    _validate_snapshot_ref(update.ref, update.planned_commit)
    destination = f"refs/heads/{update.ref}"
    refspec = f"{update.planned_commit}:{destination}"
    if update.strategy is PublicationRefUpdateStrategy.NO_OP:
        return ()
    if update.strategy in {
        PublicationRefUpdateStrategy.CREATE,
        PublicationRefUpdateStrategy.FAST_FORWARD,
    }:
        return ("push", remote_name, refspec)
    if update.observed_commit is None:
        raise ValueError("Force replacement requires the exact observed commit lease.")
    _validate_git_ref(update.ref, update.observed_commit)
    return (
        "push",
        f"--force-with-lease={destination}:{update.observed_commit}",
        remote_name,
        refspec,
    )


def publication_delete_push_arguments(
    *,
    ref: str,
    observed_commit: str,
    remote_name: str,
    tag: bool = False,
) -> tuple[str, ...]:
    """Return an exact leased deletion argument vector for one approved ref."""

    if _SAFE_REMOTE_NAME_RE.fullmatch(remote_name) is None:
        raise ValueError("Publication remote name is unsafe.")
    _validate_git_ref(ref, observed_commit)
    namespace = "refs/tags" if tag else "refs/heads"
    destination = f"{namespace}/{ref}"
    return (
        "push",
        f"--force-with-lease={destination}:{observed_commit}",
        remote_name,
        f":{destination}",
    )


def expected_publication_commit_parents(
    update: PublicationRefUpdate,
) -> tuple[str, ...] | None:
    """Return the required parents, or None when no commit may be created."""

    if update.strategy is PublicationRefUpdateStrategy.NO_OP:
        return None
    if update.strategy is PublicationRefUpdateStrategy.FAST_FORWARD:
        if update.base_commit is None:
            raise ValueError("Fast-forward publication requires an exact base commit.")
        return (update.base_commit,)
    return ()


def validate_publication_commit_parents(
    update: PublicationRefUpdate,
    *,
    actual_parents: Iterable[str] | None,
) -> tuple[str, ...]:
    """Verify root or direct-parent commit shape without admitting another lineage."""

    expected = expected_publication_commit_parents(update)
    actual = tuple(actual_parents) if actual_parents is not None else None
    if expected != actual:
        return (
            f"publication commit parents differ for {update.ref}: expected {expected}, got {actual}",
        )
    return ()


def next_publication_resume_ref(
    plan: HistoryAwarePublicationPlan,
    *,
    current_refs: Mapping[str, str],
) -> str | None:
    """Return the next safe ref after recognizing exact completed outcomes."""

    observed = dict(plan.observed_refs)
    expected = dict(plan.expected_refs)
    for ref in plan.push_order:
        current = current_refs.get(ref)
        if current not in {observed.get(ref), expected[ref]}:
            raise ValueError(f"Publication resume state is stale for {ref}.")
    main_current = current_refs.get(CANONICAL_PUBLICATION_BRANCH)
    incomplete_components = [
        ref
        for ref in plan.push_order[:-1]
        if current_refs.get(ref) != expected[ref]
    ]
    if main_current == expected[CANONICAL_PUBLICATION_BRANCH] and incomplete_components:
        raise ValueError("Canonical main advanced before every planned component result.")
    for ref in plan.push_order:
        if current_refs.get(ref) != expected[ref]:
            return ref
    return None


def validate_completed_publication(
    plan: HistoryAwarePublicationPlan,
    *,
    actual_refs: Mapping[str, str],
    actual_tags: Mapping[str, str],
    actual_parents: Mapping[str, Iterable[str]],
    publication_copies_clean: bool,
    recursive_clone_succeeded: bool,
) -> tuple[str, ...]:
    """Verify exact final refs, planned ancestry, clean copies, and recursive clone."""

    diagnostics: list[str] = []
    if dict(plan.expected_refs) != dict(actual_refs):
        diagnostics.append("Final remote branch set differs from the approved publication.")
    if dict(plan.expected_tags) != dict(actual_tags):
        diagnostics.append("Final remote tag set differs from the approved publication.")
    for update in plan.ref_updates:
        if update.strategy is PublicationRefUpdateStrategy.NO_OP:
            continue
        diagnostics.extend(
            validate_publication_commit_parents(
                update,
                actual_parents=actual_parents.get(update.ref),
            )
        )
    if not publication_copies_clean:
        diagnostics.append("A Topic Publication Copy is not clean after synchronization.")
    if not recursive_clone_succeeded:
        diagnostics.append("Fresh recursive clone verification failed.")
    return tuple(diagnostics)


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
