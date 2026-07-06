from __future__ import annotations

import contextlib
import io
import json
import os
import sqlite3
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
                "isomer-deepsci-experiment",
                "--producer",
                "isomer-deepsci-experiment",
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

    def test_topic_actor_metadata_is_stored_and_queryable_without_team_refs(self) -> None:
        root = self.make_project()
        status, created = self.run_records(
            root,
            [
                "create",
                "--record-kind",
                "artifact",
                "--id",
                "artifact-actor-note",
                "--placeholder",
                "<ACTOR_NOTE>",
                "--topic-actor",
                "operator",
                "--actor-kind",
                "operator",
                "--runtime-kind",
                "codex",
                "--controller-kind",
                "project_operator_session",
                "--body",
                "actor note",
            ],
        )
        self.assertEqual(0, status, created)
        record = created["record"]
        assert isinstance(record, dict)
        metadata = record["transition_metadata"]
        assert isinstance(metadata, dict)
        self.assertEqual("operator", metadata["topic_actor_name"])
        self.assertEqual("codex", metadata["runtime_kind"])
        lifecycle_refs = record["lifecycle_refs"]
        assert isinstance(lifecycle_refs, dict)
        self.assertEqual("operator", lifecycle_refs["topic_actor_name"])
        self.assertNotIn("agent_instance_id", lifecycle_refs)
        self.assertNotIn("agent_team_instance_id", lifecycle_refs)

        status, listed = self.run_records(root, ["list", "--topic-actor", "operator", "--runtime-kind", "codex"])
        self.assertEqual(0, status, listed)
        self.assertEqual(1, listed["count"])

    def test_structured_payload_create_show_list_and_update(self) -> None:
        root = self.make_project()
        profile_ref = canonical_record_format_ref("run.main-run-record", "profile")
        payload_file = root / "main-run-payload.json"
        payload_file.write_text('{"title":"Main run","summary":"initial"}', encoding="utf-8")
        status, validated = self.run_records(
            root,
            [
                "validate",
                "--format-profile",
                profile_ref,
                "--payload-file",
                str(payload_file),
            ],
        )
        self.assertEqual(0, status, validated)
        self.assertEqual("valid", validated["validation"]["status"])

        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "artifact-structured-main-run",
                "--record-kind",
                "artifact",
                "--placeholder",
                "<MAIN_RUN_RECORD>",
                "--format-profile",
                profile_ref,
                "--payload-file",
                str(payload_file),
            ],
        )
        self.assertEqual(0, status, created)
        record = created["record"]
        assert isinstance(record, dict)
        structured = created["structured_payload"]
        assert isinstance(structured, dict)
        self.assertEqual("valid", structured["validation_status"])
        self.assertEqual("not_requested", structured["render_status"])
        self.assertEqual(profile_ref, structured["format_profile_ref"])
        self.assertEqual("application/json", structured["payload_media_type"])
        payload_path = Path(str(structured["payload_file_path"]))
        self.assertTrue(payload_path.exists())
        self.assertEqual("payload.json", payload_path.name)
        self.assertIn("records/artifacts/research-records/artifact/artifact-structured-main-run/payload.json", payload_path.as_posix())
        self.assertEqual({"summary": "initial", "title": "Main run"}, json.loads(payload_path.read_text(encoding="utf-8")))
        manifest_path = Path(str(structured["payload_manifest_path"]))
        self.assertTrue(manifest_path.exists())
        self.assertEqual(str(payload_path), record["content_path"])
        self.assertNotIn("rendered_markdown_path", structured)
        db_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(db_path) as connection:
            stored_payload_json = connection.execute(
                "SELECT payload_json FROM structured_research_payloads WHERE record_id = ?",
                ("artifact-structured-main-run",),
            ).fetchone()[0]
        self.assertEqual("{}", stored_payload_json)

        status, shown = self.run_records(
            root,
            [
                "show",
                "artifact-structured-main-run",
                "--include-payload",
            ],
        )
        self.assertEqual(0, status, shown)
        shown_payload = shown["structured_payload"]
        assert isinstance(shown_payload, dict)
        self.assertEqual({"summary": "initial", "title": "Main run"}, shown_payload["payload"])
        self.assertEqual(str(payload_path), shown_payload["payload_file_path"])

        status, rendered = self.run_records(root, ["render", "artifact-structured-main-run"])
        self.assertEqual(0, status, rendered)
        self.assertEqual(False, rendered["mutated"])
        render = rendered["render"]
        assert isinstance(render, dict)
        self.assertIn("Main run", render["content"])
        self.assertIsNone(rendered["output_file"])

        export_path = root / "explicit-export.md"
        status, exported_render = self.run_records(
            root,
            ["render", "artifact-structured-main-run", "--output-file", str(export_path)],
        )
        self.assertEqual(0, status, exported_render)
        self.assertEqual(True, exported_render["mutated"])
        self.assertTrue(export_path.exists())
        self.assertIn("Main run", export_path.read_text(encoding="utf-8"))
        self.assertEqual(str(export_path), exported_render["output_file"])
        self.assertIsNotNone(exported_render["output_digest"])
        exported_record = exported_render["record"]
        assert isinstance(exported_record, dict)
        exported_metadata = exported_record["transition_metadata"]
        assert isinstance(exported_metadata, dict)
        generated_exports = exported_metadata["generated_exports"]
        assert isinstance(generated_exports, list)
        self.assertEqual("generated_markdown_export", generated_exports[-1]["file_role"])
        self.assertEqual(str(export_path), generated_exports[-1]["path"])

        status, listed = self.run_records(root, ["list", "--format-profile", profile_ref, "--limit", "5"])
        self.assertEqual(0, status, listed)
        self.assertEqual(1, listed["count"])
        listed_record = listed["records"][0]
        assert isinstance(listed_record, dict)
        listed_structured = listed_record["structured_payload"]
        assert isinstance(listed_structured, dict)
        self.assertNotIn("payload", listed_structured)

        payload_file.write_text('{"title":"Main run","summary":"updated"}', encoding="utf-8")
        status, updated = self.run_records(
            root,
            [
                "update",
                "artifact-structured-main-run",
                "--record-kind",
                "artifact",
                "--status",
                "complete",
                "--placeholder",
                "<MAIN_RUN_RECORD>",
                "--format-profile",
                profile_ref,
                "--payload-file",
                str(payload_file),
            ],
        )
        self.assertEqual(0, status, updated)
        updated_record = updated["record"]
        assert isinstance(updated_record, dict)
        self.assertEqual("artifact-structured-main-run", updated_record["id"])
        self.assertEqual("complete", updated_record["status"])
        updated_structured = updated["structured_payload"]
        assert isinstance(updated_structured, dict)
        updated_payload_path = Path(str(updated_structured["payload_file_path"]))
        self.assertEqual(payload_path, updated_payload_path)
        self.assertEqual({"summary": "updated", "title": "Main run"}, json.loads(updated_payload_path.read_text(encoding="utf-8")))

    def test_query_index_refresh_query_validate_and_cleanup_preview(self) -> None:
        root = self.make_project()
        workspace = root / "topic-workspaces" / "alpha"
        output_file = workspace / "outputs" / "metrics.json"
        output_file.parent.mkdir(parents=True)
        output_file.write_text('{"runtime_ms": 12.5}', encoding="utf-8")
        status, target = self.run_records(
            root,
            [
                "create",
                "--id",
                "input-record",
                "--record-kind",
                "artifact",
                "--body",
                "input",
            ],
        )
        self.assertEqual(0, status, target)
        profile_ref = canonical_record_format_ref("run.main-run-record", "profile")
        payload_file = root / "indexed-payload.json"
        payload_file.write_text(
            json.dumps(
                {
                    "title": "Indexed main run",
                    "summary": "Query index payload",
                    "tags": ["host", "gpu", "runtime"],
                    "sections": {
                        "metrics": {"runtime_ms": 12.5},
                        "claims": [
                            {
                                "claim": "Runtime is predictable",
                                "metric_key": "runtime_ms",
                                "observed_value": 12.5,
                                "expected": "stable",
                                "verdict": "supported",
                            }
                        ],
                        "raw_ideas": [{"idea_id": "idea-1", "one_liner": "Model host runtime path"}],
                        "decision": {
                            "decision": "continue",
                            "next_route": "analysis",
                            "reason": "metrics stable",
                            "selected_hypothesis_id": "idea-1",
                        },
                        "artifact_list": [{"path": "outputs/metrics.json", "file_role": "raw_results"}],
                        "unresolved_artifacts": [{"path": "validation_metrics.json"}],
                    },
                    "semantic_path_inventory": [
                        {
                            "path": str(workspace / "records" / "artifacts" / "missing"),
                            "path_kind": "directory",
                            "semantic_label": "topic.records.artifacts",
                        }
                    ],
                    "evidence_refs": ["input-record"],
                }
            ),
            encoding="utf-8",
        )
        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "indexed-main-run",
                "--record-kind",
                "run",
                "--format-profile",
                profile_ref,
                "--payload-file",
                str(payload_file),
                "--relationships-json",
                '[{"target_record_id":"input-record","relation_kind":"uses_input","relation_role":"baseline"}]',
                "--files-json",
                '[{"path":"outputs/metrics.json","file_role":"raw_results","semantic_label":"topic.records.runs"}]',
            ],
        )
        self.assertEqual(0, status, created)
        self.assertEqual(True, created["query_index"]["ok"])
        created_structured = created["structured_payload"]
        assert isinstance(created_structured, dict)
        indexed_payload_path = Path(str(created_structured["payload_file_path"]))
        self.assertTrue(indexed_payload_path.exists())

        status, listed = self.run_records(root, ["query", "list", "--record-kind", "run", "--facet", "metrics"])
        self.assertEqual(0, status, listed)
        self.assertEqual(1, listed["count"])
        indexed = listed["records"][0]
        self.assertEqual("indexed-main-run", indexed["record_id"])
        self.assertEqual("Indexed main run", indexed["title"])
        self.assertEqual(str(indexed_payload_path), indexed["payload_file_path"])
        self.assertEqual(created_structured["payload_digest"], indexed["payload_digest"])

        status, facets = self.run_records(root, ["query", "facets", "indexed-main-run"])
        self.assertEqual(0, status, facets)
        self.assertEqual("runtime_ms", facets["metrics"][0]["metric_key"])
        self.assertEqual("Runtime is predictable", facets["claims"][0]["claim"])
        self.assertEqual("Model host runtime path", facets["ideas"][0]["one_liner"])
        self.assertEqual("continue", facets["routes"][0]["decision"])

        status, files = self.run_records(root, ["query", "files", "indexed-main-run"])
        self.assertEqual(0, status, files)
        self.assertTrue(any(item["file_role"] == "structured_payload" and item["exists"] for item in files["files"]))
        self.assertTrue(any(item["file_role"] == "structured_payload_manifest" and item["exists"] for item in files["files"]))
        self.assertTrue(any(item["file_role"] == "raw_results" and item["exists"] and item["openable"] for item in files["files"]))
        self.assertFalse(any(item["path"] == "validation_metrics.json" for item in files["files"]))
        self.assertFalse(any(str(item["path"]).endswith("records/artifacts/missing") for item in files["files"]))

        status, lineage = self.run_records(root, ["query", "lineage", "indexed-main-run", "--direction", "downstream"])
        self.assertEqual(0, status, lineage)
        self.assertTrue(any(edge["target_record_id"] == "input-record" for edge in lineage["edges"]))

        status, exported = self.run_records(root, ["query", "export", "--view", "dashboard"])
        self.assertEqual(0, status, exported)
        self.assertTrue(any(node["record_id"] == "indexed-main-run" for node in exported["nodes"]))
        self.assertEqual({"total": 0, "by_code": []}, exported["diagnostic_summary"])

        status, rebuilt = self.run_records(root, ["index", "rebuild"])
        self.assertEqual(0, status, rebuilt)
        self.assertEqual(True, rebuilt["mutated"])

        status, validated = self.run_records(root, ["index", "validate"])
        self.assertEqual(0, status, validated)
        self.assertEqual([], validated["diagnostics"])

        status, cleanup = self.run_records(root, ["index", "cleanup", "--missing-files"])
        self.assertEqual(0, status, cleanup)
        self.assertEqual(False, cleanup["mutated"])

    def test_query_index_reports_openability_for_explicit_missing_file(self) -> None:
        root = self.make_project()
        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "record-with-missing-file",
                "--record-kind",
                "artifact",
                "--body",
                "record with missing attachment",
                "--files-json",
                '[{"path":"outputs/missing.json","file_role":"raw_results","semantic_label":"topic.records.runs"}]',
            ],
        )
        self.assertEqual(0, status, created)

        status, files = self.run_records(root, ["query", "files", "record-with-missing-file"])
        self.assertEqual(0, status, files)
        raw_results = [item for item in files["files"] if item["file_role"] == "raw_results"]
        self.assertEqual(1, len(raw_results), files)
        self.assertFalse(raw_results[0]["exists"])
        self.assertFalse(raw_results[0]["openable"])
        self.assertEqual("missing", raw_results[0]["open_blocked_reason"])

        status, exported = self.run_records(root, ["query", "export", "--view", "dashboard"])
        self.assertEqual(0, status, exported)
        self.assertTrue(
            any(item["code"] == "query_index_file_missing" and item["count"] == 1 for item in exported["diagnostic_summary"]["by_code"]),
            exported,
        )

    def test_structured_create_rejects_direct_body_source(self) -> None:
        root = self.make_project()
        profile_ref = canonical_record_format_ref("run.main-run-record", "profile")
        status, created = self.run_records(
            root,
            [
                "create",
                "--record-kind",
                "artifact",
                "--format-profile",
                profile_ref,
                "--body",
                "markdown body",
            ],
        )
        self.assertEqual(1, status, created)
        self.assertEqual("structured_payload_requires_json", created["error"]["code"])

    def test_structured_create_snapshots_plain_schema_and_template(self) -> None:
        root = self.make_project()
        schema_file = root / "schema.json"
        template_file = root / "record.md.j2"
        payload_file = root / "payload.json"
        schema_file.write_text(
            '{"type":"object","required":["title"],"properties":{"title":{"type":"string"}}}',
            encoding="utf-8",
        )
        template_file.write_text("# {{ payload.title }}\n", encoding="utf-8")
        payload_file.write_text('{"title":"Snapshot record"}', encoding="utf-8")
        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "artifact-snapshot",
                "--record-kind",
                "artifact",
                "--schema-file",
                str(schema_file),
                "--template-file",
                str(template_file),
                "--payload-file",
                str(payload_file),
                "--render",
                "markdown",
            ],
        )
        self.assertEqual(0, status, created)
        structured = created["structured_payload"]
        assert isinstance(structured, dict)
        self.assertEqual("file_snapshot", structured["schema_source_kind"])
        self.assertTrue(str(structured["schema_ref"]).startswith("custom:alpha/record-format/schema/snapshot/"))
        self.assertTrue(Path(str(structured["payload_file_path"])).exists())
        self.assertNotIn("rendered_markdown_path", structured)

    def test_structured_payload_missing_file_reports_digest_diagnostic(self) -> None:
        root = self.make_project()
        profile_ref = canonical_record_format_ref("run.main-run-record", "profile")
        payload_file = root / "missing-payload-source.json"
        payload_file.write_text('{"title":"Missing file","summary":"initial"}', encoding="utf-8")
        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "artifact-missing-payload",
                "--record-kind",
                "artifact",
                "--format-profile",
                profile_ref,
                "--payload-file",
                str(payload_file),
            ],
        )
        self.assertEqual(0, status, created)
        structured = created["structured_payload"]
        assert isinstance(structured, dict)
        Path(str(structured["payload_file_path"])).unlink()

        status, shown = self.run_records(root, ["show", "artifact-missing-payload", "--include-payload"])
        self.assertEqual(1, status, shown)
        self.assertEqual(True, shown["ok"])
        self.assertNotIn("payload", shown["structured_payload"])
        self.assertTrue(any(item["code"] == "ISO208" for item in shown["diagnostics"]))

    def test_migrate_payload_files_exports_legacy_sqlite_payload_rows(self) -> None:
        root = self.make_project()
        profile_ref = canonical_record_format_ref("run.main-run-record", "profile")
        payload_file = root / "legacy-source.json"
        payload_file.write_text('{"title":"Legacy row","summary":"from sqlite"}', encoding="utf-8")
        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "legacy-structured-row",
                "--record-kind",
                "artifact",
                "--format-profile",
                profile_ref,
                "--payload-file",
                str(payload_file),
            ],
        )
        self.assertEqual(0, status, created)
        structured = created["structured_payload"]
        assert isinstance(structured, dict)
        original_payload_path = Path(str(structured["payload_file_path"]))
        original_manifest_path = Path(str(structured["payload_manifest_path"]))
        original_payload_path.unlink()
        original_manifest_path.unlink()
        legacy_markdown = root / "legacy-rendered.md"
        legacy_markdown.write_text("# Legacy rendered view\n", encoding="utf-8")
        db_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(db_path) as connection:
            connection.execute(
                """
                UPDATE structured_research_payloads
                SET payload_json = ?,
                    payload_file_path = NULL,
                    payload_manifest_path = NULL,
                    rendered_markdown_path = ?,
                    rendered_markdown_digest = ?
                WHERE record_id = ?
                """,
                (
                    json.dumps({"summary": "from sqlite", "title": "Legacy row"}, sort_keys=True),
                    str(legacy_markdown),
                    "legacy-digest",
                    "legacy-structured-row",
                ),
            )
            connection.execute(
                "UPDATE lifecycle_records SET content_path = ? WHERE id = ?",
                (str(legacy_markdown), "legacy-structured-row"),
            )

        status, migrated = self.run_records(root, ["migrate-payload-files"])
        self.assertEqual(0, status, migrated)
        self.assertEqual(True, migrated["mutated"])
        self.assertEqual(1, migrated["migrated_count"])
        migrated_item = migrated["migrated"][0]
        migrated_payload_path = Path(str(migrated_item["payload_file_path"]))
        self.assertTrue(migrated_payload_path.exists())
        self.assertEqual({"summary": "from sqlite", "title": "Legacy row"}, json.loads(migrated_payload_path.read_text(encoding="utf-8")))

        status, shown = self.run_records(root, ["show", "legacy-structured-row", "--include-payload"])
        self.assertEqual(0, status, shown)
        shown_structured = shown["structured_payload"]
        assert isinstance(shown_structured, dict)
        self.assertEqual({"summary": "from sqlite", "title": "Legacy row"}, shown_structured["payload"])
        self.assertEqual(str(legacy_markdown), shown_structured["legacy_rendered_markdown_path"])
        self.assertNotIn("rendered_markdown_path", shown_structured)
        with sqlite3.connect(db_path) as connection:
            migrated_payload_json = connection.execute(
                "SELECT payload_json FROM structured_research_payloads WHERE record_id = ?",
                ("legacy-structured-row",),
            ).fetchone()[0]
        self.assertEqual("{}", migrated_payload_json)

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
