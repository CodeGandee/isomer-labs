from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts.validate_docs import (
    FORBIDDEN_TERMS,
    REQUIRED_PAGES,
    check_cli_error_example_registry,
    check_cli_coverage,
    check_forbidden_terms,
    check_legacy_workspace_paths,
    check_readme_links,
    check_required_pages,
    check_semantic_path_documentation,
    check_stale_isomer_cli_json_examples,
    get_public_commands,
)
from isomer_labs.cli.examples import COMMAND_EXAMPLES


class ValidateDocsTests(unittest.TestCase):
    def _manual_docs_dir(self, root: Path) -> Path:
        path = root / "docs" / "manual"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def test_required_pages_pass_when_present(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for relative in REQUIRED_PAGES:
                (root / relative).parent.mkdir(parents=True, exist_ok=True)
                (root / relative).write_text("# page\n", encoding="utf-8")
            self.assertEqual([], check_required_pages(root))

    def test_required_pages_fail_when_missing(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            issues = check_required_pages(root)
            self.assertEqual(len(REQUIRED_PAGES), len(issues))
            self.assertTrue(all("Missing required docs page" in issue for issue in issues))

    def test_readme_links_pass_with_docs_index(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("See [docs](docs/index.md).", encoding="utf-8")
            self.assertEqual([], check_readme_links(root))

    def test_readme_links_fail_without_docs_link(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("# Project\n", encoding="utf-8")
            issues = check_readme_links(root)
            self.assertEqual(1, len(issues))

    def test_cli_coverage_passes_when_commands_present(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            manual = self._manual_docs_dir(root)
            (manual / "cli-reference.md").write_text(
                "## Commands\n\n`init`\n`doctor`\n`validate`\n",
                encoding="utf-8",
            )
            self.assertEqual([], check_cli_coverage(root, ["init", "doctor", "validate"]))

    def test_cli_coverage_fails_when_command_missing(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            manual = self._manual_docs_dir(root)
            (manual / "cli-reference.md").write_text(
                "## Commands\n\n`init`\n`doctor`\n",
                encoding="utf-8",
            )
            issues = check_cli_coverage(root, ["init", "doctor", "validate"])
            self.assertEqual(1, len(issues))
            self.assertIn("validate", issues[0])

    def test_public_command_discovery_is_deterministic_with_parallel_help(self) -> None:
        help_by_args = {
            (): "Commands:\n  project\n  schemas\n",
            ("project",): "Commands:\n  topics\n  validate\n",
            ("project", "topics"): "Commands:\n  create\n  list\n",
            ("project", "topics", "create"): "Usage: create\n",
            ("project", "topics", "list"): "Usage: list\n",
            ("project", "validate"): "Usage: validate\n",
            ("schemas",): "Commands:\n  list\n",
            ("schemas", "list"): "Usage: list\n",
        }

        def fake_help(args: list[str]) -> str:
            return help_by_args[tuple(args)]

        with patch("scripts.validate_docs.run_cli_help", side_effect=fake_help):
            self.assertEqual(
                [
                    "project topics create",
                    "project topics list",
                    "project validate",
                    "schemas list",
                ],
                get_public_commands(max_workers=4),
            )

    def test_forbidden_terms_detected(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "concepts.md").write_text(
                "This page uses quest workspace by mistake.\n", encoding="utf-8"
            )
            issues = check_forbidden_terms(root)
            self.assertTrue(any("quest" in issue for issue in issues))

    def test_forbidden_terms_pass_when_clean(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = root / "docs"
            docs.mkdir()
            (docs / "concepts.md").write_text(
                "This page uses Research Topic and Topic Workspace.\n", encoding="utf-8"
            )
            issues = check_forbidden_terms(root)
            self.assertEqual([], issues)

    def test_forbidden_term_list_is_non_empty(self) -> None:
        self.assertTrue(FORBIDDEN_TERMS)

    def test_stale_isomer_cli_json_examples_are_reported(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            manual = self._manual_docs_dir(root)
            (root / "README.md").write_text("pixi run isomer-cli validate --json\n", encoding="utf-8")
            (manual / "cli-reference.md").write_text("pixi run isomer-cli --print-json validate\n", encoding="utf-8")
            issues = check_stale_isomer_cli_json_examples(root)
            self.assertEqual(1, len(issues))
            self.assertIn("--print-json", issues[0])

    def test_houmao_print_json_examples_are_allowed(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "README.md").write_text("houmao-mgr --print-json system-skills list\n", encoding="utf-8")
            (root / "docs" / "houmao.md").write_text("pixi run isomer-cli --print-json validate\n", encoding="utf-8")
            self.assertEqual([], check_stale_isomer_cli_json_examples(root))

    def test_cli_error_example_registry_requires_documented_examples(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = self._manual_docs_dir(root)
            all_examples = list(dict.fromkeys(example for examples in COMMAND_EXAMPLES.values() for example in examples))
            (docs / "cli-reference.md").write_text("\n".join(all_examples[1:]), encoding="utf-8")
            issues = check_cli_error_example_registry(root)
            self.assertTrue(any(all_examples[0] in issue for issue in issues), issues)

            (docs / "cli-reference.md").write_text("\n".join(all_examples), encoding="utf-8")
            self.assertEqual([], check_cli_error_example_registry(root))

    def test_legacy_workspace_paths_are_reported_outside_breaking_layout_notes(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "README.md").write_text("Current layout uses .isomer-agent/ for support.\n", encoding="utf-8")
            (root / "docs" / "topic.md").write_text("Use repos/topic-main/artifacts for worker outputs.\n", encoding="utf-8")
            issues = check_legacy_workspace_paths(root)
            self.assertEqual(2, len(issues))
            self.assertTrue(all("isomer-managed/" in issue for issue in issues))

    def test_legacy_workspace_paths_are_allowed_in_breaking_layout_notes(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "README.md").write_text("## Breaking Layout Diagnostics\n\nOld .isomer-agent/ paths are breaking diagnostics.\n", encoding="utf-8")
            (root / "docs" / "topic.md").write_text(
                "Legacy repos/topic-main/artifacts paths must be reported as breaking diagnostics.\n",
                encoding="utf-8",
            )
            self.assertEqual([], check_legacy_workspace_paths(root))

    def test_semantic_path_documentation_requires_commands_and_manifest_terms(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = self._manual_docs_dir(root)
            (root / "README.md").write_text("No tmp wording here.\n", encoding="utf-8")
            (docs / "cli-reference.md").write_text("project paths get\nproject paths list\n", encoding="utf-8")
            (docs / "topic-workspaces.md").write_text("Topic Workspace paths only.\n", encoding="utf-8")
            issues = check_semantic_path_documentation(root)
            self.assertTrue(any("project paths materialize-default" in issue for issue in issues), issues)
            self.assertTrue(any("topic-workspace.toml" in issue for issue in issues), issues)

    def test_semantic_path_documentation_flags_fixed_path_only_and_tmp_wording(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = self._manual_docs_dir(root)
            (root / "README.md").write_text("tmp/ exists here.\n", encoding="utf-8")
            (docs / "cli-reference.md").write_text(
                "project paths get\nproject paths list\nproject paths materialize-default\n",
                encoding="utf-8",
            )
            (docs / "topic-workspaces.md").write_text(
                "topic-workspace.toml and isomer-default.v1 are documented.\nAgent Workspace must use agents/<agent-name>.\n",
                encoding="utf-8",
            )
            issues = check_semantic_path_documentation(root)
            self.assertTrue(any("fixed-path-only" in issue for issue in issues), issues)
            self.assertTrue(any("tmp/ wording" in issue for issue in issues), issues)

    def test_semantic_path_documentation_passes_label_first_wording(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            docs = self._manual_docs_dir(root)
            (root / "README.md").write_text(
                "Implemented tmp/ surfaces use topic.tmp, topic.repos.main.tmp, and agent.tmp; they are local, ignored, disposable, and not durable evidence.\n",
                encoding="utf-8",
            )
            (docs / "cli-reference.md").write_text(
                "project paths default\nproject paths explain\nproject paths get\nproject paths list\nproject paths materialize\nproject paths materialize-default\nproject paths register\nproject paths reset\nproject paths unregister\nproject paths update\nproject repos create\n--storage-profile\nISOMER_PATH__TOPIC__REPOS__MAIN\nISOMER_PATH__CUSTOM__DATASETS__RAW\n--configured\n",
                encoding="utf-8",
            )
            (docs / "topic-workspaces.md").write_text(
                "topic-workspace.toml and isomer-default.v1 are documented. Bindings use label, path, and storage_profile. User labels use custom.* and repository groups use topic.repos.<group...>.<repo-name>. Agent Workspace defaults to agents/<agent-name> through agent.workspace.\n",
                encoding="utf-8",
            )
            self.assertEqual([], check_semantic_path_documentation(root))


if __name__ == "__main__":
    unittest.main()
