from __future__ import annotations

import unittest
from pathlib import Path

from isomer_labs.kaoju.execution import ExecutionAdapterCommandRequest


class KaojuExecutionTests(unittest.TestCase):
    def test_remaining_extension_points_still_create_requests(self) -> None:
        cases = {
            "pixi_mutation": ("pixi", "add", "example"),
            "smoke_run": ("pixi", "run", "--environment", "test", "python", "-c", "pass"),
            "code_trial": ("pixi", "run", "--environment", "test", "python", "trial.py"),
            "document_build": ("typst", "compile", "paper.typ"),
            "viewer_launch": ("viewer", "serve"),
            "service_dispatch": ("service", "run"),
        }

        for extension_point, argv in cases.items():
            with self.subTest(extension_point=extension_point):
                request = ExecutionAdapterCommandRequest.create(
                    extension_point=extension_point,
                    argv=argv,
                    cwd=Path("."),
                    timeout_seconds=30,
                )
                self.assertEqual(extension_point, request.extension_point)
                self.assertEqual(argv, request.argv)

    def test_repository_execution_is_not_an_extension_point(self) -> None:
        with self.assertRaisesRegex(ValueError, "Unsupported Research Operation Extension Point"):
            ExecutionAdapterCommandRequest.create(
                extension_point="repository_" "acquisition",
                argv=("git", "clone", "https://example.invalid/repo.git"),
                cwd=Path("."),
                timeout_seconds=30,
            )


if __name__ == "__main__":
    unittest.main()
