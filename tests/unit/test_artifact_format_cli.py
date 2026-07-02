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
from isomer_labs.deepsci_ext.record_formats import canonical_record_format_ref


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class ArtifactFormatCliTests(unittest.TestCase):
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

    def test_validate_builtin_deepsci_profile_emits_wrapped_json(self) -> None:
        root = self.make_project()
        payload_file = root / "payload.json"
        payload_file.write_text('{"title":"Main run","summary":"ok"}', encoding="utf-8")
        profile_ref = canonical_record_format_ref("run.main-run-record", "profile")
        status, output = self.run_main(
            [
                "--print-json",
                "project",
                "--root",
                str(root),
                "artifact-formats",
                "validate",
                "--topic",
                "alpha",
                "--format-profile",
                profile_ref,
                "--payload-file",
                str(payload_file),
            ],
            cwd=root,
        )
        self.assertEqual(0, status, output)
        data = json.loads(output)
        self.assertEqual("isomer-cli-output.v1", data["output_schema_version"])
        self.assertEqual(True, data["ok"])
        self.assertEqual("valid", data["validation"]["status"])

    def test_plain_path_render_prints_rendered_content_in_json(self) -> None:
        root = self.make_project()
        payload_file = root / "payload.json"
        schema_file = root / "schema.json"
        template_file = root / "record.md.j2"
        payload_file.write_text('{"title":"Plain render"}', encoding="utf-8")
        schema_file.write_text('{"type":"object","required":["title"],"properties":{"title":{"type":"string"}}}', encoding="utf-8")
        template_file.write_text("# {{ payload.title }}\n", encoding="utf-8")
        status, output = self.run_main(
            [
                "--print-json",
                "project",
                "--root",
                str(root),
                "artifact-formats",
                "render",
                "--topic",
                "alpha",
                "--schema-file",
                str(schema_file),
                "--template-file",
                str(template_file),
                "--payload-file",
                str(payload_file),
            ],
            cwd=root,
        )
        self.assertEqual(0, status, output)
        data = json.loads(output)
        self.assertEqual("# Plain render", data["render"]["content"].strip())

    def test_custom_registration_resolves_from_workspace_runtime(self) -> None:
        root = self.make_project()
        schema_file = root / "formats" / "ablation.schema.json"
        template_file = root / "formats" / "ablation.md.j2"
        payload_file = root / "payload.json"
        profile_ref = "custom:alpha/record-format/profile/experiment/ablation-report/v1"
        write(
            schema_file,
            """
            {
              "type": "object",
              "required": ["title", "result"],
              "properties": {
                "title": {"type": "string"},
                "result": {"type": "string"}
              }
            }
            """,
        )
        template_file.write_text("# {{ payload.title }}\n\n{{ payload.result }}\n", encoding="utf-8")
        payload_file.write_text('{"title":"Ablation","result":"passed"}', encoding="utf-8")
        status, register_output = self.run_main(
            [
                "--print-json",
                "project",
                "--root",
                str(root),
                "artifact-formats",
                "register",
                "--topic",
                "alpha",
                "--format-profile",
                profile_ref,
                "--schema-file",
                str(schema_file),
                "--template-file",
                str(template_file),
            ],
            cwd=root,
        )
        self.assertEqual(0, status, register_output)
        registered = json.loads(register_output)
        self.assertEqual(profile_ref, registered["registration"]["format_profile_ref"])
        self.assertTrue(Path(registered["registration"]["schema_snapshot_path"]).exists())

        status, validate_output = self.run_main(
            [
                "--print-json",
                "project",
                "--root",
                str(root),
                "artifact-formats",
                "validate",
                "--topic",
                "alpha",
                "--format-profile",
                profile_ref,
                "--payload-file",
                str(payload_file),
            ],
            cwd=root,
        )
        self.assertEqual(0, status, validate_output)
        validated = json.loads(validate_output)
        self.assertEqual("valid", validated["validation"]["status"])

    def test_missing_ref_reports_diagnostic(self) -> None:
        root = self.make_project()
        payload_file = root / "payload.json"
        payload_file.write_text('{"title":"Missing"}', encoding="utf-8")
        status, output = self.run_main(
            [
                "--print-json",
                "project",
                "--root",
                str(root),
                "artifact-formats",
                "validate",
                "--topic",
                "alpha",
                "--schema-ref",
                "isomer:deepsci/record-format/schema/missing/profile/v1",
                "--payload-file",
                str(payload_file),
            ],
            cwd=root,
        )
        self.assertEqual(1, status, output)
        data = json.loads(output)
        self.assertEqual(False, data["ok"])
        self.assertEqual("ISO201", data["diagnostics"][0]["code"])


if __name__ == "__main__":
    unittest.main()
