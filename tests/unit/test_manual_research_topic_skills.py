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

    def test_topic_prepare_documents_default_operator_actor_and_opt_out(self) -> None:
        skill = read_repo_file("skillset/operator/isomer-admin-topic-prepare/SKILL.md")
        workflow = read_repo_file("skillset/operator/isomer-admin-topic-prepare/references/topic-preparation-workflow.md")
        actor = read_repo_file("skillset/operator/isomer-admin-topic-prepare/references/operator-topic-actor.md")
        output_template = read_repo_file("skillset/operator/isomer-admin-topic-prepare/references/output-templates.md")
        combined = "\n".join((skill, workflow, actor, output_template))

        self.assertContainsAll(
            combined,
            (
                "default operator Topic Actor Workspace unless explicitly opted out",
                "Unless the user explicitly says not to create it",
                "operator_actor: <ready|opted-out|blocked>",
                "isomer-admin-topic-workspace-mgr",
                "project topic-actors register operator",
                "--actor-kind operator",
                "--runtime-kind human_cli",
                "--role-kind operator",
                "--controller-kind project_operator_session",
                "--materialize",
                "Do not silently recreate the `operator` Topic Actor after an explicit user opt-out",
                "does not create Topic Agent Team Profile material, Agent Team Instance records, Agent Instance records, formal Agent Workspaces, or Houmao launch material",
            ),
        )

    def test_manual_research_skill_documents_mixed_topic_actors_without_formal_team(self) -> None:
        skill = read_repo_file("skillset/operator/isomer-admin-manual-research-session/SKILL.md")
        actor_roster = read_repo_file("skillset/operator/isomer-admin-manual-research-session/references/actor-roster.md")
        bootstrap = read_repo_file("skillset/operator/isomer-admin-manual-research-session/references/research-bootstrap.md")
        start_pack = read_repo_file("skillset/operator/isomer-admin-manual-research-session/references/start-pack-template.md")
        combined = "\n".join((skill, actor_roster, bootstrap, start_pack))

        self.assertContainsAll(
            combined,
            (
                "mixed Codex, Claude Code, shell, or Houmao-backed workers",
                "without requiring a formal Topic Agent Team",
                "<operator|manual_worker|houmao_backed|service_assisted|custom.*>",
                "<human_cli|claude_code|codex|houmao|shell|custom.*>",
                "--topic-actor <topic-actor-name>",
                "--actor-kind <actor-kind>",
                "--runtime-kind <runtime-kind>",
                "--controller-kind <controller-kind>",
                "does not require it",
                "Do not claim formal adoption of Topic Actor-produced work into Agent Instance or Agent Team Instance identity",
                "actor-local copy or pointer",
            ),
        )

    def test_team_specialization_documents_common_preparation_composition_and_actor_preservation(self) -> None:
        skill = read_repo_file("skillset/operator/isomer-admin-topic-team-specialize/SKILL.md")
        fast_forward = read_repo_file("skillset/operator/isomer-admin-topic-team-specialize/references/fast-forward.md")
        validate = read_repo_file("skillset/operator/isomer-admin-topic-team-specialize/references/validate-topic-team.md")
        finalize = read_repo_file("skillset/operator/isomer-admin-topic-team-specialize/references/finalize-topic-team.md")
        dependency = read_repo_file("skillset/operator/isomer-admin-topic-team-specialize/references/step-dependencies.json")
        combined = "\n".join((skill, fast_forward, validate, finalize, dependency))

        self.assertContainsAll(
            combined,
            (
                "isomer-admin-topic-prepare",
                "Prepared-topic evidence",
                "current Topic Actor roster",
                "Topic Actor Workspace refs",
                "Preserve active Topic Actor bindings",
                "Do not archive, delete, or convert them into Agent Workspace material",
                "Current Topic Actor roster and Topic Actor Workspace refs preserved in the summary",
                "Topic Actors are not Agent Instances or Agent Team Instance members",
                "isomer-topic-summary.md",
            ),
        )


if __name__ == "__main__":
    unittest.main()
