from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from isomer_labs import cli


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class KaojuRecordLifecycleIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        write(
            self.root / ".isomer-labs/manifest.toml",
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
            self.root / ".isomer-labs/research-topics/alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            topic_statement = "Alpha survey"
            """,
        )
        write(self.root / "topic-workspaces/alpha/isomer-topic-workspace-summary.md", "# Alpha\n")
        status, output = self.run_cli(["--print-json", "project", "--root", str(self.root), "runtime", "init", "--topic", "alpha"])
        self.assertEqual(0, status, output)

    def run_cli(self, arguments: list[str]) -> tuple[int, dict[str, object]]:
        stdout = io.StringIO()
        with (
            contextlib.chdir(self.root),
            patch.dict(os.environ, {"HOME": str(self.root), "PATH": os.environ.get("PATH", "")}, clear=True),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(arguments)
        return status, json.loads(stdout.getvalue())

    def record_command(self, arguments: list[str]) -> tuple[int, dict[str, object]]:
        return self.run_cli(
            ["--print-json", "ext", "research", "records", *arguments, "--project", str(self.root), "--topic", "alpha"]
        )

    def payload(self, name: str, *, semantic_id: str, artifact_type: str, section_name: str, summary: str) -> Path:
        path = self.root / name
        path.write_text(
            json.dumps(
                {
                    "title": artifact_type.replace("-", " ").title(),
                    "summary": summary,
                    "artifact_family": "kaoju",
                    "semantic_id": semantic_id,
                    "artifact_type": artifact_type,
                    "procedure": "landscape-pass",
                    "sections": {section_name: {"state": "ready"}},
                }
            ),
            encoding="utf-8",
        )
        return path

    def test_create_revise_query_render_export_rebuild_and_reset_preservation(self) -> None:
        status, checkpoint = self.run_cli(
            ["--print-json", "project", "--root", str(self.root), "topic-reset", "checkpoint", "--topic", "alpha"]
        )
        self.assertEqual(0, status, checkpoint)
        checkpoint_id = str(checkpoint["checkpoint_id"])

        binding_index = self.payload(
            "binding-index.json",
            semantic_id="kaoju:binding-index",
            artifact_type="binding-index",
            section_name="bindings",
            summary="Selected Kaoju bindings are ready.",
        )
        status, binding_record = self.record_command(
            [
                "create",
                "--id",
                "kaoju-binding-index",
                "--record-kind",
                "view_manifest",
                "--semantic-id",
                "kaoju:binding-index",
                "--format-profile",
                "isomer:research/record-format/profile/kaoju/control/binding-index/v1",
                "--payload-file",
                str(binding_index),
            ]
        )
        self.assertEqual(0, status, binding_record)
        readiness = self.payload(
            "workspace-readiness.json",
            semantic_id="kaoju:workspace-readiness",
            artifact_type="workspace-readiness",
            section_name="readiness",
            summary="Kaoju storage surfaces are ready.",
        )
        status, readiness_record = self.record_command(
            [
                "create",
                "--id",
                "kaoju-workspace-readiness",
                "--record-kind",
                "artifact",
                "--semantic-id",
                "kaoju:workspace-readiness",
                "--format-profile",
                "isomer:research/record-format/profile/kaoju/control/workspace-readiness/v1",
                "--payload-file",
                str(readiness),
                "--parents-json",
                '[{"record_id":"kaoju-binding-index","role":"binding_index"}]',
                "--lineage-kind",
                "derived_from",
            ]
        )
        self.assertEqual(0, status, readiness_record)

        contract_v1 = self.payload(
            "contract-v1.json",
            semantic_id="kaoju:survey-contract",
            artifact_type="survey-contract",
            section_name="scope",
            summary="Initial survey boundary.",
        )
        profile = "isomer:research/record-format/profile/kaoju/contract/survey-contract/v1"
        status, created = self.record_command(
            ["create", "--id", "contract-v1", "--record-kind", "artifact", "--semantic-id", "kaoju:survey-contract", "--format-profile", profile, "--payload-file", str(contract_v1)]
        )
        self.assertEqual(0, status, created)

        contract_v2 = self.payload(
            "contract-v2.json",
            semantic_id="kaoju:survey-contract",
            artifact_type="survey-contract",
            section_name="scope",
            summary="Revised survey boundary.",
        )
        status, revised = self.record_command(["revise", "contract-v1", "--id", "contract-v2", "--payload-file", str(contract_v2)])
        self.assertEqual(0, status, revised)

        catalog = self.payload(
            "catalog.json",
            semantic_id="kaoju:related-work-catalog",
            artifact_type="related-work-catalog",
            section_name="works",
            summary="Accepted related works.",
        )
        status, catalog_record = self.record_command(
            [
                "create",
                "--id",
                "catalog-v1",
                "--record-kind",
                "artifact",
                "--semantic-id",
                "kaoju:related-work-catalog",
                "--format-profile",
                "isomer:research/record-format/profile/kaoju/catalog/related-work-catalog/v1",
                "--payload-file",
                str(catalog),
                "--parents-json",
                '[{"record_id":"contract-v2","role":"survey_contract"}]',
                "--lineage-kind",
                "derived_from",
            ]
        )
        self.assertEqual(0, status, catalog_record)

        catalog_v2 = self.payload(
            "catalog-v2.json",
            semantic_id="kaoju:related-work-catalog",
            artifact_type="related-work-catalog",
            section_name="works",
            summary="Revised accepted related works.",
        )
        status, revised_catalog = self.record_command(
            ["revise", "catalog-v1", "--id", "catalog-v2", "--payload-file", str(catalog_v2)]
        )
        self.assertEqual(0, status, revised_catalog)

        status, latest = self.record_command(["query", "list", "--artifact-family", "kaoju", "--semantic-id", "kaoju:survey-contract", "--latest-only"])
        self.assertEqual(0, status, latest)
        self.assertEqual(["contract-v2"], [item["record_id"] for item in latest["records"]])
        status, lineage = self.record_command(["query", "lineage", "catalog-v1"])
        self.assertEqual(0, status, lineage)
        self.assertTrue(
            any(
                edge["source_record_id"] == "contract-v2" and edge["target_record_id"] == "catalog-v1"
                for edge in lineage["edges"]
            )
        )
        status, latest_catalog = self.record_command(
            ["query", "list", "--artifact-family", "kaoju", "--semantic-id", "kaoju:related-work-catalog", "--latest-only"]
        )
        self.assertEqual(0, status, latest_catalog)
        self.assertEqual(["catalog-v2"], [item["record_id"] for item in latest_catalog["records"]])

        export = self.root / "exports/contract.md"
        status, rendered = self.record_command(["render", "contract-v2", "--output-file", str(export)])
        self.assertEqual(0, status, rendered)
        self.assertTrue(export.is_file())
        status, rebuilt = self.record_command(["index", "rebuild"])
        self.assertEqual(0, status, rebuilt)

        for record_id in ("kaoju-binding-index", "kaoju-workspace-readiness", "contract-v2", "catalog-v2"):
            status, updated = self.run_cli(
                [
                    "--print-json",
                    "project",
                    "--root",
                    str(self.root),
                    "topic-reset",
                    "update-checkpoint",
                    "--topic",
                    "alpha",
                    "--preserve-record",
                    record_id,
                    "--source-label",
                    "isomer-kaoju-workspace-mgr",
                    checkpoint_id,
                ]
            )
            self.assertEqual(0, status, updated)
        status, plan = self.run_cli(
            ["--print-json", "project", "--root", str(self.root), "topic-reset", "plan", "--topic", "alpha", checkpoint_id]
        )
        self.assertEqual(0, status, plan)
        preserved = {action.get("target_ref") for action in plan["actions"] if action.get("action") == "preserve"}
        self.assertTrue({"kaoju-binding-index", "kaoju-workspace-readiness", "contract-v2", "catalog-v2"} <= preserved)


if __name__ == "__main__":
    unittest.main()
