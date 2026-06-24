from __future__ import annotations

import contextlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import textwrap
import tomllib
import unittest
from pathlib import Path
from unittest.mock import patch

import click
from click.testing import CliRunner

from isomer_labs import cli
from isomer_labs.houmao.manifests import (
    ManifestKind,
    ManifestValidationError,
    MaterialFileRef,
    build_adapter_link_manifest,
    build_launch_material_manifest,
    canonical_json_digest,
    file_digest,
    load_json_manifest,
    reconcile_houmao_manifests,
    write_json_manifest,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURE_PROJECT = REPO_ROOT / "tests" / "fixtures" / "projects" / "deepsci-profile-use-cases"
UC01_FIXTURE_PROJECT = REPO_ROOT / "tests" / "fixtures" / "projects" / "uc01-headless-gb10"
UC01_RESEARCH_TOPIC_ID = "flash-attention-gb10-peak-performance-optimization"
UC01_SEED_INQUIRY_ID = "gb10-flash-attention-4-direction-selection"
UC01_RESEARCH_TASK_ID = "map-gb10-flash-attention-optimization-directions"
UC01_PROFILE_ID = "uc-01-gb10-deepsci-mini"
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
        normalized_args = self.normalize_cli_args(args)
        runner = CliRunner()
        with contextlib.chdir(root), patch.dict(os.environ, env or {}, clear=True):
            result = runner.invoke(cli.app, normalized_args, standalone_mode=False)
        if result.exception is not None:
            raise result.exception
        return int(result.return_value or 0), result.output

    def normalize_cli_args(self, args: list[str]) -> list[str]:
        normalized: list[str] = []
        print_json = False
        index = 0
        while index < len(args):
            value = args[index]
            if value == "--json":
                print_json = True
                index += 1
                continue
            if value == "--format=json":
                print_json = True
                index += 1
                continue
            if value == "--format" and index + 1 < len(args) and args[index + 1] == "json":
                print_json = True
                index += 2
                continue
            normalized.append(value)
            index += 1
        if print_json and "--print-json" not in normalized:
            normalized.insert(0, "--print-json")
        return normalized

    def init_project(self, root: Path, topic_id: str = "default") -> None:
        status, output = self.run_cli(["project", "--root", str(root), "init", topic_id], cwd=root, env=self.fake_houmao_env(root))
        self.assertEqual(0, status, output)

    def copy_fixture_project(self, name: str = "fixture-project") -> Path:
        root = self.make_root() / name
        shutil.copytree(FIXTURE_PROJECT, root)
        return root

    def copy_uc01_fixture_project(self, name: str = "uc01-fixture-project") -> Path:
        root = self.make_root() / name
        shutil.copytree(UC01_FIXTURE_PROJECT, root)
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

    def add_topic_pixi_binding(self, root: Path, topic_id: str, pixi_environment: str) -> None:
        self.append_manifest(
            root,
            f"""
            [[topic_pixi_environment_bindings]]
            research_topic_id = "{topic_id}"
            pixi_environment = "{pixi_environment}"
            purpose = "runtime"
            """,
        )

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

    def fake_houmao_command(self, root: Path) -> str:
        script = root / "fake-houmao-mgr.py"
        write(
            script,
            f"""
            #!{sys.executable}
            import json
            import os
            import sys

            args = sys.argv[1:]
            if "--version" in args:
                print("houmao-mgr 0.0.0")
                raise SystemExit(0)

            fail_on = os.environ.get("HOUMAO_FAKE_FAIL_ON")
            if fail_on and fail_on in " ".join(args):
                print(json.dumps({{"ok": False, "failed_on": fail_on, "args": args}}))
                raise SystemExit(2)

            def option(name, default=None):
                if name in args:
                    index = args.index(name)
                    if index + 1 < len(args):
                        return args[index + 1]
                return default

            payload = {{"ok": True, "args": args}}
            if "system-skills" in args and "list" in args:
                payload = {{"skills": []}}
            elif "global" in args and "list" in args:
                payload = {{"agents": []}}
            elif "project" in args and "init" in args:
                project_dir = option("--project-dir", os.getcwd())
                os.makedirs(os.path.join(project_dir, ".houmao"), exist_ok=True)
                with open(os.path.join(project_dir, ".houmao", "houmao-config.toml"), "w", encoding="utf-8") as handle:
                    handle.write("schema_version = 1\\n")
                payload = {{"project": {{"status": "initialized", "project_dir": project_dir}}}}
            elif "specialist" in args and "create" in args:
                payload = {{"specialist": {{"name": option("--name")}}}}
            elif "profile" in args and "create" in args:
                payload = {{"profile": {{"name": option("--name"), "agent_name": option("--agent-name")}}}}
            elif "agents" in args and "launch" in args:
                payload = {{"agent_id": "hm-" + str(option("--name")), "agent_name": option("--name"), "profile": option("--profile")}}
            elif "agents" in args and "list" in args:
                payload = {{"agents": []}}
            elif "agents" in args and "get" in args:
                payload = {{"agent_id": "hm-" + str(option("--name")), "agent_name": option("--name")}}
            elif "agents" in args and "stop" in args:
                payload = {{"stopped": True, "agent_name": option("--name")}}
            elif "mail" in args and "send" in args:
                payload = {{
                    "message_id": "msg-" + str(option("--handoff")),
                    "handoff": option("--handoff"),
                    "from": option("--from"),
                    "to": option("--to"),
                    "message_file": option("--message-file"),
                }}
            elif "mail" in args and "read" in args:
                payload = {{
                    "handoff": option("--handoff"),
                    "messages": [{{"message_id": "reply-" + str(option("--handoff")), "status": "candidate_completion"}}],
                }}
            elif "gateway" in args and "events" in args:
                payload = {{
                    "handoff": option("--handoff"),
                    "events": [{{"event_id": "event-" + str(option("--handoff")), "status": "candidate_completion"}}],
                }}
            else:
                print(json.dumps({{"ok": False, "args": args}}))
                raise SystemExit(2)
            print(json.dumps(payload))
            """,
        )
        return f"{sys.executable} {script}"

    def fake_houmao_env(self, root: Path, **extra: str) -> dict[str, str]:
        env = {
            "ISOMER_HOUMAO_COMMAND": self.fake_houmao_command(root),
            "HOME": str(root),
            "PATH": os.environ.get("PATH", ""),
        }
        env.update(extra)
        return env

    def create_alpha_runtime_team(self, root: Path, instance_id: str) -> None:
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main",), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
        for command in (
            ["project", "runtime", "init", "--topic", "alpha", "--json"],
            ["project", "runtime", "prepare", "--topic", "alpha", "--json"],
            [
                "project",
                "team-instances",
                "create",
                "--topic",
                "alpha",
                "--topic-agent-team-profile",
                "uc-01-alpha",
                "--id",
                instance_id,
                "--json",
            ],
        ):
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

    def launch_alpha_houmao_team(self, root: Path, instance_id: str, env: dict[str, str]) -> None:
        for command in (
            [
                "project",
                "team-instances",
                "launch-material",
                "prepare",
                instance_id,
                "--topic",
                "alpha",
                "--adapter",
                "houmao",
                "--json",
            ],
            [
                "project",
                "team-instances",
                "launch",
                instance_id,
                "--topic",
                "alpha",
                "--adapter",
                "houmao",
                "--json",
            ],
        ):
            status, output = self.run_cli(command, cwd=root, env=env)
            self.assertEqual(0, status, output)

    def alpha_agent_pair(self, root: Path, instance_id: str) -> tuple[str, str]:
        runtime_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(runtime_path) as db:
            db.row_factory = sqlite3.Row
            rows = db.execute(
                "SELECT id, agent_role_id FROM agent_instances WHERE agent_team_instance_id = ? ORDER BY agent_role_id",
                (instance_id,),
            ).fetchall()
        by_role = {row["agent_role_id"]: row["id"] for row in rows}
        return (
            by_role["deepsci-org-master"],
            by_role["deepsci-org-experimenter"],
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
            "project init",
            "project doctor",
            "project validate",
            "project topics list",
            "project workspaces list",
            "project context show",
            "project paths preview",
            "schemas list",
            "project team-templates",
            "project team-profiles",
            "project handoffs",
            "project handoffs dispatch",
            "project handoffs observe",
            "project handoffs normalize",
        ):
            self.assertIn(command, help_text)
        for command in ("uc01", "uc01 run", "uc01 inspect", "\n  init", "\n  validate", "\n  doctor"):
            self.assertNotIn(command, help_text)
        pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual("isomer_labs.cli:main", pyproject["project"]["scripts"]["isomer-cli"])

        for help_args in (
            ["project", "handoffs", "--help"],
            ["project", "handoffs", "dispatch", "--help"],
            ["project", "handoffs", "observe", "--help"],
            ["project", "handoffs", "normalize", "--help"],
        ):
            help_result = runner.invoke(cli.app, help_args)
            self.assertEqual(0, help_result.exit_code, help_result.output)
            self.assertNotIn("--json", help_result.output)
            self.assertNotIn("--format json", help_result.output)
            self.assertNotIn("--format=json", help_result.output)
        self.assertNotEqual(0, runner.invoke(cli.app, ["uc01", "--help"]).exit_code)
        for legacy_help_args in (
            ["init", "--help"],
            ["validate", "--help"],
            ["doctor", "--help"],
            ["topics", "--help"],
            ["runtime", "--help"],
            ["team-instances", "--help"],
            ["handoffs", "--help"],
        ):
            self.assertNotEqual(0, runner.invoke(cli.app, legacy_help_args).exit_code)

    def test_doctor_help_documents_read_only_common_topic_options(self) -> None:
        runner = CliRunner()
        project_result = runner.invoke(cli.app, ["project", "--help"])
        self.assertEqual(0, project_result.exit_code, project_result.output)
        self.assertIn("--root", project_result.output)
        self.assertIn("--manifest", project_result.output)
        self.assertNotIn("--project", project_result.output)

        result = runner.invoke(cli.app, ["project", "doctor", "--help"])
        self.assertEqual(0, result.exit_code, result.output)
        self.assertIn("Run read-only dependency, Project, and topic diagnostics.", result.output)
        self.assertIn("--topic", result.output)
        self.assertNotIn("--project", result.output)
        self.assertNotIn("--manifest", result.output)
        self.assertNotIn("--json", result.output)
        self.assertNotIn("--format", result.output)
        self.assertNotIn("--fix", result.output)
        self.assertNotIn("--prepare", result.output)

    def test_root_print_json_is_documented_and_applies_to_subcommands(self) -> None:
        root = self.make_root()
        runner = CliRunner()
        help_result = runner.invoke(cli.app, ["--help"])
        self.assertEqual(0, help_result.exit_code, help_result.output)
        self.assertIn("--print-json", help_result.output)
        self.assertNotIn("--json", help_result.output)
        self.assertNotIn("--format", help_result.output)

        for args in (
            ["--print-json", "project", "validate"],
            ["--print-json", "project", "doctor"],
            ["--print-json", "project", "runtime", "inspect"],
            ["--print-json", "project", "team-instances", "list"],
        ):
            status, output = self.run_cli(args, cwd=root)
            data = json.loads(output)
            self.assertIn(status, (0, 1))
            self.assertEqual("isomer-cli-output.v1", data["output_schema_version"])

    def test_default_output_is_structured_text_not_json(self) -> None:
        root = self.make_root()
        status, output = self.run_cli(["project", "validate"], cwd=root)
        self.assertEqual(1, status)
        self.assertNotIn("isomer-cli-output.v1", output)
        self.assertIn("ERROR | ISO001", output)

    def test_doctor_dependency_only_reports_missing_and_found_pixi(self) -> None:
        root = self.make_root()
        with patch("isomer_labs.doctor.shutil.which", return_value=None):
            status, output = self.run_cli(["project", "doctor", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("dependency-only", data["mode"])
        self.assertFalse(data["mutated"])
        self.assertEqual("fail", self.check(data, "host.pixi.executable")["status"])
        self.assertEqual("skip", self.check(data, "project.discovery")["status"])
        self.assertIn("ISO030", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["project", "doctor", "--json"], cwd=root)
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
            status, output = self.run_cli(["project", "doctor", "--json"], cwd=root)
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
            status, output = self.run_cli(["project", "doctor", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("fail", self.check(data, "project.pixi.manifest")["status"])

        self.add_project_pixi_manifest(root)
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["project", "doctor", "--json"], cwd=root)
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
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("pass", self.check(data, "topic.pixi.project-env.1")["status"])
        self.assertEqual("pass", self.check(data, "topic.pixi.project-env.2")["status"])

        missing_root = self.make_root()
        self.make_two_topic_project(missing_root)
        self.add_project_pixi_manifest(missing_root, environments=("alpha-main",), lockfile=True)
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=missing_root)
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
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=absent_env_root)
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
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=root)
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
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=missing_root)
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
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=duplicate_root)
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
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=invalid_root)
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
            status, output = self.run_cli(["project", "doctor"], cwd=root)
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
            status, output = self.run_cli(["project", "doctor", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertTrue(all({"id", "scope", "status", "concept", "summary"} <= set(check) for check in data["checks"]))
        self.assertEqual([], data["diagnostics"])
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "state.sqlite").exists())
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "artifacts").exists())
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / ".pixi").exists())
        self.assertFalse((root / "pixi.lock").exists())

    def test_init_creates_minimal_default_project_and_refuses_overwrite(self) -> None:
        root = self.make_root()
        status, output = self.run_cli(["project", "init"], cwd=root, env=self.fake_houmao_env(root))
        self.assertEqual(0, status, output)
        self.assertTrue((root / ".isomer-labs" / "manifest.toml").is_file())
        self.assertTrue((root / ".isomer-labs" / "research-topics" / "default.toml").is_file())
        self.assertTrue((root / "isomer-content" / "README.md").is_file())
        self.assertEqual(
            "*\n!.gitignore\n!/README.md\n",
            (root / "isomer-content" / ".gitignore").read_text(encoding="utf-8"),
        )
        self.assertTrue((root / "isomer-content" / "topic-ws" / "default").is_dir())
        self.assertTrue((root / ".houmao" / "houmao-config.toml").is_file())
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "state.sqlite").exists())
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "artifacts").exists())
        self.assertIn("Generated Content Root:", output)
        self.assertIn("Topic Workspace:", output)
        self.assertIn("Houmao Project:", output)
        help_result = CliRunner().invoke(cli.app, ["project", "init", "--help"])
        self.assertEqual(0, help_result.exit_code, help_result.output)
        self.assertNotIn("--force", help_result.output)

        status, output = self.run_cli(["project", "init"], cwd=root, env=self.fake_houmao_env(root))
        self.assertEqual(1, status)
        self.assertIn("refuses to overwrite", output)

    def test_init_uses_explicit_topic_id_consistently(self) -> None:
        root = self.make_root()
        status, output = self.run_cli(["project", "init", "paper", "--json"], cwd=root, env=self.fake_houmao_env(root))
        data = json.loads(output)
        self.assertEqual(0, status, output)
        manifest = (root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8")
        topic_config = (root / ".isomer-labs" / "research-topics" / "paper.toml").read_text(encoding="utf-8")
        self.assertIn('id = "paper"', manifest)
        self.assertIn('config_path = ".isomer-labs/research-topics/paper.toml"', manifest)
        self.assertIn('isomer_content_root = "isomer-content"', manifest)
        self.assertIn('topic_workspace_base_dir = "isomer-content/topic-ws"', manifest)
        self.assertIn('path = "isomer-content/topic-ws/paper"', manifest)
        self.assertIn('research_topic_id = "paper"', topic_config)
        self.assertTrue((root / "isomer-content" / "topic-ws" / "paper").is_dir())
        self.assertTrue(data["mutated"])
        self.assertEqual(str(root / "isomer-content"), data["content_root_path"])
        self.assertEqual(str(root / "isomer-content" / "topic-ws" / "paper"), data["topic_workspace_path"])
        self.assertEqual(str(root / ".houmao"), data["houmao_project_dir"])
        self.assertEqual("succeeded", data["houmao_bootstrap"]["status"])

    def test_init_accepts_custom_content_dir_for_default_topic(self) -> None:
        root = self.make_root()

        status, output = self.run_cli(
            ["project", "init", "--content-dir", "custom-content", "--json"],
            cwd=root,
            env=self.fake_houmao_env(root),
        )

        data = json.loads(output)
        manifest = (root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8")
        self.assertEqual(0, status, output)
        self.assertTrue((root / "custom-content" / "README.md").is_file())
        self.assertEqual(
            "*\n!.gitignore\n!/README.md\n",
            (root / "custom-content" / ".gitignore").read_text(encoding="utf-8"),
        )
        self.assertTrue((root / "custom-content" / "topic-ws" / "default").is_dir())
        self.assertIn('isomer_content_root = "custom-content"', manifest)
        self.assertIn('topic_workspace_base_dir = "custom-content/topic-ws"', manifest)
        self.assertIn('path = "custom-content/topic-ws/default"', manifest)
        self.assertEqual(str(root / "custom-content"), data["content_root_path"])
        self.assertEqual(str(root / "custom-content" / "topic-ws" / "default"), data["topic_workspace_path"])
        self.assertFalse((root / "isomer-content").exists())

    def test_init_accepts_custom_content_dir_for_explicit_topic(self) -> None:
        root = self.make_root()

        status, output = self.run_cli(
            ["project", "init", "paper", "--content-dir", "generated/isomer", "--json"],
            cwd=root,
            env=self.fake_houmao_env(root),
        )

        data = json.loads(output)
        manifest = (root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8")
        topic_config = (root / ".isomer-labs" / "research-topics" / "paper.toml").read_text(encoding="utf-8")
        self.assertEqual(0, status, output)
        self.assertIn('research_topic_id = "paper"', topic_config)
        self.assertIn('isomer_content_root = "generated/isomer"', manifest)
        self.assertIn('topic_workspace_base_dir = "generated/isomer/topic-ws"', manifest)
        self.assertIn('path = "generated/isomer/topic-ws/paper"', manifest)
        self.assertTrue((root / "generated" / "isomer" / "topic-ws" / "paper").is_dir())
        self.assertEqual(str(root / "generated" / "isomer"), data["content_root_path"])
        self.assertEqual(str(root / "generated" / "isomer" / "topic-ws" / "paper"), data["topic_workspace_path"])

    def test_init_rejects_invalid_custom_content_dirs_before_mutation(self) -> None:
        for content_dir, expected_message in (
            ("../outside", "outside the Project root"),
            (".isomer-labs/generated", "Project Config Directory"),
            (".houmao", "Houmao overlay"),
        ):
            with self.subTest(content_dir=content_dir):
                root = self.make_root()

                status, output = self.run_cli(
                    ["project", "init", "--content-dir", content_dir, "--json"],
                    cwd=root,
                    env=self.fake_houmao_env(root),
                )

                data = json.loads(output)
                self.assertEqual(1, status)
                diagnostics = data["diagnostics"]
                self.assertIn("ISO005", {diagnostic["code"] for diagnostic in diagnostics})
                self.assertTrue(any(expected_message in diagnostic["message"] for diagnostic in diagnostics), diagnostics)
                self.assertFalse((root / ".isomer-labs" / "manifest.toml").exists())
                self.assertFalse((root / "custom-content").exists())
                self.assertFalse((root / ".houmao").exists())

    def test_init_custom_content_dir_refuses_existing_project_without_creating_content(self) -> None:
        root = self.make_root()
        self.init_project(root)

        status, output = self.run_cli(
            ["project", "init", "--content-dir", "next-content", "--json"],
            cwd=root,
            env=self.fake_houmao_env(root),
        )

        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("refuses to overwrite", data["diagnostics"][0]["message"])
        self.assertFalse((root / "next-content").exists())

    def test_init_houmao_failure_does_not_write_project_manifest(self) -> None:
        root = self.make_root()
        env = self.fake_houmao_env(root, HOUMAO_FAKE_FAIL_ON="project")

        status, output = self.run_cli(["project", "init"], cwd=root, env=env)

        self.assertEqual(1, status)
        self.assertIn("ISO072", output)
        self.assertFalse((root / ".isomer-labs" / "manifest.toml").exists())
        self.assertFalse((root / "isomer-content").exists())

    def test_init_houmao_failure_does_not_write_custom_content_dir(self) -> None:
        root = self.make_root()
        env = self.fake_houmao_env(root, HOUMAO_FAKE_FAIL_ON="project")

        status, output = self.run_cli(["project", "init", "--content-dir", "custom-content"], cwd=root, env=env)

        self.assertEqual(1, status)
        self.assertIn("ISO072", output)
        self.assertFalse((root / ".isomer-labs" / "manifest.toml").exists())
        self.assertFalse((root / "custom-content").exists())

    def test_validate_reports_valid_project_as_versioned_json(self) -> None:
        root = self.make_root()
        self.init_project(root)
        status, output = self.run_cli(["project", "--root", str(root), "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertEqual("isomer-cli-output.v1", data["output_schema_version"])
        self.assertEqual([], data["diagnostics"])
        self.assertEqual("default", data["manifest"]["defaults"]["research_topic_id"])

    def test_project_selector_options_work_at_group_and_command_level(self) -> None:
        root = self.make_root()
        self.init_project(root)

        status, output = self.run_cli(["project", "--root", str(root), "validate", "--json"], cwd=root)
        group_level = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(group_level["ok"])

        status, output = self.run_cli(["project", "validate", "--project", str(root), "--json"], cwd=root)
        command_level = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(command_level["ok"])
        self.assertEqual(group_level["project"]["root"], command_level["project"]["root"])

    def test_project_subcommands_discover_parent_and_manifest_selector(self) -> None:
        root = self.make_root()
        self.init_project(root)
        nested = root / "nested" / "deeper"
        nested.mkdir(parents=True)

        status, output = self.run_cli(["project", "validate", "--json"], cwd=nested)
        discovered = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(str(root), discovered["project"]["root"])
        self.assertEqual("current directory", discovered["project"]["discovery_source"])

        other_root = self.make_root()
        self.init_project(other_root, topic_id="other")
        status, output = self.run_cli(
            ["project", "--manifest", str(root / ".isomer-labs" / "manifest.toml"), "validate", "--json"],
            cwd=other_root,
        )
        explicit = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(str(root), explicit["project"]["root"])
        self.assertEqual("explicit Project Manifest selector", explicit["project"]["discovery_source"])

    def test_project_init_refuses_nested_project_root(self) -> None:
        root = self.make_root()
        self.init_project(root)
        nested = root / "nested-project"
        nested.mkdir()

        status, output = self.run_cli(
            ["project", "--root", str(nested), "init", "nested", "--json"],
            cwd=root,
            env=self.fake_houmao_env(root),
        )

        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        self.assertEqual("ISO003", data["diagnostics"][0]["code"])
        self.assertEqual(str(root), data["ancestor_project_root"])
        self.assertFalse((nested / ".isomer-labs" / "manifest.toml").exists())

    def test_missing_and_malformed_projects_are_rejected(self) -> None:
        missing_root = self.make_root()
        status, output = self.run_cli(["project", "validate", "--json"], cwd=missing_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("ISO001", data["diagnostics"][0]["code"])

        malformed_root = self.make_root()
        write(malformed_root / ".isomer-labs" / "manifest.toml", "this is not = valid toml =\n")
        status, output = self.run_cli(["project", "validate", "--json"], cwd=malformed_root)
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
        status, output = self.run_cli(["project", "validate", "--json"], cwd=root)
        data = json.loads(output)
        codes = {diagnostic["code"] for diagnostic in data["diagnostics"]}
        self.assertEqual(1, status)
        self.assertTrue({"ISO004", "ISO005", "ISO007", "ISO009", "ISO010"} <= codes, data["diagnostics"])
        self.assertNotIn(secret_value, output)

    def test_validation_rejects_bad_generated_content_path_defaults(self) -> None:
        for content_root, expected_message in (
            ("../outside", "outside the Project root"),
            (".isomer-labs/generated", "Project Config Directory"),
        ):
            with self.subTest(content_root=content_root):
                root = self.make_root()
                write(
                    root / ".isomer-labs" / "manifest.toml",
                    f"""
                    schema_version = "isomer-project-manifest.v1"

                    [paths]
                    isomer_content_root = "{content_root}"
                    topic_workspace_base_dir = "isomer-content/topic-ws"

                    [[research_topics]]
                    id = "alpha"
                    config_path = ".isomer-labs/research-topics/alpha.toml"
                    topic_workspace_id = "alpha"

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

                status, output = self.run_cli(["project", "validate", "--json"], cwd=root)

                data = json.loads(output)
                self.assertEqual(1, status)
                diagnostics = data["diagnostics"]
                self.assertIn("ISO005", {diagnostic["code"] for diagnostic in diagnostics})
                self.assertTrue(any(expected_message in diagnostic["message"] for diagnostic in diagnostics), diagnostics)

    def test_validation_rejects_external_topic_workspace_base_default(self) -> None:
        root = self.make_root()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [paths]
            topic_workspace_base_dir = "../outside-topic-ws"

            [[research_topics]]
            id = "alpha"
            config_path = ".isomer-labs/research-topics/alpha.toml"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            """,
        )

        status, output = self.run_cli(["project", "validate", "--json"], cwd=root)

        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(
            any(diagnostic["field"] == "paths.topic_workspace_base_dir" for diagnostic in data["diagnostics"]),
            data["diagnostics"],
        )

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
            ["project", "context", "show", "--topic", "alpha", "--json"],
            cwd=root,
            env={"ISOMER_RESEARCH_TOPIC_ID": "beta"},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("alpha", data["context"]["research_topic_id"])
        self.assertEqual("explicit selector", data["context"]["sources"]["research_topic_id"])

        status, output = self.run_cli(
            ["project", "context", "show", "--json"],
            cwd=root / "topic-workspaces" / "beta",
            env={"ISOMER_RESEARCH_TOPIC_ID": "alpha"},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("beta", data["context"]["research_topic_id"])
        self.assertEqual("current directory", data["context"]["sources"]["research_topic_id"])

        status, output = self.run_cli(["project", "context", "show", "--json"], cwd=root, env={"ISOMER_RESEARCH_TOPIC_ID": "beta"})
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("beta", data["context"]["research_topic_id"])
        self.assertEqual("environment", data["context"]["sources"]["research_topic_id"])

        status, output = self.run_cli(["project", "context", "show", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("alpha", data["context"]["research_topic_id"])
        self.assertEqual(".isomer-labs/local.toml", data["context"]["sources"]["research_topic_id"])

        status, output = self.run_cli(["project", "context", "show", "--topic", "alpha", "--topic-workspace", "beta", "--json"], cwd=root)
        data = json.loads(output)
        codes = {diagnostic["code"] for diagnostic in data["diagnostics"]}
        self.assertEqual(1, status)
        self.assertIn("ISO012", codes)

    def test_lifecycle_refs_are_bounded_milestone_one_warnings(self) -> None:
        root = self.make_root()
        self.init_project(root)
        status, output = self.run_cli(["project", "context", "show", "--run", "run-1", "--json"], cwd=root)
        data = json.loads(output)
        diagnostics = data["diagnostics"]
        self.assertEqual(0, status, output)
        self.assertEqual("warning", diagnostics[0]["severity"])
        self.assertEqual("ISO015", diagnostics[0]["code"])

    def test_paths_preview_reports_sources_and_is_side_effect_free(self) -> None:
        root = self.make_root()
        self.init_project(root)
        status, output = self.run_cli(
            ["project", "paths", "preview", "--json"],
            cwd=root,
            env={"ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR": "isomer-content/topic-ws/default/custom-artifacts"},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        paths = {entry["surface"]: entry for entry in data["paths"]}
        self.assertEqual(str(root / "isomer-content"), paths["isomer_content_root"]["path"])
        self.assertEqual("env", paths["artifacts"]["source"])
        self.assertEqual("ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR", paths["artifacts"]["source_detail"])
        self.assertNotIn("plan", {entry["source"] for entry in data["paths"]})
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "state.sqlite").exists())
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "artifacts").exists())
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "custom-artifacts").exists())

        status, output = self.run_cli(
            ["project", "paths", "preview", "--json"],
            cwd=root,
            env={"ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR": "../outside"},
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO005", {diagnostic["code"] for diagnostic in data["diagnostics"]})

    def test_paths_preview_derives_topic_workspace_base_from_manifest_content_root(self) -> None:
        root = self.make_root()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [defaults]
            research_topic_id = "alpha"

            [paths]
            isomer_content_root = "generated/isomer"

            [[research_topics]]
            id = "alpha"
            config_path = ".isomer-labs/research-topics/alpha.toml"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            """,
        )

        status, output = self.run_cli(["project", "paths", "preview", "--json"], cwd=root)

        data = json.loads(output)
        self.assertEqual(0, status, output)
        paths = {entry["surface"]: entry for entry in data["paths"]}
        self.assertEqual(str(root / "generated" / "isomer"), paths["isomer_content_root"]["path"])
        self.assertEqual(str(root / "generated" / "isomer" / "topic-ws"), paths["topic_workspace_base"]["path"])
        self.assertEqual(str(root / "generated" / "isomer" / "topic-ws" / "alpha"), paths["topic_workspace"]["path"])
        self.assertFalse((root / "generated").exists())

    def test_runtime_init_prepare_inspect_validate_and_side_effect_boundaries(self) -> None:
        root = self.make_root()
        self.init_project(root)
        self.add_project_pixi_manifest(root, lockfile=True)
        self.add_topic_pixi_binding(root, "default", "default")

        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["project", "doctor", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "state.sqlite").exists())

        status, output = self.run_cli(["project", "runtime", "inspect", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["runtime"]["exists"])
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "state.sqlite").exists())

        status, output = self.run_cli(["project", "runtime", "init", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertTrue(data["runtime"]["created"])
        runtime_root = root / "isomer-content" / "topic-ws" / "default"
        self.assertTrue((runtime_root / "state.sqlite").is_file())
        for directory in ("artifacts", "agents", "tasks", "runs", "views", "logs"):
            self.assertTrue((runtime_root / directory).is_dir())
        surfaces = {record["surface"] for record in data["runtime"]["path_plans"]}
        self.assertTrue({"workspace_runtime_db", "artifacts", "agents", "tasks", "runs", "views", "logs"} <= surfaces)

        status, output = self.run_cli(["project", "runtime", "init", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertFalse(data["runtime"]["created"])

        status, output = self.run_cli(["project", "runtime", "prepare", "--actor", "operator-agent:test", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        readiness = data["preparation"]["readiness"]
        self.assertEqual("ready", readiness["status"])
        self.assertEqual(["default"], readiness["project_pixi_environment_refs"])
        self.assertEqual("operator-agent:test", readiness["actor_ref"])

        status, output = self.run_cli(["project", "runtime", "inspect", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertEqual("ready", data["runtime"]["latest_readiness"]["status"])
        self.assertEqual(1, data["runtime"]["counts"]["readiness_records"])

        status, output = self.run_cli(["project", "runtime", "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertFalse(data["mutated"])
        self.assertFalse((runtime_root / ".pixi").exists())
        self.assertFalse(any("houmao" in path.name for path in runtime_root.rglob("*")))

    def test_runtime_prepare_requires_initialized_runtime_and_records_repair_boundary(self) -> None:
        root = self.make_root()
        self.init_project(root)
        self.add_project_pixi_manifest(root, environments=("analysis",), lockfile=True)
        self.add_topic_pixi_binding(root, "default", "missing-env")

        status, output = self.run_cli(["project", "runtime", "prepare", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO040", {diagnostic["code"] for diagnostic in data["diagnostics"]})
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "state.sqlite").exists())

        status, output = self.run_cli(["project", "runtime", "init", "--json"], cwd=root)
        self.assertEqual(0, status, output)
        status, output = self.run_cli(["project", "runtime", "prepare", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        readiness = data["preparation"]["readiness"]
        self.assertEqual("failed", readiness["status"])
        self.assertIn("Service Request", readiness["repair_service_request_hint"])
        self.assertIn("ISO043", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        status, output = self.run_cli(["project", "runtime", "inspect", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("failed", data["runtime"]["latest_readiness"]["status"])

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

        status, output = self.run_cli(["project", "topics", "list", "--json"], cwd=root)
        topics = json.loads(output)["topics"]
        self.assertEqual(0, status, output)
        self.assertEqual(["alpha", "beta"], [topic["id"] for topic in topics])

        status, output = self.run_cli(["project", "workspaces", "list", "--json"], cwd=root)
        workspaces = json.loads(output)["workspaces"]
        self.assertEqual(0, status, output)
        self.assertEqual({"alpha", "beta"}, {workspace["id"] for workspace in workspaces})
        beta = next(workspace for workspace in workspaces if workspace["id"] == "beta")
        self.assertEqual("default", beta["source"])
        self.assertEqual("isomer-content/topic-ws/beta", beta["effective_path"])

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
        status, output = self.run_cli(["project", "team-templates", "list", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["deepsci-mini", "deepsci-org"], [template["id"] for template in data["templates"]])
        self.assertTrue(all(template["validation_status"] == "valid" for template in data["templates"]))

        status, output = self.run_cli(["project", "team-templates", "inspect", "deepsci-mini", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(3, len(data["template"]["roles"]))
        self.assertEqual(
            {"deepsci-mini-lead", "deepsci-mini-scout", "deepsci-mini-synth-reviewer"},
            {role["id"] for role in data["template"]["roles"]},
        )

        status, output = self.run_cli(["project", "team-templates", "inspect", "deepsci-org", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(7, len(data["template"]["roles"]))
        self.assertIn("deepsci-org-reviewer", {role["id"] for role in data["template"]["roles"]})

        status, output = self.run_cli(["project", "--root", str(FIXTURE_PROJECT), "team-templates", "list", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["deepsci-mini", "deepsci-org", "fixture-method-team"], [template["id"] for template in data["templates"]])
        self.assertTrue(all(template["validation_status"] == "valid" for template in data["templates"]))

        status, output = self.run_cli(
            ["project", "--root", str(FIXTURE_PROJECT), "team-templates", "validate", "fixture-method-team", "--json"]
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertEqual({"fixture-coordinator", "fixture-researcher"}, {role["id"] for role in data["template"]["roles"]})

        status, output = self.run_cli(["project", "--root", str(FIXTURE_PROJECT), "team-templates", "validate", "deepsci-org", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])

        help_result = CliRunner().invoke(cli.app, ["project", "team-templates", "validate", "--help"])
        self.assertEqual(0, help_result.exit_code, help_result.output)
        self.assertNotIn("--no-harness", help_result.output)

        status, output = self.run_cli(["project", "team-templates", "validate", "missing-template", "--json"])
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("ISO016", data["diagnostics"][0]["code"])

    def test_uc01_fixture_validates_and_rejects_runtime_truth_leakage(self) -> None:
        status, output = self.run_cli(["project", "--root", str(UC01_FIXTURE_PROJECT), "validate", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertEqual(UC01_RESEARCH_TOPIC_ID, data["manifest"]["defaults"]["research_topic_id"])
        self.assertEqual("deepsci-mini", data["manifest"]["defaults"]["domain_agent_team_template_id"])
        self.assertEqual(UC01_PROFILE_ID, data["manifest"]["defaults"]["topic_agent_team_profile_id"])
        self.assertEqual(
            UC01_RESEARCH_TASK_ID,
            data["topic_configs"][UC01_RESEARCH_TOPIC_ID]["defaults"]["research_task_id"],
        )
        self.assertEqual(
            "gate-policy:uc01-follow-up-inquiry",
            data["topic_configs"][UC01_RESEARCH_TOPIC_ID]["refs"]["follow_up_gate_policy_ref"],
        )
        self.assertFalse((UC01_FIXTURE_PROJECT / f"topic-workspaces/{UC01_RESEARCH_TOPIC_ID}/state.sqlite").exists())

        root = self.copy_uc01_fixture_project("uc01-runtime-truth")
        topic_config = root / ".isomer-labs" / "research-topics" / f"{UC01_RESEARCH_TOPIC_ID}.toml"
        topic_config.write_text(
            topic_config.read_text(encoding="utf-8") + '\n[leaked_runtime]\ngates = ["gate-should-not-live-here"]\n',
            encoding="utf-8",
        )
        status, output = self.run_cli(["project", "--root", str(root), "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["ok"])
        self.assertIn("ISO009", {diagnostic["code"] for diagnostic in data["diagnostics"]})

    def test_uc01_fixture_uses_generic_deepsci_mini_runtime_setup(self) -> None:
        root = self.copy_uc01_fixture_project("uc01-generic-runtime")
        for command in (
            ["project", "--root", str(root), "runtime", "init", "--json"],
            ["project", "--root", str(root), "runtime", "prepare", "--json"],
        ):
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

        status, output = self.run_cli(
            [
                "project",
                "--root",
                str(root),
                "team-instances",
                "create",
                "--topic-agent-team-profile",
                UC01_PROFILE_ID,
                "--id",
                "ati-uc01-generic",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        creation = data["creation"]
        self.assertEqual("ati-uc01-generic", creation["agent_team_instance"]["id"])
        self.assertEqual(
            ["deepsci-mini-lead", "deepsci-mini-scout", "deepsci-mini-synth-reviewer"],
            sorted(agent["agent_role_id"] for agent in creation["agent_instances"]),
        )

        status, output = self.run_cli(["project", "--root", str(root), "runtime", "validate", "--json"], cwd=root)
        validated = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(validated["ok"])
        self.assertEqual([], validated["diagnostics"])
        self.assertNotIn("uc01", validated["runtime"])

    def test_uc01_manual_harness_simulated_run_and_live_gate_skip_are_structured(self) -> None:
        env = dict(os.environ)
        env.pop("ISOMER_MANUAL_LIVE_HOUMAO", None)
        env["PYTHONPATH"] = (
            str(REPO_ROOT / "src")
            + os.pathsep
            + str(REPO_ROOT / "tests" / "manual")
            + os.pathsep
            + env.get("PYTHONPATH", "")
        )
        completed = subprocess.run(
            [sys.executable, str(REPO_ROOT / "tests" / "manual" / "uc01_headless_vertical_slice")],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr)
        data = json.loads(completed.stdout)
        self.assertTrue(data["ok"])
        self.assertEqual("uc07-measured-optimization", data["simulated"]["route_classification"])
        self.assertEqual("ati-uc01-gb10-deepsci-mini", data["simulated"]["agent_team_instance_ref"])
        self.assertEqual(9, data["simulated"]["artifact_count"])
        self.assertEqual(3, data["simulated"]["evidence_item_count"])
        self.assertEqual(3, data["simulated"]["view_manifest_count"])
        self.assertEqual("skipped", data["live"]["status"])
        self.assertEqual("ISO080", data["live"]["diagnostics"][0]["code"])
        self.assertTrue(data["uc01_summary"]["complete"])
        serialized = json.dumps(data, sort_keys=True)
        for forbidden in (
            "baseline_measurement",
            "candidate_optimization",
            "speedup",
            "utilization",
            "correctness_result",
            "automatic_replay",
            "compute_budget_gate",
        ):
            self.assertNotIn(forbidden, serialized)

    def test_uc01_packet_materializes_profile_bundle_and_runtime_provenance(self) -> None:
        root = self.copy_uc01_fixture_project("uc01-packet-materialize")
        packet_path = "fixtures/uc01/topic-team-instantiation-packet.toml"

        status, output = self.run_cli(
            [
                "project",
                "--root",
                str(root),
                "team-profiles",
                "materialize",
                "--topic",
                UC01_RESEARCH_TOPIC_ID,
                "--packet",
                packet_path,
                "--write",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        materialization = data["materialization"]
        profile = materialization["profile"]
        expected_profile_id = f"{UC01_RESEARCH_TOPIC_ID}-deepsci-mini"
        self.assertEqual(expected_profile_id, profile["id"])
        self.assertEqual("approval:uc01-deterministic-topic-team-profile", profile["approval_ref"])
        self.assertEqual(
            "topic-service-agent:uc01-deterministic-service-master",
            profile["topic_service_agent_refs"][0],
        )
        bundle_path = root / "topic-workspaces" / UC01_RESEARCH_TOPIC_ID / "team-profile"
        self.assertTrue((bundle_path / "profile.toml").is_file())
        self.assertTrue((bundle_path / "instantiation-packet.toml").is_file())
        self.assertTrue((bundle_path / "approval.toml").is_file())
        self.assertTrue((bundle_path / "execplan" / "manifest.toml").is_file())
        copied_specialization_guide = bundle_path / "execplan" / "team-specialization-guide.md"
        self.assertTrue(copied_specialization_guide.is_file())
        self.assertIn("deepsci-mini Team Specialization Guide", copied_specialization_guide.read_text(encoding="utf-8"))
        copied_operator_guide = (bundle_path / "execplan" / "docs" / "operator-guide.md").read_text(encoding="utf-8")
        self.assertIn("expected GB10 UC-01 source-map Artifacts", copied_operator_guide)
        source_operator_guide = (REPO_ROOT / "teams" / "deepsci-mini" / "execplan" / "docs" / "operator-guide.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("expected UC-01 Artifacts", source_operator_guide)

        manifest_path = root / ".isomer-labs" / "manifest.toml"
        manifest_path.write_text(
            manifest_path.read_text(encoding="utf-8")
            + f"""

[[topic_agent_team_profiles]]
id = "{expected_profile_id}"
path = "topic-workspaces/{UC01_RESEARCH_TOPIC_ID}/team-profile/profile.toml"
domain_agent_team_template_id = "deepsci-mini"
research_topic_id = "{UC01_RESEARCH_TOPIC_ID}"
status = "active"
""",
            encoding="utf-8",
        )
        for command in (
            ["project", "--root", str(root), "validate", "--json"],
            ["project", "--root", str(root), "runtime", "init", "--json"],
            ["project", "--root", str(root), "runtime", "prepare", "--json"],
        ):
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

        status, output = self.run_cli(
            [
                "project",
                "--root",
                str(root),
                "team-instances",
                "create",
                "--topic-agent-team-profile",
                expected_profile_id,
                "--id",
                "ati-uc01-bundle",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        team = data["creation"]["agent_team_instance"]
        self.assertEqual("ati-uc01-bundle", team["id"])
        self.assertEqual(f"topic-workspaces/{UC01_RESEARCH_TOPIC_ID}/team-profile", team["topic_agent_team_profile_bundle_ref"])
        self.assertEqual("approval:uc01-deterministic-topic-team-profile", team["approval_ref"])
        self.assertEqual(
            ["topic-service-agent:uc01-deterministic-service-master"],
            team["topic_service_agent_refs"],
        )

    def test_uc01_invalid_packet_is_rejected_before_materialization(self) -> None:
        root = self.copy_uc01_fixture_project("uc01-invalid-packet")
        status, output = self.run_cli(
            [
                "project",
                "--root",
                str(root),
                "team-profiles",
                "materialize",
                "--topic",
                UC01_RESEARCH_TOPIC_ID,
                "--packet",
                "fixtures/uc01/invalid-topic-team-instantiation-packet.toml",
                "--write",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        codes = {diagnostic["code"] for diagnostic in data["diagnostics"]}
        self.assertIn("ISO010", codes)
        self.assertIn("ISO009", codes)
        self.assertIn("ISO096", codes)
        self.assertIn("ISO019", codes)

    def test_profile_manifest_context_specialize_and_validate(self) -> None:
        status, output = self.run_cli(["project", "--root", str(FIXTURE_PROJECT), "validate", "--json"])
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertEqual(4, len(data["manifest"]["topic_agent_team_profiles"]))

        status, output = self.run_cli(["project", "--root", str(FIXTURE_PROJECT), "context", "show", "--topic", "novel-biomarker", "--json"])
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
                "project",
                "--root",
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
                    "project",
                    "--root",
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
                "project",
                "--root",
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
                "project",
                "--root",
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
                "project",
                "--root",
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

    def test_team_instances_create_list_show_and_duplicate_are_runtime_only(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main", "beta-main"), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
        self.add_topic_pixi_binding(root, "beta", "beta-main")

        for command in (
            ["project", "runtime", "init", "--topic", "alpha", "--json"],
            ["project", "runtime", "prepare", "--topic", "alpha", "--json"],
        ):
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "create",
                "--topic",
                "alpha",
                "--topic-agent-team-profile",
                "uc-01-alpha",
                "--id",
                "ati-alpha-manual",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        creation = data["creation"]
        team = creation["agent_team_instance"]
        self.assertEqual("ati-alpha-manual", team["id"])
        self.assertEqual("uc-01-alpha", team["topic_agent_team_profile_id"])
        self.assertEqual(7, len(creation["agent_instances"]))
        self.assertEqual(7, len(creation["agent_workspaces"]))
        self.assertEqual(0, len(team["run_ids"]))
        self.assertNotIn("houmao", output.lower())
        self.assertTrue((root / "topic-workspaces" / "alpha" / "agents").is_dir())
        self.assertFalse((root / "topic-workspaces" / "alpha" / "launch-dossiers").exists())

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "create",
                "--topic",
                "alpha",
                "--topic-agent-team-profile",
                "uc-01-alpha",
                "--id",
                "ati-alpha-manual",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO046", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        status, output = self.run_cli(["project", "team-instances", "list", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["ati-alpha-manual"], [item["id"] for item in data["agent_team_instances"]])

        status, output = self.run_cli(
            ["project", "team-instances", "show", "ati-alpha-manual", "--topic", "alpha", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        summary = data["summary"]
        self.assertEqual(7, len(summary["agent_instances"]))
        self.assertEqual(7, len(summary["agent_workspaces"]))
        self.assertGreaterEqual(len(summary["workflow_stage_cursors"]), 7)

        status, output = self.run_cli(["project", "runtime", "validate", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        first_workspace = root / summary["path_plans"][0]["path"]
        if not first_workspace.is_absolute():
            first_workspace = root / first_workspace
        shutil.rmtree(first_workspace)
        status, output = self.run_cli(["project", "runtime", "validate", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO044", {diagnostic["code"] for diagnostic in data["diagnostics"]})

    def test_agent_instance_ids_are_globally_unique_and_validated(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main", "beta-main"), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
        self.add_topic_pixi_binding(root, "beta", "beta-main")

        for topic in ("alpha", "beta"):
            for command in (
                ["project", "runtime", "init", "--topic", topic, "--json"],
                ["project", "runtime", "prepare", "--topic", topic, "--json"],
            ):
                status, output = self.run_cli(command, cwd=root)
                self.assertEqual(0, status, output)

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "create",
                "--topic",
                "alpha",
                "--topic-agent-team-profile",
                "uc-01-alpha",
                "--id",
                "ati-alpha-global",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        alpha_agents = data["creation"]["agent_instances"]
        self.assertEqual(7, len(alpha_agents))
        alpha_agent_ids = {agent["id"] for agent in alpha_agents}
        for agent_id in alpha_agent_ids:
            self.assertTrue(agent_id.startswith("agent-alpha-"))

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "create",
                "--topic",
                "alpha",
                "--topic-agent-team-profile",
                "uc-01-alpha",
                "--id",
                "ati-alpha-global-2",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        second_agent_ids = {agent["id"] for agent in data["creation"]["agent_instances"]}
        self.assertTrue(alpha_agent_ids.isdisjoint(second_agent_ids))

        status, output = self.run_cli(["project", "runtime", "validate", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)

        alpha_db = root / "topic-workspaces" / "alpha" / "state.sqlite"
        beta_db = root / "topic-workspaces" / "beta" / "state.sqlite"
        with sqlite3.connect(alpha_db) as db:
            db.row_factory = sqlite3.Row
            alpha_row = db.execute(
                "SELECT id, agent_role_id FROM agent_instances LIMIT 1"
            ).fetchone()
        duplicate_agent_id = alpha_row["id"]
        duplicate_role_id = alpha_row["agent_role_id"]

        with sqlite3.connect(beta_db) as db:
            db.execute(
                """
                INSERT INTO agent_instances (
                    id, agent_team_instance_id, agent_role_id, research_topic_id,
                    topic_workspace_id, agent_profile_ref, status, created_at,
                    updated_at, provenance_refs_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    duplicate_agent_id,
                    "ati-beta-duplicate",
                    duplicate_role_id,
                    "beta",
                    "beta",
                    None,
                    "planned",
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T00:00:00Z",
                    "[]",
                ),
            )

        status, output = self.run_cli(["project", "runtime", "validate", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        identity_diagnostics = [
            diagnostic
            for diagnostic in data["diagnostics"]
            if diagnostic["concept"] == "Agent Instance Identity"
        ]
        self.assertTrue(identity_diagnostics)
        messages = "\n".join(diagnostic["message"] for diagnostic in identity_diagnostics)
        self.assertIn(duplicate_agent_id, messages)
        self.assertIn("ati-alpha-global", messages)
        self.assertIn("ati-beta-duplicate", messages)

    def test_agent_instance_creation_rejects_project_wide_duplicate_ids(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main", "beta-main"), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
        self.add_topic_pixi_binding(root, "beta", "beta-main")

        for topic in ("alpha", "beta"):
            for command in (
                ["project", "runtime", "init", "--topic", topic, "--json"],
                ["project", "runtime", "prepare", "--topic", topic, "--json"],
            ):
                status, output = self.run_cli(command, cwd=root)
                self.assertEqual(0, status, output)

        def forced_id(topic_workspace_id: str, team_id: str, role_id: str) -> str:
            return f"agent-forced-{role_id}"

        with patch("isomer_labs.runtime.store._agent_instance_id", side_effect=forced_id):
            status, output = self.run_cli(
                [
                    "project",
                    "team-instances",
                    "create",
                    "--topic",
                    "alpha",
                    "--topic-agent-team-profile",
                    "uc-01-alpha",
                    "--id",
                    "ati-alpha-forced",
                    "--json",
                ],
                cwd=root,
            )
            self.assertEqual(0, status, output)

            beta_db = root / "topic-workspaces" / "beta" / "state.sqlite"
            before_counts = self.runtime_counts(beta_db)
            status, output = self.run_cli(
                [
                    "project",
                    "team-instances",
                    "create",
                    "--topic",
                    "beta",
                    "--topic-agent-team-profile",
                    "uc-02-beta",
                    "--id",
                    "ati-beta-forced",
                    "--json",
                ],
                cwd=root,
            )
            data = json.loads(output)
            self.assertEqual(1, status)
            self.assertFalse(data["mutated"])
            self.assertIn("Agent Instance Identity", {diagnostic["concept"] for diagnostic in data["diagnostics"]})
            self.assertEqual(before_counts, self.runtime_counts(beta_db))

    def test_agent_instance_creation_rejection_does_not_commit_partial_rows(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main",), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")

        for command in (
            ["project", "runtime", "init", "--topic", "alpha", "--json"],
            ["project", "runtime", "prepare", "--topic", "alpha", "--json"],
        ):
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

        alpha_db = root / "topic-workspaces" / "alpha" / "state.sqlite"
        existing_agent_id = "agent-alpha-existing-conflict"
        with sqlite3.connect(alpha_db) as db:
            db.execute(
                """
                INSERT INTO agent_instances (
                    id, agent_team_instance_id, agent_role_id, research_topic_id,
                    topic_workspace_id, agent_profile_ref, status, created_at,
                    updated_at, provenance_refs_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    existing_agent_id,
                    "ati-alpha-existing",
                    "deepsci-org-existing",
                    "alpha",
                    "alpha",
                    None,
                    "planned",
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T00:00:00Z",
                    "[]",
                ),
            )
        before_counts = self.runtime_counts(alpha_db)

        def generated_id(topic_workspace_id: str, team_id: str, role_id: str) -> str:
            if role_id == "deepsci-org-experimenter":
                return existing_agent_id
            return f"agent-alpha-{role_id}-candidate"

        with patch("isomer_labs.runtime.store._agent_instance_id", side_effect=generated_id):
            status, output = self.run_cli(
                [
                    "project",
                    "team-instances",
                    "create",
                    "--topic",
                    "alpha",
                    "--topic-agent-team-profile",
                    "uc-01-alpha",
                    "--id",
                    "ati-alpha-rollback",
                    "--json",
                ],
                cwd=root,
            )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        self.assertEqual(before_counts, self.runtime_counts(alpha_db))

    def runtime_counts(self, runtime_path: Path) -> dict[str, int]:
        tables = ("agent_team_instances", "agent_instances", "agent_workspaces", "path_plans")
        with sqlite3.connect(runtime_path) as db:
            return {
                table: int(db.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0])
                for table in tables
            }

    def test_houmao_json_manifest_helpers_round_trip_digest_drift_and_redaction(self) -> None:
        root = self.make_root()
        material_path = root / "launch" / "profile.json"
        write(material_path, '{"profile": "alpha"}\n')
        link_manifest = build_adapter_link_manifest(
            project_root=root,
            research_topic_id="alpha",
            topic_workspace_id="alpha",
            topic_workspace_path=root / "topic-workspaces" / "alpha",
            agent_team_instance_id="ati-alpha",
            topic_agent_team_profile_id="uc-01-alpha",
            domain_agent_team_template_id="deepsci-org",
            agent_bindings=[],
            houmao_project_dir=root / ".houmao",
            actor_ref="operator-agent:test",
            created_at="2026-06-22T00:00:00Z",
        )
        link_path = root / "adapter-link.json"
        digest = write_json_manifest(link_path, link_manifest, expected_kind=ManifestKind.ADAPTER_LINK.value)
        loaded = load_json_manifest(link_path, expected_kind=ManifestKind.ADAPTER_LINK.value)
        self.assertEqual(digest, canonical_json_digest(loaded))
        self.assertEqual(digest, canonical_json_digest(json.loads(link_path.read_text(encoding="utf-8"))))

        material_manifest = build_launch_material_manifest(
            link_manifest=loaded,
            material_files=[
                MaterialFileRef(
                    path=str(material_path),
                    digest=file_digest(material_path),
                    source="isomer_generated",
                    editable_policy="user_editable",
                )
            ],
            source="unit-test",
            created_at="2026-06-22T00:00:00Z",
        )
        result = reconcile_houmao_manifests(
            link_manifest=loaded,
            launch_material_manifest=material_manifest,
            material_base_dir=root,
        )
        self.assertEqual("linked", result.state)
        self.assertEqual([], result.material_drift)

        material_path.write_text('{"profile": "changed"}\n', encoding="utf-8")
        drifted = reconcile_houmao_manifests(
            link_manifest=loaded,
            launch_material_manifest=material_manifest,
            material_base_dir=root,
        )
        self.assertEqual("drifted", drifted.state)
        self.assertEqual("changed", drifted.material_drift[0]["status"])

        secret_manifest = dict(link_manifest)
        secret_manifest["api_key"] = "SHOULD_NOT_LEAK"
        with self.assertRaises(ManifestValidationError):
            write_json_manifest(root / "secret.json", secret_manifest, expected_kind=ManifestKind.ADAPTER_LINK.value)

    def test_houmao_manifest_cli_export_inspect_reconcile_and_adopt(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main",), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
        for command in (
            ["project", "runtime", "init", "--topic", "alpha", "--json"],
            ["project", "runtime", "prepare", "--topic", "alpha", "--json"],
            [
                "project",
                "team-instances",
                "create",
                "--topic",
                "alpha",
                "--topic-agent-team-profile",
                "uc-01-alpha",
                "--id",
                "ati-alpha-manual",
                "--json",
            ],
        ):
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "adapter-link",
                "export",
                "ati-alpha-manual",
                "--topic",
                "alpha",
                "--houmao-project-dir",
                ".houmao",
                "--actor",
                "operator-agent:test",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertEqual("adapter_link", data["manifest"]["manifest_kind"])
        link_path = Path(data["manifest_path"])
        self.assertTrue(link_path.is_file())
        self.assertEqual("adapter-link.json", link_path.name)

        status, output = self.run_cli(
            ["project", "team-instances", "inspect-live", "ati-alpha-manual", "--topic", "alpha", "--integrity", "--json"],
            cwd=root,
            env={},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertEqual("linked", data["reconciliation"]["state"])

        status, output = self.run_cli(
            ["project", "team-instances", "reconcile", "ati-alpha-manual", "--topic", "alpha", "--actor", "operator-agent:test", "--json"],
            cwd=root,
            env={},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertEqual("linked", data["reconciliation"]["state"])
        runtime_manifest_path = Path(data["runtime_manifest_path"])
        self.assertTrue(runtime_manifest_path.is_file())
        self.assertEqual("adapter-runtime-manifest.json", runtime_manifest_path.name)

        live_state = root / "live-state.json"
        live_state.write_text(
            json.dumps({"available": True, "agents": [{"agent_id": "hm-alpha", "agent_name": "deepsci-org-master"}]}),
            encoding="utf-8",
        )
        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "adopt",
                "ati-alpha-manual",
                "--topic",
                "alpha",
                "--live-state-json",
                str(live_state),
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO064", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "adopt",
                "ati-alpha-manual",
                "--topic",
                "alpha",
                "--live-state-json",
                str(live_state),
                "--yes",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("adopted", data["reconciliation"]["state"])

        status, output = self.run_cli(["project", "team-instances", "show", "ati-alpha-manual", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        summary = data["summary"]
        self.assertGreaterEqual(len(summary["adapter_manifest_refs"]), 2)
        self.assertGreaterEqual(len(summary["reconciliation_records"]), 2)
        self.assertEqual([], summary["handoffs"])
        self.assertEqual(0, len(summary["agent_team_instance"]["run_ids"]))

        status, output = self.run_cli(["project", "runtime", "validate", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(2, data["runtime"]["counts"]["adapter_reconciliation_records"])

    def test_houmao_prepare_launch_inspect_and_stop_use_cli_adapter_records(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main",), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
        for command in (
            ["project", "runtime", "init", "--topic", "alpha", "--json"],
            ["project", "runtime", "prepare", "--topic", "alpha", "--json"],
            [
                "project",
                "team-instances",
                "create",
                "--topic",
                "alpha",
                "--topic-agent-team-profile",
                "uc-01-alpha",
                "--id",
                "ati-alpha-cli",
                "--json",
            ],
        ):
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

        env = {
            "ISOMER_HOUMAO_COMMAND": self.fake_houmao_command(root),
            "HOME": str(root),
            "PATH": os.environ.get("PATH", ""),
        }
        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "launch-material",
                "prepare",
                "ati-alpha-cli",
                "--topic",
                "alpha",
                "--adapter",
                "houmao",
                "--json",
            ],
            cwd=root,
            env=env,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertEqual("prepared", data["materialization"]["status"])
        self.assertGreater(len(data["manual_guidance"]), 0)
        self.assertTrue(Path(data["materialization"]["link_manifest_path"]).is_file())
        self.assertTrue(Path(data["materialization"]["launch_material_manifest_path"]).is_file())
        self.assertFalse((Path(data["materialization"]["paths"]["adapter_root"]) / "adapter-runtime-manifest.json").exists())
        path_plan_ids = data["materialization"]["path_plan_ids"]
        self.assertTrue(any("adapter_manifest-houmao-ati-alpha-cli-adapter_link" in item for item in path_plan_ids))
        self.assertTrue(any("adapter_manifest-houmao-ati-alpha-cli-launch_material" in item for item in path_plan_ids))
        self.assertTrue(any("adapter_manifest-houmao-ati-alpha-cli-adapter_runtime" in item for item in path_plan_ids))

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "launch",
                "ati-alpha-cli",
                "--topic",
                "alpha",
                "--adapter",
                "houmao",
                "--json",
            ],
            cwd=root,
            env=env,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertEqual("launched", data["launch"]["status"])
        self.assertGreaterEqual(len(data["launch"]["command_run_ids"]), 22)
        self.assertTrue(Path(data["launch"]["runtime_manifest_path"]).is_file())
        self.assertEqual("launched_by_isomer", data["launch"]["reconciliation"]["state"])

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "inspect-live",
                "ati-alpha-cli",
                "--topic",
                "alpha",
                "--adapter",
                "houmao",
                "--json",
            ],
            cwd=root,
            env=env,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertEqual("observed", data["inspection"]["status"])
        self.assertGreaterEqual(len(data["inspection"]["command_run_ids"]), 8)

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "stop",
                "ati-alpha-cli",
                "--topic",
                "alpha",
                "--adapter",
                "houmao",
                "--json",
            ],
            cwd=root,
            env=env,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertEqual("stopped", data["stop"]["status"])

        status, output = self.run_cli(["project", "team-instances", "show", "ati-alpha-cli", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        summary = data["summary"]
        self.assertGreaterEqual(len(summary["adapter_materializations"]), 2)
        self.assertGreaterEqual(len(summary["adapter_launch_attempts"]), 1)
        self.assertGreaterEqual(len(summary["adapter_inspection_snapshots"]), 1)
        self.assertGreaterEqual(len(summary["adapter_stop_outcomes"]), 1)
        self.assertGreaterEqual(len(summary["adapter_command_runs"]), 30)
        self.assertGreaterEqual(len(summary["adapter_payload_refs"]), 30)
        manifest_refs = {record["manifest_kind"]: record for record in summary["adapter_manifest_refs"]}
        self.assertEqual({"adapter_link", "launch_material", "adapter_runtime"}, set(manifest_refs))
        self.assertTrue(all(record["path_plan_id"] for record in manifest_refs.values()))
        launch_manifest_refs = set(summary["adapter_launch_attempts"][0]["manifest_ref_ids"])
        self.assertTrue(set(manifest_refs) <= {record_id.rsplit("-", 1)[-1] for record_id in launch_manifest_refs})

        status, output = self.run_cli(["project", "runtime", "validate", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertGreaterEqual(data["runtime"]["counts"]["adapter_command_runs"], 30)
        self.assertGreaterEqual(data["runtime"]["counts"]["adapter_payload_refs"], 30)

    def test_houmao_handoffs_preflight_failure_writes_no_runtime_records(self) -> None:
        root = self.make_root()
        instance_id = "ati-alpha-no-mail"
        self.create_alpha_runtime_team(root, instance_id)
        source_agent, target_agent = self.alpha_agent_pair(root, instance_id)

        status, output = self.run_cli(
            [
                "--print-json",
                "project",
                "handoffs",
                "dispatch",
                "--topic",
                "alpha",
                "--agent-team-instance",
                instance_id,
                "--source-agent-instance",
                source_agent,
                "--target-agent-instance",
                target_agent,
                "--run",
                "run-alpha-no-mail",
                "--message",
                "Try a handoff without a launched adapter.",
            ],
            cwd=root,
            env={"HOME": str(root), "PATH": ""},
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        codes = {diagnostic["code"] for diagnostic in data["diagnostics"]}
        self.assertIn("ISO070", codes)
        self.assertIn("ISO077", codes)

        status, output = self.run_cli(["project", "team-instances", "show", instance_id, "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        summary = data["summary"]
        self.assertEqual([], summary["handoffs"])
        self.assertEqual([], summary["adapter_handoff_dispatches"])
        self.assertEqual([], summary["agent_team_instance"]["run_ids"])

    def test_houmao_handoffs_dispatch_observe_accept_and_text_output(self) -> None:
        root = self.make_root()
        instance_id = "ati-alpha-handoff"
        self.create_alpha_runtime_team(root, instance_id)
        env = self.fake_houmao_env(root)
        self.launch_alpha_houmao_team(root, instance_id, env)
        source_agent, target_agent = self.alpha_agent_pair(root, instance_id)
        runtime_path = root / "topic-workspaces" / "alpha" / "state.sqlite"

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "inspect-live",
                instance_id,
                "--topic",
                "alpha",
                "--adapter",
                "houmao",
                "--json",
            ],
            cwd=root,
            env=env,
        )
        self.assertEqual(0, status, output)

        status, output = self.run_cli(
            [
                "--print-json",
                "project",
                "handoffs",
                "dispatch",
                "--topic",
                "alpha",
                "--agent-team-instance",
                instance_id,
                "--source-agent-instance",
                source_agent,
                "--target-agent-instance",
                target_agent,
                "--run",
                "run-alpha-handoff",
                "--message",
                "Draft the experiment execution handoff.",
                "--expected-output",
                "artifact:alpha:handoff-result",
                "--completion-watcher-contract",
                "completion-watcher:alpha:handoff",
                "--actor",
                "operator-agent:test",
            ],
            cwd=root,
            env=env,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("isomer-cli-output.v1", data["output_schema_version"])
        self.assertTrue(data["mutated"])
        dispatch = data["dispatch"]
        handoff_id = dispatch["handoff_id"]
        self.assertEqual("sent", dispatch["status"])
        self.assertEqual("run-alpha-handoff", dispatch["run_id"])
        self.assertGreaterEqual(len(dispatch["command_run_ids"]), 1)
        self.assertGreaterEqual(len(dispatch["payload_ref_ids"]), 2)
        self.assertNotIn("message_id", output)

        observation_ids = []
        for source_name, extra_args in (
            ("mail", []),
            ("gateway", []),
            ("file", ["--payload-json", "handoff-observation.json"]),
            ("inspection", []),
        ):
            if source_name == "file":
                write(
                    root / "handoff-observation.json",
                    json.dumps({"candidate_completion": True, "summary": "file observation"}, sort_keys=True),
                )
            status, output = self.run_cli(
                [
                    "--print-json",
                    "project",
                    "handoffs",
                    "observe",
                    str(handoff_id),
                    "--topic",
                    "alpha",
                    "--source",
                    source_name,
                    "--summary",
                    f"{source_name} candidate completion",
                    "--actor",
                    "operator-agent:test",
                    *extra_args,
                ],
                cwd=root,
                env=env,
            )
            data = json.loads(output)
            self.assertEqual(0, status, output)
            observation = data["observation"]
            self.assertEqual("candidate_completion", observation["status"])
            self.assertFalse(observation["completion_authority"])
            observation_ids.append(observation["signal_observation_id"])
            self.assertNotIn("message_id", output)
            self.assertNotIn("event_id", output)

        with sqlite3.connect(runtime_path) as db:
            run_status = db.execute("SELECT status FROM lifecycle_records WHERE id = ?", ("run-alpha-handoff",)).fetchone()[0]
            evidence_count = db.execute(
                "SELECT COUNT(*) FROM lifecycle_records WHERE record_kind = 'evidence_item'"
            ).fetchone()[0]
        self.assertEqual("running", run_status)
        self.assertEqual(0, evidence_count)

        status, output = self.run_cli(
            [
                "--print-json",
                "project",
                "handoffs",
                "normalize",
                str(handoff_id),
                "--topic",
                "alpha",
                "--status",
                "accepted",
                "--signal-observation",
                str(observation_ids[0]),
                "--output-artifact",
                "artifact:alpha:handoff-result",
                "--rationale",
                "Operator accepted the candidate output.",
                "--actor",
                "operator-agent:test",
            ],
            cwd=root,
            env=env,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        normalization = data["normalization"]
        self.assertEqual("accepted", normalization["status"])
        self.assertEqual("run-alpha-handoff", normalization["run_id"])
        self.assertEqual(["artifact:alpha:handoff-result"], normalization["output_artifact_refs"])
        with sqlite3.connect(runtime_path) as db:
            run_status = db.execute("SELECT status FROM lifecycle_records WHERE id = ?", ("run-alpha-handoff",)).fetchone()[0]
        self.assertEqual("complete", run_status)

        status, output = self.run_cli(
            [
                "project",
                "handoffs",
                "dispatch",
                "--topic",
                "alpha",
                "--agent-team-instance",
                instance_id,
                "--source-agent-instance",
                source_agent,
                "--target-agent-instance",
                target_agent,
                "--run",
                "run-alpha-text",
                "--message",
                "Text dispatch path.",
            ],
            cwd=root,
            env=env,
        )
        self.assertEqual(0, status, output)
        self.assertIn("Handoff dispatch status: sent", output)
        self.assertNotIn("isomer-cli-output.v1", output)
        text_handoff_id = next(line.split(":", 1)[1].strip() for line in output.splitlines() if line.startswith("Handoff: "))

        status, output = self.run_cli(
            [
                "project",
                "handoffs",
                "observe",
                text_handoff_id,
                "--topic",
                "alpha",
                "--source",
                "mail",
                "--summary",
                "text observation",
            ],
            cwd=root,
            env=env,
        )
        self.assertEqual(0, status, output)
        self.assertIn("Handoff observation status: candidate_completion", output)
        self.assertIn("Completion authority: no", output)
        text_observation_id = next(
            line.split(":", 1)[1].strip() for line in output.splitlines() if line.startswith("Signal Observation: ")
        )

        status, output = self.run_cli(
            [
                "project",
                "handoffs",
                "normalize",
                text_handoff_id,
                "--topic",
                "alpha",
                "--status",
                "accepted",
                "--signal-observation",
                text_observation_id,
                "--output-artifact",
                "artifact:alpha:text-handoff",
            ],
            cwd=root,
            env=env,
        )
        self.assertEqual(0, status, output)
        self.assertIn("Handoff normalization status: accepted", output)
        self.assertNotIn("isomer-cli-output.v1", output)

        status, output = self.run_cli(["project", "team-instances", "show", instance_id, "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        summary = data["summary"]
        handoff_records = {record["id"]: record for record in summary["handoffs"]}
        self.assertEqual("accepted", handoff_records[handoff_id]["status"])
        self.assertEqual("candidate_completion", summary["signal_observations"][0]["status"])
        self.assertEqual({"file", "gateway", "inspection", "mail"}, {record["observation_kind"] for record in summary["signal_observations"]})
        serialized_summary = json.dumps(summary, sort_keys=True)
        for forbidden_field in ("message_id", "event_id", "mailbox_id", "managed_agent_id", "gateway_url"):
            self.assertNotIn(forbidden_field, serialized_summary)

        status, output = self.run_cli(["project", "runtime", "validate", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertGreaterEqual(data["runtime"]["counts"]["adapter_handoff_dispatch_records"], 2)
        self.assertGreaterEqual(data["runtime"]["counts"]["signal_observation_records"], 5)
        self.assertGreaterEqual(data["runtime"]["counts"]["handoff_normalization_records"], 2)

    def test_houmao_handoffs_rejected_repair_and_stale_validation_recover_from_disk(self) -> None:
        root = self.make_root()
        instance_id = "ati-alpha-repair"
        self.create_alpha_runtime_team(root, instance_id)
        env = self.fake_houmao_env(root)
        self.launch_alpha_houmao_team(root, instance_id, env)
        source_agent, target_agent = self.alpha_agent_pair(root, instance_id)
        runtime_path = root / "topic-workspaces" / "alpha" / "state.sqlite"

        def dispatch_for_run(run_id: str) -> str:
            status, output = self.run_cli(
                [
                    "--print-json",
                    "project",
                    "handoffs",
                    "dispatch",
                    "--topic",
                    "alpha",
                    "--agent-team-instance",
                    instance_id,
                    "--source-agent-instance",
                    source_agent,
                    "--target-agent-instance",
                    target_agent,
                    "--run",
                    run_id,
                    "--message",
                    f"Dispatch for {run_id}.",
                ],
                cwd=root,
                env=env,
            )
            data = json.loads(output)
            self.assertEqual(0, status, output)
            return str(data["dispatch"]["handoff_id"])

        def observe_mail(handoff_id: str) -> str:
            status, output = self.run_cli(
                [
                    "--print-json",
                    "project",
                    "handoffs",
                    "observe",
                    handoff_id,
                    "--topic",
                    "alpha",
                    "--source",
                    "mail",
                    "--summary",
                    "mail candidate",
                ],
                cwd=root,
                env=env,
            )
            data = json.loads(output)
            self.assertEqual(0, status, output)
            return str(data["observation"]["signal_observation_id"])

        rejected_handoff_id = dispatch_for_run("run-alpha-rejected")
        rejected_signal_id = observe_mail(rejected_handoff_id)
        status, output = self.run_cli(
            [
                "--print-json",
                "project",
                "handoffs",
                "normalize",
                rejected_handoff_id,
                "--topic",
                "alpha",
                "--status",
                "rejected",
                "--signal-observation",
                rejected_signal_id,
                "--corrective-ref",
                "service-request:alpha:reject-repair",
                "--rationale",
                "The returned payload did not satisfy the handoff.",
            ],
            cwd=root,
            env=env,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("rejected", data["normalization"]["status"])

        repair_handoff_id = dispatch_for_run("run-alpha-repair")
        repair_signal_id = observe_mail(repair_handoff_id)
        status, output = self.run_cli(
            [
                "--print-json",
                "project",
                "handoffs",
                "normalize",
                repair_handoff_id,
                "--topic",
                "alpha",
                "--status",
                "repair_routed",
                "--signal-observation",
                repair_signal_id,
                "--corrective-ref",
                "service-request:alpha:repair-route",
                "--rationale",
                "Route a repair handoff.",
            ],
            cwd=root,
            env=env,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("repair_routed", data["normalization"]["status"])

        stale_handoff_id = dispatch_for_run("run-alpha-stale")
        with sqlite3.connect(runtime_path) as db:
            db.execute(
                "UPDATE handoff_records SET stale_after = ? WHERE id = ?",
                ("2000-01-01T00:00:00Z", stale_handoff_id),
            )

        status, output = self.run_cli(["project", "team-instances", "show", instance_id, "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        handoff_records = {record["id"]: record for record in data["summary"]["handoffs"]}
        self.assertEqual("rejected", handoff_records[rejected_handoff_id]["status"])
        self.assertEqual("repair", handoff_records[repair_handoff_id]["status"])
        normalizations = {record["handoff_id"]: record for record in data["summary"]["handoff_normalizations"]}
        self.assertEqual(["service-request:alpha:reject-repair"], normalizations[rejected_handoff_id]["corrective_refs"])
        self.assertEqual(["service-request:alpha:repair-route"], normalizations[repair_handoff_id]["corrective_refs"])

        status, output = self.run_cli(["project", "runtime", "validate", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertIn("ISO045", {diagnostic["code"] for diagnostic in data["diagnostics"]})

    def test_houmao_launch_failed_preflight_writes_no_material(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main",), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
        for command in (
            ["project", "runtime", "init", "--topic", "alpha", "--json"],
            ["project", "runtime", "prepare", "--topic", "alpha", "--json"],
            [
                "project",
                "team-instances",
                "create",
                "--topic",
                "alpha",
                "--topic-agent-team-profile",
                "uc-01-alpha",
                "--id",
                "ati-alpha-no-houmao",
                "--json",
            ],
        ):
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "launch",
                "ati-alpha-no-houmao",
                "--topic",
                "alpha",
                "--adapter",
                "houmao",
                "--json",
            ],
            cwd=root,
            env={"PATH": "", "HOME": str(root)},
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO070", {diagnostic["code"] for diagnostic in data["diagnostics"]})
        adapter_root = root / "topic-workspaces" / "alpha" / "runtime" / "adapters" / "houmao" / "ati-alpha-no-houmao"
        self.assertFalse(adapter_root.exists())

    def test_houmao_partial_launch_preserves_recovery_records(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main",), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
        for command in (
            ["project", "runtime", "init", "--topic", "alpha", "--json"],
            ["project", "runtime", "prepare", "--topic", "alpha", "--json"],
            [
                "project",
                "team-instances",
                "create",
                "--topic",
                "alpha",
                "--topic-agent-team-profile",
                "uc-01-alpha",
                "--id",
                "ati-alpha-partial",
                "--json",
            ],
        ):
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

        env = {
            "ISOMER_HOUMAO_COMMAND": self.fake_houmao_command(root),
            "HOUMAO_FAKE_FAIL_ON": "deepsci-org-framer",
            "HOME": str(root),
            "PATH": os.environ.get("PATH", ""),
        }
        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "launch",
                "ati-alpha-partial",
                "--topic",
                "alpha",
                "--adapter",
                "houmao",
                "--json",
            ],
            cwd=root,
            env=env,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("partial", data["launch"]["status"])
        self.assertTrue(Path(data["launch"]["runtime_manifest_path"]).is_file())

        status, output = self.run_cli(["project", "team-instances", "show", "ati-alpha-partial", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        attempts = data["summary"]["adapter_launch_attempts"]
        self.assertEqual(1, len(attempts))
        self.assertEqual("partial", attempts[0]["status"])
        self.assertGreater(len(attempts[0]["adapter_refs"]), 0)
        self.assertLess(len(attempts[0]["adapter_refs"]), 7)
        self.assertGreater(len(attempts[0]["command_run_ids"]), 0)

        stop_env = {
            "ISOMER_HOUMAO_COMMAND": self.fake_houmao_command(root),
            "HOUMAO_FAKE_FAIL_ON": "deepsci-org-framer",
            "HOME": str(root),
            "PATH": os.environ.get("PATH", ""),
        }
        status, output = self.run_cli(
            [
                "project",
                "team-instances",
                "stop",
                "ati-alpha-partial",
                "--topic",
                "alpha",
                "--adapter",
                "houmao",
                "--json",
            ],
            cwd=root,
            env=stop_env,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("partial", data["stop"]["status"])

    def test_workspace_runtime_schema_diagnostics_transaction_rollback_and_isolation(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main", "beta-main"), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
        self.add_topic_pixi_binding(root, "beta", "beta-main")

        for topic, profile, instance in (
            ("alpha", "uc-01-alpha", "ati-alpha"),
            ("beta", "uc-02-beta", "ati-beta"),
        ):
            for command in (
                ["project", "runtime", "init", "--topic", topic, "--json"],
                ["project", "runtime", "prepare", "--topic", topic, "--json"],
                [
                    "project",
                    "team-instances",
                    "create",
                    "--topic",
                    topic,
                    "--topic-agent-team-profile",
                    profile,
                    "--id",
                    instance,
                    "--json",
                ],
            ):
                status, output = self.run_cli(command, cwd=root)
                self.assertEqual(0, status, output)

        status, output = self.run_cli(["project", "team-instances", "list", "--topic", "alpha", "--json"], cwd=root)
        alpha = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["ati-alpha"], [item["id"] for item in alpha["agent_team_instances"]])

        status, output = self.run_cli(["project", "team-instances", "list", "--topic", "beta", "--json"], cwd=root)
        beta = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["ati-beta"], [item["id"] for item in beta["agent_team_instances"]])

        alpha_db = root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(alpha_db) as connection:
            before = connection.execute("SELECT COUNT(*) FROM lifecycle_records").fetchone()[0]
            with self.assertRaises(sqlite3.IntegrityError):
                with connection:
                    connection.execute(
                        """
                        INSERT INTO lifecycle_records
                            (
                                id, record_kind, research_topic_id, topic_workspace_id,
                                status, created_at, updated_at, lifecycle_refs_json,
                                transition_metadata_json, provenance_refs_json
                            )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            "rollback-sentinel",
                            "run",
                            "alpha",
                            "alpha",
                            "planned",
                            "2026-01-01T00:00:00Z",
                            "2026-01-01T00:00:00Z",
                            "{}",
                            "{}",
                            "[]",
                        ),
                    )
                    connection.execute(
                        "INSERT INTO lifecycle_records (id) VALUES (?)",
                        ("broken-row",),
                    )
            after = connection.execute("SELECT COUNT(*) FROM lifecycle_records").fetchone()[0]
            self.assertEqual(before, after)
            connection.execute(
                "UPDATE runtime_metadata SET value = ? WHERE key = 'schema_version'",
                ("isomer-workspace-runtime.v2",),
            )

        status, output = self.run_cli(["project", "runtime", "inspect", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("newer", data["diagnostics"][0]["message"])

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

        status, output = self.run_cli(["project", "validate", "--json"], cwd=root)
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

        status, output = self.run_cli(["project", "validate", "--json"], cwd=root)
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
                ["project", "--root", str(root), "team-profiles", "validate", str(candidate), "--json"],
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
            ["project", "--root", str(missing_root), "team-templates", "validate", "fixture-method-team", "--json"],
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
            ["project", "--root", str(boundary_root), "team-templates", "validate", "fixture-method-team", "--json"],
            cwd=boundary_root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO018", {diagnostic["code"] for diagnostic in data["diagnostics"]})
