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
from isomer_labs.team_repositories import TEAM_REPOSITORIES_ENV, load_team_repository
from isomer_labs.team_templates import discover_domain_agent_team_templates


REPO_ROOT = Path(__file__).resolve().parents[2]


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class TeamRepositoryTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def test_missing_malformed_and_path_escaping_manifests_report_errors(self) -> None:
        missing = load_team_repository(self.make_root())
        self.assertFalse(missing.ok)
        self.assertEqual(["ISO001"], [diagnostic.code for diagnostic in missing.diagnostics])

        malformed_root = self.make_root()
        write(malformed_root / "isomer-team-repo.toml", "schema_version =")
        malformed = load_team_repository(malformed_root)
        self.assertFalse(malformed.ok)
        self.assertEqual(["ISO002"], [diagnostic.code for diagnostic in malformed.diagnostics])

        escaping_root = self.make_root()
        write(
            escaping_root / "isomer-team-repo.toml",
            """
            schema_version = "isomer-team-repository.v1"
            id = "escaping"

            [[domain_agent_team_templates]]
            id = "bad"
            path = "../outside"
            """,
        )
        escaping = load_team_repository(escaping_root)
        self.assertFalse(escaping.ok)
        self.assertEqual([], escaping.templates)
        self.assertIn("ISO016", {diagnostic.code for diagnostic in escaping.diagnostics})

    def test_project_local_and_team_repository_templates_merge_with_provenance(self) -> None:
        root = self.make_root()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [[domain_agent_team_templates]]
            id = "local-method"
            path = "templates/local-method"

            [[team_repositories]]
            id = "local-repo"
            path = "team-repo"
            """,
        )
        write(
            root / "team-repo" / "isomer-team-repo.toml",
            """
            schema_version = "isomer-team-repository.v1"
            id = "local-repo"

            [[domain_agent_team_templates]]
            id = "repo-method"
            path = "templates/repo-method"
            """,
        )
        project, diagnostics = discover_project(cwd=root, env={})
        self.assertEqual([], diagnostics)
        self.assertIsNotNone(project)
        assert project is not None

        templates = discover_domain_agent_team_templates(project)
        by_id = {template.id: template for template in templates}
        self.assertEqual(["local-method", "repo-method"], sorted(by_id))
        self.assertEqual("project", by_id["local-method"].source_kind)
        self.assertEqual("team-repository", by_id["repo-method"].source_kind)
        self.assertEqual("local-repo", by_id["repo-method"].team_repository_id)

    def test_cli_lists_no_templates_without_checkout_local_team_repository(self) -> None:
        status, data = self._run_json(["--print-json", "project", "team-templates", "list"])
        self.assertEqual(0, status)
        self.assertEqual([], data["templates"])

    def test_package_smoke_imports_entrypoint_lists_schemas_and_templates_without_team_repo(self) -> None:
        self.assertTrue(callable(cli.main))
        status, data = self._run_json(["--print-json", "schemas", "list"])
        self.assertEqual(0, status)
        self.assertTrue(data["schemas"])

        status, data = self._run_json(["--print-json", "project", "team-templates", "list"])
        self.assertEqual(0, status)
        self.assertEqual([], data["templates"])

    def test_cli_lists_templates_from_explicit_team_repository(self) -> None:
        status, data = self._run_json(
            ["--print-json", "project", "team-repositories", "list"],
            env={TEAM_REPOSITORIES_ENV: str(REPO_ROOT)},
        )
        self.assertEqual(0, status)
        self.assertEqual(["isomer-local-teams"], [repo["id"] for repo in data["team_repositories"]])

        status, data = self._run_json(
            ["--print-json", "project", "team-templates", "list"],
            env={TEAM_REPOSITORIES_ENV: str(REPO_ROOT)},
        )
        self.assertEqual(0, status)
        self.assertEqual(["deepsci-mini", "deepsci-org"], [template["id"] for template in data["templates"]])
        self.assertEqual({"team-repository"}, {template["source_kind"] for template in data["templates"]})

    def test_cli_registers_team_repository_template_into_project_manifest(self) -> None:
        root = self.make_root()
        write(root / ".isomer-labs" / "manifest.toml", 'schema_version = "isomer-project-manifest.v1"\n')

        status, data = self._run_json(
            [
                "--print-json",
                "project",
                "--root",
                str(root),
                "team-templates",
                "register",
                "deepsci-mini",
                "--from-repository",
                "isomer-local-teams",
                "--write",
            ],
            env={TEAM_REPOSITORIES_ENV: str(REPO_ROOT)},
        )
        self.assertEqual(0, status)
        self.assertTrue(data["mutated"])
        manifest_text = (root / ".isomer-labs" / "manifest.toml").read_text(encoding="utf-8")
        self.assertIn('id = "deepsci-mini"', manifest_text)
        self.assertIn('source_kind = "team-repository"', manifest_text)
        self.assertIn('team_repository_id = "isomer-local-teams"', manifest_text)

    def _run_json(self, args: list[str], env: dict[str, str] | None = None) -> tuple[int, dict[str, object]]:
        runner = CliRunner()
        root = self.make_root()
        with contextlib.chdir(root), patch.dict(os.environ, env or {}, clear=True):
            result = runner.invoke(cli.app, args, standalone_mode=False)
        if result.exception is not None:
            raise result.exception
        return int(result.return_value or 0), json.loads(result.output)


if __name__ == "__main__":
    unittest.main()
