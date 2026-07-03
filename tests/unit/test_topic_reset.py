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
from isomer_labs.project.context import resolve_effective_topic_context
from isomer_labs.core.diagnostics import has_errors
from isomer_labs.models import SelectionRequest
from isomer_labs.project import discover_project
from isomer_labs.runtime.records import ResetCheckpointRecord, utc_timestamp
from isomer_labs.runtime.store import open_workspace_runtime
from isomer_labs.runtime.validation import validate_workspace_runtime
from isomer_labs.workspace.reset import apply_topic_reset, plan_topic_reset
from isomer_labs.project.validation import build_project_state


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class TopicResetTests(unittest.TestCase):
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
        write(root / "topic-workspaces" / "alpha" / "isomer-topic-workspace-summary.md", "# Alpha summary\n")
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

    def run_project(self, root: Path, args: list[str]) -> tuple[int, dict[str, object]]:
        status, output = self.run_main(["--print-json", "project", "--root", str(root), *args], cwd=root)
        return status, json.loads(output)

    def run_cli(self, root: Path, args: list[str]) -> tuple[int, dict[str, object]]:
        status, output = self.run_main(["--print-json", *args], cwd=root)
        return status, json.loads(output)

    def context_for_root(self, root: Path):
        project, project_diagnostics = discover_project(cwd=root, env=os.environ, project_selector=str(root))
        self.assertIsNotNone(project, [diagnostic.message for diagnostic in project_diagnostics])
        assert project is not None
        state = build_project_state(project)
        context, diagnostics = resolve_effective_topic_context(
            state,
            SelectionRequest(research_topic_id="alpha"),
            cwd=root,
            env=os.environ,
        )
        self.assertIsNotNone(context, [diagnostic.message for diagnostic in diagnostics])
        return context

    def test_cli_checkpoint_plan_and_apply_destructively_deletes_post_checkpoint_record(self) -> None:
        root = self.make_project()
        status, checkpoint = self.run_project(root, ["topic-reset", "checkpoint", "--topic", "alpha", "--render", "markdown"])
        self.assertEqual(0, status, checkpoint)
        checkpoint_id = str(checkpoint["checkpoint_id"])
        status, created = self.run_cli(
            root,
            [
                "ext",
                "research",
                "records",
                "create",
                "--project",
                str(root),
                "--topic",
                "alpha",
                "--id",
                "artifact-post-checkpoint",
                "--record-kind",
                "artifact",
                "--body",
                "post checkpoint research",
                "--content-name",
                "post-checkpoint.md",
            ],
        )
        self.assertEqual(0, status, created)
        record = created["record"]
        assert isinstance(record, dict)
        content_path = Path(str(record["content_path"]))
        self.assertTrue(content_path.exists())

        status, plan = self.run_project(root, ["topic-reset", "plan", "--topic", "alpha", checkpoint_id, "--render", "markdown"])
        self.assertEqual(0, status, plan)
        plan_id = str(plan["plan_id"])
        actions = plan["actions"]
        assert isinstance(actions, list)
        self.assertTrue(any(isinstance(action, dict) and action.get("action") == "delete_record" and action.get("target_ref") == "artifact-post-checkpoint" for action in actions))
        self.assertTrue(content_path.exists())
        with sqlite3.connect(root / "topic-workspaces" / "alpha" / "state.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute("SELECT id FROM lifecycle_records WHERE id = ?", ("artifact-post-checkpoint",)).fetchone()
        self.assertIsNotNone(row)

        status, outcome = self.run_project(root, ["topic-reset", "apply", "--topic", "alpha", "--yes", checkpoint_id, plan_id, "--render", "markdown"])
        self.assertEqual(0, status, outcome)
        self.assertFalse(content_path.exists())
        with sqlite3.connect(root / "topic-workspaces" / "alpha" / "state.sqlite") as connection:
            connection.row_factory = sqlite3.Row
            row = connection.execute("SELECT id FROM lifecycle_records WHERE id = ?", ("artifact-post-checkpoint",)).fetchone()
        self.assertIsNone(row)

    def test_plan_and_apply_delete_managed_actor_workspace_contents(self) -> None:
        root = self.make_project()
        context = self.context_for_root(root)
        status, checkpoint = self.run_project(root, ["topic-reset", "checkpoint", "--topic", "alpha"])
        self.assertEqual(0, status, checkpoint)
        checkpoint_id = str(checkpoint["checkpoint_id"])
        actor_root = root / "topic-workspaces" / "alpha" / "actors" / "operator"
        actor_root.mkdir(parents=True)
        scratch = actor_root / "scratch.txt"
        scratch.write_text("manual scratch", encoding="utf-8")
        store, diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
        self.assertIsNotNone(store, [diagnostic.message for diagnostic in diagnostics])
        assert store is not None
        try:
            with store.connection:
                store.record_path_plan(
                    topic_workspace_id=context.topic_workspace_id,
                    surface="topic_actor_workspace:operator",
                    path=actor_root,
                    source="test",
                    source_detail="operator actor workspace",
                    semantic_label="topic.actors.workspace",
                    scope_ref="topic_actor_name:operator",
                    compatibility_surface="topic_actor_workspace:operator",
                    storage_profile="topic_actor_worktree",
                )
        finally:
            store.close()

        plan_payload, plan_diagnostics = plan_topic_reset(context, checkpoint_id, env=os.environ)
        self.assertFalse(has_errors(plan_diagnostics), [diagnostic.message for diagnostic in plan_diagnostics])
        actions = plan_payload["actions"]
        assert isinstance(actions, list)
        self.assertTrue(any(isinstance(action, dict) and action.get("action") == "delete_file" and action.get("target_path") == str(scratch.resolve()) for action in actions))
        outcome, apply_diagnostics = apply_topic_reset(
            context,
            env=os.environ,
            checkpoint_id=checkpoint_id,
            plan_id=str(plan_payload["plan_id"]),
            yes=True,
        )
        self.assertFalse(has_errors(apply_diagnostics), [diagnostic.message for diagnostic in apply_diagnostics])
        self.assertTrue(outcome["ok"])
        self.assertTrue(actor_root.exists())
        self.assertFalse(scratch.exists())

    def test_checkpoint_update_preserves_later_preparation_record(self) -> None:
        root = self.make_project()
        status, checkpoint = self.run_project(root, ["topic-reset", "checkpoint", "--topic", "alpha", "--render", "markdown"])
        self.assertEqual(0, status, checkpoint)
        checkpoint_id = str(checkpoint["checkpoint_id"])
        status, created = self.run_cli(
            root,
            [
                "ext",
                "research",
                "records",
                "create",
                "--project",
                str(root),
                "--topic",
                "alpha",
                "--id",
                "v2-bootstrap-prep",
                "--record-kind",
                "decision_record",
                "--body",
                "v2 bootstrap setup that should survive reset",
                "--content-name",
                "v2-bootstrap-prep.md",
            ],
        )
        self.assertEqual(0, status, created)
        record = created["record"]
        assert isinstance(record, dict)
        content_path = Path(str(record["content_path"]))
        status, updated = self.run_project(
            root,
            [
                "topic-reset",
                "update-checkpoint",
                "--topic",
                "alpha",
                "--preserve-record",
                "v2-bootstrap-prep",
                "--preserve-semantic-label",
                "topic.records.views",
                "--source-label",
                "isomer-rsch-workspace-mgr",
                "--provenance-ref",
                "test:v2-bootstrap",
                "--render",
                "markdown",
                checkpoint_id,
            ],
        )
        self.assertEqual(0, status, updated)
        checkpoint_payload = updated["checkpoint"]
        assert isinstance(checkpoint_payload, dict)
        payload = checkpoint_payload["payload"]
        assert isinstance(payload, dict)
        self.assertIn("v2-bootstrap-prep", payload["preserved_record_ids"])
        status, plan = self.run_project(root, ["topic-reset", "plan", "--topic", "alpha", checkpoint_id])
        self.assertEqual(0, status, plan)
        actions = plan["actions"]
        assert isinstance(actions, list)
        self.assertTrue(any(isinstance(action, dict) and action.get("action") == "preserve" and action.get("target_ref") == "v2-bootstrap-prep" for action in actions))
        self.assertFalse(any(isinstance(action, dict) and action.get("action") == "delete_record" and action.get("target_ref") == "v2-bootstrap-prep" for action in actions))
        self.assertTrue(content_path.exists())

    def test_plan_blocks_secret_like_managed_workspace_material_and_apply_rejects(self) -> None:
        root = self.make_project()
        context = self.context_for_root(root)
        status, checkpoint = self.run_project(root, ["topic-reset", "checkpoint", "--topic", "alpha"])
        self.assertEqual(0, status, checkpoint)
        checkpoint_id = str(checkpoint["checkpoint_id"])
        actor_root = root / "topic-workspaces" / "alpha" / "actors" / "operator"
        actor_root.mkdir(parents=True)
        secret_path = actor_root / "token.txt"
        secret_path.write_text("secret-ish material", encoding="utf-8")
        store, diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
        self.assertIsNotNone(store, [diagnostic.message for diagnostic in diagnostics])
        assert store is not None
        try:
            with store.connection:
                store.record_path_plan(
                    topic_workspace_id=context.topic_workspace_id,
                    surface="topic_actor_workspace:operator",
                    path=actor_root,
                    source="test",
                    source_detail="operator actor workspace",
                    semantic_label="topic.actors.workspace",
                    scope_ref="topic_actor_name:operator",
                    compatibility_surface="topic_actor_workspace:operator",
                    storage_profile="topic_actor_worktree",
                )
        finally:
            store.close()

        plan_payload, plan_diagnostics = plan_topic_reset(context, checkpoint_id, env=os.environ)
        self.assertFalse(has_errors(plan_diagnostics), [diagnostic.message for diagnostic in plan_diagnostics])
        self.assertFalse(plan_payload["ok"])
        actions = plan_payload["actions"]
        assert isinstance(actions, list)
        self.assertTrue(any(isinstance(action, dict) and action.get("action") == "blocked" and action.get("target_kind") == "possible_secret_material" for action in actions))
        outcome, apply_diagnostics = apply_topic_reset(
            context,
            env=os.environ,
            checkpoint_id=checkpoint_id,
            plan_id=str(plan_payload["plan_id"]),
            yes=True,
        )
        self.assertTrue(has_errors(apply_diagnostics), [diagnostic.message for diagnostic in apply_diagnostics])
        self.assertFalse(outcome["ok"])
        self.assertTrue(secret_path.exists())

    def test_apply_rejects_stale_plan_after_runtime_state_changes(self) -> None:
        root = self.make_project()
        status, checkpoint = self.run_project(root, ["topic-reset", "checkpoint", "--topic", "alpha"])
        self.assertEqual(0, status, checkpoint)
        checkpoint_id = str(checkpoint["checkpoint_id"])
        status, plan = self.run_project(root, ["topic-reset", "plan", "--topic", "alpha", checkpoint_id])
        self.assertEqual(0, status, plan)
        plan_id = str(plan["plan_id"])
        status, created = self.run_cli(
            root,
            [
                "ext",
                "research",
                "records",
                "create",
                "--project",
                str(root),
                "--topic",
                "alpha",
                "--id",
                "artifact-after-plan",
                "--record-kind",
                "artifact",
                "--body",
                "late mutation",
            ],
        )
        self.assertEqual(0, status, created)
        status, stale = self.run_project(root, ["topic-reset", "apply", "--topic", "alpha", "--yes", checkpoint_id, plan_id])
        self.assertEqual(1, status, stale)
        diagnostics = stale["diagnostics"]
        assert isinstance(diagnostics, list)
        self.assertTrue(any(isinstance(diagnostic, dict) and "stale" in str(diagnostic.get("message", "")).lower() for diagnostic in diagnostics))

    def test_cli_surfaces_update_list_show_show_plan_help_human_and_confirmation(self) -> None:
        root = self.make_project()
        status, help_output = self.run_main(["project", "--root", str(root), "topic-reset", "--help"], cwd=root)
        self.assertEqual(0, status, help_output)
        self.assertIn("update-checkpoint", help_output)
        self.assertIn("show-plan", help_output)
        status, checkpoint = self.run_project(root, ["topic-reset", "checkpoint", "--topic", "alpha", "--render", "markdown"])
        self.assertEqual(0, status, checkpoint)
        checkpoint_id = str(checkpoint["checkpoint_id"])
        status, updated = self.run_project(
            root,
            [
                "topic-reset",
                "update-checkpoint",
                "--topic",
                "alpha",
                "--preserve-semantic-label",
                "topic.records.views",
                "--source-label",
                "manual-prep",
                checkpoint_id,
            ],
        )
        self.assertEqual(0, status, updated)
        status, listed = self.run_project(root, ["topic-reset", "list", "--topic", "alpha", "--include-payload"])
        self.assertEqual(0, status, listed)
        self.assertGreaterEqual(int(listed["count"]), 1)
        status, shown = self.run_project(root, ["topic-reset", "show", "--topic", "alpha", "--include-payload", "--include-rendered-body", checkpoint_id])
        self.assertEqual(0, status, shown)
        self.assertIn("rendered_body", shown)
        status, plan = self.run_project(root, ["topic-reset", "plan", "--topic", "alpha", checkpoint_id, "--render", "markdown"])
        self.assertEqual(0, status, plan)
        plan_id = str(plan["plan_id"])
        status, shown_plan = self.run_project(root, ["topic-reset", "show-plan", "--topic", "alpha", "--include-payload", "--include-rendered-body", plan_id])
        self.assertEqual(0, status, shown_plan)
        self.assertIn("actions", shown_plan)
        status, rejected = self.run_project(root, ["topic-reset", "apply", "--topic", "alpha", checkpoint_id, plan_id])
        self.assertEqual(1, status, rejected)
        diagnostics = rejected["diagnostics"]
        assert isinstance(diagnostics, list)
        self.assertTrue(any(isinstance(diagnostic, dict) and "--yes" in str(diagnostic.get("message", "")) for diagnostic in diagnostics))
        status, human_output = self.run_main(["project", "--root", str(root), "topic-reset", "list", "--topic", "alpha"], cwd=root)
        self.assertEqual(0, status, human_output)
        self.assertIn("Topic reset list: ok", human_output)

    def test_cli_checkpoint_reports_missing_initialized_topic_context(self) -> None:
        root = self.make_root()
        status, output = self.run_main(["--print-json", "project", "--root", str(root), "topic-reset", "checkpoint", "--topic", "alpha"], cwd=root)
        self.assertEqual(1, status, output)
        payload = json.loads(output)
        self.assertFalse(payload["ok"])
        self.assertEqual("context_resolution_failed", payload["error"]["code"])

    def test_runtime_validation_reports_forbidden_git_reset_payload_metadata(self) -> None:
        root = self.make_project()
        context = self.context_for_root(root)
        store, diagnostics = open_workspace_runtime(context, env=os.environ, read_only=False)
        self.assertIsNotNone(store, [diagnostic.message for diagnostic in diagnostics])
        assert store is not None
        now = utc_timestamp()
        try:
            with store.connection:
                store.upsert_reset_checkpoint(
                    ResetCheckpointRecord(
                        id="topic-reset-checkpoint-bad",
                        research_topic_id="alpha",
                        topic_workspace_id="alpha",
                        status="ready",
                        payload_json={
                            "title": "Topic Reset Checkpoint",
                            "summary": "bad",
                            "status": "ready",
                            "research_topic_id": "alpha",
                            "topic_workspace_id": "alpha",
                            "checkpoint_id": "topic-reset-checkpoint-bad",
                            "workspace_runtime_schema_version": "isomer-workspace-runtime.v1",
                            "semantic_path_inventory": [],
                            "preserved_record_ids": [],
                            "preserved_structured_payload_ids": [],
                            "runtime_high_watermarks": {},
                            "blockers": [],
                            "no_git_operations": True,
                            "git_stash_id": "stash@{0}",
                        },
                        payload_digest="bad",
                        checkpoint_digest="bad",
                        created_at=now,
                        updated_at=now,
                    )
                )
        finally:
            store.close()
        _inspection, validation_diagnostics = validate_workspace_runtime(context, env=os.environ)
        self.assertTrue(any(diagnostic.code == "ISO223" for diagnostic in validation_diagnostics), [diagnostic.message for diagnostic in validation_diagnostics])


if __name__ == "__main__":
    unittest.main()
