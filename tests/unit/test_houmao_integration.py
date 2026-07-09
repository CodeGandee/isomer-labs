from __future__ import annotations

import contextlib
import json
import os
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from click.testing import CliRunner

from isomer_labs import cli
from isomer_labs.project import discover_project
from isomer_labs.project.houmao_integration import (
    TOPIC_SERVICE_MASTER_ROUTES,
    houmao_integration_state,
)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class HoumaoIntegrationTests(unittest.TestCase):
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
    ) -> tuple[int, dict[str, object]]:
        root = cwd or self.make_root()
        normalized = ["--print-json", *args]
        runner = CliRunner()
        with contextlib.chdir(root), patch.dict(os.environ, env or {}, clear=True):
            result = runner.invoke(cli.app, normalized, standalone_mode=False)
        if result.exception is not None:
            raise result.exception
        return int(result.return_value or 0), json.loads(result.output)

    def write_minimal_project(self, root: Path, *, integration: str | None = None) -> None:
        integration_text = ""
        if integration is not None:
            integration_text = f"""
            [operator.integrations.houmao]
            status = "{integration}"
            skill_root = ".isomer-labs/houmao-skills"
            project_dir = ".isomer-labs"
            """
        write(
            root / ".isomer-labs" / "manifest.toml",
            f"""
            schema_version = "isomer-project-manifest.v1"
            {integration_text}
            """,
        )

    def write_topic_project(self, root: Path, *, integration: str = "enabled") -> None:
        write(
            root / ".isomer-labs" / "manifest.toml",
            f"""
            schema_version = "isomer-project-manifest.v1"

            [defaults]
            research_topic_id = "alpha"
            topic_workspace_id = "alpha"

            [operator.integrations.houmao]
            status = "{integration}"
            skill_root = ".isomer-labs/houmao-skills"
            project_dir = ".isomer-labs"

            [[research_topics]]
            id = "alpha"
            config_path = ".isomer-labs/research-topics/alpha.toml"
            topic_workspace_id = "alpha"
            status = "active"

            [[topic_workspaces]]
            id = "alpha"
            research_topic_id = "alpha"
            path = "topic-workspaces/alpha"
            status = "active"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            topic_statement = "Investigate alpha."
            """,
        )

    def write_houmao_skill_source(self, root: Path) -> Path:
        source = root / "houmao-source"
        write(source / "catalog.toml", "schema_version = 1\n")
        skill_names = {
            "houmao-agent-definition",
            "houmao-agent-email-comms",
            "houmao-agent-gateway",
            "houmao-agent-inspect",
            "houmao-agent-instance",
            "houmao-agent-messaging",
            "houmao-credential-mgr",
            "houmao-mailbox-mgr",
            "houmao-project-mgr",
            "houmao-utils-workspace-mgr",
        }
        for skill_name in sorted(skill_names):
            write(
                source / skill_name / "SKILL.md",
                f"""
                ---
                name: {skill_name}
                description: Test Houmao skill.
                ---

                # {skill_name}
                """,
            )
        return source

    def discover(self, root: Path):
        project, diagnostics = discover_project(cwd=root, env={}, project_selector=str(root))
        self.assertIsNotNone(project)
        self.assertEqual([], [diagnostic.to_json() for diagnostic in diagnostics])
        return project

    def test_manifest_policy_parses_missing_disabled_enabled_and_invalid_paths(self) -> None:
        root = self.make_root()
        self.write_minimal_project(root)
        project = self.discover(root)
        state = houmao_integration_state(project)
        self.assertEqual("not_configured", state.integration_status)
        self.assertEqual(root / ".isomer-labs" / "houmao-skills", state.skill_root_path)

        status, payload = self.run_cli(["project", "--root", str(root), "integrations", "houmao", "disable"], cwd=root)
        self.assertEqual(0, status, payload)
        self.assertEqual("disabled", payload["integration_status"])
        self.assertIn("[operator.integrations.houmao]", (root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8"))

        status, payload = self.run_cli(["project", "--root", str(root), "integrations", "houmao", "enable"], cwd=root)
        self.assertEqual(0, status, payload)
        self.assertEqual("enabled", payload["integration_status"])

        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [operator.integrations.houmao]
            status = "enabled"
            skill_root = "../outside"
            project_dir = ".isomer-labs"
            """,
        )
        status, payload = self.run_cli(["project", "--root", str(root), "integrations", "houmao", "status"], cwd=root)
        self.assertEqual(1, status, payload)
        self.assertTrue(any(diagnostic["field"] == "operator.integrations.houmao.skill_root" for diagnostic in payload["diagnostics"]))

    def test_prepare_skills_projects_routes_idempotently_and_refuses_unmanaged_collision(self) -> None:
        root = self.make_root()
        self.write_minimal_project(root, integration="enabled")
        source = self.write_houmao_skill_source(root)
        env = {"ISOMER_HOUMAO_SYSTEM_SKILLS_SOURCE": str(source)}

        status, payload = self.run_cli(["project", "--root", str(root), "integrations", "houmao", "prepare-skills"], cwd=root, env=env)
        self.assertEqual(0, status, payload)
        self.assertTrue(payload["mutated"])
        self.assertEqual(list(TOPIC_SERVICE_MASTER_ROUTES), payload["projected_routes"])
        projection_root = root / ".isomer-labs" / "houmao-skills"
        self.assertTrue((projection_root / "projection-manifest.json").is_file())
        self.assertTrue((projection_root / "prepare-topic-service-master" / ".isomer-projection.json").is_file())
        self.assertFalse((projection_root / ".houmao").exists())

        status, payload = self.run_cli(["project", "--root", str(root), "integrations", "houmao", "prepare-skills"], cwd=root, env=env)
        self.assertEqual(0, status, payload)
        self.assertFalse(payload["mutated"])

        unmanaged = root / ".isomer-labs" / "houmao-skills" / "launch-topic-service-master"
        for child in unmanaged.iterdir():
            if child.is_file() and child.name != ".isomer-projection.json":
                child.unlink()
        (unmanaged / ".isomer-projection.json").unlink()
        write(unmanaged / "SKILL.md", "# unmanaged\n")
        status, payload = self.run_cli(["project", "--root", str(root), "integrations", "houmao", "prepare-skills"], cwd=root, env=env)
        self.assertEqual(1, status, payload)
        self.assertTrue(any("Refusing to overwrite unmanaged" in diagnostic["message"] for diagnostic in payload["diagnostics"]))

    def test_cli_skill_context_uses_manifest_routes_and_topic_context(self) -> None:
        root = self.make_root()
        self.write_topic_project(root)
        source = self.write_houmao_skill_source(root)
        env = {"ISOMER_HOUMAO_SYSTEM_SKILLS_SOURCE": str(source)}
        status, payload = self.run_cli(["project", "--root", str(root), "integrations", "houmao", "prepare-skills"], cwd=root, env=env)
        self.assertEqual(0, status, payload)

        status, payload = self.run_cli(
            [
                "project",
                "--root",
                str(root),
                "integrations",
                "houmao",
                "skill-context",
                "prepare-topic-service-master",
                "--topic",
                "alpha",
            ],
            cwd=root,
        )
        self.assertEqual(0, status, payload)
        self.assertEqual("enabled", payload["integration_status"])
        self.assertEqual("alpha", payload["research_topic_id"])
        self.assertEqual("alpha", payload["topic_workspace_id"])
        self.assertTrue(str(payload["houmao_skill_path"]).endswith("prepare-topic-service-master/SKILL.md"))
        self.assertIn("--project-dir", str(payload["instructions"]))

        status, payload = self.run_cli(["project", "--root", str(root), "integrations", "houmao", "skill-context", "unknown-route"], cwd=root)
        self.assertEqual(1, status, payload)
        self.assertIsNone(payload["houmao_skill_path"])
        self.assertTrue(any("Unknown Houmao skill route" in diagnostic["message"] for diagnostic in payload["diagnostics"]))

    def test_disabled_policy_skips_prepare_and_skill_context(self) -> None:
        root = self.make_root()
        self.write_minimal_project(root, integration="disabled")

        status, payload = self.run_cli(["project", "--root", str(root), "integrations", "houmao", "prepare-skills"], cwd=root)
        self.assertEqual(0, status, payload)
        self.assertFalse(payload["mutated"])
        self.assertEqual("disabled", payload["integration_status"])
        self.assertFalse((root / ".isomer-labs" / "houmao-skills").exists())

        status, payload = self.run_cli(["project", "--root", str(root), "integrations", "houmao", "skill-context", "prepare-topic-service-master"], cwd=root)
        self.assertEqual(0, status, payload)
        self.assertEqual("disabled", payload["integration_status"])
        self.assertIsNone(payload["houmao_skill_path"])
        self.assertIn("disables Houmao integration", str(payload["skip_reason"]))


if __name__ == "__main__":
    unittest.main()
