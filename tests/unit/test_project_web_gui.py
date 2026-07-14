from __future__ import annotations

import asyncio
import contextlib
import io
import json
import os
import sqlite3
import tempfile
import textwrap
import unittest
from pathlib import Path
from urllib.parse import urlsplit
from unittest.mock import patch

from isomer_labs import cli
from isomer_labs.deepsci_ext.record_formats import canonical_record_format_ref
from isomer_labs.web import create_app
from isomer_labs.web.contracts import (
    IdeaDetailResponseContract,
    RecordDetailResponseContract,
    RecordFilesResponseContract,
    RecordViewerDescriptorContract,
    TopicGraphResponseContract,
    TopicOverviewResponseContract,
    validate_gui_payload,
)
from isomer_labs.web.read_model import ProjectWebReadModel


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class ProjectWebGuiTests(unittest.TestCase):
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

    def run_main(self, args: list[str], *, cwd: Path | None = None) -> tuple[int, str]:
        selected_cwd = cwd or Path.cwd()
        stdout = io.StringIO()
        with (
            contextlib.chdir(selected_cwd),
            patch.dict(os.environ, {"HOME": str(selected_cwd), "PATH": os.environ.get("PATH", "")}, clear=True),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(args)
        return status, stdout.getvalue()

    def read_model(self, root: Path) -> ProjectWebReadModel:
        return ProjectWebReadModel(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})

    def asgi_get_response(self, app: object, path: str, *, request_headers: dict[str, str] | None = None) -> tuple[int, dict[str, str], bytes]:
        async def call() -> tuple[int, dict[str, str], bytes]:
            messages: list[dict[str, object]] = []
            parsed = urlsplit(path)
            received = False

            async def receive() -> dict[str, object]:
                nonlocal received
                if received:
                    return {"type": "http.disconnect"}
                received = True
                return {"type": "http.request", "body": b"", "more_body": False}

            async def send(message: dict[str, object]) -> None:
                messages.append(message)

            scope = {
                "type": "http",
                "asgi": {"version": "3.0"},
                "http_version": "1.1",
                "method": "GET",
                "scheme": "http",
                "path": parsed.path,
                "raw_path": parsed.path.encode(),
                "query_string": parsed.query.encode(),
                "headers": [
                    (key.lower().encode("latin1"), value.encode("latin1"))
                    for key, value in (request_headers or {}).items()
                ],
                "client": ("testclient", 50000),
                "server": ("testserver", 80),
                "root_path": "",
            }
            await app(scope, receive, send)  # type: ignore[operator]
            start = next(message for message in messages if message["type"] == "http.response.start")
            headers = {
                key.decode("latin1").lower(): value.decode("latin1")
                for key, value in start["headers"]  # type: ignore[index]
            }
            body = b"".join(
                message.get("body", b"")  # type: ignore[arg-type]
                for message in messages
                if message["type"] == "http.response.body"
            )
            return int(start["status"]), headers, body

        return asyncio.run(call())

    def asgi_get(self, app: object, path: str, *, headers: dict[str, str] | None = None) -> tuple[int, dict[str, str]]:
        status, headers, _body = self.asgi_get_response(app, path, request_headers=headers)
        return status, headers

    def create_indexed_idea_record(
        self,
        root: Path,
        *,
        record_id: str,
        idea_id: str,
        idea_text: str,
        relationships_json: str | None = None,
        files_json: str | None = None,
        include_idea: bool = True,
        payload_extra: dict[str, object] | None = None,
        format_profile_ref: str | None = None,
    ) -> None:
        payload_file = root / f"{record_id}.json"
        payload: dict[str, object] = {
            "title": idea_text,
            "summary": f"Summary for {idea_text}",
            "sections": {},
        }
        if include_idea:
            payload["sections"] = {
                "raw_ideas": [
                    {
                        "idea_id": idea_id,
                        "title": idea_text,
                        "summary": f"Summary for {idea_text}",
                        "status": "active",
                    }
                ]
            }
        if payload_extra:
            payload.update(payload_extra)
        payload_file.write_text(
            json.dumps(payload),
            encoding="utf-8",
        )
        args = [
            "--print-json",
            "ext",
            "research",
            "records",
            "create",
            "--project",
            str(root),
            "--topic",
            "alpha",
            "--id",
            record_id,
            "--record-kind",
            "run",
            "--format-profile",
            format_profile_ref or canonical_record_format_ref("report.raw-idea-slate", "profile"),
            "--payload-file",
            str(payload_file),
        ]
        if relationships_json is not None:
            args.extend(["--relationships-json", relationships_json])
        if files_json is not None:
            args.extend(["--files-json", files_json])
        status, output = self.run_main(args, cwd=root)
        self.assertEqual(0, status, output)

    def register_canonical_idea(
        self,
        root: Path,
        *,
        idea_id: str,
        title: str,
        summary: str | None = None,
        record_id: str | None = None,
        source_json_path: str | None = None,
    ) -> None:
        upsert_args = [
            "--print-json",
            "ext",
            "research",
            "ideas",
            "upsert",
            "--project",
            str(root),
            "--topic",
            "alpha",
            "--idea-id",
            idea_id,
            "--title",
            title,
            "--summary",
            summary or f"Summary for {title}",
            "--status",
            "candidate",
        ]
        if record_id is not None:
            upsert_args.extend(["--source-record-id", record_id])
        if source_json_path is not None:
            upsert_args.extend(["--source-json-path", source_json_path])
        status, output = self.run_main(upsert_args, cwd=root)
        self.assertEqual(0, status, output)
        if record_id is None:
            return
        realize_args = [
            "--print-json",
            "ext",
            "research",
            "ideas",
            "realize",
            "--project",
            str(root),
            "--topic",
            "alpha",
            "--idea-id",
            idea_id,
            "--record-id",
            record_id,
        ]
        if source_json_path is not None:
            realize_args.extend(["--source-json-path", source_json_path])
        status, output = self.run_main(realize_args, cwd=root)
        self.assertEqual(0, status, output)

    def test_neutral_kaoju_record_uses_generic_web_read_contracts(self) -> None:
        root = self.make_project()
        payload_file = root / "kaoju-source-digest.json"
        payload_file.write_text(
            json.dumps(
                {
                    "title": "Source Digest",
                    "summary": "Exact inspection of one work.",
                    "artifact_family": "kaoju",
                    "semantic_id": "kaoju:source-digest",
                    "artifact_type": "source-digest",
                    "procedure": "landscape-pass",
                    "sections": {
                        "source_identity": {"source_class": "paper"},
                        "findings": [{"claim": "Method uses retrieval.", "verdict": "source-supported"}],
                    },
                    "files": [{"path": "paper.pdf", "file_role": "source"}],
                }
            ),
            encoding="utf-8",
        )
        status, output = self.run_main(
            [
                "--print-json",
                "ext",
                "research",
                "records",
                "create",
                "--project",
                str(root),
                "--topic",
                "alpha",
                "--id",
                "kaoju-source-digest",
                "--record-kind",
                "evidence_item",
                "--semantic-id",
                "kaoju:source-digest",
                "--format-profile",
                "isomer:research/record-format/profile/kaoju/evidence/source-digest/v1",
                "--payload-file",
                str(payload_file),
            ],
            cwd=root,
        )
        self.assertEqual(0, status, output)

        read_model = self.read_model(root)
        detail = read_model.record_detail("alpha", "kaoju-source-digest", include_payload=True)
        validate_gui_payload(detail, RecordDetailResponseContract)
        self.assertTrue(detail["ok"], detail)
        self.assertEqual("Source Digest", detail["query_summary"]["title"])
        self.assertEqual("kaoju:source-digest", detail["query_summary"]["semantic_id"])
        self.assertEqual("kaoju", detail["query_summary"]["artifact_family"])
        self.assertEqual("Method uses retrieval.", detail["facets"]["claims"][0]["claim"])
        self.assertTrue(any(item["file_role"] == "structured_payload" for item in detail["files"]))
        self.assertIn("payload", detail["structured_payload"])
        self.assertIn("validation_status", detail["structured_payload"])
        self.assertIn("edges", detail["lineage"])

    def test_project_topic_runtime_read_model_and_static_routes(self) -> None:
        root = self.make_project()
        app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})
        route_paths = {getattr(route, "path", "") for route in app.routes}
        self.assertIn("/api/project", route_paths)
        self.assertIn("/api/explorer/project", route_paths)
        self.assertIn("/api/openable/{openable_item_id:path}", route_paths)
        self.assertIn("/api/topics/{topic_id}/records/export", route_paths)
        self.assertIn("/api/topics/{topic_id}/graphs/{graph_scope}", route_paths)
        self.assertIn("/api/topics/{topic_id}/viewer/records/{record_id}", route_paths)
        self.assertIn("/api/topics/{topic_id}/ideas/{idea_id}", route_paths)
        self.assertIn("/api/topics/{topic_id}/overview", route_paths)
        self.assertIn("/api/topics/{topic_id}/overview/json", route_paths)
        self.assertIn("/api/events", route_paths)
        self.assertNotIn("/api/explorer/files", route_paths)
        self.assertTrue((Path("src/isomer_labs/web/static/index.html")).exists())
        self.assertTrue(list(Path("src/isomer_labs/web/static/assets").glob("*.js")))

        read_model = self.read_model(root)
        project = read_model.project_summary()
        self.assertTrue(project["ok"], project)
        self.assertEqual(str(root.resolve()), project["project"]["root"])

        topics = read_model.topics()
        self.assertTrue(topics["ok"], topics)
        self.assertEqual(["alpha"], [topic["id"] for topic in topics["topics"]])
        self.assertIn("topic_workspace_path", topics["topics"][0])

        topic = read_model.topic("alpha")
        self.assertTrue(topic["ok"], topic)
        self.assertEqual("Alpha topic", topic["topic_config"]["topic_statement"])
        self.assertIn("topic_workspace_manifest", topic)

        runtime = read_model.runtime("alpha")
        self.assertTrue(runtime["ok"], runtime)
        self.assertTrue(runtime["runtime"]["exists"])
        self.assertIn("lifecycle_records", runtime["runtime"]["counts"])

    def test_project_explorer_and_openable_descriptors_are_semantic_and_read_only(self) -> None:
        root = self.make_project()
        read_model = self.read_model(root)

        explorer = read_model.project_explorer()
        self.assertTrue(explorer["ok"], explorer)
        self.assertFalse(explorer["mutated"])
        self.assertTrue(str(explorer["revision"]).startswith("pexp:"))
        self.assertEqual(["project"], explorer["root_node_ids"])
        nodes = {node["id"]: node for node in explorer["nodes"]}
        self.assertIn("project", nodes)
        self.assertIn("project:manifest", nodes)
        self.assertNotIn("project:settings", nodes)
        self.assertIn("project:topics", nodes)
        self.assertIn("topic:alpha", nodes)
        self.assertTrue(nodes["topic:alpha"]["has_children"])
        self.assertFalse(nodes["topic:alpha"]["children_loaded"])
        self.assertFalse(any(str(node["id"]).startswith("topic:alpha:graph:") for node in explorer["nodes"]))

        expanded = read_model.project_explorer(expanded_topic_ids=("alpha",))
        expanded_nodes = {node["id"]: node for node in expanded["nodes"]}
        self.assertTrue(expanded_nodes["topic:alpha"]["children_loaded"])
        self.assertIn("topic:alpha:overview", expanded_nodes)
        self.assertIn("topic:alpha:graphs", expanded_nodes)
        self.assertIn("topic:alpha:graph:idea-lineage", expanded_nodes)
        self.assertIn("topic:alpha:records", expanded_nodes)
        self.assertNotIn("topic:alpha:runtime", expanded_nodes)
        self.assertNotIn("topic:alpha:actors", expanded_nodes)
        self.assertNotIn("topic:alpha:repositories", expanded_nodes)
        self.assertFalse(any(str(node["id"]).startswith("file:") for node in expanded["nodes"]))

        descriptor = read_model.openable_item_descriptor("topic:alpha:graph:idea-lineage")
        self.assertTrue(descriptor["ok"], descriptor)
        self.assertFalse(descriptor["mutated"])
        self.assertEqual("topic-alpha-graph-idea-lineage", descriptor["tab_id"])
        self.assertEqual("ideaGraph", descriptor["preferred_tab_component"])
        self.assertEqual("idea-lineage", descriptor["graph_scope"])

        overview = read_model.openable_item_descriptor("topic:alpha:overview")
        self.assertTrue(overview["ok"], overview)
        self.assertEqual("topicOverview", overview["preferred_tab_component"])
        self.assertEqual("/api/topics/alpha/overview", overview["detail_urls"]["overview"])
        self.assertEqual("/api/topics/alpha", overview["detail_urls"]["topic"])
        self.assertEqual("/api/topics/alpha/runtime", overview["detail_urls"]["runtime"])

        stale_runtime = read_model.openable_item_descriptor("topic:alpha:runtime")
        self.assertTrue(stale_runtime["ok"], stale_runtime)
        self.assertEqual("runtime", stale_runtime["preferred_tab_component"])
        self.assertEqual("/api/topics/alpha/runtime", stale_runtime["detail_urls"]["runtime"])

        settings = read_model.openable_item_descriptor("project:settings")
        self.assertTrue(settings["ok"], settings)
        self.assertFalse(settings["mutated"])
        self.assertEqual("project-settings", settings["tab_id"])
        self.assertEqual("settings", settings["preferred_tab_component"])
        self.assertEqual("Project Settings", settings["title"])

        missing = read_model.openable_item_descriptor("topic:missing:overview")
        self.assertFalse(missing["ok"], missing)
        self.assertEqual("topic_not_found", missing["error"]["code"])

    def test_topic_overview_api_reads_markdown_and_defers_supporting_json(self) -> None:
        root = self.make_project()
        write(
            root / "topic-workspaces" / "alpha" / "intent" / "src" / "topic-overview.md",
            """
            # Alpha Overview

            Human-readable topic summary.
            """,
        )
        read_model = self.read_model(root)

        overview = read_model.topic_overview("alpha")
        validate_gui_payload(overview, TopicOverviewResponseContract)
        self.assertTrue(overview["ok"], overview)
        self.assertFalse(overview["mutated"])
        self.assertEqual("alpha", overview["topic_id"])
        self.assertEqual("alpha", overview["topic_workspace_id"])
        self.assertEqual("topic.intent.overview", overview["overview"]["semantic_label"])
        self.assertTrue(overview["overview"]["exists"])
        self.assertIn("Human-readable topic summary.", overview["overview"]["content_markdown"])
        self.assertIsNone(overview["topic_payload"])
        self.assertIsNone(overview["runtime_payload"])

        supporting_json = read_model.topic_overview_supporting_json("alpha")
        self.assertTrue(supporting_json["ok"], supporting_json)
        self.assertEqual("Alpha topic", supporting_json["topic_payload"]["topic_config"]["topic_statement"])
        self.assertTrue(supporting_json["runtime_payload"]["runtime"]["exists"])

        app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})
        status, _headers, body = self.asgi_get_response(app, "/api/topics/alpha/overview")
        self.assertEqual(200, status)
        route_payload = json.loads(body)
        self.assertTrue(route_payload["ok"], route_payload)
        self.assertIn("Human-readable topic summary.", route_payload["overview"]["content_markdown"])
        self.assertIsNone(route_payload["topic_payload"])
        self.assertIsNone(route_payload["runtime_payload"])

        status, _headers, body = self.asgi_get_response(app, "/api/topics/alpha/overview/json")
        self.assertEqual(200, status)
        route_payload = json.loads(body)
        self.assertEqual("Alpha topic", route_payload["topic_payload"]["topic_config"]["topic_statement"])

    def test_topic_overview_api_reports_missing_markdown_without_failing_topic(self) -> None:
        root = self.make_project()
        read_model = self.read_model(root)

        overview = read_model.topic_overview("alpha")
        validate_gui_payload(overview, TopicOverviewResponseContract)
        self.assertTrue(overview["ok"], overview)
        self.assertFalse(overview["mutated"])
        self.assertFalse(overview["overview"]["exists"])
        self.assertIsNone(overview["overview"]["content_markdown"])
        self.assertTrue(any(diagnostic["code"] == "topic_overview_missing" for diagnostic in overview["diagnostics"]), overview)
        self.assertIsNone(overview["topic_payload"])
        self.assertIsNone(overview["runtime_payload"])

        app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})
        status, _headers, body = self.asgi_get_response(app, "/api/topics/alpha/overview")
        self.assertEqual(200, status)
        route_payload = json.loads(body)
        self.assertTrue(route_payload["ok"], route_payload)
        self.assertFalse(route_payload["overview"]["exists"])

    def test_idea_detail_resolves_source_json_and_openable_descriptor_read_only(self) -> None:
        root = self.make_project()
        self.create_indexed_idea_record(
            root,
            record_id="idea-source",
            idea_id="idea-source",
            idea_text="Source path idea",
        )
        self.register_canonical_idea(
            root,
            idea_id="idea-source",
            title="Canonical source idea",
            record_id="idea-source",
            source_json_path="$.sections.raw_ideas[0]",
        )
        db_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        before_mtime = db_path.stat().st_mtime_ns
        read_model = self.read_model(root)

        detail = read_model.idea_detail("alpha", "idea-source")
        validate_gui_payload(detail, IdeaDetailResponseContract)
        self.assertTrue(detail["ok"], detail)
        self.assertFalse(detail["mutated"])
        self.assertEqual("Canonical source idea", detail["idea"]["title"])
        self.assertEqual("idea-source", detail["latest_realization"]["record_id"])
        self.assertEqual("latest_realization_source_path", detail["source"]["source_kind"])
        self.assertEqual("$.sections.raw_ideas[0]", detail["source"]["source_json_path"])
        self.assertEqual("$.sections.raw_ideas[0]", detail["source_provenance"]["source_json_path"])
        self.assertEqual("exact", detail["source_provenance"]["source_fragment_status"])
        self.assertEqual("canonical_idea_source", detail["source_provenance"]["source_classification"])
        self.assertEqual("Summary for Source path idea", detail["idea_content"]["summary"])
        self.assertEqual("Summary for Source path idea", detail["source"]["source_json"]["summary"])
        self.assertEqual(before_mtime, db_path.stat().st_mtime_ns)

        descriptor = read_model.openable_item_descriptor("idea:alpha:idea-source")
        self.assertTrue(descriptor["ok"], descriptor)
        self.assertEqual("ideaDetail", descriptor["preferred_tab_component"])
        self.assertEqual("idea-source", descriptor["idea_id"])
        self.assertEqual("topic-alpha-idea-idea-source", descriptor["tab_id"])

        app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})
        status, _headers, body = self.asgi_get_response(app, "/api/topics/alpha/ideas/idea-source")
        self.assertEqual(200, status)
        route_payload = json.loads(body)
        validate_gui_payload(route_payload, IdeaDetailResponseContract)
        self.assertTrue(route_payload["ok"], route_payload)
        self.assertEqual("Summary for Source path idea", route_payload["idea_content"]["summary"])
        self.assertEqual("idea-source", route_payload["source_provenance"]["source_record_id"])

        with sqlite3.connect(db_path) as connection:
            connection.execute(
                "UPDATE research_idea_realizations SET source_json_path = ? WHERE idea_id = ?",
                ("$", "idea-source"),
            )
        fallback = read_model.idea_detail("alpha", "idea-source")
        self.assertTrue(fallback["ok"], fallback)
        self.assertEqual("Canonical source idea", fallback["idea_content"]["title"])
        self.assertEqual("legacy_fallback", fallback["source_provenance"]["source_fragment_status"])
        self.assertTrue(any(item["code"] == "source_json_path_broad" for item in fallback["diagnostics"]))
        self.assertNotIn("sections", fallback["source"]["source_json"])

    def test_idea_detail_reports_missing_and_oversized_source_json_without_repair(self) -> None:
        root = self.make_project()
        self.register_canonical_idea(root, idea_id="metadata-only", title="Metadata Only")
        self.create_indexed_idea_record(
            root,
            record_id="large-source",
            idea_id="large-source",
            idea_text="Large source idea",
        )
        (root / "topic-workspaces" / "alpha" / "records" / "runs" / "research-records" / "run" / "large-source" / "payload.json").write_text(
            json.dumps(
                {
                    "title": "Large Source",
                    "summary": "Large Source",
                    "sections": {
                        "raw_ideas": [
                            {
                                "idea_id": "large-source",
                                "title": "Large source idea",
                                "summary": "Summary for Large source idea",
                                "large_blob": "x" * (1024 * 1024 + 64),
                            }
                        ]
                    },
                }
            ),
            encoding="utf-8",
        )
        self.register_canonical_idea(root, idea_id="large-source", title="Large Source", record_id="large-source", source_json_path="$.sections.raw_ideas[0]")
        read_model = self.read_model(root)

        metadata_detail = read_model.idea_detail("alpha", "metadata-only")
        validate_gui_payload(metadata_detail, IdeaDetailResponseContract)
        self.assertTrue(metadata_detail["ok"], metadata_detail)
        self.assertEqual("idea_metadata", metadata_detail["source"]["source_kind"])
        self.assertTrue(any(item["code"] == "source_json_unavailable" for item in metadata_detail["diagnostics"]))

        large_detail = read_model.idea_detail("alpha", "large-source")
        validate_gui_payload(large_detail, IdeaDetailResponseContract)
        self.assertTrue(large_detail["ok"], large_detail)
        self.assertTrue(large_detail["source"]["source_json_truncated"])
        self.assertNotIn("source_json", large_detail["source"])
        self.assertTrue(any(item["code"] == "source_json_truncated" for item in large_detail["diagnostics"]))

        full_detail = read_model.idea_detail("alpha", "large-source", include_source_json=True)
        validate_gui_payload(full_detail, IdeaDetailResponseContract)
        self.assertTrue(full_detail["ok"], full_detail)
        self.assertFalse(full_detail["source"]["source_json_truncated"])
        self.assertIn("large_blob", full_detail["source"]["source_json"])

        missing = read_model.openable_item_descriptor("idea:alpha:unknown-idea")
        self.assertFalse(missing["ok"], missing)
        self.assertEqual("ideaDetail", missing["preferred_tab_component"])
        self.assertEqual("idea_not_found", missing["error"]["code"])

    def test_web_gui_cache_modes_and_compression_are_visible(self) -> None:
        root = self.make_project()
        app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})
        asset_path = next(Path("src/isomer_labs/web/static/assets").glob("*.js"))

        status, headers, body = self.asgi_get_response(app, "/api/health")
        self.assertEqual(200, status)
        self.assertEqual("normal", json.loads(body)["cache_mode"])
        self.assertEqual("normal", headers["x-isomer-web-cache-mode"])
        self.assertEqual("no-cache", headers["cache-control"])
        self.assertIn("app;dur=", headers["server-timing"])

        status, headers = self.asgi_get(app, "/")
        self.assertEqual(200, status)
        self.assertEqual("no-cache", headers["cache-control"])

        status, headers = self.asgi_get(app, f"/assets/{asset_path.name}")
        self.assertEqual(200, status)
        if "-" in asset_path.stem:
            self.assertEqual("public, max-age=31536000, immutable", headers["cache-control"])

        status, headers = self.asgi_get(app, f"/assets/{asset_path.name}", headers={"accept-encoding": "gzip"})
        self.assertEqual(200, status)
        self.assertEqual("gzip", headers.get("content-encoding"))

        debug_app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")}, cache_mode="debug")
        for path in ("/", f"/assets/{asset_path.name}", "/api/health"):
            status, headers = self.asgi_get(debug_app, path)
            self.assertEqual(200, status, path)
            self.assertEqual("debug", headers["x-isomer-web-cache-mode"])
            self.assertEqual("no-store, no-cache, must-revalidate, max-age=0", headers["cache-control"])
            self.assertEqual("no-cache", headers["pragma"])
            self.assertEqual("0", headers["expires"])

    def test_record_read_and_index_maintenance_routes_are_explicit(self) -> None:
        root = self.make_project()
        self.create_indexed_idea_record(root, record_id="idea-list-row", idea_id="idea-list-row", idea_text="List row idea")
        read_model = self.read_model(root)

        records = read_model.records("alpha", limit=1)
        self.assertTrue(records["ok"], records)
        self.assertIn("records", records)
        self.assertEqual("table-summary", records["projection"]["kind"])
        self.assertEqual(1, records["returned_count"])
        self.assertEqual(1, records["limit"])
        self.assertEqual("idea-list-row", records["records"][0]["record_id"])
        self.assertIn("title", records["records"][0])
        self.assertNotIn("metadata", records["records"][0])
        self.assertNotIn("transition_metadata", records["records"][0])

        export = read_model.records_export("alpha", view="dashboard")
        self.assertTrue(export["ok"], export)
        self.assertIn("nodes", export)
        self.assertIn("diagnostics", export)
        self.assertIn("diagnostic_summary", export)

        validate = read_model.index_validate("alpha")
        self.assertIn("mutated", validate)
        self.assertFalse(validate["mutated"])

        cleanup = read_model.index_cleanup("alpha", missing_files=True, apply_cleanup=False)
        self.assertTrue(cleanup["ok"], cleanup)
        self.assertFalse(cleanup["mutated"])

    def test_graph_view_descriptor_and_event_read_models_are_read_only(self) -> None:
        root = self.make_project()
        self.create_indexed_idea_record(root, record_id="idea-parent", idea_id="idea-parent", idea_text="Parent runtime idea")
        self.create_indexed_idea_record(
            root,
            record_id="idea-child",
            idea_id="idea-child",
            idea_text="Child runtime idea",
            relationships_json='[{"target_record_id":"idea-parent","relation_kind":"derived_from"}]',
        )
        self.create_indexed_idea_record(
            root,
            record_id="route-record",
            idea_id="route-record",
            idea_text="Route decision record",
            include_idea=False,
            payload_extra={"decision": {"decision": "selected", "next_route": "idea-child", "reason": "Best evidence"}},
        )
        self.create_indexed_idea_record(root, record_id="idea-hop-target", idea_id="idea-hop-target", idea_text="Target hop idea")
        self.create_indexed_idea_record(
            root,
            record_id="support-hop",
            idea_id="support-hop",
            idea_text="Supporting hop record",
            include_idea=False,
            relationships_json='[{"target_record_id":"idea-hop-target","relation_kind":"derived_from"}]',
        )
        self.create_indexed_idea_record(
            root,
            record_id="idea-hop-source",
            idea_id="idea-hop-source",
            idea_text="Source hop idea",
            relationships_json='[{"target_record_id":"support-hop","relation_kind":"derived_from"}]',
        )

        read_model = self.read_model(root)
        export = read_model.records_export("alpha", view="ideas")
        self.assertTrue(export["ok"], export)
        self.assertFalse(export["mutated"])
        self.assertIn("index_revision", export)
        self.assertIn("index_revision_state", export)

        graph = read_model.topic_graph("alpha", graph_scope="idea-lineage", renderer="auto")
        validate_gui_payload(graph, TopicGraphResponseContract)
        self.assertTrue(graph["ok"], graph)
        self.assertFalse(graph["mutated"])
        self.assertEqual("idea-lineage", graph["graph_scope"])
        self.assertEqual("react-flow-detail", graph["renderer_hint"])
        self.assertTrue(graph["topology_complete"])
        self.assertEqual(len(graph["nodes"]), graph["total_node_count"])
        self.assertEqual(len(graph["edges"]), graph["total_edge_count"])
        self.assertIn("index_revision", graph)
        self.assertGreaterEqual(len(graph["nodes"]), 2)
        self.assertTrue(all(node["material_kind"] == "idea" for node in graph["nodes"]))
        self.assertTrue(any(node["record_id"] == "idea-parent" for node in graph["nodes"]))
        direct_edges = [edge for edge in graph["edges"] if edge["relation_kind"] == "derived_from" and edge["source_record_refs"] == ["idea-child", "idea-parent"]]
        self.assertTrue(direct_edges, graph["edges"])
        self.assertFalse(direct_edges[0]["collapsed"])
        self.assertTrue(direct_edges[0]["source_relationship_refs"])
        collapsed_edges = [edge for edge in graph["edges"] if edge.get("collapsed") and edge.get("source_record_refs") == ["idea-hop-source", "support-hop", "idea-hop-target"]]
        self.assertEqual(1, len(collapsed_edges), graph["edges"])
        self.assertEqual("collapsed-projection", collapsed_edges[0]["source_classification"])
        self.assertGreaterEqual(graph["facets"]["counts"]["ideas"], 2)
        self.assertFalse(any(node["record_id"] == "route-record" for node in graph["nodes"]))

        limited_graph = read_model.topic_graph("alpha", graph_scope="idea-lineage", renderer="react-flow", limit=1)
        validate_gui_payload(limited_graph, TopicGraphResponseContract)
        self.assertTrue(limited_graph["ok"], limited_graph)
        self.assertFalse(limited_graph["topology_complete"])
        self.assertEqual(graph["total_node_count"], limited_graph["total_node_count"])

        graph_with_supporting = read_model.topic_graph("alpha", graph_scope="idea-lineage", renderer="auto", include_secondary=True)
        validate_gui_payload(graph_with_supporting, TopicGraphResponseContract)
        self.assertTrue(graph_with_supporting["ok"], graph_with_supporting)
        self.assertTrue(any(node["material_kind"] == "decision" and node["record_id"] == "route-record" for node in graph_with_supporting["nodes"]))

        dense = read_model.topic_graph("alpha", graph_scope="artifact-overview", renderer="sigma", include_secondary=True)
        validate_gui_payload(dense, TopicGraphResponseContract)
        self.assertFalse(dense["ok"], dense)
        self.assertEqual("unsupported_graph_scope", dense["error"]["code"])
        self.assertFalse(dense["mutated"])
        recent_errors = read_model.recent_errors("alpha")
        self.assertFalse(recent_errors["mutated"])
        self.assertEqual("unsupported_graph_scope", recent_errors["errors"][0]["code"])
        self.assertEqual("graph:artifact-overview", recent_errors["errors"][0]["source_view"])

        invalid = read_model.topic_graph("alpha", graph_scope="unknown")
        validate_gui_payload(invalid, TopicGraphResponseContract)
        self.assertFalse(invalid["ok"], invalid)
        self.assertEqual("unsupported_graph_scope", invalid["error"]["code"])
        self.assertFalse(invalid["mutated"])

        descriptor = read_model.record_viewer_descriptor("alpha", "idea-parent")
        validate_gui_payload(descriptor, RecordViewerDescriptorContract)
        self.assertTrue(descriptor["ok"], descriptor)
        self.assertFalse(descriptor["mutated"])
        self.assertEqual("idea-parent", descriptor["record_id"])
        self.assertEqual("markdown", descriptor["viewer_kind"])
        self.assertNotIn("structured_payload", descriptor)
        self.assertTrue(descriptor.get("topic_workspace_relative_path"), descriptor)
        self.assertTrue(str(descriptor.get("absolute_filepath", "")).endswith(".json"), descriptor)
        self.assertEqual("idea-parent", descriptor["direct_parent_idea"]["idea_id"])
        self.assertIn(descriptor["direct_parent_idea"]["source"], {"canonical_realization", "query_index_ideas"})

        detail = read_model.record_detail("alpha", "idea-parent", include_payload=True)
        validate_gui_payload(detail, RecordDetailResponseContract)
        self.assertFalse(detail["mutated"])
        self.assertEqual(descriptor["absolute_filepath"], detail["absolute_filepath"])
        self.assertEqual("idea-parent", detail["direct_parent_idea"]["idea_id"])

        rendered = read_model.record_render("alpha", "idea-parent")
        self.assertTrue(rendered["ok"], rendered)
        self.assertFalse(rendered["mutated"])
        self.assertEqual(descriptor["absolute_filepath"], rendered["absolute_filepath"])

        openable_record = read_model.openable_item_descriptor("record:alpha:idea-parent")
        self.assertTrue(openable_record["ok"], openable_record)
        self.assertEqual("recordDetail", openable_record["preferred_tab_component"])
        self.assertEqual("topic-alpha-record-idea-parent", openable_record["tab_id"])

        missing = read_model.record_viewer_descriptor("alpha", "missing-record")
        validate_gui_payload(missing, RecordViewerDescriptorContract)
        self.assertFalse(missing["ok"], missing)
        self.assertFalse(missing["mutated"])
        self.assertEqual("record_not_found", missing["error"]["code"])

        event = read_model.topic_change_event("alpha")
        self.assertTrue(event["ok"], event)
        self.assertFalse(event["mutated"])
        self.assertEqual("topic.index.changed", event["event_type"])
        self.assertEqual(export["index_revision"], event["index_revision"])

        app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})
        status, headers = self.asgi_get(app, "/api/events?topic_id=alpha&once=true")
        self.assertEqual(200, status)
        self.assertEqual("text/event-stream; charset=utf-8", headers["content-type"])

    def test_idea_graph_prefers_canonical_research_ideas_when_present(self) -> None:
        root = self.make_project()
        self.create_indexed_idea_record(root, record_id="legacy-parent", idea_id="legacy-parent", idea_text="Legacy parent idea")
        self.create_indexed_idea_record(root, record_id="legacy-child", idea_id="legacy-child", idea_text="Legacy child idea")
        commands = [
            [
                "ext",
                "research",
                "ideas",
                "upsert",
                "--project",
                str(root),
                "--topic",
                "alpha",
                "--idea-id",
                "idea-parent",
                "--title",
                "Canonical parent",
                "--summary",
                "Canonical parent summary.",
                "--status",
                "candidate",
                "--source-record-id",
                "legacy-parent",
                "--source-json-path",
                "$.sections.raw_ideas[0]",
            ],
            [
                "ext",
                "research",
                "ideas",
                "upsert",
                "--project",
                str(root),
                "--topic",
                "alpha",
                "--idea-id",
                "idea-child",
                "--title",
                "Canonical child",
                "--summary",
                "Canonical child summary.",
                "--status",
                "selected",
                "--alias",
                "legacy-child",
                "--source-record-id",
                "legacy-child",
                "--source-json-path",
                "$.sections.raw_ideas[0]",
            ],
            [
                "ext",
                "research",
                "ideas",
                "realize",
                "--project",
                str(root),
                "--topic",
                "alpha",
                "--idea-id",
                "idea-child",
                "--record-id",
                "legacy-child",
                "--source-json-path",
                "$.sections.raw_ideas[0]",
            ],
            [
                "ext",
                "research",
                "ideas",
                "lineage",
                "add",
                "--project",
                str(root),
                "--topic",
                "alpha",
                "idea-parent",
                "idea-child",
                "--lineage-kind",
                "derived_from",
            ],
        ]
        for command in commands:
            status, output = self.run_main(["--print-json", *command], cwd=root)
            self.assertEqual(0, status, output)

        read_model = self.read_model(root)
        graph = read_model.topic_graph("alpha", graph_scope="idea-lineage", renderer="auto")
        self.assertTrue(graph["ok"], graph)
        self.assertEqual({"idea:idea-parent", "idea:idea-child"}, {node["id"] for node in graph["nodes"]})
        self.assertEqual({"I-1", "I-2"}, {node["display_key"] for node in graph["nodes"]})
        self.assertEqual(["derived_from"], [edge["relation_kind"] for edge in graph["edges"]])
        self.assertFalse(any(item["code"] == "idea_graph_heuristic_fallback" for item in graph["diagnostics"]))

        db_path = root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(db_path) as connection:
            connection.execute("UPDATE research_ideas SET display_key = ? WHERE idea_id = ?", ("I1", "idea-parent"))
        legacy_graph = read_model.topic_graph("alpha", graph_scope="idea-lineage", renderer="auto")
        self.assertTrue(any(item["code"] == "idea_display_key_legacy_format" and item["display_key"] == "I1" for item in legacy_graph["diagnostics"]))

    def test_file_backed_record_content_opens_through_semantic_record_descriptor(self) -> None:
        root = self.make_project()
        metrics = root / "topic-workspaces" / "alpha" / "outputs" / "metrics.json"
        write(metrics, '{"runtime_ms": 12.3}')
        self.create_indexed_idea_record(
            root,
            record_id="idea-with-file",
            idea_id="idea-with-file",
            idea_text="Idea with file",
            files_json='[{"path":"outputs/metrics.json","file_role":"raw_results","semantic_label":"topic.records.runs"}]',
        )

        read_model = self.read_model(root)
        descriptor = read_model.record_viewer_descriptor("alpha", "idea-with-file")
        validate_gui_payload(descriptor, RecordViewerDescriptorContract)
        self.assertTrue(descriptor["ok"], descriptor)
        self.assertEqual("json", descriptor["viewer_kind"])
        self.assertIn("/files/", descriptor["primary_content_url"])
        self.assertTrue(str(descriptor["primary_content_url"]).endswith("/content"))
        self.assertEqual(str(metrics.resolve(strict=False)), descriptor["absolute_filepath"])
        self.assertEqual("outputs/metrics.json", descriptor["topic_workspace_relative_path"])

        file_id = str(descriptor["primary_content_url"]).split("/files/", 1)[1].split("/content", 1)[0]
        files = read_model.record_files("alpha", "idea-with-file")
        validate_gui_payload(files, RecordFilesResponseContract)
        self.assertEqual("alpha", files["topic_id"])
        content = read_model.record_file_content("alpha", "idea-with-file", file_id)
        self.assertTrue(content["ok"], content)
        self.assertEqual(metrics.resolve(strict=False), content["path"])

        file_descriptor = read_model.openable_item_descriptor(f"file:alpha:idea-with-file:{file_id}")
        self.assertTrue(file_descriptor["ok"], file_descriptor)
        self.assertEqual("fileArtifact", file_descriptor["preferred_tab_component"])
        self.assertEqual(str(descriptor["primary_content_url"]), file_descriptor["content_url"])

        app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})
        status, _headers, body = self.asgi_get_response(app, str(descriptor["primary_content_url"]))
        self.assertEqual(200, status)
        self.assertEqual(b'{"runtime_ms": 12.3}', body.strip())

        status, _headers, body = self.asgi_get_response(app, "/api/explorer/files")
        self.assertEqual(404, status)
        self.assertIn(b"api_route_not_found", body)

    def test_cli_registers_project_web_commands(self) -> None:
        status, output = self.run_main(["project", "web", "--help"])
        self.assertEqual(0, status, output)
        self.assertIn("serve", output)

        status, output = self.run_main(["project", "web", "serve", "--help"])
        self.assertEqual(0, status, output)
        self.assertIn("--no-browser", output)
        self.assertIn("--root", output)


if __name__ == "__main__":
    unittest.main()
