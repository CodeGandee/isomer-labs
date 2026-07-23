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
    PublicationBinding,
    PublicationState,
    RemoteVisibility,
    TemporaryDirectoryEvidence,
    choose_publication_destination,
    classify_remote_branch,
    component_push_order,
    derive_publication_status,
    publication_plan_fingerprint,
    redact_remote_locator,
    select_publication_components,
    update_project_publication_ignore,
    validate_force_replacements,
    validate_publication_destination,
    validate_remote_locator,
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
        main = self._component("main", ComponentKind.TOPIC_MAIN, "topic-owner/main")
        first = publication_plan_fingerprint(
            source_fingerprints={"README.md": "a" * 64},
            expected_output_fingerprints={"README.md": "a" * 64},
            copy_fingerprints={},
            binding=binding,
            components=(main,),
            remote_refs={"topic-owner/main": None},
        )
        second = publication_plan_fingerprint(
            source_fingerprints={"README.md": "a" * 64},
            expected_output_fingerprints={"README.md": "a" * 64},
            copy_fingerprints={},
            binding=binding,
            components=(main, self._component("agent:coder", ComponentKind.AGENT, "per-agent/coder/main")),
            remote_refs={"topic-owner/main": None, "per-agent/coder/main": None},
        )
        self.assertNotEqual(first, second)

    def test_remote_branch_compatibility_and_component_first_order(self) -> None:
        absent = classify_remote_branch(
            branch="topic-owner/main",
            local_commit="a" * 40,
            remote_commit=None,
            remote_is_ancestor=None,
        )
        compatible = classify_remote_branch(
            branch="topic-owner/main",
            local_commit="b" * 40,
            remote_commit="a" * 40,
            remote_is_ancestor=True,
        )
        incompatible = classify_remote_branch(
            branch="topic-owner/main",
            local_commit="b" * 40,
            remote_commit="c" * 40,
            remote_is_ancestor=False,
        )
        self.assertEqual(BranchCompatibilityState.ABSENT, absent.state)
        self.assertEqual(BranchCompatibilityState.COMPATIBLE, compatible.state)
        self.assertEqual(BranchCompatibilityState.INCOMPATIBLE, incompatible.state)
        order = component_push_order(
            (
                self._component("main", ComponentKind.TOPIC_MAIN, "topic-owner/main"),
                self._component("agent:coder", ComponentKind.AGENT, "per-agent/coder/main"),
            )
        )
        self.assertEqual("topic-workspace/main", order[-1])

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

    @staticmethod
    def _component(component_id: str, kind: ComponentKind, branch: str) -> ComponentBinding:
        name = component_id.rsplit(":", 1)[-1]
        relative_path = "repos/topic-main" if kind is ComponentKind.TOPIC_MAIN else f"{kind.value}s/{name}"
        return ComponentBinding(
            component_id=component_id,
            kind=kind,
            name=name,
            relative_path=relative_path,
            branch=branch,
            selection=ComponentSelection.SELECTED,
        )


if __name__ == "__main__":
    unittest.main()
