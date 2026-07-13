from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from isomer_labs import cli
from isomer_labs.cli.commands.research_templates_ext import (
    DEFAULT_TEMPLATE_NAME,
    TEMPLATE_SEMANTIC_ID,
)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class ResearchTemplatesExtensionTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def make_project(self) -> Path:
        root = self.make_root()
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
            topic_statement = "Alpha topic"
            """,
        )
        (root / "topic-workspaces" / "alpha").mkdir(parents=True)
        status, output = self.run_main(["--print-json", "project", "--root", str(root), "runtime", "init", "--topic", "alpha"], cwd=root)
        self.assertEqual(0, status, output)
        return root

    def run_main(self, args: list[str], *, cwd: Path) -> tuple[int, str]:
        stdout = io.StringIO()
        with (
            contextlib.chdir(cwd),
            patch.dict(os.environ, {"HOME": str(cwd), "PATH": os.environ.get("PATH", "")}, clear=True),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(args)
        return status, stdout.getvalue()

    def run_templates(self, root: Path, args: list[str]) -> tuple[int, dict[str, object]]:
        status, output = self.run_main(["ext", "research", "templates", *args, "--project", str(root), "--topic", "alpha"], cwd=root)
        return status, json.loads(output)

    def test_create_default_main_template_and_record(self) -> None:
        root = self.make_project()
        with patch("isomer_labs.cli.commands.research_templates_ext._compile_preview") as compile_mock:
            compile_mock.return_value = {
                "ok": True,
                "engine": "tectonic",
                "fallback": False,
                "fallback_reason": None,
                "attempts": [],
                "preview_pdf": str(root / "topic-workspaces" / "alpha" / "intent" / "derived" / "writing-template" / "main" / "preview.pdf"),
            }
            status, created = self.run_templates(root, ["create"])
        self.assertEqual(0, status, created)
        self.assertTrue(created.get("ok"), created)
        template_dir = Path(root / "topic-workspaces" / "alpha" / "intent" / "derived" / "writing-template" / "main")
        self.assertTrue((template_dir / "main.tex").exists())
        self.assertTrue((template_dir / "references.bib").exists())
        self.assertTrue((template_dir / "README.md").exists())
        record = created["record"]
        assert isinstance(record, dict)
        self.assertEqual(TEMPLATE_SEMANTIC_ID, record["transition_metadata"]["semantic_id"])

    def test_create_named_template_and_list_shows_default(self) -> None:
        root = self.make_project()
        with patch("isomer_labs.cli.commands.research_templates_ext._compile_preview") as compile_mock:
            compile_mock.return_value = {"ok": True, "engine": "tectonic", "fallback": False, "fallback_reason": None, "attempts": [], "preview_pdf": ""}
            status, _ = self.run_templates(root, ["create", "--name", "neurips"])
            self.assertEqual(0, status)
            status, listed = self.run_templates(root, ["list"])
        self.assertEqual(0, status, listed)
        records = listed["records"]
        self.assertEqual(1, len(records))
        self.assertFalse(records[0].get("is_default"))
        status, main_created = self.run_templates(root, ["create", "--name", DEFAULT_TEMPLATE_NAME])
        self.assertEqual(0, status, main_created)
        status, listed = self.run_templates(root, ["list"])
        self.assertEqual(0, status, listed)
        defaults = [r for r in listed["records"] if r.get("is_default")]
        self.assertEqual(1, len(defaults))

    def test_show_returns_file_tree_and_readme(self) -> None:
        root = self.make_project()
        with patch("isomer_labs.cli.commands.research_templates_ext._compile_preview") as compile_mock:
            compile_mock.return_value = {"ok": True, "engine": "tectonic", "fallback": False, "fallback_reason": None, "attempts": [], "preview_pdf": ""}
            status, _ = self.run_templates(root, ["create", "--name", "iclr", "--venue", "iclr"])
            self.assertEqual(0, status)
            status, shown = self.run_templates(root, ["show", "--name", "iclr"])
        self.assertEqual(0, status, shown)
        self.assertIn("main.tex", shown["file_tree"])
        self.assertIn("Writing Template: iclr", shown["readme"])

    def test_refresh_creates_descendant_record(self) -> None:
        root = self.make_project()
        with patch("isomer_labs.cli.commands.research_templates_ext._compile_preview") as compile_mock:
            compile_mock.return_value = {"ok": True, "engine": "tectonic", "fallback": False, "fallback_reason": None, "attempts": [], "preview_pdf": ""}
            status, created = self.run_templates(root, ["create", "--name", "refreshable"])
            self.assertEqual(0, status)
            first_id = created["record"]["id"]
            status, refreshed = self.run_templates(root, ["refresh", "--name", "refreshable"])
        self.assertEqual(0, status, refreshed)
        self.assertEqual(first_id, refreshed["revision_of_record_id"])

    def test_compile_revises_record_status(self) -> None:
        root = self.make_project()
        with patch("isomer_labs.cli.commands.research_templates_ext._compile_preview") as compile_mock:
            compile_mock.return_value = {"ok": True, "engine": "tectonic", "fallback": False, "fallback_reason": None, "attempts": [], "preview_pdf": ""}
            status, created = self.run_templates(root, ["create", "--name", "recompilable"])
            self.assertEqual(0, status)
            compile_mock.return_value = {"ok": False, "engine": None, "fallback": False, "attempts": [], "preview_pdf": None}
            status, compiled = self.run_templates(root, ["compile", "--name", "recompilable"])
        self.assertEqual(1, status, compiled)
        self.assertEqual("failed", compiled["preview_build"]["ok"])

    def test_remove_archives_record_and_can_delete_files(self) -> None:
        root = self.make_project()
        with patch("isomer_labs.cli.commands.research_templates_ext._compile_preview") as compile_mock:
            compile_mock.return_value = {"ok": True, "engine": "tectonic", "fallback": False, "fallback_reason": None, "attempts": [], "preview_pdf": ""}
            status, created = self.run_templates(root, ["create", "--name", "removable"])
        self.assertEqual(0, status)
        template_dir = Path(root / "topic-workspaces" / "alpha" / "intent" / "derived" / "writing-template" / "removable")
        self.assertTrue(template_dir.exists())
        status, removed = self.run_templates(root, ["remove", "--name", "removable", "--delete-files"])
        self.assertEqual(0, status, removed)
        self.assertEqual("archived", removed["record"]["status"])
        self.assertFalse(template_dir.exists())


if __name__ == "__main__":
    unittest.main()
