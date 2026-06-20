from __future__ import annotations

import contextlib
import json
import os
import tempfile
import textwrap
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

import click
from click.testing import CliRunner

from isomer_labs import cli


REPO_ROOT = Path(__file__).resolve().parents[2]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class IsomerCliTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def run_cli(
        self,
        args: list[str],
        *,
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
    ) -> tuple[int, str]:
        root = cwd or self.make_root()
        runner = CliRunner()
        with contextlib.chdir(root), patch.dict(os.environ, env or {}, clear=True):
            result = runner.invoke(cli.app, args, standalone_mode=False)
        if result.exception is not None:
            raise result.exception
        return int(result.return_value or 0), result.output

    def init_project(self, root: Path, topic_id: str = "default") -> None:
        status, output = self.run_cli(["--project", str(root), "init", topic_id], cwd=root)
        self.assertEqual(0, status, output)

    def make_two_topic_project(self, root: Path) -> None:
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [defaults]
            research_topic_id = "alpha"
            topic_workspace_id = "alpha"

            [[research_topics]]
            id = "alpha"
            config_path = ".isomer-labs/research-topics/alpha.toml"
            topic_workspace_id = "alpha"
            status = "active"

            [[research_topics]]
            id = "beta"
            config_path = ".isomer-labs/research-topics/beta.toml"
            topic_workspace_id = "beta"
            status = "active"

            [[topic_workspaces]]
            id = "alpha"
            research_topic_id = "alpha"
            path = "topic-workspaces/alpha"
            status = "active"

            [[topic_workspaces]]
            id = "beta"
            research_topic_id = "beta"
            path = "topic-workspaces/beta"
            status = "active"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            topic_statement = "Alpha topic"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "beta.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "beta"
            topic_statement = "Beta topic"
            """,
        )
        (root / "topic-workspaces" / "alpha").mkdir(parents=True)
        (root / "topic-workspaces" / "beta").mkdir(parents=True)

    def test_help_and_project_script_metadata_expose_command_surface(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli.app, ["--help"])
        self.assertEqual(0, result.exit_code, result.output)
        self.assertIsInstance(cli.app, click.Group)
        self.assertIsInstance(cli.build_parser(), click.Group)
        help_text = result.output
        for command in (
            "init",
            "validate",
            "topics list",
            "workspaces list",
            "context show",
            "paths preview",
            "schemas list",
            "team-templates",
            "team-profiles",
        ):
            self.assertIn(command, help_text)
        pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual("isomer_labs.cli:main", pyproject["project"]["scripts"]["isomer-cli"])

    def test_init_creates_minimal_default_project_and_refuses_overwrite(self) -> None:
        root = self.make_root()
        status, output = self.run_cli(["init"], cwd=root)
        self.assertEqual(0, status, output)
        self.assertTrue((root / ".isomer-labs" / "manifest.toml").is_file())
        self.assertTrue((root / ".isomer-labs" / "research-topics" / "default.toml").is_file())
        self.assertTrue((root / "topic-workspaces" / "default").is_dir())
        self.assertFalse((root / "topic-workspaces" / "default" / "state.sqlite").exists())
        self.assertFalse((root / "topic-workspaces" / "default" / "artifacts").exists())
        help_result = CliRunner().invoke(cli.app, ["init", "--help"])
        self.assertEqual(0, help_result.exit_code, help_result.output)
        self.assertNotIn("--force", help_result.output)

        status, output = self.run_cli(["init"], cwd=root)
        self.assertEqual(1, status)
        self.assertIn("refuses to overwrite", output)

    def test_init_uses_explicit_topic_id_consistently(self) -> None:
        root = self.make_root()
        status, output = self.run_cli(["init", "paper"], cwd=root)
        self.assertEqual(0, status, output)
        manifest = (root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8")
        topic_config = (root / ".isomer-labs" / "research-topics" / "paper.toml").read_text(encoding="utf-8")
        self.assertIn('id = "paper"', manifest)
        self.assertIn('config_path = ".isomer-labs/research-topics/paper.toml"', manifest)
        self.assertIn('path = "topic-workspaces/paper"', manifest)
        self.assertIn('research_topic_id = "paper"', topic_config)
        self.assertTrue((root / "topic-workspaces" / "paper").is_dir())

    def test_validate_reports_valid_project_as_versioned_json(self) -> None:
        root = self.make_root()
        self.init_project(root)
        status, output = self.run_cli(["--project", str(root), "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertEqual("isomer-cli-output.v1", data["output_schema_version"])
        self.assertEqual([], data["diagnostics"])
        self.assertEqual("default", data["manifest"]["defaults"]["research_topic_id"])

    def test_common_options_work_at_root_and_command_level(self) -> None:
        root = self.make_root()
        self.init_project(root)

        status, output = self.run_cli(["--project", str(root), "validate", "--json"], cwd=root)
        root_level = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(root_level["ok"])

        status, output = self.run_cli(["validate", "--project", str(root), "--json"], cwd=root)
        command_level = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(command_level["ok"])
        self.assertEqual(root_level["project"]["root"], command_level["project"]["root"])

    def test_missing_and_malformed_projects_are_rejected(self) -> None:
        missing_root = self.make_root()
        status, output = self.run_cli(["validate", "--json"], cwd=missing_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("ISO001", data["diagnostics"][0]["code"])

        malformed_root = self.make_root()
        write(malformed_root / ".isomer-labs" / "manifest.toml", "this is not = valid toml =\n")
        status, output = self.run_cli(["validate", "--json"], cwd=malformed_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("ISO002", data["diagnostics"][0]["code"])

    def test_validation_reports_duplicates_mismatch_external_paths_and_secret_fields(self) -> None:
        root = self.make_root()
        secret_value = "SHOULD_NOT_LEAK"
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"
            api_key = "SHOULD_NOT_LEAK"

            [defaults]
            research_topic_id = "dup"

            [[research_topics]]
            id = "dup"
            config_path = ".isomer-labs/research-topics/dup.toml"
            topic_workspace_id = "dup"

            [[research_topics]]
            id = "dup"
            config_path = ".isomer-labs/research-topics/dup.toml"
            topic_workspace_id = "dup"

            [[topic_workspaces]]
            id = "dup"
            research_topic_id = "dup"
            path = "../outside"

            [[topic_workspaces]]
            id = "dup"
            research_topic_id = "dup"
            path = "topic-workspaces/dup"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "dup.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "other"
            token = "SHOULD_NOT_LEAK"
            run_status = "done"
            """,
        )
        status, output = self.run_cli(["validate", "--json"], cwd=root)
        data = json.loads(output)
        codes = {diagnostic["code"] for diagnostic in data["diagnostics"]}
        self.assertEqual(1, status)
        self.assertTrue({"ISO004", "ISO005", "ISO007", "ISO009", "ISO010"} <= codes, data["diagnostics"])
        self.assertNotIn(secret_value, output)

    def test_context_selection_precedence_and_conflicts_are_reported(self) -> None:
        root = self.make_root()
        self.make_two_topic_project(root)
        write(
            root / ".isomer-labs" / "local.toml",
            """
            schema_version = "isomer-local-active-context.v1"
            research_topic_id = "alpha"
            """,
        )

        status, output = self.run_cli(
            ["context", "show", "--topic", "alpha", "--json"],
            cwd=root,
            env={"ISOMER_RESEARCH_TOPIC_ID": "beta"},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("alpha", data["context"]["research_topic_id"])
        self.assertEqual("explicit selector", data["context"]["sources"]["research_topic_id"])

        status, output = self.run_cli(
            ["context", "show", "--json"],
            cwd=root / "topic-workspaces" / "beta",
            env={"ISOMER_RESEARCH_TOPIC_ID": "alpha"},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("beta", data["context"]["research_topic_id"])
        self.assertEqual("current directory", data["context"]["sources"]["research_topic_id"])

        status, output = self.run_cli(["context", "show", "--json"], cwd=root, env={"ISOMER_RESEARCH_TOPIC_ID": "beta"})
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("beta", data["context"]["research_topic_id"])
        self.assertEqual("environment", data["context"]["sources"]["research_topic_id"])

        status, output = self.run_cli(["context", "show", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("alpha", data["context"]["research_topic_id"])
        self.assertEqual(".isomer-labs/local.toml", data["context"]["sources"]["research_topic_id"])

        status, output = self.run_cli(["context", "show", "--topic", "alpha", "--topic-workspace", "beta", "--json"], cwd=root)
        data = json.loads(output)
        codes = {diagnostic["code"] for diagnostic in data["diagnostics"]}
        self.assertEqual(1, status)
        self.assertIn("ISO012", codes)

    def test_lifecycle_refs_are_bounded_milestone_one_warnings(self) -> None:
        root = self.make_root()
        self.init_project(root)
        status, output = self.run_cli(["context", "show", "--run", "run-1", "--json"], cwd=root)
        data = json.loads(output)
        diagnostics = data["diagnostics"]
        self.assertEqual(0, status, output)
        self.assertEqual("warning", diagnostics[0]["severity"])
        self.assertEqual("ISO015", diagnostics[0]["code"])

    def test_paths_preview_reports_sources_and_is_side_effect_free(self) -> None:
        root = self.make_root()
        self.init_project(root)
        status, output = self.run_cli(
            ["paths", "preview", "--json"],
            cwd=root,
            env={"ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR": "topic-workspaces/default/custom-artifacts"},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        paths = {entry["surface"]: entry for entry in data["paths"]}
        self.assertEqual("env", paths["artifacts"]["source"])
        self.assertEqual("ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR", paths["artifacts"]["source_detail"])
        self.assertNotIn("plan", {entry["source"] for entry in data["paths"]})
        self.assertFalse((root / "topic-workspaces" / "default" / "state.sqlite").exists())
        self.assertFalse((root / "topic-workspaces" / "default" / "artifacts").exists())
        self.assertFalse((root / "topic-workspaces" / "default" / "custom-artifacts").exists())

        status, output = self.run_cli(
            ["paths", "preview", "--json"],
            cwd=root,
            env={"ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR": "../outside"},
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO005", {diagnostic["code"] for diagnostic in data["diagnostics"]})

    def test_topics_workspaces_and_schemas_list_use_declared_sources(self) -> None:
        root = self.make_root()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [defaults]
            research_topic_id = "alpha"

            [[research_topics]]
            id = "alpha"
            config_path = ".isomer-labs/research-topics/alpha.toml"
            topic_workspace_id = "alpha"

            [[research_topics]]
            id = "beta"
            config_path = ".isomer-labs/research-topics/beta.toml"

            [[topic_workspaces]]
            id = "alpha"
            research_topic_id = "alpha"
            path = "topic-workspaces/alpha"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "beta.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "beta"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "unregistered.toml",
            """
            research_topic_id = "unregistered"
            """,
        )

        status, output = self.run_cli(["topics", "list", "--json"], cwd=root)
        topics = json.loads(output)["topics"]
        self.assertEqual(0, status, output)
        self.assertEqual(["alpha", "beta"], [topic["id"] for topic in topics])

        status, output = self.run_cli(["workspaces", "list", "--json"], cwd=root)
        workspaces = json.loads(output)["workspaces"]
        self.assertEqual(0, status, output)
        self.assertEqual({"alpha", "beta"}, {workspace["id"] for workspace in workspaces})
        beta = next(workspace for workspace in workspaces if workspace["id"] == "beta")
        self.assertEqual("default", beta["source"])
        self.assertEqual("topic-workspaces/beta", beta["effective_path"])

        status, output = self.run_cli(["schemas", "list", "--json"], cwd=root)
        schemas = json.loads(output)["schemas"]
        names = {schema["name"] for schema in schemas}
        self.assertEqual(0, status, output)
        self.assertIn("isomer-project-manifest", names)
        self.assertFalse(any("openspec" in name.lower() for name in names))
        self.assertNotIn("implement-isomer-cli-project-discovery", output)

    def make_deepsci_profile_project(self, root: Path) -> None:
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [defaults]
            research_topic_id = "alpha"
            domain_agent_team_template_id = "deepsci-org"
            topic_agent_team_profile_id = "uc-01-alpha"

            [[research_topics]]
            id = "alpha"
            config_path = ".isomer-labs/research-topics/alpha.toml"
            topic_workspace_id = "alpha"

            [[research_topics]]
            id = "beta"
            config_path = ".isomer-labs/research-topics/beta.toml"
            topic_workspace_id = "beta"

            [[topic_workspaces]]
            id = "alpha"
            research_topic_id = "alpha"
            path = "topic-workspaces/alpha"

            [[topic_workspaces]]
            id = "beta"
            research_topic_id = "beta"
            path = "topic-workspaces/beta"

            [[topic_agent_team_profiles]]
            id = "uc-01-alpha"
            path = ".isomer-labs/team-profiles/uc-01-alpha.toml"
            domain_agent_team_template_id = "deepsci-org"
            research_topic_id = "alpha"

            [[topic_agent_team_profiles]]
            id = "uc-02-beta"
            path = ".isomer-labs/team-profiles/uc-02-beta.toml"
            domain_agent_team_template_id = "deepsci-org"
            research_topic_id = "beta"

            [[topic_agent_team_profiles]]
            id = "uc-03-alpha"
            path = ".isomer-labs/team-profiles/uc-03-alpha.toml"
            domain_agent_team_template_id = "deepsci-org"
            research_topic_id = "alpha"

            [[topic_agent_team_profiles]]
            id = "uc-05-beta"
            path = ".isomer-labs/team-profiles/uc-05-beta.toml"
            domain_agent_team_template_id = "deepsci-org"
            research_topic_id = "beta"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            topic_statement = "Explore a new direction"
            default_domain_agent_team_template_id = "deepsci-org"
            default_topic_agent_team_profile_id = "uc-01-alpha"
            coordination_policy_ref = "coordination-policy:alpha-manual"
            gate_policy_ref = "gate-policy:alpha-human-return"
            baseline_waiver_policy_ref = "baseline-waiver-policy:alpha"

            [capability_binding_refs]
            default = "capability-binding:alpha-default"

            [skill_binding_projection_refs]
            default = "skill-projection:alpha-default"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "beta.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "beta"
            topic_statement = "Optimize a baseline"
            default_domain_agent_team_template_id = "deepsci-org"
            default_topic_agent_team_profile_id = "uc-02-beta"
            coordination_policy_ref = "coordination-policy:beta-manual"
            gate_policy_ref = "gate-policy:beta-human-return"
            scheduler_policy_ref = "scheduler-policy:beta"
            """,
        )
        write(root / ".isomer-labs" / "team-profiles" / "uc-01-alpha.toml", self.profile_fixture("uc-01-alpha", "alpha", "UC-01"))
        write(root / ".isomer-labs" / "team-profiles" / "uc-02-beta.toml", self.profile_fixture("uc-02-beta", "beta", "UC-02"))
        write(root / ".isomer-labs" / "team-profiles" / "uc-03-alpha.toml", self.profile_fixture("uc-03-alpha", "alpha", "UC-03"))
        write(root / ".isomer-labs" / "team-profiles" / "uc-05-beta.toml", self.profile_fixture("uc-05-beta", "beta", "UC-05", automatic=True))
        (root / "topic-workspaces" / "alpha").mkdir(parents=True)
        (root / "topic-workspaces" / "beta").mkdir(parents=True)

    def profile_fixture(
        self,
        profile_id: str,
        topic_id: str,
        use_case: str,
        *,
        automatic: bool = False,
        workspace_topic_id: str | None = None,
        runtime_truth: bool = False,
        missing_fanout: bool = False,
    ) -> str:
        workspace_topic = workspace_topic_id or topic_id
        execution_mode = "automatic" if automatic else "manual"
        automatic_policy = 'automatic_mode_policy_ref = "automatic-mode-policy:test"\n' if automatic else ""
        runtime_line = 'run_status = "done"\n' if runtime_truth else ""
        roles = [
            ("deepsci-org-master", ["isomer-rsch-shared", "isomer-rsch-intake", "isomer-rsch-decision", "isomer-rsch-finalize"], ["isomer-rsch-review"]),
            ("deepsci-org-framer", ["isomer-rsch-shared", "isomer-rsch-scout", "isomer-rsch-baseline"], ["isomer-rsch-science", "isomer-rsch-paper-outline"]),
            ("deepsci-org-designer", ["isomer-rsch-shared", "isomer-rsch-idea", "isomer-rsch-optimize"], ["isomer-rsch-scout"]),
            ("deepsci-org-experimenter", ["isomer-rsch-shared", "isomer-rsch-experiment", "isomer-rsch-science"], ["isomer-rsch-analysis"]),
            ("deepsci-org-analyzer", ["isomer-rsch-shared", "isomer-rsch-analysis", "isomer-rsch-science"], ["isomer-rsch-paper-plot", "isomer-rsch-figure-polish"]),
            ("deepsci-org-publisher", ["isomer-rsch-shared", "isomer-rsch-paper-outline", "isomer-rsch-write", "isomer-rsch-paper-plot", "isomer-rsch-figure-polish"], ["nature-data", "nature-figure", "nature-paper2ppt", "nature-polishing"]),
            ("deepsci-org-reviewer", ["isomer-rsch-shared", "isomer-rsch-review", "isomer-rsch-rebuttal", "isomer-rsch-analysis"], ["isomer-rsch-scout"]),
        ]
        role_blocks = []
        for role_id, required, optional in roles:
            role_blocks.append(
                f"""
                [[role_bindings]]
                role_id = "{role_id}"
                active = true
                agent_profile_ref = "{profile_id}:{role_id}:agent-profile"
                capability_binding_ref = "{profile_id}:{role_id}:capability-binding"
                skill_binding_projection_ref = "{profile_id}:{role_id}:skill-binding-projection"
                agent_workspace_ref = "topic-workspaces/{workspace_topic}/agent-workspaces/{profile_id}/{role_id}"
                required_skills = {json.dumps(required)}
                optional_skills = {json.dumps(optional)}
                """
            )
        fanout = ""
        if not missing_fanout:
            fanout = f"""
                [[fanout_policies]]
                role_id = "deepsci-org-experimenter"
                parallel_execution_scope = "research_task"
                max_shards = 2
                allocation_rule = "{profile_id}:experimenter-shards"

                [[fanout_policies]]
                role_id = "deepsci-org-analyzer"
                parallel_execution_scope = "research_task"
                max_shards = 2
                allocation_rule = "{profile_id}:analyzer-shards"
                """
        return textwrap.dedent(
            f"""
            schema_version = "isomer-topic-agent-team-profile.v1"
            id = "{profile_id}"
            domain_agent_team_template_id = "deepsci-org"
            research_topic_id = "{topic_id}"
            topic_workspace_id = "{topic_id}"
            coordination_policy_ref = "coordination-policy:{topic_id}"
            gate_policy_ref = "gate-policy:{topic_id}"
            baseline_waiver_policy_ref = "baseline-waiver-policy:{topic_id}"
            default_execution_mode = "{execution_mode}"
            {automatic_policy}reviewer_read_access_policy = "promoted-artifacts-only"
            expected_artifacts = ["{use_case}:research-plan", "{use_case}:evidence-summary"]
            constraints = ["use_case:{use_case}"]
            {runtime_line}
            {"".join(role_blocks)}
            {fanout}
            """
        )

    def test_team_templates_cli_commands_are_deterministic(self) -> None:
        status, output = self.run_cli(["team-templates", "list", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["deepsci-org"], [template["id"] for template in data["templates"]])
        self.assertEqual("valid", data["templates"][0]["validation_status"])

        status, output = self.run_cli(["team-templates", "inspect", "deepsci-org", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(7, len(data["template"]["roles"]))
        self.assertIn("deepsci-org-reviewer", {role["id"] for role in data["template"]["roles"]})

        status, output = self.run_cli(["team-templates", "validate", "missing-template", "--json"])
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("ISO016", data["diagnostics"][0]["code"])

    def test_profile_manifest_context_specialize_and_validate(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)

        status, output = self.run_cli(["validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])

        status, output = self.run_cli(["context", "show", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("deepsci-org", data["context"]["domain_agent_team_template_id"])
        self.assertEqual("uc-01-alpha", data["context"]["topic_agent_team_profile_id"])
        self.assertEqual("coordination-policy:alpha-manual", data["context"]["profile_refs"]["coordination_policy_ref"])

        status, output = self.run_cli(
            ["team-profiles", "specialize", "--topic", "alpha", "--profile-id", "preview-alpha", "--use-case", "UC-01", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("preview-alpha", data["profile"]["id"])
        self.assertEqual("research-inquiry-map", data["profile"]["expected_artifacts"][0])
        self.assertIsNone(data["written_path"])

        status, output = self.run_cli(
            ["team-profiles", "validate", ".isomer-labs/team-profiles/uc-01-alpha.toml", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])

    def test_profile_validation_rejects_isolation_and_runtime_truth(self) -> None:
        root = self.make_root()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [defaults]
            research_topic_id = "alpha"
            topic_agent_team_profile_id = "dup"

            [[research_topics]]
            id = "alpha"
            config_path = ".isomer-labs/research-topics/alpha.toml"
            topic_workspace_id = "alpha"

            [[research_topics]]
            id = "beta"
            config_path = ".isomer-labs/research-topics/beta.toml"
            topic_workspace_id = "beta"

            [[topic_workspaces]]
            id = "alpha"
            research_topic_id = "alpha"
            path = "topic-workspaces/alpha"

            [[topic_workspaces]]
            id = "beta"
            research_topic_id = "beta"
            path = "topic-workspaces/beta"

            [[topic_agent_team_profiles]]
            id = "dup"
            path = ".isomer-labs/team-profiles/dup.toml"
            domain_agent_team_template_id = "deepsci-org"
            research_topic_id = "alpha"

            [[topic_agent_team_profiles]]
            id = "dup"
            path = ".isomer-labs/team-profiles/dup-beta.toml"
            domain_agent_team_template_id = "deepsci-org"
            research_topic_id = "beta"

            [[topic_agent_team_profiles]]
            id = "workspace-local"
            path = "topic-workspaces/alpha/teams/workspace-local.toml"
            domain_agent_team_template_id = "deepsci-org"
            research_topic_id = "alpha"
            """,
        )
        write(root / ".isomer-labs" / "research-topics" / "alpha.toml", 'research_topic_id = "alpha"\ndefault_topic_agent_team_profile_id = "dup"\n')
        write(root / ".isomer-labs" / "research-topics" / "beta.toml", 'research_topic_id = "beta"\n')
        write(root / ".isomer-labs" / "team-profiles" / "dup.toml", self.profile_fixture("dup", "alpha", "UC-01", workspace_topic_id="beta", runtime_truth=True, missing_fanout=True))
        write(root / ".isomer-labs" / "team-profiles" / "dup-beta.toml", self.profile_fixture("dup", "beta", "UC-02"))

        status, output = self.run_cli(["validate", "--json"], cwd=root)
        data = json.loads(output)
        codes = {diagnostic["code"] for diagnostic in data["diagnostics"]}
        self.assertEqual(1, status)
        self.assertTrue({"ISO004", "ISO009", "ISO019", "ISO020"} <= codes, data["diagnostics"])
