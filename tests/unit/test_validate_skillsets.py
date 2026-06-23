from __future__ import annotations

import importlib.util
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_DIR = REPO_ROOT / "scripts"
SCRIPT_PATH = SCRIPT_DIR / "validate_skillsets.py"
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))
SPEC = importlib.util.spec_from_file_location("validate_skillsets", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def codes(diagnostics: list[object]) -> set[str]:
    return {diagnostic.code for diagnostic in diagnostics}


def messages(diagnostics: list[object]) -> list[str]:
    return [diagnostic.render() for diagnostic in diagnostics]


class SkillsetValidatorTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        write(root / "pyproject.toml", "[project]\nname = \"fixture\"\n")
        write(root / "skillset" / "research-paradigm" / "README.md", "# Research Skills\n")
        write(root / "skillset" / "service" / "README.md", "# Service Skills\n")
        return root

    def write_topic_team_specialization_skill(self, root: Path, *, omit_final_report: bool = False) -> None:
        final_report = "" if omit_final_report else "Final Report"
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "SKILL.md",
            f"""
            ---
            name: isomer-admin-topic-team-specialize
            description: Valid fixture skill.
            ---

            # Isomer Admin Topic Team Specialize

            ## Workflow

            1. Select from the subskills.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subskills

            Use `references/project-awareness.md`, `references/template-inspection.md`, `references/topic-context-resolution.md`, `references/service-request-routing.md`, `references/placeholder-reconciliation.md`, `references/topic-profile-drafting.md`, `references/profile-review-approval.md`, `references/profile-materialization.md`, and `references/team-launch-orchestration.md`.

            Use `team-specialization-guide.md`, `team-specialization-plan.md`, `Generated Guide`, `{final_report}`, and `<topic-workspace>/team-profile/execplan/`.
            """,
        )
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-admin-topic-team-specialize"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-admin-topic-team-specialize to validate this fixture."
            """,
        )
        for subskill_name in validator.TOPIC_TEAM_SPECIALIZATION_SUBSKILLS:
            write(
                root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / subskill_name,
                f"""
                # {subskill_name}

                ## Workflow

                1. Run the subskill fixture step.

                If the user's task does not map cleanly to these steps, use your native planning tool.
                """,
            )

    def write_deepsci_mini_guide(self, root: Path, *, omit_contract: bool = False) -> None:
        contract = "" if omit_contract else "contract"
        write(
            root / "teams" / "deepsci-mini" / "execplan" / "team-specialization-guide.md",
            f"""
            # deepsci-mini Team Specialization Guide

            This guide mentions placeholder, assumption, workflow, {contract}, cooperation example, deepsci-mini-lead, deepsci-mini-scout, deepsci-mini-synth-reviewer, and <topic-workspace>/team-profile/execplan/.
            """,
        )

    def test_operator_validator_accepts_topic_team_specialization_contract(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertEqual([], messages(diagnostics))

    def test_operator_validator_requires_module_artifact_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root, omit_final_report=True)
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("Final Report" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_team_subskills(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        (root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "project-awareness.md").unlink()

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("project-awareness.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_topic_team_evals(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "evals" / "evals.json", "{}")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("must not contain evals/" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_incorporated_standalone_skill(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-admin-project-aware" / "SKILL.md",
            """
            ---
            name: isomer-admin-project-aware
            description: Duplicated fixture skill.
            ---

            # Duplicate
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("incorporated into isomer-admin-topic-team-specialize" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_deepsci_mini_guide_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root, omit_contract=True)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS004", codes(diagnostics))
        self.assertTrue(any("contract" in message for message in messages(diagnostics)), messages(diagnostics))
