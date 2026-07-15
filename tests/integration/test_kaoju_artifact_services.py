from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from isomer_labs import cli
from isomer_labs.records.store import ResearchRecordError


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class KaojuArtifactServiceIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        write(
            self.root / ".isomer-labs/manifest.toml",
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
            self.root / ".isomer-labs/research-topics/alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            topic_statement = "Alpha survey"
            """,
        )
        write(self.root / "topic-workspaces/alpha/isomer-topic-workspace-summary.md", "# Alpha\n")
        status, output = self.run_cli("project", "--root", str(self.root), "runtime", "init", "--topic", "alpha")
        self.assertEqual(0, status, output)

    def run_cli(self, *arguments: str) -> tuple[int, dict[str, object]]:
        stdout = io.StringIO()
        with (
            contextlib.chdir(self.root),
            patch.dict(os.environ, {"HOME": str(self.root), "PATH": os.environ.get("PATH", "")}, clear=True),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(["--print-json", *arguments])
        return status, json.loads(stdout.getvalue())

    def artifact(self, *arguments: str) -> tuple[int, dict[str, object]]:
        return self.run_cli("project", "--root", str(self.root), "artifacts", *arguments, "--topic", "alpha")

    def direction_payload(self, name: str, title: str) -> Path:
        path = self.root / name
        path.write_text(
            json.dumps(
                {
                    "title": title,
                    "summary": "Actor-confirmed survey directions.",
                    "artifact_family": "kaoju",
                    "semantic_id": "KAOJU:DIRECTION-SET",
                    "artifact_type": "direction-set",
                    "sections": {
                        "proposals": [
                            {
                                "id": "d1",
                                "title": title,
                                "research_question": "Which systems mechanisms are supported by primary evidence?",
                                "boundary": "Systems evidence through 2026-07-14",
                                "source_classes": ["paper", "technical_report", "framework_doc", "repository", "dataset"],
                                "coverage_date": "2026-07-14",
                                "expected_depth": "section-level",
                                "deliverables": ["reading-list", "source-digests"],
                                "empirical_feasibility": "requires-environment-work",
                            },
                            {
                                "id": "d2",
                                "title": "Comparative mechanisms",
                                "research_question": "How do mechanisms differ?",
                                "boundary": "Primary papers",
                                "source_classes": ["paper", "technical_report"],
                                "coverage_date": "2026-07-14",
                                "expected_depth": "full-text",
                                "deliverables": ["comparison"],
                                "empirical_feasibility": "unknown",
                            },
                            {
                                "id": "d3",
                                "title": "Implementation lineage",
                                "research_question": "Which code implements the reported methods?",
                                "boundary": "Verified repositories",
                                "source_classes": ["paper", "repository"],
                                "coverage_date": "2026-07-14",
                                "expected_depth": "code-level",
                                "deliverables": ["source-digests"],
                                "empirical_feasibility": "available",
                            },
                        ],
                        "selections": ["d1"],
                        "confirmation": {"status": "accepted", "actor_ref": "topic-actor:test"},
                    },
                }
            ),
            encoding="utf-8",
        )
        return path

    def test_binding_inference_scoped_revision_and_producer_rejection(self) -> None:
        status, described = self.artifact("describe", "KAOJU:DIRECTION-SET")
        self.assertEqual(0, status, described)
        binding = described["binding"]
        self.assertNotIn("subpath", binding)
        self.assertNotIn("path_template", binding)

        payload = self.direction_payload("direction-v1.json", "Systems")
        relationships = '[{"role":"survey_contract","target_record_id":"contract-v1"}]'
        status, rejected = self.artifact(
            "put",
            "KAOJU:DIRECTION-SET",
            str(payload),
            "--producer",
            "isomer-kaoju-discover",
            "--scope-key",
            "survey-main",
            "--relationships-json",
            relationships,
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_producer_rejected", rejected["error"]["code"])

        status, created = self.artifact(
            "put",
            "KAOJU:DIRECTION-SET",
            str(payload),
            "--producer",
            "isomer-kaoju-frame",
            "--scope-key",
            "survey-main",
            "--relationships-json",
            relationships,
            "--id",
            "directions-v1",
            "--idempotency-key",
            "directions-main-v1",
        )
        self.assertEqual(0, status, created)
        self.assertEqual("directions-v1", created["record"]["id"])
        status, replay = self.artifact(
            "put",
            "KAOJU:DIRECTION-SET",
            str(payload),
            "--producer",
            "isomer-kaoju-frame",
            "--scope-key",
            "survey-main",
            "--relationships-json",
            relationships,
            "--idempotency-key",
            "directions-main-v1",
        )
        self.assertEqual(0, status, replay)
        self.assertTrue(replay["idempotent_replay"])

        revised_payload = self.direction_payload("direction-v2.json", "Systems and compilers")
        status, revised = self.artifact(
            "revise",
            "directions-v1",
            str(revised_payload),
            "--producer",
            "isomer-kaoju-frame",
            "--relationships-json",
            relationships,
            "--id",
            "directions-v2",
        )
        self.assertEqual(0, status, revised)
        status, latest = self.artifact("latest", "KAOJU:DIRECTION-SET", "--scope-key", "survey-main")
        self.assertEqual(0, status, latest)
        self.assertEqual(["directions-v2"], [item["record_id"] for item in latest["records"]])

        for record_id in ("legacy-directions-a", "legacy-directions-b"):
            status, legacy = self.run_cli(
                "ext",
                "research",
                "records",
                "create",
                "--project",
                str(self.root),
                "--topic",
                "alpha",
                "--id",
                record_id,
                "--record-kind",
                "decision_record",
                "--semantic-id",
                "KAOJU:DIRECTION-SET",
                "--format-profile",
                "isomer:research/record-format/profile/kaoju/decision/direction-set/v1",
                "--payload-file",
                str(payload),
            )
            self.assertEqual(0, status, legacy)
        status, ambiguous = self.artifact("latest", "KAOJU:DIRECTION-SET")
        self.assertEqual(1, status)
        self.assertEqual("artifact_latest_ambiguous", ambiguous["error"]["code"])

    def test_directory_manifest_integrity_and_terminal_run_immutability(self) -> None:
        tree = self.root / "template-export"
        write(tree / "template.md", "# Survey\n")
        write(tree / "notes.txt", "human notes\n")
        relationships = '[{"role":"paper_template","target_record_id":"template-v1"},{"role":"paper_draft","target_record_id":"draft-v1"}]'
        status, created = self.artifact(
            "put",
            "KAOJU:PAPER-TEMPLATE-EXPORT",
            str(tree),
            "--producer",
            "isomer-kaoju-write",
            "--scope-key",
            "paper-main:export-1",
            "--relationships-json",
            relationships,
            "--id",
            "template-export-v1",
        )
        self.assertEqual(0, status, created)
        manifest_path = Path(str(created["record"]["content_path"]))
        self.assertEqual(".isomer-artifact-manifest.json", manifest_path.name)
        self.assertIn("research-records", manifest_path.parts)
        status, shown = self.artifact("show", "template-export-v1")
        self.assertEqual(0, status, shown)
        self.assertEqual([], shown["content_diagnostics"])
        (manifest_path.parent / "template.md").write_text("corrupt\n", encoding="utf-8")
        status, corrupt = self.artifact("show", "template-export-v1")
        self.assertEqual(0, status, corrupt)
        self.assertEqual("artifact_content_corrupt", corrupt["content_diagnostics"][0]["code"])

        failed_tree = self.root / "failed-export"
        write(failed_tree / "template.md", "# Failed\n")
        with patch(
            "isomer_labs.kaoju.artifacts.create_record",
            side_effect=ResearchRecordError(
                "simulated DB commit failure",
                code="record_commit_failed",
                payload={"recovery_actions": ["retry"]},
            ),
        ):
            status, failed = self.artifact(
                "put",
                "KAOJU:PAPER-TEMPLATE-EXPORT",
                str(failed_tree),
                "--producer",
                "isomer-kaoju-write",
                "--scope-key",
                "paper-main:failed-export",
                "--relationships-json",
                relationships,
                "--id",
                "failed-template-export",
            )
        self.assertEqual(1, status, failed)
        self.assertEqual("record_commit_failed", failed["error"]["code"])
        failed_owner = self.root / "topic-workspaces/alpha/records/artifacts/research-records/artifact/failed-template-export"
        self.assertFalse(failed_owner.exists())

        status, begun = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "runs",
            "begin",
            "--topic",
            "alpha",
            "--procedure-id",
            "choose-directions",
            "--stage-id",
            "frame",
            "--id",
            "run-directions-1",
        )
        self.assertEqual(0, status, begun)
        status, checkpoint = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "runs",
            "checkpoint",
            "--topic",
            "alpha",
            "run-directions-1",
            "--stage-id",
            "confirm",
            "--completed-ref",
            "directions-v1",
        )
        self.assertEqual(0, status, checkpoint)
        status, completed = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "runs",
            "complete",
            "--topic",
            "alpha",
            "run-directions-1",
            "--terminal-status",
            "complete",
            "--completed-ref",
            "directions-v1",
        )
        self.assertEqual(0, status, completed)
        status, rejected = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "runs",
            "checkpoint",
            "--topic",
            "alpha",
            "run-directions-1",
            "--stage-id",
            "late-change",
        )
        self.assertEqual(1, status)
        self.assertEqual("run_terminal", rejected["error"]["code"])

    def test_verified_repository_acquisition_registers_only_after_success(self) -> None:
        upstream = self.root / "upstream"
        upstream.mkdir()
        subprocess.run(["git", "init", "-q", str(upstream)], check=True)
        subprocess.run(["git", "-C", str(upstream), "config", "user.email", "test@example.com"], check=True)
        subprocess.run(["git", "-C", str(upstream), "config", "user.name", "Test User"], check=True)
        write(upstream / "README.md", "# Upstream\n")
        subprocess.run(["git", "-C", str(upstream), "add", "README.md"], check=True)
        subprocess.run(["git", "-C", str(upstream), "commit", "-q", "-m", "initial"], check=True)
        expected_commit = subprocess.run(
            ["git", "-C", str(upstream), "rev-parse", "HEAD"],
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()

        status, acquired = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "repos",
            "acquire",
            f"file://{upstream}",
            "--topic",
            "alpha",
            "--semantic-label",
            "topic.repos.sources.example",
        )
        self.assertEqual(0, status, acquired)
        self.assertEqual(expected_commit, acquired["repository"]["commit"])
        self.assertEqual(1, acquired["repository"]["depth"])
        target = Path(str(acquired["repository"]["path"]))
        self.assertTrue((target / ".git").is_dir())
        topic_manifest = self.root / "topic-workspaces/alpha/topic-workspace.toml"
        self.assertIn("topic.repos.sources.example", topic_manifest.read_text(encoding="utf-8"))

        status, failed = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "repos",
            "acquire",
            "file:///definitely/missing/repository",
            "--topic",
            "alpha",
            "--semantic-label",
            "topic.repos.sources.missing",
        )
        self.assertEqual(1, status)
        self.assertEqual("repository_remote_unreachable", failed["error"]["code"])
        self.assertNotIn("topic.repos.sources.missing", topic_manifest.read_text(encoding="utf-8"))

    def test_service_request_is_distinct_and_dispatches_synchronously(self) -> None:
        command_request = json.dumps(
            {
                "extension_point": "service_dispatch",
                "argv": [sys.executable, "-c", "print('ready')"],
                "cwd": str(self.root / "topic-workspaces/alpha"),
            }
        )
        status, created = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "service-requests",
            "create",
            "--topic",
            "alpha",
            "--task-description",
            "Run the task-critical smoke check",
            "--scope-kind",
            "topic_workspace",
            "--scope-ref",
            "alpha",
            "--expected-output-ref",
            "KAOJU:SMOKE-RUN-RESULT",
            "--authorization",
            "execute the recorded smoke command inside the selected Topic Workspace",
            "--dispatch-form",
            "tool_native_subagent",
            "--completion-observation",
            "zero exit status and ready output",
            "--command-request-json",
            command_request,
            "--actor-ref",
            "project-operator-session:test",
            "--id",
            "service-request-smoke-1",
        )
        self.assertEqual(0, status, created)
        self.assertEqual("service_request", created["record"]["record_kind"])
        self.assertNotIn("houmao", json.dumps(created).lower())
        self.assertNotIn("provider_payload", json.dumps(created))

        status, dispatched = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "service-requests",
            "dispatch",
            "--topic",
            "alpha",
            "service-request-smoke-1",
            "--service-actor-ref",
            "service-agent:tool-native",
        )
        self.assertEqual(0, status, dispatched)
        self.assertEqual("complete", dispatched["terminal_status"])
        self.assertEqual("succeeded", dispatched["observation"]["status"])
        self.assertIn("ready", dispatched["observation"]["stdout"])
        self.assertTrue(str(dispatched["support_artifact_ref"]).startswith("support-artifact-"))

        status, service_status = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "service-requests",
            "status",
            "--topic",
            "alpha",
            "service-request-smoke-1",
        )
        self.assertEqual(0, status, service_status)
        record = service_status["record"]
        self.assertEqual("service_request", record["record_kind"])
        self.assertNotEqual("research_task", record["record_kind"])
        self.assertNotEqual("workflow_stage_cursor", record["record_kind"])

        status, second = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "service-requests",
            "create",
            "--topic",
            "alpha",
            "--task-description",
            "Prepare an environment",
            "--scope-kind",
            "topic_workspace",
            "--scope-ref",
            "alpha",
            "--authorization",
            "inspect only",
            "--dispatch-form",
            "launched_service_agent",
            "--actor-ref",
            "project-operator-session:test",
            "--id",
            "service-request-env-1",
        )
        self.assertEqual(0, status, second)
        status, no_wait = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "service-requests",
            "dispatch",
            "--topic",
            "alpha",
            "service-request-env-1",
            "--service-actor-ref",
            "service-agent:env",
            "--no-wait",
        )
        self.assertEqual(1, status)
        self.assertEqual("service_request_no_wait_unsupported", no_wait["error"]["code"])


if __name__ == "__main__":
    unittest.main()
