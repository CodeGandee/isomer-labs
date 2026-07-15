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
from isomer_labs.records.idea_sources import (
    SOURCE_STATUS_BROAD_PATH,
    SOURCE_STATUS_EXACT,
    SOURCE_STATUS_NON_OBJECT,
    extract_json_path,
    resolve_payload_source_fragment,
)


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

    def run_ideas(self, root: Path, args: list[str]) -> tuple[int, dict[str, object]]:
        status, output = self.run_main(["ext", "research", "ideas", *args, "--project", str(root), "--topic", "alpha"], cwd=root)
        return status, json.loads(output)

    def test_idea_source_fragment_resolver_uses_bounded_paths_and_requires_objects(self) -> None:
        payload = {"sections": {"raw_ideas": [{"id": "R1", "title": "Idea one", "summary": "First idea summary"}], "filter_notes": ["not idea"]}}

        value, unresolved = extract_json_path(payload, "$.sections.raw_ideas[0]")
        self.assertFalse(unresolved)
        self.assertEqual({"id": "R1", "title": "Idea one", "summary": "First idea summary"}, value)

        exact = resolve_payload_source_fragment(payload, "$.sections.raw_ideas[0]", format_profile_ref=canonical_record_format_ref("report.raw-idea-slate", "profile"))
        self.assertEqual(SOURCE_STATUS_EXACT, exact.status)
        self.assertEqual({"id": "R1", "title": "Idea one", "summary": "First idea summary"}, exact.source_json)

        broad = resolve_payload_source_fragment(payload, "$.sections.raw_ideas", format_profile_ref=canonical_record_format_ref("report.raw-idea-slate", "profile"))
        self.assertEqual(SOURCE_STATUS_NON_OBJECT, broad.status)

        context = resolve_payload_source_fragment(payload, "$.sections.filter_notes", format_profile_ref=canonical_record_format_ref("report.raw-idea-slate", "profile"))
        self.assertEqual(SOURCE_STATUS_BROAD_PATH, context.status)

    def test_record_crud_preserves_semantic_identity_and_body(self) -> None:
        root = self.make_project()
        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "artifact-main-run",
                "--record-kind",
                "artifact",
                "--semantic-id",
                "DEEPSCI:MAIN-RUN-RECORD",
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
        self.assertEqual("DEEPSCI:MAIN-RUN-RECORD", metadata["semantic_id"])
        self.assertNotIn("placeholder", metadata)
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
                "--semantic-id",
                "DEEPSCI:MAIN-RUN-RECORD",
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
                "--semantic-id",
                "DEEPSCI:MAIN-RUN-RECORD",
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

    def test_semantic_id_lifecycle_neutral_profile_and_latest_queries(self) -> None:
        root = self.make_project()
        profile_ref = "isomer:research/record-format/profile/kaoju/contract/survey-contract/v1"

        def payload(path: Path, summary: str) -> None:
            path.write_text(
                json.dumps(
                    {
                        "title": "Survey Contract",
                        "summary": summary,
                        "artifact_family": "kaoju",
                        "semantic_id": "KAOJU:SURVEY-CONTRACT",
                        "artifact_type": "survey-contract",
                        "procedure": "survey-field",
                        "sections": {"scope": {"question": "What methods exist?"}},
                    }
                ),
                encoding="utf-8",
            )

        first_payload = root / "survey-contract.json"
        payload(first_payload, "Initial bounded survey scope.")
        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "survey-contract-1",
                "--record-kind",
                "artifact",
                "--semantic-id",
                "KAOJU:SURVEY-CONTRACT",
                "--format-profile",
                profile_ref,
                "--skill",
                "isomer-kaoju-frame",
                "--payload-file",
                str(first_payload),
            ],
        )
        self.assertEqual(0, status, created)
        metadata = created["record"]["transition_metadata"]
        self.assertEqual("KAOJU:SURVEY-CONTRACT", metadata["semantic_id"])
        self.assertEqual("KAOJU:SURVEY-CONTRACT", created["query_index"]["counts"] and metadata["semantic_id"])

        status, shown = self.run_records(root, ["show", "survey-contract-1", "--include-payload"])
        self.assertEqual(0, status, shown)
        self.assertEqual("KAOJU:SURVEY-CONTRACT", shown["structured_payload"]["payload"]["semantic_id"])
        status, listed = self.run_records(root, ["list", "--semantic-id", "KAOJU:SURVEY-CONTRACT"])
        self.assertEqual(0, status, listed)
        self.assertEqual(["survey-contract-1"], [record["id"] for record in listed["records"]])

        status, updated = self.run_records(
            root,
            ["update", "survey-contract-1", "--record-kind", "artifact", "--semantic-id", "KAOJU:SURVEY-CONTRACT", "--status", "complete"],
        )
        self.assertEqual(0, status, updated)
        self.assertEqual("KAOJU:SURVEY-CONTRACT", updated["record"]["transition_metadata"]["semantic_id"])

        revised_payload = root / "survey-contract-revised.json"
        payload(revised_payload, "Revised bounded survey scope.")
        status, revised = self.run_records(
            root,
            ["revise", "survey-contract-1", "--id", "survey-contract-2", "--payload-file", str(revised_payload)],
        )
        self.assertEqual(0, status, revised)
        self.assertEqual("KAOJU:SURVEY-CONTRACT", revised["record"]["transition_metadata"]["semantic_id"])
        self.assertEqual("survey-contract-1", revised["revision_of_record_id"])

        status, latest = self.run_records(
            root,
            ["query", "list", "--artifact-family", "kaoju", "--semantic-id", "KAOJU:SURVEY-CONTRACT", "--procedure", "survey-field", "--latest-only"],
        )
        self.assertEqual(0, status, latest)
        self.assertEqual(["survey-contract-2"], [record["record_id"] for record in latest["records"]])
        self.assertEqual([], latest["diagnostics"])

        status, competing = self.run_records(
            root,
            [
                "create",
                "--id",
                "survey-contract-competing",
                "--record-kind",
                "artifact",
                "--semantic-id",
                "KAOJU:SURVEY-CONTRACT",
                "--format-profile",
                profile_ref,
                "--payload-file",
                str(first_payload),
            ],
        )
        self.assertEqual(0, status, competing)
        status, ambiguous = self.run_records(
            root,
            ["query", "list", "--artifact-family", "kaoju", "--semantic-id", "KAOJU:SURVEY-CONTRACT", "--latest-only"],
        )
        self.assertEqual(0, status, ambiguous)
        self.assertEqual({"survey-contract-2", "survey-contract-competing"}, {record["record_id"] for record in ambiguous["records"]})
        self.assertEqual("query_index_latest_ambiguous", ambiguous["diagnostics"][0]["code"])

        status, facets = self.run_records(root, ["query", "facets", "survey-contract-2", "--facet", "facts"])
        self.assertEqual(0, status, facets)
        self.assertTrue(
            any(
                fact["json_path"] == "$.procedure"
                and fact["metadata"].get("profile_ref") == profile_ref
                for fact in facets["facts"]
            ),
            facets,
        )

        status, archived = self.run_records(root, ["delete", "survey-contract-1", "--reason", "superseded"])
        self.assertEqual(0, status, archived)
        self.assertEqual("archived", archived["record"]["status"])
        status, _ = self.run_records(root, ["delete", "survey-contract-competing", "--reason", "not selected"])
        self.assertEqual(0, status)

        mismatch_payload = root / "survey-contract-mismatch.json"
        payload(mismatch_payload, "Mismatched request identity.")
        status, mismatch = self.run_records(
            root,
            ["create", "--record-kind", "artifact", "--semantic-id", "KAOJU:FIELD-SUMMARY", "--format-profile", profile_ref, "--payload-file", str(mismatch_payload)],
        )
        self.assertEqual(1, status)
        self.assertTrue(any(item["code"] == "semantic_id_payload_mismatch" for item in mismatch["diagnostics"]))

        status, kind_mismatch = self.run_records(
            root,
            ["create", "--record-kind", "evidence_item", "--semantic-id", "KAOJU:SURVEY-CONTRACT", "--format-profile", profile_ref, "--payload-file", str(first_payload)],
        )
        self.assertEqual(1, status)
        self.assertTrue(any(item["code"] == "record_kind_profile_mismatch" for item in kind_mismatch["diagnostics"]))

        status, invalid = self.run_records(root, ["list", "--semantic-id", "not-valid"])
        self.assertEqual(1, status)
        self.assertEqual("invalid_artifact_identity", invalid["error"]["code"])

        status, wrong_owner = self.run_records(
            root,
            [
                "create",
                "--record-kind",
                "artifact",
                "--semantic-id",
                "KAOJU:SURVEY-CONTRACT",
                "--skill",
                "isomer-deepsci-experiment",
                "--body",
                "wrong owner",
            ],
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_identity_extension_mismatch", wrong_owner["error"]["code"])
        self.assertEqual("DEEPSCI", wrong_owner["expected_namespace"])
        self.assertNotIn("canonical_recovery", wrong_owner)

    def test_old_identity_forms_are_rejected_and_never_derived_during_indexing(self) -> None:
        root = self.make_project()
        status, rejected = self.run_main(
            [
                "ext",
                "research",
                "records",
                "create",
                "--id",
                "legacy-placeholder",
                "--record-kind",
                "artifact",
                "--placeholder",
                "<MAIN_RUN_RECORD>",
                "--body",
                "legacy",
                "--project",
                str(root),
                "--topic",
                "alpha",
            ],
            cwd=root,
        )
        self.assertNotEqual(0, status)
        self.assertIn("--placeholder", rejected)

        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "legacy-placeholder",
                "--record-kind",
                "artifact",
                "--semantic-id",
                "DEEPSCI:MAIN-RUN-RECORD",
                "--skill",
                "isomer-deepsci-experiment",
                "--body",
                "legacy",
            ],
        )
        self.assertEqual(0, status, created)
        db_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(db_path) as connection:
            raw_metadata = connection.execute(
                "SELECT transition_metadata_json FROM lifecycle_records WHERE id = ?",
                ("legacy-placeholder",),
            ).fetchone()[0]
            legacy_metadata = json.loads(raw_metadata)
            legacy_metadata.pop("semantic_id")
            legacy_metadata["placeholder"] = "<DEEPSCI:MAIN-RUN-RECORD>"
            connection.execute(
                "UPDATE lifecycle_records SET transition_metadata_json = ? WHERE id = ?",
                (json.dumps(legacy_metadata, sort_keys=True), "legacy-placeholder"),
            )
        status, rebuilt = self.run_records(root, ["index", "rebuild", "--record-id", "legacy-placeholder"])
        self.assertEqual(0, status, rebuilt)
        status, listed = self.run_records(root, ["query", "list", "--semantic-id", "DEEPSCI:MAIN-RUN-RECORD"])
        self.assertEqual(0, status, listed)
        self.assertEqual(0, listed["count"])

        status, unfiltered = self.run_records(root, ["query", "list"])
        self.assertEqual(0, status, unfiltered)
        indexed = next(record for record in unfiltered["records"] if record["record_id"] == "legacy-placeholder")
        self.assertIsNone(indexed["semantic_id"])
        self.assertIsNone(indexed["semantic_id_source"])
        self.assertNotIn("placeholder", indexed)

        status, lowercase = self.run_records(root, ["list", "--semantic-id", "deepsci:main-run-record"])
        self.assertEqual(1, status)
        self.assertEqual("invalid_artifact_identity", lowercase["error"]["code"])
        self.assertNotIn("canonical_recovery", lowercase)

    def test_structured_record_v1_profile_is_rejected_for_new_writes(self) -> None:
        root = self.make_project()
        payload_file = root / "legacy-v1-payload.json"
        payload_file.write_text(json.dumps({"title": "Legacy v1 payload", "summary": "Valid display fields but unsupported profile."}), encoding="utf-8")
        v1_profile = canonical_record_format_ref("report.raw-idea-slate", "profile", version="v1")

        status, payload = self.run_records(
            root,
            [
                "create",
                "--id",
                "legacy-v1-write",
                "--record-kind",
                "artifact",
                "--format-profile",
                v1_profile,
                "--payload-file",
                str(payload_file),
            ],
        )

        self.assertEqual(1, status, payload)
        self.assertFalse(payload["ok"])
        self.assertEqual("diagnostics_failed", payload["error"]["code"])
        self.assertTrue(any(item["code"] == "structured_record_v1_unsupported" for item in payload["diagnostics"]))

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
                "--semantic-id",
                "DEEPSCI:MAIN-RUN-RECORD",
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
                "--semantic-id",
                "DEEPSCI:ACTOR-NOTE",
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
                "--semantic-id",
                "DEEPSCI:MAIN-RUN-RECORD",
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
                "--semantic-id",
                "DEEPSCI:MAIN-RUN-RECORD",
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
                        "raw_ideas": [{"idea_id": "idea-1", "title": "Model host runtime path", "summary": "Model host runtime path as a candidate idea."}],
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
        self.assertEqual([], facets["ideas"])
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

    def test_canonical_lineage_create_revise_query_siblings_and_cycle_rejection(self) -> None:
        root = self.make_project()
        for record_id in ("parent-a", "parent-b"):
            status, created = self.run_records(
                root,
                [
                    "create",
                    "--id",
                    record_id,
                    "--record-kind",
                    "artifact",
                    "--body",
                    record_id,
                ],
            )
            self.assertEqual(0, status, created)

        parent_refs = json.dumps(
            [
                {"record_id": "parent-a", "role": "board"},
                {"record_id": "parent-b", "role": "survey"},
            ]
        )
        for child_id in ("candidate-one", "candidate-two"):
            status, created = self.run_records(
                root,
                [
                    "create",
                    "--id",
                    child_id,
                    "--record-kind",
                    "artifact",
                    "--body",
                    child_id,
                    "--parents-json",
                    parent_refs,
                    "--lineage-kind",
                    "selected_from",
                    "--generation-id",
                    "idea-pass-1",
                    "--generation-purpose",
                    "test candidate siblings",
                    "--decision-record-id",
                    "decision-alpha",
                ],
            )
            self.assertEqual(0, status, created)
            self.assertEqual(2, len(created["lineage"]["edges"]))
            generation_group = created["lineage"]["generation_group"]
            assert isinstance(generation_group, dict)
            self.assertEqual("idea-pass-1", generation_group["id"])

        status, upstream = self.run_records(root, ["query", "lineage", "candidate-one", "--direction", "upstream"])
        self.assertEqual(0, status, upstream)
        self.assertEqual("canonical", upstream["lineage_source"])
        self.assertEqual(
            {"parent-a", "parent-b"},
            {edge["parent_record_id"] for edge in upstream["edges"]},
        )

        status, downstream = self.run_records(root, ["query", "lineage", "parent-a", "--direction", "downstream"])
        self.assertEqual(0, status, downstream)
        self.assertEqual({"candidate-one", "candidate-two"}, {edge["child_record_id"] for edge in downstream["edges"]})

        status, siblings = self.run_records(root, ["query", "siblings", "candidate-one"])
        self.assertEqual(0, status, siblings)
        self.assertEqual(["candidate-two"], [node["record_id"] for node in siblings["nodes"]])
        self.assertEqual(2, len(siblings["edges"]))

        status, exported = self.run_records(root, ["query", "export", "--view", "graph"])
        self.assertEqual(0, status, exported)
        self.assertTrue(
            any(
                edge["source_classification"] == "canonical-lineage"
                and edge["source_record_id"] == "parent-a"
                and edge["target_record_id"] == "candidate-one"
                for edge in exported["edges"]
            ),
            exported["edges"],
        )

        status, cycle = self.run_records(
            root,
            [
                "lineage",
                "add",
                "candidate-one",
                "parent-a",
                "--lineage-kind",
                "derived_from",
            ],
        )
        self.assertEqual(1, status, cycle)
        self.assertEqual("lineage_validation_failed", cycle["error"]["code"])
        self.assertTrue(any(item["code"] == "lineage_cycle" for item in cycle["diagnostics"]))

        status, revised = self.run_records(
            root,
            [
                "revise",
                "candidate-one",
                "--id",
                "candidate-one-rev",
                "--body",
                "revised candidate",
            ],
        )
        self.assertEqual(0, status, revised)
        self.assertEqual("revise", revised["operation"])
        self.assertEqual("candidate-one", revised["revision_of_record_id"])

        status, revised_lineage = self.run_records(root, ["query", "lineage", "candidate-one-rev", "--direction", "upstream"])
        self.assertEqual(0, status, revised_lineage)
        self.assertTrue(
            any(edge["lineage_kind"] == "revision_of" and edge["parent_record_id"] == "candidate-one" for edge in revised_lineage["edges"]),
            revised_lineage,
        )

        status, validated = self.run_records(root, ["lineage", "validate"])
        self.assertEqual(0, status, validated)
        self.assertEqual([], validated["diagnostics"])

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
        payload_file.write_text('{"title":"Snapshot record","summary":"Snapshot record summary."}', encoding="utf-8")
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

    def test_research_ideas_cli_records_canonical_graph_and_rejects_revision_edges(self) -> None:
        root = self.make_project()
        for record_id in ("record-parent", "record-child"):
            status, created = self.run_records(
                root,
                ["create", "--id", record_id, "--record-kind", "artifact", "--body", record_id],
            )
            self.assertEqual(0, status, created)

        status, parent = self.run_ideas(
            root,
            [
                "upsert",
                "--idea-id",
                "idea-parent",
                "--title",
                "Parent idea",
                "--summary",
                "Parent idea summary.",
                "--status",
                "candidate",
                "--alias",
                "R1",
                "--source-record-id",
                "record-parent",
            ],
        )
        self.assertEqual(0, status, parent)
        self.assertEqual("idea-parent", parent["idea"]["idea_id"])

        status, child = self.run_ideas(
            root,
            [
                "upsert",
                "--idea-id",
                "idea-child",
                "--title",
                "Child idea",
                "--summary",
                "Child idea summary.",
                "--status",
                "selected",
                "--alias",
                "C1",
                "--source-record-id",
                "record-child",
            ],
        )
        self.assertEqual(0, status, child)

        status, realization = self.run_ideas(root, ["realize", "--idea-id", "idea-child", "--record-id", "record-child", "--realization-stage", "selected-hypothesis"])
        self.assertEqual(0, status, realization)
        self.assertEqual("record-child", realization["realization"]["record_id"])

        status, group = self.run_ideas(root, ["generation", "upsert", "--generation-id", "idea-pass-1", "--parent-idea-id", "idea-parent", "--purpose", "test candidates"])
        self.assertEqual(0, status, group)

        status, edge = self.run_ideas(
            root,
            [
                "lineage",
                "add",
                "idea-parent",
                "idea-child",
                "--lineage-kind",
                "subsumes",
                "--generation-id",
                "idea-pass-1",
                "--rationale",
                "Child covers the parent as a test role.",
            ],
        )
        self.assertEqual(0, status, edge)
        self.assertEqual("subsumes", edge["edge"]["lineage_kind"])

        status, bad_edge = self.run_ideas(root, ["lineage", "add", "idea-parent", "idea-child", "--lineage-kind", "revision_of"])
        self.assertEqual(1, status, bad_edge)
        self.assertEqual("idea_lineage_validation_failed", bad_edge["error"]["code"])
        self.assertTrue(any(item["code"] == "idea_revision_edge_rejected" for item in bad_edge["diagnostics"]))

        status, exported = self.run_records(root, ["query", "export", "--view", "graph"])
        self.assertEqual(0, status, exported)
        self.assertEqual(["idea-child", "idea-parent"], sorted(row["idea_id"] for row in exported["canonical_ideas"]))
        self.assertEqual(["subsumes"], [row["lineage_kind"] for row in exported["canonical_idea_edges"]])

        status, graph = self.run_ideas(root, ["graph"])
        self.assertEqual(0, status, graph)
        self.assertEqual("canonical", graph["graph_source"])
        self.assertEqual(["idea-child", "idea-parent"], sorted(row["idea_id"] for row in graph["nodes"]))
        self.assertEqual(["subsumes"], [row["lineage_kind"] for row in graph["edges"]])

    def test_research_idea_display_keys_are_stable_and_explicitly_repaired(self) -> None:
        root = self.make_project()
        status, first = self.run_ideas(root, ["upsert", "--idea-id", "idea-one", "--title", "Idea One", "--summary", "Idea One summary."])
        self.assertEqual(0, status, first)
        self.assertEqual("I-1", first["idea"]["display_key"])

        status, second = self.run_ideas(root, ["upsert", "--idea-id", "idea-two", "--title", "Idea Two", "--summary", "Idea Two summary."])
        self.assertEqual(0, status, second)
        self.assertEqual("I-2", second["idea"]["display_key"])

        db_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(db_path) as connection:
            connection.execute("UPDATE research_ideas SET display_key = NULL WHERE idea_id = ?", ("idea-one",))

        status, validate = self.run_ideas(root, ["validate"])
        self.assertEqual(0, status, validate)
        self.assertTrue(any(item["code"] == "idea_display_key_missing" and item["idea_id"] == "idea-one" for item in validate["diagnostics"]))

        status, repair_plan = self.run_ideas(root, ["repair"])
        self.assertEqual(0, status, repair_plan)
        display_key_actions = [item for item in repair_plan["plan"] if item["action"] == "assign_display_key"]
        self.assertEqual([{"action": "assign_display_key", "idea_id": "idea-one", "display_key": "I-3", "visibility": "primary", "status": "candidate"}], display_key_actions)

        status, repair = self.run_ideas(root, ["repair", "--apply"])
        self.assertEqual(0, status, repair)
        self.assertIn({"idea_id": "idea-one", "display_key": "I-3"}, repair["applied"])

        with sqlite3.connect(db_path) as connection:
            connection.execute("UPDATE research_ideas SET display_key = ? WHERE idea_id = ?", ("I2", "idea-two"))

        status, validate_old = self.run_ideas(root, ["validate"])
        self.assertEqual(1, status, validate_old)
        self.assertTrue(any(item["code"] == "idea_display_key_invalid" and item["display_key"] == "I2" for item in validate_old["diagnostics"]))

        status, migrate_plan = self.run_ideas(root, ["repair"])
        self.assertEqual(1, status, migrate_plan)
        migrate_actions = [item for item in migrate_plan["plan"] if item["action"] == "migrate_display_key"]
        self.assertEqual(
            [
                {
                    "action": "migrate_display_key",
                    "idea_id": "idea-two",
                    "previous_display_key": "I2",
                    "display_key": "I-2",
                    "visibility": "primary",
                    "status": "candidate",
                    "diagnostics": [],
                }
            ],
            migrate_actions,
        )

        status, migrated = self.run_ideas(root, ["repair", "--apply"])
        self.assertEqual(0, status, migrated)
        self.assertIn({"idea_id": "idea-two", "display_key": "I-2", "previous_display_key": "I2"}, migrated["applied"])

        status, query = self.run_ideas(root, ["query"])
        self.assertEqual(0, status, query)
        display_keys = {item["idea_id"]: item["display_key"] for item in query["ideas"]}
        self.assertEqual({"idea-one": "I-3", "idea-two": "I-2"}, display_keys)

    def test_research_idea_display_key_migration_rejects_collisions(self) -> None:
        root = self.make_project()
        status, first = self.run_ideas(root, ["upsert", "--idea-id", "idea-one", "--title", "Idea One", "--summary", "Idea One summary."])
        self.assertEqual(0, status, first)
        status, second = self.run_ideas(root, ["upsert", "--idea-id", "idea-two", "--title", "Idea Two", "--summary", "Idea Two summary."])
        self.assertEqual(0, status, second)

        db_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(db_path) as connection:
            connection.execute("UPDATE research_ideas SET display_key = ? WHERE idea_id = ?", ("I1", "idea-one"))
            connection.execute("UPDATE research_ideas SET display_key = ? WHERE idea_id = ?", ("I-1", "idea-two"))

        status, repair_plan = self.run_ideas(root, ["repair"])
        self.assertEqual(1, status, repair_plan)
        migrate_actions = [item for item in repair_plan["plan"] if item["action"] == "migrate_display_key"]
        self.assertEqual(1, len(migrate_actions))
        self.assertEqual("I-1", migrate_actions[0]["display_key"])
        self.assertTrue(any(item["code"] == "idea_display_key_migration_collision" for item in migrate_actions[0]["diagnostics"]))

        status, repair = self.run_ideas(root, ["repair", "--apply"])
        self.assertEqual(1, status, repair)
        self.assertFalse(repair["mutated"])
        self.assertEqual("idea_repair_plan_blocked", repair["error"]["code"])

        with sqlite3.connect(db_path) as connection:
            row = connection.execute("SELECT display_key FROM research_ideas WHERE idea_id = ?", ("idea-one",)).fetchone()
        self.assertEqual("I1", row[0])

    def test_research_idea_source_contract_validates_imports_exports_and_repairs(self) -> None:
        root = self.make_project()
        profile_ref = canonical_record_format_ref("report.raw-idea-slate", "profile")
        payload_path = root / "raw-idea-slate.json"
        write(
            payload_path,
            """
            {
              "title": "Raw Idea Slate",
              "summary": "Two raw model ideas ready for import.",
              "sections": {
                "filter_notes": ["R2 deferred; not an idea entry."],
                "raw_ideas": [
                  {"id": "R1", "title": "Occupancy correction", "summary": "Add occupancy correction.", "family": "model"},
                  {"id": "R2", "title": "Symbolic regression fallback", "summary": "Add symbolic regression fallback.", "family": "model", "status": "deferred"}
                ]
              }
            }
            """,
        )
        status, created = self.run_records(
            root,
            [
                "create",
                "--id",
                "raw-record",
                "--record-kind",
                "artifact",
                "--format-profile",
                profile_ref,
                "--payload-file",
                str(payload_path),
            ],
        )
        self.assertEqual(0, status, created)

        status, imported = self.run_ideas(root, ["import-from-record", "raw-record"])
        self.assertEqual(0, status, imported)
        self.assertEqual(["$.sections.raw_ideas[0]", "$.sections.raw_ideas[1]"], [item["source_json_path"] for item in imported["plan"]])

        status, idea = self.run_ideas(root, ["upsert", "--idea-id", "idea-occupancy", "--title", "Occupancy", "--summary", "Add occupancy correction.", "--alias", "R1", "--source-record-id", "raw-record"])
        self.assertEqual(0, status, idea)
        status, realization = self.run_ideas(root, ["realize", "--idea-id", "idea-occupancy", "--record-id", "raw-record", "--source-json-path", "$.sections.raw_ideas[0]"])
        self.assertEqual(0, status, realization)

        status, bad_idea = self.run_ideas(root, ["upsert", "--idea-id", "idea-bad", "--title", "Bad", "--summary", "Bad source path test.", "--alias", "R1", "--source-record-id", "raw-record"])
        self.assertEqual(0, status, bad_idea)
        status, bad_realization = self.run_ideas(root, ["realize", "--idea-id", "idea-bad", "--record-id", "raw-record", "--source-json-path", "$.sections.raw_ideas"])
        self.assertEqual(1, status, bad_realization)
        self.assertEqual("idea_realization_validation_failed", bad_realization["error"]["code"])
        self.assertTrue(any(item["code"] == "source_json_fragment_non_object" for item in bad_realization["diagnostics"]))

        status, exported = self.run_records(root, ["query", "export", "--view", "ideas"])
        self.assertEqual(0, status, exported)
        realization_rows = [row for row in exported["canonical_idea_realizations"] if row["idea_id"] == "idea-occupancy"]
        self.assertEqual(SOURCE_STATUS_EXACT, realization_rows[0]["source_fragment_status"])

        db_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(db_path) as connection:
            connection.execute(
                "UPDATE research_idea_realizations SET source_json_path = ? WHERE idea_id = ?",
                ("$.raw_ideas", "idea-occupancy"),
            )
        status, validate = self.run_ideas(root, ["validate"])
        self.assertEqual(1, status, validate)
        self.assertEqual(False, validate["ok"])
        self.assertTrue(any(item["code"] == "source_json_path_unresolved" for item in validate["diagnostics"]))

        status, repair = self.run_ideas(root, ["repair", "--apply"])
        self.assertEqual(0, status, repair)
        self.assertEqual([{"realization_id": realization["realization"]["id"], "source_json_path": "$.sections.raw_ideas[0]"}], repair["applied"])
