from __future__ import annotations

import re
import unittest
from pathlib import Path

from isomer_labs.kaoju.contracts import load_contract


REPO_ROOT = Path(__file__).resolve().parents[2]
KAOJU_ROOT = REPO_ROOT / "src" / "isomer_labs" / "assets" / "system_skills" / "research-paradigm" / "kaoju"
ENTRYPOINT = KAOJU_ROOT / "isomer-ext-kaoju-entrypoint"
SUBSKILLS = ENTRYPOINT / "subskills"


CONTRACT = load_contract()
EXPECTED_SKILLS = set(CONTRACT.skills)
COMMANDS = (
    set(CONTRACT.survey_intents)
    | set(CONTRACT.compatibility_procedures)
    | set(CONTRACT.exploration_procedures)
    | set(CONTRACT.manager_actions)
)


def skill_entrypoint(skill: Path) -> Path:
    return skill / ("SKILL.md" if skill == ENTRYPOINT else "SKILL-MAIN.md")


class KaojuSkillAssetTests(unittest.TestCase):
    def test_exact_skill_inventory_and_identity_contract(self) -> None:
        actual = {ENTRYPOINT.name, *(path.name for path in SUBSKILLS.glob("isomer-kaoju-*") if path.is_dir())}
        self.assertEqual(EXPECTED_SKILLS, actual)
        for name in sorted(actual):
            skill = ENTRYPOINT if name == ENTRYPOINT.name else SUBSKILLS / name
            skill_text = skill_entrypoint(skill).read_text(encoding="utf-8")
            agent_text = (skill / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertRegex(skill_text, rf"(?m)^name: {re.escape(name)}$")
            self.assertRegex(skill_text, r"(?m)^description: Use when")
            self.assertIn("## Workflow", "\n".join(skill_text.splitlines()[:40]), name)
            self.assertIn("## When to Use", skill_text, name)
            self.assertIn("## Guardrails", skill_text, name)
            self.assertIn(f'display_name: "{name}"', agent_text)
            self.assertIn(f"${ENTRYPOINT.name}", agent_text)

    def test_pipeline_uses_checked_intent_compatibility_and_manager_groups(self) -> None:
        pipeline = ENTRYPOINT
        text = (pipeline / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Survey Intents", text)
        self.assertIn("## Compatibility Procedures", text)
        self.assertIn("## Exploration Procedures", text)
        self.assertIn("## Grouped Managers", text)
        command_names = {path.stem for path in (pipeline / "commands").glob("*.md")}
        self.assertEqual(COMMANDS, command_names)
        for name in sorted(command_names):
            page = (pipeline / "commands" / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("## Workflow", page, name)
            self.assertTrue("does not map cleanly" in page or "Gates, Blockers, and Resume" in page, name)
            self.assertIn(f"`{name}`", text)
            self.assertIn(f"commands/{name}.md", text)
        self.assertIn("`help`", text)

    def test_manager_actions_are_grouped(self) -> None:
        commands = ENTRYPOINT / "commands"
        survey = (commands / "manage-survey.md").read_text(encoding="utf-8")
        dataset = (commands / "manage-dataset.md").read_text(encoding="utf-8")
        for action in ("list", "show", "status", "export"):
            self.assertIn(f"`{action}`", survey)
        for action in ("register", "list", "show", "refresh", "remove"):
            self.assertIn(f"`{action}`", dataset)
        self.assertIn("Topic Workspace owner", dataset)
        self.assertIn("never alter or delete the external target", dataset)

        paper = (commands / "manage-paper-template.md").read_text(encoding="utf-8")
        for action in ("list", "show", "create", "copy", "update", "replace", "merge", "file put", "file remove", "metadata patch", "export", "observe", "archive", "delete"):
            self.assertIn(f"`{action}`", paper)
        self.assertIn("content", paper)
        self.assertIn("LaTeX", paper)
        self.assertIn("paper-line TeX snapshots", paper)
        roles = CONTRACT.raw["template_roles"]
        self.assertEqual("KAOJU:PAPER-TEMPLATE-MYST", roles["content"]["semantic_id"])
        self.assertEqual("KAOJU:PAPER-TEMPLATE-LATEX", roles["latex"]["semantic_id"])
        self.assertEqual("main", roles["content"]["default_name"])
        self.assertEqual("main", roles["latex"]["default_name"])

    def test_paper_template_unnamed_update_discovery_order_is_explicit(self) -> None:
        commands = ENTRYPOINT / "commands"
        manager = (commands / "manage-paper-template.md").read_text(encoding="utf-8")
        role = manager.index("template role before source discovery")
        explicit = manager.index("Resolve an explicit role-local name")
        exports = manager.index("template exports --kind KIND")
        one_edited = manager.index("exactly one eligible export")
        ambiguous = manager.index("If several selected-role exports")
        topic_main = manager.index("inspect `<root>/<kind>/main/`")
        clarification = manager.index("If no selected-role source exists")
        self.assertEqual(sorted((role, explicit, exports, one_edited, ambiguous, topic_main, clarification)), [role, explicit, exports, one_edited, ambiguous, topic_main, clarification])
        self.assertIn("even when the database has no selected-role `main`", manager)
        self.assertIn("other role's database records", manager)

        writer = skill_entrypoint(SUBSKILLS / "isomer-kaoju-write").read_text(encoding="utf-8")
        self.assertIn("Resolve role before using", writer)
        self.assertIn("use exactly one eligible edited export of that role", writer)
        self.assertIn("<topic.paper.template_exchange_root>/<kind>/main/", writer)
        self.assertIn("Same-named records or exports of the other role are ineligible", writer)
        self.assertIn("paper-specific TeX draft", writer)

    def test_shared_contract_references_are_complete_and_linked(self) -> None:
        shared = SUBSKILLS / "isomer-kaoju-shared"
        expected = {
            "artifact-recording.md",
            "artifact-semantics.md",
            "evidence-contract.md",
            "external-owner-routing.md",
            "interaction-and-gates.md",
            "lineage.md",
            "mindset-contract.md",
            "prerequisite-recovery.md",
            "research-idea-recording.md",
            "source-identity.md",
            "survey-artifacts.md",
            "terminal-report.md",
        }
        actual = {path.name for path in (shared / "references").glob("*.md")}
        self.assertEqual(expected, actual)
        skill_text = skill_entrypoint(shared).read_text(encoding="utf-8")
        for name in sorted(expected):
            self.assertIn(f"references/{name}", skill_text)

    def test_generic_maintenance_procedures_are_absent(self) -> None:
        pipeline = ENTRYPOINT
        command_names = {path.stem for path in (pipeline / "commands").glob("*.md")}
        forbidden = {
            "environment-repair",
            "full-kaoju",
            "list-passes",
            "refresh",
            "repository-refresh",
            "reproduction",
            "resume",
            "source-audit",
        }
        self.assertFalse(command_names & forbidden)
        text = (pipeline / "SKILL.md").read_text(encoding="utf-8")
        for name in forbidden:
            self.assertNotRegex(text, rf"(?m)^\| `{re.escape(name)}` \|")

    def test_mindsets_add_topic_creation_without_a_manager_or_specialized_cli(self) -> None:
        text = (ENTRYPOINT / "SKILL.md").read_text(encoding="utf-8")
        commands = {path.stem for path in (ENTRYPOINT / "commands").glob("*.md")}
        subskills = {path.name for path in SUBSKILLS.glob("isomer-kaoju-*") if path.is_dir()}
        self.assertIn("create-topic", commands)
        self.assertIn("isomer-kaoju-topic-creator", subskills)
        self.assertNotIn("manage-mindset", commands)
        self.assertNotIn("isomer-kaoju-mindsets", subskills)
        self.assertNotIn("ext kaoju mindsets", text)
        for forbidden in ("KAOJU:MINDSET-SOURCE", "manage-mindset", "isomer-cli ext kaoju mindsets"):
            self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
