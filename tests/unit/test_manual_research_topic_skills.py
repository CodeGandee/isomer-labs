from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def read_repo_file(relative_path: str) -> str:
    return (REPO_ROOT / relative_path).read_text(encoding="utf-8")


class ManualResearchTopicSkillContractTests(unittest.TestCase):
    def assertContainsAll(self, text: str, terms: tuple[str, ...]) -> None:
        for term in terms:
            with self.subTest(term=term):
                self.assertIn(term, text)

    def test_topic_creator_documents_operator_owned_topic_and_actor_setup(self) -> None:
        skill = read_repo_file("skillset/operator/isomer-op-topic-creator/SKILL.md")
        help_page = read_repo_file("skillset/operator/isomer-op-topic-creator/references/help.md")
        fast_forward = read_repo_file("skillset/operator/isomer-op-topic-creator/references/fast-forward.md")
        actors = read_repo_file("skillset/operator/isomer-op-topic-creator/references/setup-actors.md")
        finalize = read_repo_file("skillset/operator/isomer-op-topic-creator/references/finalize.md")
        step_by_step = read_repo_file("skillset/operator/isomer-op-topic-creator/references/step-by-step.md")
        run_to = read_repo_file("skillset/operator/isomer-op-topic-creator/references/run-to.md")
        combined = "\n".join((skill, help_page, fast_forward, actors, finalize, step_by_step, run_to))

        self.assertContainsAll(
            combined,
            (
                "isomer-op-topic-creator",
                "prepared Topic Workspace",
                "`ensure-project`",
                "`resolve-topic-input`",
                "`register-topic`",
                "`create-research-intent`",
                "`init-runtime`",
                "`define-topic-env`",
                "`setup-topic-env`",
                "`define-actors`",
                "`setup-actors`",
                "`finalize`",
                "`step-by-step`",
                "`run-to`",
                "`status`",
                "`repair`",
                "default to `run-to define-topic-env`",
                "default bare topic-creation dispatch",
                "Use `fast-forward` only when the user explicitly asks",
                "with the `define-topic-env` target included by default",
                "include the target by default",
                "`before <target>`",
                "`stop before <target>`",
                "`excluding <target>`",
                "`up to but not including <target>`",
                "actor onboarding",
                "topic.workspace.summary",
                "structured reset checkpoint",
                "isomer-cli project topic-reset checkpoint",
                "operator-level readiness evidence",
                "ready/verified/blocked",
                "topic.repos.main` as the Git anchor and integration surface",
                "startup convenience",
            ),
        )
        self.assertNotIn("`bootstrap-research`", combined)
        self.assertNotIn("isomer-deepsci-workspace-mgr", combined)
        self.assertNotIn("placeholder-bindings.md", combined)
        self.assertNotIn("isomer-cli ext research records", combined)
        self.assertNotIn("`start-manual-research`", combined)
        self.assertNotIn("start-pack record refs", combined)
        self.assertNotIn("normal exclusive mode", combined)
        self.assertNotIn("excluded by default", combined)
        self.assertNotIn("explicit inclusive", combined)

    def test_topic_creator_defaults_unspecified_workspace_under_topic_workspace_base(self) -> None:
        resolve_topic_input = read_repo_file("skillset/operator/isomer-op-topic-creator/references/resolve-topic-input.md")
        register_topic = read_repo_file("skillset/operator/isomer-op-topic-creator/references/register-topic.md")
        combined = "\n".join((resolve_topic_input, register_topic))

        self.assertContainsAll(
            combined,
            (
                "`topic_workspace_base_dir`",
                "`isomer-content/topic-ws/<topic-id>`",
                "`isomer-cli project topics create <topic-id> --statement \"<research topic>\"` without `--workspace-dir`",
                "explicitly supplied a custom Topic Workspace directory",
                "`--workspace-dir <topic-workspace-dir>`",
                "DO NOT substitute a bare `<topic-id>` for `<topic-workspace-dir>`",
            ),
        )

    def test_topic_manager_owns_reset_plan_inspect_and_apply_guidance(self) -> None:
        skill = read_repo_file("skillset/operator/isomer-op-topic-mgr/SKILL.md")
        help_page = read_repo_file("skillset/operator/isomer-op-topic-mgr/references/help.md")
        status = read_repo_file("skillset/operator/isomer-op-topic-mgr/references/status.md")
        reset_plan = read_repo_file("skillset/operator/isomer-op-topic-mgr/references/reset-plan.md")
        reset_inspect = read_repo_file("skillset/operator/isomer-op-topic-mgr/references/reset-inspect.md")
        reset_apply = read_repo_file("skillset/operator/isomer-op-topic-mgr/references/reset-apply.md")
        combined = "\n".join((skill, help_page, status, reset_plan, reset_inspect, reset_apply))
        reset_only = "\n".join((reset_plan, reset_inspect, reset_apply))

        self.assertContainsAll(
            combined,
            (
                "Reset Subcommands",
                "`reset-plan`",
                "`reset-inspect`",
                "`reset-apply`",
                "isomer-cli project topic-reset plan",
                "isomer-cli project topic-reset show",
                "isomer-cli project topic-reset show-plan",
                "isomer-cli project topic-reset apply",
                "structured records and Workspace Runtime state",
                "approved structured reset plan",
                "managed payload file path",
            ),
        )
        self.assertNotIn("skillset/research-paradigm", reset_only)
        self.assertNotIn("isomer-deepsci-", reset_only)

    def test_team_specialization_consumes_current_topic_readiness_evidence(self) -> None:
        skill = read_repo_file("skillset/operator/isomer-op-topic-team-specialize/SKILL.md")
        fast_forward = read_repo_file("skillset/operator/isomer-op-topic-team-specialize/references/fast-forward.md")
        validate = read_repo_file("skillset/operator/isomer-op-topic-team-specialize/references/validate-topic-team.md")
        finalize = read_repo_file("skillset/operator/isomer-op-topic-team-specialize/references/finalize-topic-team.md")
        dependency = read_repo_file("skillset/operator/isomer-op-topic-team-specialize/references/step-dependencies.json")
        combined = "\n".join((skill, fast_forward, validate, finalize, dependency))

        self.assertContainsAll(
            combined,
            (
                "isomer-op-topic-creator",
                "Topic Manager topology evidence",
                "current Topic Actor roster",
                "Topic Actor Workspace refs",
                "Preserve active Topic Actor bindings",
                "Do not archive, delete, or convert them into Agent Workspace material",
                "Current Topic Actor roster and Topic Actor Workspace refs preserved in the summary",
                "Topic Actors are not Agent Instances or Agent Team Instance members",
                "isomer-topic-summary.md",
            ),
        )
        self.assertNotIn("isomer-op-topic-prepare", combined)

    def test_team_specialization_routing_requires_explicit_or_contextual_team_intent(self) -> None:
        entrypoint = read_repo_file("skillset/operator/isomer-op-entrypoint/SKILL.md")
        routing = read_repo_file("skillset/operator/isomer-op-entrypoint/references/routing-rules.md")
        welcome = read_repo_file("skillset/operator/isomer-op-welcome/SKILL.md")
        project_manager = read_repo_file("skillset/operator/isomer-op-project-mgr/SKILL.md")
        topic_creator = read_repo_file("skillset/operator/isomer-op-topic-creator/SKILL.md")
        specialization = read_repo_file("skillset/operator/isomer-op-topic-team-specialize/SKILL.md")
        workspace_blockers = read_repo_file(
            "skillset/research-paradigm/deepsci/isomer-deepsci-workspace-mgr/references/validation-and-blockers.md"
        )
        combined = "\n".join(
            (
                entrypoint,
                routing,
                welcome,
                project_manager,
                topic_creator,
                specialization,
                workspace_blockers,
            )
        )

        self.assertContainsAll(
            combined,
            (
                "Establish formal Agent Team intent before specialization",
                "explicitly invokes that skill or a named specialization route",
                "`prepare the topic <topic-name>` with no formal Agent Team target",
                "contextually selected formal Agent Team",
                "Generic topic preparation, launch-facing work, readiness gaps, missing summaries, or missing Agent Workspaces do not establish Agent Team intent",
                "A delegated request must preserve prompt or authoritative context that identifies a formal Agent Team target",
                "When the selected topology includes a formal Agent Team layer",
                "When no formal Agent Team layer is selected",
            ),
        )

    def test_v2_workspace_manager_owns_research_bootstrap_contract(self) -> None:
        skill = read_repo_file("skillset/research-paradigm/deepsci/isomer-deepsci-workspace-mgr/SKILL.md")
        bootstrap = read_repo_file("skillset/research-paradigm/deepsci/isomer-deepsci-workspace-mgr/references/bootstrap-workflow.md")
        access = read_repo_file("skillset/research-paradigm/deepsci/isomer-deepsci-workspace-mgr/references/agent-access-plan.md")
        bindings = read_repo_file("skillset/research-paradigm/deepsci/isomer-deepsci-workspace-mgr/placeholder-bindings.md")
        combined = "\n".join((skill, bootstrap, access, bindings))

        self.assertContainsAll(
            combined,
            (
                "own production DeepSci research workspace bootstrap",
                "selected production DeepSci skill readiness",
                "placeholder binding readiness",
                "Topic Creator summaries",
                "Topic Manager topology evidence",
                "actor metadata for production DeepSci records",
                "accepted research artifact",
                "isomer-cli project topic-reset update-checkpoint",
                "redo-after-reset behavior",
                "--topic-actor <topic-actor-name>",
                "--actor-kind",
                "--runtime-kind",
                "--controller-kind",
            ),
        )
        self.assertNotIn("isomer-op-topic-prepare", combined)


if __name__ == "__main__":
    unittest.main()
