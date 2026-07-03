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

            Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.

            ### Essential Output

            - Report the concise status, blockers, evidence, and next action.

            ### Complete Output

            - Include all bookkeeping, semantic refs, audit evidence, and handoff fields.
"""


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
        self.write_topic_team_dependency_contract(root)
        self.write_project_manager_skill(root)
        self.write_topic_creator_skill(root)
        self.write_topic_manager_skill(root)

    def write_topic_team_dependency_contract(self, root: Path) -> None:
        skill_dir = root / "skillset" / "operator" / "isomer-admin-topic-team-specialize"
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
            root / "skillset" / "operator" / "isomer-admin-project-mgr" / "SKILL.md",
            f"""
            ---
            name: isomer-admin-project-mgr
            description: Valid fixture project manager skill.
            ---

            # Isomer Admin Project Mgr

            ## Workflow

            1. **Default help mode**: If invoked without a prompt, run `help`.
            2. Select one subcommand and load only the selected subcommand page.
            3. Preserve `.isomer-labs/`, `.isomer-labs/.houmao/`, root `.houmao/` as external user-owned state, `isomer-content/`, `isomer-content/topic-ws/<topic-id>/`, `--content-dir <content-dir>`, `<content-dir>/topic-ws/<topic-id>/`, Isomer-managed Houmao overlay, `isomer-cli project init`, `isomer-cli project cleanup --part <part> --dry-run`, `isomer-cli project cleanup --part <part> --yes`, `--purge-content-root`, `isomer-cli project content-root move --to <content-dir> --dry-run`, `isomer-cli project content-root move --to <content-dir> --yes`, unknown files, `isomer-cli project validate`, `isomer-cli project doctor`, `isomer-cli project runtime init`, `isomer-cli project runtime prepare`, `isomer-admin-topic-creator`, `isomer-admin-topic-mgr`, and `isomer-admin-topic-team-specialize` boundaries.

            If the user's task does not map cleanly to these steps, use your native planning tool.

            ## Subcommands

            Use `references/help.md`, `references/init-project.md`, `references/cleanup-project.md`, `references/move-content.md`, `references/check-project.md`, `references/list-topics.md`, `references/show-context.md`, `references/init-runtime.md`, `references/prep-runtime.md`, `references/prepare-topic.md`, `references/manual-research.md`, and `references/specialize-team.md`.

            {OUTPUT_CONTRACT_FIXTURE}
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

    def write_topic_creator_skill(
        self,
        root: Path,
        *,
        omit_command: str | None = None,
        omit_skill_term: str | None = None,
    ) -> None:
        skill_dir = root / "skillset" / "operator" / "isomer-admin-topic-creator"
        command_links = ", ".join(f"`references/{command_name}`" for command_name in validator.TOPIC_CREATOR_COMMANDS)
        skill_text = f"""
            ---
            name: isomer-admin-topic-creator
            description: Valid fixture topic creator skill.
            ---

            # Isomer Admin Topic Creator

            Create a prepared Topic Workspace through Project Manifest-backed context, `topic.repos.main`, `topic.intent.overview`, `topic.intent.topic_env_requirements`, `topic.intent.actor_definitions`, `topic.env.actor_env_gates`, `topic.workspace.summary`, structured reset checkpoint, Workspace Runtime, Topic Actor roster, actor cwd, and actor onboarding.

            ## Workflow

            1. **Default help mode**: If invoked without a prompt, run `help`.
            2. Select one subcommand and load only that subcommand page.
            3. Preserve lower-level owner boundaries for `isomer-admin-project-mgr`, `isomer-srv-topic-env-setup`, `isomer-admin-topic-mgr`, and `isomer-admin-topic-team-specialize`.

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
              display_name: "isomer-admin-topic-creator"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-admin-topic-creator to validate this fixture."
            """,
        )
        for command_name in validator.TOPIC_CREATOR_COMMANDS:
            if command_name == omit_command:
                continue
            extra_terms = {
                "help.md": "Subcommand Functionalities. Procedural Subcommands. Helper Subcommands. Misc Subcommands. Default to **Essential Output** in chat. Print **Complete Output** only when the user asks for complete, verbose, audit, debug, full handoff, JSON, or full output.",
                "fast-forward.md": "`fast-forward` stops at the first blocker, routes through `define-topic-env` and `define-actors`, and ends at `finalize`.",
                "resolve-topic-input.md": "Resolve a concrete Research Topic and does not write `topic.intent.overview`.",
                "create-research-intent.md": "Write only `topic.intent.overview`; do not write `topic.intent.topic_env_requirements`.",
                "define-topic-env.md": "Create `topic.intent.topic_env_requirements`, wait for user verification, and report `fast-forward` assumptions.",
                "setup-topic-env.md": "Delegate to `isomer-srv-topic-env-setup`, read `topic.intent.topic_env_requirements`, derive `topic.env.topic_setup_target_spec`, and report `topic.repos.main` readiness.",
                "define-actors.md": "Create `topic.intent.actor_definitions` for the default `operator` and each actor source env gate.",
                "setup-actors.md": "Delegate to `isomer-admin-topic-mgr`, consume `topic.intent.actor_definitions`, report `topic.actors.workspace`, and verify `topic.env.actor_env_gates`.",
                "finalize.md": "Resolve `topic.workspace.summary`, run `isomer-cli project topic-reset checkpoint`, create a structured reset checkpoint from operator-level readiness evidence, report ready, verified, blocked, and skipped state. Do not recommend a next research step.",
                "step-by-step.md": "Follow the same main workflow order as `fast-forward`, show an option table with Recommended choices, and require acknowledgement.",
                "run-to.md": "Valid targets are procedural. The target is excluded by default, can be inclusive on request, and stops on missing user input.",
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
        skill_dir = root / "skillset" / "operator" / "isomer-admin-topic-mgr"
        if skill_dir.exists():
            shutil.rmtree(skill_dir)
        subcommand_links = ", ".join(
            f"`references/{subcommand_name}`" for subcommand_name in validator.TOPIC_MANAGER_SUBCOMMANDS
        )
        skill_terms = "\n".join(f"            {term}" for term in validator.TOPIC_MANAGER_REQUIRED_SKILL_TERMS)
        skill_text = f"""
            ---
            name: isomer-admin-topic-mgr
            description: Valid fixture topic manager skill.
            ---

            # Isomer Admin Topic Mgr

            Manage an initialized-topic after `isomer-admin-topic-creator` handoff. This fixture covers storage, actors, team topology, environment mutation, environment verification, reset checkpoint handling, diagnostics, and blocker reporting.

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
        write(root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "SKILL.md", skill_text)
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "agents" / "openai.yaml",
            """
            interface:
              display_name: "isomer-admin-topic-mgr"
              short_description: "Valid fixture"
              default_prompt: "Use $isomer-admin-topic-mgr to validate this fixture."
            """,
        )
        for subcommand_name in validator.TOPIC_MANAGER_SUBCOMMANDS:
            if subcommand_name == omit_subcommand:
                continue
            if subcommand_name == "help.md":
                write(
                    root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "references" / subcommand_name,
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
                root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "references" / subcommand_name,
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

            Procedural Subcommands: `resolve-topic-workspace`, `read-env-gate`, `derive-env-gate`, `ensure-topic-main-repository`, `ensure-topic-repos`, `project-extern-repos`, `install-topic-deps`, and `verify-env-gate`.

            Misc Subcommands: `setup-topic-env` and `help`.

            Use {subcommand_links}.

            Commands include `pixi run --manifest-path <manifest_path> --environment <pixi_environment>`, `pixi add --manifest-path <manifest_path>`, and `pixi install --manifest-path <manifest_path> --environment <pixi_environment>`.
            Use `.isomer-user-env/` only as fallback and block sudo.
            Report `semantic_paths` for `topic.workspace`, `topic.repos.main`, `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, `topic.repos.main.projections.manifest`, `topic.records`, `topic.runtime`, `topic.intent.topic_env_requirements`, and `topic.env.topic_setup_target_spec`; accept an explicit manual target spec; produce Topic Workspace predecessor evidence, Topic Main Development Repository Git state, external repo projection evidence, and `per_agent_readiness_status` when per-agent readiness is not checked. Also resolve the appropriate topic repository label before creating repos.
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
            "ensure-topic-repos.md": "Use resolved non-main `topic.repos.*` paths from `semantic_paths`; report semantic label, path, and path source. Keep existing canonical external repos read-only by default. Do not place task repos outside the resolved semantic path, and default helper-created repos under `repos/extern/...`.",
            "project-extern-repos.md": "Create external repo projection entries under `topic.repos.main.projections.readonly` or `topic.repos.main.projections.writable`, track metadata in `topic.repos.main.projections.manifest`, and distinguish read-only projections from writable projections.",
            "read-env-gate.md": "Resolve and read `topic.intent.topic_env_requirements`. Interpret the runnable target as what one agent or operator must run.",
            "derive-env-gate.md": "Write `topic.env.topic_setup_target_spec` or validate an explicit manual target spec. Include `## Gate Checklist`, `- [ ]`, and `- [x]`. Define the required readiness work contract with a pass condition, evidence source, optional diagnostics outside the checklist, and blocker condition. Preserve every source-intent runnable target and use bounded real-path verification; consult `isomer-misc-bounded-run-tips`, record `classification_source`, `classification_result`, `classification_reason`, `resource_dimensions`, `unknown-risk`, the bounded-run guidance source, and use generic best-effort judgment only when no recipe applies. A simple smoke test that misses the source path is insufficient unless the user explicitly records a downgrade. Consult `isomer-misc-pkg-specifics` before generic package routing and record `no package-specific rule` when no page exists.",
            "install-topic-deps.md": "Read `topic.env.topic_setup_target_spec` and require enclosure strategy plus classification evidence, `unknown-risk`, bounded-run guidance source, generic best-effort fallback evidence when used, and bounded real setup path decisions. Use `isomer-misc-pkg-specifics` evidence or `no package-specific rule` from the target spec before package mutation.",
            "setup-topic-env.md": "Do not require `team-profile/` before running this setup chain. Require `semantic_paths`, `topic.repos.main`, `ensure-topic-main-repository`, `project-extern-repos`, `AGENTS.md`, `CLAUDE.md`, agent guidance posture, guidance block version, `topic.tmp`, and resolved `topic.tmp`; tmp material is local, ignored, disposable, not shared, and not durable evidence. Report `per_agent_readiness_status: not checked` and Do not read `topic.intent.agent_env_requirements`. Use bounded real-path verification; a generic smoke test is not enough.",
            "verify-env-gate.md": "Do not require or verify `team-profile/` before reporting environment readiness. per-Agent Workspace cwd verification is not checked here. Report Topic Workspace predecessor evidence, Topic Main Development Repository evidence, projection evidence, bounded real-path coverage, operation classification evidence, `unknown-risk`, bounded-run guidance source, generic best-effort fallback evidence when used, source-intent runnable target coverage, every required `## Gate Checklist` item checked with supporting evidence, the exact checklist item when blocked, failed, or not checked, any weaker smoke test limitation, any user downgrade, `isomer-misc-pkg-specifics`, and `no package-specific rule`.",
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

            Do not initialize, repair, or configure the Topic Main Development Repository. Do not create per-agent Pixi manifests. Do not install or mutate Topic Workspace dependencies. Do not create Agent Instances or mutate Workspace Runtime records.

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

    def test_operator_validator_accepts_topic_team_specialization_contract(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)

        diagnostics = validator.validate_operator_skillset(root)

        self.assertEqual([], messages(diagnostics))

    def test_operator_validator_requires_split_output_contract_trigger(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "SKILL.md"
        skill_path.write_text(
            skill_path.read_text(encoding="utf-8").replace(
                "complete, verbose, audit, debug, full handoff, JSON, or full output",
                "complete output",
            ),
            encoding="utf-8",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("complete, verbose, audit, debug, full handoff, JSON, or full output" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_complete_output_as_default(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "SKILL.md"
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
        reference_path = root / "skillset" / "operator" / "isomer-admin-topic-team-specialize" / "references" / "help.md"
        reference_path.write_text(
            reference_path.read_text(encoding="utf-8")
            + "\n## Output Contract\n\nDefault to **Essential Output** in chat.\n\n### Essential Output\n\n- Fixture summary.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS007", codes(diagnostics))
        self.assertTrue(any("Complete Output" in message for message in messages(diagnostics)), messages(diagnostics))

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

    def test_operator_validator_rejects_core_owned_heavy_operation_lists(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        subcommand_path = (
            root
            / "skillset"
            / "operator"
            / "isomer-admin-topic-team-specialize"
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
            / "isomer-admin-topic-team-specialize"
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
            / "isomer-admin-topic-team-specialize"
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
            / "isomer-admin-topic-team-specialize"
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
            / "isomer-admin-topic-team-specialize"
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

            1. Run `isomer-cli --project <project-root> validate`.

            If the user's task does not map cleanly to these steps, use your native planning tool.
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS005", codes(diagnostics))
        self.assertTrue(any("isomer-cli project ..." in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_repo_local_isomer_cli_wrapper(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_project_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-admin-project-mgr" / "references" / "check-project.md"
        skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\nRun `pixi run isomer-cli project validate`.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS010", codes(diagnostics))
        self.assertTrue(any("global isomer-cli directly" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        shutil.rmtree(root / "skillset" / "operator" / "isomer-admin-topic-mgr")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("isomer-admin-topic-mgr is required" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_creator(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        shutil.rmtree(root / "skillset" / "operator" / "isomer-admin-topic-creator")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS008", codes(diagnostics))
        self.assertTrue(any("isomer-admin-topic-creator is required" in message for message in messages(diagnostics)), messages(diagnostics))

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
            root / "skillset" / "operator" / "isomer-admin-topic-creator" / "references" / "define-topic.md",
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
            root / "skillset" / "operator" / "isomer-admin-topic-creator" / "references" / "start-manual-research.md",
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
            root / "skillset" / "operator" / "isomer-admin-topic-prepare" / "SKILL.md",
            """
            ---
            name: isomer-admin-topic-prepare
            description: Retired fixture.
            ---

            # Retired
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("isomer-admin-topic-prepare is no longer part of the active operator skillset" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_retired_topic_workspace_manager_folder(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_deepsci_mini_guide(root)
        write(
            root / "skillset" / "operator" / "isomer-admin-topic-workspace-mgr" / "SKILL.md",
            """
            ---
            name: isomer-admin-topic-workspace-mgr
            description: Retired fixture.
            ---

            # Retired
            """,
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS003", codes(diagnostics))
        self.assertTrue(any("isomer-admin-topic-workspace-mgr is no longer part of the active operator skillset" in message for message in messages(diagnostics)), messages(diagnostics))

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
        path = root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "references" / "team-validate-workspaces.md"
        path.write_text(path.read_text(encoding="utf-8").replace("hard-coded default-only evidence", ""), encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("hard-coded default-only evidence" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager_package_specific_terms(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        path = root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "references" / "env-install-packages.md"
        path.write_text(path.read_text(encoding="utf-8").replace("isomer-misc-pkg-specifics", ""), encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("isomer-misc-pkg-specifics" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_requires_topic_manager_package_specific_evidence_output(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        path = root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "references" / "env-update-packages.md"
        path.write_text(path.read_text(encoding="utf-8").replace("package_specifics", ""), encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("package_specifics" in message for message in messages(diagnostics)), messages(diagnostics))

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
        reset_path = root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "references" / "reset-plan.md"
        reset_path.write_text(reset_path.read_text(encoding="utf-8") + "\nWhen topic-reset is stale, run `git stash` before planning.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("must not recommend Git reset" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_research_paradigm_routing_in_reset_guidance(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        reset_path = root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "references" / "reset-inspect.md"
        reset_path.write_text(reset_path.read_text(encoding="utf-8") + "\nFor reset checkpoint inspection, route to skillset/research-paradigm/v2 first.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("must not route to or depend on research-paradigm" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_topic_manager_agent_key_wording(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "SKILL.md"
        skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\nUse `<agent-key>` for public examples.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("agent-name public wording" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_operator_validator_rejects_topic_manager_legacy_support_root_wording(self) -> None:
        root = self.make_root()
        self.write_topic_team_specialization_skill(root)
        self.write_topic_manager_skill(root)
        self.write_deepsci_mini_guide(root)
        skill_path = root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "SKILL.md"
        skill_path.write_text(skill_path.read_text(encoding="utf-8") + "\nUse `.isomer-agent/` for current support.\n", encoding="utf-8")

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any(".isomer-agent/" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_topic_manager_validator_requires_topic_main_agent_guidance_terms(self) -> None:
        root = self.make_root()
        self.write_topic_manager_skill(root)
        path = root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "references" / "storage-inspect-main.md"
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
        path = root / "skillset" / "operator" / "isomer-admin-topic-mgr" / "references" / "storage-inspect-main.md"
        path.write_text(
            path.read_text(encoding="utf-8") + "\nThis repository is an Isomer Topic Main Development Repository.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_operator_skillset(root)

        self.assertIn("OPS006", codes(diagnostics))
        self.assertTrue(any("copying the rendered block body" in message for message in messages(diagnostics)), messages(diagnostics))

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
                "complete, verbose, audit, debug, full handoff, JSON, or full output",
                "complete output",
            ),
            encoding="utf-8",
        )

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("complete, verbose, audit, debug, full handoff, JSON, or full output" in message for message in messages(diagnostics)), messages(diagnostics))

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

    def test_service_validator_requires_topic_env_predecessor_boundary_terms(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_skill_term="Topic Workspace predecessor evidence")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("Topic Workspace predecessor evidence" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_service_validator_requires_per_agent_readiness_not_checked_reference(self) -> None:
        root = self.make_root()
        self.write_topic_env_setup_service(root, omit_reference_term="per_agent_readiness_status: not checked")
        self.write_agent_env_setup_service(root)

        diagnostics = validator.validate_service_skillset(root)

        self.assertIn("SVS002", codes(diagnostics))
        self.assertTrue(any("per_agent_readiness_status: not checked" in message for message in messages(diagnostics)), messages(diagnostics))

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
