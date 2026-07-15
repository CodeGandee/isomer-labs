from __future__ import annotations

import contextlib
import json
from pathlib import Path
import tempfile
import unittest

from click.testing import CliRunner

from isomer_labs import cli
from isomer_labs.kaoju.artifacts import KaojuArtifactService
from isomer_labs.kaoju.contracts import describe_binding, load_binding_registry


class KaojuResourceCliTests(unittest.TestCase):
    def invoke(self, args: list[str], *, cwd: Path) -> tuple[int, str]:
        with contextlib.chdir(cwd):
            result = CliRunner().invoke(cli.app, args, standalone_mode=False)
        if result.exception is not None:
            raise result.exception
        return int(result.return_value or 0), result.output

    def json_invoke(self, args: list[str], *, cwd: Path) -> tuple[int, dict[str, object]]:
        status, output = self.invoke(["--print-json", *args], cwd=cwd)
        value = json.loads(output)
        self.assertIsInstance(value, dict)
        return status, value

    def test_resource_groups_have_discoverable_help(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            cases = (
                (["ext", "kaoju", "--help"], ("process", "bindings")),
                (["ext", "kaoju", "process", "--help"], ("show",)),
                (["ext", "kaoju", "bindings", "--help"], ("list", "describe")),
            )
            for args, terms in cases:
                with self.subTest(args=args):
                    status, output = self.invoke(args, cwd=cwd)
                    self.assertEqual(0, status)
                    for term in terms:
                        self.assertIn(term, output)

    def test_process_show_is_context_free_and_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            status, first = self.json_invoke(["ext", "kaoju", "process", "show"], cwd=cwd)
            second_status, second = self.json_invoke(["ext", "kaoju", "process", "show"], cwd=cwd)
            self.assertEqual((0, first), (second_status, second))
            self.assertTrue(first["ok"])
            self.assertFalse(first["mutated"])
            process = first["process"]
            self.assertIsInstance(process, dict)
            assert isinstance(process, dict)
            self.assertEqual(
                {
                    "list": "isomer-cli --print-json ext kaoju bindings list",
                    "describe": "isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT",
                },
                process["binding_queries"],
            )
            self.assertNotIn("binding_registry_resource", process)
            self.assertNotIn("semantic_aliases", process)

    def test_binding_list_is_sorted_and_text_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            status, payload = self.json_invoke(["ext", "kaoju", "bindings", "list"], cwd=cwd)
            self.assertEqual(0, status)
            bindings = payload["bindings"]
            self.assertIsInstance(bindings, list)
            assert isinstance(bindings, list)
            semantic_ids = [str(item["semantic_id"]) for item in bindings if isinstance(item, dict)]
            self.assertEqual(sorted(load_binding_registry()), semantic_ids)
            self.assertEqual(len(semantic_ids), payload["count"])
            text_status, first = self.invoke(["ext", "kaoju", "bindings", "list"], cwd=cwd)
            second_status, second = self.invoke(["ext", "kaoju", "bindings", "list"], cwd=cwd)
            self.assertEqual((0, first), (text_status, second))
            self.assertEqual(text_status, second_status)

    def test_binding_describe_matches_shared_loader_and_project_service(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            status, payload = self.json_invoke(
                ["ext", "kaoju", "bindings", "describe", "KAOJU:SURVEY-CONTRACT"],
                cwd=Path(tmp),
            )
            self.assertEqual(0, status)
            expected = describe_binding("KAOJU:SURVEY-CONTRACT")
            self.assertEqual(expected, payload["binding"])
            service = object.__new__(KaojuArtifactService)
            self.assertEqual(expected, service.describe("KAOJU:SURVEY-CONTRACT")["binding"])

    def test_binding_describe_rejects_every_removed_identity_shape(self) -> None:
        cases = {
            "kaoju:survey-contract": "invalid_artifact_identity",
            "Kaoju:SURVEY-CONTRACT": "invalid_artifact_identity",
            "SURVEY-CONTRACT": "invalid_artifact_identity",
            "<KAOJU:SURVEY-CONTRACT>": "invalid_artifact_identity",
            "OTHER:SURVEY-CONTRACT": "artifact_identity_extension_mismatch",
            "KAOJU:PAPER-DRAFT": "unknown_semantic_id",
            "KAOJU:UNKNOWN": "unknown_semantic_id",
        }
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)
            for semantic_id, expected_code in cases.items():
                with self.subTest(semantic_id=semantic_id):
                    status, payload = self.json_invoke(
                        ["ext", "kaoju", "bindings", "describe", semantic_id],
                        cwd=cwd,
                    )
                    self.assertEqual(1, status)
                    error = payload["error"]
                    self.assertIsInstance(error, dict)
                    assert isinstance(error, dict)
                    self.assertEqual(expected_code, error["code"])
                    self.assertEqual(semantic_id, payload["artifact_identity"])


if __name__ == "__main__":
    unittest.main()
