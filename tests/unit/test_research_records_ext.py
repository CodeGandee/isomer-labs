from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from isomer_labs import cli


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class ResearchRecordsExtensionTests(unittest.TestCase):
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

    def run_records(self, root: Path, args: list[str]) -> tuple[int, dict[str, object]]:
        status, output = self.run_main(["ext", "research", "records", *args, "--project", str(root), "--topic", "alpha"], cwd=root)
        return status, json.loads(output)

    def test_record_crud_preserves_placeholder_metadata_and_body(self) -> None:
        root = self.make_project()
        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "artifact-main-run",
                "--record-kind",
                "artifact",
                "--placeholder",
                "<MAIN_RUN_RECORD>",
                "--profile",
                "run.main-experiment",
                "--skill",
                "isomer-rsch-experiment-v2",
                "--producer",
                "isomer-rsch-experiment-v2",
                "--consumer",
                "analysis",
                "--body",
                "measured run body",
                "--content-name",
                "main-run.md",
                "--metadata-json",
                '{"quality":"draft"}',
                "--lifecycle-refs-json",
                '{"research_task_id":"task-alpha"}',
            ],
        )
        self.assertEqual(0, status, created)
        self.assertEqual(True, created["ok"])
        record = created["record"]
        assert isinstance(record, dict)
        self.assertEqual("artifact-main-run", record["id"])
        self.assertEqual("artifact", record["record_kind"])
        self.assertEqual("ready", record["status"])
        metadata = record["transition_metadata"]
        assert isinstance(metadata, dict)
        self.assertEqual("<MAIN_RUN_RECORD>", metadata["placeholder"])
        self.assertEqual("run.main-experiment", metadata["profile"])
        self.assertEqual("draft", metadata["quality"])
        lifecycle_refs = record["lifecycle_refs"]
        assert isinstance(lifecycle_refs, dict)
        self.assertEqual("task-alpha", lifecycle_refs["research_task_id"])
        content_path = Path(str(record["content_path"]))
        self.assertTrue(content_path.exists())
        self.assertEqual("measured run body", content_path.read_text(encoding="utf-8"))

        status, listed = self.run_records(
            root,
            [
                "list",
                "--record-kind",
                "artifact",
                "--placeholder",
                "<MAIN_RUN_RECORD>",
                "--profile",
                "run.main-experiment",
            ],
        )
        self.assertEqual(0, status, listed)
        self.assertEqual(1, listed["count"])

        status, shown = self.run_records(root, ["show", "artifact-main-run", "--include-body"])
        self.assertEqual(0, status, shown)
        self.assertEqual("measured run body", shown["body"])

        status, updated = self.run_records(
            root,
            [
                "update",
                "artifact-main-run",
                "--record-kind",
                "artifact",
                "--status",
                "complete",
                "--placeholder",
                "<MAIN_RUN_RECORD>",
                "--body",
                "updated run body",
                "--content-name",
                "main-run-updated.md",
            ],
        )
        self.assertEqual(0, status, updated)
        updated_record = updated["record"]
        assert isinstance(updated_record, dict)
        self.assertEqual("complete", updated_record["status"])
        updated_path = Path(str(updated_record["content_path"]))
        self.assertEqual("updated run body", updated_path.read_text(encoding="utf-8"))

        status, deleted = self.run_records(root, ["delete", "artifact-main-run", "--reason", "superseded"])
        self.assertEqual(0, status, deleted)
        archived_record = deleted["record"]
        assert isinstance(archived_record, dict)
        self.assertEqual("archived", archived_record["status"])
        self.assertTrue(updated_path.exists())
        archive_metadata = archived_record["transition_metadata"]
        assert isinstance(archive_metadata, dict)
        self.assertEqual("superseded", archive_metadata["archive_reason"])

    def test_create_can_copy_body_file_to_run_records_label(self) -> None:
        root = self.make_project()
        body_file = root / "source-run.txt"
        body_file.write_text("run output", encoding="utf-8")
        status, created = self.run_records(
            root,
            [
                "create",
                "--record-kind",
                "run",
                "--id",
                "run-alpha",
                "--placeholder",
                "<MAIN_RUN_RECORD>",
                "--body-file",
                str(body_file),
                "--content-name",
                "run-alpha.txt",
            ],
        )
        self.assertEqual(0, status, created)
        record = created["record"]
        assert isinstance(record, dict)
        content_path = Path(str(record["content_path"]))
        self.assertIn("records/runs", content_path.as_posix())
        self.assertEqual("run output", content_path.read_text(encoding="utf-8"))

    def test_context_resolution_failure_is_deterministic(self) -> None:
        root = self.make_root()
        status, output = self.run_main(
            ["ext", "research", "records", "list", "--project", str(root), "--topic", "missing"],
            cwd=root,
        )
        self.assertEqual(1, status, output)
        payload = json.loads(output)
        self.assertEqual(False, payload["ok"])
        self.assertEqual("context_resolution_failed", payload["error"]["code"])
