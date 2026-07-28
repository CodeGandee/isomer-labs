from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from isomer_labs.topic_git import (
    BranchOutcome,
    BranchOutcomeStatus,
    LocalTrackingState,
    PrivacyDisposition,
    PublicationBinding,
    PublicationHistoryCompatibility,
    PublicationRefKind,
    PublicationRefOperation,
    PublicationRefOutcome,
    PublicationRefUpdate,
    PublicationRefUpdateStrategy,
    PublicationSnapshotMode,
    PublicationSnapshotOutcome,
    PublicationState,
    RemoteVisibility,
    SupportFileKind,
    TopicGitStatus,
    copy_support_root,
    load_support_file,
    promote_publication_binding,
    publication_plan_approval_is_stale,
    runtime_support_root,
    validate_support_payload,
    write_support_file,
)


class TopicGitModelTests(unittest.TestCase):
    def test_typed_state_values_cover_both_independent_layers(self) -> None:
        self.assertEqual(
            {"disabled", "enabled", "invalid"},
            {state.value for state in LocalTrackingState},
        )
        self.assertEqual(
            {"disabled", "prepared", "synchronized", "stale", "copy-missing", "blocked"},
            {state.value for state in PublicationState},
        )
        self.assertEqual(
            {"track", "template", "exclude", "component", "block"},
            {state.value for state in PrivacyDisposition},
        )
        self.assertEqual(
            {"private", "restricted", "public", "unknown"},
            {state.value for state in RemoteVisibility},
        )

    def test_overall_status_reports_four_layer_combinations(self) -> None:
        combinations = {
            (LocalTrackingState.DISABLED, PublicationState.DISABLED),
            (LocalTrackingState.ENABLED, PublicationState.DISABLED),
            (LocalTrackingState.DISABLED, PublicationState.PREPARED),
            (LocalTrackingState.ENABLED, PublicationState.SYNCHRONIZED),
        }
        for local, publication in combinations:
            with self.subTest(local=local, publication=publication):
                payload = TopicGitStatus(local, publication).to_json()
                self.assertEqual(local.value, payload["local"]["state"])  # type: ignore[index]
                self.assertEqual(publication.value, payload["publication"]["state"])  # type: ignore[index]

    def test_every_support_file_kind_has_a_valid_schema_example(self) -> None:
        digest = "a" * 64
        examples: dict[SupportFileKind, dict[str, object]] = {
            SupportFileKind.LOCAL_STATE: {
                "schema_version": "isomer-topic-git-local-state.v1",
                "research_topic_id": "topic-a",
                "topic_workspace_id": "workspace-a",
                "state": "enabled",
                "repository_identity": "root:workspace-a",
                "head_sha": "abcdef1",
                "ignore_fingerprint": digest,
                "nested_workspaces": [],
                "updated_at": "2026-07-23T00:00:00Z",
            },
            SupportFileKind.LOCAL_PLAN: {
                "schema_version": "isomer-topic-git-local-plan.v1",
                "plan_id": "local-plan-a",
                "research_topic_id": "topic-a",
                "topic_workspace_id": "workspace-a",
                "repository_fingerprint": digest,
                "approved_paths": ["README.md"],
                "approved_ignore_rules": ["/runtime/"],
                "secret_like_warnings": [],
                "approved_at": None,
            },
            SupportFileKind.PUBLICATION_BINDING: self._binding_payload(),
            SupportFileKind.PUBLICATION_PLAN: {
                "schema_version": "isomer-topic-git-publication-plan.v1",
                "plan_id": "publication-plan-a",
                "binding_id": "binding-a",
                "research_topic_id": "topic-a",
                "topic_workspace_id": "workspace-a",
                "copy_path": "tmp/topic-workspace-publish/topic-a",
                "visibility": "private",
                "fingerprints": {"source": digest},
                "entries": [],
                "components": [],
                "conflicts": [],
                "push_order": ["topic-workspace/main"],
                "blockers": [],
                "approval": {"privacy": True, "remote_mutation": False},
            },
            SupportFileKind.PROJECTION_MANIFEST: {
                "schema_version": "isomer-topic-git-projection-manifest.v1",
                "binding_id": "binding-a",
                "plan_id": "publication-plan-a",
                "created_at": "2026-07-23T00:00:00Z",
                "entries": [],
                "components": [],
            },
            SupportFileKind.PUBLICATION_OUTCOMES: {
                "schema_version": "isomer-topic-git-publication-outcomes.v1",
                "binding_id": "binding-a",
                "plan_id": "publication-plan-a",
                "branch_outcomes": [],
                "resume_at": None,
                "updated_at": "2026-07-23T00:00:00Z",
            },
        }
        self.assertEqual(set(SupportFileKind), set(examples))
        for kind, payload in examples.items():
            with self.subTest(kind=kind):
                self.assertEqual((), validate_support_payload(kind, payload))

    def test_support_validation_rejects_secrets_raw_diffs_and_credential_urls(self) -> None:
        payload = self._binding_payload()
        payload["remote_url"] = "https://user:password@example.test/topic.git?signature=value"
        diagnostics = validate_support_payload(SupportFileKind.PUBLICATION_BINDING, payload)
        self.assertTrue(any("credential-bearing" in diagnostic for diagnostic in diagnostics))

        plan = {
            "schema_version": "isomer-topic-git-publication-plan.v1",
            "plan_id": "plan",
            "binding_id": "binding",
            "research_topic_id": "topic",
            "topic_workspace_id": "workspace",
            "copy_path": "tmp/topic-workspace-publish/topic",
            "visibility": "private",
            "fingerprints": {},
            "entries": [],
            "components": [],
            "push_order": [],
            "blockers": [],
            "approval": {"token": "do-not-store"},
        }
        self.assertTrue(validate_support_payload(SupportFileKind.PUBLICATION_PLAN, plan))

    def test_support_writes_are_namespaced_and_never_target_state_database(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            runtime_root = runtime_support_root(root / "runtime")
            path = write_support_file(
                runtime_root / "publication-binding.json",
                support_root=runtime_root,
                kind=SupportFileKind.PUBLICATION_BINDING,
                payload=self._binding_payload(),
            )
            self.assertEqual(self._binding_payload(), load_support_file(path, kind=SupportFileKind.PUBLICATION_BINDING))
            with self.assertRaisesRegex(ValueError, "state.sqlite"):
                write_support_file(
                    runtime_root / "state.sqlite",
                    support_root=runtime_root,
                    kind=SupportFileKind.PUBLICATION_BINDING,
                    payload=self._binding_payload(),
                )

    def test_pre_runtime_binding_promotes_only_during_approved_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            publication_copy = root / "tmp" / "copy"
            source_root = copy_support_root(publication_copy)
            write_support_file(
                source_root / "publication-binding.json",
                support_root=source_root,
                kind=SupportFileKind.PUBLICATION_BINDING,
                payload=self._binding_payload(),
            )
            topic_runtime = root / "topic" / "runtime"
            with self.assertRaisesRegex(ValueError, "Read-only status"):
                promote_publication_binding(
                    publication_copy=publication_copy,
                    topic_runtime=topic_runtime,
                    expected_binding_id="binding-a",
                    approved_mutation=False,
                )
            promoted = promote_publication_binding(
                publication_copy=publication_copy,
                topic_runtime=topic_runtime,
                expected_binding_id="binding-a",
                approved_mutation=True,
            )
            self.assertEqual(runtime_support_root(topic_runtime) / "publication-binding.json", promoted)
            self.assertTrue(promoted.is_file())
            self.assertFalse((topic_runtime / "state.sqlite").exists())

    def test_publication_binding_serialization_is_credential_safe_and_typed(self) -> None:
        binding = PublicationBinding(
            binding_id="binding-a",
            research_topic_id="topic-a",
            topic_workspace_id="workspace-a",
            copy_path="tmp/topic-workspace-publish/topic-a",
            remote_name="origin",
            remote_url="ssh://git@example.test/topic.git",
            visibility=RemoteVisibility.RESTRICTED,
            created_at="2026-07-23T00:00:00Z",
        )
        self.assertEqual("restricted", binding.to_json()["visibility"])
        self.assertNotIn("credentials", binding.to_json())

        exclusive = PublicationBinding(
            binding_id="binding-a",
            research_topic_id="topic-a",
            topic_workspace_id="workspace-a",
            copy_path="tmp/topic-workspace-publish/topic-a",
            remote_name="origin",
            remote_url="ssh://git@example.test/topic.git",
            visibility=RemoteVisibility.RESTRICTED,
            created_at="2026-07-23T00:00:00Z",
            snapshot_mode=PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT,
        )
        restored = PublicationBinding.from_json(exclusive.to_json())
        self.assertEqual(PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT, restored.snapshot_mode)
        self.assertEqual("main", restored.canonical_branch)
        self.assertEqual(exclusive.authority_fingerprint(), restored.authority_fingerprint())

    def test_branch_outcomes_capture_partial_failure_and_safe_resume(self) -> None:
        pushed = BranchOutcome(
            branch="topic-owner/main",
            status=BranchOutcomeStatus.PUSHED,
            pushed_commit="a" * 40,
        )
        failed = BranchOutcome(
            branch="per-agent/coder/main",
            status=BranchOutcomeStatus.FAILED,
            observed_remote_commit="b" * 40,
            replacement_commit="c" * 40,
            diagnostic="remote rejected exact update",
            safe_resume=True,
        )
        self.assertEqual("pushed", pushed.to_json()["status"])
        self.assertTrue(failed.to_json()["safe_resume"])
        self.assertNotIn("topic-workspace/main", pushed.branch)

        snapshot = PublicationSnapshotOutcome(
            binding_id="binding",
            plan_id="plan",
            ref_outcomes=(
                PublicationRefOutcome(
                    ref="refs/heads/main",
                    kind=PublicationRefKind.BRANCH,
                    operation=PublicationRefOperation.UPDATE,
                    status=BranchOutcomeStatus.PUSHED,
                    strategy=PublicationRefUpdateStrategy.FAST_FORWARD,
                    base_commit="c" * 40,
                    observed_lease="c" * 40,
                    resulting_commit="d" * 40,
                    verified=True,
                ),
                PublicationRefOutcome(
                    ref="refs/heads/topic-workspace/main",
                    kind=PublicationRefKind.BRANCH,
                    operation=PublicationRefOperation.DELETE,
                    status=BranchOutcomeStatus.DELETED,
                ),
                PublicationRefOutcome(
                    ref="HEAD",
                    kind=PublicationRefKind.REMOTE_HEAD,
                    operation=PublicationRefOperation.OBSERVE,
                    status=BranchOutcomeStatus.BLOCKED,
                    diagnostic="provider default branch still selects a legacy ref",
                ),
            ),
            resume_at="provider-default-branch",
            observed_remote_head="topic-workspace/main",
            provider_default_branch_action_required=True,
            updated_at="2026-07-27T00:00:00Z",
        )
        payload = snapshot.to_json()
        self.assertEqual(
            "isomer-topic-git-publication-outcomes.v3",
            payload["schema_version"],
        )
        self.assertEqual(
            (),
            validate_support_payload(SupportFileKind.PUBLICATION_OUTCOMES, payload),
        )
        self.assertEqual("provider-default-branch", payload["resume_at"])
        restored = PublicationSnapshotOutcome.from_json(payload)
        self.assertEqual(
            PublicationRefUpdateStrategy.FAST_FORWARD,
            restored.ref_outcomes[0].strategy,
        )
        self.assertTrue(restored.ref_outcomes[0].verified)

    def test_history_aware_plan_schema_and_legacy_approval_staleness(self) -> None:
        digest = "a" * 64
        update = PublicationRefUpdate(
            ref="main",
            strategy=PublicationRefUpdateStrategy.CREATE,
            planned_commit="b" * 40,
            compatibility=PublicationHistoryCompatibility(
                compatible=False,
                evidence=("remote ref is absent",),
            ),
        )
        payload: dict[str, object] = {
            "schema_version": "isomer-topic-git-publication-plan.v2",
            "plan_id": "publication-plan-v2",
            "binding_id": "binding-a",
            "research_topic_id": "topic-a",
            "topic_workspace_id": "workspace-a",
            "copy_path": "tmp/topic-workspace-publish/topic-a",
            "visibility": "private",
            "snapshot_mode": "exclusive_snapshot",
            "canonical_branch": "main",
            "history_disposition": "retain",
            "fingerprints": {"plan": digest},
            "entries": [],
            "components": [],
            "references": [],
            "generated_paths": [],
            "observed_remote_refs": {},
            "expected_remote_refs": {"main": "b" * 40},
            "observed_remote_tags": {},
            "expected_remote_tags": {},
            "observed_remote_head": None,
            "expected_remote_head": "main",
            "ref_updates": [update.to_json()],
            "ref_deletions": [],
            "tag_deletions": [],
            "conflicts": [],
            "push_order": ["main"],
            "blockers": [],
            "approval": {"privacy": True, "remote_mutation": True},
        }
        self.assertEqual(
            (),
            validate_support_payload(SupportFileKind.PUBLICATION_PLAN, payload),
        )
        self.assertFalse(publication_plan_approval_is_stale(payload))
        self.assertTrue(
            publication_plan_approval_is_stale(
                {"schema_version": "isomer-topic-git-publication-plan.v1"}
            )
        )

    def test_stable_projection_manifest_v3_schema_omits_operational_fields(self) -> None:
        payload = {
            "schema_version": "isomer-topic-git-projection-manifest.v3",
            "binding_id": "binding-a",
            "canonical_branch": "main",
            "history_format": "sanitized-linear.v1",
            "entries": [],
            "components": [],
            "selection": {},
            "reference_repositories": [],
            "reproduction_limitations": [],
        }
        self.assertEqual(
            (),
            validate_support_payload(SupportFileKind.PROJECTION_MANIFEST, payload),
        )
        self.assertNotIn("plan_id", payload)
        self.assertNotIn("created_at", payload)

    @staticmethod
    def _binding_payload() -> dict[str, object]:
        return {
            "schema_version": "isomer-topic-git-publication-binding.v1",
            "binding_id": "binding-a",
            "research_topic_id": "topic-a",
            "topic_workspace_id": "workspace-a",
            "copy_path": "tmp/topic-workspace-publish/topic-a",
            "remote_name": "origin",
            "remote_url": "ssh://git@example.test/topic.git",
            "visibility": "private",
            "created_at": "2026-07-23T00:00:00Z",
        }


if __name__ == "__main__":
    unittest.main()
