from __future__ import annotations

from pathlib import Path
import unittest

from isomer_labs.topic_git import (
    AncestorRepositoryEvidence,
    LocalCandidateDisposition,
    LocalPlanFingerprint,
    LocalRepositoryEvidence,
    NestedWorkspacePointer,
    classify_local_candidate,
    evaluate_ancestor_repositories,
    render_local_version_manifest,
    update_local_managed_ignore,
    verify_exact_index,
)


class TopicGitLocalTests(unittest.TestCase):
    def test_no_ancestor_repository_satisfies_prerequisite(self) -> None:
        self.assertEqual((), evaluate_ancestor_repositories(Path("/project/topic"), ()))

    def test_tracked_or_unignored_ancestor_blocks_local_init(self) -> None:
        source = Path("/project/isomer-content/topic-ws/topic-a")
        blockers = evaluate_ancestor_repositories(
            source,
            (
                AncestorRepositoryEvidence(
                    top_level=Path("/project"),
                    source_tracked=True,
                    tracked_paths=("isomer-content/topic-ws/topic-a/README.md",),
                    source_ignored=False,
                ),
            ),
        )
        self.assertTrue(any("tracks" in blocker for blocker in blockers))
        self.assertTrue(any("does not effectively ignore" in blocker for blocker in blockers))

    def test_effectively_ignored_untracked_ancestor_is_safe(self) -> None:
        source = Path("/project/isomer-content/topic-ws/topic-a")
        self.assertEqual(
            (),
            evaluate_ancestor_repositories(
                source,
                (
                    AncestorRepositoryEvidence(
                        top_level=Path("/project"),
                        source_tracked=False,
                        tracked_paths=(),
                        source_ignored=True,
                        ignore_evidence=".gitignore:3:isomer-content/",
                    ),
                ),
            ),
        )

    def test_ancestor_project_repository_does_not_enable_local_tracking(self) -> None:
        source = Path("/project/topic")
        evidence = LocalRepositoryEvidence(
            top_level=Path("/project"),
            git_dir_valid=True,
            head_sha="abcdef1",
            index_paths=(),
            working_tree_fingerprint="a" * 64,
            ignore_fingerprint="b" * 64,
        )
        self.assertEqual("disabled", evidence.local_state(source))
        self.assertTrue(evidence.repository_identity(source).startswith("ancestor:"))

    def test_candidate_classification_uses_whole_files_and_redacted_warnings(self) -> None:
        self.assertEqual(
            LocalCandidateDisposition.IGNORE,
            classify_local_candidate("runtime/state.sqlite").disposition,
        )
        warning = classify_local_candidate("config.txt", b"api_key=abcdefghijk")
        self.assertEqual(LocalCandidateDisposition.WARN, warning.disposition)
        self.assertNotIn("abcdefghijk", " ".join(warning.reasons))
        self.assertEqual(
            LocalCandidateDisposition.BLOCK,
            classify_local_candidate(".git/config").disposition,
        )

    def test_managed_ignore_is_idempotent_and_preserves_user_rules(self) -> None:
        original = "*.bak\n# user rule\n"
        first = update_local_managed_ignore(
            original,
            nested_workspace_paths=("repos/topic-main", "actors/reviewer", "agents/coder"),
        )
        second = update_local_managed_ignore(
            first,
            nested_workspace_paths=("repos/topic-main", "actors/reviewer", "agents/coder"),
        )
        self.assertEqual(first, second)
        self.assertTrue(first.startswith(original))
        self.assertIn("/repos/topic-main/", first)
        self.assertIn("/actors/reviewer/", first)
        self.assertIn("/agents/coder/", first)

    def test_exact_index_rejects_missing_and_unexpected_paths(self) -> None:
        diagnostics = verify_exact_index(
            ("README.md", "unexpected.txt"),
            ("README.md", "topic-workspace.toml"),
        )
        self.assertIn("unexpected staged path: unexpected.txt", diagnostics)
        self.assertIn("approved path is not staged: topic-workspace.toml", diagnostics)
        self.assertEqual((), verify_exact_index(("README.md",), ("README.md",)))

    def test_local_plan_fingerprint_stales_on_own_layer_changes_only(self) -> None:
        evidence = LocalRepositoryEvidence(
            top_level=Path("/project/topic"),
            git_dir_valid=True,
            head_sha="abcdef1",
            index_paths=(),
            working_tree_fingerprint="a" * 64,
            ignore_fingerprint="b" * 64,
        )
        initial = LocalPlanFingerprint.from_evidence(evidence, approved_paths=("README.md",))
        repeated = LocalPlanFingerprint.from_evidence(evidence, approved_paths=("README.md",))
        changed = LocalPlanFingerprint.from_evidence(
            LocalRepositoryEvidence(
                top_level=evidence.top_level,
                git_dir_valid=True,
                head_sha="abcdef2",
                index_paths=(),
                working_tree_fingerprint=evidence.working_tree_fingerprint,
                ignore_fingerprint=evidence.ignore_fingerprint,
            ),
            approved_paths=("README.md",),
        )
        self.assertEqual(initial, repeated)
        self.assertNotEqual(initial, changed)

    def test_local_version_manifest_records_relative_pointers_not_content(self) -> None:
        rendered = render_local_version_manifest(
            (
                NestedWorkspacePointer(
                    label="topic.repos.main",
                    relative_path="repos/topic-main",
                    branch="topic-owner/main",
                    commit_sha="abcdef1",
                    dirty=True,
                ),
            )
        )
        self.assertIn('path = "repos/topic-main"', rendered)
        self.assertIn('branch = "topic-owner/main"', rendered)
        self.assertIn("dirty = true", rendered)
        self.assertIn("Pointers only", rendered)
        self.assertNotIn("/project/", rendered)


if __name__ == "__main__":
    unittest.main()
