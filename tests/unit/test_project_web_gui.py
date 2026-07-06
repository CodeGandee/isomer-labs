from __future__ import annotations

import asyncio
import contextlib
import io
import os
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from isomer_labs import cli
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

            async def receive() -> dict[str, object]:
                return {"type": "http.request", "body": b"", "more_body": False}

            async def send(message: dict[str, object]) -> None:
                messages.append(message)

            scope = {
                "type": "http",
                "asgi": {"version": "3.0"},
                "http_version": "1.1",
                "method": "GET",
                "scheme": "http",
                "path": path,
                "raw_path": path.encode(),
                "query_string": b"",
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

    def test_project_topic_runtime_read_model_and_static_routes(self) -> None:
        root = self.make_project()
        app = create_app(root, env={"HOME": str(root), "PATH": os.environ.get("PATH", "")})
        route_paths = {getattr(route, "path", "") for route in app.routes}
        self.assertIn("/api/project", route_paths)
        self.assertIn("/api/topics/{topic_id}/records/export", route_paths)
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
