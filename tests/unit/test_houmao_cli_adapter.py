from __future__ import annotations

import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

from isomer_labs.houmao_cli_adapter import (
    HOUMAO_COMMAND_ENV,
    HoumaoCommandCatalog,
    HoumaoCommandRunner,
)


class HoumaoCliAdapterTests(unittest.TestCase):
    def test_adapter_import_does_not_import_houmao(self) -> None:
        self.assertNotIn("houmao", sys.modules)

    def test_command_catalog_uses_print_json_boundary(self) -> None:
        catalog = HoumaoCommandCatalog()
        project_dir = Path("/tmp/project")
        self.assertEqual(["--version"], catalog.version().args)
        self.assertEqual(["--print-json", "system-skills", "list"], catalog.system_skills_list().args)
        self.assertEqual(
            ["--print-json", "project", "--project-dir", str(project_dir), "agents", "list"],
            catalog.agents_list(project_dir).args,
        )
        self.assertEqual(
            ["--print-json", "agents", "global", "list", "--state", "all"],
            catalog.global_agents_list().args,
        )

    def test_runner_parses_json_success(self) -> None:
        runner = HoumaoCommandRunner(Path("/tmp/project"), env={HOUMAO_COMMAND_ENV: "houmao-mgr"})
        completed = subprocess.CompletedProcess(["houmao-mgr"], 0, stdout='{"ok": true}\n', stderr="")
        with patch("isomer_labs.houmao_cli_adapter.subprocess.run", return_value=completed):
            result = runner.run(HoumaoCommandCatalog().system_skills_list())
        self.assertTrue(result.succeeded)
        self.assertEqual({"ok": True}, result.parsed_json)
        self.assertEqual("succeeded", result.status)

    def test_runner_reports_invalid_json_nonzero_and_timeout(self) -> None:
        runner = HoumaoCommandRunner(Path("/tmp/project"), env={HOUMAO_COMMAND_ENV: "houmao-mgr"})
        catalog = HoumaoCommandCatalog()
        invalid = subprocess.CompletedProcess(["houmao-mgr"], 0, stdout="not-json\n", stderr="")
        with patch("isomer_labs.houmao_cli_adapter.subprocess.run", return_value=invalid):
            invalid_result = runner.run(catalog.system_skills_list())
        self.assertEqual("invalid_json", invalid_result.status)
        self.assertIn("ISO071", {diagnostic.code for diagnostic in invalid_result.diagnostics})

        nonzero = subprocess.CompletedProcess(["houmao-mgr"], 2, stdout='{"ok": false}\n', stderr="failed")
        with patch("isomer_labs.houmao_cli_adapter.subprocess.run", return_value=nonzero):
            nonzero_result = runner.run(catalog.system_skills_list())
        self.assertEqual("failed", nonzero_result.status)
        self.assertIn("ISO072", {diagnostic.code for diagnostic in nonzero_result.diagnostics})

        with patch(
            "isomer_labs.houmao_cli_adapter.subprocess.run",
            side_effect=subprocess.TimeoutExpired(["houmao-mgr"], 1, output="", stderr="late"),
        ):
            timeout_result = runner.run(catalog.system_skills_list(), timeout_seconds=1)
        self.assertEqual("timed_out", timeout_result.status)
        self.assertIn("ISO073", {diagnostic.code for diagnostic in timeout_result.diagnostics})


if __name__ == "__main__":
    unittest.main()
