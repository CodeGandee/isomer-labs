from __future__ import annotations

import contextlib
import json
import os
import shutil
import subprocess
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
FIXTURE_PROJECT = REPO_ROOT / "tests" / "fixtures" / "projects" / "deepsci-profile-use-cases"
FIXTURE_PROFILE_IDS = (
    "uc-01-novel-biomarker",
    "uc-02-baseline-optimizer",
    "uc-03-novel-biomarker-revision",
    "uc-05-baseline-optimizer-mixed",
)


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

    def copy_fixture_project(self, name: str = "fixture-project") -> Path:
        root = self.make_root() / name
        shutil.copytree(FIXTURE_PROJECT, root)
        return root

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

    def add_project_pixi_manifest(
        self,
        root: Path,
        *,
        environments: tuple[str, ...] = (),
        requires_pixi: str | None = None,
        lockfile: bool = False,
    ) -> None:
        workspace_lines = [
            "[tool.pixi.workspace]",
            'channels = ["conda-forge"]',
            'platforms = ["linux-64"]',
        ]
        if requires_pixi is not None:
            workspace_lines.append(f'requires-pixi = "{requires_pixi}"')
        env_lines = ["[tool.pixi.environments]"]
        env_lines.extend(f'"{environment}" = ["default"]' for environment in environments)
        write(
            root / "pyproject.toml",
            "\n".join(
                [
                    "[project]",
                    'name = "fixture"',
                    'version = "0.1.0"',
                    "",
                    *workspace_lines,
                    "",
                    *env_lines,
                    "",
                ]
            ),
        )
        if lockfile:
            write(root / "pixi.lock", "version: 1\n")

    def append_manifest(self, root: Path, content: str) -> None:
        manifest_path = root / ".isomer-labs" / "manifest.toml"
        current = manifest_path.read_text(encoding="utf-8")
        manifest_path.write_text(current + "\n" + textwrap.dedent(content).lstrip(), encoding="utf-8")

    def patch_pixi(
        self,
        *,
        path: str | None = "/usr/bin/pixi",
        version_returncode: int = 0,
        requires_returncode: int = 0,
    ):
        def fake_run(args: list[str], **_: object) -> subprocess.CompletedProcess[str]:
            if args[1:] == ["--version"]:
                return subprocess.CompletedProcess(args, version_returncode, stdout="pixi 0.99.0\n", stderr="")
            if args[1:4] == ["workspace", "requires-pixi", "verify"]:
                return subprocess.CompletedProcess(args, requires_returncode, stdout="", stderr="")
            return subprocess.CompletedProcess(args, 2, stdout="", stderr="unexpected command")

        return (
            patch("isomer_labs.doctor.shutil.which", return_value=path),
            patch("isomer_labs.doctor.subprocess.run", side_effect=fake_run),
        )

    def check(self, data: dict[str, object], check_id: str) -> dict[str, object]:
        checks = data["checks"]
        self.assertIsInstance(checks, list)
        for check in checks:
            self.assertIsInstance(check, dict)
            if check.get("id") == check_id:
                return check
        self.fail(f"Missing doctor check: {check_id}")

    def test_help_and_project_script_metadata_expose_command_surface(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli.app, ["--help"])
        self.assertEqual(0, result.exit_code, result.output)
        self.assertIsInstance(cli.app, click.Group)
        self.assertIsInstance(cli.build_parser(), click.Group)
        help_text = result.output
        for command in (
            "init",
            "doctor",
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

    def test_doctor_help_documents_read_only_common_topic_and_json_options(self) -> None:
        runner = CliRunner()
        result = runner.invoke(cli.app, ["doctor", "--help"])
        self.assertEqual(0, result.exit_code, result.output)
        self.assertIn("Run read-only dependency, Project, and topic diagnostics.", result.output)
        for option in ("--project", "--manifest", "--topic", "--json", "--format"):
            self.assertIn(option, result.output)
        self.assertNotIn("--fix", result.output)
        self.assertNotIn("--prepare", result.output)

    def test_doctor_dependency_only_reports_missing_and_found_pixi(self) -> None:
        root = self.make_root()
        with patch("isomer_labs.doctor.shutil.which", return_value=None):
            status, output = self.run_cli(["doctor", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("dependency-only", data["mode"])
        self.assertFalse(data["mutated"])
        self.assertEqual("fail", self.check(data, "host.pixi.executable")["status"])
        self.assertEqual("skip", self.check(data, "project.discovery")["status"])
        self.assertIn("ISO030", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertEqual("dependency-only", data["mode"])
        self.assertEqual("pass", self.check(data, "host.pixi.version")["status"])
        self.assertEqual("pixi 0.99.0", data["pixi"]["version"])

    def test_doctor_project_pixi_manifest_lockfile_and_requires_checks(self) -> None:
        root = self.make_root()
        self.init_project(root)
        self.add_project_pixi_manifest(root, requires_pixi=">=0.67", lockfile=True)
        self.append_manifest(
            root,
            """
            [[topic_pixi_environment_bindings]]
            research_topic_id = "default"
            pixi_environment = "default"
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("topic", data["mode"])
        self.assertEqual("pass", self.check(data, "project.pixi.manifest")["status"])
        self.assertEqual("pass", self.check(data, "project.pixi.lockfile")["status"])
        self.assertEqual("pass", self.check(data, "project.pixi.requires")["status"])
        self.assertEqual(["default"], data["project"]["pixi_manifest"]["environments"])

    def test_doctor_project_missing_manifest_and_lockfile_warning_are_stable(self) -> None:
        root = self.make_root()
        self.init_project(root)
        self.append_manifest(
            root,
            """
            [[topic_pixi_environment_bindings]]
            research_topic_id = "default"
            pixi_environment = "default"
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("fail", self.check(data, "project.pixi.manifest")["status"])

        self.add_project_pixi_manifest(root)
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("warn", self.check(data, "project.pixi.lockfile")["status"])
        self.assertFalse((root / "pixi.lock").exists())

    def test_doctor_topic_bindings_cover_multiple_missing_and_missing_named_envs(self) -> None:
        root = self.make_root()
        self.make_two_topic_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main", "alpha-analysis"), lockfile=True)
        self.append_manifest(
            root,
            """
            [[topic_pixi_environment_bindings]]
            research_topic_id = "alpha"
            pixi_environment = "alpha-main"
            purpose = "runtime"

            [[topic_pixi_environment_bindings]]
            research_topic_id = "alpha"
            pixi_environment = "alpha-analysis"
            purpose = "analysis"
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("pass", self.check(data, "topic.pixi.project-env.1")["status"])
        self.assertEqual("pass", self.check(data, "topic.pixi.project-env.2")["status"])

        missing_root = self.make_root()
        self.make_two_topic_project(missing_root)
        self.add_project_pixi_manifest(missing_root, environments=("alpha-main",), lockfile=True)
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--topic", "alpha", "--json"], cwd=missing_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("fail", self.check(data, "topic.pixi.binding.present")["status"])

        absent_env_root = self.make_root()
        self.make_two_topic_project(absent_env_root)
        self.add_project_pixi_manifest(absent_env_root, environments=("alpha-main",), lockfile=True)
        self.append_manifest(
            absent_env_root,
            """
            [[topic_pixi_environment_bindings]]
            research_topic_id = "alpha"
            pixi_environment = "missing-env"
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--topic", "alpha", "--json"], cwd=absent_env_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("fail", self.check(data, "topic.pixi.project-env.1")["status"])

    def test_doctor_standalone_bindings_and_invalid_binding_config(self) -> None:
        root = self.make_root()
        self.make_two_topic_project(root)
        self.add_project_pixi_manifest(root, lockfile=True)
        self.append_manifest(
            root,
            """
            [[topic_standalone_pixi_bindings]]
            research_topic_id = "alpha"
            manifest_path = "topic-workspaces/alpha/pixi.toml"
            pixi_environment = "default"
            """,
        )
        write(
            root / "topic-workspaces" / "alpha" / "pixi.toml",
            """
            [workspace]
            channels = ["conda-forge"]
            platforms = ["linux-64"]
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("pass", self.check(data, "topic.pixi.standalone.1")["status"])

        missing_root = self.make_root()
        self.make_two_topic_project(missing_root)
        self.add_project_pixi_manifest(missing_root, lockfile=True)
        self.append_manifest(
            missing_root,
            """
            [[topic_standalone_pixi_bindings]]
            research_topic_id = "alpha"
            manifest_path = "topic-workspaces/alpha/missing-pixi.toml"
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--topic", "alpha", "--json"], cwd=missing_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("fail", self.check(data, "topic.pixi.standalone.1")["status"])

        duplicate_root = self.make_root()
        self.make_two_topic_project(duplicate_root)
        self.add_project_pixi_manifest(duplicate_root, lockfile=True)
        self.append_manifest(
            duplicate_root,
            """
            [[topic_pixi_environment_bindings]]
            research_topic_id = "alpha"
            pixi_environment = "default"

            [[topic_pixi_environment_bindings]]
            research_topic_id = "alpha"
            pixi_environment = "default"
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--topic", "alpha", "--json"], cwd=duplicate_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO004", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        invalid_root = self.make_root()
        self.make_two_topic_project(invalid_root)
        self.add_project_pixi_manifest(invalid_root, lockfile=True)
        self.append_manifest(
            invalid_root,
            """
            [[topic_pixi_environment_bindings]]
            research_topic_id = "alpha"
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--topic", "alpha", "--json"], cwd=invalid_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO003", {diagnostic["code"] for diagnostic in data["diagnostics"]})

    def test_doctor_text_json_shape_secret_redaction_and_side_effects(self) -> None:
        root = self.make_root()
        self.init_project(root)
        self.add_project_pixi_manifest(root)
        self.append_manifest(
            root,
            """
            [[topic_pixi_environment_bindings]]
            research_topic_id = "default"
            pixi_environment = "default"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "default.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "default"
            api_key = "SHOULD_NOT_LEAK"
            environment_readiness_status = "ready"
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor"], cwd=root)
        self.assertEqual(1, status)
        self.assertIn("Doctor mode:", output)
        self.assertIn("Host", output)
        self.assertIn("Project", output)
        self.assertIn("Topic", output)
        self.assertNotIn("SHOULD_NOT_LEAK", output)

        write(
            root / ".isomer-labs" / "research-topics" / "default.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "default"
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["doctor", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertTrue(all({"id", "scope", "status", "concept", "summary"} <= set(check) for check in data["checks"]))
        self.assertEqual([], data["diagnostics"])
        self.assertFalse((root / "topic-workspaces" / "default" / "state.sqlite").exists())
        self.assertFalse((root / "topic-workspaces" / "default" / "artifacts").exists())
        self.assertFalse((root / "topic-workspaces" / "default" / ".pixi").exists())
        self.assertFalse((root / "pixi.lock").exists())

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
        launch_truth: bool = False,
        secret_like: bool = False,
        missing_fanout: bool = False,
        policy_topic_id: str | None = None,
        artifact_topic_id: str | None = None,
    ) -> str:
        workspace_topic = workspace_topic_id or topic_id
        policy_topic = policy_topic_id or topic_id
        artifact_topic = artifact_topic_id or topic_id
        execution_mode = "automatic" if automatic else "manual"
        automatic_policy = 'automatic_mode_policy_ref = "automatic-mode-policy:test"\n' if automatic else ""
        runtime_line = 'run_status = "done"\n' if runtime_truth else ""
        launch_line = 'launch_ref = "houmao-launch:test"\nhoumao_managed_agent_id = "managed-agent:test"\n' if launch_truth else ""
        secret_line = 'api_key = "SHOULD_NOT_LEAK"\n' if secret_like else ""
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
            coordination_policy_ref = "coordination-policy:{policy_topic}:test"
            gate_policy_ref = "gate-policy:{policy_topic}:test"
            baseline_waiver_policy_ref = "baseline-waiver-policy:{policy_topic}:test"
            default_execution_mode = "{execution_mode}"
            {automatic_policy}reviewer_read_access_policy = "promoted-artifacts-only"
            expected_artifacts = ["artifact:{artifact_topic}:{use_case}:research-plan", "artifact:{artifact_topic}:{use_case}:evidence-summary"]
            constraints = ["use_case:{use_case}"]
            {runtime_line}{launch_line}{secret_line}
            {"".join(role_blocks)}
            {fanout}
            """
        )

    def _without_role_binding(self, profile_text: str, role_id: str) -> str:
        start = profile_text.index(f'[[role_bindings]]\nrole_id = "{role_id}"')
        next_role = profile_text.find("\n[[role_bindings]]", start + 1)
        next_fanout = profile_text.find("\n[[fanout_policies]]", start + 1)
        stops = [index for index in (next_role, next_fanout) if index != -1]
        stop = min(stops) if stops else len(profile_text)
        return profile_text[:start] + profile_text[stop:]

    def _without_fanout_policy(self, profile_text: str, role_id: str) -> str:
        start = profile_text.index(f'[[fanout_policies]]\nrole_id = "{role_id}"')
        next_fanout = profile_text.find("\n[[fanout_policies]]", start + 1)
        stop = next_fanout if next_fanout != -1 else len(profile_text)
        return profile_text[:start] + profile_text[stop:]

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

        status, output = self.run_cli(["--project", str(FIXTURE_PROJECT), "team-templates", "list", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["deepsci-org", "fixture-method-team"], [template["id"] for template in data["templates"]])
        self.assertTrue(all(template["validation_status"] == "valid" for template in data["templates"]))

        status, output = self.run_cli(
            ["--project", str(FIXTURE_PROJECT), "team-templates", "validate", "fixture-method-team", "--json"]
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertEqual({"fixture-coordinator", "fixture-researcher"}, {role["id"] for role in data["template"]["roles"]})

        status, output = self.run_cli(["--project", str(FIXTURE_PROJECT), "team-templates", "validate", "deepsci-org", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])

        help_result = CliRunner().invoke(cli.app, ["team-templates", "validate", "--help"])
        self.assertEqual(0, help_result.exit_code, help_result.output)
        self.assertNotIn("--no-harness", help_result.output)

        status, output = self.run_cli(["team-templates", "validate", "missing-template", "--json"])
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("ISO016", data["diagnostics"][0]["code"])

    def test_profile_manifest_context_specialize_and_validate(self) -> None:
        status, output = self.run_cli(["--project", str(FIXTURE_PROJECT), "validate", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertEqual(4, len(data["manifest"]["topic_agent_team_profiles"]))

        status, output = self.run_cli(["--project", str(FIXTURE_PROJECT), "context", "show", "--topic", "novel-biomarker", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("deepsci-org", data["context"]["domain_agent_team_template_id"])
        self.assertEqual("uc-01-novel-biomarker", data["context"]["topic_agent_team_profile_id"])
        self.assertEqual(
            "coordination-policy:novel-biomarker-manual-review",
            data["context"]["profile_refs"]["coordination_policy_ref"],
        )

        status, output = self.run_cli(
            [
                "--project",
                str(FIXTURE_PROJECT),
                "team-profiles",
                "specialize",
                "--topic",
                "novel-biomarker",
                "--profile-id",
                "preview-novel-biomarker",
                "--use-case",
                "UC-01",
                "--json",
            ],
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("preview-novel-biomarker", data["profile"]["id"])
        self.assertEqual("research-inquiry-map", data["profile"]["expected_artifacts"][0])
        self.assertIsNone(data["written_path"])
        self.assertIsNone(data["registration_suggestion"])

        for profile_id in FIXTURE_PROFILE_IDS:
            status, output = self.run_cli(
                [
                    "--project",
                    str(FIXTURE_PROJECT),
                    "team-profiles",
                    "validate",
                    f".isomer-labs/team-profiles/{profile_id}.toml",
                    "--json",
                ]
            )
            data = json.loads(output)
            self.assertEqual(0, status, output)
            self.assertTrue(data["ok"])

    def test_profile_specialize_write_reports_registration_without_manifest_mutation(self) -> None:
        root = self.copy_fixture_project("write-profile")
        manifest_path = root / ".isomer-labs" / "manifest.toml"
        topic_config_path = root / ".isomer-labs" / "research-topics" / "novel-biomarker.toml"
        manifest_before = manifest_path.read_text(encoding="utf-8")
        topic_config_before = topic_config_path.read_text(encoding="utf-8")

        status, output = self.run_cli(
            [
                "--project",
                str(root),
                "team-profiles",
                "specialize",
                "--topic",
                "novel-biomarker",
                "--profile-id",
                "preview-novel-biomarker",
                "--use-case",
                "UC-01",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertIsNone(data["written_path"])
        self.assertIsNone(data["registration_suggestion"])
        self.assertFalse((root / ".isomer-labs" / "team-profiles" / "preview-novel-biomarker.toml").exists())
        self.assertEqual(manifest_before, manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(topic_config_before, topic_config_path.read_text(encoding="utf-8"))

        status, output = self.run_cli(
            [
                "--project",
                str(root),
                "team-profiles",
                "specialize",
                "--topic",
                "novel-biomarker",
                "--profile-id",
                "written-novel-biomarker",
                "--use-case",
                "UC-01",
                "--write",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        written_path = root / ".isomer-labs" / "team-profiles" / "written-novel-biomarker.toml"
        self.assertEqual(str(written_path), data["written_path"])
        self.assertTrue(written_path.is_file())
        self.assertEqual(
            {
                "target": "Project Manifest",
                "section": "topic_agent_team_profiles",
                "id": "written-novel-biomarker",
                "path": ".isomer-labs/team-profiles/written-novel-biomarker.toml",
                "domain_agent_team_template_id": "deepsci-org",
                "research_topic_id": "novel-biomarker",
                "status": "active",
            },
            data["registration_suggestion"],
        )
        self.assertEqual(manifest_before, manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(topic_config_before, topic_config_path.read_text(encoding="utf-8"))

        status, output = self.run_cli(
            [
                "--project",
                str(root),
                "team-profiles",
                "specialize",
                "--topic",
                "novel-biomarker",
                "--profile-id",
                "written-text-novel-biomarker",
                "--write",
            ],
            cwd=root,
        )
        self.assertEqual(0, status, output)
        self.assertIn("Registration suggestion: add [[topic_agent_team_profiles]]", output)

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
        write(
            root / ".isomer-labs" / "team-profiles" / "dup.toml",
            self.profile_fixture(
                "dup",
                "alpha",
                "UC-01",
                workspace_topic_id="beta",
                runtime_truth=True,
                launch_truth=True,
                secret_like=True,
                missing_fanout=True,
                policy_topic_id="beta",
                artifact_topic_id="beta",
            ),
        )
        write(root / ".isomer-labs" / "team-profiles" / "dup-beta.toml", self.profile_fixture("dup", "beta", "UC-02"))

        status, output = self.run_cli(["validate", "--json"], cwd=root)
        data = json.loads(output)
        codes = {diagnostic["code"] for diagnostic in data["diagnostics"]}
        self.assertEqual(1, status)
        self.assertTrue({"ISO004", "ISO009", "ISO010", "ISO019", "ISO020"} <= codes, data["diagnostics"])
        self.assertNotIn("SHOULD_NOT_LEAK", output)

    def test_archived_duplicate_profile_ids_are_rejected(self) -> None:
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

            [[topic_agent_team_profiles]]
            id = "dup"
            path = ".isomer-labs/team-profiles/dup.toml"
            domain_agent_team_template_id = "deepsci-org"
            research_topic_id = "alpha"
            status = "active"

            [[topic_agent_team_profiles]]
            id = "dup"
            path = ".isomer-labs/team-profiles/dup-archived.toml"
            domain_agent_team_template_id = "deepsci-org"
            research_topic_id = "alpha"
            status = "archived"
            """,
        )
        write(root / ".isomer-labs" / "research-topics" / "alpha.toml", 'research_topic_id = "alpha"\n')
        write(root / ".isomer-labs" / "team-profiles" / "dup.toml", self.profile_fixture("dup", "alpha", "UC-01"))

        status, output = self.run_cli(["validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO004", {diagnostic["code"] for diagnostic in data["diagnostics"]})

    def test_profile_validation_rejects_role_and_policy_omissions(self) -> None:
        root = self.copy_fixture_project("profile-negatives")
        profile_path = root / ".isomer-labs" / "team-profiles" / "uc-01-novel-biomarker.toml"
        valid_profile = profile_path.read_text(encoding="utf-8")

        cases = [
            ("missing-role", self._without_role_binding(valid_profile, "deepsci-org-reviewer"), "role_bindings.deepsci-org-reviewer"),
            (
                "inactive-required-role",
                valid_profile.replace('role_id = "deepsci-org-framer"\nactive = true', 'role_id = "deepsci-org-framer"\nactive = false'),
                "role_bindings.deepsci-org-framer.active",
            ),
            (
                "missing-required-skill",
                valid_profile.replace(
                    'required_skills = ["isomer-rsch-shared", "isomer-rsch-scout", "isomer-rsch-baseline"]',
                    'required_skills = ["isomer-rsch-shared", "isomer-rsch-baseline"]',
                    1,
                ),
                "role_bindings.deepsci-org-framer.required_skills",
            ),
            (
                "missing-fanout",
                self._without_fanout_policy(valid_profile, "deepsci-org-experimenter"),
                "fanout_policies.deepsci-org-experimenter",
            ),
            (
                "automatic-without-policy",
                valid_profile.replace('default_execution_mode = "manual"', 'default_execution_mode = "automatic"'),
                "automatic_mode_policy_ref",
            ),
            (
                "reviewer-without-access",
                valid_profile.replace('reviewer_read_access_policy = "promoted-artifacts-only"\n', ""),
                "reviewer_read_access_policy",
            ),
        ]
        for label, content, expected_field in cases:
            candidate = root / ".isomer-labs" / "team-profiles" / f"{label}.toml"
            write(candidate, content.replace('id = "uc-01-novel-biomarker"', f'id = "{label}"', 1))
            status, output = self.run_cli(
                ["--project", str(root), "team-profiles", "validate", str(candidate), "--json"],
                cwd=root,
            )
            data = json.loads(output)
            fields = {diagnostic.get("field") for diagnostic in data["diagnostics"]}
            self.assertEqual(1, status, output)
            self.assertIn(expected_field, fields, data["diagnostics"])

    def test_template_fixture_missing_artifact_and_boundary_leak_are_rejected(self) -> None:
        missing_root = self.copy_fixture_project("missing-template-artifact")
        missing_run_contract = (
            missing_root
            / ".isomer-labs"
            / "domain-agent-team-templates"
            / "fixture-method-team"
            / "execplan"
            / "specs"
            / "run"
            / "run-contract.md"
        )
        missing_run_contract.unlink()
        status, output = self.run_cli(
            ["--project", str(missing_root), "team-templates", "validate", "fixture-method-team", "--json"],
            cwd=missing_root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(
            any(
                diagnostic["code"] == "ISO017" and diagnostic["path"].endswith("specs/run/run-contract.md")
                for diagnostic in data["diagnostics"]
            ),
            data["diagnostics"],
        )

        boundary_root = self.copy_fixture_project("template-boundary-leak")
        workspace_contract = (
            boundary_root
            / ".isomer-labs"
            / "domain-agent-team-templates"
            / "fixture-method-team"
            / "execplan"
            / "specs"
            / "workspace"
            / "workspace.toml"
        )
        workspace_contract.write_text(
            workspace_contract.read_text(encoding="utf-8").replace(
                'topic_workspace_ref = "{topic_workspace_ref}"',
                'topic_workspace_ref = "topic-workspaces/novel-biomarker"',
            ),
            encoding="utf-8",
        )
        status, output = self.run_cli(
            ["--project", str(boundary_root), "team-templates", "validate", "fixture-method-team", "--json"],
            cwd=boundary_root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO018", {diagnostic["code"] for diagnostic in data["diagnostics"]})
