from __future__ import annotations

import contextlib
import io
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

    def run_main(
        self,
        args: list[str],
        *,
        cwd: Path | None = None,
        env: dict[str, str] | None = None,
    ) -> tuple[int, str, str]:
        root = cwd or self.make_root()
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            contextlib.chdir(root),
            patch.dict(os.environ, env or {}, clear=True),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            status = cli.main(args)
        return status, stdout.getvalue(), stderr.getvalue()

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

    def init_project(self, root: Path, topic_id: str = "default", *, create_topic: bool = True) -> None:
        status, output = self.run_cli(["project", "--root", str(root), "init"], cwd=root, env=self.fake_houmao_env(root))
        self.assertEqual(0, status, output)
        if create_topic:
            status, output = self.run_cli(
                [
                    "project",
                    "--root",
                    str(root),
                    "topics",
                    "create",
                    topic_id,
                    "--statement",
                    f"Investigate concrete research questions for {topic_id}.",
                    "--set-default",
                ],
                cwd=root,
            )
            self.assertEqual(0, status, output)

    def copy_fixture_project(self, name: str = "fixture-project") -> Path:
        root = self.make_root() / name
        shutil.copytree(FIXTURE_PROJECT, root)
        self._append_local_team_repository_registration(root)
        return root

    def copy_uc01_fixture_project(self, name: str = "uc01-fixture-project") -> Path:
        root = self.make_root() / name
        shutil.copytree(UC01_FIXTURE_PROJECT, root)
        self._append_local_team_repository_registration(root)
        return root

    def _append_local_team_repository_registration(self, root: Path) -> None:
        manifest_path = root / ".isomer-labs" / "manifest.toml"
        manifest_text = manifest_path.read_text(encoding="utf-8")
        manifest_text = manifest_text.replace('path = "../../../.."', f'path = "{REPO_ROOT.as_posix()}"')
        manifest_path.write_text(manifest_text, encoding="utf-8")

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

            [[team_repositories]]
            id = "isomer-local-teams"
            path = "{repo_root}"
            status = "active"
            """.format(repo_root=REPO_ROOT.as_posix()),
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

    def default_topic_workspace(self, root: Path, topic_id: str = "default") -> Path:
        return root / "isomer-content" / "topic-ws" / topic_id

    def prepare_topic_main_repo(self, root: Path, topic_id: str = "default") -> Path:
        topic_main = self.default_topic_workspace(root, topic_id) / "repos" / "topic-main"
        topic_main.mkdir(parents=True, exist_ok=True)
        subprocess.run(["git", "init"], cwd=topic_main, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=topic_main, check=True)
        subprocess.run(["git", "config", "user.name", "Isomer Test"], cwd=topic_main, check=True)
        write(topic_main / "README.md", "# Topic Main\n")
        subprocess.run(["git", "add", "README.md"], cwd=topic_main, check=True)
        subprocess.run(["git", "commit", "-m", "init topic main"], cwd=topic_main, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return topic_main

    def patch_pixi(
        self,
        *,
        path: str | None = "/usr/bin/pixi",
        version_returncode: int = 0,
        requires_returncode: int = 0,
        info_returncode: int = 0,
        info_stdout: str | None = None,
        info_stderr: str = "",
    ):
        def fake_run(args: list[str], **_: object) -> subprocess.CompletedProcess[str]:
            if args[1:] == ["--version"]:
                return subprocess.CompletedProcess(args, version_returncode, stdout="pixi 0.99.0\n", stderr="")
            if args[1:4] == ["workspace", "requires-pixi", "verify"]:
                return subprocess.CompletedProcess(args, requires_returncode, stdout="", stderr="")
            if args[1:4] == ["info", "--json", "--manifest-path"]:
                stdout = info_stdout
                if stdout is None:
                    stdout = self.fake_pixi_info_stdout(Path(args[4]))
                return subprocess.CompletedProcess(args, info_returncode, stdout=stdout, stderr=info_stderr)
            return subprocess.CompletedProcess(args, 2, stdout="", stderr="unexpected command")

        return (
            patch("shutil.which", return_value=path),
            patch("subprocess.run", side_effect=fake_run),
        )

    def fake_pixi_info_stdout(self, target: Path) -> str:
        manifest_path = self.fake_pixi_manifest_for_target(target)
        if manifest_path is None:
            return json.dumps(
                {
                    "project_info": None,
                    "environments_info": [],
                }
            )
        environment_names = self.fake_pixi_environment_names(manifest_path)
        return json.dumps(
            {
                "project_info": {
                    "name": manifest_path.parent.name,
                    "manifest_path": str(manifest_path),
                },
                "environments_info": [
                    {
                        "name": environment_name,
                        "prefix": str(manifest_path.parent / ".pixi" / "envs" / environment_name),
                    }
                    for environment_name in environment_names
                ],
            }
        )

    def fake_pixi_manifest_for_target(self, target: Path) -> Path | None:
        if target.is_file():
            return target
        if not target.is_dir():
            return None
        pixi_toml = target / "pixi.toml"
        if pixi_toml.is_file():
            return pixi_toml
        pyproject = target / "pyproject.toml"
        if pyproject.is_file():
            return pyproject
        return None

    def fake_pixi_environment_names(self, manifest_path: Path) -> list[str]:
        environment_names = {"default"}
        try:
            raw = tomllib.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, tomllib.TOMLDecodeError):
            return sorted(environment_names)
        pixi_config = raw
        if manifest_path.name == "pyproject.toml":
            tool = raw.get("tool")
            pixi_config = tool.get("pixi") if isinstance(tool, dict) and isinstance(tool.get("pixi"), dict) else {}
        environments = pixi_config.get("environments") if isinstance(pixi_config, dict) else None
        if isinstance(environments, dict):
            environment_names.update(str(name) for name in environments)
        return sorted(environment_names)

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
            "project cleanup",
            "project doctor",
            "project validate",
            "project topics list",
            "project workspaces list",
            "project skill-callbacks register",
            "project skill-callbacks install",
            "project skill-callbacks resolve",
            "project skill-callbacks insertion-points",
            "project skill-callbacks list",
            "project skill-callbacks show",
            "project skill-callbacks disable",
            "project skill-callbacks validate",
            "project system-extensions list",
            "project system-extensions remember",
            "project system-extensions forget",
            "project context show",
            "project self show",
            "project self identity",
            "project self pixi",
            "project self env",
            "project self paths",
            "project self queries",
            "project topic-main-guidance render",
            "project topic-main-guidance inspect",
            "project topic-main-guidance ensure",
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
            ["project", "skill-callbacks", "--help"],
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

    def test_main_normalizes_text_invocation_errors(self) -> None:
        cases = (
            (["project", "paths", "get"], "Missing argument 'SEMANTIC_LABEL'.", "project paths get"),
            (["project", "paths", "gte"], "No such command 'gte'", "project paths"),
            (
                ["project", "paths", "get", "topic.records.artifacts", "--bogus"],
                "No such option '--bogus'.",
                "project paths get",
            ),
        )
        for args, message, example_fragment in cases:
            with self.subTest(args=args):
                status, stdout, stderr = self.run_main(args)
                self.assertNotEqual(0, status)
                self.assertEqual("", stderr)
                self.assertIn("ERROR | ISOCLI001 | CLI invocation", stdout)
                self.assertIn(message, stdout)
                self.assertIn("Usage:", stdout)
                self.assertIn("Examples:", stdout)
                self.assertIn(example_fragment, stdout)
                self.assertNotIn("Traceback (most recent call last)", stdout)

    def test_main_invocation_errors_include_bounded_examples(self) -> None:
        status, output, _ = self.run_main(["--print-json", "project", "paths", "get"])
        data = json.loads(output)
        self.assertEqual(2, status)
        diagnostic = data["diagnostics"][0]
        self.assertEqual("project paths get", data["command"])
        self.assertEqual("ISOCLI001", diagnostic["code"])
        self.assertEqual("isomer-cli project paths get [OPTIONS] SEMANTIC_LABEL", diagnostic["usage"])
        self.assertIn("hint", diagnostic)
        self.assertGreaterEqual(len(diagnostic["examples"]), 1)
        self.assertLessEqual(len(diagnostic["examples"]), 3)
        self.assertTrue(all("project paths get" in example for example in diagnostic["examples"]))

    def test_main_malformed_invocations_honor_print_json(self) -> None:
        for args in (
            ["--print-json", "project", "paths", "get"],
            ["--print-json", "project", "unknown-command"],
        ):
            with self.subTest(args=args):
                status, output, stderr = self.run_main(args)
                data = json.loads(output)
                self.assertEqual(2, status)
                self.assertEqual("", stderr)
                self.assertEqual("isomer-cli-output.v1", data["output_schema_version"])
                self.assertFalse(data["ok"])
                self.assertFalse(data["mutated"])
                self.assertEqual("ISOCLI001", data["diagnostics"][0]["code"])

    def test_main_unexpected_exception_suppresses_traceback_by_default(self) -> None:
        from isomer_labs.cli.commands import project as project_commands

        with patch.object(project_commands, "_cmd_schemas_list", side_effect=RuntimeError("boom")):
            status, stdout, stderr = self.run_main(["schemas", "list"])
        self.assertEqual(1, status)
        self.assertEqual("", stderr)
        self.assertIn("ERROR | ISOCLI500 | CLI internal error", stdout)
        self.assertIn("Mutation state: unknown", stdout)
        self.assertNotIn("Traceback (most recent call last)", stdout)
        self.assertNotIn("RuntimeError: boom", stdout)

    def test_main_debug_mode_exposes_traceback(self) -> None:
        from isomer_labs.cli.commands import project as project_commands

        with patch.object(project_commands, "_cmd_schemas_list", side_effect=RuntimeError("boom")):
            status, stdout, _ = self.run_main(["--debug", "schemas", "list"])
        self.assertEqual(1, status)
        self.assertIn("ERROR | ISOCLI500 | CLI internal error", stdout)
        self.assertIn("Debug traceback:", stdout)
        self.assertIn("Traceback (most recent call last)", stdout)
        self.assertIn("RuntimeError: boom", stdout)

    def test_main_debug_json_isolates_traceback_details(self) -> None:
        from isomer_labs.cli.commands import project as project_commands

        with patch.object(project_commands, "_cmd_schemas_list", side_effect=RuntimeError("boom")):
            status, output, _ = self.run_main(
                ["--print-json", "schemas", "list"],
                env={"ISOMER_CLI_DEBUG": "1"},
            )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("isomer-cli-output.v1", data["output_schema_version"])
        self.assertEqual("unknown", data["mutation_state"])
        self.assertEqual("RuntimeError", data["debug"]["exception_type"])
        self.assertTrue(any("RuntimeError: boom" in line for line in data["debug"]["traceback"]))
        self.assertNotIn("RuntimeError: boom", data["diagnostics"][0]["message"])

    def test_main_keyboard_interrupt_is_normalized(self) -> None:
        from isomer_labs.cli.commands import project as project_commands

        with patch.object(project_commands, "_cmd_schemas_list", side_effect=KeyboardInterrupt):
            status, stdout, stderr = self.run_main(["schemas", "list"])
        self.assertEqual(130, status)
        self.assertEqual("", stderr.strip())
        self.assertIn("ERROR | ISOCLI130 | CLI invocation", stdout)
        self.assertNotIn("Traceback (most recent call last)", stdout)

    def test_domain_diagnostics_without_remediation_fields_remain_compatible(self) -> None:
        status, output, _ = self.run_main(["--print-json", "project", "validate"])
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("isomer-cli-output.v1", data["output_schema_version"])
        diagnostic = data["diagnostics"][0]
        self.assertNotIn("hint", diagnostic)
        self.assertNotIn("usage", diagnostic)
        self.assertNotIn("examples", diagnostic)

        status, output, _ = self.run_main(["project", "validate"])
        self.assertEqual(1, status)
        self.assertNotIn("Hint:", output)
        self.assertNotIn("Usage:", output)
        self.assertNotIn("Examples:", output)

    def test_default_output_is_structured_text_not_json(self) -> None:
        root = self.make_root()
        status, output = self.run_cli(["project", "validate"], cwd=root)
        self.assertEqual(1, status)
        self.assertNotIn("isomer-cli-output.v1", output)
        self.assertIn("ERROR | ISO001", output)

    def test_doctor_dependency_only_reports_missing_and_found_pixi(self) -> None:
        root = self.make_root()
        with patch("isomer_labs.project.doctor.shutil.which", return_value=None):
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
            manifest_path_or_dir = "topic-workspaces/alpha/pixi.toml"
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
            manifest_path_or_dir = "topic-workspaces/alpha/missing-pixi.toml"
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

    def test_doctor_standalone_directory_and_implicit_default_resolution(self) -> None:
        root = self.make_root()
        self.make_two_topic_project(root)
        self.add_project_pixi_manifest(root, lockfile=True)
        self.append_manifest(
            root,
            """
            [[topic_standalone_pixi_bindings]]
            research_topic_id = "alpha"
            manifest_path_or_dir = "topic-workspaces/alpha"
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
        check = self.check(data, "topic.pixi.standalone.1")
        self.assertEqual("pass", check["status"])
        self.assertEqual("directory", check["details"]["target_kind"])
        self.assertEqual("topic-workspaces/alpha/pixi.toml", check["details"]["resolved_manifest_path"])
        self.assertEqual("explicit", check["details"]["source"])

        implicit_root = self.make_root()
        self.make_two_topic_project(implicit_root)
        self.add_project_pixi_manifest(implicit_root, lockfile=True)
        write(
            implicit_root / "topic-workspaces" / "alpha" / "pixi.toml",
            """
            [workspace]
            channels = ["conda-forge"]
            platforms = ["linux-64"]
            """,
        )

        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=implicit_root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        check = self.check(data, "topic.pixi.standalone.default")
        self.assertEqual("pass", check["status"])
        self.assertEqual("implicit-default", check["details"]["source"])
        self.assertEqual("default", check["details"]["pixi_environment"])
        self.assertEqual("topic-workspaces/alpha", check["details"]["target_path"])

    def test_doctor_standalone_pixi_tooling_and_confinement_failures(self) -> None:
        root = self.make_root()
        self.make_two_topic_project(root)
        self.add_project_pixi_manifest(root, lockfile=True)
        write(
            root / "topic-workspaces" / "alpha" / "pixi.toml",
            """
            [workspace]
            channels = ["conda-forge"]
            platforms = ["linux-64"]
            """,
        )

        which_patch, run_patch = self.patch_pixi(info_stdout="{not-json")
        with which_patch, run_patch:
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        check = self.check(data, "topic.pixi.standalone.default")
        self.assertEqual("fail", check["status"])
        self.assertEqual("Pixi tooling", check["concept"])
        self.assertIn("install_guidance", check["details"])
        self.assertIn("ISO031", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        confined_root = self.make_root()
        self.make_two_topic_project(confined_root)
        self.add_project_pixi_manifest(confined_root, lockfile=True)
        write(
            confined_root / "topic-workspaces" / "alpha" / "pixi.toml",
            """
            [workspace]
            channels = ["conda-forge"]
            platforms = ["linux-64"]
            """,
        )
        escaping_payload = json.dumps(
            {
                "project_info": {
                    "name": "project-root",
                    "manifest_path": str(confined_root / "pyproject.toml"),
                },
                "environments_info": [
                    {
                        "name": "default",
                        "prefix": str(confined_root / ".pixi" / "envs" / "default"),
                    }
                ],
            }
        )
        which_patch, run_patch = self.patch_pixi(info_stdout=escaping_payload)
        with which_patch, run_patch:
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=confined_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        check = self.check(data, "topic.pixi.standalone.default")
        self.assertEqual("fail", check["status"])
        self.assertEqual("Topic Workspace Pixi confinement", check["concept"])
        self.assertIn("ISO005", {diagnostic["code"] for diagnostic in data["diagnostics"]})

    def test_manifest_rejects_superseded_standalone_pixi_target_fields(self) -> None:
        root = self.make_root()
        self.make_two_topic_project(root)
        self.add_project_pixi_manifest(root, lockfile=True)
        self.append_manifest(
            root,
            """
            [[topic_standalone_pixi_bindings]]
            research_topic_id = "alpha"
            manifest_path = "topic-workspaces/alpha/pixi.toml"
            """,
        )

        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["project", "doctor", "--topic", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO003", {diagnostic["code"] for diagnostic in data["diagnostics"]})
        self.assertTrue(
            any("manifest_path_or_dir" in diagnostic["message"] for diagnostic in data["diagnostics"]),
            data["diagnostics"],
        )

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
        self.assertFalse((root / ".isomer-labs" / "research-topics" / "default.toml").exists())
        self.assertTrue((root / "isomer-content" / "README.md").is_file())
        self.assertEqual(
            "*\n!.gitignore\n!/README.md\n",
            (root / "isomer-content" / ".gitignore").read_text(encoding="utf-8"),
        )
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default").exists())
        self.assertTrue((root / ".isomer-labs" / ".houmao" / "houmao-config.toml").is_file())
        self.assertFalse((root / ".houmao").exists())
        manifest = tomllib.loads((root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8"))
        self.assertEqual("isomer-content", manifest["paths"]["isomer_content_root"])
        self.assertEqual("isomer-content/topic-ws", manifest["paths"]["topic_workspace_base_dir"])
        self.assertNotIn("defaults", manifest)
        self.assertNotIn("research_topics", manifest)
        self.assertNotIn("topic_workspaces", manifest)
        self.assertIn("Generated Content Root:", output)
        self.assertIn("Topic Workspace Base:", output)
        self.assertIn("Research Topics: none registered", output)
        self.assertIn("Houmao Project Directory:", output)
        self.assertIn("Houmao Overlay:", output)
        help_result = CliRunner().invoke(cli.app, ["project", "init", "--help"])
        self.assertEqual(0, help_result.exit_code, help_result.output)
        self.assertNotIn("--force", help_result.output)

        status, output = self.run_cli(["project", "init"], cwd=root, env=self.fake_houmao_env(root))
        self.assertEqual(1, status)
        self.assertIn("refuses to overwrite", output)
        self.assertIn("project cleanup --part bootstrap --dry-run", output)

    def test_init_rejects_old_topic_initialization_forms(self) -> None:
        for args in (
            ["project", "init", "paper", "--json"],
            ["project", "init", "--topic-id", "paper", "--json"],
            ["project", "init", "--topic-statement", "Investigate paper behavior.", "--json"],
        ):
            with self.subTest(args=args):
                root = self.make_root()
                status, output = self.run_cli(args, cwd=root, env=self.fake_houmao_env(root))
                data = json.loads(output)
                self.assertEqual(1, status)
                self.assertFalse(data["mutated"])
                self.assertTrue(any("Project init does not create Research Topics" in diagnostic["message"] for diagnostic in data["diagnostics"]))
                self.assertFalse((root / ".isomer-labs" / "manifest.toml").exists())

    def test_empty_project_allows_project_commands_and_reports_topic_context_guidance(self) -> None:
        root = self.make_root()
        self.init_project(root, create_topic=False)

        status, output = self.run_cli(["project", "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertEqual([], data["manifest"]["research_topics"])

        status, output = self.run_cli(["project", "topics", "list", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual([], data["topics"])

        status, output = self.run_cli(["project", "workspaces", "list", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual([], data["workspaces"])

        status, output = self.run_cli(["project", "runtime", "inspect", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("project topics create" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

    def test_init_and_cleanup_preserve_external_root_houmao_overlay(self) -> None:
        root = self.make_root()
        write(root / ".houmao" / "external.toml", "user_owned = true\n")

        status, output = self.run_cli(["project", "init"], cwd=root, env=self.fake_houmao_env(root))
        self.assertEqual(0, status, output)
        self.assertTrue((root / ".houmao" / "external.toml").is_file())
        self.assertTrue((root / ".isomer-labs" / ".houmao" / "houmao-config.toml").is_file())

        status, output = self.run_cli(["project", "cleanup", "--part", "houmao-overlay", "--yes", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertFalse((root / ".isomer-labs" / ".houmao").exists())
        self.assertTrue((root / ".houmao" / "external.toml").is_file())

    def test_project_cleanup_dry_run_and_default_non_mutating_plan(self) -> None:
        root = self.make_root()
        self.init_project(root)

        status, output = self.run_cli(["project", "cleanup", "--part", "project-config", "--dry-run", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertFalse(data["mutated"])
        self.assertTrue(data["dry_run"])
        self.assertEqual(["project-config"], data["selected_parts"])
        self.assertEqual(root / ".isomer-labs", Path(data["planned_removals"][0]["path"]))
        self.assertTrue((root / ".isomer-labs" / "manifest.toml").is_file())

        status, output = self.run_cli(["project", "cleanup", "--part", "project-config"], cwd=root)
        self.assertEqual(0, status, output)
        self.assertIn("Mode: dry-run", output)
        self.assertIn("pass --yes", output)
        self.assertTrue((root / ".isomer-labs" / "manifest.toml").is_file())

    def test_project_cleanup_confirmed_partial_and_bootstrap_cleanup(self) -> None:
        root = self.make_root()
        self.init_project(root)

        status, output = self.run_cli(
            [
                "project",
                "cleanup",
                "--part",
                "houmao-overlay",
                "--part",
                "content-policy",
                "--yes",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertFalse((root / ".isomer-labs" / ".houmao").exists())
        self.assertFalse((root / "isomer-content" / "README.md").exists())
        self.assertFalse((root / "isomer-content" / ".gitignore").exists())
        self.assertTrue((root / ".isomer-labs" / "manifest.toml").is_file())
        self.assertTrue((root / "isomer-content" / "topic-ws" / "default").is_dir())

        status, output = self.run_cli(["project", "cleanup", "--part", "bootstrap", "--yes", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertFalse((root / ".isomer-labs").exists())
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default").exists())

        status, output = self.run_cli(["project", "init"], cwd=root, env=self.fake_houmao_env(root))
        self.assertEqual(0, status, output)
        self.assertTrue((root / ".isomer-labs" / "manifest.toml").is_file())

    def test_project_cleanup_runtime_preserves_topic_source_material(self) -> None:
        root = self.make_root()
        self.init_project(root)
        runtime_root = root / "isomer-content" / "topic-ws" / "default"
        write(runtime_root / "team-profile" / "profile.toml", 'id = "source"\n')
        status, output = self.run_cli(["project", "runtime", "init", "--json"], cwd=root)
        self.assertEqual(0, status, output)
        write(runtime_root / "runtime" / "adapters" / "houmao" / "ati-default" / "adapter-link.json", "{}\n")

        status, output = self.run_cli(["project", "cleanup", "--part", "runtime", "--topic", "default", "--yes", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertFalse((runtime_root / "state.sqlite").exists())
        for directory in ("repos", "agents", "records", "runtime"):
            self.assertFalse((runtime_root / directory).exists())
        self.assertTrue((runtime_root / "team-profile" / "profile.toml").is_file())

    def test_project_cleanup_topic_workspace_and_content_root_purge(self) -> None:
        root = self.make_root()
        self.make_two_topic_project(root)
        write(root / "topic-workspaces" / "alpha" / "topic-def" / "topic-overview.md", "# Alpha\n")
        write(root / "topic-workspaces" / "beta" / "topic-def" / "topic-overview.md", "# Beta\n")
        write(root / "isomer-content" / "README.md", "# Isomer Content\n")
        write(root / "isomer-content" / ".gitignore", "*\n")
        write(root / "isomer-content" / "unknown.txt", "operator-owned\n")

        status, output = self.run_cli(["project", "cleanup", "--part", "topic-workspace", "--topic", "beta", "--yes", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertTrue((root / "topic-workspaces" / "alpha" / "topic-def" / "topic-overview.md").is_file())
        self.assertFalse((root / "topic-workspaces" / "beta").exists())
        self.assertTrue((root / "isomer-content" / "unknown.txt").is_file())

        status, output = self.run_cli(["project", "cleanup", "--part", "content-root", "--purge-content-root", "--yes", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertFalse((root / "isomer-content").exists())

    def test_project_cleanup_manifest_limited_authority_and_topic_refusal(self) -> None:
        root = self.make_root()
        write(root / ".isomer-labs" / "manifest.toml", "not toml = [\n")
        write(root / ".houmao" / "houmao-config.toml", "schema_version = 1\n")
        write(root / ".isomer-labs" / ".houmao" / "houmao-config.toml", "schema_version = 1\n")
        write(root / "isomer-content" / "README.md", "# Isomer Content\n")
        write(root / "isomer-content" / ".gitignore", "*\n")

        status, output = self.run_cli(["project", "cleanup", "--part", "content-policy", "--dry-run", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(any(diagnostic["severity"] == "warning" for diagnostic in data["diagnostics"]))
        self.assertEqual(
            {str(root / "isomer-content" / "README.md"), str(root / "isomer-content" / ".gitignore")},
            {target["path"] for target in data["planned_removals"]},
        )

        status, output = self.run_cli(["project", "cleanup", "--part", "runtime", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("requires a valid Project Manifest" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])
        self.assertTrue((root / ".houmao" / "houmao-config.toml").is_file())
        self.assertTrue((root / ".isomer-labs" / ".houmao" / "houmao-config.toml").is_file())

        missing_manifest_root = self.make_root()
        write(missing_manifest_root / ".houmao" / "houmao-config.toml", "schema_version = 1\n")
        write(missing_manifest_root / ".isomer-labs" / ".houmao" / "houmao-config.toml", "schema_version = 1\n")
        status, output = self.run_cli(
            ["project", "--root", str(missing_manifest_root), "cleanup", "--part", "houmao-overlay", "--dry-run", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["dry_run"])
        self.assertEqual(str(missing_manifest_root / ".isomer-labs" / ".houmao"), data["planned_removals"][0]["path"])
        self.assertTrue((missing_manifest_root / ".houmao" / "houmao-config.toml").is_file())

    def test_project_cleanup_content_root_requires_purge_and_respects_symlink_entries(self) -> None:
        root = self.make_root()
        self.init_project(root)

        status, output = self.run_cli(["project", "cleanup", "--part", "content-root", "--yes", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        self.assertTrue((root / "isomer-content").is_dir())
        self.assertIn("requires --purge-content-root", data["diagnostics"][0]["message"])

        status, output = self.run_cli(
            ["project", "cleanup", "--part", "content-policy", "--content-dir", "../outside", "--dry-run", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        self.assertTrue(any("outside the Project root" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        status, output = self.run_cli(
            ["project", "cleanup", "--part", "content-policy", "--content-dir", ".isomer-labs/generated", "--dry-run", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        self.assertTrue(any("Project Config Directory" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        outside = self.make_root() / "outside-houmao"
        write(outside / "keep.txt", "keep\n")
        shutil.rmtree(root / ".isomer-labs" / ".houmao")
        (root / ".isomer-labs" / ".houmao").symlink_to(outside, target_is_directory=True)

        status, output = self.run_cli(["project", "cleanup", "--part", "houmao-overlay", "--yes", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertFalse((root / ".isomer-labs" / ".houmao").exists())
        self.assertTrue((outside / "keep.txt").is_file())

        status, output = self.run_cli(
            ["project", "cleanup", "--part", "content-root", "--content-dir", ".", "--purge-content-root", "--yes", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        self.assertTrue(any("Project root" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

    def test_project_content_root_move_dry_run_and_default_non_mutating_plan(self) -> None:
        root = self.make_root()
        self.init_project(root)
        write(root / "isomer-content" / "unknown.txt", "operator-owned\n")

        status, output = self.run_cli(["project", "content-root", "move", "--to", "generated", "--dry-run", "--json"], cwd=root)
        data = json.loads(output)

        self.assertEqual(0, status, output)
        self.assertTrue(data["ok"])
        self.assertFalse(data["mutated"])
        self.assertTrue(data["dry_run"])
        self.assertEqual(str(root / "isomer-content"), data["old_content_root"])
        self.assertEqual(str(root / "generated"), data["new_content_root"])
        self.assertIn("runtime", " ".join(data["warnings"]).lower())
        self.assertIn(
            str(root / "isomer-content" / "unknown.txt"),
            {entry["path"] for entry in data["unmanaged_leftovers"]},
        )
        self.assertTrue((root / "isomer-content" / "topic-ws" / "default").is_dir())
        self.assertFalse((root / "generated").exists())
        manifest = (root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8")
        self.assertIn('isomer_content_root = "isomer-content"', manifest)

        status, output = self.run_cli(["project", "content-root", "move", "--to", "generated"], cwd=root)
        self.assertEqual(0, status, output)
        self.assertIn("Mode: dry-run", output)
        self.assertIn("pass --yes", output)
        self.assertFalse((root / "generated").exists())

    def test_project_content_root_move_confirmed_updates_manifest_and_preserves_leftovers(self) -> None:
        root = self.make_root()
        self.init_project(root)
        write(root / "isomer-content" / "topic-ws" / "default" / "topic-def" / "topic-overview.md", "# Default\n")
        write(root / "isomer-content" / "unknown.txt", "operator-owned\n")

        status, output = self.run_cli(["project", "content-root", "move", "--to", "generated", "--yes", "--json"], cwd=root)
        data = json.loads(output)

        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertFalse(data["dry_run"])
        self.assertTrue((root / "generated" / "README.md").is_file())
        self.assertTrue((root / "generated" / ".gitignore").is_file())
        self.assertTrue((root / "generated" / "topic-ws" / "default" / "topic-def" / "topic-overview.md").is_file())
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default").exists())
        self.assertTrue((root / "isomer-content" / "unknown.txt").is_file())
        manifest = (root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8")
        self.assertIn('isomer_content_root = "generated"', manifest)
        self.assertIn('topic_workspace_base_dir = "generated/topic-ws"', manifest)
        self.assertIn('path = "generated/topic-ws/default"', manifest)

        status, output = self.run_cli(["project", "validate", "--json"], cwd=root)
        self.assertEqual(0, status, output)

    def test_project_content_root_move_refusals_and_external_workspace_preservation(self) -> None:
        root = self.make_root()
        self.init_project(root)
        self.append_manifest(
            root,
            """
            [[research_topics]]
            id = "external"
            config_path = ".isomer-labs/research-topics/external.toml"
            topic_workspace_id = "external"
            status = "active"

            [[topic_workspaces]]
            id = "external"
            research_topic_id = "external"
            path = "topic-workspaces/external"
            status = "active"
            """,
        )
        write(root / ".isomer-labs" / "research-topics" / "external.toml", 'research_topic_id = "external"\n')
        write(root / "topic-workspaces" / "external" / "note.md", "external\n")

        status, output = self.run_cli(["project", "content-root", "move", "--to", "generated", "--dry-run", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertIn(
            str(root / "topic-workspaces" / "external"),
            {entry["path"] for entry in data["skipped_entries"]},
        )
        self.assertFalse(any(update["field"] == "topic_workspaces.external.path" for update in data["manifest_updates"]))

        for content_dir, expected_message in (
            ("../outside", "outside the Project root"),
            (".isomer-labs/generated", "Project Config Directory"),
            (".houmao/generated", "external Houmao state"),
            (".", "Project root"),
        ):
            with self.subTest(content_dir=content_dir):
                status, output = self.run_cli(
                    ["project", "content-root", "move", "--to", content_dir, "--yes", "--json"],
                    cwd=root,
                )
                data = json.loads(output)
                self.assertEqual(1, status)
                self.assertFalse(data["mutated"])
                self.assertTrue(any(expected_message in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        (root / "linked-content").symlink_to(root / "isomer-content", target_is_directory=True)
        status, output = self.run_cli(["project", "content-root", "move", "--to", "linked-content", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("symlink" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

    def test_project_content_root_move_preserves_runtime_internals(self) -> None:
        root = self.make_root()
        self.init_project(root)
        runtime_root = root / "isomer-content" / "topic-ws" / "default"
        status, output = self.run_cli(["project", "runtime", "init", "--json"], cwd=root)
        self.assertEqual(0, status, output)
        write(runtime_root / ".pixi" / "prefix.txt", "old-prefix\n")
        write(runtime_root / "runtime" / "adapters" / "houmao" / "ati-default" / "adapter-runtime-manifest.json", "{}\n")
        write(runtime_root / "logs" / "run.log", "old log\n")
        old_db_path = runtime_root / "state.sqlite"
        with sqlite3.connect(old_db_path) as db:
            old_paths = {row[0] for row in db.execute("SELECT path FROM path_plans")}
        self.assertTrue(any(str(runtime_root) in path for path in old_paths))

        status, output = self.run_cli(["project", "content-root", "move", "--to", "generated", "--yes", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertTrue(any("state.sqlite" in warning for warning in data["warnings"]), data["warnings"])
        new_runtime_root = root / "generated" / "topic-ws" / "default"
        new_db_path = new_runtime_root / "state.sqlite"
        self.assertFalse(old_db_path.exists())
        self.assertTrue(new_db_path.is_file())
        self.assertTrue((new_runtime_root / ".pixi" / "prefix.txt").is_file())
        self.assertTrue((new_runtime_root / "runtime" / "adapters" / "houmao" / "ati-default" / "adapter-runtime-manifest.json").is_file())
        self.assertTrue((new_runtime_root / "logs" / "run.log").is_file())
        with sqlite3.connect(new_db_path) as db:
            new_paths = {row[0] for row in db.execute("SELECT path FROM path_plans")}
        self.assertEqual(old_paths, new_paths)
        self.assertTrue(any(str(runtime_root) in path for path in new_paths))

    def test_project_content_root_move_help_and_discovery_selectors(self) -> None:
        root = self.make_root()
        self.init_project(root)
        nested = root / "nested" / "deeper"
        nested.mkdir(parents=True)
        runner = CliRunner()
        for help_args, expected in (
            (["project", "--help"], "content-root"),
            (["project", "content-root", "--help"], "move"),
            (["project", "content-root", "move", "--help"], "--to"),
        ):
            result = runner.invoke(cli.app, help_args)
            self.assertEqual(0, result.exit_code, result.output)
            self.assertIn(expected, result.output)

        result = runner.invoke(cli.app, ["project", "content-root", "move", "--dry-run"])
        self.assertNotEqual(0, result.exit_code)

        status, output = self.run_cli(["project", "content-root", "move", "--to", "generated", "--dry-run", "--json"], cwd=nested)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(str(root), data["project_root"])

        status, output = self.run_cli(
            ["project", "--root", str(root), "content-root", "move", "--to", "generated", "--dry-run", "--json"],
            cwd=self.make_root(),
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(str(root), data["project_root"])

        status, output = self.run_cli(
            [
                "project",
                "--manifest",
                str(root / ".isomer-labs" / "manifest.toml"),
                "content-root",
                "move",
                "--to",
                "generated",
                "--dry-run",
                "--json",
            ],
            cwd=self.make_root(),
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(str(root), data["project_root"])

    def test_topics_create_default_workspace_and_show(self) -> None:
        root = self.make_root()
        self.init_project(root, create_topic=False)

        status, output = self.run_cli(
            ["project", "topics", "create", "paper", "--statement", "Investigate paper retrieval quality.", "--set-default", "--json"],
            cwd=root,
        )
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
        self.assertEqual(str(root / "isomer-content" / "topic-ws" / "paper"), data["topic_workspace_path"])
        self.assertTrue(data["set_default"])

        status, output = self.run_cli(["project", "topics", "show", "paper", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("paper", data["topic"]["id"])
        self.assertEqual("Investigate paper retrieval quality.", data["topic_config"]["topic_statement"])
        self.assertEqual(str(root / "isomer-content" / "topic-ws" / "paper"), data["topic_workspace_path"])

        status, output = self.run_cli(["project", "topics", "show", "missing", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("not registered" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

    def test_init_accepts_custom_content_dir_without_creating_topic_workspace(self) -> None:
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
        self.assertFalse((root / "custom-content" / "topic-ws" / "default").exists())
        self.assertIn('isomer_content_root = "custom-content"', manifest)
        self.assertIn('topic_workspace_base_dir = "custom-content/topic-ws"', manifest)
        self.assertNotIn('path = "custom-content/topic-ws/default"', manifest)
        self.assertNotIn("[[research_topics]]", manifest)
        self.assertNotIn("[[topic_workspaces]]", manifest)
        self.assertEqual(str(root / "custom-content"), data["content_root_path"])
        self.assertEqual(str(root / "custom-content" / "topic-ws"), data["topic_workspace_base_path"])
        self.assertFalse((root / "isomer-content").exists())

    def test_topics_create_uses_custom_content_dir_defaults_and_validates_inputs(self) -> None:
        root = self.make_root()
        status, output = self.run_cli(
            ["project", "init", "--content-dir", "generated/isomer", "--json"],
            cwd=root,
            env=self.fake_houmao_env(root),
        )
        self.assertEqual(0, status, output)

        status, output = self.run_cli(
            ["project", "topics", "create", "paper", "--statement", "Investigate paper retrieval quality.", "--json"],
            cwd=root,
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
        self.assertEqual(str(root / "generated" / "isomer" / "topic-ws" / "paper"), data["topic_workspace_path"])

        status, output = self.run_cli(
            ["project", "topics", "create", "paper", "--statement", "Investigate another topic.", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("already registered" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        status, output = self.run_cli(["project", "topics", "create", "placeholder", "--statement", "placeholder", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("generic placeholder" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        status, output = self.run_cli(
            ["project", "topics", "create", "outside", "--statement", "Investigate outside workspace handling.", "--workspace-dir", "../outside", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("outside the Project root" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        status, output = self.run_cli(
            ["project", "topics", "create", "custom", "--statement", "Investigate custom topic workspace handling.", "--workspace-dir", "topic-workspaces/custom", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(str(root / "topic-workspaces" / "custom"), data["topic_workspace_path"])
        self.assertTrue((root / "topic-workspaces" / "custom").is_dir())

    def test_topics_update_statement_status_default_and_refuses_rename(self) -> None:
        root = self.make_root()
        self.init_project(root, "alpha")
        status, output = self.run_cli(
            ["project", "topics", "create", "beta", "--statement", "Investigate beta topic behavior.", "--json"],
            cwd=root,
        )
        self.assertEqual(0, status, output)

        status, output = self.run_cli(
            [
                "project",
                "topics",
                "update",
                "beta",
                "--statement",
                "Investigate updated beta topic behavior.",
                "--status",
                "archived",
                "--set-default",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertEqual(
            {"topic_statement", "status", "defaults.research_topic_id", "defaults.topic_workspace_id"},
            set(data["updated_fields"]),
        )

        manifest = tomllib.loads((root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8"))
        beta = next(topic for topic in manifest["research_topics"] if topic["id"] == "beta")
        self.assertEqual("archived", beta["status"])
        self.assertEqual("beta", manifest["defaults"]["research_topic_id"])
        beta_config = tomllib.loads((root / ".isomer-labs" / "research-topics" / "beta.toml").read_text(encoding="utf-8"))
        self.assertEqual("Investigate updated beta topic behavior.", beta_config["topic_statement"])

        status, output = self.run_cli(["project", "topics", "update", "beta", "--status", "paused", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("active or archived" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        status, output = self.run_cli(["project", "topics", "update", "beta", "--new-id", "gamma", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("rename is not supported" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

    def test_topics_delete_plans_confirms_preserves_workspace_and_blocks_dependencies(self) -> None:
        root = self.make_root()
        self.init_project(root, "alpha")
        write(root / "isomer-content" / "topic-ws" / "alpha" / "topic-def" / "topic-overview.md", "# Alpha\n")

        status, output = self.run_cli(["project", "topics", "delete", "alpha", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("requires --dry-run or --yes" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        status, output = self.run_cli(["project", "topics", "delete", "alpha", "--dry-run", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertTrue(data["dry_run"])
        self.assertIn(str(root / "isomer-content" / "topic-ws" / "alpha"), data["preserved_paths"])
        self.assertTrue((root / ".isomer-labs" / "research-topics" / "alpha.toml").is_file())

        write(root / "isomer-content" / "topic-ws" / "alpha" / "state.sqlite", "")
        status, output = self.run_cli(["project", "topics", "delete", "alpha", "--yes", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(data["delete_plan"]["blockers"])
        self.assertTrue((root / ".isomer-labs" / "research-topics" / "alpha.toml").is_file())

        (root / "isomer-content" / "topic-ws" / "alpha" / "state.sqlite").unlink()
        status, output = self.run_cli(["project", "topics", "delete", "alpha", "--yes", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertFalse((root / ".isomer-labs" / "research-topics" / "alpha.toml").exists())
        self.assertTrue((root / "isomer-content" / "topic-ws" / "alpha" / "topic-def" / "topic-overview.md").is_file())
        manifest = tomllib.loads((root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8"))
        self.assertNotIn("defaults", manifest)
        self.assertNotIn("research_topics", manifest)
        self.assertNotIn("topic_workspaces", manifest)

    def test_init_rejects_invalid_custom_content_dirs_before_mutation(self) -> None:
        for content_dir, expected_message in (
            ("../outside", "outside the Project root"),
            (".isomer-labs/generated", "Project Config Directory"),
            (".houmao", "external Houmao state"),
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
                self.assertFalse((root / ".isomer-labs" / ".houmao").exists())

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
            ["project", "--root", str(nested), "init", "--json"],
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

    def test_skill_callbacks_register_resolve_show_disable_validate_and_context_refs(self) -> None:
        root = self.make_root()
        self.init_project(root)

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "register",
                "--topic",
                "default",
                "--id",
                "scout-begin-domain",
                "--skill",
                "isomer-deepsci-scout",
                "--stage",
                "begin",
                "--prompt",
                "Prefer the local benchmark contract before broad discovery.",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertEqual("scout-begin-domain", data["callback"]["id"])
        self.assertEqual("prompt", data["callback"]["source"]["source_type"])
        registry_path = root / ".isomer-labs" / "user-skill-callbacks" / "topics" / "default" / "registry.toml"
        self.assertTrue(registry_path.is_file())
        prompt_path = root / ".isomer-labs" / "user-skill-callbacks" / "topics" / "default" / "prompts" / "scout-begin-domain.md"
        self.assertTrue(prompt_path.is_file())

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "resolve",
                "--topic",
                "default",
                "--skill",
                "isomer-deepsci-scout",
                "--stage",
                "begin",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["scout-begin-domain"], [callback["id"] for callback in data["callbacks"]])

        for command in ("list", "show", "validate"):
            args = ["project", "skill-callbacks", command, "--topic", "default", "--json"]
            if command == "show":
                args.insert(3, "scout-begin-domain")
            status, output = self.run_cli(args, cwd=root)
            data = json.loads(output)
            self.assertEqual(0, status, output)
            self.assertTrue(data["ok"])

        status, output = self.run_cli(["project", "context", "show", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(
            [".isomer-labs/user-skill-callbacks/topics/default/registry.toml"],
            data["context"]["user_skill_callback_registry_refs"]["research_topic"],
        )

        status, output = self.run_cli(
            ["project", "skill-callbacks", "disable", "scout-begin-domain", "--topic", "default", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("active", data["previous_status"])
        self.assertEqual("inactive", data["new_status"])

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "resolve",
                "--topic",
                "default",
                "--skill",
                "isomer-deepsci-scout",
                "--stage",
                "begin",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual([], data["callbacks"])

    def test_system_extensions_cli_remembers_and_forgets_project_declarations(self) -> None:
        root = self.make_root()
        self.init_project(root, create_topic=False)

        status, output = self.run_cli(["project", "system-extensions", "list", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertEqual(["deepsci"], [extension["extension_id"] for extension in data["extensions"]])
        self.assertFalse(data["extensions"][0]["declared_installed"])
        self.assertFalse(data["extensions"][0]["installation_verified"])

        status, output = self.run_cli(["project", "system-extensions", "remember", "deepsci", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertTrue(data["extensions"][0]["declared_installed"])
        self.assertEqual("project_manifest_user_declared", data["extensions"][0]["availability_basis"])
        manifest_text = (root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8")
        self.assertIn("[operator.system_extensions]", manifest_text)
        self.assertIn('installed = ["deepsci"]', manifest_text)

        status, output = self.run_cli(["project", "system-extensions", "remember", "deepsci", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])

        status, output = self.run_cli(["project", "system-extensions", "forget", "deepsci", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertFalse(data["extensions"][0]["declared_installed"])

    def test_system_extensions_cli_rejects_unknown_and_missing_project(self) -> None:
        root = self.make_root()
        self.init_project(root, create_topic=False)

        status, output = self.run_cli(["project", "system-extensions", "remember", "unknown", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status, output)
        self.assertFalse(data["mutated"])
        self.assertTrue(any("Unknown packaged system extension" in diagnostic["message"] for diagnostic in data["diagnostics"]))

        empty = self.make_root()
        status, output = self.run_cli(["project", "system-extensions", "list", "--json"], cwd=empty)
        data = json.loads(output)
        self.assertEqual(1, status, output)
        self.assertEqual([], data["extensions"])

    def test_skill_callback_insertion_points_query_catalog_and_project_declarations(self) -> None:
        root = self.make_root()
        self.init_project(root, create_topic=False)

        status, output = self.run_cli(["project", "skill-callbacks", "insertion-points", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual([], data["insertion_points"])

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "insertion-points",
                "--extension",
                "deepsci",
                "--skill",
                "isomer-deepsci-scout",
                "--stage",
                "begin",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(1, len(data["insertion_points"]))
        self.assertEqual("catalog_requested_not_verified", data["insertion_points"][0]["availability_basis"])
        self.assertFalse(data["insertion_points"][0]["installation_verified"])

        status, output = self.run_cli(["project", "system-extensions", "remember", "deepsci", "--json"], cwd=root)
        self.assertEqual(0, status, output)

        status, output = self.run_cli(["project", "skill-callbacks", "insertion-points", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(44, len(data["insertion_points"]))
        self.assertEqual("project_manifest_user_declared", data["insertion_points"][0]["availability_basis"])

        status, output = self.run_cli(["project", "skill-callbacks", "insertion-points", "--all-catalog-extensions", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(44, len(data["insertion_points"]))

        status, output = self.run_cli(["project", "skill-callbacks", "insertion-points", "--core-only", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual([], data["insertion_points"])

    def test_skill_callback_insertion_points_reject_invalid_filters_and_missing_project(self) -> None:
        root = self.make_root()
        self.init_project(root, create_topic=False)

        status, output = self.run_cli(["project", "skill-callbacks", "insertion-points", "--extension", "unknown", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status, output)
        self.assertTrue(any("Unknown packaged system extension" in diagnostic["message"] for diagnostic in data["diagnostics"]))

        status, output = self.run_cli(
            ["project", "skill-callbacks", "insertion-points", "--core-only", "--extension", "deepsci", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status, output)
        self.assertTrue(any("--core-only" in diagnostic["message"] for diagnostic in data["diagnostics"]))

        empty = self.make_root()
        status, output = self.run_cli(["project", "skill-callbacks", "insertion-points", "--json"], cwd=empty)
        data = json.loads(output)
        self.assertEqual(1, status, output)
        self.assertEqual([], data["insertion_points"])

    def test_skill_callback_validation_rejects_undeclared_insertion_points(self) -> None:
        root = self.make_root()
        self.init_project(root)

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "register",
                "--topic",
                "default",
                "--id",
                "entrypoint-begin",
                "--skill",
                "isomer-op-entrypoint",
                "--stage",
                "begin",
                "--prompt",
                "Prefer local context.",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status, output)
        self.assertTrue(any("isomer-op-entrypoint/begin" in diagnostic["message"] for diagnostic in data["diagnostics"]))
        self.assertTrue(any("skill-callbacks insertion-points" in diagnostic["message"] for diagnostic in data["diagnostics"]))

        write(
            root / "toolboxes" / "bad" / "manifest.toml",
            """
            schema_version = "isomer-toolbox.v1"
            kind = "toolbox-callback-bundle"
            toolbox_id = "bad.toolbox"

            [[callbacks]]
            target_skill = "isomer-op-entrypoint"
            stage = "begin"
            source_type = "prompt"
            prompt = "Prefer local context."
            """,
        )
        status, output = self.run_cli(
            ["project", "skill-callbacks", "install", "--topic", "default", "--toolbox-dir", "toolboxes/bad", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status, output)
        self.assertTrue(any("isomer-op-entrypoint/begin" in diagnostic["message"] for diagnostic in data["diagnostics"]))

    def test_toolbox_cli_manages_project_and_topic_agent_runtime_params(self) -> None:
        root = self.make_root()
        self.init_project(root)
        write(
            root / "toolboxes" / "demo" / "manifest.toml",
            """
            schema_version = "isomer-toolbox.v1"
            toolbox_id = "demo.toolbox"
            kind = "toolbox-callback-bundle"
            """,
        )

        status, output = self.run_cli(
            ["project", "toolboxes", "install", "--toolbox-dir", "toolboxes/demo", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("demo.toolbox", data["toolbox"]["toolbox_id"])

        status, output = self.run_cli(
            [
                "project",
                "toolbox-params",
                "set",
                "demo.toolbox:mode",
                "--value",
                "strict",
                "--value-type",
                "enum",
                "--allowed-value",
                "strict",
                "--allowed-value",
                "relaxed",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("strict", data["param"]["value"])

        status, output = self.run_cli(
            [
                "project",
                "toolbox-params",
                "set",
                "demo.toolbox:mode",
                "--topic",
                "default",
                "--scope",
                "topic_agent",
                "--topic-agent",
                "coder",
                "--value",
                "relaxed",
                "--value-type",
                "enum",
                "--allowed-value",
                "strict",
                "--allowed-value",
                "relaxed",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("topic_agent", data["param"]["effective_scope"])

        status, output = self.run_cli(
            ["project", "toolbox-params", "get", "demo.toolbox:mode", "--topic", "default", "--topic-agent", "coder", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("relaxed", data["param"]["value"])
        self.assertEqual("coder", data["param"]["source"]["topic_agent_name"])

        for args in (
            ["project", "toolboxes", "list", "--topic", "default", "--json"],
            ["project", "toolboxes", "show", "demo.toolbox", "--topic", "default", "--json"],
            ["project", "toolboxes", "explain", "demo.toolbox", "--topic", "default", "--json"],
            ["project", "toolboxes", "validate", "--topic", "default", "--json"],
            ["project", "toolbox-params", "list", "--topic", "default", "--topic-agent", "coder", "--json"],
            ["project", "toolbox-params", "explain", "demo.toolbox:mode", "--topic", "default", "--topic-agent", "coder", "--json"],
            ["project", "toolbox-params", "validate", "--topic", "default", "--topic-agent", "coder", "--json"],
        ):
            status, output = self.run_cli(args, cwd=root)
            data = json.loads(output)
            self.assertEqual(0, status, output)
            self.assertTrue(data["ok"])

        status, output = self.run_cli(["project", "toolboxes", "disable", "demo.toolbox", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("disabled", data["toolbox"]["status"])
        status, output = self.run_cli(["project", "toolboxes", "enable", "demo.toolbox", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("active", data["toolbox"]["status"])
        status, output = self.run_cli(["project", "toolboxes", "update-source", "demo.toolbox", "--source-path", "toolboxes/renamed", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("toolboxes/renamed", data["toolbox"]["source_path"])

        write(
            root / ".isomer-labs" / "param-defaults.toml",
            """
            schema_version = "isomer-toolbox-runtime-params.v1"

            [[toolbox_runtime_params]]
            toolbox_id = "demo.toolbox"
            key = "profile"
            value = "default"
            value_type = "string"
            scope = "project"
            """,
        )
        status, output = self.run_cli(["project", "toolbox-params", "import", "add", "demo.toolbox", "param-defaults.toml", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("param-defaults.toml", data["import"]["path"])
        status, output = self.run_cli(["project", "toolbox-params", "import", "list", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("param-defaults.toml", data["imports"][0]["path"])
        status, output = self.run_cli(["project", "toolbox-params", "import", "show", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["imports"])
        status, output = self.run_cli(["project", "toolbox-params", "import", "remove", "demo.toolbox", "param-defaults.toml", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])

        status, output = self.run_cli(["project", "toolbox-params", "unset", "demo.toolbox:mode", "--topic", "default", "--scope", "topic_agent", "--topic-agent", "coder", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        status, output = self.run_cli(["project", "toolboxes", "uninstall", "demo.toolbox", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])

    def test_old_toolbox_cli_names_are_rejected(self) -> None:
        root = self.make_root()
        self.init_project(root)

        for args in (
            ["project", "user-plugins", "list"],
            ["project", "user-plugin-params", "list"],
            ["project", "skill-callbacks", "install", "--plugin-dir", "skillset/toolboxes/demo"],
        ):
            status, stdout, stderr = self.run_main(args, cwd=root)
            self.assertNotEqual(0, status)
            self.assertIn("No such", stdout + stderr)

    def test_skill_callbacks_project_scope_external_skill_dir_requires_explicit_flag(self) -> None:
        root = self.make_root()
        self.init_project(root)
        external_root = self.make_root() / "external-skill"
        write(
            external_root / "SKILL.md",
            """
            ---
            name: callback-extension
            description: External callback fixture.
            ---

            # Callback Extension
            """,
        )

        base_args = [
            "project",
            "skill-callbacks",
            "register",
            "--scope",
            "project",
            "--id",
            "project-end-callback",
            "--skill",
            "isomer-deepsci-scout",
            "--stage",
            "end",
            "--skill-dir",
            str(external_root),
            "--json",
        ]
        status, output = self.run_cli(base_args, cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO005", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        status, output = self.run_cli([*base_args[:-1], "--allow-external-source", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["callback"]["source"]["external"])
        self.assertEqual("skill_dir", data["callback"]["source"]["source_type"])

    def test_skill_callbacks_install_toolbox_manifest_composes_same_extension_point(self) -> None:
        root = self.make_root()
        self.init_project(root)
        toolbox_a = root / "skillset" / "toolboxes" / "toolbox-a"
        toolbox_b = root / "skillset" / "toolboxes" / "toolbox-b"
        write(toolbox_a / "callback-a" / "SKILL.md", "# A\n")
        write(toolbox_a / "callback-b" / "SKILL.md", "# B\n")
        write(toolbox_a / "callback-z" / "SKILL.md", "# Z\n")
        write(toolbox_b / "callback-a" / "SKILL.md", "# B\n")
        write(
            toolbox_a / "manifest.toml",
            """
            schema_version = "isomer-toolbox.v1"
            toolbox_id = "toolbox-a"
            kind = "toolbox-callback-bundle"

            [[callbacks]]
            key = "a"
            target_skill = "isomer-deepsci-scout"
            stage = "begin"
            priority = 1
            source_type = "skill_dir"
            skill_dir = "callback-a"

            [[callbacks]]
            key = "b"
            target_skill = "isomer-deepsci-scout"
            stage = "begin"
            priority = 20
            source_type = "skill_dir"
            skill_dir = "callback-b"

            [[callbacks]]
            key = "group/z"
            target_skill = "isomer-deepsci-scout"
            stage = "begin"
            priority = 999
            source_type = "skill_dir"
            skill_dir = "callback-z"
            """,
        )
        write(
            toolbox_b / "manifest.toml",
            """
            schema_version = "isomer-toolbox.v1"
            toolbox_id = "toolbox-b"
            kind = "toolbox-callback-bundle"

            [[callbacks]]
            key = "a"
            target_skill = "isomer-deepsci-scout"
            stage = "begin"
            source_type = "skill_dir"
            skill_dir = "callback-a"
            """,
        )

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "install",
                "--topic",
                "default",
                "--toolbox-dir",
                "skillset/toolboxes/toolbox-a",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("toolbox-a", data["toolbox_id"])
        self.assertEqual(["toolbox-a:a", "toolbox-a:b", "toolbox-a:group/z"], [callback["id"] for callback in data["callbacks"]])
        self.assertEqual(["a", "b", "group/z"], [callback["toolbox_key"] for callback in data["callbacks"]])
        self.assertEqual([100, 100, 100], [callback["priority"] for callback in data["callbacks"]])

        status, output = self.run_cli(["project", "toolboxes", "show", "toolbox-a", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("toolbox-a", data["toolbox"]["toolbox_id"])
        self.assertEqual("research_topic", data["toolbox"]["scope"])

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "install",
                "--topic",
                "default",
                "--toolbox-dir",
                "skillset/toolboxes/toolbox-b",
                "--json",
            ],
            cwd=root,
        )
        self.assertEqual(0, status, output)

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "resolve",
                "--topic",
                "default",
                "--skill",
                "isomer-deepsci-scout",
                "--stage",
                "begin",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(
            {"toolbox-a:a", "toolbox-a:b", "toolbox-a:group/z", "toolbox-b:a"},
            {callback["id"] for callback in data["callbacks"]},
        )
        self.assertEqual(["a", "b", "group/z"], [callback["toolbox_key"] for callback in data["callbacks"] if callback["toolbox_id"] == "toolbox-a"])

        status, output = self.run_cli(
            ["project", "skill-callbacks", "list", "--topic", "default", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(
            {"toolbox-a:a", "toolbox-a:b", "toolbox-a:group/z", "toolbox-b:a"},
            {callback["id"] for callback in data["callbacks"]},
        )

        status, output = self.run_cli(
            ["project", "skill-callbacks", "disable", "toolbox-a:a", "--topic", "default", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("inactive", data["new_status"])

    def test_skill_callbacks_install_rejects_duplicate_unlabeled_entries(self) -> None:
        root = self.make_root()
        self.init_project(root)
        toolbox = root / "skillset" / "toolboxes" / "bad-toolbox"
        write(toolbox / "one" / "SKILL.md", "# One\n")
        write(toolbox / "two" / "SKILL.md", "# Two\n")
        write(
            toolbox / "manifest.toml",
            """
            schema_version = "isomer-toolbox.v1"
            toolbox_id = "bad-toolbox"
            kind = "toolbox-callback-bundle"

            [[callbacks]]
            target_skill = "isomer-deepsci-scout"
            stage = "begin"
            source_type = "skill_dir"
            skill_dir = "one"

            [[callbacks]]
            target_skill = "isomer-deepsci-scout"
            stage = "begin"
            source_type = "skill_dir"
            skill_dir = "two"
            """,
        )

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "install",
                "--topic",
                "default",
                "--toolbox-dir",
                "skillset/toolboxes/bad-toolbox",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO104", {diagnostic["code"] for diagnostic in data["diagnostics"]})

    def test_skill_callbacks_install_rejects_same_toolbox_id_from_different_source_without_replace(self) -> None:
        root = self.make_root()
        self.init_project(root)
        toolbox_a = root / "skillset" / "toolboxes" / "toolbox-a"
        toolbox_copy = root / "skillset" / "toolboxes" / "toolbox-copy"
        for toolbox, callback_name in ((toolbox_a, "a"), (toolbox_copy, "copy")):
            write(toolbox / callback_name / "SKILL.md", "# Callback\n")
            write(
                toolbox / "manifest.toml",
                f"""
                schema_version = "isomer-toolbox.v1"
                toolbox_id = "shared-toolbox"
                kind = "toolbox-callback-bundle"

                [[callbacks]]
                key = "{callback_name}"
                target_skill = "isomer-deepsci-scout"
                stage = "begin"
                source_type = "skill_dir"
                skill_dir = "{callback_name}"
                """,
            )

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "install",
                "--topic",
                "default",
                "--toolbox-dir",
                "skillset/toolboxes/toolbox-a",
                "--json",
            ],
            cwd=root,
        )
        self.assertEqual(0, status, output)

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "install",
                "--topic",
                "default",
                "--toolbox-dir",
                "skillset/toolboxes/toolbox-copy",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO104", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        status, output = self.run_cli(
            [
                "project",
                "skill-callbacks",
                "install",
                "--topic",
                "default",
                "--toolbox-dir",
                "skillset/toolboxes/toolbox-copy",
                "--replace",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["shared-toolbox:copy"], [callback["id"] for callback in data["callbacks"]])

    def test_skill_callbacks_missing_project_is_rejected_without_creating_registry(self) -> None:
        root = self.make_root()

        status, output = self.run_cli(["project", "skill-callbacks", "list", "--json"], cwd=root)

        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("ISO001", data["diagnostics"][0]["code"])
        self.assertFalse((root / ".isomer-labs" / "user-skill-callbacks").exists())

    def test_config_accepts_callback_registry_refs_and_rejects_inline_callback_bodies(self) -> None:
        root = self.make_root()
        self.init_project(root)
        write(
            root / ".isomer-labs" / "user-skill-callbacks" / "registry.toml",
            """
            schema_version = "isomer-user-skill-callback-registry.v1"
            """,
        )
        manifest_path = root / ".isomer-labs" / "manifest.toml"
        manifest_text = manifest_path.read_text(encoding="utf-8")
        manifest_text = manifest_text.replace(
            "\n\n[paths]\n",
            '\nuser_skill_callback_registry_refs = [".isomer-labs/user-skill-callbacks/registry.toml"]\n\n[paths]\n',
            1,
        )
        manifest_path.write_text(manifest_text, encoding="utf-8")

        status, output = self.run_cli(["project", "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual([".isomer-labs/user-skill-callbacks/registry.toml"], data["manifest"]["user_skill_callback_registry_refs"])

        manifest_path.write_text(
            manifest_path.read_text(encoding="utf-8").replace(
                "\n\n[paths]\n",
                '\ncallback_prompt = "Do this inline."\n\n[paths]\n',
                1,
            ),
            encoding="utf-8",
        )
        status, output = self.run_cli(["project", "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO009", {diagnostic["code"] for diagnostic in data["diagnostics"]})
        self.assertTrue(any("User Skill Callback instruction bodies" in diagnostic["message"] for diagnostic in data["diagnostics"]))

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
            ["project", "paths", "preview", "--topic", "default", "--json"],
            cwd=root,
            env={"ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR": "isomer-content/topic-ws/default/custom-artifacts"},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        paths = {entry["surface"]: entry for entry in data["paths"]}
        self.assertEqual(str(root / "isomer-content"), paths["isomer_content_root"]["path"])
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "repos" / "topic-main" / "isomer-managed"),
            paths["topic_main_isomer_managed"]["path"],
        )
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "repos" / "topic-main" / "isomer-managed" / "tracked" / "artifacts"),
            paths["topic_main_tracked_artifacts"]["path"],
        )
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "repos" / "topic-main" / "isomer-managed" / "topic-owned" / "readonly" / "extern"),
            paths["topic_main_projections_readonly"]["path"],
        )
        self.assertEqual("topic.repos.main.projections.readonly", paths["topic_main_projections_readonly"]["semantic_label"])
        self.assertEqual("topic_repo_readonly_projection_dir", paths["topic_main_projections_readonly"]["storage_profile"])
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "repos" / "topic-main" / "isomer-managed" / "topic-owned" / "writable" / "extern"),
            paths["topic_main_projections_writable"]["path"],
        )
        self.assertEqual("topic_repo_writable_projection_dir", paths["topic_main_projections_writable"]["storage_profile"])
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "repos" / "topic-main" / "isomer-managed" / "tracked" / "manifests" / "extern-projections.toml"),
            paths["topic_main_projections_manifest"]["path"],
        )
        self.assertEqual("topic_repo_tracked_file", paths["topic_main_projections_manifest"]["storage_profile"])
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "tmp"),
            paths["topic_tmp"]["path"],
        )
        self.assertEqual("topic.tmp", paths["topic_tmp"]["semantic_label"])
        self.assertEqual("disposable", paths["topic_tmp"]["durability"])
        self.assertEqual("private", paths["topic_tmp"]["sharing"])
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "repos" / "topic-main" / "tmp"),
            paths["topic_main_tmp"]["path"],
        )
        self.assertEqual("env", paths["records_artifacts"]["source"])
        self.assertEqual("ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR", paths["records_artifacts"]["source_detail"])
        self.assertNotIn("plan", {entry["source"] for entry in data["paths"]})
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "state.sqlite").exists())
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "records" / "artifacts").exists())
        self.assertFalse((root / "isomer-content" / "topic-ws" / "default" / "custom-artifacts").exists())

        status, output = self.run_cli(
            ["project", "paths", "preview", "--topic", "default", "--json"],
            cwd=root,
            env={"ISOMER_TOPIC_WORKSPACE_ARTIFACTS_DIR": "../outside"},
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO005", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        status, output = self.run_cli(
            ["project", "paths", "preview", "--topic", "default", "--json"],
            cwd=root,
            env={
                "ISOMER_AGENT_WORKSPACE_DIR": "isomer-content/topic-ws/default/agents/alice",
                "ISOMER_AGENT_WORKSPACE_RUNTIME_DIR": "isomer-content/topic-ws/default/agents/alice/custom-runtime",
            },
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        paths = {entry["surface"]: entry for entry in data["paths"]}
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "agents" / "alice" / "isomer-managed"),
            paths["agent_isomer_managed"]["path"],
        )
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "agents" / "alice" / "tmp"),
            paths["agent_tmp"]["path"],
        )
        self.assertEqual("agent.tmp", paths["agent_tmp"]["semantic_label"])
        self.assertEqual("disposable", paths["agent_tmp"]["durability"])
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "agents" / "alice" / "isomer-managed" / "agent-owned"),
            paths["agent_owned"]["path"],
        )
        self.assertEqual("env", paths["agent_runtime"]["source"])
        self.assertEqual("ISOMER_AGENT_WORKSPACE_RUNTIME_DIR", paths["agent_runtime"]["source_detail"])
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "agents" / "alice" / "isomer-managed" / "agent-owned" / "public"),
            paths["agent_public_share"]["path"],
        )
        self.assertEqual(
            str(root / "isomer-content" / "topic-ws" / "default" / "agents" / "alice" / "isomer-managed" / "topic-owned" / "readonly"),
            paths["agent_topic_readonly"]["path"],
        )
        self.assertTrue(
            any("compatibility override for `isomer-managed/agent-owned/*`" in diagnostic["message"] for diagnostic in data["diagnostics"]),
            data["diagnostics"],
        )

    def test_semantic_paths_get_list_and_materialize_default_side_effects(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        manifest_path = topic_workspace / "topic-workspace.toml"
        records_artifacts = topic_workspace / "records" / "artifacts"

        status, output = self.run_cli(["project", "paths", "get", "records_artifacts", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertEqual("topic.records.artifacts", data["path"]["semantic_label"])
        self.assertEqual("records_artifacts", data["path"]["compatibility_surface"])
        self.assertEqual(str(records_artifacts), data["path"]["path"])
        self.assertFalse(manifest_path.exists())
        self.assertFalse(records_artifacts.exists())

        status, output = self.run_cli(["project", "paths", "get", "topic_tmp", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("topic.tmp", data["path"]["semantic_label"])
        self.assertEqual("topic_tmp", data["path"]["compatibility_surface"])
        self.assertEqual("disposable", data["path"]["durability"])
        self.assertEqual("private", data["path"]["sharing"])

        status, output = self.run_cli(["project", "paths", "get", "topic.workspace.summary", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertEqual("topic.workspace.summary", data["path"]["semantic_label"])
        self.assertEqual("topic_workspace_summary", data["path"]["compatibility_surface"])
        self.assertEqual("topic_workspace_summary_file", data["path"]["storage_profile"])
        self.assertEqual("file", data["path"]["path_kind"])
        self.assertEqual(str(topic_workspace / "isomer-topic-workspace-summary.md"), data["path"]["path"])

        status, output = self.run_cli(["project", "paths", "list", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        listed = {item["semantic_label"]: item for item in data["paths"]}
        self.assertTrue(listed["topic.records.artifacts"]["resolved"])
        self.assertTrue(listed["topic.workspace.summary"]["resolved"])
        self.assertEqual("topic_workspace_summary_file", listed["topic.workspace.summary"]["storage_profile"])
        self.assertEqual("file", listed["topic.workspace.summary"]["path_kind"])
        self.assertFalse(listed["agent.private_artifacts"]["resolved"])
        self.assertFalse(manifest_path.exists())
        self.assertFalse(records_artifacts.exists())

        status, output = self.run_cli(["project", "paths", "explain", "topic.workspace.summary", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("topic.workspace.summary", data["explanation"]["semantic_label"])
        self.assertEqual("topic_workspace_summary_file", data["explanation"]["selected"]["storage_profile"])

        status, output = self.run_cli(
            ["project", "paths", "materialize-default", "--topic", "default", "--label", "agent.private_artifacts", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        self.assertIn("ISO061", {diagnostic["code"] for diagnostic in data["diagnostics"]})
        self.assertFalse(manifest_path.exists())

        status, output = self.run_cli(
            ["project", "paths", "materialize-default", "--topic", "default", "--label", "topic.records.artifacts", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertTrue(manifest_path.is_file())
        self.assertTrue(records_artifacts.is_dir())
        self.assertIn('label = "topic.records.artifacts"', manifest_path.read_text(encoding="utf-8"))

        status, output = self.run_cli(
            ["project", "paths", "materialize-default", "--topic", "default", "--label", "topic.workspace.summary", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertIn(str(topic_workspace), data["materialization"]["created_paths"])
        self.assertFalse((topic_workspace / "isomer-topic-workspace-summary.md").exists())
        self.assertIn('label = "topic.workspace.summary"', manifest_path.read_text(encoding="utf-8"))

        status, output = self.run_cli(
            ["project", "paths", "materialize-default", "--topic", "default", "--label", "topic.tmp", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertTrue((topic_workspace / "tmp").is_dir())
        self.assertFalse((topic_workspace / "tmp" / ".gitkeep").exists())
        self.assertIn("tmp/\n", (topic_workspace / ".gitignore").read_text(encoding="utf-8"))

        status, output = self.run_cli(
            ["project", "paths", "materialize-default", "--topic", "default", "--agent", "alice", "--label", "agent.private_artifacts", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertTrue((topic_workspace / "agents" / "alice" / "isomer-managed" / "agent-owned" / "artifacts").is_dir())
        self.assertIn('label = "agent.private_artifacts"', manifest_path.read_text(encoding="utf-8"))

        status, output = self.run_cli(
            ["project", "paths", "materialize-default", "--topic", "default", "--agent", "alice", "--label", "agent.output_root", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        agent_output_root = topic_workspace / "agents" / "alice" / "isomer-managed" / "worker-output" / "agents" / "alice"
        self.assertTrue(agent_output_root.is_dir())
        self.assertFalse((agent_output_root / ".gitkeep").exists())
        self.assertIn('label = "agent.output_root"', manifest_path.read_text(encoding="utf-8"))

        status, output = self.run_cli(
            [
                "project",
                "paths",
                "materialize-default",
                "--topic",
                "default",
                "--topic-actor",
                "operator",
                "--label",
                "topic.actors.output_root",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        actor_output_root = topic_workspace / "actors" / "operator" / "isomer-managed" / "worker-output" / "topic-actors" / "operator"
        self.assertTrue(actor_output_root.is_dir())
        self.assertFalse((actor_output_root / ".gitkeep").exists())
        self.assertIn('label = "topic.actors.output_root"', manifest_path.read_text(encoding="utf-8"))

        status, output = self.run_cli(
            ["project", "paths", "materialize-default", "--topic", "default", "--agent", "alice", "--label", "agent.tmp", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertTrue((topic_workspace / "agents" / "alice" / "tmp").is_dir())
        self.assertIn("tmp/\n", (topic_workspace / "repos" / "topic-main" / ".gitignore").read_text(encoding="utf-8"))

    def test_outputs_policy_reports_root_tracking_authority_and_commit_preference(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        write(
            topic_workspace / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [agent_output_defaults]
            output_root = "isomer-managed/worker-output/agents/{agent_name}"
            commit_after_operation = false

            [[agent_output_overrides]]
            agent_name = "alice"
            output_root = "plain-output/{agent_name}"
            commit_after_operation = true

            [[topic_actors]]
            topic_actor_name = "operator"
            actor_kind = "operator"
            runtime_kind = "codex"
            role_kind = "operator"
            controller_kind = "project_operator_session"
            output_root = "plain-output/topic-actors/operator"
            commit_after_operation = false
            status = "ready"
            """,
        )

        status, output = self.run_cli(["project", "outputs", "policy", "--topic", "default", "--agent", "alice", "--json"], cwd=root)
        data = json.loads(output)

        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        policy = data["output_policy"]
        self.assertEqual("agent", policy["worker_kind"])
        self.assertEqual("alice", policy["worker_name"])
        self.assertEqual(str(topic_workspace / "agents" / "alice" / "plain-output" / "alice"), policy["absolute_root"])
        self.assertEqual("plain-output/alice", policy["worker_relative_root"])
        self.assertEqual("sets/{timestamp}-{operation}-{shortid}", policy["operation_set_pattern"])
        self.assertTrue(policy["commit_after_operation"])
        self.assertEqual(".gitignore and Git status", policy["tracking_authority"])
        self.assertIn(".gitignore and Git status", policy["tracking_note"])

        status, output = self.run_cli(["project", "outputs", "policy", "--topic", "default", "--topic-actor", "operator", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        actor_policy = data["output_policy"]
        self.assertEqual("topic_actor", actor_policy["worker_kind"])
        self.assertEqual("operator", actor_policy["worker_name"])
        self.assertEqual(str(topic_workspace / "actors" / "operator" / "plain-output" / "topic-actors" / "operator"), actor_policy["absolute_root"])
        self.assertEqual("plain-output/topic-actors/operator", actor_policy["worker_relative_root"])
        self.assertFalse(actor_policy["commit_after_operation"])

    def test_semantic_path_binding_lifecycle_and_custom_env_overrides(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        manifest_path = topic_workspace / "topic-workspace.toml"

        status, output = self.run_cli(["project", "paths", "default", "topic.repos.main", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO013", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        status, output = self.run_cli(["project", "paths", "default", "topic.repos.main", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(str(topic_workspace / "repos" / "topic-main"), data["path"]["path"])
        self.assertEqual("topic_repo", data["path"]["storage_profile"])

        status, output = self.run_cli(
            ["project", "paths", "get", "custom.datasets.raw", "--json"],
            cwd=topic_workspace,
            env={"ISOMER_PATH__CUSTOM__DATASETS__RAW": "override/raw"},
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO061", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        status, output = self.run_cli(
            [
                "project",
                "paths",
                "register",
                "custom.datasets.raw",
                "--path",
                "data/raw",
                "--storage-profile",
                "topic_records_dir",
                "--create",
                "--json",
            ],
            cwd=topic_workspace,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertTrue((topic_workspace / "data" / "raw").is_dir())
        manifest_text = manifest_path.read_text(encoding="utf-8")
        self.assertIn('label = "custom.datasets.raw"', manifest_text)
        self.assertIn('storage_profile = "topic_records_dir"', manifest_text)

        status, output = self.run_cli(["project", "paths", "list", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        listed = {item["semantic_label"]: item for item in data["paths"]}
        self.assertEqual(str(topic_workspace / "data" / "raw"), listed["custom.datasets.raw"]["path"])
        self.assertEqual("topic_records_dir", listed["custom.datasets.raw"]["storage_profile"])

        status, output = self.run_cli(
            ["project", "paths", "get", "custom.datasets.raw", "--json"],
            cwd=topic_workspace,
            env={"ISOMER_PATH__CUSTOM__DATASETS__RAW": "override/raw"},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("env", data["path"]["source"])
        self.assertEqual("ISOMER_PATH__CUSTOM__DATASETS__RAW", data["path"]["source_detail"])
        self.assertEqual(str(root / "override" / "raw"), data["path"]["path"])

        status, output = self.run_cli(
            ["project", "paths", "update", "custom.datasets.raw", "--path", "data/raw-v2", "--create", "--json"],
            cwd=topic_workspace,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue((topic_workspace / "data" / "raw-v2").is_dir())
        self.assertTrue((topic_workspace / "data" / "raw").is_dir())

        status, output = self.run_cli(["project", "paths", "materialize", "custom.datasets.raw", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertIn(str(topic_workspace / "data" / "raw-v2"), data["materialization"]["created_paths"])

        status, output = self.run_cli(["project", "paths", "explain", "custom.datasets.raw", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("custom.datasets.raw", data["explanation"]["semantic_label"])
        self.assertEqual("configured", data["explanation"]["selected_mode"])

        status, output = self.run_cli(["project", "paths", "unregister", "custom.datasets.raw", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue((topic_workspace / "data" / "raw-v2").is_dir())
        status, output = self.run_cli(["project", "paths", "get", "custom.datasets.raw", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(1, status)

        status, output = self.run_cli(
            [
                "project",
                "paths",
                "register",
                "topic.repos.main",
                "--path",
                "source/main",
                "--storage-profile",
                "topic_repo",
                "--create",
                "--json",
            ],
            cwd=topic_workspace,
        )
        self.assertEqual(0, status, output)
        status, output = self.run_cli(["project", "paths", "get", "topic.repos.main.tracked.artifacts", "--configured", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(str(topic_workspace / "source" / "main" / "isomer-managed" / "tracked" / "artifacts"), data["path"]["path"])
        status, output = self.run_cli(["project", "paths", "get", "topic.repos.main.projections.readonly", "--configured", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(str(topic_workspace / "source" / "main" / "isomer-managed" / "topic-owned" / "readonly" / "extern"), data["path"]["path"])
        self.assertEqual("topic_repo_readonly_projection_dir", data["path"]["storage_profile"])
        status, output = self.run_cli(["project", "paths", "explain", "topic.repos.main.projections.manifest", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("topic.repos.main.projections.manifest", data["explanation"]["semantic_label"])
        self.assertEqual("configured", data["explanation"]["selected_mode"])
        self.assertEqual("topic_repo_tracked_file", data["explanation"]["selected"]["storage_profile"])
        status, output = self.run_cli(["project", "paths", "reset", "topic.repos.main", "--json"], cwd=topic_workspace)
        self.assertEqual(0, status, output)
        status, output = self.run_cli(["project", "paths", "get", "topic.repos.main", "--configured", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(str(topic_workspace / "repos" / "topic-main"), data["path"]["path"])
        self.assertTrue((topic_workspace / "source" / "main").is_dir())

        status, output = self.run_cli(["project", "repos", "create", "main", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(1, status, output)
        self.assertFalse((topic_workspace / "repos" / "main").exists())
        self.assertTrue(any(diagnostic["field"] == "topic.repos.main" for diagnostic in data["diagnostics"]))

        status, output = self.run_cli(["project", "repos", "create", "inner_group.some_repo_name", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue((topic_workspace / "repos" / "extern" / "inner_group" / "some_repo_name").is_dir())
        status, output = self.run_cli(["project", "paths", "get", "topic.repos.inner_group.some_repo_name", "--json"], cwd=topic_workspace)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("topic_repo", data["path"]["storage_profile"])
        self.assertEqual(str(topic_workspace / "repos" / "extern" / "inner_group" / "some_repo_name"), data["path"]["path"])

    def test_topic_actor_crud_materialization_and_path_resolution(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        topic_main = self.prepare_topic_main_repo(root)

        status, output = self.run_cli(["project", "runtime", "init", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue((topic_workspace / "actors").is_dir())
        surfaces = {record["surface"] for record in data["runtime"]["path_plans"]}
        self.assertIn("actors", surfaces)

        status, output = self.run_cli(
            [
                "project",
                "topic-actors",
                "register",
                "operator",
                "--topic",
                "default",
                "--runtime-kind",
                "codex",
                "--materialize",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        actor = data["topic_actor"]
        self.assertEqual("operator", actor["topic_actor_name"])
        self.assertEqual("per-topic-actor/operator/main", actor["branch"])
        self.assertEqual("git-worktree", data["materialization"]["worktree_mode"])
        self.assertEqual("ready", data["materialization"]["worktree_status"]["status"])
        self.assertEqual(str(topic_main.resolve()), data["materialization"]["worktree_status"]["source_repo_path"])
        self.assertTrue((topic_workspace / "actors" / "operator").is_dir())
        self.assertTrue((topic_workspace / "actors" / "operator" / ".git").is_file())
        self.assertTrue((topic_workspace / "actors" / "operator" / "tmp").is_dir())
        self.assertIn("tmp/\n", (topic_workspace / "actors" / "operator" / ".gitignore").read_text(encoding="utf-8"))

        status, output = self.run_cli(["project", "topic-actors", "materialize", "operator", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("ready", data["materialization"]["worktree_status"]["status"])
        self.assertNotIn(str((topic_workspace / "actors" / "operator").resolve()), data["materialization"]["created_paths"])

        status, output = self.run_cli(
            ["project", "paths", "get", "topic.actors.workspace", "--topic", "default", "--topic-actor", "operator", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(str(topic_workspace / "actors" / "operator"), data["path"]["path"])
        self.assertEqual("operator", data["path"]["topic_actor_name"])
        self.assertEqual("topic_actor:operator", data["path"]["scope_ref"])

        status, output = self.run_cli(["project", "topic-actors", "diagnose", "--topic", "default", "--topic-actor", "operator", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        labels = {item["semantic_label"] for item in data["actor_paths"]}
        self.assertIn("topic.actors.workspace", labels)
        self.assertIn("topic.actors.private_artifacts", labels)
        self.assertEqual("ready", data["worktree_status_by_actor"]["operator"]["status"])
        self.assertEqual("per-topic-actor/operator/main", data["worktree_status_by_actor"]["operator"]["expected_branch"])

        with sqlite3.connect(topic_workspace / "state.sqlite") as connection:
            actor_records = connection.execute(
                "SELECT COUNT(*) FROM lifecycle_records WHERE transition_metadata_json LIKE ?",
                ('%"topic_actor_name":"operator"%',),
            ).fetchone()[0]
            actor_plan = connection.execute(
                "SELECT path FROM path_plans WHERE semantic_label = ? AND scope_ref = ?",
                ("topic.actors.workspace", "topic_actor:operator"),
            ).fetchone()
        self.assertGreaterEqual(actor_records, 1)
        self.assertIsNotNone(actor_plan)

    def test_topic_actor_materialization_blocks_existing_nonmatching_path(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        self.prepare_topic_main_repo(root)
        actor_workspace = topic_workspace / "actors" / "operator"
        write(actor_workspace / "local.txt", "keep me\n")

        status, output = self.run_cli(["project", "topic-actors", "register", "operator", "--topic", "default", "--json"], cwd=root)
        self.assertEqual(0, status, output)

        status, output = self.run_cli(["project", "topic-actors", "materialize", "operator", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["ok"])
        self.assertIsNone(data["materialization"])
        self.assertEqual("keep me\n", (actor_workspace / "local.txt").read_text(encoding="utf-8"))
        self.assertFalse((actor_workspace / ".git").exists())
        self.assertTrue(any("not a worktree of topic.repos.main" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        status, output = self.run_cli(["project", "topic-actors", "diagnose", "--topic", "default", "--topic-actor", "operator", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual("blocked_existing_nonmatching_path", data["worktree_status_by_actor"]["operator"]["status"])

    def test_topic_actor_materialization_blocks_duplicate_branch_checkout(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        topic_main = self.prepare_topic_main_repo(root)
        duplicate_path = topic_workspace / "actors" / "operator-other"
        subprocess.run(
            ["git", "-C", str(topic_main), "worktree", "add", "-b", "per-topic-actor/operator/main", str(duplicate_path)],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        status, output = self.run_cli(["project", "topic-actors", "register", "operator", "--topic", "default", "--json"], cwd=root)
        self.assertEqual(0, status, output)

        status, output = self.run_cli(["project", "topic-actors", "materialize", "operator", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIsNone(data["materialization"])
        self.assertTrue(any("already checked out in another topic-main worktree" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        status, output = self.run_cli(["project", "topic-actors", "diagnose", "--topic", "default", "--topic-actor", "operator", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        worktree_status = data["worktree_status_by_actor"]["operator"]
        self.assertEqual("blocked_duplicate_branch_checkout", worktree_status["status"])
        self.assertEqual(str(duplicate_path.resolve()), worktree_status["duplicate_branch_path"])

    def test_topic_actor_materialization_requires_git_topic_main(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)

        status, output = self.run_cli(["project", "topic-actors", "register", "operator", "--topic", "default", "--json"], cwd=root)
        self.assertEqual(0, status, output)

        status, output = self.run_cli(["project", "topic-actors", "materialize", "operator", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIsNone(data["materialization"])
        self.assertFalse((topic_workspace / "actors" / "operator").exists())
        self.assertTrue(any("topic.repos.main is missing or is not a Git repository" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

    def test_topic_actor_roster_supports_manual_and_houmao_workers_without_team_membership(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        self.prepare_topic_main_repo(root)

        status, output = self.run_cli(["project", "runtime", "init", "--topic", "default", "--json"], cwd=root)
        self.assertEqual(0, status, output)

        actor_commands = (
            [
                "project",
                "topic-actors",
                "register",
                "operator",
                "--topic",
                "default",
                "--actor-kind",
                "operator",
                "--runtime-kind",
                "codex",
                "--role-kind",
                "operator",
                "--controller-kind",
                "project_operator_session",
                "--materialize",
                "--json",
            ],
            [
                "project",
                "topic-actors",
                "register",
                "claude-scout",
                "--topic",
                "default",
                "--actor-kind",
                "manual_worker",
                "--runtime-kind",
                "claude_code",
                "--role-kind",
                "scout",
                "--controller-kind",
                "human_user",
                "--materialize",
                "--json",
            ],
            [
                "project",
                "topic-actors",
                "register",
                "houmao-exp",
                "--topic",
                "default",
                "--actor-kind",
                "houmao_backed",
                "--runtime-kind",
                "houmao",
                "--role-kind",
                "experimenter",
                "--controller-kind",
                "houmao",
                "--adapter-ref",
                "houmao:manual",
                "--materialize",
                "--json",
            ],
        )
        for command in actor_commands:
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

        status, output = self.run_cli(["project", "topic-actors", "list", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        actors = {actor["topic_actor_name"]: actor for actor in data["topic_actors"]}
        self.assertEqual({"operator", "claude-scout", "houmao-exp"}, set(actors))
        self.assertEqual("manual_worker", actors["claude-scout"]["actor_kind"])
        self.assertEqual("houmao_backed", actors["houmao-exp"]["actor_kind"])
        self.assertEqual("houmao", actors["houmao-exp"]["runtime_kind"])
        for actor_name in actors:
            self.assertTrue((topic_workspace / "actors" / actor_name).is_dir())

        self.assertFalse((topic_workspace / "team-profile").exists())
        self.assertFalse((topic_workspace / ".houmao").exists())
        with sqlite3.connect(topic_workspace / "state.sqlite") as connection:
            agent_team_count = connection.execute("SELECT COUNT(*) FROM agent_team_instances").fetchone()[0]
            agent_instance_count = connection.execute("SELECT COUNT(*) FROM agent_instances").fetchone()[0]
            actor_records = connection.execute(
                "SELECT COUNT(*) FROM lifecycle_records WHERE transition_metadata_json LIKE ?",
                ('%"operation":"topic_actor_register"%',),
            ).fetchone()[0]
        self.assertEqual(0, agent_team_count)
        self.assertEqual(0, agent_instance_count)
        self.assertGreaterEqual(actor_records, 3)

    def test_topic_workspace_manifest_custom_bindings_and_diagnostics(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        manifest_path = topic_workspace / "topic-workspace.toml"
        write(
            manifest_path,
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"
            layout_profile = "isomer-default.v1"

            [[bindings]]
            label = "topic.repos.main"
            path = "custom-main"
            storage_profile = "topic_repo"
            status = "active"

            [[bindings]]
            label = "topic.repos.main.tmp"
            path = "custom-main/local-tmp"
            storage_profile = "topic_repo_disposable_dir"
            status = "active"

            [[bindings]]
            label = "agent.workspace"
            path = "worktrees/{agent_name}"
            storage_profile = "agent_worktree"
            status = "active"

            [[bindings]]
            label = "agent.tmp"
            path = "worktrees/{agent_name}/local-tmp"
            storage_profile = "agent_disposable_dir"
            status = "active"
            """,
        )

        status, output = self.run_cli(["project", "paths", "get", "topic.repos.main", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("topic_workspace_manifest", data["path"]["source"])
        self.assertEqual(str(topic_workspace / "custom-main"), data["path"]["path"])

        status, output = self.run_cli(["project", "paths", "get", "topic.repos.main.tmp", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("topic_workspace_manifest", data["path"]["source"])
        self.assertEqual(str(topic_workspace / "custom-main" / "local-tmp"), data["path"]["path"])
        self.assertEqual("topic_main_tmp", data["path"]["compatibility_surface"])

        status, output = self.run_cli(["project", "paths", "get", "topic.repos.main.projections.writable", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("default_profile", data["path"]["source"])
        self.assertEqual(str(topic_workspace / "custom-main" / "isomer-managed" / "topic-owned" / "writable" / "extern"), data["path"]["path"])
        self.assertEqual("topic_repo_writable_projection_dir", data["path"]["storage_profile"])

        status, output = self.run_cli(
            ["project", "paths", "get", "agent.private_artifacts", "--topic", "default", "--agent", "alice", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("default_profile", data["path"]["source"])
        self.assertEqual(
            str(topic_workspace / "worktrees" / "alice" / "isomer-managed" / "agent-owned" / "artifacts"),
            data["path"]["path"],
        )
        self.assertEqual("alice", data["path"]["agent_name"])

        status, output = self.run_cli(
            ["project", "paths", "get", "agent.tmp", "--topic", "default", "--agent", "alice", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("topic_workspace_manifest", data["path"]["source"])
        self.assertEqual(str(topic_workspace / "worktrees" / "alice" / "local-tmp"), data["path"]["path"])
        self.assertEqual("agent_tmp:alice", data["path"]["compatibility_surface"])

        write(
            manifest_path,
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.repos.main"
            path = "custom-main"
            storage_profile = "topic_repo"
            status = "active"

            [[bindings]]
            label = "topic.repos.main"
            path = "another-main"
            storage_profile = "topic_repo"
            status = "active"
            """,
        )
        status, output = self.run_cli(["project", "paths", "get", "topic.repos.main", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO060", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        write(
            manifest_path,
            f"""
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.repos.main"
            path = "{(root.parent / 'outside').as_posix()}"
            storage_profile = "topic_repo"
            status = "active"
            """,
        )
        status, output = self.run_cli(["project", "paths", "get", "topic.repos.main", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO005", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        write(
            manifest_path,
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.repos.main.unexpected"
            path = "repos/topic-main/unexpected"
            storage_profile = "topic_repo"
            status = "active"
            """,
        )
        status, output = self.run_cli(["project", "paths", "get", "topic.repos.main.unexpected", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("Unknown or reserved Topic Main Development Repository semantic label" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

    def test_topic_main_guidance_render_is_topic_independent(self) -> None:
        root = self.make_root()

        status, output = self.run_cli(["project", "topic-main-guidance", "render", "--json"], cwd=root)
        data = json.loads(output)

        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertEqual("v1", data["guidance"]["version"])
        self.assertEqual(
            "assets/topic_main_guidance/isomer-labs-topic-main-guidance.v1.md.j2",
            data["guidance"]["template_resource"],
        )
        rendered = data["rendered"]
        self.assertIn("<!-- BEGIN isomer-labs-topic-main-guidance v1 -->", rendered)
        self.assertIn("```isomer-labs-topic-main-guidance", rendered)
        self.assertIn("pixi run --manifest-path <manifest_path> --environment <pixi_environment> python ...", rendered)
        self.assertLess(
            rendered.index("isomer-cli --print-json project self show"),
            rendered.index("isomer-cli --print-json project self identity"),
        )
        self.assertLess(
            rendered.index("isomer-cli --print-json project self show"),
            rendered.index("isomer-cli --print-json project context show"),
        )
        self.assertIn("isomer-cli --print-json project self pixi", rendered)
        self.assertIn("isomer-cli --print-json project self env", rendered)
        self.assertIn("isomer-cli --print-json project self paths <semantic-label>", rendered)
        self.assertIn("isomer-cli --print-json project paths get <semantic-label>", rendered)
        self.assertIn("isomer-cli --print-json project paths explain <semantic-label>", rendered)
        self.assertIn("topic.repos.main", rendered)
        self.assertNotIn("project self --all", rendered)
        self.assertNotIn("project self show --all", rendered)
        self.assertNotIn(str(root), rendered)

    def test_topic_main_guidance_inspect_and_ensure_are_idempotent(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_main = self.default_topic_workspace(root) / "repos" / "topic-main"
        topic_main.mkdir(parents=True)
        subprocess.run(["git", "init"], cwd=topic_main, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        status, output = self.run_cli(
            ["project", "topic-main-guidance", "inspect", "--topic", "default", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertEqual(["missing", "missing"], [target["status"] for target in data["targets"]])

        status, output = self.run_cli(
            ["project", "topic-main-guidance", "ensure", "--topic", "default", "--yes", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(data["mutated"])
        self.assertEqual(["AGENTS.md", "CLAUDE.md"], data["changed_files"])
        self.assertEqual(["created", "created"], [target["action"] for target in data["targets"]])
        self.assertTrue((topic_main / "AGENTS.md").is_file())
        self.assertTrue((topic_main / "CLAUDE.md").is_file())

        status, output = self.run_cli(
            ["project", "topic-main-guidance", "ensure", "--topic", "default", "--yes", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertEqual([], data["changed_files"])
        self.assertEqual(["current", "current"], [target["status"] for target in data["targets"]])
        self.assertEqual(["unchanged", "unchanged"], [target["action"] for target in data["targets"]])

    def test_topic_main_guidance_ensure_requires_confirmation(self) -> None:
        root = self.make_root()

        status, output = self.run_cli(["project", "topic-main-guidance", "ensure", "--json"], cwd=root)
        data = json.loads(output)

        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        self.assertTrue(any(diagnostic["field"] == "--yes" for diagnostic in data["diagnostics"]))

    def test_topic_main_guidance_ensure_blocks_unsafe_repo(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_main = self.default_topic_workspace(root) / "repos" / "topic-main"
        topic_main.mkdir(parents=True)

        status, output = self.run_cli(
            ["project", "topic-main-guidance", "ensure", "--topic", "default", "--yes", "--json"],
            cwd=root,
        )
        data = json.loads(output)

        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        self.assertEqual([], data["changed_files"])
        self.assertFalse((topic_main / "AGENTS.md").exists())
        self.assertTrue(any(diagnostic["field"] == "topic.repos.main" for diagnostic in data["diagnostics"]))

    def test_cwd_derived_agent_context_and_selector_conflicts(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        alice_cwd = topic_workspace / "agents" / "alice" / "nested"
        alice_cwd.mkdir(parents=True)

        status, output = self.run_cli(["project", "paths", "get", "agent.private_artifacts", "--json"], cwd=alice_cwd)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("alice", data["path"]["agent_name"])
        self.assertEqual("cwd", data["path"]["agent_context_source"])
        self.assertEqual(
            str(topic_workspace / "agents" / "alice" / "isomer-managed" / "agent-owned" / "artifacts"),
            data["path"]["path"],
        )

        status, output = self.run_cli(["project", "context", "show", "--json"], cwd=alice_cwd)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("alice", data["effective_agent_context"]["agent_name"])
        self.assertEqual("cwd", data["effective_agent_context"]["source"])

        topic_main_cwd = topic_workspace / "repos" / "topic-main" / "src"
        topic_main_cwd.mkdir(parents=True)
        status, output = self.run_cli(["project", "paths", "get", "agent.private_artifacts", "--json"], cwd=topic_main_cwd)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO061", {diagnostic["code"] for diagnostic in data["diagnostics"]})

        bob_cwd = topic_workspace / "agents" / "bob"
        bob_cwd.mkdir(parents=True)
        status, output = self.run_cli(
            ["project", "paths", "get", "agent.workspace", "--json"],
            cwd=bob_cwd,
            env={"ISOMER_AGENT_NAME": "alice"},
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("conflicts" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

        status, output = self.run_cli(["project", "paths", "get", "agent.workspace", "--agent", "alice", "--json"], cwd=bob_cwd)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("alice", data["path"]["agent_name"])
        self.assertEqual("explicit selector", data["path"]["agent_context_source"])

        write(
            topic_workspace / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "agent.workspace"
            path = "worktrees/{agent_name}/nested/{agent_name}"
            storage_profile = "agent_worktree"
            status = "active"
            """,
        )
        carol_cwd = topic_workspace / "agents" / "carol"
        carol_cwd.mkdir(parents=True)
        status, output = self.run_cli(["project", "paths", "get", "agent.workspace", "--json"], cwd=carol_cwd)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(
            any("exactly one {agent_name}" in diagnostic["message"] for diagnostic in data["diagnostics"]),
            data["diagnostics"],
        )

        two_topic_root = self.make_root()
        self.make_two_topic_project(two_topic_root)
        beta_cwd = two_topic_root / "topic-workspaces" / "beta" / "agents" / "bob"
        beta_cwd.mkdir(parents=True)
        status, output = self.run_cli(["project", "paths", "get", "agent.workspace", "--topic", "alpha", "--json"], cwd=beta_cwd)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(
            any("another Research Topic" in diagnostic["message"] for diagnostic in data["diagnostics"]),
            data["diagnostics"],
        )

    def test_self_show_from_topic_main_cwd_is_small(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_main_cwd = self.default_topic_workspace(root) / "repos" / "topic-main" / "src"
        topic_main_cwd.mkdir(parents=True)

        status, output = self.run_cli(
            ["project", "self", "show", "--json"],
            cwd=topic_main_cwd,
            env={"ISOMER_AGENT_NAME": "alice"},
        )

        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["mutated"])
        self.assertEqual("default", data["summary"]["topic"]["research_topic_id"])
        self.assertEqual("alice", data["summary"]["agent"]["agent_name"])
        self.assertIn("available_queries", data)
        for omitted in ("identity", "environment", "semantic_paths", "pixi", "queries"):
            self.assertNotIn(omitted, data)

    def test_self_identity_reports_agent_topic_actor_missing_and_conflicts(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        topic_main_cwd = topic_workspace / "repos" / "topic-main" / "src"
        topic_main_cwd.mkdir(parents=True)
        write(
            topic_workspace / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[topic_actors]]
            topic_actor_name = "operator"
            runtime_kind = "codex"
            """,
        )

        status, output = self.run_cli(
            ["project", "self", "identity", "--topic-actor", "operator", "--json"],
            cwd=topic_main_cwd,
            env={"ISOMER_AGENT_NAME": "alice"},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("default", data["identity"]["context"]["research_topic_id"])
        self.assertEqual("operator", data["identity"]["topic_actor"]["topic_actor_name"])
        self.assertEqual("alice", data["identity"]["agent"]["agent_name"])
        self.assertEqual("environment", data["identity"]["agent"]["source"])
        self.assertNotIn("environment", data)
        self.assertNotIn("pixi", data)

        status, output = self.run_cli(["project", "self", "identity", "--json"], cwd=topic_main_cwd)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertFalse(data["identity"]["agent"]["resolved"])
        self.assertIn("--agent", data["agent_resolution_help"])

        bob_cwd = topic_workspace / "agents" / "bob"
        bob_cwd.mkdir(parents=True)
        status, output = self.run_cli(
            ["project", "self", "identity", "--json"],
            cwd=bob_cwd,
            env={"ISOMER_AGENT_NAME": "alice"},
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertTrue(any("conflicts" in diagnostic["message"] for diagnostic in data["diagnostics"]), data["diagnostics"])

    def test_self_env_reports_allowlist_and_redacts_values(self) -> None:
        root = self.make_root()
        self.init_project(root)

        env = {
            "ISOMER_AGENT_NAME": "alice",
            "ISOMER_PATH__CUSTOM_DATA": str(root / "data"),
            "ISOMER_API_KEY": "super-secret",
            "UNRELATED_VALUE": "visible-nowhere",
        }
        status, output = self.run_cli(["project", "self", "env", "--json"], cwd=root, env=env)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        names = {entry["name"]: entry for entry in data["environment"]["recognized"]}
        self.assertTrue(names["ISOMER_AGENT_NAME"]["present"])
        self.assertNotIn("value", names["ISOMER_AGENT_NAME"])
        self.assertIn("ISOMER_PATH__CUSTOM_DATA", names)
        self.assertIn("ISOMER_API_KEY", data["environment"]["omitted_secret_like"])
        self.assertNotIn("super-secret", output)
        self.assertNotIn("visible-nowhere", output)

        status, output = self.run_cli(["project", "self", "env", "--values", "--json"], cwd=root, env=env)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        names = {entry["name"]: entry for entry in data["environment"]["recognized"]}
        self.assertEqual("alice", names["ISOMER_AGENT_NAME"]["value"])
        self.assertNotIn("super-secret", output)

    def test_self_paths_requires_labels_and_resolves_requested_only(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_main_cwd = self.default_topic_workspace(root) / "repos" / "topic-main" / "src"
        topic_main_cwd.mkdir(parents=True)

        status, output = self.run_cli(["project", "self", "paths", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual([], data["semantic_paths"])
        self.assertTrue(any(diagnostic["field"] == "semantic_label" for diagnostic in data["diagnostics"]))

        status, output = self.run_cli(
            ["project", "self", "paths", "topic.repos.main", "agent.workspace", "--json"],
            cwd=topic_main_cwd,
            env={"ISOMER_AGENT_NAME": "alice"},
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["topic.repos.main", "agent.workspace"], [entry["semantic_label"] for entry in data["semantic_paths"]])
        self.assertNotIn("paths", data)
        self.assertNotIn("queries", data)

    def test_self_pixi_project_standalone_ambiguous_and_missing(self) -> None:
        root = self.make_root()
        self.init_project(root)
        self.add_project_pixi_manifest(root, environments=("default",), lockfile=True)
        self.add_topic_pixi_binding(root, "default", "default")

        status, output = self.run_cli(["project", "self", "pixi", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("project", data["pixi"]["selected"]["kind"])
        self.assertEqual("default", data["pixi"]["selected"]["pixi_environment"])
        self.assertIn("pixi run --manifest-path", data["pixi"]["python_command"])

        standalone_root = self.make_root()
        self.init_project(standalone_root)
        self.append_manifest(
            standalone_root,
            """
            [[topic_standalone_pixi_bindings]]
            research_topic_id = "default"
            manifest_path_or_dir = "isomer-content/topic-ws/default/pixi.toml"
            pixi_environment = "default"
            """,
        )
        write(
            self.default_topic_workspace(standalone_root) / "pixi.toml",
            """
            [workspace]
            channels = ["conda-forge"]
            platforms = ["linux-64"]
            """,
        )
        which_patch, run_patch = self.patch_pixi()
        with which_patch, run_patch:
            status, output = self.run_cli(["project", "self", "pixi", "--json"], cwd=standalone_root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("standalone", data["pixi"]["selected"]["kind"])

        ambiguous_root = self.make_root()
        self.init_project(ambiguous_root)
        self.add_project_pixi_manifest(ambiguous_root, environments=("main", "analysis"), lockfile=True)
        self.add_topic_pixi_binding(ambiguous_root, "default", "main")
        self.add_topic_pixi_binding(ambiguous_root, "default", "analysis")
        status, output = self.run_cli(["project", "self", "pixi", "--json"], cwd=ambiguous_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertEqual(2, len(data["pixi"]["candidates"]))
        self.assertIsNone(data["pixi"]["python_command"])

        missing_root = self.make_root()
        self.init_project(missing_root)
        status, output = self.run_cli(["project", "self", "pixi", "--json"], cwd=missing_root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIsNone(data["pixi"]["selected"])
        self.assertTrue(any(diagnostic["code"] == "ISO032" for diagnostic in data["diagnostics"]))

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

        status, output = self.run_cli(["project", "paths", "preview", "--topic", "alpha", "--json"], cwd=root)

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
        for directory in (
            "repos",
            "repos/topic-main",
            "repos/topic-main/isomer-managed",
            "agents",
            "records",
            "records/artifacts",
            "records/tasks",
            "records/runs",
            "records/views",
            "records/logs",
            "runtime",
        ):
            self.assertTrue((runtime_root / directory).is_dir())
        surfaces = {record["surface"] for record in data["runtime"]["path_plans"]}
        self.assertTrue(
            {
                "workspace_runtime_db",
                "repos",
                "topic_main_repo",
                "topic_main_isomer_managed",
                "agents",
                "records",
                "records_artifacts",
                "records_tasks",
                "records_runs",
                "records_views",
                "records_logs",
                "runtime",
            }
            <= surfaces
        )
        plans = {record["semantic_label"]: record for record in data["runtime"]["path_plans"] if "semantic_label" in record}
        self.assertEqual("topic_repo", plans["topic.repos.main"]["storage_profile"])
        self.assertEqual("repository", plans["topic.repos.main"]["storage_profile_traits"]["kind"])
        self.assertEqual("topic_records_dir", plans["topic.records.artifacts"]["storage_profile"])

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

    def test_runtime_path_plans_include_semantics_and_manifest_drift_is_diagnostic(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)

        status, output = self.run_cli(["project", "runtime", "init", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        plans = {plan["semantic_label"]: plan for plan in data["runtime"]["path_plans"] if "semantic_label" in plan}
        self.assertEqual("default_profile", plans["topic.runtime.db"]["source"])
        self.assertEqual("topic_workspace:default", plans["topic.records.artifacts"]["scope_ref"])
        self.assertEqual("records_artifacts", plans["topic.records.artifacts"]["compatibility_surface"])
        original_artifact_path = plans["topic.records.artifacts"]["path"]

        status, output = self.run_cli(["project", "runtime", "inspect", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        inspected_plans = {plan["semantic_label"]: plan for plan in data["runtime"]["path_plans"] if "semantic_label" in plan}
        self.assertEqual(original_artifact_path, inspected_plans["topic.records.artifacts"]["path"])

        write(
            topic_workspace / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.records.artifacts"
            path = "records/v2-artifacts"
            storage_profile = "topic_records_dir"
            status = "active"
            """,
        )
        status, output = self.run_cli(["project", "runtime", "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(
            any("Stored path plan differs from current Workspace Path Resolution output." == diagnostic["message"] for diagnostic in data["diagnostics"]),
            data["diagnostics"],
        )
        status, output = self.run_cli(["project", "runtime", "inspect", "--json"], cwd=root)
        data = json.loads(output)
        inspected_plans = {plan["semantic_label"]: plan for plan in data["runtime"]["path_plans"] if "semantic_label" in plan}
        self.assertEqual(original_artifact_path, inspected_plans["topic.records.artifacts"]["path"])

    def test_runtime_custom_path_plan_drift_and_missing_binding_are_diagnostics(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        manifest_path = topic_workspace / "topic-workspace.toml"
        write(
            manifest_path,
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "custom.datasets.raw"
            path = "data/raw"
            storage_profile = "topic_records_dir"
            status = "active"
            """,
        )

        status, output = self.run_cli(["project", "runtime", "init", "--json"], cwd=root)
        self.assertEqual(0, status, output)
        raw_path = topic_workspace / "data" / "raw"
        raw_path.mkdir(parents=True, exist_ok=True)
        artifact_path = raw_path / "sample.txt"
        artifact_path.write_text("raw\n", encoding="utf-8")
        loose_path = topic_workspace / "loose.txt"
        loose_path.write_text("loose\n", encoding="utf-8")
        db_path = topic_workspace / "state.sqlite"
        with sqlite3.connect(db_path) as db:
            db.execute(
                """
                INSERT INTO path_plans
                    (
                        id, topic_workspace_id, surface, path, source, source_detail,
                        semantic_label, scope_ref, compatibility_surface, storage_profile,
                        storage_profile_traits_json, created_at
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "path-plan-default-custom-datasets-raw",
                    "default",
                    "custom.datasets.raw",
                    str(raw_path),
                    "topic_workspace_manifest",
                    "topic-workspace.toml",
                    "custom.datasets.raw",
                    "topic_workspace:default",
                    "custom.datasets.raw",
                    "topic_records_dir",
                    json.dumps(
                        {
                            "id": "topic_records_dir",
                            "context": "topic",
                            "kind": "directory",
                            "lifecycle": "durable",
                            "visibility": "topic",
                            "safety_policy": "topic_workspace_local",
                            "owner": "topic",
                            "path_kind": "directory",
                        }
                    ),
                    "2026-01-01T00:00:00Z",
                ),
            )
            db.execute(
                """
                INSERT INTO lifecycle_records
                    (
                        id, record_kind, research_topic_id, topic_workspace_id, status,
                        created_at, updated_at, lifecycle_refs_json, transition_metadata_json,
                        content_path, provenance_refs_json
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "artifact-custom-raw",
                    "artifact",
                    "default",
                    "default",
                    "recorded",
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T00:00:00Z",
                    "{}",
                    "{}",
                    str(artifact_path),
                    "[]",
                ),
            )
            db.execute(
                """
                INSERT INTO lifecycle_records
                    (
                        id, record_kind, research_topic_id, topic_workspace_id, status,
                        created_at, updated_at, lifecycle_refs_json, transition_metadata_json,
                        content_path, provenance_refs_json
                    )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "artifact-loose-path",
                    "artifact",
                    "default",
                    "default",
                    "recorded",
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T00:00:00Z",
                    "{}",
                    "{}",
                    str(loose_path),
                    "[]",
                ),
            )

        status, output = self.run_cli(["project", "runtime", "inspect", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        locators = {locator["record_id"]: locator for locator in data["runtime"]["semantic_file_locators"]}
        self.assertEqual("custom.datasets.raw", locators["artifact-custom-raw"]["semantic_label"])
        self.assertEqual("path-plan-default-custom-datasets-raw", locators["artifact-custom-raw"]["path_plan_id"])
        self.assertEqual("sample.txt", locators["artifact-custom-raw"]["relative_path"])

        status, output = self.run_cli(["project", "runtime", "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(
            any("Project-local file ref has no semantic file locator evidence;" in diagnostic["message"] for diagnostic in data["diagnostics"]),
            data["diagnostics"],
        )

        write(
            manifest_path,
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "custom.datasets.raw"
            path = "data/raw-v2"
            storage_profile = "topic_records_dir"
            status = "active"
            """,
        )
        status, output = self.run_cli(["project", "runtime", "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertTrue(
            any("Stored path plan differs from current Workspace Path Resolution output." == diagnostic["message"] for diagnostic in data["diagnostics"]),
            data["diagnostics"],
        )

        write(
            manifest_path,
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"
            """,
        )
        status, output = self.run_cli(["project", "runtime", "validate", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        messages = {diagnostic["message"] for diagnostic in data["diagnostics"]}
        self.assertIn("Historical path plan remains, but the current semantic binding is missing.", messages)
        inspected_plans = {plan["semantic_label"]: plan for plan in data["runtime"]["path_plans"] if "semantic_label" in plan}
        self.assertEqual(str(raw_path), inspected_plans["custom.datasets.raw"]["path"])
        self.assertEqual("topic_records_dir", inspected_plans["custom.datasets.raw"]["storage_profile"])

    def test_runtime_path_plan_lookup_uses_manifest_runtime_db_binding(self) -> None:
        root = self.make_root()
        self.init_project(root)
        topic_workspace = self.default_topic_workspace(root)
        write(
            topic_workspace / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.runtime.db"
            path = "runtime/custom-state.sqlite"
            storage_profile = "topic_runtime_file"
            status = "active"
            """,
        )

        status, output = self.run_cli(["project", "runtime", "init", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        custom_db = topic_workspace / "runtime" / "custom-state.sqlite"
        self.assertTrue(custom_db.is_file())
        self.assertFalse((topic_workspace / "state.sqlite").exists())
        plans = {plan["semantic_label"]: plan for plan in data["runtime"]["path_plans"] if "semantic_label" in plan}
        self.assertEqual(str(custom_db), plans["topic.runtime.db"]["path"])
        self.assertEqual("topic_workspace_manifest", plans["topic.runtime.db"]["source"])

        status, output = self.run_cli(["project", "runtime", "inspect", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        inspected_plans = {plan["semantic_label"]: plan for plan in data["runtime"]["path_plans"] if "semantic_label" in plan}
        self.assertEqual(str(custom_db), inspected_plans["topic.runtime.db"]["path"])

        status, output = self.run_cli(["project", "paths", "get", "topic.records.artifacts", "--topic", "default", "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("path_plan", data["path"]["source"])

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

    def test_agent_team_instance_creation_uses_manifest_agent_workspace_template(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        self.add_project_pixi_manifest(root, environments=("alpha-main",), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
        write(
            root / "topic-workspaces" / "alpha" / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "alpha"
            topic_workspace_id = "alpha"

            [[bindings]]
            label = "agent.workspace"
            path = "worktrees/{agent_name}"
            storage_profile = "agent_worktree"
            status = "active"
            """,
        )
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
                "ati-alpha-custom-worktrees",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        creation = data["creation"]
        master_workspace = next(workspace for workspace in creation["agent_workspaces"] if workspace["agent_name"] == "deepsci-org-master")
        self.assertTrue(master_workspace["support_root_path"].endswith("topic-workspaces/alpha/worktrees/deepsci-org-master/isomer-managed"))
        master_workspace_plan = next(plan for plan in creation["path_plans"] if plan["surface"] == "agent_workspace:deepsci-org-master")
        self.assertEqual(
            str((root / "topic-workspaces" / "alpha" / "worktrees" / "deepsci-org-master").resolve()),
            master_workspace_plan["path"],
        )
        self.assertEqual("agent.workspace", master_workspace_plan["semantic_label"])
        self.assertIn("semantic_source=topic_workspace_manifest", master_workspace_plan["source_detail"])
        self.assertTrue((root / "topic-workspaces" / "alpha" / "worktrees" / "deepsci-org-master" / "isomer-managed" / "links").is_dir())

        status, output = self.run_cli(
            ["project", "paths", "get", "agent.workspace", "--topic", "alpha", "--agent", "deepsci-org-master", "--json"],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual("path_plan", data["path"]["source"])
        self.assertEqual(master_workspace_plan["path"], data["path"]["path"])

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

            [[team_repositories]]
            id = "isomer-local-teams"
            path = "{repo_root}"
            status = "active"

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
            """.format(repo_root=REPO_ROOT.as_posix()),
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
        agent_workspace_refs: dict[str, str] | None = None,
    ) -> str:
        policy_topic = policy_topic_id or topic_id
        artifact_topic = artifact_topic_id or topic_id
        execution_mode = "automatic" if automatic else "manual"
        automatic_policy = 'automatic_mode_policy_ref = "automatic-mode-policy:test"\n' if automatic else ""
        runtime_line = 'run_status = "done"\n' if runtime_truth else ""
        launch_line = 'launch_ref = "houmao-launch:test"\nhoumao_managed_agent_id = "managed-agent:test"\n' if launch_truth else ""
        secret_line = 'api_key = "SHOULD_NOT_LEAK"\n' if secret_like else ""
        roles = [
            ("deepsci-org-master", ["isomer-deepsci-shared", "isomer-deepsci-decision", "isomer-deepsci-finalize"], ["isomer-deepsci-review"]),
            ("deepsci-org-framer", ["isomer-deepsci-shared", "isomer-deepsci-scout", "isomer-deepsci-baseline"], ["isomer-deepsci-science", "isomer-deepsci-paper-outline"]),
            ("deepsci-org-designer", ["isomer-deepsci-shared", "isomer-deepsci-idea", "isomer-deepsci-optimize"], ["isomer-deepsci-scout"]),
            ("deepsci-org-experimenter", ["isomer-deepsci-shared", "isomer-deepsci-experiment", "isomer-deepsci-science"], ["isomer-deepsci-analysis"]),
            ("deepsci-org-analyzer", ["isomer-deepsci-shared", "isomer-deepsci-analysis", "isomer-deepsci-science"], ["isomer-deepsci-paper-plot", "isomer-deepsci-figure-polish"]),
            ("deepsci-org-publisher", ["isomer-deepsci-shared", "isomer-deepsci-paper-outline", "isomer-deepsci-write", "isomer-deepsci-paper-plot", "isomer-deepsci-figure-polish"], ["isomer-deepsci-nature-data", "isomer-deepsci-nature-figure", "isomer-deepsci-nature-paper2ppt", "isomer-deepsci-nature-polishing"]),
            ("deepsci-org-reviewer", ["isomer-deepsci-shared", "isomer-deepsci-review", "isomer-deepsci-rebuttal", "isomer-deepsci-analysis"], ["isomer-deepsci-scout"]),
        ]
        role_blocks = []
        for role_id, required, optional in roles:
            workspace_ref_line = ""
            agent_name = role_id
            if agent_workspace_refs is not None and role_id in agent_workspace_refs:
                workspace_ref = agent_workspace_refs[role_id]
                agent_name = workspace_ref.rstrip("/").rsplit("/", 1)[-1]
                workspace_ref_line = f'agent_workspace_ref = "{workspace_ref}"\n'
            role_blocks.append(
                f"""
                [[role_bindings]]
                role_id = "{role_id}"
                active = true
                agent_profile_ref = "{profile_id}:{role_id}:agent-profile"
                capability_binding_ref = "{profile_id}:{role_id}:capability-binding"
                skill_binding_projection_ref = "{profile_id}:{role_id}:skill-binding-projection"
                agent_name = "{agent_name}"
                agent_branch = "per-agent/{agent_name}/main"
                {workspace_ref_line}
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
        self.assertEqual([], [template["id"] for template in data["templates"]])

        team_repo_env = {"ISOMER_TEAM_REPOSITORIES": str(REPO_ROOT)}
        status, output = self.run_cli(["project", "team-templates", "list", "--json"], env=team_repo_env)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(["deepsci-mini", "deepsci-org"], [template["id"] for template in data["templates"]])
        self.assertEqual({"team-repository"}, {template["source_kind"] for template in data["templates"]})
        self.assertTrue(all(template["validation_status"] == "valid" for template in data["templates"]))

        status, output = self.run_cli(["project", "team-templates", "inspect", "deepsci-mini", "--json"], env=team_repo_env)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(3, len(data["template"]["roles"]))
        self.assertEqual(
            {"deepsci-mini-lead", "deepsci-mini-scout", "deepsci-mini-synth-reviewer"},
            {role["id"] for role in data["template"]["roles"]},
        )

        status, output = self.run_cli(["project", "team-templates", "inspect", "deepsci-org", "--json"], env=team_repo_env)
        data = json.loads(output)
        self.assertEqual(0, status, output)
        self.assertEqual(7, len(data["template"]["roles"]))
        self.assertIn("deepsci-org-reviewer", {role["id"] for role in data["template"]["roles"]})

        status, output = self.run_cli(["project", "--root", str(FIXTURE_PROJECT), "team-templates", "list", "--json"], env=team_repo_env)
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

        status, output = self.run_cli(
            ["project", "--root", str(FIXTURE_PROJECT), "team-templates", "validate", "deepsci-org", "--json"],
            env=team_repo_env,
        )
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
        packet_name_plans = [
            plan
            for plan in data["creation"]["path_plans"]
            if plan["source"] == "topic_team_instantiation_packet.agent_name" and plan["surface"].startswith("agent_workspace:")
        ]
        self.assertEqual(3, len(packet_name_plans))
        self.assertTrue(all("agent_name" in plan["source_detail"] for plan in packet_name_plans))
        packet_isomer_plans = [
            plan
            for plan in data["creation"]["path_plans"]
            if plan["source"] == "topic_team_instantiation_packet.agent_name" and plan["surface"].startswith("agent_isomer_managed:")
        ]
        self.assertEqual(3, len(packet_isomer_plans))

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

    def test_uc01_packet_rejects_cross_topic_agent_workspace_ref(self) -> None:
        root = self.copy_uc01_fixture_project("uc01-cross-topic-workspace-ref")
        self.append_manifest(
            root,
            """
            [[research_topics]]
            id = "other-topic"
            config_path = ".isomer-labs/research-topics/other-topic.toml"
            topic_workspace_id = "other-topic"

            [[topic_workspaces]]
            id = "other-topic"
            research_topic_id = "other-topic"
            path = "topic-workspaces/other-topic"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "other-topic.toml",
            """
            research_topic_id = "other-topic"
            topic_statement = "Other topic."
            """,
        )
        (root / "topic-workspaces" / "other-topic").mkdir(parents=True)
        packet_path = root / "fixtures" / "uc01" / "topic-team-instantiation-packet.toml"
        packet_path.write_text(
            packet_path.read_text(encoding="utf-8").replace(
                f"topic-workspaces/{UC01_RESEARCH_TOPIC_ID}/agents/deepsci-mini-lead",
                "topic-workspaces/other-topic/agents/alice",
            ),
            encoding="utf-8",
        )

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
                "fixtures/uc01/topic-team-instantiation-packet.toml",
                "--write",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO019", {diagnostic["code"] for diagnostic in data["diagnostics"]})
        self.assertIn(
            "role_bindings.deepsci-mini-lead.agent_workspace_ref",
            {diagnostic.get("field") for diagnostic in data["diagnostics"]},
        )

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
        self.assertTrue(all(plan["source"] == "topic_agent_team_profile.agent_name" for plan in creation["path_plans"]))
        master_workspace = next(workspace for workspace in creation["agent_workspaces"] if workspace["agent_name"] == "deepsci-org-master")
        self.assertIn("isomer_managed_path_plan_id", master_workspace)
        self.assertTrue(master_workspace["support_root_path"].endswith("agents/deepsci-org-master/isomer-managed"))
        self.assertEqual([f"{master_workspace['id']}:workspace-boundary"], master_workspace["boundary_refs"])
        self.assertIn("links_root", master_workspace["generated_link_summary"])
        master_isomer_plan = next(plan for plan in creation["path_plans"] if plan["surface"] == "agent_isomer_managed:deepsci-org-master")
        self.assertEqual(master_workspace["isomer_managed_path_plan_id"], master_isomer_plan["id"])
        self.assertEqual(0, len(team["run_ids"]))
        self.assertNotIn("houmao", output.lower())
        self.assertTrue((root / "topic-workspaces" / "alpha" / "agents").is_dir())
        self.assertTrue((root / "topic-workspaces" / "alpha" / "agents" / "deepsci-org-master" / "isomer-managed" / "agent-owned" / "public").is_dir())
        self.assertTrue((root / "topic-workspaces" / "alpha" / "agents" / "deepsci-org-master" / "isomer-managed" / "topic-owned" / "readonly").is_dir())
        self.assertTrue((root / "topic-workspaces" / "alpha" / "agents" / "deepsci-org-master" / "isomer-managed" / "links").is_dir())
        self.assertFalse((root / "topic-workspaces" / "alpha" / "agents" / "deepsci-org-master" / ".isomer-agent").exists())
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

    def test_runtime_validate_reports_isomer_managed_layout_diagnostics(self) -> None:
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
                "ati-alpha-diagnostics",
                "--json",
            ],
        ):
            status, output = self.run_cli(command, cwd=root)
            self.assertEqual(0, status, output)

        workspace = root / "topic-workspaces" / "alpha" / "agents" / "deepsci-org-master"
        (workspace / ".isomer-agent" / "runtime").mkdir(parents=True)
        shutil.rmtree(workspace / "isomer-managed" / "agent-owned" / "public")
        unsafe_target = root / "outside-link-target"
        unsafe_target.mkdir()
        (workspace / "isomer-managed" / "links" / "unsafe").symlink_to(unsafe_target, target_is_directory=True)
        unpromoted_artifact = workspace / "isomer-managed" / "agent-owned" / "artifacts" / "draft.txt"
        write(unpromoted_artifact, "draft\n")
        topic_tmp_artifact = root / "topic-workspaces" / "alpha" / "tmp" / "draft.txt"
        write(topic_tmp_artifact, "tmp draft\n")
        topic_main = root / "topic-workspaces" / "alpha" / "repos" / "topic-main"
        subprocess.run(["git", "init"], cwd=topic_main, check=True, capture_output=True, text=True)
        tracked_tmp = topic_main / "tmp" / "tracked.txt"
        write(tracked_tmp, "tracked tmp\n")
        subprocess.run(["git", "-C", str(topic_main), "add", "-f", "tmp/tracked.txt"], check=True, capture_output=True, text=True)
        (topic_main / ".gitignore").unlink(missing_ok=True)
        runtime_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(runtime_path) as db:
            db.execute(
                """
                INSERT INTO lifecycle_records (
                    id, record_kind, research_topic_id, topic_workspace_id, status,
                    created_at, updated_at, lifecycle_refs_json, transition_metadata_json,
                    content_path, provenance_refs_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "artifact:unpromoted",
                    "artifact",
                    "alpha",
                    "alpha",
                    "candidate",
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T00:00:00Z",
                    "{}",
                    "{}",
                    str(unpromoted_artifact),
                    "[]",
                ),
            )
            db.execute(
                """
                INSERT INTO lifecycle_records (
                    id, record_kind, research_topic_id, topic_workspace_id, status,
                    created_at, updated_at, lifecycle_refs_json, transition_metadata_json,
                    content_path, provenance_refs_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "artifact:tmp",
                    "artifact",
                    "alpha",
                    "alpha",
                    "candidate",
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T00:00:00Z",
                    "{}",
                    "{}",
                    str(topic_tmp_artifact),
                    "[]",
                ),
            )

        status, output = self.run_cli(["project", "runtime", "validate", "--topic", "alpha", "--json"], cwd=root)

        data = json.loads(output)
        self.assertEqual(1, status)
        messages = [diagnostic["message"] for diagnostic in data["diagnostics"]]
        self.assertTrue(any("legacy `.isomer-agent/`" in message for message in messages), messages)
        self.assertTrue(any("missing a standard `isomer-managed/` support subpath" in message for message in messages), messages)
        self.assertTrue(any("target points outside the selected Topic Workspace" in message for message in messages), messages)
        self.assertTrue(any("depends on untracked `isomer-managed/agent-owned/`" in message for message in messages), messages)
        self.assertTrue(any("ignore policy is missing" in message for message in messages), messages)
        self.assertTrue(any("Git tracks content under a Local Tmp Surface" in message for message in messages), messages)
        self.assertTrue(any("depends on Local Tmp Surface `topic.tmp`" in message for message in messages), messages)

    def test_team_instance_creation_uses_agent_name_path_plan_without_identity_alias(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        write(
            root / ".isomer-labs" / "team-profiles" / "uc-01-alpha.toml",
            self.profile_fixture(
                "uc-01-alpha",
                "alpha",
                "UC-01",
                agent_workspace_refs={
                    "deepsci-org-master": "topic-workspaces/alpha/agents/alice",
                },
            ),
        )
        self.add_project_pixi_manifest(root, environments=("alpha-main",), lockfile=True)
        self.add_topic_pixi_binding(root, "alpha", "alpha-main")
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
                "ati-alpha-ref",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(0, status, output)
        creation = data["creation"]
        agent_by_role = {agent["agent_role_id"]: agent for agent in creation["agent_instances"]}
        master_id = agent_by_role["deepsci-org-master"]["id"]
        self.assertNotEqual("alice", master_id)
        master_plan = next(plan for plan in creation["path_plans"] if plan["surface"] == "agent_workspace:alice")
        self.assertEqual(str((root / "topic-workspaces" / "alpha" / "agents" / "alice").resolve()), master_plan["path"])
        self.assertEqual("topic_agent_team_profile.agent_name", master_plan["source"])
        self.assertIn("role_bindings.deepsci-org-master.agent_name=alice", master_plan["source_detail"])
        master_isomer_plan = next(plan for plan in creation["path_plans"] if plan["surface"] == "agent_isomer_managed:alice")
        self.assertEqual(str((root / "topic-workspaces" / "alpha" / "agents" / "alice" / "isomer-managed").resolve()), master_isomer_plan["path"])
        self.assertTrue((root / "topic-workspaces" / "alpha" / "agents" / "alice").is_dir())

        fallback_plan = next(plan for plan in creation["path_plans"] if plan["surface"] == "agent_workspace:deepsci-org-framer")
        self.assertEqual("topic_agent_team_profile.agent_name", fallback_plan["source"])
        self.assertTrue(fallback_plan["path"].endswith("topic-workspaces/alpha/agents/deepsci-org-framer"))

    def test_team_instance_creation_rejects_unsafe_agent_workspace_ref_without_mutation(self) -> None:
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
        write(
            root / ".isomer-labs" / "team-profiles" / "uc-01-alpha.toml",
            self.profile_fixture(
                "uc-01-alpha",
                "alpha",
                "UC-01",
                agent_workspace_refs={
                    "deepsci-org-master": "topic-workspaces/beta/agents/alice",
                },
            ),
        )
        runtime_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        before_counts = self.runtime_counts(runtime_path)

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
                "ati-alpha-unsafe-ref",
                "--json",
            ],
            cwd=root,
        )
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertFalse(data["mutated"])
        self.assertIn("ISO019", {diagnostic["code"] for diagnostic in data["diagnostics"]})
        self.assertIn(
            "role_bindings.deepsci-org-master.agent_workspace_ref",
            {diagnostic.get("field") for diagnostic in data["diagnostics"]},
        )
        self.assertEqual(before_counts, self.runtime_counts(runtime_path))

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

        with patch("isomer_labs.runtime.records._agent_instance_id", side_effect=forced_id):
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

        with patch("isomer_labs.runtime.records._agent_instance_id", side_effect=generated_id):
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
            houmao_project_dir=None,
            actor_ref="operator-agent:test",
            created_at="2026-06-22T00:00:00Z",
        )
        self.assertEqual(str(root / ".isomer-labs"), link_manifest["houmao"]["project_dir"])
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

    def test_profile_validation_accepts_topic_workspace_agent_refs_and_rejects_cross_topic_refs(self) -> None:
        root = self.make_root()
        self.make_deepsci_profile_project(root)
        valid_profile = root / ".isomer-labs" / "team-profiles" / "valid-workspace-ref.toml"
        write(
            valid_profile,
            self.profile_fixture(
                "valid-workspace-ref",
                "alpha",
                "UC-01",
                agent_workspace_refs={
                    "deepsci-org-master": "topic-workspaces/alpha/agents/alice",
                },
            ),
        )

        status, output = self.run_cli(["project", "team-profiles", "validate", str(valid_profile), "--json"], cwd=root)
        self.assertEqual(0, status, output)

        cross_topic_profile = root / ".isomer-labs" / "team-profiles" / "cross-topic-workspace-ref.toml"
        write(
            cross_topic_profile,
            self.profile_fixture(
                "cross-topic-workspace-ref",
                "alpha",
                "UC-01",
                agent_workspace_refs={
                    "deepsci-org-master": "topic-workspaces/beta/agents/alice",
                },
            ),
        )

        status, output = self.run_cli(["project", "team-profiles", "validate", str(cross_topic_profile), "--json"], cwd=root)
        data = json.loads(output)
        self.assertEqual(1, status)
        self.assertIn("ISO019", {diagnostic["code"] for diagnostic in data["diagnostics"]})
        self.assertIn(
            "role_bindings.deepsci-org-master.agent_workspace_ref",
            {diagnostic.get("field") for diagnostic in data["diagnostics"]},
        )

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
                    'required_skills = ["isomer-deepsci-shared", "isomer-deepsci-scout", "isomer-deepsci-baseline"]',
                    'required_skills = ["isomer-deepsci-shared", "isomer-deepsci-baseline"]',
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
