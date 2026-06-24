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

    def write_topic_team_specialization_skill(
        self,
        root: Path,
        *,
        omit_final_report: bool = False,
        omit_fallback: bool = False,
        omit_skill_term: str | None = None,
        omit_prerequisite_subcommand: str | None = None,
    ) -> None:
        final_report = "" if omit_final_report else "Final Report"
        fallback = "" if omit_fallback else "If the user's task does not map cleanly to these steps, use your native planning tool."
        subcommand_links = ", ".join(
            f"`references/{subcommand_name}`" for subcommand_name in validator.TOPIC_TEAM_SPECIALIZATION_SUBCOMMANDS
        )
        skill_text = f"""
            ---
            name: isomer-admin-topic-team-specialize
            description: Valid fixture skill.
            ---

            # Isomer Admin Topic Team Specialize

            ## Workflow

            1. **Default help mode**: If invoked without a prompt, run `help`.
            2. **Manual mode**: Select one subcommand, load only its detail page, and report the result.
            3. **Guided mode**: Run `step-by-step`.
            4. **Automatic mode**: Run `fast-forward`.

            {fallback}

            ## Subcommands

            Procedural Subcommands: `init-topic`, `clarify-topic`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, and `materialize-profile`.

            Helper Subcommands: five lower-level implementation commands: `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile`.

            Misc Subcommands: `help`, `fast-forward`, and `step-by-step`.

            Use {subcommand_links}.

            Use static material readiness, durable setup state, `topic-overview.md`, provisional topic workspace seed, `isomer-content/topic-ws/<topic-slug>/`, `team-specialization-guide.md`, `team-specialization-plan.md`, `{final_report}`, `<topic-workspace>/team-profile/execplan/`, and `isomer-topic-summary.md`.

            Report `selected_domain_team_template_ref`, `topic_environment_status`, `agent_workspace_paths`, `topic_team_validation_status`, and `isomer_topic_summary_path`.

            ```generated-guide
            Generated Guide
            ```
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "SKILL.md",
            skill_text,
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
            if subcommand_name == "help.md":
                write(
                    root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / subcommand_name,
                    """
                    # Help

                    ## Workflow

                    1. Print public subcommands as a table.

                    If the user's task does not map cleanly to these steps, use your native planning tool.

                    ## Public Subcommands

                    | Subcommand | Purpose | Produces |
                    | --- | --- | --- |
                    | `init-topic` | Start topic setup. | `topic-overview.md`. |
                    | `clarify-topic` | Clarify topic. | Updated `topic-overview.md`. |
                    | `specialize-team` | Specialize topic team. | Draft profile inputs. |
                    | `setup-topic-env` | Prepare topic environment. | `topic_environment_status`. |
                    | `setup-agent-workspace` | Prepare Agent Workspaces. | `agent_workspace_paths`. |
                    | `validate-topic-team` | Validate static material. | `topic_team_validation_status`. |
                    | `finalize-topic-team` | Finalize topic team. | `isomer-topic-summary.md`. |
                    | `approve-profile` | Approve profile material. | Approval provenance. |
                    | `materialize-profile` | Materialize profile material. | Static profile bundle. |
                    | `fast-forward` | Run automatic flow. | Final summary. |
                    | `step-by-step` | Run guided flow. | Step summaries. |
                    """,
                )
                continue
            prerequisite = ""
            if (
                subcommand_name in validator.TOPIC_TEAM_SPECIALIZATION_PROCEDURAL_SUBCOMMANDS
                and subcommand_name != omit_prerequisite_subcommand
            ):
                prerequisite = """
                ## Prerequisite Artifacts

                If any required predecessor artifact is missing, refuse to run and tell the user why.
                """
            write(
                root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / subcommand_name,
                f"""
                # {subcommand_name}

                ## Workflow

                1. Run the subcommand fixture step.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                {prerequisite}
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
        self.write_project_manager_skill(root)

    def write_project_manager_skill(
        self,
        root: Path,
        *,
        omit_subcommand: str | None = None,
        external_ref: bool = False,
        omit_subcommand_fallback: bool = False,
    ) -> None:
        write(
            root / "skillset" / "operator" / "isomer-admin-project-mgr" / "SKILL.md",
            """
            ---
            name: isomer-admin-project-mgr
            description: Valid fixture project manager skill.
            ---

            # Isomer Admin Project Mgr

            ## Workflow

            1. **Default help mode**: If invoked without a prompt, run `help`.
            2. Select one subcommand and load only the selected subcommand page.
            3. Preserve `.isomer-labs/`, `isomer-content/`, `isomer-content/topic-ws/<topic-id>/`, `--content-dir <content-dir>`, `<content-dir>/topic-ws/<topic-id>/`, `.houmao/`, Project-level Houmao overlay, `isomer-cli project init`, `isomer-cli project cleanup --part <part> --dry-run`, `isomer-cli project cleanup --part <part> --yes`, `--purge-content-root`, unknown files, `isomer-cli project validate`, `isomer-cli project doctor`, `isomer-cli project runtime init`, `isomer-cli project runtime prepare`, and `isomer-admin-topic-team-specialize` boundaries.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            Use `references/help.md`, `references/init-project.md`, `references/cleanup-project.md`, `references/check-project.md`, `references/list-topics.md`, `references/show-context.md`, `references/init-runtime.md`, `references/prep-runtime.md`, and `references/specialize-team.md`.
            """,
        )
        write(
            root / "skillset" / "operator" / "isomer-admin-project-mgr" / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-admin-project-mgr"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-admin-project-mgr to validate this fixture."
            """,
        )
        for subcommand_name in validator.PROJECT_MANAGER_SUBCOMMANDS:
            if subcommand_name == omit_subcommand:
                continue
            fallback = "" if omit_subcommand_fallback and subcommand_name == "help.md" else "If the user's task does not map cleanly to these steps, use your native planning tool."
            external = "Read `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`." if external_ref and subcommand_name == "check-project.md" else ""
            write(
                root / "skillset" / "operator" / "isomer-admin-project-mgr" / "references" / subcommand_name,
                f"""
                # {subcommand_name}

                ## Workflow

                1. Run the subcommand fixture step. {external}

                {fallback}
                """,
            )
        for support_reference_name in validator.PROJECT_MANAGER_SUPPORT_REFERENCES:
            write(
                root / "skillset" / "operator" / "isomer-admin-project-mgr" / "references" / support_reference_name,
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

    def test_operator_validator_requires_topic_team_subcommand_groups(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root, omit_skill_term="Procedural Subcommands")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("Procedural Subcommands" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_team_topic_setup_validation_and_summary_terms(self) -> None:
        required_terms = (
            "topic-overview.md",
            "selected_domain_team_template_ref",
            "topic_environment_status",
            "agent_workspace_paths",
            "topic_team_validation_status",
            "isomer_topic_summary_path",
        )
        for term in required_terms:
            with self.subTest(term=term):
                root = self.make_root()
                self.write_topic_team_specialization_skill(root, omit_skill_term=term)
                self.write_deepsci_mini_guide(root)

                diagnostics = validator.validate_operator_skillset(root)

                self.assertIn("OPS003", codes(diagnostics))
                self.assertTrue(any(term in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_team_skill_fallback(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root, omit_fallback=True)
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("must include a freeform fallback" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_team_subcommands(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        (root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "resolve-project.md").unlink()

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("resolve-project.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_new_topic_team_subcommands(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        (root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "init-topic.md").unlink()

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("init-topic.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_procedural_subcommand_prerequisites(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root, omit_prerequisite_subcommand="specialize-team.md")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("specialize-team.md" in message and "predecessor artifacts" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_private_helpers_in_help(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "help.md",
            """
            # Help

            ## Workflow

            1. List public commands and `resolve-project`.

            If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("private helper subcommand 'resolve-project'" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_launch_team_in_help(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "help.md",
            """
            # Help

            ## Workflow

            1. List public commands and `launch-team`.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Public Subcommands

            | Subcommand | Purpose | Produces |
            | --- | --- | --- |
            | `launch-team` | Run live team. | Runtime records. |
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("private helper subcommand 'launch-team'" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_help_subcommand_table(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "help.md",
            """
            # Help

            ## Workflow

            1. List public commands.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Public Subcommands

            - `init-topic`
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("three-column table" in message for message in messages(diagnostics)), messages(diagnostics))

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

    def test_operator_validator_rejects_launch_team_subcommand(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "launch-team.md",
            """
            # Launch Team

            ## Workflow

            1. Launch live team.

            If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("unexpected reference page references/launch-team.md" in message for message in messages(diagnostics)), messages(diagnostics))

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

    def test_operator_validator_requires_project_manager_subcommands(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        (root / "skillset" / "operator" / "isomer-admin-project-mgr" / "references" / "list-topics.md").unlink()

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS005", codes(diagnostics))
        self.assertTrue(any("list-topics.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_external_project_manager_support_refs(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_project_manager_skill(root, external_ref=True)
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS005", codes(diagnostics))
        self.assertTrue(any("must keep required support references inside its skill directory" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_project_manager_subcommand_fallback(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_project_manager_skill(root, omit_subcommand_fallback=True)
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS005", codes(diagnostics))
        self.assertTrue(any("must include a freeform fallback" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_project_manager_evals(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(root / "skillset" / "operator" / "isomer-admin-project-mgr" / "evals" / "evals.json", "{}")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS005", codes(diagnostics))
        self.assertTrue(any("must not contain evals/" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_root_project_manager_cli_shapes(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_project_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-admin-project-mgr" / "references" / "check-project.md",
            """
            # Check Project

            ## Workflow

            1. Run `pixi run isomer-cli --project <project-root> validate`.

            If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS005", codes(diagnostics))
        self.assertTrue(any("isomer-cli project ..." in message for message in messages(diagnostics)), messages(diagnostics))
