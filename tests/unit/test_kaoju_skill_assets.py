from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
KAOJU_ROOT = REPO_ROOT / "src" / "isomer_labs" / "assets" / "system_skills" / "research-paradigm" / "kaoju"

CONTRACT = json.loads((KAOJU_ROOT / "contracts/survey-process.v2.json").read_text(encoding="utf-8"))
EXPECTED_SKILLS = set(CONTRACT["skills"])
COMMANDS = set(CONTRACT["survey_intents"]) | set(CONTRACT["compatibility_procedures"]) | set(CONTRACT["manager_actions"])


class KaojuSkillAssetTests(unittest.TestCase):
    def test_exact_skill_inventory_and_identity_contract(self) -> None:
        actual = {path.name for path in KAOJU_ROOT.glob("isomer-kaoju-*") if path.is_dir()}
        self.assertEqual(EXPECTED_SKILLS, actual)
        for name in sorted(actual):
            skill = KAOJU_ROOT / name
            skill_text = (skill / "SKILL.md").read_text(encoding="utf-8")
            agent_text = (skill / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertRegex(skill_text, rf"(?m)^name: {re.escape(name)}$")
            self.assertRegex(skill_text, r"(?m)^description: Use when")
            self.assertIn("## Workflow", "\n".join(skill_text.splitlines()[:40]), name)
            self.assertIn("## When to Use", skill_text, name)
            self.assertIn("## Common Mistakes", skill_text, name)
            self.assertIn(f'display_name: "{name}"', agent_text)
            self.assertIn(f"${name}", agent_text)

    def test_pipeline_uses_checked_intent_compatibility_and_manager_groups(self) -> None:
        pipeline = KAOJU_ROOT / "isomer-kaoju-pipeline"
        text = (pipeline / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Survey Intents", text)
        self.assertIn("## Compatibility Procedures", text)
        self.assertIn("## Grouped Managers", text)
        command_names = {path.stem for path in (pipeline / "commands").glob("*.md")}
        self.assertEqual(COMMANDS, command_names)
        for name in sorted(command_names):
            page = (pipeline / "commands" / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn("## Workflow", "\n".join(page.splitlines()[:20]), name)
            self.assertTrue("does not map cleanly" in page or "Gates, Blockers, and Resume" in page, name)
            self.assertIn(f"`{name}`", text)
            self.assertIn(f"commands/{name}.md", text)
        self.assertIn("`help`", text)

    def test_manager_actions_are_grouped(self) -> None:
        commands = KAOJU_ROOT / "isomer-kaoju-pipeline" / "commands"
        survey = (commands / "manage-survey.md").read_text(encoding="utf-8")
        dataset = (commands / "manage-dataset.md").read_text(encoding="utf-8")
        for action in ("list", "show", "status", "export"):
            self.assertIn(f"`{action}`", survey)
        for action in ("register", "list", "show", "refresh", "remove"):
            self.assertIn(f"`{action}`", dataset)
        self.assertIn("Topic Workspace owner", dataset)
        self.assertIn("never alter or delete the external target", dataset)

    def test_shared_contract_references_are_complete_and_linked(self) -> None:
        shared = KAOJU_ROOT / "isomer-kaoju-shared"
        expected = {
            "artifact-recording.md",
            "artifact-semantics.md",
            "evidence-contract.md",
            "external-owner-routing.md",
            "interaction-and-gates.md",
            "lineage.md",
            "source-identity.md",
            "survey-artifacts.md",
            "terminal-report.md",
        }
        actual = {path.name for path in (shared / "references").glob("*.md")}
        self.assertEqual(expected, actual)
        skill_text = (shared / "SKILL.md").read_text(encoding="utf-8")
        for name in sorted(expected):
            self.assertIn(f"references/{name}", skill_text)

    def test_generic_maintenance_procedures_are_absent(self) -> None:
        pipeline = KAOJU_ROOT / "isomer-kaoju-pipeline"
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


if __name__ == "__main__":
    unittest.main()
