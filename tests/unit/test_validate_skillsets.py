from __future__ import annotations

import importlib.util
import json
import shutil
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


OUTPUT_CONTRACT_FIXTURE = """
            ## Output Contract

            Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

            ### Essential Output

            - Report the concise status, blockers, evidence, and next action.

            ### Complete Output

            - Include all bookkeeping, semantic refs, audit evidence, and handoff fields.

            ## Chat Response

            Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
"""

INVOCATION_NOTATION_FRONTMATTER = """
            skill_invocation_notation: >
              Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
              `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
              `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
              subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
              by parent subcommand parent. Intermediate subcommands act as object generators.
              Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
"""

SYSTEM_SKILL_MANAGER_SOURCE = (
    REPO_ROOT
    / "skillset"
    / "operator"
    / "isomer-op-entrypoint"
    / "subskills"
    / "isomer-op-system-skill-mgr"
)


class SkillsetValidatorTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        write(root / "pyproject.toml", "[project]\nname = \"fixture\"\n")
        write(root / "skillset" / "research-paradigm" / "README.md", "# Research Skills\n")
        write(root / "skillset" / "service" / "README.md", "# Service Skills\n")
        return root

    def write_v3_invocation_fixture(self, root: Path) -> None:
        write(
            root / "skillset" / "manifest.toml",
            """
            schema_version = "isomer-skillset-manifest.v3"

            [[packs]]
            pack_id = "core"
            description = "Fixture public pack."
            kind = "core"
            source_path = "operator/isomer-op-entrypoint"
            entry_skill = "isomer-op-entrypoint"
            always_available = true
            minimum_compatible_skill_version = "0.1.0"
            public_commands = ["manage", "project"]
            protected_members = ["isomer-op-project-mgr"]
            legacy_aliases = []
            callback_insertion_points = []

            [[capabilities]]
            logical_id = "isomer-op-project-mgr"
            pack_id = "core"
            area = "operator"
            member_name = "project"
            source_path = "operator/isomer-op-entrypoint/subskills/isomer-op-project-mgr"
            invocation_designator = "isomer-op-entrypoint->project"
            dependencies = []
            legacy_aliases = []
            callback_insertion_points = []
            """,
        )
        pack = root / "skillset" / "operator" / "isomer-op-entrypoint"
        write(
            pack / "SKILL.md",
            f"""
            ---
            name: isomer-op-entrypoint
            description: Use when validating invocation routes.
            {INVOCATION_NOTATION_FRONTMATTER}
            ---

            # Fixture Entrypoint

            `isomer-op-entrypoint->project` selects the protected member while `isomer-op-entrypoint->project()` selects the same-name public command.
            `isomer-op-entrypoint->manage()->list()` selects a nested public command.
            """,
        )
        write(
            pack / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-op-entrypoint"
              default_prompt: "Use $isomer-op-entrypoint for this task."
            """,
        )
        write(
            pack / "commands" / "manage.md",
            f"""
            ---
            {INVOCATION_NOTATION_FRONTMATTER}
            ---

            # Manage

            ## Subcommands

            | Child | Detail |
            | --- | --- |
            | `isomer-op-entrypoint->manage()->list()` | [commands/manage/list.md](commands/manage/list.md) |
            """,
        )
        write(
            pack / "commands" / "manage" / "list.md",
            f"""
            ---
            {INVOCATION_NOTATION_FRONTMATTER}
            ---

            # List

            Route: `isomer-op-entrypoint->manage()->list()`.
            """,
        )
        capability = pack / "subskills" / "isomer-op-project-mgr"
        write(
            capability / "SKILL.md",
            f"""
            ---
            name: isomer-op-project-mgr
            description: Use when validating a protected member route.
            {INVOCATION_NOTATION_FRONTMATTER}
            ---

            # Project Manager

            Route: `isomer-op-entrypoint->project`.

            ## Subcommands

            | Child | Detail |
            | --- | --- |
            | `isomer-op-entrypoint->project->inspect()` | [commands/inspect.md](commands/inspect.md) |
            """,
        )
        write(
            capability / "commands" / "inspect.md",
            f"""
            ---
            {INVOCATION_NOTATION_FRONTMATTER}
            ---

            # Inspect

            Route: `isomer-op-entrypoint->project->inspect()`.
            """,
        )
        write(
            capability / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-op-project-mgr"
              default_prompt: "Use $isomer-op-entrypoint use project to inspect the project."
            """,
        )

    def test_v3_invocation_validator_distinguishes_same_name_member_and_command(self) -> None:
        root = self.make_root()
        self.write_v3_invocation_fixture(root)

        diagnostics = validator.validate_system_skill_invocations(root)

        self.assertEqual([], messages(diagnostics))

    def test_v3_invocation_validator_rejects_ambiguous_malformed_and_undeclared_routes(self) -> None:
        root = self.make_root()
        self.write_v3_invocation_fixture(root)
        page = root / "skillset" / "operator" / "isomer-op-entrypoint" / "commands" / "broken.md"
        write(
            page,
            f"""
            ---
            {INVOCATION_NOTATION_FRONTMATTER}
            ---

            # Broken Routes

            `isomer-op-entrypoint->manage`
            `isomer-op-entrypoint->manage()->list`
            `isomer-op-entrypoint->manage()->remove()`
            `isomer-op-entrypoint->manage()->latex()`
            """,
        )
        write(
            root
            / "skillset"
            / "operator"
            / "isomer-op-entrypoint"
            / "subskills"
            / "undeclared"
            / "SKILL.md",
            "# Undeclared\n",
        )

        rendered = messages(validator.validate_system_skill_invocations(root))

        self.assertTrue(any("declared command and must use ()" in message for message in rendered), rendered)
        self.assertTrue(any("must not return to a bare component" in message for message in rendered), rendered)
        self.assertTrue(any("does not declare child route" in message for message in rendered), rendered)
        self.assertTrue(any("role parameters" in message for message in rendered), rendered)
        self.assertTrue(any("not declared as a protected capability" in message for message in rendered), rendered)

    def test_v3_invocation_validator_requires_notation_and_public_protected_prompts(self) -> None:
        root = self.make_root()
        self.write_v3_invocation_fixture(root)
        pack = root / "skillset" / "operator" / "isomer-op-entrypoint"
        write(pack / "references" / "missing-notation.md", "Use `isomer-op-entrypoint->project`.\n")
        write(
            pack / "subskills" / "isomer-op-project-mgr" / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-op-project-mgr"
              default_prompt: "Use $isomer-op-project-mgr directly."
            """,
        )

        rendered = messages(validator.validate_system_skill_invocations(root))

        self.assertTrue(any("exact standard skill_invocation_notation" in message for message in rendered), rendered)
        self.assertTrue(any("owning public entrypoint" in message for message in rendered), rendered)

    def test_repository_boundary_scans_source_mirrored_symlink_projection(self) -> None:
        root = self.make_root()
        projected_source = root / "src" / "packaged-skills" / "operator"
        write(
            projected_source / "isomer-op-fixture" / "SKILL.md",
            "# Fixture\n\nRun `project repos "
            "acquire SOURCE --semantic-label topic.repos.sources.fixture`.\n",
        )
        operator_projection = root / "skillset" / "operator"
        operator_projection.parent.mkdir(parents=True, exist_ok=True)
        operator_projection.symlink_to(projected_source, target_is_directory=True)

        diagnostics = validator.validate_system_skill_repository_boundary(root, (operator_projection,))

        self.assertEqual({"SKL008"}, codes(diagnostics))
        self.assertTrue(any("removed repository command" in message for message in messages(diagnostics)))

        write(
            projected_source / "isomer-op-fixture" / "SKILL.md",
            "# Fixture\n\nRun the user-selected repository command externally, verify immutable identity, then use `project repos register`.\n",
        )
        self.assertEqual([], validator.validate_system_skill_repository_boundary(root, (operator_projection,)))

    def write_current_template_fixture(self, root: Path) -> None:
        write(
            root / "skillset" / "manifest.toml",
            """
            [groups.core]
            skills = ["misc/isomer-misc-template-fixture"]

            [groups.deepsci]
            skills = ["research-paradigm/deepsci/isomer-deepsci-template-fixture"]

            [groups.kaoju]
            skills = ["research-paradigm/kaoju/isomer-kaoju-template-fixture"]
            """,
        )
        for relative_skill in (
            "misc/isomer-misc-template-fixture",
            "research-paradigm/deepsci/isomer-deepsci-template-fixture",
            "research-paradigm/kaoju/isomer-kaoju-template-fixture",
        ):
            skill_name = Path(relative_skill).name
            write(
                root / "skillset" / relative_skill / "SKILL.md",
                f"""
                ---
                name: {skill_name}
                description: Use when validating the packaged system-skill template fixture.
                ---

                # {skill_name}

                ## Overview

                This fixture exercises current packaged system-skill structure.

                ## When to Use

                Use it only in validator tests; do not use it as a production skill.

                ## Workflow

                1. Read the fixture input.
                2. Report the fixture result.

                If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan, then execute the plan.

                ## Subcommands

                | Subcommand | Use For | Detail |
                | --- | --- | --- |
                | `run` | Execute the fixture. | [commands/run.md](commands/run.md) |

                ## Guardrails

                - DO NOT treat excluded fixture files as active instructions.
                - DO NOT discard the current-template structure.
                """,
            )
            write(
                root / "skillset" / relative_skill / "commands" / "run.md",
                """
                # Run Fixture

                ## Workflow

                1. Read the input.
                2. Report the output.

                If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan, then execute the plan.

                ## Guardrails

                - DO NOT make the fixture nondeterministic.

                ## Troubleshooting Guide

                - The fixture input is missing.
                  - If the fixture input is missing, then report the missing input.
                """,
            )
            write(
                root / "skillset" / relative_skill / "references" / "explanation.md",
                """
                # Explanation

                This page explains the fixture and is not an executable procedure.
                """,
            )
            write(
                root / "skillset" / relative_skill / "org" / "src" / "SKILL.md",
                """
                # Historical Source

                ## Common Mistakes

                Do not rewrite this provenance copy.
                """,
            )
            write(root / "skillset" / relative_skill / "migrate" / "notes.md", "## Common Mistakes\n")
            write(root / "skillset" / relative_skill / "templates" / "output.md", "## Common Mistakes\n")

    def test_packaged_template_validator_discovers_all_groups_and_excludes_passive_roles(self) -> None:
        root = self.make_root()
        self.write_current_template_fixture(root)

        manifest_diagnostics: list[object] = []
        skill_dirs = validator.packaged_skill_dirs(root, manifest_diagnostics)
        diagnostics = validator.validate_packaged_skill_template(root)

        self.assertEqual(3, len(skill_dirs))
        self.assertEqual([], messages(manifest_diagnostics))
        self.assertEqual([], messages(diagnostics))
        active_paths = {
            path.relative_to(skill_dirs[0]).as_posix()
            for path in validator.active_skill_markdown_pages(skill_dirs[0])
        }
        self.assertNotIn("org/src/SKILL.md", active_paths)
        self.assertNotIn("migrate/notes.md", active_paths)
        self.assertNotIn("templates/output.md", active_paths)

    def test_packaged_template_validator_rejects_entrypoint_template_gaps(self) -> None:
        root = self.make_root()
        self.write_current_template_fixture(root)
        skill_path = root / "skillset" / "misc" / "isomer-misc-template-fixture" / "SKILL.md"
        write(
            skill_path,
            """
            ---
            name: isomer-misc-template-fixture
            description: Validate a fixture by running its workflow.
            ---

            # Broken Fixture

            ## Workflow

            Run the fixture.

            ## Guardrails

            - Do not skip the fixture.

            ## Guardrails

            - MUST report the fixture.

            ## Common Mistakes

            Do not omit output.
            """,
        )

        diagnostics = validator.validate_packaged_skill_template(root)
        rendered = messages(diagnostics)

        self.assertIn(validator.SYSTEM_SKILL_TEMPLATE_CODE, codes(diagnostics))
        self.assertTrue(any("description must start with 'Use when'" in message for message in rendered), rendered)
        self.assertTrue(any("## Overview" in message for message in rendered), rendered)
        self.assertTrue(any("## When to Use" in message for message in rendered), rendered)
        self.assertTrue(any("numbered steps" in message for message in rendered), rendered)
        self.assertTrue(any("freeform planning fallback" in message for message in rendered), rendered)
        self.assertTrue(any("exactly one ## Guardrails" in message for message in rendered), rendered)
        self.assertTrue(any("must not contain ## Common Mistakes" in message for message in rendered), rendered)

    def test_packaged_template_validator_requires_workflow_before_other_top_level_sections(self) -> None:
        root = self.make_root()
        self.write_current_template_fixture(root)
        skill_path = root / "skillset" / "misc" / "isomer-misc-template-fixture" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "## Workflow",
                "## Background\n\nSupporting detail.\n\n## Workflow",
                1,
            ),
            encoding="utf-8",
        )

        diagnostics = validator.validate_packaged_skill_template(root)

        self.assertTrue(any("before other top-level sections" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_packaged_template_validator_allows_plan_first_before_overview(self) -> None:
        root = self.make_root()
        self.write_current_template_fixture(root)
        skill_path = root / "skillset" / "misc" / "isomer-misc-template-fixture" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "## Overview",
                "## Plan First\n\nCreate a plan with the internal todo list before executing this complex workflow.\n\n## Overview",
                1,
            ),
            encoding="utf-8",
        )

        diagnostics = validator.validate_packaged_skill_template(root)

        self.assertFalse(any("before other top-level sections" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_packaged_template_validator_checks_executable_subpages_and_guardrails(self) -> None:
        root = self.make_root()
        self.write_current_template_fixture(root)
        command_path = root / "skillset" / "misc" / "isomer-misc-template-fixture" / "commands" / "run.md"
        write(
            command_path,
            """
            # Broken Command

            ## Workflow

            1. Run the command.

            ## Guardrails

            - MUST keep the fixture deterministic.
            """,
        )

        diagnostics = validator.validate_packaged_skill_template(root)
        rendered = messages(diagnostics)

        self.assertTrue(any("freeform planning fallback" in message and "commands/run.md" in message for message in rendered), rendered)
        self.assertTrue(any("must start with DO NOT" in message and "commands/run.md" in message for message in rendered), rendered)
        self.assertFalse(any("references/explanation.md" in message for message in rendered), rendered)

    def test_packaged_template_validator_rejects_malformed_optional_troubleshooting(self) -> None:
        root = self.make_root()
        self.write_current_template_fixture(root)
        reference_path = root / "skillset" / "misc" / "isomer-misc-template-fixture" / "references" / "explanation.md"
        write(
            reference_path,
            """
            # Explanation

            ## Troubleshooting Guide

            - A fixture problem occurs.
              - Retry the operation.
              - If the fixture problem occurs, then inspect the input.
            """,
        )

        diagnostics = validator.validate_packaged_skill_template(root)
        rendered = messages(diagnostics)

        self.assertTrue(any("exactly one nested solution" in message for message in rendered), rendered)
        self.assertTrue(any("If <problem>, then <action>." in message for message in rendered), rendered)

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
            name: isomer-op-topic-team-specialize
            description: Use when the user explicitly invokes Topic Team Specialization or the prompt or authoritative context establishes a formal Agent Team target and applies the requested action to that team.
            ---

            # Isomer Admin Topic Team Specialize

            ## Workflow

            1. **Default help mode**: If invoked without a prompt, run `help`.
            2. **Manual mode**: Select one subcommand, load only its detail page, and report the result.
            3. **Guided mode**: Run `step-by-step`.
            4. **Automatic mode**: Run `fast-forward`.

            {fallback}

            A delegated request must preserve prompt or authoritative context that identifies a formal Agent Team target. Generic preparation, launch-facing language, readiness gaps, missing summaries, and missing Agent Workspaces do not establish that target.

            Use `references/step-dependencies.json` and `scripts/query_step_dependencies.py` for procedural dependency paths.

            ## Subcommands

            Procedural Subcommands: `init-topic`, `clarify-topic`, `ensure-topic-registration`, `adapt-team-template`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, and `materialize-profile`.

            Helper Subcommands: five lower-level implementation commands: `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile`.

            Misc Subcommands: `help`, `fast-forward`, and `step-by-step`.

            Use {subcommand_links}.

            Use static material readiness, durable setup state, `topic-overview.md`, concrete Research Topic, default Research Topic, provisional topic workspace seed, `isomer-content/topic-ws/<topic-slug>/`, `team-specialization-guide.md`, `team-specialization-plan.md`, `{final_report}`, `<topic-workspace>/team-profile/execplan/`, `isomer-managed/`, and `isomer-topic-summary.md`.

            Require semantic label evidence for `topic.repos.main`, `agent.workspace`, and required `agent.*` support paths. Report `selected_domain_team_template_ref`, `topic_environment_status`, `agent_workspace_paths`, `semantic_paths`, semantic labels, path sources, `topic_team_validation_status`, and `isomer_topic_summary_path`.

            ```generated-guide
            Generated Guide
            ```

            {OUTPUT_CONTRACT_FIXTURE}
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(
            root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "SKILL.md",
            skill_text,
        )
        write(
            root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-op-topic-team-specialize"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-op-topic-team-specialize to validate this fixture."
            """,
        )
        for subcommand_name in validator.TOPIC_TEAM_SPECIALIZATION_SUBCOMMANDS:
            if subcommand_name == "help.md":
                write(
                    root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / subcommand_name,
                    """
                    # Help

                    ## Workflow

                    1. Print public subcommands as a table with semantic path evidence.
                    2. Explain that `references/step-dependencies.json` and `scripts/query_step_dependencies.py` provide centralized dependency paths.

                    If the user's task does not map cleanly to these steps, use your native planning tool.

                    ## Public Subcommands

                    | Subcommand | Purpose | Produces |
                    | --- | --- | --- |
                    | `init-topic` | Start topic setup. | `topic-overview.md`. |
                    | `clarify-topic` | Clarify topic. | Updated `topic-overview.md`. |
                    | `ensure-topic-registration` | Ensure Project registration. | Registered topic refs. |
                    | `adapt-team-template` | Adapt team template. | Draft profile inputs. |
                    | `setup-topic-env` | Prepare topic environment. | `topic_environment_status`. |
                    | `setup-agent-workspace` | Prepare Agent Workspaces. | `semantic_paths`, `topic.repos.main`, `agent.workspace`, `agent_workspace_paths`. |
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
            extra_terms = ""
            if subcommand_name == "setup-agent-workspace.md":
                extra_terms = """
                Require `topic.repos.main`, `agent.workspace`, `agent.tmp`, required `agent.*` support paths, `semantic_paths`, `local_tmp_path_status`, semantic labels, path sources, `topic.intent.agent_env_requirements`, `topic.env.agent_setup_target_spec`, and `isomer-srv-agent-env-setup`. generate the source gate from a clear task and reject default-looking directories without semantic labels and path sources. Accept readiness only when every required per-agent `## Gate Checklist` item has evidence, preserve selected-agent partial evidence, require `operation_classification` with classification source, and record any weaker smoke-test substitution as a limitation.
                """
            elif subcommand_name == "validate-topic-team.md":
                extra_terms = """
                Require `topic.repos.main`, `agent.workspace`, `agent.tmp`, required `agent.*` support labels, `semantic_paths`, `local_tmp_path_status`, path sources, and reject hard-coded default-only paths without semantic labels. Verify every required topic gate checklist item and every required per-agent checklist item, require operation classification evidence, and preserve any weaker smoke-test downgrade.
                """
            elif subcommand_name == "finalize-topic-team.md":
                extra_terms = """
                Report semantic labels first with `topic.repos.main`, `topic.repos.main.tmp`, `agent.workspace`, `agent.tmp`, path sources, `isomer-default.v1`, and reject hard-coded default-only paths without semantic label evidence. Include required topic `## Gate Checklist` completion evidence, required per-agent `## Gate Checklist` completion evidence, and smoke-test downgrades.
                """
            elif subcommand_name == "setup-topic-env.md":
                extra_terms = """
                Require complete required `## Gate Checklist` evidence before accepting ready, keep each required checklist item visible when blocked, failed, or not checked, require `operation_classification`, state that bounded-run tips owns the classification decision, and reject a weaker smoke test as readiness evidence.
                """
            elif subcommand_name == "fast-forward.md":
                extra_terms = """
                Use `scripts/query_step_dependencies.py` and `references/step-dependencies.json` to compute full and targeted fast-forward paths.
                """
            write(
                root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / subcommand_name,
                f"""
                # {subcommand_name}

                ## Workflow

                1. Run the subcommand fixture step.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                {prerequisite}
                {extra_terms}
                """,
            )
        for support_reference_name in validator.TOPIC_TEAM_SPECIALIZATION_SUPPORT_REFERENCES:
            write(
                root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / support_reference_name,
                f"""
                # {support_reference_name}

                Local support reference.
                """,
            )
        self.write_topic_team_dependency_contract(root)
        self.write_project_manager_skill(root)
        self.write_topic_creator_skill(root)
        self.write_topic_manager_skill(root)
        self.write_welcome_skill(root)
        self.write_entrypoint_skill(root)
        self.write_switch_identity_skill(root)
        shutil.copytree(
            SYSTEM_SKILL_MANAGER_SOURCE,
            root / "skillset" / "operator" / "isomer-op-system-skill-mgr",
        )

    def write_topic_team_dependency_contract(self, root: Path) -> None:
        skill_dir = root / "skillset" / "operator" / "isomer-op-topic-team-specialize"
        step_ids = [subcommand.removesuffix(".md") for subcommand in validator.TOPIC_TEAM_SPECIALIZATION_PROCEDURAL_SUBCOMMANDS]
        steps = {}
        edges = []
        previous_step_id = None
        for step_id in step_ids:
            predecessors = []
            if previous_step_id is not None:
                predecessors.append({"step": previous_step_id, "condition": "Fixture predecessor output is missing."})
                edges.append({"from": previous_step_id, "to": step_id, "condition": "Fixture canonical order."})
            steps[step_id] = {
                "id": step_id,
                "display_name": step_id.replace("-", " ").title(),
                "kind": "procedural",
                "predecessors": predecessors,
                "requires": ["Fixture input."],
                "produces": ["Fixture output."],
                "recovery_conditions": ["Fixture recovery condition."],
                "mutation_notes": ["Fixture mutation note."],
                "unrecoverable_blockers": ["Fixture blocker."],
            }
            previous_step_id = step_id
        manifest = {
            "version": 1,
            "description": "Fixture step dependency graph.",
            "canonical_order": step_ids,
            "steps": steps,
            "edges": edges,
        }
        write(
            skill_dir / "references" / "step-dependencies.json",
            json.dumps(manifest, indent=2),
        )
        write(
            skill_dir / "scripts" / "query_step_dependencies.py",
            """
            #!/usr/bin/env python3
            from __future__ import annotations

            import json
            import sys
            from pathlib import Path


            def main() -> int:
                if len(sys.argv) > 1 and sys.argv[1] == "validate":
                    manifest_path = Path(__file__).resolve().parents[1] / "references" / "step-dependencies.json"
                    json.loads(manifest_path.read_text(encoding="utf-8"))
                    print("step-dependencies.json is valid")
                    return 0
                print("fixture dependency query")
                return 0


            if __name__ == "__main__":
                raise SystemExit(main())
            """,
        )

    def write_project_manager_skill(
        self,
        root: Path,
        *,
        omit_subcommand: str | None = None,
        external_ref: bool = False,
        omit_subcommand_fallback: bool = False,
    ) -> None:
        write(
            root / "skillset" / "operator" / "isomer-op-project-mgr" / "SKILL.md",
            f"""
            ---
            name: isomer-op-project-mgr
            description: Valid fixture project manager skill.
            ---

            # Isomer Admin Project Mgr

            ## Workflow

            1. **Default help mode**: If invoked without a prompt, run `help`.
            2. Select one subcommand and load only the selected subcommand page.
            3. Preserve `.isomer-labs/`, `.isomer-labs/.houmao/`, root `.houmao/` as external user-owned state, `isomer-content/`, `isomer-content/topic-ws/<topic-id>/`, `--content-dir <content-dir>`, `<content-dir>/topic-ws/<topic-id>/`, Isomer-managed Houmao overlay, `isomer-cli project init`, `isomer-cli project cleanup --part <part> --dry-run`, `isomer-cli project cleanup --part <part> --yes`, `--purge-content-root`, `isomer-cli project content-root move --to <content-dir> --dry-run`, `isomer-cli project content-root move --to <content-dir> --yes`, unknown files, `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project runtime init`, `isomer-cli project runtime prepare`, `isomer-op-topic-creator`, `isomer-op-topic-mgr`, and `isomer-op-topic-team-specialize` boundaries.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            Use `references/help.md`, `references/init-project.md`, `references/cleanup-project.md`, `references/move-content.md`, `references/check-project.md`, `references/list-topics.md`, `references/show-context.md`, `references/init-runtime.md`, `references/prep-runtime.md`, `references/prepare-topic.md`, `references/manual-research.md`, and `references/specialize-team.md`.

            {OUTPUT_CONTRACT_FIXTURE}
            """,
        )
        write(
            root / "skillset" / "operator" / "isomer-op-project-mgr" / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-op-project-mgr"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-op-project-mgr to validate this fixture."
            """,
        )
        for subcommand_name in validator.PROJECT_MANAGER_SUBCOMMANDS:
            if subcommand_name == omit_subcommand:
                continue
            fallback = "" if omit_subcommand_fallback and subcommand_name == "help.md" else "If the user's task does not map cleanly to these steps, use your native planning tool."
            external = "Read `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`." if external_ref and subcommand_name == "check-project.md" else ""
            write(
                root / "skillset" / "operator" / "isomer-op-project-mgr" / "references" / subcommand_name,
                f"""
                # {subcommand_name}

                ## Workflow

                1. Run the subcommand fixture step. {external}

                {fallback}
                """,
            )
        for support_reference_name in validator.PROJECT_MANAGER_SUPPORT_REFERENCES:
            write(
                root / "skillset" / "operator" / "isomer-op-project-mgr" / "references" / support_reference_name,
                f"""
                # {support_reference_name}

                Local support reference.
                """,
            )

    def write_topic_creator_skill(
        self,
        root: Path,
        *,
        omit_command: str | None = None,
        omit_skill_term: str | None = None,
    ) -> None:
        skill_dir = root / "skillset" / "operator" / "isomer-op-topic-creator"
        command_links = ", ".join(f"`references/{command_name}`" for command_name in validator.TOPIC_CREATOR_COMMANDS)
        skill_text = f"""
            ---
            name: isomer-op-topic-creator
            description: Valid fixture topic creator skill.
            ---

            # Isomer Admin Topic Creator

            Create a prepared Topic Workspace through Project Manifest-backed context, `topic.repos.main`, `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.actor_env_gates`, `topic.workspace.summary`, structured reset checkpoint, Workspace Runtime, Topic Actors and their workspaces, actor-scoped semantic paths, and actor onboarding.

            ## Workflow

            1. **Default help mode**: If invoked without a prompt, run `help`.
            2. Select one subcommand and load only that subcommand page.
            3. Preserve lower-level owner boundaries for `isomer-op-project-mgr`, `isomer-srv-topic-env-setup`, `isomer-op-topic-mgr`, and `isomer-op-topic-team-specialize`.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            Procedural Subcommands: `setup-topic-env`, `setup-actors`, and `finalize`.

            Procedural Subcommands: `create-research-intent`, `define-topic-env`, `setup-topic-env`, `define-actors`, `setup-actors`, and `finalize`.

            Helper Subcommands are lower-level ladder stages: `ensure-project`, `resolve-topic-input`, `register-topic`, `init-runtime`.

            Misc Subcommands: `help`, `fast-forward`, `step-by-step`, `run-to`, `status`, and `repair`.

            Use {command_links}.

            {OUTPUT_CONTRACT_FIXTURE}
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(skill_dir / "SKILL.md", skill_text)
        write(
            skill_dir / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-op-topic-creator"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-op-topic-creator to validate this fixture."
            """,
        )
        for command_name in validator.TOPIC_CREATOR_COMMANDS:
            if command_name == omit_command:
                continue
            extra_terms = {
                "help.md": "Subcommand Functionalities. Procedural Subcommands. Helper Subcommands. Misc Subcommands. Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.",
                "fast-forward.md": "`fast-forward` stops at the first blocker, routes through `define-topic-env` and `define-actors`, and ends at `finalize`.",
                "resolve-topic-input.md": "Resolve a concrete Research Topic. DO NOT use this helper to write `topic.intent.overview`.",
                "create-research-intent.md": "Write only `topic.intent.overview` from `templates/topic-overview.md`; Strip `>` example blocks; populate `Research Topic`, `Motivation`, `Topic Breakdown` with `Do's` and `Don'ts`, `Expected Outcome`, and `Related Links`; do not write `topic.intent.topic_env_requirements`.",
                "clarify-research-intent.md": "Refine `topic.intent.overview` interactively through Coverage and Clarity Scan, Question Format, Sequential Clarification Loop, Direct Topic Overview Integration, Prerequisite Artifacts, and Guardrails. Check `Research Topic`, `Motivation`, `Topic Breakdown`, `Do's`, `Don'ts`, `Expected Outcome`, and `Related Links`.",
                "define-topic-env.md": "Create `topic.intent.topic_env_requirements`, wait for user verification, and report `fast-forward` assumptions.",
                "setup-topic-env.md": "Delegate to `isomer-srv-topic-env-setup`, read `topic.intent.topic_env_requirements`, derive `topic.env.topic_setup_target_spec`, and report `topic.repos.main` readiness.",
                "define-actors.md": "Create `topic.intent.actor_definitions` for the default `operator` and each actor source env gate.",
                "setup-actors.md": "Delegate to `isomer-op-topic-mgr`, consume `topic.intent.actor_definitions`, report `topic.actors.workspace`, and verify `topic.env.actor_env_gates`.",
                "finalize.md": "Resolve `topic.workspace.summary`, run `isomer-cli project topic-reset checkpoint`, create a structured reset checkpoint from operator-level readiness evidence, report ready, verified, blocked, and skipped state. DO NOT recommend a next research step.",
                "step-by-step.md": "Follow the same main workflow order as `fast-forward`, show an option table with Recommended choices, and require acknowledgement.",
                "run-to.md": "Valid targets are procedural. The target is included by default, explicit exclusion stops before it, and the command stops on missing user input.",
                "status.md": "Report ready, blocked, skipped, and `topic.workspace.summary` state.",
                "repair.md": "Repair the first blocked stage without rerunning ready destructive work.",
            }.get(command_name, "Report blocker state and next subcommand.")
            write(
                skill_dir / "references" / command_name,
                f"""
                # {command_name}

                ## Workflow

                1. Run the command fixture step and report any blocker.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                {extra_terms}
                """,
            )

    def write_topic_manager_skill(
        self,
        root: Path,
        *,
        omit_subcommand: str | None = None,
        omit_skill_term: str | None = None,
        omit_subcommand_fallback: bool = False,
    ) -> None:
        skill_dir = root / "skillset" / "operator" / "isomer-op-topic-mgr"
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        subcommand_links = ", ".join(
            f"`references/{subcommand_name}`" for subcommand_name in validator.TOPIC_MANAGER_SUBCOMMANDS
        )
        skill_terms = "\n".join(f"            {term}" for term in validator.TOPIC_MANAGER_REQUIRED_SKILL_TERMS)
        skill_text = f"""
            ---
            name: isomer-op-topic-mgr
            description: Valid fixture topic manager skill.
            ---

            # Isomer Admin Topic Mgr

            Manage an initialized-topic after `isomer-op-topic-creator` handoff. This fixture covers storage, actors, team topology, environment mutation, environment verification, reset checkpoint handling, diagnostics, and blocker reporting.

            ## Workflow

            1. **Default subcommand**: Run `status`.
            2. Select one subcommand and load only its detail page.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            Status Subcommands: `status`, `doctor`, and `help`.
            Storage Subcommands: `storage-resolve`, `storage-inspect-main`, `storage-validate`, and `storage-register-repo`.
            Actor Subcommands: `actors-manage`, `actors-materialize`, and `actors-diagnose`.
            Team Subcommands: `team-plan`, `team-materialize-workspaces`, `team-write-boundaries`, `team-create-branch`, and `team-validate-workspaces`.
            Environment Mutation Subcommands: `env-install-packages`, `env-update-packages`, and `env-remove-packages`.
            Environment Verification Subcommands: `env-verify-topic`, `env-verify-actors`, and `env-verify-agents`.
            Reset Subcommands: `reset-plan`, `reset-inspect`, and `reset-apply`.

            Use {subcommand_links}.

            ## Required Terms

{skill_terms}

            {OUTPUT_CONTRACT_FIXTURE}
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(root / "skillset" / "operator" / "isomer-op-topic-mgr" / "SKILL.md", skill_text)
        write(
            root / "skillset" / "operator" / "isomer-op-topic-mgr" / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-op-topic-mgr"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-op-topic-mgr to validate this fixture."
            """,
        )
        for subcommand_name in validator.TOPIC_MANAGER_SUBCOMMANDS:
            if subcommand_name == omit_subcommand:
                continue
            if subcommand_name == "help.md":
                write(
                    root / "skillset" / "operator" / "isomer-op-topic-mgr" / "references" / subcommand_name,
                    """
                    # Help

                    ## Workflow

                    1. Print the public subcommands and blocker guidance.

                    If the user's task does not map cleanly to these steps, use your native planning tool.

                    ## Public Subcommands

                    | Subcommand | Purpose | Produces |
                    | --- | --- | --- |
                    | `status` | Inspect initialized topic state. | `semantic_paths`, Topic Manager evidence, read-only blocker report. |
                    | `doctor` | Run diagnostic checks. | diagnostic storage diagnostics and retired-skill blockers. |
                    | `help` | Print usage. | Help output and blocker guidance. |
                    | `storage-resolve` | Resolve Project context. | `semantic_paths`, `topic.repos.main`, `agent.workspace`. |
                    | `storage-inspect-main` | Inspect main repo. | Repo readiness and blocker state. |
                    | `storage-validate` | Validate storage labels. | Storage validation blockers. |
                    | `storage-register-repo` | Register a topic repo. | `topic.repos.*`, `storage_profile`, `project repos create`, and `project paths register`. |
                    | `actors-manage` | Manage Topic Actors. | `topic.actors.workspace` and actor blockers. |
                    | `actors-materialize` | Materialize actors. | Topic Actor workspace blockers. |
                    | `actors-diagnose` | Diagnose actor readiness. | Actor diagnostic blockers. |
                    | `team-plan` | Plan agents. | Agent workspace path-source blockers. |
                    | `team-materialize-workspaces` | Materialize team workspaces. | Worktree readiness blockers. |
                    | `team-write-boundaries` | Write boundaries. | Boundary paths and blocker state. |
                    | `team-create-branch` | Create branch. | Branch result and blockers. |
                    | `team-validate-workspaces` | Validate workspaces. | Validation status and blockers. |
                    | `env-install-packages` | Install packages. | Pixi install plan and blockers. |
                    | `env-update-packages` | Update packages. | Pixi update plan and blockers. |
                    | `env-remove-packages` | Remove packages. | Pixi removal plan and blockers. |
                    | `env-verify-topic` | Verify topic env. | Service evidence and blockers. |
                    | `env-verify-actors` | Verify actor env. | Actor cwd readiness blockers. |
                    | `env-verify-agents` | Verify agent env. | Service evidence and blockers. |
                    | `reset-plan` | Plan reset. | Reset plan blockers. |
                    | `reset-inspect` | Inspect reset. | Reset checkpoint blockers. |
                    | `reset-apply` | Apply reset. | Reset outcome blockers. |
                    """,
                )
                continue
            fallback = "" if omit_subcommand_fallback and subcommand_name == "team-plan.md" else "If the user's task does not map cleanly to these steps, use your native planning tool."
            extra_terms = " ".join(validator.TOPIC_MANAGER_SEMANTIC_REFERENCE_REQUIRED_TERMS.get(subcommand_name, ()))
            write(
                root / "skillset" / "operator" / "isomer-op-topic-mgr" / "references" / subcommand_name,
                f"""
                # {subcommand_name}

                ## Workflow

                1. Run the fixture step and report any blocker.

                {fallback}
                {extra_terms}
                """,
            )

    def write_welcome_skill(
        self,
        root: Path,
        *,
        omit_skill_term: str | None = None,
        omit_reference_term: str | None = None,
        omit_direct_owner: str | None = None,
        active_retired_route: bool = False,
        automatic_tool_pack_route: bool = False,
    ) -> None:
        skill_dir = root / "skillset" / "operator" / "isomer-op-welcome"
        skill_text = """
            ---
            name: isomer-op-welcome
            description: Manual invocation only; use when an Isomer Labs Project Operator Session needs welcome routing and visible usage paths.
            ---

            # Isomer Admin Welcome

            ## Overview

            Manual invocation only. This fixture shows the action-oriented welcome menu and keeps mutation inside owner skills.

            ## When to Use

            Use this skill for Isomer Labs option menus, path choice, visible usage paths, and read-only next-step recommendations.

            ## Workflow

            1. **Handle the default**. Select `show-options`.
            2. **Select one subcommand** from the table.
            3. **Load the selected reference** and follow its workflow.
            4. **Preserve the read-only boundary** and route mutation to the owner.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            These routines are peers. Manual or Agent Team is execution topology; DeepSci or Kaoju is research paradigm.

            | Subcommand | Kind | Use For | Owner or Safe Next Route | Detail |
            | --- | --- | --- | --- | --- |
            | `start-research-manually` | Topology | Manual research. | `Use $isomer-op-topic-creator fast-forward`. | [references/start-research-manually.md](references/start-research-manually.md) |
            | `start-research-by-agent-team` | Topology | Team research. | `Use $isomer-op-topic-team-specialize fast-forward`. | [references/start-research-by-agent-team.md](references/start-research-by-agent-team.md) |
            | `start-deepsci-research` | Paradigm | Hypothesis research. | `Use $isomer-op-entrypoint` with the goal. | [references/start-deepsci-research.md](references/start-deepsci-research.md) |
            | `start-kaoju-survey` | Paradigm | Evidence-led survey. | `Use $isomer-op-entrypoint` with the goal. | [references/start-kaoju-survey.md](references/start-kaoju-survey.md) |
            | `show-options` | Discovery | Options. | Read-only. | [references/show-options.md](references/show-options.md) |
            | `show-extensions` | Discovery | Extension options. | `Use $isomer-op-system-skill-mgr`. | [references/show-extensions.md](references/show-extensions.md) |
            | `choose-path` | Routing | Path choice. | Read-only. | [references/choose-path.md](references/choose-path.md) |
            | `show-skill-map` | Discovery | Skill map. | Read-only. | [references/show-skill-map.md](references/show-skill-map.md) |
            | `next-step` | Routing | Read-only next step. | Read-only. | [references/next-step.md](references/next-step.md) |
            | `help` | Support | Help. | Read-only. | [references/help.md](references/help.md) |

            ## Output Contract

            Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

            ### Essential Output

            Explain naturally how you understood the user's goal, then recommend the visible workflow and active owner skill. Provide the safe first invocation, name any missing context that blocks progress, and state the next action.

            ### Complete Output

            Group the complete explanation by context evidence, read-only commands, alternate owner workflows, routing rationale, and retired routes.

            ## Guardrails

            The skill is read-only and uses `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, `isomer-cli project context show`, `isomer-cli system-skills extensions list`, and `isomer-cli project system-extensions list` only for inspection.
            Route concrete tasks to `isomer-op-entrypoint`, extension work to `isomer-op-system-skill-mgr`, Project checks to `isomer-op-project-mgr`, Project Web GUI work to `isomer-op-gui-mgr`, identity work to `isomer-op-switch-identity`, Toolbox work to `isomer-op-toolbox-mgr`, topic creation to `isomer-op-topic-creator`, initialized-topic work to `isomer-op-topic-mgr`, and Topic Team work to `isomer-op-topic-team-specialize`. Route bounded Houmao adapter support through the owning operator workflow to `isomer-srv-houmao-interop`; service skills are not first-click owner routes.
            DeepSci uses `isomer-ext-deepsci-entrypoint`; Kaoju uses `isomer-ext-kaoju-entrypoint`. Distinguish `catalog-known`, Project-declared, and host-usable extension evidence. Manual versus Agent Team is execution topology; DeepSci versus Kaoju is research paradigm. The `isomer-cli ext` namespace does not install system-skill extensions.
            Do not ask users or agents to invoke `isomer-op-topic-workspace-mgr`, `isomer-op-topic-prepare`, or `isomer-op-manual-research-session`; they are retired.
            Do not automatically route to `isomer-misc-tool-packs`; mention `isomer-misc-tool-packs` only as a manual skill when explicitly relevant.
            Route Topic Team Specialization only for an explicit invocation or a formal Agent Team target established by the prompt or authoritative context. A generic topic preparation request, launch-facing language, readiness gaps, missing summaries, and missing Agent Workspaces do not establish that target.

            ## Chat Response

            Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(skill_dir / "SKILL.md", skill_text)
        write(
            skill_dir / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-op-welcome"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-op-welcome show-options to validate this fixture."
            policy:
              allow_implicit_invocation: false
            """,
        )
        reference_texts = {
            "help.md": """
                # Help

                ## Workflow

                1. List usage paths and owner routes.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                | Subcommand | Purpose | Produces |
                | --- | --- | --- |
                | `start-research-manually` | Manual research. | Owner route. |
                | `start-research-by-agent-team` | Agent Team research. | Owner route. |
                | `start-deepsci-research` | Hypothesis research. | `isomer-ext-deepsci-entrypoint`. |
                | `start-kaoju-survey` | Evidence-led survey. | `isomer-ext-kaoju-entrypoint`. |
                | `isomer-op-entrypoint` | Concrete route and proceed. | Owner route. |
                | `isomer-op-system-skill-mgr` | Extension lifecycle. | Owner route. |
                | `isomer-op-gui-mgr` | Project Web GUI lifecycle and backend API reference. | Owner route. |
                | `show-options` | Options. | Menu. |
                | `show-extensions` | Extensions. | Read-only extension state. |
                | `choose-path` | Choose. | Recommendation. |
                | `show-skill-map` | Map. | Map. |
                | `next-step` | Next step. | Read-only recommendation. |
            """,
            "show-options.md": """
                # Show Options

                ## Workflow

                1. Print visible usage paths first and invite the user to invoke the named owner skill directly.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                `start-deepsci-research` uses `isomer-ext-deepsci-entrypoint`; `start-kaoju-survey` uses `isomer-ext-kaoju-entrypoint`. Use `isomer-op-system-skill-mgr` for extension lifecycle and Use $isomer-op-entrypoint for a concrete task. Manual or Agent Team is execution topology; DeepSci or Kaoju is research paradigm.

                Project setup or checks, Project Web GUI work with `isomer-op-gui-mgr`, Research Topic setup, Topic Team work, and Houmao support all name owner workflows.
            """,
            "show-extensions.md": """
                # Show Extensions

                ## Workflow

                1. Run `isomer-cli --print-json system-skills extensions list`, `isomer-cli --print-json system-skills extensions show <extension-id>`, and `isomer-cli --print-json project system-extensions list` when useful.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                Distinguish `catalog-known`, Project-declared, and Host-usable evidence. Route lifecycle work to `isomer-op-system-skill-mgr`; Use $isomer-op-entrypoint for concrete work. DeepSci uses `isomer-ext-deepsci-entrypoint`, Kaoju uses `isomer-ext-kaoju-entrypoint`, and `isomer-cli ext` is a runtime namespace.
            """,
            "choose-path.md": """
                # Choose Path

                ## Workflow

                1. Interpret manual research or Domain Agent Team Template intent, then compare `start-deepsci-research` and `start-kaoju-survey` when a research paradigm applies.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                It recommends visible paths. Use this command to recommend the visible workflow, route extensions to `isomer-op-system-skill-mgr`, concrete tasks to `isomer-op-entrypoint`, and GUI questions to `isomer-op-gui-mgr`, explain how it understood the goal, distinguish execution topology from research paradigm, name the owner skill and safe first invocation, report blockers, and state the next action.
            """,
            "show-skill-map.md": """
                # Show Skill Map

                ## Workflow

                1. Print Direct Invocation guidance.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                Use $isomer-op-entrypoint, Use $isomer-op-project-mgr, Use $isomer-op-system-skill-mgr, Use $isomer-op-gui-mgr, Use $isomer-op-switch-identity, Use $isomer-op-toolbox-mgr, Use $isomer-op-topic-creator, Use $isomer-op-topic-mgr, and Use $isomer-op-topic-team-specialize. Route bounded support to `isomer-srv-houmao-interop`; service skills are not first-click owner routes.
            """,
            "next-step.md": """
                # Next Step

                ## Workflow

                1. Run read-only Project inspection only.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                Use `isomer-cli project validate`, `isomer-cli doctor`, `isomer-cli project topics list`, `isomer-cli project context show`, `isomer-cli project self show`, `isomer-cli project outputs policy`, `isomer-cli system-skills extensions list`, and `isomer-cli project system-extensions list`. Route extension evidence to `isomer-op-system-skill-mgr`; Use $isomer-op-entrypoint for a concrete task. Do not run mutating commands.
            """,
            "start-research-manually.md": """
                # Start Research Manually

                ## Workflow

                1. Recommend human-orchestrated research through `isomer-op-topic-creator`.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                Use $isomer-op-topic-creator fast-forward or Use $isomer-op-topic-creator step-by-step. Treat research paradigm as a separate choice. Report the mutation boundary.
            """,
            "start-research-by-agent-team.md": """
                # Start Research by Agent Team

                ## Workflow

                1. Recommend Domain Agent Team Template specialization through `isomer-op-topic-team-specialize`.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                Use $isomer-op-topic-team-specialize fast-forward. Treat research paradigm as a separate choice. Report the mutation boundary and route Houmao questions to bounded service support through `isomer-srv-houmao-interop`.
            """,
            "start-deepsci-research.md": """
                # Start DeepSci Research

                ## Workflow

                1. Recommend hypothesis-driven production research through `isomer-ext-deepsci-entrypoint` while preserving execution topology as a separate choice.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                Use $isomer-op-entrypoint when readiness is unclear. Route extension state to `isomer-op-system-skill-mgr` and bootstrap to `isomer-ext-deepsci-entrypoint->workspace`.

                ## Mutation Boundary

                This path does not run research or mutate state.
            """,
            "start-kaoju-survey.md": """
                # Start Kaoju Survey

                ## Workflow

                1. Recommend an evidence-led survey through `isomer-ext-kaoju-entrypoint` while preserving execution topology as a separate choice.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                Use $isomer-op-entrypoint when readiness is unclear. Route extension state to `isomer-op-system-skill-mgr` and readiness to `isomer-ext-kaoju-entrypoint->workspace`.

                ## Mutation Boundary

                This path does not run research or mutate state.
            """,
        }
        for reference_name, reference_text in reference_texts.items():
            if omit_reference_term is not None:
                reference_text = reference_text.replace(omit_reference_term, "")
            if omit_direct_owner is not None:
                reference_text = reference_text.replace(f"Use ${omit_direct_owner}", f"Use {omit_direct_owner}")
            write(skill_dir / "references" / reference_name, reference_text)
        if active_retired_route:
            help_path = skill_dir / "references" / "help.md"
            help_path.write_text(help_path.read_text(encoding="utf-8") + "\nInvoke `isomer-op-topic-prepare` as an active route.\n", encoding="utf-8")
        if automatic_tool_pack_route:
            help_path = skill_dir / "references" / "help.md"
            help_path.write_text(help_path.read_text(encoding="utf-8") + "\nUse `isomer-misc-tool-packs` for tool setup.\n", encoding="utf-8")

    def write_entrypoint_skill(
        self,
        root: Path,
        *,
        omit_skill_term: str | None = None,
        omit_reference_term: str | None = None,
        service_first_click: bool = False,
        active_retired_route: bool = False,
    ) -> None:
        skill_dir = root / "skillset" / "operator" / "isomer-op-entrypoint"
        reference_links = "\n            ".join(f"- [references/{name}](references/{name})" for name in validator.ENTRYPOINT_REFERENCES)
        skill_text = f"""
            ---
            name: isomer-op-entrypoint
            description: Use when a Project Operator needs an informed-user entrypoint to route a concrete prompt, file, extension request, system skill request, or Isomer CLI need and proceed.
            ---

            # Isomer Operator Entrypoint

            ## Overview

            This skill routes informed user tasks across system skills and Isomer CLI functionality.

            ## When to Use

            Use it for route-and-proceed dispatch. Use `isomer-op-welcome` for read-only orientation.

            ## Workflow

            1. Parse the task input.
            2. Run safe read-only context discovery.
            3. Classify exactly one route.
            4. Establish formal Agent Team intent before specialization.
            5. Check owner boundaries because service skills are only bounded support.
            6. Preflight target prerequisites before target mutation.
            7. Route prerequisite recovery with run-to-target, next-prerequisite-only, alternate-route, and stop choices. After explicit authorization, use the native planning tool.
            8. Proceed with the selected route while preserving separate mutation, Run, checkpoint, Gate, and terminal-report boundaries across owners.
            9. Stop at each nondelegable boundary.
            10. Report the entrypoint result.

            If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step routing plan, then execute the plan.

            ## Reference Pages

            {reference_links}

            ## Output Contract

            Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

            ### Essential Output

            Lead with the routing and execution outcome. Explain how you understood the goal, name the selected route and material context, summarize changes, and state blockers and the next action.

            ### Complete Output

            Group the complete explanation by routing alternatives and rationale, commands and selected context, extension readiness, service delegation, and retired routes excluded from consideration.

            ## Guardrails

            - MUST route through `isomer-op-welcome`, `isomer-op-project-mgr`, `isomer-op-system-skill-mgr`, `isomer-op-gui-mgr`, `isomer-op-switch-identity`, `isomer-op-topic-creator`, `isomer-op-topic-mgr`, and `isomer-op-topic-team-specialize`. Service skills are only bounded support unless explicitly invoked. `isomer-misc-tool-packs` is used explicitly, not automatically.
            - MUST select Topic Team Specialization only for an explicit invocation or a formal Agent Team target established by the prompt or authoritative context. A generic topic preparation request, launch-facing language, readiness gaps, missing summaries, and missing Agent Workspaces do not establish that target.
            - DO NOT stop after only listing routes when the task is concrete.

            ## Chat Response

            Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(skill_dir / "SKILL.md", skill_text)
        write(
            skill_dir / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-op-entrypoint"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-op-entrypoint to validate this fixture."
            """,
        )
        reference_texts = {
            "input-surfaces.md": """
                # Input Surfaces

                ## Workflow

                1. Resolve explicit skill name, CLI command, file path, Project root, Research Topic, Topic Actor, Agent, Domain Agent Team Template, and DeepSci stage.

                If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
            "routing-rules.md": """
                # Routing Rules

                ## Workflow

                1. Proceed for concrete tasks.
                2. Use read-only discovery.
                3. Select one route and preserve owner boundaries.
                4. Remember Service skills are only bounded support.
                5. Retired compatibility skills are not active routes.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                ## Topic Team Specialization Examples

                | Request or Context | Route |
                | --- | --- |
                | `prepare the topic <topic-name>` with no formal Agent Team target | `isomer-op-topic-creator` |
                | Deploy or use a contextually selected formal Agent Team | `isomer-op-topic-team-specialize` |
            """,
            "prerequisite-recovery.md": """
                # Prerequisite Recovery

                ## Workflow

                1. Preflight the target before mutation.
                2. Present Run to the target, Execute the next prerequisite only, Inspect or choose another route, and Stop choices for an ordinary `do <task>` request.
                3. Use the native planning tool for explicit run-to authorization.
                4. Use `paused` for a known producer and Use `blocked` for unavailable external state.
                5. Invoke each owner separately across owner routes, preserve separate Research Tasks, Runs, terminal reports and stop at Nondelegable Boundaries.

                If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
            "system-skill-index.md": """
                # System Skill Index

                ## Workflow

                1. Choose Operator Skills, Service Skills, or Misc Skills.
                2. Keep services not a normal first-click owner route.
                3. Keep `isomer-misc-tool-packs` explicit and not automatic package mutation.
                4. Route through `isomer-op-entrypoint`.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                `isomer-op-welcome`, `isomer-op-project-mgr`, `isomer-op-system-skill-mgr`, `isomer-op-gui-mgr`, `isomer-op-switch-identity`, `isomer-op-topic-creator`, `isomer-op-topic-mgr`, `isomer-op-topic-team-specialize`, `isomer-op-entrypoint`.
                `isomer-srv-topic-env-setup`, `isomer-srv-agent-env-setup`, `isomer-srv-houmao-interop`, `isomer-srv-resolve-pkg-repo`, `isomer-srv-topic-service-agent-support`.
                `isomer-misc-tool-packs` is explicitly requested.
            """,
            "extension-skill-index.md": f"""
                # Extension Skill Index

                ## Workflow

                1. Use DeepSci Bootstrap and Pipeline when readiness or pass execution is requested.
                2. Use DeepSci Core Research Loop for research stages.
                3. Use DeepSci Writing and Companion Skills for paper work.
                4. Preserve latest-context preflight and worker-output policy.
                5. Do not let ordinary DeepSci research-stage skills fabricate missing readiness.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                {" ".join(validator.ENTRYPOINT_DEEPSCI_SKILLS)}
            """,
            "cli-index.md": f"""
                # CLI Index

                ## Workflow

                1. Use Safe Discovery Commands.
                2. Use Project and Topic Command Families.
                3. Use Research Records and Artifact Formats.
                4. Use Team and Handoff Command Families.
                5. Do not hand-edit research record indexes.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                {" ".join(validator.ENTRYPOINT_CLI_TERMS)}
            """,
        }
        for reference_name, reference_text in reference_texts.items():
            if omit_reference_term is not None:
                reference_text = reference_text.replace(omit_reference_term, "")
            extra = ""
            if service_first_click and reference_name == "system-skill-index.md":
                extra += "\nUse `isomer-srv-topic-env-setup` as a first-click owner route.\n"
            if active_retired_route and reference_name == "routing-rules.md":
                extra += "\nUse `isomer-op-topic-prepare` as an active route.\n"
            write(skill_dir / "references" / reference_name, reference_text + extra)

    def write_switch_identity_skill(
        self,
        root: Path,
        *,
        omit_command: str | None = None,
        omit_skill_term: str | None = None,
        omit_command_term: str | None = None,
        active_directory_scanning: bool = False,
        active_fabricated_claim: bool = False,
    ) -> None:
        skill_dir = root / "skillset" / "operator" / "isomer-op-switch-identity"
        command_links = ", ".join(f"`commands/{command_name}`" for command_name in validator.SWITCH_IDENTITY_COMMANDS)
        skill_text = f"""
            ---
            name: isomer-op-switch-identity
            description: Use when a Project Operator needs to switch identity posture to a selected Topic Actor or Agent workspace cwd.
            ---

            # Isomer Operator Switch Identity

            ## Overview

            Use when switching identity posture for a Topic Actor or Agent. Resolve `topic.actors.workspace`, `agent.workspace`, and the resolved cwd through `isomer-cli --print-json project paths get topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>` or `isomer-cli --print-json project paths get agent.workspace --topic <topic> --agent <agent-name>`.

            ## When to Use

            Use this for `act-as`, one-task, persistent, status, and reset work. The Project Operator acted as or on behalf of the selected identity and must avoid OS-level impersonation, launched Agent Instance claims, Houmao launch claims, and Execution Adapter claims.

            ## Workflow

            1. Select `switch`, `act-as`, `status`, `reset`, or `help`.
            2. Resolve target kind and name for a Topic Actor or Agent.
            3. Use semantic path resolution and do not infer a target by scanning workspace directories.
            4. Use one-task mode by default, persistent mode only when explicit, and restore after one-prompt `act-as`.
            5. Run from cwd and preserve provenance.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Commands

            Use {command_links}.

            ## Guardrails

            - DO NOT infer a target by scanning workspace directories.
            - DO NOT use the Project root, Topic Workspace root, or `topic.repos.main` as the default switched cwd.

            {OUTPUT_CONTRACT_FIXTURE}
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(skill_dir / "SKILL.md", skill_text)
        write(
            skill_dir / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-op-switch-identity"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-op-switch-identity help to validate this fixture."
            """,
        )
        command_terms = {
            "switch.md": "target kind target name one-task persistent isomer-cli --print-json project paths get topic.actors.workspace isomer-cli --print-json project paths get agent.workspace resolved `topic.actors.workspace` or `agent.workspace`. DO NOT infer the target by scanning workspace directories.",
            "act-as.md": "following prompt. Save the previous Project Operator identity posture. Restore the previous Project Operator identity posture. temporary one-time execution. DO NOT leave a switched posture active. resolved `topic.actors.workspace` or `agent.workspace`.",
            "status.md": "persistent temporary unknown re-resolve before running commands target workspace cwd normal Project Operator cwd.",
            "reset.md": "Clear the active switched posture. normal Project Operator identity. future commands no longer default. does not delete workspace files.",
            "help.md": "| Command | Purpose | Produces |; | --- | --- | --- |; `switch` `act-as` `status` `reset` one-prompt restore cwd discipline.",
        }
        for command_name in validator.SWITCH_IDENTITY_COMMANDS:
            if command_name == omit_command:
                continue
            terms = command_terms[command_name]
            if omit_command_term is not None:
                terms = terms.replace(omit_command_term, "")
            extra = ""
            if active_directory_scanning and command_name == "switch.md":
                extra += "\nInfer the target by scanning workspace directories.\n"
            if active_fabricated_claim and command_name == "act-as.md":
                extra += "\nClaim launched Agent Instance execution and Houmao launch produced the work.\n"
            write(
                skill_dir / "commands" / command_name,
                f"""
                # {command_name}

                ## Workflow

                1. Run the command fixture step.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                {terms}
                {extra}
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

    def write_topic_env_setup_service(
        self,
        root: Path,
        *,
        omit_skill_term: str | None = None,
        omit_reference_term: str | None = None,
        include_legacy_folder: bool = False,
    ) -> None:
        skill_dir = root / "skillset" / "service" / "isomer-srv-topic-env-setup"
        subcommand_links = ", ".join(
            f"`references/{subcommand_name}`" for subcommand_name in validator.TOPIC_ENV_SETUP_SUBCOMMANDS
        )
        skill_text = f"""
            ---
            name: isomer-srv-topic-env-setup
            description: Valid fixture topic env setup service.
            ---

            # Isomer Service Topic Environment Setup

            Topic environment setup is independent of Topic Agent Team structure.
            A single capable agent or operator uses this skill to prepare the Topic Workspace environment.
            DO NOT require or inspect Topic Agent Team Profile material, team-profile material, roles, or agent count.

            ## Workflow

            1. Select one subcommand and report blockers.

            ## Subcommands

            Procedural Subcommands: `resolve-topic-workspace`, `read-env-gate`, `derive-env-gate`, `ensure-topic-main-repository`, `ensure-topic-repos`, `project-extern-repos`, `install-topic-deps`, and `verify-env-gate`.

            Misc Subcommands: `setup-topic-env` and `help`.

            Use {subcommand_links}.

            Commands include `pixi run --manifest-path <manifest_path> --environment <pixi_environment>`, `pixi add --manifest-path <manifest_path>`, and `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`.
            Use `.isomer-user-env/` only as fallback and block sudo.
            Report `semantic_paths` for `topic.workspace`, `topic.repos.main`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.records`, `topic.runtime`, `topic.intent.topic_env_requirements`, and `topic.env.topic_setup_target_spec`; accept an explicit manual target spec; produce Topic Workspace predecessor evidence, Topic Main Development Repository Git state, external repo projection evidence, and `per_agent_readiness_status` when per-agent readiness is not checked. Resolve the appropriate topic repository label before creating repos.
            Use bounded real-path verification for source-intent paths classified as `heavy` or `unknown-risk`. Consult `isomer-misc-bounded-run-tips`, record `operation_classification`, classification source, classification result, and generic best-effort judgment only when no recipe applies. A generic smoke test is allowed only as supporting evidence.

            {OUTPUT_CONTRACT_FIXTURE}
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(skill_dir / "SKILL.md", skill_text)
        write(
            skill_dir / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-srv-topic-env-setup"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-srv-topic-env-setup to validate this fixture."
            """,
        )
        reference_terms = {
            "resolve-topic-workspace.md": "Do not block solely because `<topic-workspace>/team-profile/`; diagnostics are non-blocking for this subcommand unless they break env setup. Report `semantic_paths`, `topic.repos.main`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.records`, `topic.runtime`, `topic.intent.topic_env_requirements`, `topic.env.topic_setup_target_spec`, and each path source.",
            "ensure-topic-main-repository.md": "Prepare the Topic Main Development Repository at `topic.repos.main` as a normal non-bare repo, with `topic.repos.main.isomer_managed`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, and `topic.repos.main.projections.manifest`. Route root `AGENTS.md` and `CLAUDE.md` guidance mutation through `isomer-cli --print-json project topic-main-guidance ensure --topic <topic> --yes`, use `isomer-cli --print-json project topic-main-guidance inspect --topic <topic>` for checks, and use `isomer-cli project topic-main-guidance render` for rendering. Treat `isomer-labs-topic-main-guidance.v1.md.j2` as the `.j2` canonical large-text template asset, must not duplicate the full rendered prose, and report guidance block version.",
            "ensure-topic-repos.md": "Use resolved non-main `topic.repos.*` paths from `semantic_paths`; report semantic label, path, and path source. Query `project paths default`, run user-supplied or agent-selected commands outside Isomer, verify source and immutable identity before registration, then call `project repos register`. The external caller owns partial content. Keep existing canonical external repos read-only by default. Do not place task repos outside the resolved semantic path, and default helper-created repos under `repos/extern/...`.",
            "project-extern-repos.md": "Create external repo projection entries under `topic.repos.main.projections.readonly` or `topic.repos.main.projections.writable`, track metadata in `topic.repos.main.projections.manifest`, and distinguish read-only projections from writable projections.",
            "read-env-gate.md": "Resolve and read `topic.intent.topic_env_requirements`. Interpret the runnable target as what one agent or operator must run.",
            "derive-env-gate.md": "Write `topic.env.topic_setup_target_spec` or validate an explicit manual target spec. Include `## Gate Checklist`, `- [ ]`, and `- [x]`. Define the required readiness work contract with a pass condition, evidence source, optional diagnostics outside the checklist, and blocker condition. Preserve every source-intent runnable target and use bounded real-path verification; consult `isomer-misc-bounded-run-tips`, record `classification_source`, `classification_result`, `classification_reason`, `resource_dimensions`, `unknown-risk`, the bounded-run guidance source, and use generic best-effort judgment only when no recipe applies. A simple smoke test that misses the source path is insufficient unless the user explicitly records a downgrade. Consult `isomer-misc-pkg-specifics` before generic package routing and record `no package-specific rule` when no page exists.",
            "install-topic-deps.md": "Read `topic.env.topic_setup_target_spec` and require enclosure strategy plus classification evidence, `unknown-risk`, bounded-run guidance source, generic best-effort fallback evidence when used, and bounded real setup path decisions. Use `isomer-misc-pkg-specifics` evidence or `no package-specific rule` from the target spec before package mutation.",
            "setup-topic-env.md": "DO NOT require `team-profile/` before running this setup chain. Require `semantic_paths`, `topic.repos.main`, `ensure-topic-main-repository`, `project-extern-repos`, `AGENTS.md`, `CLAUDE.md`, agent guidance posture, guidance block version, `topic.tmp`, and resolved `topic.tmp`; tmp material is local, ignored, disposable, not shared, and not durable evidence. State naturally that per-Agent readiness was not checked and Do not read `topic.intent.agent_env_requirements`. Use bounded real-path verification; a generic smoke test is not enough.",
            "verify-env-gate.md": "DO NOT require or verify `team-profile/` before reporting environment readiness. per-Agent Workspace cwd verification is not checked here. Report Topic Workspace predecessor evidence, Topic Main Development Repository evidence, projection evidence, bounded real-path coverage, operation classification evidence, `unknown-risk`, bounded-run guidance source, generic best-effort fallback evidence when used, source-intent runnable target coverage, every required `## Gate Checklist` item checked with supporting evidence, the exact checklist item when blocked, failed, or not checked, any weaker smoke test limitation, any user downgrade, `isomer-misc-pkg-specifics`, and `no package-specific rule`.",
        }
        for subcommand_name in validator.TOPIC_ENV_SETUP_SUBCOMMANDS:
            term = reference_terms.get(subcommand_name, "Topic Workspace environment setup reference.")
            if omit_reference_term is not None:
                term = term.replace(omit_reference_term, "")
            write(
                skill_dir / "references" / subcommand_name,
                f"""
                # {subcommand_name}

                ## Workflow

                1. Run the service fixture step.

                {term}
                """,
            )
        if include_legacy_folder:
            write(
                root / "skillset" / "service" / "isomer-srv-env-setup" / "SKILL.md",
                """
                ---
                name: isomer-srv-env-setup
                description: Legacy fixture.
                ---

                # Legacy
                """,
            )

    def write_package_specifics_skill(self, root: Path, *, omit_term: str | None = None) -> None:
        skill_text = """
            ---
            name: isomer-misc-pkg-specifics
            description: Valid fixture package specifics skill.
            ---

            # Isomer Misc Package Specifics

            ## Overview

            - **First lookup**: operational env gate derivation, package mutation, and package-specific runtime verification callers check this skill before applying generic package rules.

            ## When to Use

            Use this skill before applying a generic PyPI, Conda, local-package, or system-Python source ladder.

            ## Workflow

            1. Select a package page.
            2. Report `no package-specific rule` when no package page exists.
            3. Report selected source or unresolved source, required variant, verification expectation, warnings, and blockers.

            Do not replace generic Pixi mechanics, package-source reachability checks, bounded-run classification, env gate writing, or final readiness reporting.
            """
        if omit_term is not None:
            skill_text = skill_text.replace(omit_term, "")
        write(root / "skillset" / "misc" / "isomer-misc-pkg-specifics" / "SKILL.md", skill_text)
        write(
            root / "skillset" / "misc" / "isomer-misc-pkg-specifics" / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-misc-pkg-specifics"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-misc-pkg-specifics to validate this fixture."
            """,
        )
        write(
            root / "skillset" / "misc" / "isomer-misc-pkg-specifics" / "references" / "pytorch.md",
            """
            # PyTorch

            Package source evidence, variant evidence, verification expectation, and blocker guidance.
            """,
        )

    def write_agent_env_setup_service(
        self,
        root: Path,
        *,
        omit_skill_term: str | None = None,
        omit_reference_term: str | None = None,
        omit_subcommand: str | None = None,
    ) -> None:
        skill_dir = root / "skillset" / "service" / "isomer-srv-agent-env-setup"
        subcommand_links = ", ".join(
            f"`references/{subcommand_name}`" for subcommand_name in validator.AGENT_ENV_SETUP_SUBCOMMANDS
        )
        skill_text = f"""
            ---
            name: isomer-srv-agent-env-setup
            description: Valid fixture agent env setup service.
            ---

            # Isomer Service Agent Environment Setup

            ## Workflow

            1. Select one subcommand and report blockers.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            Procedural Subcommands: `resolve-agent-env-context`, `require-topic-env-ready`, `read-agent-env-gate`, `plan-agent-workspaces`, `derive-agent-env-gate`, `require-topic-main-ready`, `create-agent-worktrees`, and `verify-agent-env-gate`.

            Misc Subcommands: `setup-agent-env` and `help`.

            Use {subcommand_links}.

            This fixture reads `topic.intent.agent_env_requirements`, writes or validates `topic.env.agent_setup_target_spec`, accepts an explicit manual target spec, consumes `topic.env.topic_setup_target_spec`, requires prepared Topic Main Development Repository and projection predecessor evidence at `topic.repos.main`, uses authoritative Agent Names, resolves `agent.workspace`, runs `pixi run --manifest-path <manifest_path> --environment <pixi_environment>`, records selected-agent partial evidence, Service Request refs, Provenance refs, and `overall_readiness_status`.
            Use bounded real-path verification for cwd commands classified as `heavy` or `unknown-risk`. Consult `isomer-misc-bounded-run-tips`, record `operation_classification`, classification source, classification result, and generic best-effort judgment only when no recipe applies. A generic smoke test is only supporting evidence.

            DO NOT initialize, repair, or configure the Topic Main Development Repository. DO NOT create per-agent Pixi manifests. DO NOT install or mutate Topic Workspace dependencies. Do not create Agent Instances or mutate Workspace Runtime records.

            {OUTPUT_CONTRACT_FIXTURE}
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(skill_dir / "SKILL.md", skill_text)
        write(
            skill_dir / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-srv-agent-env-setup"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-srv-agent-env-setup to validate this fixture."
            """,
        )
        for subcommand_name in validator.AGENT_ENV_SETUP_SUBCOMMANDS:
            if subcommand_name == omit_subcommand:
                continue
            terms = "\n".join(validator.AGENT_ENV_SETUP_REFERENCE_REQUIRED_TERMS.get(subcommand_name, ()))
            if omit_reference_term is not None:
                terms = terms.replace(omit_reference_term, "")
            write(
                skill_dir / "references" / subcommand_name,
                f"""
                # {subcommand_name}

                ## Required Inputs

                Fixture inputs.

                ## Workflow

                1. Run the service fixture step.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                {terms}
                """,
            )
        self.write_houmao_interop_service(root)

    def write_houmao_interop_service(
        self,
        root: Path,
        *,
        omit_skill_term: str | None = None,
        omit_reference_term: str | None = None,
        omit_subcommand: str | None = None,
        include_legacy_operator_folder: bool = False,
    ) -> None:
        skill_dir = root / "skillset" / "service" / "isomer-srv-houmao-interop"
        subcommand_links = ", ".join(
            f"`references/{subcommand_name}`" for subcommand_name in validator.HOUMAO_INTEROP_SERVICE_SUBCOMMANDS
        )
        skill_text = f"""
            ---
            name: isomer-srv-houmao-interop
            description: Valid fixture Houmao interop service.
            ---

            # Isomer Service Houmao Interop

            Use this skill as bounded Service Team support for Houmao adapter questions from a Project Operator Session, Operator Agent, Topic Service Agent, Topic Service Master, or Service Request.

            ## Workflow

            1. **Default help mode**: If invoked without a prompt, run `help`.
            2. **Explain-loop mode**: Explain the Houmao loop.
            3. **Customize-loop mode**: Identify adapter customization points.
            4. **Map-template mode**: Map Domain Agent Team Templates onto Houmao concepts.
            5. **Inspect-runtime mode**: Inspect runtime state.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            Use {subcommand_links}.

            Route user-facing Project lifecycle back to `isomer-op-project-mgr` and Topic Team Specialization back to `isomer-op-topic-team-specialize`. Include `next_action` in output.

            {OUTPUT_CONTRACT_FIXTURE}

            ## Guardrails

            DO NOT own Project lifecycle, Research Topic creation, Topic Team Specialization, approval provenance, Agent Team Instance launch orchestration, Gate decisions, Research Claims, or research task routing.
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(skill_dir / "SKILL.md", skill_text)
        write(
            skill_dir / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-srv-houmao-interop"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-srv-houmao-interop to validate this fixture."
            """,
        )
        for subcommand_name in validator.HOUMAO_INTEROP_SERVICE_SUBCOMMANDS:
            if subcommand_name == omit_subcommand:
                continue
            terms = "\n".join(validator.HOUMAO_INTEROP_SERVICE_REFERENCE_REQUIRED_TERMS.get(subcommand_name, ()))
            if omit_reference_term is not None:
                terms = terms.replace(omit_reference_term, "")
            write(
                skill_dir / "references" / subcommand_name,
                f"""
                # {subcommand_name}

                ## Workflow

                1. Run the Houmao interop service fixture step.

                If the user's task does not map cleanly to these steps, use your native planning tool.

                {terms}
                """,
            )
        if include_legacy_operator_folder:
            old_skill_name = "isomer-op-" + "houmao-interop"
            write(
                root / "skillset" / "operator" / old_skill_name / "SKILL.md",
                f"""
                ---
                name: {old_skill_name}
                description: Legacy fixture.
                ---
                """,
            )

    def test_operator_validator_accepts_topic_team_specialization_contract(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertEqual([], messages(diagnostics))

    def test_operator_validator_requires_topic_team_defensive_inbound_gate(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(
            root,
            omit_skill_term="A delegated request must preserve prompt or authoritative context that identifies a formal Agent Team target",
        )

        diagnostics = validator.validate_topic_team_specialization_module(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("delegated request must preserve" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_split_output_contract_trigger(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "complete, verbose, audit, debug, full handoff, or full output",
                "complete output",
            ),
            encoding="utf-8",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("complete, verbose, audit, debug, full handoff, or full output" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_complete_output_as_default(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "Default to **Essential Output** in chat.",
                "Default to **Complete Output** in chat.",
            ),
            encoding="utf-8",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("Default to **Essential Output** in chat." in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_checks_reference_output_contract_shape(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        reference_path = root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / "help.md"
        reference_path.write_text(
            reference_path.read_text(encoding="utf-8")
            + "\n## Output Contract\n\nDefault to **Essential Output** in chat.\n\n### Essential Output\n\n- Fixture summary.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS007", codes(diagnostics))
        self.assertTrue(any("Complete Output" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_chat_output_validator_requires_shared_natural_language_policy(self) -> None:
        root = self.make_root()
        write(
            root / "skillset" / "toolboxes" / "example" / "SKILL.md",
            """
            ---
            name: example
            description: Example skill.
            ---

            # Example
            """,
        )

        diagnostics = validator.validate_chat_output_presentation(
            root,
            (root / "skillset" / "toolboxes",),
            code="SKL006",
        )

        self.assertIn("SKL006", codes(diagnostics))
        self.assertTrue(any("natural-language chat presentation" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_chat_output_validator_rejects_machine_shaped_chat_contract_items(self) -> None:
        root = self.make_root()
        chat_policy = "\n".join(validator.CHAT_RESPONSE_REQUIRED_TERMS)
        write(
            root / "skillset" / "toolboxes" / "example" / "SKILL.md",
            f"""
            ---
            name: example
            description: Example skill.
            ---

            # Example

            ## Output Contract

            - `interpreted_goal`: State the interpreted goal.

            ## Chat Response

            {chat_policy}
            """,
        )

        diagnostics = validator.validate_chat_output_presentation(
            root,
            (root / "skillset" / "toolboxes",),
            code="SKL006",
        )

        self.assertIn("SKL006", codes(diagnostics))
        self.assertTrue(any("`snake_case: details`" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_chat_output_validator_accepts_natural_chat_and_structured_artifact_schema(self) -> None:
        root = self.make_root()
        chat_policy = "\n".join(validator.CHAT_RESPONSE_REQUIRED_TERMS)
        skill_dir = root / "skillset" / "toolboxes" / "example"
        write(
            skill_dir / "SKILL.md",
            f"""
            ---
            name: example
            description: Example skill.
            ---

            # Example

            ## Output Contract

            Explain the interpreted goal and availability in natural prose. If the user explicitly asks for JSON, return the same information in JSON.

            ## Chat Response

            {chat_policy}
            """,
        )
        write(
            skill_dir / "references" / "terminal-report.md",
            """
            # Terminal Report

            ## Durable Artifact Schema

            - `interpreted_goal`: The normalized goal stored in the report artifact.
            """,
        )

        diagnostics = validator.validate_chat_output_presentation(
            root,
            (root / "skillset" / "toolboxes",),
            code="SKL006",
        )

        self.assertEqual([], messages(diagnostics))

    def test_global_cli_validator_rejects_non_dev_pixi_isomer_cli_wrapper(self) -> None:
        root = self.make_root()
        write(root / "skillset" / "misc" / "isomer-misc-example" / "SKILL.md", "Run `pixi run isomer-cli project validate`.\n")

        diagnostics = validator.validate_global_isomer_cli_invocation(root, (root / "skillset",), code="SKL004")

        self.assertIn("SKL004", codes(diagnostics))
        self.assertTrue(any("global isomer-cli directly" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_global_cli_validator_exempts_dev_skills(self) -> None:
        root = self.make_root()
        write(root / "skillset" / "dev" / "isomer-dev-example" / "SKILL.md", "Run `pixi run isomer-cli project validate`.\n")

        diagnostics = validator.validate_global_isomer_cli_invocation(root, (root / "skillset",), code="SKL004")

        self.assertEqual([], messages(diagnostics))

    def test_operator_validator_accepts_welcome_contract(self) -> None:
        root = self.make_root()
        self.write_welcome_skill(root)

        diagnostics = validator.validate_welcome_module(root)

        self.assertEqual([], messages(diagnostics))

    def test_operator_validator_requires_welcome_formal_team_gate(self) -> None:
        root = self.make_root()
        self.write_welcome_skill(root)
        skill_path = root / "skillset" / "operator" / "isomer-op-welcome" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace("formal Agent Team target", "team target"),
            encoding="utf-8",
        )

        diagnostics = validator.validate_welcome_module(root)

        self.assertIn("OPS011", codes(diagnostics))
        self.assertTrue(any("formal Agent Team target" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_welcome_usage_paths_in_skill_md(self) -> None:
        root = self.make_root()
        self.write_welcome_skill(root, omit_skill_term="start-research-by-agent-team")

        diagnostics = validator.validate_welcome_module(root)

        self.assertIn("OPS011", codes(diagnostics))
        self.assertTrue(any("start-research-by-agent-team" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_welcome_extension_paths_in_skill_md(self) -> None:
        root = self.make_root()
        self.write_welcome_skill(root, omit_skill_term="start-kaoju-survey")

        diagnostics = validator.validate_welcome_module(root)

        self.assertIn("OPS011", codes(diagnostics))
        self.assertTrue(any("start-kaoju-survey" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_welcome_extension_evidence_labels(self) -> None:
        root = self.make_root()
        self.write_welcome_skill(root, omit_reference_term="Host-usable")

        diagnostics = validator.validate_welcome_module(root)

        self.assertIn("OPS011", codes(diagnostics))
        self.assertTrue(any("Host-usable" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_welcome_manual_invocation_policy(self) -> None:
        root = self.make_root()
        self.write_welcome_skill(root)
        manifest_path = root / "skillset" / "operator" / "isomer-op-welcome" / "agents" / "openai.yaml"
        manifest_path.write_text(
            manifest_path.read_text(encoding="utf-8").replace("allow_implicit_invocation: false", "allow_implicit_invocation: true"),
            encoding="utf-8",
        )

        diagnostics = validator.validate_welcome_module(root)

        self.assertIn("OPS011", codes(diagnostics))
        self.assertTrue(any("allow_implicit_invocation: false" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_welcome_direct_owner_invocation_language(self) -> None:
        root = self.make_root()
        self.write_welcome_skill(root, omit_direct_owner="isomer-op-topic-mgr")

        diagnostics = validator.validate_welcome_module(root)

        self.assertIn("OPS011", codes(diagnostics))
        self.assertTrue(any("direct invocation language for $isomer-op-topic-mgr" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_welcome_active_retired_route(self) -> None:
        root = self.make_root()
        self.write_welcome_skill(root, active_retired_route=True)

        diagnostics = validator.validate_welcome_module(root)

        self.assertIn("OPS011", codes(diagnostics))
        self.assertTrue(any("retired skill 'isomer-op-topic-prepare'" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_welcome_automatic_tool_pack_route(self) -> None:
        root = self.make_root()
        self.write_welcome_skill(root, automatic_tool_pack_route=True)

        diagnostics = validator.validate_welcome_module(root)

        self.assertIn("OPS011", codes(diagnostics))
        self.assertTrue(any("isomer-misc-tool-packs only as manual explicit routing" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_accepts_entrypoint_contract(self) -> None:
        root = self.make_root()
        self.write_entrypoint_skill(root)

        diagnostics = validator.validate_entrypoint_module(root)

        self.assertEqual([], messages(diagnostics))

    def test_operator_validator_requires_entrypoint_formal_team_gate(self) -> None:
        root = self.make_root()
        self.write_entrypoint_skill(root)
        skill_path = root / "skillset" / "operator" / "isomer-op-entrypoint" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "Establish formal Agent Team intent before specialization",
                "Check specialization intent",
            ),
            encoding="utf-8",
        )

        diagnostics = validator.validate_entrypoint_module(root)

        self.assertIn("OPS013", codes(diagnostics))
        self.assertTrue(any("Establish formal Agent Team intent before specialization" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_entrypoint_prerequisite_preflight(self) -> None:
        root = self.make_root()
        self.write_entrypoint_skill(root, omit_skill_term="Preflight target prerequisites")

        diagnostics = validator.validate_entrypoint_module(root)

        self.assertIn("OPS013", codes(diagnostics))
        self.assertTrue(any("Preflight target prerequisites" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_entrypoint_prerequisite_recovery_contract(self) -> None:
        root = self.make_root()
        self.write_entrypoint_skill(root, omit_reference_term="ordinary `do <task>`")

        diagnostics = validator.validate_entrypoint_module(root)

        self.assertIn("OPS013", codes(diagnostics))
        self.assertTrue(any("ordinary `do <task>`" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_accepts_ordinary_prerequisite_pause_fixture(self) -> None:
        root = self.make_root()
        self.write_entrypoint_skill(root)

        diagnostics = validator.validate_entrypoint_module(root)

        self.assertEqual([], messages(diagnostics))

    def test_operator_validator_accepts_authorized_cross_owner_run_to_fixture(self) -> None:
        root = self.make_root()
        self.write_entrypoint_skill(root)

        diagnostics = validator.validate_entrypoint_module(root)

        self.assertEqual([], messages(diagnostics))

    def test_operator_validator_accepts_system_skill_manager_contract(self) -> None:
        diagnostics = validator.validate_system_skill_manager_module(REPO_ROOT)

        self.assertEqual([], messages(diagnostics))

    def test_operator_validator_rejects_system_skill_manager_universal_provider_path(self) -> None:
        root = self.make_root()
        source = SYSTEM_SKILL_MANAGER_SOURCE
        target = root / "skillset" / "operator" / "isomer-op-system-skill-mgr"
        shutil.copytree(source, target)
        skill_md = target / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8") + "\nAlways discover project extensions from `.claude/skills`.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_system_skill_manager_module(root)

        self.assertIn("OPS014", codes(diagnostics))
        self.assertTrue(any("universal discovery authority" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_system_skill_manager_trust_order_regression(self) -> None:
        root = self.make_root()
        source = SYSTEM_SKILL_MANAGER_SOURCE
        target = root / "skillset" / "operator" / "isomer-op-system-skill-mgr"
        shutil.copytree(source, target)
        skill_md = target / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        skill_md.write_text(
            text.replace("# Isomer Operator", "**Limited live inventory** first.\n\n# Isomer Operator", 1),
            encoding="utf-8",
        )

        diagnostics = validator.validate_system_skill_manager_module(root)

        self.assertIn("OPS014", codes(diagnostics))
        self.assertTrue(
            any(
                "declaration, current-v4 receipt, explicit-root, then live-inventory order" in message
                for message in messages(diagnostics)
            ),
            messages(diagnostics),
        )

    def test_operator_validator_rejects_system_skill_manager_home_override(self) -> None:
        root = self.make_root()
        source = SYSTEM_SKILL_MANAGER_SOURCE
        target = root / "skillset" / "operator" / "isomer-op-system-skill-mgr"
        shutil.copytree(source, target)
        install_reference = target / "references" / "install-extension.md"
        install_reference.write_text(
            install_reference.read_text(encoding="utf-8")
            + "\nRun `isomer-cli system-skills install --target generic --home /tmp/skills`.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_system_skill_manager_module(root)

        self.assertIn("OPS014", codes(diagnostics))
        self.assertTrue(any("must use scoped installation guidance" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_stale_universal_install_scope_claim(self) -> None:
        root = self.make_root()
        source = SYSTEM_SKILL_MANAGER_SOURCE
        target = root / "skillset" / "operator" / "isomer-op-system-skill-mgr"
        shutil.copytree(source, target)
        install_reference = target / "references" / "install-extension.md"
        install_reference.write_text(
            install_reference.read_text(encoding="utf-8")
            + "\nEvery system-skills install requires an explicit `--scope`.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_system_skill_manager_module(root)

        self.assertIn("OPS014", codes(diagnostics))
        self.assertTrue(any("stale universal install scope requirement" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_entrypoint_deepsci_extension_coverage(self) -> None:
        root = self.make_root()
        self.write_entrypoint_skill(root, omit_reference_term="isomer-deepsci-scout")

        diagnostics = validator.validate_entrypoint_module(root)

        self.assertIn("OPS013", codes(diagnostics))
        self.assertTrue(any("isomer-deepsci-scout" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_entrypoint_service_first_click_route(self) -> None:
        root = self.make_root()
        self.write_entrypoint_skill(root, service_first_click=True)

        diagnostics = validator.validate_entrypoint_module(root)

        self.assertIn("OPS013", codes(diagnostics))
        self.assertTrue(any("first-click owner routes" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_entrypoint_active_retired_route(self) -> None:
        root = self.make_root()
        self.write_entrypoint_skill(root, active_retired_route=True)

        diagnostics = validator.validate_entrypoint_module(root)

        self.assertIn("OPS013", codes(diagnostics))
        self.assertTrue(any("isomer-op-topic-prepare" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_entrypoint_route_and_proceed_behavior(self) -> None:
        root = self.make_root()
        self.write_entrypoint_skill(root, omit_skill_term="Proceed with the selected route")

        diagnostics = validator.validate_entrypoint_module(root)

        self.assertIn("OPS013", codes(diagnostics))
        self.assertTrue(any("Proceed with the selected route" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_manifest_inventory_accepts_welcome_and_rejects_retired_entries(self) -> None:
        root = self.make_root()
        write(
            root / "skillset" / "manifest.toml",
            """
            [groups.core]
            skills = [
              "operator/isomer-op-entrypoint",
              "operator/isomer-op-gui-mgr",
              "operator/isomer-op-welcome",
              "operator/isomer-op-switch-identity",
              "operator/isomer-op-project-mgr",
              "operator/isomer-op-system-skill-mgr",
            ]
            """,
        )

        diagnostics = validator.validate_operator_manifest_inventory(root)

        self.assertEqual([], messages(diagnostics))

        write(
            root / "skillset" / "manifest.toml",
            """
            [groups.core]
            skills = [
              "operator/isomer-op-topic-prepare",
              "operator/isomer-op-manual-research-session",
            ]
            """,
        )

        diagnostics = validator.validate_operator_manifest_inventory(root)

        self.assertIn("OPS011", codes(diagnostics))
        rendered = "\n".join(messages(diagnostics))
        self.assertIn("operator/isomer-op-welcome", rendered)
        self.assertIn("operator/isomer-op-switch-identity", rendered)
        self.assertIn("operator/isomer-op-entrypoint", rendered)
        self.assertIn("operator/isomer-op-gui-mgr", rendered)
        self.assertIn("operator/isomer-op-topic-prepare", rendered)
        self.assertIn("operator/isomer-op-manual-research-session", rendered)

    def test_operator_validator_accepts_switch_identity_contract(self) -> None:
        root = self.make_root()
        self.write_switch_identity_skill(root)

        diagnostics = validator.validate_switch_identity_module(root)

        self.assertEqual([], messages(diagnostics))

    def test_operator_validator_requires_switch_identity_command_pages(self) -> None:
        root = self.make_root()
        self.write_switch_identity_skill(root, omit_command="act-as.md")

        diagnostics = validator.validate_switch_identity_module(root)

        self.assertIn("OPS012", codes(diagnostics))
        self.assertTrue(any("commands/act-as.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_switch_identity_act_as_restore_guidance(self) -> None:
        root = self.make_root()
        self.write_switch_identity_skill(root, omit_command_term="Restore the previous Project Operator identity posture")

        diagnostics = validator.validate_switch_identity_module(root)

        self.assertIn("OPS012", codes(diagnostics))
        self.assertTrue(any("Restore the previous Project Operator identity posture" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_switch_identity_persistent_guidance(self) -> None:
        root = self.make_root()
        self.write_switch_identity_skill(root, omit_skill_term="persistent")

        diagnostics = validator.validate_switch_identity_module(root)

        self.assertIn("OPS012", codes(diagnostics))
        self.assertTrue(any("persistent" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_switch_identity_cwd_discipline(self) -> None:
        root = self.make_root()
        self.write_switch_identity_skill(root, omit_skill_term="DO NOT use the Project root, Topic Workspace root, or `topic.repos.main` as the default switched cwd")

        diagnostics = validator.validate_switch_identity_module(root)

        self.assertIn("OPS012", codes(diagnostics))
        self.assertTrue(any("Project root" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_switch_identity_directory_scanning_resolution(self) -> None:
        root = self.make_root()
        self.write_switch_identity_skill(root, active_directory_scanning=True)

        diagnostics = validator.validate_switch_identity_module(root)

        self.assertIn("OPS012", codes(diagnostics))
        self.assertTrue(any("scanning workspace directories" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_switch_identity_fabricated_runtime_claims(self) -> None:
        root = self.make_root()
        self.write_switch_identity_skill(root, active_fabricated_claim=True)

        diagnostics = validator.validate_switch_identity_module(root)

        self.assertIn("OPS012", codes(diagnostics))
        self.assertTrue(any("launched Agent Instance" in message or "Houmao launch" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_core_owned_heavy_operation_lists(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        subcommand_path = (
            root
            / "skillset"
            / "operator"
            / "isomer-op-topic-team-specialize"
            / "references"
            / "setup-topic-env.md"
        )
        subcommand_path.write_text(
            subcommand_path.read_text(encoding="utf-8")
            + "\nUse a heavy setup or verification command such as compilation, deep model inference, or broad test suite execution.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("delegate heavy-operation classification" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_team_dependency_manifest(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        (
            root
            / "skillset"
            / "operator"
            / "isomer-op-topic-team-specialize"
            / "references"
            / "step-dependencies.json"
        ).unlink()

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("step-dependencies.json" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_team_dependency_script(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        (
            root
            / "skillset"
            / "operator"
            / "isomer-op-topic-team-specialize"
            / "scripts"
            / "query_step_dependencies.py"
        ).unlink()

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("query_step_dependencies.py" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_team_dependency_manifest_coverage(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        manifest_path = (
            root
            / "skillset"
            / "operator"
            / "isomer-op-topic-team-specialize"
            / "references"
            / "step-dependencies.json"
        )
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["steps"].pop("adapt-team-template")
        manifest["canonical_order"].remove("adapt-team-template")
        manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("adapt-team-template" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_duplicated_topic_team_recovery_chain(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        subcommand_path = (
            root
            / "skillset"
            / "operator"
            / "isomer-op-topic-team-specialize"
            / "references"
            / "validate-topic-team.md"
        )
        subcommand_path.write_text(
            subcommand_path.read_text(encoding="utf-8")
            + "\nThe inclusive default path is resolve-topic-intent -> ensure-topic-registration -> validate-topic-team.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("must not duplicate targeted recovery chains" in message for message in messages(diagnostics)), messages(diagnostics))

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
            "semantic label evidence",
            "topic.repos.main",
            "agent.workspace",
            "required `agent.*` support paths",
            "agent_workspace_paths",
            "semantic_paths",
            "semantic labels",
            "path sources",
            "topic_team_validation_status",
            "isomer-managed/",
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

    def test_operator_validator_requires_topic_team_semantic_reference_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        path = root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / "validate-topic-team.md"
        path.write_text(path.read_text(encoding="utf-8").replace("hard-coded default-only paths without semantic labels", ""), encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("hard-coded default-only paths without semantic labels" in message for message in messages(diagnostics)), messages(diagnostics))

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
        (root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / "resolve-project.md").unlink()

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("resolve-project.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_new_topic_team_subcommands(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        (root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / "init-topic.md").unlink()

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("init-topic.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_procedural_subcommand_prerequisites(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root, omit_prerequisite_subcommand="adapt-team-template.md")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("adapt-team-template.md" in message and "predecessor artifacts" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_private_helpers_in_help(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / "help.md",
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
            root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / "help.md",
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
            root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / "help.md",
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
            root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / "route-service.md",
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
            root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / "launch-team.md",
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
        write(root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "evals" / "evals.json", "{}")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("must not contain evals/" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_incorporated_standalone_skill(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-op-project-aware" / "SKILL.md",
            """
            ---
            name: isomer-op-project-aware
            description: Duplicated fixture skill.
            ---

            # Duplicate
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("must not be a standalone skill" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_stale_skill_namespaces(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        stale_admin = "isomer-" + "admin-project-mgr"
        stale_rsch = "isomer-" + "rsch-scout"
        write(
            root / "docs" / "routes.md",
            f"""
            # Routes

            Use ${stale_admin} for project checks and ${stale_rsch} for research framing.
            """,
        )
        write(
            root / "src" / "isomer_labs" / "assets" / "system_skills" / "research-paradigm" / "deepsci" / "example" / "migrate" / "notes.md",
            f"Historical reference to ${stale_admin} and ${stale_rsch} is passive.\n",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS002", codes(diagnostics))
        rendered = "\n".join(messages(diagnostics))
        self.assertIn("stale skill namespace 'isomer-" + "admin-'", rendered)
        self.assertIn("stale skill namespace 'isomer-" + "rsch-'", rendered)
        self.assertNotIn("migrate/notes.md", rendered)

    def test_operator_validator_rejects_external_topic_team_support_refs(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-op-topic-team-specialize" / "references" / "resolve-project.md",
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
        (root / "skillset" / "operator" / "isomer-op-project-mgr" / "references" / "list-topics.md").unlink()

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
        write(root / "skillset" / "operator" / "isomer-op-project-mgr" / "evals" / "evals.json", "{}")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS005", codes(diagnostics))
        self.assertTrue(any("must not contain evals/" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_root_project_manager_cli_shapes(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_project_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-op-project-mgr" / "references" / "check-project.md",
            """
            # Check Project

            ## Workflow

            1. Run `isomer-cli --project <project-root> validate`.

            If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS005", codes(diagnostics))
        self.assertTrue(any("supported isomer-cli command shapes" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_repo_local_isomer_cli_wrapper(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_project_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-op-project-mgr" / "references" / "check-project.md"
        skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\nRun `pixi run isomer-cli project validate`.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS010", codes(diagnostics))
        self.assertTrue(any("global isomer-cli directly" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        shutil.rmtree(root / "skillset" / "operator" / "isomer-op-topic-mgr")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("isomer-op-topic-mgr is required" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_creator(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        shutil.rmtree(root / "skillset" / "operator" / "isomer-op-topic-creator")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS008", codes(diagnostics))
        self.assertTrue(any("isomer-op-topic-creator is required" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_creator_staged_flow_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_creator_skill(root, omit_skill_term="define-topic-env")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS008", codes(diagnostics))
        self.assertTrue(any("define-topic-env" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_actor_definition_gate_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_creator_skill(root, omit_skill_term="topic.env.actor_env_gates")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS008", codes(diagnostics))
        self.assertTrue(any("topic.env.actor_env_gates" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_stale_define_topic_reference(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_creator_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-op-topic-creator" / "references" / "define-topic.md",
            """
            # Define Topic

            ## Workflow

            1. Write topic intent from a stale command.

            If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS008", codes(diagnostics))
        self.assertTrue(any("define-topic.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_stale_start_manual_research_reference(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_creator_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-op-topic-creator" / "references" / "start-manual-research.md",
            """
            # Start Manual Research

            ## Workflow

            1. Write stale start-pack material.

            If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS008", codes(diagnostics))
        self.assertTrue(any("start-manual-research.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_retired_operator_skill_folders(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-op-topic-prepare" / "SKILL.md",
            """
            ---
            name: isomer-op-topic-prepare
            description: Retired fixture.
            ---

            # Retired
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("isomer-op-topic-prepare is no longer part of the active operator skillset" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_retired_topic_workspace_manager_folder(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-op-topic-workspace-mgr" / "SKILL.md",
            """
            ---
            name: isomer-op-topic-workspace-mgr
            description: Retired fixture.
            ---

            # Retired
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("isomer-op-topic-workspace-mgr is no longer part of the active operator skillset" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager_subcommands(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root, omit_subcommand="team-materialize-workspaces.md")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("team-materialize-workspaces.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager_guardrail_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root, omit_skill_term="Workspace Runtime")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("Workspace Runtime" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager_semantic_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root, omit_skill_term="semantic workspace labels")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("semantic workspace labels" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager_semantic_reference_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        path = root / "skillset" / "operator" / "isomer-op-topic-mgr" / "references" / "team-validate-workspaces.md"
        path.write_text(path.read_text(encoding="utf-8").replace("hard-coded default-only evidence", ""), encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("hard-coded default-only evidence" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager_package_specific_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        path = root / "skillset" / "operator" / "isomer-op-topic-mgr" / "references" / "env-install-packages.md"
        path.write_text(path.read_text(encoding="utf-8").replace("isomer-misc-pkg-specifics", ""), encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("isomer-misc-pkg-specifics" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager_package_specific_evidence_output(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        path = root / "skillset" / "operator" / "isomer-op-topic-mgr" / "references" / "env-update-packages.md"
        path.write_text(path.read_text(encoding="utf-8").replace("package-specific guidance", ""), encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("package-specific guidance" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager_isomer_managed_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root, omit_skill_term="isomer-managed/")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("isomer-managed/" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_git_reset_guidance_in_reset_workflows(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        reset_path = root / "skillset" / "operator" / "isomer-op-topic-mgr" / "references" / "reset-plan.md"
        reset_path.write_text(reset_path.read_text(encoding="utf-8") + "\nWhen topic-reset is stale, run `git stash` before planning.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("must not recommend Git reset" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_research_paradigm_routing_in_reset_guidance(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        reset_path = root / "skillset" / "operator" / "isomer-op-topic-mgr" / "references" / "reset-inspect.md"
        reset_path.write_text(reset_path.read_text(encoding="utf-8") + "\nFor reset checkpoint inspection, route to skillset/research-paradigm/deepsci first.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("must not route to or depend on research-paradigm" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_topic_manager_agent_key_wording(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-op-topic-mgr" / "SKILL.md"
        skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\nUse `<agent-key>` for public examples.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("agent-name public wording" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_topic_manager_legacy_support_root_wording(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-op-topic-mgr" / "SKILL.md"
        skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\nUse `.isomer-agent/` for current support.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any(".isomer-agent/" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_topic_manager_validator_requires_topic_main_agent_guidance_terms(self) -> None:
        root = self.make_root()
        self.write_topic_manager_skill(root)
        path = root / "skillset" / "operator" / "isomer-op-topic-mgr" / "references" / "storage-inspect-main.md"
        path.write_text(
            path.read_text(encoding="utf-8").replace("isomer-labs-topic-main-guidance", ""),
            encoding="utf-8",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("isomer-labs-topic-main-guidance" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_topic_manager_validator_rejects_copied_topic_main_guidance_body(self) -> None:
        root = self.make_root()
        self.write_topic_manager_skill(root)
        path = root / "skillset" / "operator" / "isomer-op-topic-mgr" / "references" / "storage-inspect-main.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\nThis repository is an Isomer Topic Main Development Repository.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("copying the rendered block body" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_research_validator_requires_worker_output_policy_for_plain_file_guidance(self) -> None:
        root = self.make_root()
        skill_path = root / "skillset" / "research-paradigm" / "v2" / "isomer-deepsci-write" / "SKILL.md"
        write(
            skill_path,
            """
            # Isomer Research Write

            ## Workflow

            Write Markdown drafts, reports, local summaries, and paper builds.
            """,
        )
        document = validator.research_validator.Document(
            path=skill_path,
            rel_repo="skillset/research-paradigm/deepsci/isomer-deepsci-write/SKILL.md",
            rel_target="deepsci/isomer-deepsci-write/SKILL.md",
            lines=tuple(skill_path.read_text(encoding="utf-8").splitlines()),
            sections_by_line=(),
            roles=frozenset({"deepsci", "active"}),
        )
        diagnostics: list[object] = []

        validator.research_validator.validate_deepsci_worker_output_policy(document, root, diagnostics)

        self.assertIn("RPS015", codes(diagnostics))
        self.assertTrue(any("project outputs policy" in message for message in messages(diagnostics)), messages(diagnostics))

        fixed_path = root / "skillset" / "research-paradigm" / "deepsci" / "isomer-deepsci-paper-plot" / "SKILL.md"
        write(
            fixed_path,
            """
            # Isomer Research Paper Plot

            ## Workflow

            Write CSVs and figures only after resolving `project outputs policy`; use an operation-specific child set and check `commit_after_operation`.
            """,
        )
        fixed_document = validator.research_validator.Document(
            path=fixed_path,
            rel_repo="skillset/research-paradigm/deepsci/isomer-deepsci-paper-plot/SKILL.md",
            rel_target="deepsci/isomer-deepsci-paper-plot/SKILL.md",
            lines=tuple(fixed_path.read_text(encoding="utf-8").splitlines()),
            sections_by_line=(),
            roles=frozenset({"deepsci", "active"}),
        )
        fixed_diagnostics: list[object] = []

        validator.research_validator.validate_deepsci_worker_output_policy(fixed_document, root, fixed_diagnostics)

        self.assertEqual([], fixed_diagnostics)

    def test_service_validator_accepts_topic_env_setup_contract(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertEqual([], messages(diagnostics))

    def test_service_validator_requires_split_output_contract_trigger(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)
        skill_path = root / "skillset" / "service" / "isomer-srv-topic-env-setup" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "complete, verbose, audit, debug, full handoff, or full output",
                "complete output",
            ),
            encoding="utf-8",
        )

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("complete, verbose, audit, debug, full handoff, or full output" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_rejects_legacy_env_setup_folder(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, include_legacy_folder=True)
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("legacy isomer-srv-env-setup" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_topic_env_setup_subcommands(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)
        (root / "skillset" / "service" / "isomer-srv-topic-env-setup" / "references" / "setup-topic-env.md").unlink()

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("setup-topic-env.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_team_independent_env_setup_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="DO NOT require `team-profile/`")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("team-independent environment setup" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_semantic_path_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_skill_term="semantic_paths")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("semantic_paths" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_topic_env_predecessor_boundary_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_skill_term="Topic Workspace predecessor evidence")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("Topic Workspace predecessor evidence" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_per_agent_readiness_not_checked_reference(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="per-Agent readiness was not checked")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("per-Agent readiness was not checked" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_tmp_label_posture_reference_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="topic.tmp")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("topic.tmp" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_bounded_real_path_topic_env_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="bounded real-path")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("bounded real-path" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_topic_main_agent_guidance_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="isomer-labs-topic-main-guidance")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("isomer-labs-topic-main-guidance" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_rejects_copied_topic_main_guidance_body(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)
        path = root / "skillset" / "service" / "isomer-srv-topic-env-setup" / "references" / "ensure-topic-main-repository.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\nThis repository is an Isomer Topic Main Development Repository.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("copying the rendered block body" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_rejects_core_owned_heavy_operation_lists(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)
        skill_path = root / "skillset" / "service" / "isomer-srv-topic-env-setup" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8") + "\nTreat compilation, deep model inference, and full dataset download as heavy.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("delegate heavy-operation classification" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_rejects_repo_local_isomer_cli_wrapper(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)
        skill_path = root / "skillset" / "service" / "isomer-srv-topic-env-setup" / "references" / "resolve-topic-workspace.md"
        skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\nRun `pixi run isomer-cli project paths get`.\n", encoding="utf-8")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS005", codes(diagnostics))
        self.assertTrue(any("global isomer-cli directly" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_complete_checklist_readiness_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="every required `## Gate Checklist` item")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("every required `## Gate Checklist` item" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_explicit_blocked_checklist_item_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="exact checklist item")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("exact checklist item" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_rejects_missing_smoke_test_substitution_guardrail(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="weaker smoke test")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("weaker smoke test" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_package_specifics_validator_accepts_contract(self) -> None:
        root = self.make_root()
        self.write_package_specifics_skill(root)

        diagnostics = validator.validate_package_specifics_skill(root)

        self.assertEqual([], messages(diagnostics))

    def test_package_specifics_validator_requires_first_lookup_contract(self) -> None:
        root = self.make_root()
        self.write_package_specifics_skill(root, omit_term="First lookup")

        diagnostics = validator.validate_package_specifics_skill(root)

        self.assertIn("SKL005", codes(diagnostics))
        self.assertTrue(any("First lookup" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_package_specifics_validator_requires_no_rule_evidence(self) -> None:
        root = self.make_root()
        self.write_package_specifics_skill(root, omit_term="no package-specific rule")

        diagnostics = validator.validate_package_specifics_skill(root)

        self.assertIn("SKL005", codes(diagnostics))
        self.assertTrue(any("no package-specific rule" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_topic_env_package_specific_first_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="isomer-misc-pkg-specifics")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("isomer-misc-pkg-specifics" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_topic_env_no_package_specific_rule_evidence(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="no package-specific rule")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("no package-specific rule" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_accepts_agent_env_setup_contract(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertEqual([], messages(diagnostics))

    def test_service_validator_accepts_houmao_interop_contract(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertEqual([], messages(diagnostics))

    def test_service_validator_requires_houmao_interop_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)
        self.write_houmao_interop_service(root, omit_skill_term="bounded Service Team support")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS006", codes(diagnostics))
        self.assertTrue(any("bounded Service Team support" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_rejects_legacy_houmao_interop_operator_folder(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)
        self.write_houmao_interop_service(root, include_legacy_operator_folder=True)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS006", codes(diagnostics))
        self.assertTrue(any("legacy" in message and "operator skill folder" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_agent_env_setup_subcommands(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root, omit_subcommand="verify-agent-env-gate.md")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS003", codes(diagnostics))
        self.assertTrue(any("verify-agent-env-gate.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_agent_env_source_intent_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root, omit_skill_term="topic.intent.agent_env_requirements")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS003", codes(diagnostics))
        self.assertTrue(any("topic.intent.agent_env_requirements" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_bounded_real_path_agent_env_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root, omit_reference_term="bounded real-path")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS003", codes(diagnostics))
        self.assertTrue(any("bounded real-path" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_agent_env_target_spec_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root, omit_skill_term="topic.env.agent_setup_target_spec")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS003", codes(diagnostics))
        self.assertTrue(any("topic.env.agent_setup_target_spec" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_agent_env_semantic_path_terms(self) -> None:
        for term in ("topic.repos.main", "agent.workspace"):
            with self.subTest(term=term):
                root = self.make_root()
                self.write_topic_env_setup_service(root)
                self.write_agent_env_setup_service(root, omit_skill_term=term)

                diagnostics = validator.validate_service_skillset(root)

                self.assertIn("SVS003", codes(diagnostics))
                self.assertTrue(any(term in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_agent_env_pixi_and_cwd_terms(self) -> None:
        for term in (
            "pixi run --manifest-path <manifest_path> --environment <pixi_environment>",
            "Agent Workspace cwd",
        ):
            with self.subTest(term=term):
                root = self.make_root()
                self.write_topic_env_setup_service(root)
                if term.startswith("pixi run"):
                    self.write_agent_env_setup_service(root, omit_skill_term=term)
                else:
                    self.write_agent_env_setup_service(root, omit_reference_term=term)

                diagnostics = validator.validate_service_skillset(root)

                self.assertIn("SVS003", codes(diagnostics))
                self.assertTrue(any(term in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_agent_env_no_runtime_mutation_guardrail(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root, omit_skill_term="mutate Workspace Runtime records")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS003", codes(diagnostics))
        self.assertTrue(any("mutate Workspace Runtime records" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_agent_env_package_repair_route(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root, omit_reference_term="do not invent a separate per-agent package install plan")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS003", codes(diagnostics))
        self.assertTrue(any("separate per-agent package install plan" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_agent_env_package_specific_verification_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root, omit_reference_term="isomer-misc-pkg-specifics")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS003", codes(diagnostics))
        self.assertTrue(any("isomer-misc-pkg-specifics" in message for message in messages(diagnostics)), messages(diagnostics))
