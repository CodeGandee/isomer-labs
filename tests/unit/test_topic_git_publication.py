from __future__ import annotations

import tempfile
from pathlib import Path
import unittest

from isomer_labs.topic_git import (
    BranchCompatibilityState,
    ComponentBinding,
    ComponentKind,
    ComponentSelection,
    DestructiveBranchReplacement,
    DestructiveChangePlan,
    PrivacyDisposition,
    ProjectionEntry,
    ProjectionEntryOrigin,
    ProjectionManifest,
    PublicationBinding,
    PublicationCopyPreparationAction,
    PublicationHistoryCompatibility,
    PublicationHistoryDisposition,
    PublicationRefUpdate,
    PublicationRefUpdateStrategy,
    PublicationSnapshotMode,
    PublicationSelectionSettings,
    PublicationState,
    ReferenceRepositoryBinding,
    RemoteVisibility,
    TemporaryDirectoryEvidence,
    choose_publication_destination,
    classify_remote_branch,
    component_push_order,
    derive_publication_status,
    evaluate_publication_history_compatibility,
    expected_publication_commit_parents,
    history_withdrawal_replacement_scope,
    legacy_publication_refs,
    normalize_publication_components,
    normalize_github_repository_locator,
    next_publication_resume_ref,
    plan_history_aware_publication,
    plan_publication_copy_preparation,
    plan_snapshot_replacement,
    publication_component_branch,
    publication_delete_push_arguments,
    publication_plan_fingerprint,
    publication_push_arguments,
    redact_remote_locator,
    render_publication_gitmodules,
    remote_head_action_required,
    select_publication_components,
    select_reference_repositories,
    update_publication_copy_exclude,
    update_project_publication_ignore,
    validate_exclusive_snapshot_authority,
    validate_completed_publication,
    validate_force_replacements,
    validate_generated_publication_paths,
    validate_latest_paper_mapping,
    validate_history_aware_publication,
    validate_publication_commit_parents,
    validate_publication_component_topology,
    validate_publication_destination,
    validate_reference_repository,
    validate_remote_locator,
    validate_snapshot_replacement,
    validate_staged_publication_topology,
)


