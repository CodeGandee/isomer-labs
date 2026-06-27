from __future__ import annotations

import importlib.util
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

            Procedural Subcommands: `init-topic`, `clarify-topic`, `ensure-topic-registration`, `specialize-team`, `clarify-topic-team`, `setup-topic-env`, `setup-agent-workspace`, `validate-topic-team`, `finalize-topic-team`, `approve-profile`, and `materialize-profile`.

            Helper Subcommands: five lower-level implementation commands: `resolve-project`, `inspect-template`, `resolve-context`, `map-placeholders`, and `draft-profile`.

            Misc Subcommands: `help`, `fast-forward`, and `step-by-step`.

            Use {subcommand_links}.

            Use static material readiness, durable setup state, `topic-overview.md`, concrete Research Topic, default Research Topic, provisional topic workspace seed, `isomer-content/topic-ws/<topic-slug>/`, `team-specialization-guide.md`, `team-specialization-plan.md`, `{final_report}`, `<topic-workspace>/team-profile/execplan/`, `isomer-managed/`, and `isomer-topic-summary.md`.

            Require semantic label evidence for `topic.repos.main`, `agent.workspace`, and required `agent.*` support paths. Report `selected_domain_team_template_ref`, `topic_environment_status`, `agent_workspace_paths`, `semantic_paths`, semantic labels, path sources, `topic_team_validation_status`, and `isomer_topic_summary_path`.

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

                    1. Print public subcommands as a table with semantic path evidence.

                    If the user's task does not map cleanly to these steps, use your native planning tool.

                    ## Public Subcommands

                    | Subcommand | Purpose | Produces |
                    | --- | --- | --- |
                    | `init-topic` | Start topic setup. | `topic-overview.md`. |
                    | `clarify-topic` | Clarify topic. | Updated `topic-overview.md`. |
                    | `ensure-topic-registration` | Ensure Project registration. | Registered topic refs. |
                    | `specialize-team` | Specialize topic team. | Draft profile inputs. |
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
                Require `topic.repos.main`, `agent.workspace`, `agent.tmp`, required `agent.*` support paths, `semantic_paths`, `local_tmp_path_status`, semantic labels, path sources, and reject default-looking directories without semantic labels and path sources.
                """
            elif subcommand_name == "validate-topic-team.md":
                extra_terms = """
                Require `topic.repos.main`, `agent.workspace`, `agent.tmp`, required `agent.*` support labels, `semantic_paths`, `local_tmp_path_status`, path sources, and reject hard-coded default-only paths without semantic labels.
                """
            elif subcommand_name == "finalize-topic-team.md":
                extra_terms = """
                Report semantic labels first with `topic.repos.main`, `topic.repos.main.tmp`, `agent.workspace`, `agent.tmp`, path sources, `isomer-default.v1`, and reject hard-coded default-only paths without semantic label evidence.
                """
            write(
                root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / subcommand_name,
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
                root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / support_reference_name,
                f"""
                # {support_reference_name}

                Local support reference.
                """,
            )
        self.write_project_manager_skill(root)
        self.write_topic_workspace_manager_skill(root)

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
            3. Preserve `.isomer-labs/`, `.isomer-labs/.houmao/`, root `.houmao/` as external user-owned state, `isomer-content/`, `isomer-content/topic-ws/<topic-id>/`, `--content-dir <content-dir>`, `<content-dir>/topic-ws/<topic-id>/`, Isomer-managed Houmao overlay, `isomer-cli project init`, `isomer-cli project cleanup --part <part> --dry-run`, `isomer-cli project cleanup --part <part> --yes`, `--purge-content-root`, `isomer-cli project content-root move --to <content-dir> --dry-run`, `isomer-cli project content-root move --to <content-dir> --yes`, unknown files, `isomer-cli project validate`, `isomer-cli project doctor`, `isomer-cli project runtime init`, `isomer-cli project runtime prepare`, and `isomer-admin-topic-team-specialize` boundaries.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            Use `references/help.md`, `references/init-project.md`, `references/cleanup-project.md`, `references/move-content.md`, `references/check-project.md`, `references/list-topics.md`, `references/show-context.md`, `references/init-runtime.md`, `references/prep-runtime.md`, and `references/specialize-team.md`.
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

    def write_topic_workspace_manager_skill(
        self,
        root: Path,
        *,
        omit_subcommand: str | None = None,
        omit_skill_term: str | None = None,
        omit_subcommand_fallback: bool = False,
    ) -> None:
        skill_dir = root / "skillset" / "operator" / "isomer-admin-topic-workspace-mgr"
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        subcommand_links = ", ".join(
            f"`references/{subcommand_name}`" for subcommand_name in validator.TOPIC_WORKSPACE_MANAGER_SUBCOMMANDS
        )
        skill_text = f"""
            ---
            name: isomer-admin-topic-workspace-mgr
            description: Valid fixture topic workspace manager skill.
            ---

            # Isomer Admin Topic Workspace Mgr

            Prepare semantic workspace labels through Topic Workspace Manifest bindings and `isomer-default.v1`, including `project paths register`, `project repos create`, explicit `storage_profile`, `custom.*`, grouped `topic.repos.*`, `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, `topic.agents_root`, `agent.workspace`, `agent.tmp`, `agent.private_artifacts`, `agent.public_share`, `agent.links`, `semantic_paths`, `local_tmp_path_status`, `topic-owner/main`, `per-agent/<agent-name>/main`, `isomer-managed/`, `tracked/`, `agent-owned/`, `topic-owned/`, `links/`, `topic.records.*`, and `per-agent/<agent-name>/<branch-name>` while planning `agent_name`, `agent_branch`, and derived compatibility `agent_workspace_ref` values, and preserving Agent Instance, Workspace Runtime, Houmao, Execution Adapter, Workspace Boundary, Peer Read Access, blockers, and `next_operator_action` boundaries.

            ## Workflow

            1. **Default subcommand**: Run `topic-workspace`.
            2. Select one subcommand and load only its detail page.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            Procedural Subcommands: `resolve-workspace`, `ensure-main-repo`, `plan-agents`, `create-worktrees`, `write-boundaries`, `create-agent-branch`, `validate-worktrees`, and `summarize`.

            Helper Subcommands: `resolve-workspace`, `ensure-main-repo`, `plan-agents`, `create-worktrees`, and `validate-worktrees`.

            Misc Subcommands: `help` and `topic-workspace`.

            Use {subcommand_links}.
            """
        if omit_skill_term is not None:
            skill_text = skill_text.replace(omit_skill_term, "")
        write(root / "skillset" / "operator" / "isomer-admin-topic-workspace-mgr" / "SKILL.md", skill_text)
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-workspace-mgr" / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-admin-topic-workspace-mgr"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-admin-topic-workspace-mgr to validate this fixture."
            """,
        )
        for subcommand_name in validator.TOPIC_WORKSPACE_MANAGER_SUBCOMMANDS:
            if subcommand_name == omit_subcommand:
                continue
            if subcommand_name == "help.md":
                write(
                    root / "skillset" / "operator" / "isomer-admin-topic-workspace-mgr" / "references" / subcommand_name,
                    """
                    # Help

                    ## Workflow

                    1. Print the public subcommands and blocker guidance.

                    If the user's task does not map cleanly to these steps, use your native planning tool.

                    ## Public Subcommands

                    | Subcommand | Purpose | Produces |
                    | --- | --- | --- |
                    | `resolve-workspace` | Resolve Project context. | `semantic_paths`, `topic.repos.main`, `agent.workspace`. |
                    | `ensure-main-repo` | Prepare repo. | Repo readiness. |
                    | `plan-agents` | Plan agents. | Agent name plans. |
                    | `create-worktrees` | Create worktrees. | Worktree readiness. |
                    | `write-boundaries` | Write boundaries. | Boundary paths. |
                    | `create-agent-branch` | Create branch. | Branch result. |
                    | `validate-worktrees` | Validate worktrees. | Validation status. |
                    | `summarize` | Summarize results. | Next operator action. |
                    | `topic-workspace` | Run full flow. | Full setup result. |
                    | `help` | Print usage. | Help output. |
                    """,
                )
                continue
            fallback = "" if omit_subcommand_fallback and subcommand_name == "plan-agents.md" else "If the user's task does not map cleanly to these steps, use your native planning tool."
            extra_terms = {
                "resolve-workspace.md": "Use `isomer-cli project paths get`, `project paths explain`, `semantic_paths`, `topic.repos.main`, and `agent.workspace` before mutation.",
                "ensure-main-repo.md": "Use `topic.repos.main`, `topic.repos.main.tmp`, `topic.repos.main.isomer_managed`, and `isomer-default.v1` examples only after semantic resolution.",
                "plan-agents.md": "Resolve `agent.workspace` through Workspace Path Resolution and report path sources.",
                "create-worktrees.md": "Create worktrees at `agent.workspace` from `topic.repos.main`, with `agent.tmp`, path sources, and semantic support paths.",
                "write-boundaries.md": "Write boundary notes for `topic.repos.main`, `agent.workspace`, each path source, and self-query guidance without passing Agent Name.",
                "validate-worktrees.md": "Validate semantic label bindings, `topic.repos.main.tmp`, `agent.tmp`, tracked tmp contents, and reject hard-coded default-only evidence.",
                "summarize.md": "Report `semantic_paths`, `local_tmp_path_status`, `agent.tmp`, cwd-friendly guidance, and self-query guidance without passing Agent Name.",
                "topic-workspace.md": "Use `project repos create` with explicit `storage_profile`. Prepare `topic.repos.main.tmp` and `agent.tmp`. Runtime later consumes `agent.workspace` path plans. Missing semantic label evidence is a blocker.",
            }.get(subcommand_name, "")
            write(
                root / "skillset" / "operator" / "isomer-admin-topic-workspace-mgr" / "references" / subcommand_name,
                f"""
                # {subcommand_name}

                ## Workflow

                1. Run the fixture step and report any blocker.

                {fallback}
                {extra_terms}
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
            Do not require or inspect Topic Agent Team Profile material, team-profile material, roles, or agent count.

            ## Workflow

            1. Select one subcommand and report blockers.

            ## Subcommands

            Procedural Subcommands: `resolve-topic-workspace`, `read-env-gate`, `ensure-topic-repos`, `derive-env-gate`, `install-topic-deps`, and `verify-env-gate`.

            Misc Subcommands: `setup-topic-env` and `help`.

            Use {subcommand_links}.

            Commands include `pixi run --manifest-path <manifest_path> --environment <pixi_environment>`, `pixi add --manifest-path <manifest_path>`, and `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`.
            Use `.isomer-user-env/` only as fallback and block sudo.
            Report `semantic_paths` for `topic.workspace`, `topic.repos.main`, `topic.records`, `topic.runtime`, and any agent-scoped target; resolve the appropriate topic repository label before creating repos.
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
            "resolve-topic-workspace.md": "Do not block solely because `<topic-workspace>/team-profile/`; diagnostics are non-blocking for this subcommand unless they break env setup. Report `semantic_paths`, `topic.repos.main`, `topic.records`, `topic.runtime`, and each path source.",
            "ensure-topic-repos.md": "Use the resolved topic repository root from `semantic_paths`; report semantic label and path source. Do not place task repos outside the resolved root.",
            "read-env-gate.md": "Interpret the runnable target as what one agent or operator must run.",
            "setup-topic-env.md": "Do not require `team-profile/` before running this setup chain. Require `semantic_paths`, `topic.repos.main`, `topic.tmp`, and resolved `topic.tmp`; tmp material is local, ignored, disposable, not shared, and not durable evidence.",
            "verify-env-gate.md": "Do not require or verify `team-profile/` before reporting environment readiness.",
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

            Procedural Subcommands: `resolve-agent-env-context`, `require-topic-env-ready`, `read-agent-env-gate`, `plan-agent-workspaces`, `derive-agent-env-gate`, `ensure-topic-main-repository`, `create-agent-worktrees`, and `verify-agent-env-gate`.

            Misc Subcommands: `setup-agent-env` and `help`.

            Use {subcommand_links}.

            This fixture reads `user-intent/src/agent-env-gate.md`, writes `user-intent/derived/isomer-agent-env-gate.md`, prepares the Topic Main Repository at `topic.repos.main`, uses authoritative Agent Names, resolves `agent.workspace`, runs `pixi run --manifest-path <manifest_path> --environment <pixi_environment>`, records selected-agent partial evidence, Service Request refs, Provenance refs, and `overall_readiness_status`.

            Do not create per-agent Pixi manifests. Do not install or mutate Topic Workspace dependencies. Do not create Agent Instances or mutate Workspace Runtime records.
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
        path = root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "validate-topic-team.md"
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

    def test_operator_validator_requires_topic_workspace_manager(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        shutil.rmtree(root / "skillset" / "operator" / "isomer-admin-topic-workspace-mgr")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("isomer-admin-topic-workspace-mgr is required" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_workspace_subcommands(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_workspace_manager_skill(root, omit_subcommand="create-worktrees.md")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("create-worktrees.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_workspace_guardrail_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_workspace_manager_skill(root, omit_skill_term="Workspace Runtime")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("Workspace Runtime" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_workspace_semantic_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_workspace_manager_skill(root, omit_skill_term="semantic workspace labels")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("semantic workspace labels" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_workspace_semantic_reference_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_workspace_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        path = root / "skillset" / "operator" / "isomer-admin-topic-workspace-mgr" / "references" / "validate-worktrees.md"
        path.write_text(path.read_text(encoding="utf-8").replace("hard-coded default-only evidence", ""), encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("hard-coded default-only evidence" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_workspace_isomer_managed_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_workspace_manager_skill(root, omit_skill_term="isomer-managed/")
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("isomer-managed/" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_topic_workspace_agent_key_wording(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_workspace_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-admin-topic-workspace-mgr" / "SKILL.md"
        skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\nUse `<agent-key>` for public examples.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("agent-name public wording" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_topic_workspace_legacy_support_root_wording(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_workspace_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-admin-topic-workspace-mgr" / "SKILL.md"
        skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\nUse `.isomer-agent/` for current support.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any(".isomer-agent/" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_accepts_topic_env_setup_contract(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertEqual([], messages(diagnostics))

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
        self.write_topic_env_setup_service(root, omit_reference_term="Do not require `team-profile/`")
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

    def test_service_validator_requires_tmp_label_posture_reference_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="topic.tmp")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("topic.tmp" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_accepts_agent_env_setup_contract(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertEqual([], messages(diagnostics))

    def test_service_validator_requires_agent_env_setup_subcommands(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root, omit_subcommand="verify-agent-env-gate.md")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS003", codes(diagnostics))
        self.assertTrue(any("verify-agent-env-gate.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_agent_env_gate_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root, omit_skill_term="user-intent/src/agent-env-gate.md")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS003", codes(diagnostics))
        self.assertTrue(any("user-intent/src/agent-env-gate.md" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_agent_env_derived_gate_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root)
        self.write_agent_env_setup_service(root, omit_skill_term="user-intent/derived/isomer-agent-env-gate.md")

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS003", codes(diagnostics))
        self.assertTrue(any("user-intent/derived/isomer-agent-env-gate.md" in message for message in messages(diagnostics)), messages(diagnostics))

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
