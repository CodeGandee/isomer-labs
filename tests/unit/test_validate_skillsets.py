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

            1. **Manual mode**: Select one subcommand, load only its detail page, and report the result.
            2. **Automatic mode**: Run `fast-forward`.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            Use `references/resolve-project.md`, `references/inspect-template.md`, `references/resolve-context.md`, `references/map-placeholders.md`, `references/draft-profile.md`, `references/approve-profile.md`, `references/materialize-profile.md`, `references/launch-team.md`, and `references/fast-forward.md`.

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
        for subcommand_name in validator.TOPIC_TEAM_SPECIALIZATION_SUBCOMMANDS:
            write(
                root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / subcommand_name,
                f"""
                # {subcommand_name}

                ## Workflow

                1. Run the subcommand fixture step.

                If the user's task does not map cleanly to these steps, use your native planning tool.
                """,
            )
        for support_reference_name in validator.TOPIC_TEAM_SPECIALIZATION_SUPPORT_REFERENCES:
            write(
                root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / support_reference_name,
                f"""
                # {support_reference_name}

                Local support reference.
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

    def test_operator_validator_requires_topic_team_subcommands(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        (root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "resolve-project.md").unlink()

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("resolve-project.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_route_service_subcommand(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "route-service.md",
            """
            # Route Service

            ## Workflow

            1. Route service work.

            If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("unexpected reference page references/route-service.md" in message for message in messages(diagnostics)), messages(diagnostics))

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
        self.assertTrue(any("must not be a standalone skill" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_external_topic_team_support_refs(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "resolve-project.md",
            """
            # Resolve Project

            ## Workflow

            1. Read `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`.

            If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("must keep required support references inside its skill directory" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_deepsci_mini_guide_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root, omit_contract=True)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS004", codes(diagnostics))
        self.assertTrue(any("contract" in message for message in messages(diagnostics)), messages(diagnostics))
