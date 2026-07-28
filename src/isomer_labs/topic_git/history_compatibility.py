"""Compatibility evidence and copy preparation for sanitized publication history."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from pathlib import Path
from typing import Iterable

from isomer_labs.topic_git.history_models import (
    PublicationHistoryCompatibility,
    PublicationHistoryDisposition,
)
from isomer_labs.topic_git.models import PublicationBinding, PublicationSnapshotMode
from isomer_labs.topic_git.projection import ProjectionManifest
from isomer_labs.topic_git.publication import (
    CANONICAL_PUBLICATION_BRANCH,
    _COMPONENT_BRANCH_RE,
)


class PublicationCopyPreparationAction(StrEnum):
    REUSE = "reuse"
    RECOVER = "recover"
    BLOCK = "block"


@dataclass(frozen=True)
class PublicationCopyPreparationPlan:
    action: PublicationCopyPreparationAction
    repository_path: Path | None
    reason: str
    preserves_existing_copy: bool


def plan_publication_copy_preparation(
    *,
    copy_path: Path,
    recovery_path: Path,
    copy_exists: bool,
    copy_clean: bool,
    binding_matches: bool,
    current_head: str | None,
    expected_base: str | None,
    remote_recovery_available: bool,
) -> PublicationCopyPreparationPlan:
    """Choose safe reuse, disposable remote recovery, or a preserving blocker."""

    if (
        copy_exists
        and copy_clean
        and binding_matches
        and current_head == expected_base
    ):
        return PublicationCopyPreparationPlan(
            PublicationCopyPreparationAction.REUSE,
            copy_path,
            "existing Topic Publication Copy is clean and based on the exact observed commit",
            False,
        )
    if not remote_recovery_available:
        return PublicationCopyPreparationPlan(
            PublicationCopyPreparationAction.BLOCK,
            None,
            "exact compatible remote recovery state is unavailable",
            copy_exists,
        )
    if copy_exists and recovery_path == copy_path:
        return PublicationCopyPreparationPlan(
            PublicationCopyPreparationAction.BLOCK,
            None,
            "an unusable existing Topic Publication Copy requires a separate recovery path",
            True,
        )
    target = recovery_path if copy_exists else copy_path
    return PublicationCopyPreparationPlan(
        PublicationCopyPreparationAction.RECOVER,
        target,
        "recover exact planned refs into a validated disposable publication repository",
        copy_exists,
    )


def evaluate_publication_history_compatibility(
    *,
    binding: PublicationBinding,
    manifest: ProjectionManifest,
    branch: str,
    remote_is_ancestor: bool | None,
    remote_commit_fetched: bool,
    topology_diagnostics: Iterable[str] = (),
    pinned_component_commit: str | None = None,
    observed_component_commit: str | None = None,
    history_disposition: PublicationHistoryDisposition = PublicationHistoryDisposition.RETAIN,
) -> PublicationHistoryCompatibility:
    """Evaluate whether one observed sanitized publication commit may be a parent."""

    diagnostics: list[str] = []
    evidence: list[str] = []
    if binding.snapshot_mode is not PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT:
        diagnostics.append("Publication Binding lacks exclusive-snapshot fallback authority.")
    else:
        evidence.append("matching exclusive_snapshot Publication Binding")
    if binding.canonical_branch != CANONICAL_PUBLICATION_BRANCH:
        diagnostics.append("Publication Binding canonical branch is not main.")
    else:
        evidence.append("canonical publication branch is main")
    if manifest.binding_id != binding.binding_id:
        diagnostics.append("Tracked projection manifest binding identity differs.")
    else:
        evidence.append("tracked projection manifest binding matches")
    if manifest.source_schema_version not in {
        "isomer-topic-git-projection-manifest.v1",
        "isomer-topic-git-projection-manifest.v2",
        "isomer-topic-git-projection-manifest.v3",
    }:
        diagnostics.append("Tracked projection manifest schema is unsupported.")
    else:
        evidence.append(f"supported tracked manifest {manifest.source_schema_version}")
    if manifest.canonical_branch != CANONICAL_PUBLICATION_BRANCH:
        diagnostics.append("Tracked projection manifest canonical branch differs.")
    else:
        evidence.append("tracked canonical topology matches")
    if manifest.history_format not in {
        "legacy-sanitized-root.v1",
        "sanitized-linear.v1",
    }:
        diagnostics.append("Tracked publication history format is unsupported.")
    else:
        evidence.append(f"supported sanitized history format {manifest.history_format}")
    if (
        branch != CANONICAL_PUBLICATION_BRANCH
        and _COMPONENT_BRANCH_RE.fullmatch(branch) is None
    ):
        diagnostics.append("Branch is outside the deterministic publication namespace.")
    if not remote_commit_fetched:
        diagnostics.append("Observed remote commit was not fetched through an exact ref.")
    else:
        evidence.append("observed remote commit was fetched exactly")
    if remote_is_ancestor is not True:
        diagnostics.append("Observed remote commit is not a verified publication-history base.")
    else:
        evidence.append("observed remote commit is verified as the planned ancestor")
    topology_issues = tuple(str(item) for item in topology_diagnostics)
    diagnostics.extend(topology_issues)
    if not topology_issues:
        evidence.append("tracked component topology is valid")
    if (
        pinned_component_commit is not None
        and pinned_component_commit != observed_component_commit
    ):
        diagnostics.append("Tracked component pin differs from the observed component ref.")
    elif pinned_component_commit is not None:
        evidence.append("tracked component pin matches the observed component ref")
    if history_disposition is PublicationHistoryDisposition.PURGE:
        diagnostics.append("Current privacy plan requires prior publication history to be purged.")
    else:
        evidence.append("current privacy plan permits publication-history retention")
    return PublicationHistoryCompatibility(
        compatible=not diagnostics,
        evidence=tuple(evidence),
        reason="; ".join(diagnostics) if diagnostics else None,
    )
