from __future__ import annotations

import asyncio
import contextlib
import io
import json
import os
import tempfile
import textwrap
import unittest
from pathlib import Path
from urllib.parse import urlsplit
from unittest.mock import patch

from isomer_labs import cli
from isomer_labs.deepsci_ext.record_formats import canonical_record_format_ref
from isomer_labs.web import create_app
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

    def asgi_get(self, app: object, path: str) -> tuple[int, dict[str, str]]:
        async def call() -> tuple[int, dict[str, str]]:
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
                "headers": [],
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
            return int(start["status"]), headers

        return asyncio.run(call())

    def create_indexed_idea_record(
        self,
        root: Path,
        *,
        record_id: str,
        idea_id: str,
        idea_text: str,
        relationships_json: str | None = None,
    ) -> None:
        payload_file = root / f"{record_id}.json"
        payload_file.write_text(
            json.dumps(
                {
                    "title": idea_text,
                    "summary": f"Summary for {idea_text}",
                    "sections": {
                        "raw_ideas": [
                            {
                                "idea_id": idea_id,
                                "one_liner": idea_text,
                                "status": "active",
                            }
                        ]
                    },
                }
            ),
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
            canonical_record_format_ref("run.main-run-record", "profile"),
            "--payload-file",
            str(payload_file),
        ]
        if relationships_json is not None:
            args.extend(["--relationships-json", relationships_json])
        status, output = self.run_main(args, cwd=root)
        self.assertEqual(0, status, output)

    def test_project_topic_runtime_read_model_and_static_routes(self) -> None:
        root = self.make_project()
        app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})
        route_paths = {getattr(route, "path", "") for route in app.routes}
        self.assertIn("/api/project", route_paths)
        self.assertIn("/api/topics/{topic_id}/records/export", route_paths)
        self.assertIn("/api/topics/{topic_id}/graphs/{graph_scope}", route_paths)
        self.assertIn("/api/topics/{topic_id}/viewer/records/{record_id}", route_paths)
        self.assertIn("/api/events", route_paths)
        self.assertTrue((Path("src/isomer_labs/web/static/index.html")).exists())
        self.assertTrue((Path("src/isomer_labs/web/static/assets/app.js")).exists())

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

    def test_web_gui_responses_disable_browser_cache(self) -> None:
        root = self.make_project()
        app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})

        for path in ("/", "/assets/app.js", "/api/health"):
            status, headers = self.asgi_get(app, path)
            self.assertEqual(200, status, path)
            self.assertEqual("no-store, no-cache, must-revalidate, max-age=0", headers["cache-control"])
            self.assertEqual("no-cache", headers["pragma"])
            self.assertEqual("0", headers["expires"])

    def test_record_read_and_index_maintenance_routes_are_explicit(self) -> None:
        root = self.make_project()
        read_model = self.read_model(root)

        records = read_model.records("alpha")
        self.assertTrue(records["ok"], records)
        self.assertIn("records", records)

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

        read_model = self.read_model(root)
        export = read_model.records_export("alpha", view="ideas")
        self.assertTrue(export["ok"], export)
        self.assertFalse(export["mutated"])
        self.assertIn("index_revision", export)
        self.assertIn("index_revision_state", export)

        graph = read_model.topic_graph("alpha", graph_scope="idea-lineage", renderer="auto")
        self.assertTrue(graph["ok"], graph)
        self.assertFalse(graph["mutated"])
        self.assertEqual("idea-lineage", graph["graph_scope"])
        self.assertEqual("react-flow-detail", graph["renderer_hint"])
        self.assertIn("index_revision", graph)
        self.assertGreaterEqual(len(graph["nodes"]), 2)
        self.assertTrue(any(node["record_id"] == "idea-parent" for node in graph["nodes"]))
        self.assertTrue(any(edge["relation_kind"] == "derived_from" for edge in graph["edges"]))
        self.assertGreaterEqual(graph["facets"]["counts"]["ideas"], 2)

        dense = read_model.topic_graph("alpha", graph_scope="artifact-overview", renderer="sigma", include_secondary=True)
        self.assertTrue(dense["ok"], dense)
        self.assertEqual("sigma-overview", dense["renderer_hint"])
        self.assertFalse(dense["mutated"])

        invalid = read_model.topic_graph("alpha", graph_scope="unknown")
        self.assertFalse(invalid["ok"], invalid)
        self.assertEqual("unsupported_graph_scope", invalid["error"]["code"])
        self.assertFalse(invalid["mutated"])

        descriptor = read_model.record_viewer_descriptor("alpha", "idea-parent")
        self.assertTrue(descriptor["ok"], descriptor)
        self.assertFalse(descriptor["mutated"])
        self.assertEqual("idea-parent", descriptor["record_id"])
        self.assertEqual("markdown", descriptor["viewer_kind"])
        self.assertNotIn("structured_payload", descriptor)

        missing = read_model.record_viewer_descriptor("alpha", "missing-record")
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
