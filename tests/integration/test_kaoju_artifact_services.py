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


def repository_evidence(label: str, locator: str, commit: str, *, observed_at: str = "2026-07-15T12:00:00Z") -> dict[str, object]:
    return {
        "semantic_label": label,
        "requested_locator": locator,
        "resolved_locator": locator,
        "immutable_identity": {"kind": "git_commit", "value": commit},
        "acquisition_method": {
            "tool_class": "git",
            "operation": "clone-and-checkout",
            "description": "The integration test ran external Git commands before invoking Isomer.",
            "options": ["local fixture source", "selected immutable revision"],
        },
        "command_evidence": [
            {
                "tool_class": "git",
                "operation": "identity-verification",
                "description": "The integration test observed the checked-out revision outside Isomer.",
                "status": "succeeded",
                "observed_identity": commit,
            }
        ],
        "verification": {"status": "verified", "method": "external rev-parse and source comparison"},
        "observed_at": observed_at,
        "access": {"status": "available", "basis": "local authorized fixture"},
        "license": {"status": "unknown", "basis": "not established by acquisition"},
        "relationship_basis": "The fixture source is the selected project repository.",
        "limitations": ["Local fixture does not exercise network authentication."],
        "blockers": [],
    }


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

    def direction_payload(self, name: str, title: str, *, initial: bool = True) -> Path:
        path = self.root / name
        actor_ref = "topic-actor:test"
        generation_id = f"generation-{Path(name).stem}"
        proposal_specs = [
            ("d1", "direction-systems", title, "Which systems mechanisms are supported by primary evidence?", "Systems evidence through 2026-07-14", ["paper", "technical_report", "framework_doc", "repository", "dataset"], "section-level", ["reading-list", "source-digests"], "requires-environment-work", "selected", "The actor selected the systems direction."),
            ("d2", "direction-comparative", "Comparative mechanisms", "How do mechanisms differ?", "Primary papers", ["paper", "technical_report"], "full-text", ["comparison"], "unknown", "not_selected", "Keep this direction open as an alternative."),
            ("d3", "direction-lineage", "Implementation lineage", "Which code implements the reported methods?", "Verified repositories", ["paper", "repository"], "code-level", ["source-digests"], "available", "not_selected", "Keep this direction open for later exploration."),
        ]
        proposals = []
        for index, (direction_id, idea_id, proposal_title, question, boundary, sources, depth, deliverables, feasibility, outcome, rationale) in enumerate(proposal_specs):
            proposals.append(
                {
                    "id": direction_id,
                    "idea_id": idea_id,
                    "title": proposal_title,
                    "summary": f"Investigate {proposal_title.lower()} as a durable survey direction.",
                    "research_question": question,
                    "boundary": boundary,
                    "source_classes": sources,
                    "coverage_date": "2026-07-14",
                    "expected_depth": depth,
                    "deliverables": deliverables,
                    "empirical_feasibility": feasibility,
                    "source_json_path": f"$.sections.proposals[{index}]",
                    "generation_id": generation_id,
                    "decision_outcome": outcome,
                    "disposition_rationale": rationale,
                    "transition_required": initial and outcome == "selected",
                }
            )
        effects = {
            "atomic": True,
            "artifact_family": "kaoju",
            "actor_ref": actor_ref,
            "ideas": [
                {
                    "idea_id": proposal["idea_id"],
                    "title": proposal["title"],
                    "summary": proposal["summary"],
                    "source_json_path": proposal["source_json_path"],
                    "exploration_state": "unexplored",
                    "decision_state": "selected" if proposal["decision_outcome"] == "selected" else "open",
                    "evidence_state": "unassessed",
                    "archive_state": "active",
                    "visibility": "primary",
                    "aliases": [proposal["id"]],
                }
                for proposal in proposals
            ],
            "generation_groups": [{"generation_id": generation_id, "member_idea_ids": [proposal["idea_id"] for proposal in proposals], "parent_idea_ids": []}],
            "decision_options": [
                {"idea_id": proposal["idea_id"], "outcome": proposal["decision_outcome"], "ordinal": index, "generation_id": generation_id, "rationale": proposal["disposition_rationale"], "actor_ref": actor_ref}
                for index, proposal in enumerate(proposals)
            ],
            "transitions": (
                [{"idea_id": "direction-systems", "facet": "decision_state", "previous_value": "open", "next_value": "selected", "actor_ref": actor_ref, "rationale": "The actor selected this direction."}]
                if initial
                else []
            ),
        }
        path.write_text(
            json.dumps(
                {
                    "title": title,
                    "summary": "Actor-confirmed survey directions.",
                    "artifact_family": "kaoju",
                    "semantic_id": "KAOJU:DIRECTION-SET",
                    "artifact_type": "direction-set",
                    "sections": {
                        "proposals": proposals,
                        "selections": ["d1"],
                        "confirmation": {"status": "accepted", "actor_ref": actor_ref},
                    },
                    "research_idea_effects": effects,
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

        revised_payload = self.direction_payload("direction-v2.json", "Systems and compilers", initial=False)
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

        legacy_payload = self.root / "legacy-direction-set-v1.json"
        legacy_data = json.loads(payload.read_text(encoding="utf-8"))
        legacy_data.pop("research_idea_effects", None)
        legacy_payload.write_text(json.dumps(legacy_data), encoding="utf-8")
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
                str(legacy_payload),
            )
            self.assertEqual(0, status, legacy)
        status, ambiguous = self.artifact("latest", "KAOJU:DIRECTION-SET")
        self.assertEqual(1, status)
        self.assertEqual("artifact_latest_ambiguous", ambiguous["error"]["code"])

    def test_directory_manifest_integrity_and_terminal_run_immutability(self) -> None:
        tree = self.root / "template-export"
        write(tree / "template.md", "# Survey\n")
        write(tree / "notes.txt", "human notes\n")
        relationships = '[{"role":"paper_template","target_record_id":"template-v1"}]'
        status, created = self.artifact(
            "put",
            "KAOJU:PAPER-TEMPLATE-EXPORT",
            str(tree),
            "--producer",
            "isomer-kaoju-write",
            "--scope-key",
            "main",
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
                "main",
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

    def test_external_repository_acquire_verify_register_and_record_boundaries(self) -> None:
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

        workspace = self.root / "topic-workspaces/alpha"
        target = workspace / "repos/extern/sources/example"
        target.parent.mkdir(parents=True)
        subprocess.run(["git", "clone", "-q", f"file://{upstream}", str(target)], check=True)
        observed_commit = subprocess.run(
            ["git", "-C", str(target), "rev-parse", "HEAD"],
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        self.assertEqual(expected_commit, observed_commit)

        topic_manifest = workspace / "topic-workspace.toml"
        self.assertFalse(topic_manifest.exists())
        status, registered = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "repos",
            "register",
            "sources.example",
            "--path",
            str(target),
            "--topic",
            "alpha",
        )
        self.assertEqual(0, status, registered)
        self.assertTrue(registered["mutated"])
        self.assertEqual(str(target), registered["repository"]["path"])
        self.assertTrue((target / ".git").is_dir())
        self.assertIn("topic.repos.sources.example", topic_manifest.read_text(encoding="utf-8"))

        evidence_v1 = repository_evidence("topic.repos.sources.example", f"file://{upstream}", observed_commit)
        associated_v1 = self.root / "associated-v1.json"
        write(
            associated_v1,
            json.dumps(
                {
                    "title": "Associated source v1",
                    "summary": "Externally verified repository evidence.",
                    "artifact_family": "kaoju",
                    "semantic_id": "KAOJU:ASSOCIATED-SOURCE-CODE",
                    "artifact_type": "associated-source-code",
                    "sections": {
                        "source": {"paper_ref": "paper-1", "version_family": "paper-v1"},
                        "repository": evidence_v1,
                        "relationship": {"status": "verified", "basis": "Fixture-selected source."},
                    },
                },
                indent=2,
            )
            + "\n",
        )
        relationships = '[{"role":"source","target_ref":"paper-1"},{"role":"repository","target_ref":"topic.repos.sources.example"}]'
        status, recorded = self.artifact(
            "put",
            "KAOJU:ASSOCIATED-SOURCE-CODE",
            str(associated_v1),
            "--producer",
            "isomer-kaoju-acquire",
            "--scope-key",
            "source:paper-1",
            "--relationships-json",
            relationships,
            "--id",
            "associated-source-v1",
        )
        self.assertEqual(0, status, recorded)

        mismatched = json.loads(associated_v1.read_text(encoding="utf-8"))
        mismatched["sections"]["repository"]["immutable_identity"]["value"] = "b" * 40
        mismatch_path = self.root / "associated-mismatch.json"
        write(mismatch_path, json.dumps(mismatched, indent=2) + "\n")
        status, rejected = self.artifact(
            "put",
            "KAOJU:ASSOCIATED-SOURCE-CODE",
            str(mismatch_path),
            "--producer",
            "isomer-kaoju-acquire",
            "--scope-key",
            "source:mismatch",
            "--relationships-json",
            relationships,
            "--id",
            "associated-source-mismatch",
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_contract_invalid", rejected["error"]["code"])
        self.assertIn("does not match immutable_identity", rejected["error"]["message"])
        self.assertIn("topic.repos.sources.example", topic_manifest.read_text(encoding="utf-8"))

        partial = workspace / "repos/extern/sources/partial"
        partial.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", str(partial)], check=True)
        write(partial / "INCOMPLETE", "external command stopped before verification\n")
        self.assertNotIn("topic.repos.sources.partial", topic_manifest.read_text(encoding="utf-8"))

        conflict_target = workspace / "repos/extern/sources/example-conflict"
        subprocess.run(["git", "clone", "-q", f"file://{upstream}", str(conflict_target)], check=True)
        status, conflict = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "repos",
            "register",
            "sources.example",
            "--path",
            str(conflict_target),
            "--topic",
            "alpha",
        )
        self.assertEqual(1, status)
        self.assertFalse(conflict["mutated"])
        self.assertTrue(conflict_target.is_dir())

        write(upstream / "CHANGELOG.md", "second revision\n")
        subprocess.run(["git", "-C", str(upstream), "add", "CHANGELOG.md"], check=True)
        subprocess.run(["git", "-C", str(upstream), "commit", "-q", "-m", "second"], check=True)
        subprocess.run(["git", "-C", str(target), "pull", "-q", "--ff-only"], check=True)
        second_commit = subprocess.run(
            ["git", "-C", str(target), "rev-parse", "HEAD"],
            check=True,
            text=True,
            capture_output=True,
        ).stdout.strip()
        self.assertNotEqual(expected_commit, second_commit)
        evidence_v2 = repository_evidence(
            "topic.repos.sources.example",
            f"file://{upstream}",
            second_commit,
            observed_at="2026-07-15T13:00:00Z",
        )
        associated_v2 = self.root / "associated-v2.json"
        revised_payload = json.loads(associated_v1.read_text(encoding="utf-8"))
        revised_payload["title"] = "Associated source v2"
        revised_payload["sections"]["repository"] = evidence_v2
        write(associated_v2, json.dumps(revised_payload, indent=2) + "\n")
        status, revised = self.artifact(
            "revise",
            "associated-source-v1",
            str(associated_v2),
            "--producer",
            "isomer-kaoju-acquire",
            "--relationships-json",
            relationships,
            "--id",
            "associated-source-v2",
        )
        self.assertEqual(0, status, revised)
        status, resolved = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "paths",
            "get",
            "topic.repos.sources.example",
            "--topic",
            "alpha",
        )
        self.assertEqual(0, status, resolved)
        self.assertEqual(str(target), resolved["path"]["path"])
        status, latest = self.artifact("latest", "KAOJU:ASSOCIATED-SOURCE-CODE", "--scope-key", "source:paper-1")
        self.assertEqual(0, status, latest)
        self.assertEqual(["associated-source-v2"], [item["record_id"] for item in latest["records"]])

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
