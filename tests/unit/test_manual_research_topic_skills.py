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
        skill = read_repo_file("skillset/operator/isomer-admin-topic-creator/SKILL.md")
        help_page = read_repo_file("skillset/operator/isomer-admin-topic-creator/references/help.md")
        fast_forward = read_repo_file("skillset/operator/isomer-admin-topic-creator/references/fast-forward.md")
        actors = read_repo_file("skillset/operator/isomer-admin-topic-creator/references/setup-actors.md")
        finalize = read_repo_file("skillset/operator/isomer-admin-topic-creator/references/finalize.md")
        step_by_step = read_repo_file("skillset/operator/isomer-admin-topic-creator/references/step-by-step.md")
        run_to = read_repo_file("skillset/operator/isomer-admin-topic-creator/references/run-to.md")
        combined = "\n".join((skill, help_page, fast_forward, actors, finalize, step_by_step, run_to))

        self.assertContainsAll(
            combined,
            (
                "isomer-admin-topic-creator",
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
                "actor onboarding",
                "topic.workspace.summary",
                "ready/verified/blocked",
                "topic.repos.main` as the Git anchor and integration surface",
                "startup convenience",
            ),
        )
        self.assertNotIn("`bootstrap-research`", combined)
        self.assertNotIn("isomer-rsch-workspace-mgr-v2", combined)
        self.assertNotIn("placeholder-bindings.md", combined)
        self.assertNotIn("isomer-cli ext research records", combined)
        self.assertNotIn("`start-manual-research`", combined)
        self.assertNotIn("start-pack record refs", combined)

    def test_team_specialization_consumes_current_topic_readiness_evidence(self) -> None:
        skill = read_repo_file("skillset/operator/isomer-admin-topic-team-specialize/SKILL.md")
        fast_forward = read_repo_file("skillset/operator/isomer-admin-topic-team-specialize/references/fast-forward.md")
        validate = read_repo_file("skillset/operator/isomer-admin-topic-team-specialize/references/validate-topic-team.md")
        finalize = read_repo_file("skillset/operator/isomer-admin-topic-team-specialize/references/finalize-topic-team.md")
        dependency = read_repo_file("skillset/operator/isomer-admin-topic-team-specialize/references/step-dependencies.json")
        combined = "\n".join((skill, fast_forward, validate, finalize, dependency))

        self.assertContainsAll(
            combined,
            (
                "isomer-admin-topic-creator",
                "Topic Workspace Manager topology evidence",
                "current Topic Actor roster",
                "Topic Actor Workspace refs",
                "Preserve active Topic Actor bindings",
                "Do not archive, delete, or convert them into Agent Workspace material",
                "Current Topic Actor roster and Topic Actor Workspace refs preserved in the summary",
                "Topic Actors are not Agent Instances or Agent Team Instance members",
                "isomer-topic-summary.md",
            ),
        )
        self.assertNotIn("isomer-admin-topic-prepare", combined)

    def test_v2_workspace_manager_owns_research_bootstrap_contract(self) -> None:
        skill = read_repo_file("skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2/SKILL.md")
        bootstrap = read_repo_file("skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2/references/bootstrap-workflow.md")
        access = read_repo_file("skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2/references/agent-access-plan.md")
        bindings = read_repo_file("skillset/research-paradigm/v2/isomer-rsch-workspace-mgr-v2/placeholder-bindings.md")
        combined = "\n".join((skill, bootstrap, access, bindings))

        self.assertContainsAll(
            combined,
            (
                "own v2 research workspace bootstrap",
                "selected v2 skill readiness",
                "placeholder binding readiness",
                "Topic Creator summaries",
                "Topic Workspace Manager topology evidence",
                "actor metadata for v2 records",
                "accepted research artifact",
                "--topic-actor <topic-actor-name>",
                "--actor-kind",
                "--runtime-kind",
                "--controller-kind",
            ),
        )
        self.assertNotIn("isomer-admin-topic-prepare", combined)


if __name__ == "__main__":
    unittest.main()