class TopicGitPublicationTests(unittest.TestCase):
    def test_destination_prefers_ignored_tmp_then_temp(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            topic_workspace = project / "isomer-content" / "topic-ws" / "topic-a"
            candidates = (
                TemporaryDirectoryEvidence("tmp", project / "tmp", True, True, "direct ignore evidence"),
                TemporaryDirectoryEvidence("temp", project / "temp", True, True, "direct ignore evidence"),
            )
            plan = choose_publication_destination(
                project_root=project,
                topic_id="topic-a",
                candidates=candidates,
                forbidden_roots=(topic_workspace, project / ".isomer-labs", project / "isomer-content"),
            )
            self.assertEqual(project / "tmp" / "topic-workspace-publish" / "topic-a", plan.path)
            self.assertFalse(plan.update_project_ignore)

            fallback = choose_publication_destination(
                project_root=project,
                topic_id="topic-a",
                candidates=(
                    TemporaryDirectoryEvidence("tmp", project / "tmp", False, False, "unignored"),
                    TemporaryDirectoryEvidence("temp", project / "temp", False, True, "declared rule"),
                ),
                forbidden_roots=(topic_workspace, project / ".isomer-labs", project / "isomer-content"),
            )
            self.assertEqual(project / "temp" / "topic-workspace-publish" / "topic-a", fallback.path)

    def test_missing_candidates_plan_managed_tmp_creation(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            project = Path(temporary)
            plan = choose_publication_destination(
                project_root=project,
                topic_id="topic-a",
                candidates=(),
                forbidden_roots=(project / ".isomer-labs", project / "isomer-content"),
            )
            self.assertTrue(plan.create_directory)
            self.assertTrue(plan.update_project_ignore)

    def test_unsafe_custom_destinations_are_rejected(self) -> None:
        project = Path("/project")
        forbidden = (project / ".isomer-labs", project / "isomer-content", project / "houmao")
        self.assertTrue(
            validate_publication_destination(
                Path("/outside/copy"),
                project_root=project,
                forbidden_roots=forbidden,
            )
        )
        self.assertTrue(
            validate_publication_destination(
                project / "isomer-content" / "copy",
                project_root=project,
                forbidden_roots=forbidden,
            )
        )
        self.assertEqual(
            (),
            validate_publication_destination(
                project / "tmp" / "topic-workspace-publish" / "topic-a",
                project_root=project,
                forbidden_roots=forbidden,
            ),
        )

    def test_project_ignore_block_is_idempotent_and_preserves_negation(self) -> None:
        original = "tmp/*\n!tmp/keep.txt\n"
        first = update_project_publication_ignore(original)
        self.assertEqual(first, update_project_publication_ignore(first))
        self.assertTrue(first.startswith(original))
        self.assertIn("/tmp/topic-workspace-publish/", first)

    def test_remote_validation_and_reporting_reject_credentials_and_signed_urls(self) -> None:
        for safe in (
            "https://example.test/topic.git",
            "ssh://git@example.test/topic.git",
            "git@example.test:owner/topic.git",
            "file:///tmp/topic.git",
            "/tmp/topic.git",
        ):
            with self.subTest(safe=safe):
                self.assertEqual((), validate_remote_locator(safe))
        unsafe = "https://user:password@example.test/topic.git?signature=secret"
        self.assertTrue(validate_remote_locator(unsafe))
        rendered = redact_remote_locator(unsafe)
        self.assertNotIn("password", rendered)
        self.assertNotIn("secret", rendered)

    def test_all_available_components_are_selected_unless_explicitly_excluded(self) -> None:
        components = (
            self._component("main", ComponentKind.TOPIC_MAIN, "topic-owner/main"),
            self._component("actor:reviewer", ComponentKind.TOPIC_ACTOR, "per-topic-actor/reviewer/main"),
            self._component("agent:coder", ComponentKind.AGENT, "per-agent/coder/main"),
            ComponentBinding(
                component_id="agent:future",
                kind=ComponentKind.AGENT,
                name="future",
                relative_path="agents/future",
                branch="per-agent/future/main",
                selection=ComponentSelection.UNAVAILABLE,
                reason="workspace does not exist",
            ),
        )
        selected = select_publication_components(components, explicit_exclusions=("actor:reviewer",))
        by_id = {component.component_id: component for component in selected}
        self.assertEqual(ComponentSelection.SELECTED, by_id["main"].selection)
        self.assertEqual(ComponentSelection.EXCLUDED, by_id["actor:reviewer"].selection)
        self.assertEqual(ComponentSelection.SELECTED, by_id["agent:coder"].selection)
        self.assertEqual(ComponentSelection.UNAVAILABLE, by_id["agent:future"].selection)
        self.assertEqual("components/topic-main", by_id["main"].branch)
        self.assertEqual("main", by_id["agent:coder"].git_anchor_component_id)

    def test_registered_github_references_are_selected_normalized_and_rendered_upstream(self) -> None:
        reference = self._reference("powerinfer", "git@github.com:SJTU-IPADS/PowerInfer.git")
        excluded = self._reference("llama-cpp", "https://github.com/ggerganov/llama.cpp")
        selected = select_reference_repositories((reference, excluded), explicit_exclusions=("llama-cpp",))
        by_id = {item.reference_id: item for item in selected}
        self.assertEqual(ComponentSelection.SELECTED, by_id["powerinfer"].selection)
        self.assertEqual(ComponentSelection.EXCLUDED, by_id["llama-cpp"].selection)
        self.assertEqual(
            "https://github.com/SJTU-IPADS/PowerInfer.git",
            normalize_github_repository_locator(reference.remote_url),
        )
        self.assertEqual((), validate_reference_repository(reference))
        rendered = render_publication_gitmodules(
            publication_remote="https://github.com/CodeGandee/pwinfer-analysis.git",
            components=normalize_publication_components(
                (self._component("main", ComponentKind.TOPIC_MAIN, "topic-owner/main"),)
            ),
            references=(reference,),
        )
        self.assertIn('url = "https://github.com/SJTU-IPADS/PowerInfer.git"', rendered)
        self.assertIn('branch = "components/topic-main"', rendered)
        reference_section = rendered.split('[submodule "reference:powerinfer"]', maxsplit=1)[1].split(
            "[submodule",
            maxsplit=1,
        )[0]
        self.assertNotIn("branch =", reference_section)

        unsafe = self._reference("private", "https://alice:secret@github.com/org/private.git")
        self.assertTrue(validate_reference_repository(unsafe))
        with self.assertRaisesRegex(ValueError, "authentication"):
            normalize_github_repository_locator(unsafe.remote_url)

    def test_new_component_changes_publication_plan_fingerprint(self) -> None:
        binding = PublicationBinding(
            "binding",
            "topic",
            "workspace",
            "tmp/topic-workspace-publish/topic",
            "origin",
            "https://example.test/topic.git",
            RemoteVisibility.PRIVATE,
            "2026-07-23T00:00:00Z",
        )
        main = normalize_publication_components(
            (self._component("main", ComponentKind.TOPIC_MAIN, "topic-owner/main"),)
        )[0]
        first = publication_plan_fingerprint(
            source_fingerprints={"README.md": "a" * 64},
            expected_output_fingerprints={"README.md": "a" * 64},
            copy_fingerprints={},
            binding=binding,
            components=(main,),
            remote_refs={"components/topic-main": None},
        )
        second = publication_plan_fingerprint(
            source_fingerprints={"README.md": "a" * 64},
            expected_output_fingerprints={"README.md": "a" * 64},
            copy_fingerprints={},
            binding=binding,
            components=normalize_publication_components(
                (
                    main,
                    self._component("agent:coder", ComponentKind.AGENT, "per-agent/coder/main"),
                )
            ),
            remote_refs={"components/topic-main": None, "components/agents/coder": None},
        )
        self.assertNotEqual(first, second)

    def test_selection_reference_navigation_and_limitations_change_plan_fingerprint(self) -> None:
        binding = PublicationBinding(
            "binding",
            "topic",
            "workspace",
            "tmp/topic-workspace-publish/topic",
            "origin",
            "https://example.test/topic.git",
            RemoteVisibility.PRIVATE,
            "2026-07-23T00:00:00Z",
        )
        base = {
            "source_fingerprints": {},
            "expected_output_fingerprints": {},
            "copy_fingerprints": {},
            "binding": binding,
            "components": (),
            "remote_refs": {},
        }
        default = publication_plan_fingerprint(**base)
        raw = publication_plan_fingerprint(
            **base,
            selection=PublicationSelectionSettings(include_raw_material_bytes=True),
        )
        reference = publication_plan_fingerprint(
            **base,
            reference_repositories=(self._reference("powerinfer", "https://github.com/SJTU-IPADS/PowerInfer"),),
        )
        generated = publication_plan_fingerprint(
            **base,
            generated_output_fingerprints={"README.md": "a" * 64},
            reproduction_limitations=("Private source requires organization access.",),
        )
        self.assertEqual(4, len({default, raw, reference, generated}))

    def test_remote_branch_compatibility_and_component_first_order(self) -> None:
        absent = classify_remote_branch(
            branch="components/topic-main",
            local_commit="a" * 40,
            remote_commit=None,
            remote_is_ancestor=None,
        )
        compatible = classify_remote_branch(
            branch="components/topic-main",
            local_commit="b" * 40,
            remote_commit="b" * 40,
            remote_is_ancestor=True,
        )
        incompatible = classify_remote_branch(
            branch="components/topic-main",
            local_commit="b" * 40,
            remote_commit="c" * 40,
            remote_is_ancestor=False,
        )
        fast_forward = classify_remote_branch(
            branch="components/topic-main",
            local_commit="d" * 40,
            remote_commit="c" * 40,
            remote_is_ancestor=True,
        )
        unknown = classify_remote_branch(
            branch="components/topic-main",
            local_commit="d" * 40,
            remote_commit="c" * 40,
            remote_is_ancestor=None,
        )
        self.assertEqual(BranchCompatibilityState.ABSENT, absent.state)
        self.assertEqual(BranchCompatibilityState.COMPATIBLE, compatible.state)
        self.assertEqual(BranchCompatibilityState.INCOMPATIBLE, incompatible.state)
        self.assertEqual(BranchCompatibilityState.COMPATIBLE, fast_forward.state)
        self.assertEqual(BranchCompatibilityState.BLOCKED, unknown.state)
        order = component_push_order(
            normalize_publication_components(
                (
                    self._component("main", ComponentKind.TOPIC_MAIN, "topic-owner/main"),
                    self._component("agent:coder", ComponentKind.AGENT, "per-agent/coder/main"),
                )
            )
        )
        self.assertEqual("main", order[-1])

    def test_history_compatibility_requires_binding_manifest_topology_and_ancestry(self) -> None:
        binding = self._exclusive_binding()
        manifest = ProjectionManifest(
            binding_id=binding.binding_id,
            plan_id="legacy-plan",
            created_at="2026-07-27T00:00:00Z",
            entries=(),
            components=(),
        )
        compatible = evaluate_publication_history_compatibility(
            binding=binding,
            manifest=manifest,
            branch="main",
            remote_is_ancestor=True,
            remote_commit_fetched=True,
        )
        self.assertTrue(compatible.compatible)
        purge = evaluate_publication_history_compatibility(
            binding=binding,
            manifest=manifest,
            branch="main",
            remote_is_ancestor=True,
            remote_commit_fetched=True,
            history_disposition=PublicationHistoryDisposition.PURGE,
        )
        self.assertFalse(purge.compatible)
        mismatched = evaluate_publication_history_compatibility(
            binding=binding,
            manifest=ProjectionManifest(
                binding_id="other-binding",
                plan_id="legacy-plan",
                created_at="2026-07-27T00:00:00Z",
                entries=(),
                components=(),
            ),
            branch="main",
            remote_is_ancestor=True,
            remote_commit_fetched=True,
            topology_diagnostics=("component pin is malformed",),
        )
        self.assertFalse(mismatched.compatible)
        self.assertIn("component pin is malformed", str(mismatched.reason))

    def test_history_aware_plan_selects_all_strategies_and_exact_push_forms(self) -> None:
        binding = self._exclusive_binding()
        observed = {
            "components/topic-main": "a" * 40,
            "components/topic-actors/reviewer": "b" * 40,
            "main": "c" * 40,
            "legacy": "9" * 40,
        }
        expected = {
            "components/agents/coder": "d" * 40,
            "components/topic-actors/reviewer": "e" * 40,
            "components/topic-main": "a" * 40,
            "main": "f" * 40,
        }
        compatible = PublicationHistoryCompatibility(
            compatible=True,
            evidence=("matching binding", "verified ancestry"),
        )
        incompatible = PublicationHistoryCompatibility(
            compatible=False,
            evidence=("matching binding",),
            reason="tracked layout is unsupported",
        )
        order = (
            "components/agents/coder",
            "components/topic-actors/reviewer",
            "components/topic-main",
            "main",
        )
        plan = plan_history_aware_publication(
            plan_id="history-aware",
            binding=binding,
            observed_refs=observed,
            expected_refs=expected,
            compatibility_by_ref={
                "components/topic-actors/reviewer": incompatible,
                "components/topic-main": compatible,
                "main": compatible,
            },
            observed_tags={"old": "8" * 40},
            expected_tags={},
            observed_remote_head="main",
            push_order=order,
        )
        strategies = {update.ref: update.strategy for update in plan.ref_updates}
        self.assertEqual(
            {
                "components/agents/coder": PublicationRefUpdateStrategy.CREATE,
                "components/topic-actors/reviewer": PublicationRefUpdateStrategy.FORCE_REPLACEMENT,
                "components/topic-main": PublicationRefUpdateStrategy.NO_OP,
                "main": PublicationRefUpdateStrategy.FAST_FORWARD,
            },
            strategies,
        )
        self.assertEqual(("legacy",), plan.ref_deletions)
        self.assertEqual(("old",), plan.tag_deletions)
        self.assertEqual(
            (),
            validate_history_aware_publication(
                plan,
                binding=binding,
                current_refs=observed,
                current_tags={"old": "8" * 40},
                current_remote_head="main",
                requested_refs=expected,
                requested_tags={},
            ),
        )
        stale = validate_history_aware_publication(
            plan,
            binding=binding,
            current_refs={**observed, "main": "7" * 40},
            current_tags={"old": "8" * 40},
            current_remote_head="main",
            requested_refs=expected,
            requested_tags={},
        )
        self.assertTrue(any("stale" in diagnostic for diagnostic in stale))
        by_ref = {update.ref: update for update in plan.ref_updates}
        self.assertEqual(
            (),
            publication_push_arguments(
                by_ref["components/topic-main"],
                remote_name="publication",
            ),
        )
        normal = publication_push_arguments(by_ref["main"], remote_name="publication")
        self.assertEqual("push", normal[0])
        self.assertFalse(any("force" in argument for argument in normal))
        forced = publication_push_arguments(
            by_ref["components/topic-actors/reviewer"],
            remote_name="publication",
        )
        self.assertIn(
            "--force-with-lease=refs/heads/components/topic-actors/reviewer:"
            + "b" * 40,
            forced,
        )
        self.assertNotIn("--force", forced)
        deletion = publication_delete_push_arguments(
            ref="legacy",
            observed_commit="9" * 40,
            remote_name="publication",
        )
        self.assertIn(
            "--force-with-lease=refs/heads/legacy:" + "9" * 40,
            deletion,
        )
        self.assertEqual(
            ("c" * 40,),
            expected_publication_commit_parents(by_ref["main"]),
        )
        self.assertEqual(
            (),
            validate_publication_commit_parents(
                by_ref["main"],
                actual_parents=("c" * 40,),
            ),
        )
        self.assertEqual(
            (),
            expected_publication_commit_parents(
                by_ref["components/agents/coder"]
            ),
        )

        changed_strategy = PublicationRefUpdate(
            ref="main",
            strategy=PublicationRefUpdateStrategy.FORCE_REPLACEMENT,
            observed_commit="c" * 40,
            planned_commit="f" * 40,
            compatibility=incompatible,
            fallback_reason="manual structural fallback",
        )
        fingerprint_inputs = {
            "source_fingerprints": {},
            "expected_output_fingerprints": {},
            "copy_fingerprints": {},
            "binding": binding,
            "components": (),
            "remote_refs": observed,
        }
        self.assertNotEqual(
            publication_plan_fingerprint(
                **fingerprint_inputs,
                ref_updates=plan.ref_updates,
            ),
            publication_plan_fingerprint(
                **fingerprint_inputs,
                ref_updates=(changed_strategy,),
            ),
        )

    def test_withdrawal_conflict_copy_recovery_resume_and_final_verification(self) -> None:
        binding = self._exclusive_binding()
        compatible = PublicationHistoryCompatibility(True, ("verified ancestry",))
        reviewer = "components/topic-actors/reviewer"
        observed = {reviewer: "a" * 40, "main": "b" * 40}
        expected = {reviewer: "c" * 40, "main": "d" * 40}
        self.assertEqual(
            (reviewer, "main"),
            history_withdrawal_replacement_scope((reviewer,)),
        )
        plan = plan_history_aware_publication(
            plan_id="withdraw",
            binding=binding,
            observed_refs=observed,
            expected_refs=expected,
            compatibility_by_ref={reviewer: compatible, "main": compatible},
            observed_remote_head="main",
            push_order=(reviewer, "main"),
            history_withdrawal_refs=(reviewer,),
            conflicted_refs=(reviewer,),
        )
        self.assertTrue(plan.blockers)
        self.assertTrue(
            all(
                update.strategy is PublicationRefUpdateStrategy.FORCE_REPLACEMENT
                for update in plan.ref_updates
            )
        )
        self.assertTrue(
            validate_history_aware_publication(
                plan,
                binding=binding,
                current_refs=observed,
                current_tags={},
                current_remote_head="main",
                requested_refs=expected,
                requested_tags={},
            )
        )

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            missing = plan_publication_copy_preparation(
                copy_path=root / "copy",
                recovery_path=root / "recovery",
                copy_exists=False,
                copy_clean=False,
                binding_matches=True,
                current_head=None,
                expected_base="b" * 40,
                remote_recovery_available=True,
            )
            self.assertEqual(PublicationCopyPreparationAction.RECOVER, missing.action)
            dirty = plan_publication_copy_preparation(
                copy_path=root / "copy",
                recovery_path=root / "recovery",
                copy_exists=True,
                copy_clean=False,
                binding_matches=True,
                current_head="b" * 40,
                expected_base="b" * 40,
                remote_recovery_available=True,
            )
            self.assertEqual(PublicationCopyPreparationAction.RECOVER, dirty.action)
            self.assertTrue(dirty.preserves_existing_copy)

        unblocked = plan_history_aware_publication(
            plan_id="publish",
            binding=binding,
            observed_refs=observed,
            expected_refs=expected,
            compatibility_by_ref={reviewer: compatible, "main": compatible},
            observed_remote_head="main",
            push_order=(reviewer, "main"),
        )
        self.assertEqual(
            reviewer,
            next_publication_resume_ref(unblocked, current_refs=observed),
        )
        self.assertEqual(
            "main",
            next_publication_resume_ref(
                unblocked,
                current_refs={reviewer: "c" * 40, "main": "b" * 40},
            ),
        )
        self.assertEqual(
            (),
            validate_completed_publication(
                unblocked,
                actual_refs=expected,
                actual_tags={},
                actual_parents={
                    reviewer: ("a" * 40,),
                    "main": ("b" * 40,),
                },
                publication_copies_clean=True,
                recursive_clone_succeeded=True,
            ),
        )

    def test_force_replacement_requires_exact_fresh_branch_scoped_approval(self) -> None:
        replacement = DestructiveBranchReplacement(
            branch="topic-owner/main",
            observed_remote_commit="a" * 40,
            replacement_commit="b" * 40,
            displaced_commits=("a" * 40,),
            warning="Replacing this branch may make displaced commits unreachable.",
        )
        plan = DestructiveChangePlan(
            plan_id="force-plan",
            binding_id="binding",
            replacements=(replacement,),
            push_order=("topic-owner/main", "topic-workspace/main"),
            approved_branches=("topic-owner/main",),
        )
        self.assertEqual(
            (),
            validate_force_replacements(
                plan,
                fetched_remote_refs={"topic-owner/main": "a" * 40},
                requested_replacements={"topic-owner/main": "b" * 40},
            ),
        )
        stale = validate_force_replacements(
            plan,
            fetched_remote_refs={"topic-owner/main": "c" * 40},
            requested_replacements={"topic-owner/main": "b" * 40},
        )
        self.assertTrue(any("stale" in diagnostic for diagnostic in stale))
        unlisted = validate_force_replacements(
            plan,
            fetched_remote_refs={"topic-owner/main": "a" * 40, "per-agent/coder/main": "d" * 40},
            requested_replacements={"per-agent/coder/main": "e" * 40},
        )
        self.assertTrue(any("not listed" in diagnostic for diagnostic in unlisted))

    def test_publication_status_does_not_depend_on_local_tracking(self) -> None:
        self.assertEqual(
            PublicationState.DISABLED,
            derive_publication_status(
                binding_exists=False,
                copy_exists=False,
                synchronized=False,
                stale=False,
                blockers=(),
            ),
        )
        self.assertEqual(
            PublicationState.COPY_MISSING,
            derive_publication_status(
                binding_exists=True,
                copy_exists=False,
                synchronized=True,
                stale=False,
                blockers=(),
            ),
        )
        self.assertEqual(
            PublicationState.SYNCHRONIZED,
            derive_publication_status(
                binding_exists=True,
                copy_exists=True,
                synchronized=True,
                stale=False,
                blockers=(),
            ),
        )
        self.assertEqual(
            PublicationState.BLOCKED,
            derive_publication_status(
                binding_exists=True,
                copy_exists=True,
                synchronized=False,
                stale=False,
                blockers=("visibility is unknown",),
            ),
        )

    def test_component_branches_and_topic_main_anchors_are_deterministic(self) -> None:
        components = normalize_publication_components(
            (
                self._component("main", ComponentKind.TOPIC_MAIN, "source/main"),
                self._component("actor:operator", ComponentKind.TOPIC_ACTOR, "source/actor"),
                self._component("agent:coder", ComponentKind.AGENT, "source/agent"),
            )
        )
        by_id = {component.component_id: component for component in components}
        self.assertEqual("components/topic-main", by_id["main"].branch)
        self.assertEqual("components/topic-actors/operator", by_id["actor:operator"].branch)
        self.assertEqual("components/agents/coder", by_id["agent:coder"].branch)
        self.assertEqual("main", by_id["actor:operator"].git_anchor_component_id)
        self.assertEqual("main", by_id["agent:coder"].git_anchor_component_id)
        self.assertEqual((), validate_publication_component_topology(components))
        self.assertEqual(
            "components/topic-actors/operator",
            publication_component_branch(ComponentKind.TOPIC_ACTOR, "operator"),
        )

    def test_exclusive_snapshot_authority_binds_remote_topic_workspace_and_mode(self) -> None:
        binding = self._exclusive_binding()
        self.assertEqual(
            (),
            validate_exclusive_snapshot_authority(
                binding,
                remote_url=binding.remote_url,
                research_topic_id=binding.research_topic_id,
                topic_workspace_id=binding.topic_workspace_id,
            ),
        )
        changed = validate_exclusive_snapshot_authority(
            binding,
            remote_url="https://example.test/other.git",
            research_topic_id=binding.research_topic_id,
            topic_workspace_id=binding.topic_workspace_id,
        )
        self.assertTrue(any("remote identity changed" in diagnostic for diagnostic in changed))
        self.assertNotIn("password", binding.to_json())
        self.assertEqual(64, len(str(binding.to_json()["authority_fingerprint"])))

    def test_snapshot_plan_replaces_complete_refs_and_tags_and_detects_staleness(self) -> None:
        binding = self._exclusive_binding()
        observed_refs = {
            "main": "a" * 40,
            "topic-workspace/main": "b" * 40,
            "manual": "c" * 40,
        }
        expected_refs = {
            "components/topic-main": "d" * 40,
            "components/agents/coder": "e" * 40,
            "main": "f" * 40,
        }
        plan = plan_snapshot_replacement(
            plan_id="snapshot",
            binding=binding,
            observed_refs=observed_refs,
            expected_refs=expected_refs,
            observed_tags={"old": "1" * 40},
            expected_tags={},
            observed_remote_head="topic-workspace/main",
            push_order=("components/agents/coder", "components/topic-main", "main"),
        )
        self.assertEqual(("manual", "topic-workspace/main"), plan.ref_deletions)
        self.assertEqual(("old",), plan.tag_deletions)
        self.assertTrue(remote_head_action_required(plan.observed_remote_head))
        self.assertTrue(plan.provider_default_branch_action_required)
        self.assertEqual("topic-workspace/main", plan.remote_head_ref_deletion)
        self.assertEqual(
            "topic-workspace/main",
            plan.to_json()["remote_head_ref_deletion"],
        )
        self.assertEqual(
            (),
            validate_snapshot_replacement(
                plan,
                binding=binding,
                current_refs=observed_refs,
                current_tags={"old": "1" * 40},
                current_remote_head="topic-workspace/main",
                requested_refs=expected_refs,
                requested_tags={},
            ),
        )
        stale = validate_snapshot_replacement(
            plan,
            binding=binding,
            current_refs={**observed_refs, "manual": "9" * 40},
            current_tags={"old": "1" * 40},
            current_remote_head="main",
            requested_refs=expected_refs,
            requested_tags={},
        )
        self.assertTrue(any("stale" in diagnostic for diagnostic in stale))
        self.assertTrue(any("remote HEAD changed" in diagnostic for diagnostic in stale))
        self.assertEqual(
            ("manual", "topic-workspace/main"),
            legacy_publication_refs(observed_refs, expected_refs=expected_refs),
        )

    def test_generated_paths_latest_paper_and_copy_exclude_are_validated(self) -> None:
        self.assertEqual(
            (),
            validate_generated_publication_paths(
                source_paths=("pixi.toml", "README.md"),
                generated_paths=(
                    "README.md",
                    ".gitmodules",
                    ".isomer-publication/research-record-index.json",
                ),
            ),
        )
        self.assertTrue(
            validate_generated_publication_paths(
                source_paths=(".isomer-publication/private.json",),
                generated_paths=(".isomer-publication/research-record-index.json",),
            )
        )
        approved_paper = "records/artifacts/paper/pwinfer-analysis.pdf"
        self.assertEqual(
            (),
            validate_latest_paper_mapping(
                approved_paper,
                approved_artifact_paths=(approved_paper,),
            ),
        )
        self.assertTrue(
            validate_latest_paper_mapping(
                "paper/latest.pdf",
                approved_artifact_paths=(approved_paper,),
            )
        )
        self.assertEqual("/cache/\n/.isomer/\n", update_publication_copy_exclude("/cache/\n"))

    def test_complete_staged_topology_requires_exact_gitlinks_and_no_flattening(self) -> None:
        components = normalize_publication_components(
            (
                self._component("main", ComponentKind.TOPIC_MAIN, "source/main"),
                self._component("agent:coder", ComponentKind.AGENT, "source/agent"),
            )
        )
        entries = (
            ProjectionEntry(
                "pixi.toml",
                "pixi.toml",
                PrivacyDisposition.TRACK,
                "a" * 64,
            ),
            ProjectionEntry(
                None,
                ".isomer-publication/topic-workspace-projection.json",
                PrivacyDisposition.TRACK,
                None,
                origin=ProjectionEntryOrigin.GENERATED,
            ),
        )
        actual = {
            "pixi.toml": "100644",
            ".isomer-publication/topic-workspace-projection.json": "100644",
            "repos/topic-main": "160000",
            "agents/coder": "160000",
        }
        self.assertEqual(
            (),
            validate_staged_publication_topology(
                actual,
                entries=entries,
                components=components,
                generated_paths=(".isomer-publication/topic-workspace-projection.json",),
            ),
        )
        flattened = dict(actual)
        flattened["agents/coder/source.py"] = "100644"
        self.assertTrue(
            any(
                "flattened" in diagnostic
                for diagnostic in validate_staged_publication_topology(
                    flattened,
                    entries=entries,
                    components=components,
                    generated_paths=(".isomer-publication/topic-workspace-projection.json",),
                )
            )
        )
    @staticmethod
    def _component(component_id: str, kind: ComponentKind, branch: str) -> ComponentBinding:
        name = component_id.rsplit(":", 1)[-1]
        if kind is ComponentKind.TOPIC_MAIN:
            relative_path = "repos/topic-main"
        elif kind is ComponentKind.TOPIC_ACTOR:
            relative_path = f"actors/{name}"
        else:
            relative_path = f"agents/{name}"
        return ComponentBinding(
            component_id=component_id,
            kind=kind,
            name=name,
            relative_path=relative_path,
            branch=branch,
            selection=ComponentSelection.SELECTED,
        )

    @staticmethod
    def _reference(reference_id: str, remote_url: str) -> ReferenceRepositoryBinding:
        return ReferenceRepositoryBinding(
            reference_id=reference_id,
            semantic_label=f"topic.repos.sources.{reference_id}",
            relative_path=f"repos/extern/sources/{reference_id}",
            remote_url=remote_url,
            commit_sha="a" * 40,
            visibility=RemoteVisibility.PUBLIC,
            license_status="Apache-2.0",
        )

    @staticmethod
    def _exclusive_binding() -> PublicationBinding:
        return PublicationBinding(
            binding_id="binding",
            research_topic_id="topic",
            topic_workspace_id="workspace",
            copy_path="tmp/topic-workspace-publish/topic",
            remote_name="origin",
            remote_url="https://example.test/topic.git",
            visibility=RemoteVisibility.PRIVATE,
            created_at="2026-07-27T00:00:00Z",
            snapshot_mode=PublicationSnapshotMode.EXCLUSIVE_SNAPSHOT,
        )


if __name__ == "__main__":
    unittest.main()
