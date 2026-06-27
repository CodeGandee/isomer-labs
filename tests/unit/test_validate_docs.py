from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from scripts.validate_docs import (
    FORBIDDEN_TERMS,
    REQUIRED_PAGES,
    check_cli_coverage,
    check_forbidden_terms,
    check_legacy_workspace_paths,
    check_readme_links,
    check_required_pages,
    check_stale_isomer_cli_json_examples,
)


class ValidateDocsTests(unittest.TestCase):
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
            (root / "docs").mkdir()
            (root / "docs" / "isomer-cli.md").write_text(
                "## Commands\n\n`init`\n`doctor`\n`validate`\n",
                encoding="utf-8",
            )
            self.assertEqual([], check_cli_coverage(root, ["init", "doctor", "validate"]))

    def test_cli_coverage_fails_when_command_missing(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs" / "isomer-cli.md").write_text(
                "## Commands\n\n`init`\n`doctor`\n",
                encoding="utf-8",
            )
            issues = check_cli_coverage(root, ["init", "doctor", "validate"])
            self.assertEqual(1, len(issues))
            self.assertIn("validate", issues[0])

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
            (root / "docs").mkdir()
            (root / "README.md").write_text("pixi run isomer-cli validate --json\n", encoding="utf-8")
            (root / "docs" / "isomer-cli.md").write_text("pixi run isomer-cli --print-json validate\n", encoding="utf-8")
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

    def test_legacy_workspace_paths_are_reported_outside_migration_notes(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "README.md").write_text("Current layout uses .isomer-agent/ for support.\n", encoding="utf-8")
            (root / "docs" / "topic.md").write_text("Use repos/topic-main/artifacts for worker outputs.\n", encoding="utf-8")
            issues = check_legacy_workspace_paths(root)
            self.assertEqual(2, len(issues))
            self.assertTrue(all("isomer-managed/" in issue for issue in issues))

    def test_legacy_workspace_paths_are_allowed_in_migration_notes(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "README.md").write_text("## Legacy Layout Migration\n\nOld .isomer-agent/ paths are migration diagnostics.\n", encoding="utf-8")
            (root / "docs" / "topic.md").write_text(
                "Legacy repos/topic-main/artifacts paths must be reported as migration diagnostics.\n",
                encoding="utf-8",
            )
            self.assertEqual([], check_legacy_workspace_paths(root))


if __name__ == "__main__":
    unittest.main()
