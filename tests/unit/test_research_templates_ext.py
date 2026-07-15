from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from sqlalchemy.exc import OperationalError

from isomer_labs import cli
from isomer_labs.cli.commands.research_templates_ext import (
    DEFAULT_TEMPLATE_NAME,
    TEMPLATE_SEMANTIC_ID,
    _find_template_record,
    _template_summary_from_index_row,
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
        status, output = self.run_main(["--print-json", "ext", "research", "templates", *args, "--project", str(root), "--topic", "alpha"], cwd=root)
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

    def test_domain_failure_is_text_by_default_and_non_mutating(self) -> None:
        root = self.make_project()
        status, output = self.run_main(
            ["ext", "research", "templates", "show", "--name", "missing", "--project", str(root), "--topic", "alpha"],
            cwd=root,
        )
        self.assertEqual(1, status, output)
        self.assertFalse(output.lstrip().startswith("{"), output)
        self.assertIn("template_not_found", output)
        self.assertIn("Mutated: false", output)

    def test_domain_failure_uses_versioned_json_when_requested(self) -> None:
        root = self.make_project()
        status, output = self.run_main(
            ["--print-json", "ext", "research", "templates", "show", "--name", "missing", "--project", str(root), "--topic", "alpha"],
            cwd=root,
        )
        self.assertEqual(1, status, output)
        payload = json.loads(output)
        self.assertEqual("isomer-cli-output.v1", payload["output_schema_version"])
        self.assertEqual("ext research templates show", payload["command"])
        self.assertEqual("template_not_found", payload["error"]["code"])
        self.assertFalse(payload["mutated"])

    def test_context_failure_has_actionable_text_guidance(self) -> None:
        root = self.make_root()
        write(
            root / ".isomer-labs" / "manifest.toml",
            'schema_version = "isomer-project-manifest.v1"\n',
        )
        status, output = self.run_main(
            ["ext", "research", "templates", "list", "--project", str(root)],
            cwd=root,
        )
        self.assertEqual(1, status, output)
        self.assertIn("context_resolution_failed", output)
        self.assertIn("Pass --topic <topic-id>", output)
        self.assertIn("Mutated: false", output)

    def test_template_context_skips_unrelated_capability_validation(self) -> None:
        root = self.make_project()
        skipped = (
            "validate_callback_registry_refs",
            "validate_project_toolboxes",
            "_validate_template_registrations",
            "_validate_profile_registrations",
            "_validate_topic_config_profile_defaults",
            "_validate_profile_files",
        )
        patches = [
            patch(
                f"isomer_labs.project.validation.{name}",
                side_effect=AssertionError(f"template context called {name}"),
            )
            for name in skipped
        ]
        with contextlib.ExitStack() as stack:
            for capability_patch in patches:
                stack.enter_context(capability_patch)
            status, listed = self.run_templates(root, ["list"])
        self.assertEqual(0, status, listed)

    def test_template_context_loads_only_the_selected_topic_config(self) -> None:
        root = self.make_project()
        manifest_path = root / ".isomer-labs" / "manifest.toml"
        write(
            manifest_path,
            manifest_path.read_text(encoding="utf-8")
            + """

            [[research_topics]]
            id = "beta"
            config_path = ".isomer-labs/research-topics/beta.toml"
            topic_workspace_id = "beta"
            status = "active"

            [[topic_workspaces]]
            id = "beta"
            research_topic_id = "beta"
            path = "topic-workspaces/beta"
            status = "active"
            """,
        )
        write(root / ".isomer-labs" / "research-topics" / "beta.toml", "this is not valid toml = [")
        (root / "topic-workspaces" / "beta").mkdir(parents=True)
        status, listed = self.run_templates(root, ["list"])
        self.assertEqual(0, status, listed)

    def test_list_uses_exact_index_query_and_preserves_index_guidance(self) -> None:
        root = self.make_project()
        indexed_payload = {
            "ok": True,
            "mutated": False,
            "operation": "query.list",
            "count": 1,
            "records": [
                {
                    "record_id": "artifact-template-1",
                    "record_kind": "artifact",
                    "research_topic_id": "alpha",
                    "topic_workspace_id": "alpha",
                    "status": "ready",
                    "updated_at": "2026-07-13T12:00:00Z",
                    "metadata": {
                        "transition_metadata": {
                            "template_name": "main",
                            "venue": "acl",
                            "paper_type": "survey",
                        },
                    },
                },
            ],
            "diagnostics": [
                {
                    "code": "ISO249",
                    "severity": "warning",
                    "message": "Index is stale; run the explicit index rebuild command.",
                },
            ],
        }
        with patch("isomer_labs.cli.commands.research_templates_ext.query_index_list") as query_mock:
            query_mock.return_value = (indexed_payload, [])
            status, listed = self.run_templates(root, ["list", "--venue", "acl"])
        self.assertEqual(0, status, listed)
        self.assertEqual("list", listed["operation"])
        self.assertEqual(indexed_payload["diagnostics"], listed["diagnostics"])
        self.assertEqual(1, len(listed["records"]))
        kwargs = query_mock.call_args.kwargs
        self.assertEqual(TEMPLATE_SEMANTIC_ID, kwargs["semantic_id"])
        self.assertEqual(20, kwargs["limit"])

    def test_list_ignores_unrelated_lifecycle_records_without_scanning_them(self) -> None:
        root = self.make_project()
        status, output = self.run_main(
            [
                "--print-json",
                "ext",
                "research",
                "records",
                "create",
                "--record-kind",
                "artifact",
                "--semantic-id",
                "KAOJU:UNRELATED-ARTIFACT",
                "--project",
                str(root),
                "--topic",
                "alpha",
            ],
            cwd=root,
        )
        self.assertEqual(0, status, output)
        with patch("isomer_labs.cli.commands.research_templates_ext._compile_preview") as compile_mock:
            compile_mock.return_value = {
                "ok": True,
                "engine": "tectonic",
                "fallback": False,
                "fallback_reason": None,
                "attempts": [],
                "preview_pdf": "",
            }
            status, created = self.run_templates(root, ["create"])
        self.assertEqual(0, status, created)
        with patch("isomer_labs.records.store.list_records", side_effect=AssertionError("template list scanned lifecycle records")):
            status, listed = self.run_templates(root, ["list"])
        self.assertEqual(0, status, listed)
        self.assertEqual(1, len(listed["records"]))
        self.assertEqual(TEMPLATE_SEMANTIC_ID, listed["records"][0]["transition_metadata"]["semantic_id"])

    def test_list_reports_stale_index_schema_with_rebuild_guidance(self) -> None:
        root = self.make_project()
        database_error = OperationalError(
            "SELECT research_record_index.artifact_family",
            {},
            Exception("no such column: research_record_index.artifact_family"),
        )
        with patch("isomer_labs.records.index._query_records", side_effect=database_error):
            status, output = self.run_main(
                ["ext", "research", "templates", "list", "--project", str(root), "--topic", "alpha"],
                cwd=root,
            )
        self.assertEqual(1, status, output)
        self.assertIn("query_index_unavailable", output)
        self.assertIn("index rebuild", output)
        self.assertIn("Mutated: false", output)

    def test_full_project_validation_retains_capability_validation(self) -> None:
        root = self.make_project()
        names = (
            "validate_callback_registry_refs",
            "validate_project_toolboxes",
            "_validate_template_registrations",
            "_validate_profile_registrations",
            "_validate_topic_config_profile_defaults",
            "_validate_profile_files",
        )
        mocks: list[MagicMock] = []
        with contextlib.ExitStack() as stack:
            for name in names:
                mocks.append(stack.enter_context(patch(f"isomer_labs.project.validation.{name}", return_value=[])))
            status, output = self.run_main(
                ["--print-json", "project", "validate", "--project", str(root)],
                cwd=root,
            )
        self.assertEqual(0, status, output)
        for validator in mocks:
            validator.assert_called_once()


class ResearchExtensionErrorExamplesTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def run_main(self, args: list[str], *, cwd: Path) -> tuple[int, str]:
        stdout = io.StringIO()
        with (
            contextlib.chdir(cwd),
            patch.dict(os.environ, {"HOME": str(cwd), "PATH": os.environ.get("PATH", "")}, clear=True),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(args)
        return status, stdout.getvalue()

    def _examples_for(self, group_args: list[str]) -> list[str]:
        root = self.make_root()
        status, output = self.run_main(["--print-json", *group_args, "not-a-command"], cwd=root)
        self.assertEqual(2, status)
        payload = json.loads(output)
        diagnostics = payload.get("diagnostics", [])
        self.assertTrue(diagnostics)
        examples = diagnostics[0].get("examples", [])
        return [str(example) for example in examples]

    def test_templates_unknown_command_shows_templates_examples(self) -> None:
        examples = self._examples_for(["ext", "research", "templates"])
        self.assertTrue(any("ext research templates create" in example for example in examples))
        self.assertTrue(any("ext research templates list" in example for example in examples))
        self.assertTrue(any("ext research templates show" in example for example in examples))

    def test_records_unknown_command_shows_records_examples(self) -> None:
        examples = self._examples_for(["ext", "research", "records"])
        self.assertTrue(any("ext research records list" in example for example in examples))
        self.assertTrue(any("ext research records show" in example for example in examples))

    def test_ideas_unknown_command_shows_ideas_examples(self) -> None:
        examples = self._examples_for(["ext", "research", "ideas"])
        self.assertTrue(any("ext research ideas list" in example for example in examples))
        self.assertTrue(any("ext research ideas graph" in example for example in examples))


class FindTemplateRecordTests(unittest.TestCase):
    def test_find_template_record_uses_query_index_not_list_records(self) -> None:
        context = MagicMock()
        record_id = "artifact-test-123"
        query_payload = {
            "ok": True,
            "records": [
                {
                    "record_id": record_id,
                    "status": "ready",
                    "metadata": {
                        "transition_metadata": {
                            "template_name": "main",
                            "semantic_id": TEMPLATE_SEMANTIC_ID,
                        },
                    },
                }
            ],
        }
        with (
            patch("isomer_labs.cli.commands.research_templates_ext.query_index_list") as query_mock,
            patch("isomer_labs.records.store.list_records") as list_mock,
        ):
            query_mock.return_value = (query_payload, [])
            found = _find_template_record(context, "main")
        self.assertIsNotNone(found)
        assert isinstance(found, dict)
        self.assertEqual(record_id, found["id"])
        self.assertEqual("ready", found["status"])
        self.assertEqual("main", found["transition_metadata"]["template_name"])
        query_mock.assert_called_once()
        self.assertEqual(TEMPLATE_SEMANTIC_ID, query_mock.call_args.kwargs["semantic_id"])
        self.assertEqual("ready", query_mock.call_args.kwargs["status"])
        self.assertIsNone(query_mock.call_args.kwargs["limit"])
        list_mock.assert_not_called()

    def test_find_template_record_skips_archived(self) -> None:
        context = MagicMock()
        query_payload = {
            "ok": True,
            "records": [
                {
                    "record_id": "archived-record",
                    "status": "archived",
                    "metadata": {
                        "transition_metadata": {"template_name": "main"},
                    },
                }
            ],
        }
        with patch("isomer_labs.cli.commands.research_templates_ext.query_index_list") as query_mock:
            query_mock.return_value = (query_payload, [])
            found = _find_template_record(context, "main")
        self.assertIsNone(found)

    def test_indexed_row_mapping_preserves_template_summary_fields(self) -> None:
        summary = _template_summary_from_index_row(
            {
                "record_id": "artifact-template-1",
                "record_kind": "artifact",
                "research_topic_id": "alpha",
                "topic_workspace_id": "alpha",
                "status": "ready",
                "updated_at": "2026-07-13T12:00:00Z",
                "metadata": {
                    "lifecycle_refs": {"run_id": "run-1"},
                    "transition_metadata": {
                        "template_name": "main",
                        "venue": "acl",
                        "paper_type": "survey",
                        "preview_status": "ready",
                    },
                },
            }
        )
        assert summary is not None
        self.assertEqual("artifact-template-1", summary["id"])
        self.assertEqual("acl", summary["venue"])
        self.assertEqual("survey", summary["paper_type"])
        self.assertEqual("ready", summary["preview_status"])
        self.assertEqual("2026-07-13T12:00:00Z", summary["updated_at"])
        self.assertTrue(summary["is_default"])


if __name__ == "__main__":
    unittest.main()
