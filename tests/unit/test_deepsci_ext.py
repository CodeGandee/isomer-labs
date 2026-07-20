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
from isomer_labs.artifact_formats import ArtifactFormatResolver, ArtifactFormatRegistry
from isomer_labs.deepsci_ext.tools import ARTIFACT_TOOLS, BASH_EXEC_TOOLS, MEMORY_TOOLS, TOOL_ARGUMENT_KEYS
from isomer_labs.deepsci_ext.record_formats import (
    active_deepsci_binding_profile_names,
    canonical_record_format_ref,
    register_deepsci_record_format_provider,
)
from isomer_labs.skills.system_assets import iter_system_skill_capabilities, resolve_system_skill, resolve_system_skill_capability


REPO_ROOT = Path(__file__).resolve().parents[2]
CONTRACT_FIXTURE = REPO_ROOT / "tests" / "fixtures" / "deepsci_ext" / "deepscientist_contract.json"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def load_contract() -> dict[str, object]:
    return json.loads(CONTRACT_FIXTURE.read_text(encoding="utf-8"))


def assert_required_keys(test: unittest.TestCase, payload: dict[str, object], fixture_key: str) -> None:
    contract = load_contract()
    response_keys = contract["required_response_keys"]
    assert isinstance(response_keys, dict)
    required = response_keys[fixture_key]
    assert isinstance(required, list)
    missing = sorted(str(key) for key in required if str(key) not in payload)
    test.assertEqual([], missing, payload)


