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