class DeepScientistCompatibilityExtensionTests(unittest.TestCase):
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

    def run_deepsci(self, root: Path, tool_name: str, payload: dict[str, object]) -> tuple[int, dict[str, object]]:
        status, output = self.run_main(
            [
                "ext",
                "deepsci",
                "call",
                tool_name,
                "--project",
                str(root),
                "--topic",
                "alpha",
                "--input-json",
                json.dumps(payload),
            ],
            cwd=root,
        )
        return status, json.loads(output)

    def runtime_db(self, root: Path) -> Path:
        return root / "topic-workspaces" / "alpha" / "state.sqlite"

    def test_registry_matches_deepscientist_contract_fixture(self) -> None:
        contract = load_contract()
        self.assertEqual(contract["memory_tools"], list(MEMORY_TOOLS))
        self.assertEqual(contract["artifact_tools"], list(ARTIFACT_TOOLS))
        self.assertEqual(contract["bash_exec_tools"], list(BASH_EXEC_TOOLS))
        expected_args = contract["tool_argument_keys"]
        assert isinstance(expected_args, dict)
        for tool_name, keys in expected_args.items():
            self.assertEqual(keys, list(TOOL_ARGUMENT_KEYS[str(tool_name)]))

    def test_record_format_provider_covers_active_deepsci_binding_profiles(self) -> None:
        registry = ArtifactFormatRegistry()
        register_deepsci_record_format_provider(registry)
        resolver = ArtifactFormatResolver(registry)
        active = {canonical_record_format_ref(profile_name, "profile") for profile_name in active_deepsci_binding_profile_names()}
        discovered: set[str] = set()
        pack_root = resolve_system_skill("research-paradigm/deepsci/isomer-ext-deepsci-entrypoint")
        binding_paths = [pack_root / "placeholder-bindings.md"]
        binding_paths.extend(
            resolve_system_skill_capability(capability.logical_id) / "placeholder-bindings.md"
            for capability in iter_system_skill_capabilities("deepsci")
        )
        for binding in sorted(path for path in binding_paths if path.is_file()):
            for line in binding.read_text(encoding="utf-8").splitlines():
                if not (line.startswith("| DEEPSCI:") or line.startswith("| `DEEPSCI:")):
                    continue
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if len(cells) >= 6:
                    discovered.add(cells[5].strip("`"))
        self.assertTrue(discovered)
        self.assertEqual(discovered, active)
        for profile_ref in sorted(discovered):
            profile, _resolution, diagnostics = resolver.resolve_profile(profile_ref)
            self.assertEqual([], diagnostics, profile_ref)
            self.assertIsNotNone(profile, profile_ref)

    def test_tools_command_lists_memory_tools(self) -> None:
        root = self.make_project()
        status, output = self.run_main(["ext", "deepsci", "tools", "memory"], cwd=root)
        self.assertEqual(0, status, output)
        payload = json.loads(output)
        self.assertEqual(True, payload["ok"])
        self.assertEqual(list(MEMORY_TOOLS), payload["tools"])

    def test_memory_tools_round_trip_through_sqlite_without_deepscientist_layout(self) -> None:
        root = self.make_project()
        status, written = self.run_deepsci(
            root,
            "memory.write",
            {
                "kind": "knowledge",
                "title": "Storage finding",
                "body": "retrieval works from sqlite",
                "scope": "quest",
                "tags": "stage:mock, type:storage",
                "metadata": {"source": "unit-test"},
            },
        )
        self.assertEqual(0, status, written)
        self.assertNotIn("output_schema_version", written)
        assert_required_keys(self, written, "memory.write")
        self.assertEqual(["stage:mock", "type:storage"], written["metadata"]["tags"])

        status, search = self.run_deepsci(root, "memory.search", {"query": "retrieval", "scope": "quest", "limit": 10})
        self.assertEqual(0, status, search)
        assert_required_keys(self, search, "memory.search")
        self.assertEqual(1, search["count"])
        item = search["items"][0]
        self.assertIn("document_id", item)
        self.assertEqual("knowledge", item["type"])

        status, recent = self.run_deepsci(root, "memory.list_recent", {"scope": "both", "limit": 10})
        self.assertEqual(0, status, recent)
        assert_required_keys(self, recent, "memory.list_recent")
        self.assertEqual(1, recent["count"])

        db_path = self.runtime_db(root)
        with sqlite3.connect(db_path) as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table' AND name LIKE 'deepsci_compat_%'"
                )
            }
            self.assertIn("deepsci_compat_memory_cards", tables)
            row = connection.execute("SELECT COUNT(*) FROM deepsci_compat_memory_cards").fetchone()
            self.assertEqual(1, row[0])
        self.assertFalse((root / "topic-workspaces" / "alpha" / "memory").exists())

    def test_artifact_calls_preserve_input_shape_and_do_not_mutate_external_state(self) -> None:
        root = self.make_project()
        write(root / "topic-workspaces" / "alpha" / "brief.md", "Line 1\nLine 2\n")
        status, state = self.run_deepsci(root, "artifact.get_quest_state", {"detail": "full"})
        self.assertEqual(0, status, state)
        assert_required_keys(self, state, "artifact.get_quest_state")
        self.assertEqual(True, state["mocked"])
        self.assertEqual("mocked", state["quest_state"]["runtime_status"])

        status, docs = self.run_deepsci(root, "artifact.read_quest_documents", {"names": ["brief"], "mode": "excerpt", "max_lines": 1})
        self.assertEqual(0, status, docs)
        assert_required_keys(self, docs, "artifact.read_quest_documents")
        self.assertEqual("Line 1", docs["items"][0]["content"])

        request_payload = {"payload": {"kind": "decision", "snake_field": "kept"}}
        status, record = self.run_deepsci(root, "artifact.record", request_payload)
        self.assertEqual(0, status, record)
        self.assertEqual(True, record["mocked"])
        with sqlite3.connect(self.runtime_db(root)) as connection:
            row = connection.execute(
                "SELECT request_json FROM deepsci_compat_artifact_calls WHERE tool_name = 'artifact.record' ORDER BY sequence DESC LIMIT 1"
            ).fetchone()
        self.assertEqual(request_payload, json.loads(row[0]))

        status, git_payload = self.run_deepsci(root, "artifact.git", {"action": "status"})
        self.assertEqual(0, status, git_payload)
        self.assertEqual(True, git_payload["mocked"])
        self.assertFalse((root / "topic-workspaces" / "alpha" / ".git").exists())

    def test_unsupported_tool_returns_raw_error_without_writing_rows(self) -> None:
        root = self.make_project()
        status, first = self.run_deepsci(root, "artifact.get_quest_state", {})
        self.assertEqual(0, status, first)
        with sqlite3.connect(self.runtime_db(root)) as connection:
            before = connection.execute("SELECT COUNT(*) FROM deepsci_compat_artifact_calls").fetchone()[0]
        status, output = self.run_main(
            [
                "ext",
                "deepsci",
                "call",
                "artifact.unknown_tool",
                "--project",
                str(root),
                "--topic",
                "alpha",
                "--input-json",
                "{}",
            ],
            cwd=root,
        )
        self.assertEqual(1, status, output)
        payload = json.loads(output)
        self.assertEqual(False, payload["ok"])
        self.assertEqual("unsupported_tool", payload["error"]["code"])
        with sqlite3.connect(self.runtime_db(root)) as connection:
            after = connection.execute("SELECT COUNT(*) FROM deepsci_compat_artifact_calls").fetchone()[0]
        self.assertEqual(before, after)

    def test_bash_exec_mock_sessions_do_not_launch_or_kill_processes(self) -> None:
        root = self.make_project()
        with patch("subprocess.Popen", side_effect=AssertionError("no subprocess should launch")):
            status, detach = self.run_deepsci(root, "bash_exec.bash_exec", {"mode": "detach", "command": "echo hello"})
        self.assertEqual(0, status, detach)
        assert_required_keys(self, detach, "bash_exec.bash_exec.detach")
        self.assertEqual(True, detach["mocked"])
        self.assertEqual("running", detach["status"])
        self.assertTrue(str(detach["log_path"]).startswith("sqlite://"))

        status, read_payload = self.run_deepsci(root, "bash_exec.bash_exec", {"mode": "read", "id": detach["bash_id"]})
        self.assertEqual(0, status, read_payload)
        assert_required_keys(self, read_payload, "bash_exec.bash_exec.read")
        self.assertIn("Command was not executed", read_payload["log"])

        status, listed = self.run_deepsci(root, "bash_exec.bash_exec", {"mode": "list"})
        self.assertEqual(0, status, listed)
        assert_required_keys(self, listed, "bash_exec.bash_exec.list")
        self.assertEqual(1, listed["count"])

        status, history = self.run_deepsci(root, "bash_exec.bash_exec", {"mode": "history"})
        self.assertEqual(0, status, history)
        assert_required_keys(self, history, "bash_exec.bash_exec.history")
        self.assertEqual(1, history["count"])

        with patch("os.kill", side_effect=AssertionError("no process should be killed")):
            status, killed = self.run_deepsci(root, "bash_exec.bash_exec", {"mode": "kill", "id": detach["bash_id"]})
        self.assertEqual(0, status, killed)
        self.assertEqual("stopped", killed["status"])


if __name__ == "__main__":
    unittest.main()
