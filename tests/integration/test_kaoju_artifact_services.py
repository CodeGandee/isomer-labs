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
from isomer_labs.kaoju.mindsets import (
    canonical_digest,
    ensure_mindset_sources,
    load_mindset_source,
    materialize_record_payload,
    mindset_source_child,
    packaged_default_root,
    replace_mindset_source,
)
from isomer_labs.models import SelectionRequest
from isomer_labs.project import discover_project
from isomer_labs.project.context import resolve_effective_topic_context
from isomer_labs.project.validation import build_project_state
from isomer_labs.records.store import ResearchRecordError
from isomer_labs.skills.installer import install_system_skills, resolve_system_skill_selection, resolve_targets, upgrade_system_skills
from isomer_labs.workspace.path_resolution import resolve_semantic_path


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

    def topic_context(self) -> object:
        project, diagnostics = discover_project(cwd=self.root, env={})
        self.assertEqual([], diagnostics)
        assert project is not None
        state = build_project_state(project)
        self.assertEqual([], state.diagnostics)
        context, diagnostics = resolve_effective_topic_context(state, SelectionRequest(), cwd=self.root, env={})
        self.assertEqual([], diagnostics)
        assert context is not None
        return context

    def test_late_install_is_read_only_then_lazy_ensure_specializes_and_preserves_topic_sources(self) -> None:
        overview = self.root / "topic-workspaces/alpha/intent/src/topic-overview.md"
        write(
            overview,
            """
            # Alpha Survey

            Survey compiler reliability, with emphasis on silent miscompilation evidence.
            """,
        )
        mindset_root = self.root / "topic-workspaces/alpha/intent/derived/mindsets"
        self.assertFalse(mindset_root.exists())

        target = resolve_targets("generic", scope="project", cwd=self.root)[0]
        selection = resolve_system_skill_selection(extensions=("kaoju",))
        installed = install_system_skills(target, selection)
        self.assertTrue(installed.ok)
        self.assertFalse(mindset_root.exists(), "installing Kaoju must not scan or mutate existing topics")
        core_topic_creator = target.skill_root / "isomer-op-entrypoint/subskills/isomer-op-topic-creator/SKILL-MAIN.md"
        core_text = core_topic_creator.read_text(encoding="utf-8")
        self.assertNotIn("topic.intent.kaoju_mindsets", core_text)
        self.assertNotIn("mindset-source", core_text.lower())

        context = self.topic_context()
        resolution, diagnostics = resolve_semantic_path(context, "topic.intent.kaoju_mindsets", env={}, cwd=self.root)
        self.assertEqual([], diagnostics)
        assert resolution is not None
        self.assertEqual(mindset_root, resolution.path)
        self.assertFalse(mindset_root.exists(), "read-only semantic resolution must not initialize mindset intent")

        def specialize(seed: dict[str, object], overview_text: str) -> dict[str, object]:
            if seed["mindset_key"] == "paper.deep-dive" and "miscompilation" in overview_text:
                questions = seed["questions"]
                assert isinstance(questions, list)
                questions[0]["additional_notes"] = "Ask how the paper bears on silent miscompilation evidence."
            return seed

        created = ensure_mindset_sources(context, env={}, cwd=self.root, specialize=specialize)
        self.assertTrue(created["ok"], created)
        self.assertEqual(set(("paper.deep-dive", "paper.skimming", "source-code.ingest")), {item["mindset_key"] for item in created["created"]})
        deep, diagnostics = load_mindset_source(mindset_source_child(mindset_root, "paper.deep-dive"))
        self.assertEqual([], diagnostics)
        assert deep is not None
        self.assertEqual("Ask how the paper bears on silent miscompilation evidence.", deep["questions"][0]["additional_notes"])
        skim, diagnostics = load_mindset_source(mindset_source_child(mindset_root, "paper.skimming"))
        seed_skim, seed_diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics + seed_diagnostics)
        self.assertEqual(seed_skim, skim, "a seed remains an unchanged topic-owned copy when specialization adds no value")

        assert skim is not None
        skim["questions"][0]["additional_notes"] = "User-authored triage emphasis."
        skim_path = mindset_source_child(mindset_root, "paper.skimming")
        replaced = replace_mindset_source(skim_path, skim, observed_digest=canonical_digest(seed_skim or {}))
        upgraded = upgrade_system_skills(target, selection)
        self.assertTrue(upgraded.ok)
        replay = ensure_mindset_sources(context, env={}, cwd=self.root)
        self.assertFalse(replay["mutated"])
        self.assertEqual(set(("paper.deep-dive", "paper.skimming", "source-code.ingest")), {item["mindset_key"] for item in replay["preserved"]})
        persisted, diagnostics = load_mindset_source(skim_path)
        self.assertEqual([], diagnostics)
        assert persisted is not None
        self.assertEqual(replaced["new_digest"], canonical_digest(persisted))
        self.assertEqual("User-authored triage emphasis.", persisted["questions"][0]["additional_notes"])

    def test_mindset_record_create_scoped_revision_and_fail_closed_validation(self) -> None:
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        payload = materialize_record_payload(
            source,
            relative_path="paper.skimming.json",
            topic_id="alpha",
            run_ref="run-mindset-1",
            survey_contract_ref="survey-contract-1",
            survey_context_refs=("direction-set-1",),
        )
        payload_path = self.root / "mindset-record-v1.json"
        payload_path.write_text(json.dumps(payload), encoding="utf-8")
        relationships = '[{"role":"run","target_ref":"run-mindset-1"},{"role":"survey_contract","target_ref":"survey-contract-1"}]'
        status, created = self.artifact(
            "put",
            "KAOJU:MINDSET-RECORD",
            str(payload_path),
            "--producer",
            "isomer-ext-kaoju-entrypoint",
            "--scope-key",
            "run-mindset-1",
            "--relationships-json",
            relationships,
            "--id",
            "mindset-record-v1",
            "--status",
            "active",
        )
        self.assertEqual(0, status, created)
        status, latest = self.artifact("latest", "KAOJU:MINDSET-RECORD", "--scope-key", "run-mindset-1")
        self.assertEqual(0, status, latest)
        self.assertEqual(["mindset-record-v1"], [item["record_id"] for item in latest["records"]])

        revision = json.loads(json.dumps(payload))
        revision["sections"]["source_snapshot"]["questions"][0]["answer_state"] = "answered"
        revision["sections"]["source_snapshot"]["questions"][0]["answer"] = "The paper is a triage candidate."
        revision_path = self.root / "mindset-record-v2.json"
        revision_path.write_text(json.dumps(revision), encoding="utf-8")
        status, revised = self.artifact(
            "revise",
            "mindset-record-v1",
            str(revision_path),
            "--producer",
            "isomer-ext-kaoju-entrypoint",
            "--relationships-json",
            relationships,
            "--id",
            "mindset-record-v2",
        )
        self.assertEqual(0, status, revised)
        status, prior = self.artifact("show", "mindset-record-v1")
        self.assertEqual(0, status, prior)
        self.assertEqual("mindset-record-v1", prior["record"]["id"])

        status, rejected = self.artifact(
            "revise",
            "mindset-record-v1",
            str(revision_path),
            "--producer",
            "isomer-ext-kaoju-entrypoint",
            "--relationships-json",
            relationships,
        )
        self.assertEqual(1, status)
        self.assertEqual("mindset_record_revision_stale", rejected["error"]["code"])

        changed_snapshot = json.loads(json.dumps(revision))
        changed_snapshot["sections"]["source_snapshot"]["questions"][0]["prompt"] = "Changed prompt"
        changed_path = self.root / "mindset-record-changed.json"
        changed_path.write_text(json.dumps(changed_snapshot), encoding="utf-8")
        status, rejected = self.artifact(
            "revise",
            "mindset-record-v2",
            str(changed_path),
            "--producer",
            "isomer-ext-kaoju-entrypoint",
            "--relationships-json",
            relationships,
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_contract_invalid", rejected["error"]["code"])

        invalid_evidence = json.loads(json.dumps(payload))
        invalid_evidence["sections"]["source_snapshot"]["questions"][0]["evidence_refs"] = ["../cross-topic"]
        invalid_evidence_path = self.root / "mindset-record-invalid-evidence.json"
        invalid_evidence_path.write_text(json.dumps(invalid_evidence), encoding="utf-8")
        status, rejected = self.artifact(
            "put",
            "KAOJU:MINDSET-RECORD",
            str(invalid_evidence_path),
            "--producer",
            "isomer-ext-kaoju-entrypoint",
            "--scope-key",
            "run-mindset-1",
            "--relationships-json",
            relationships,
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_contract_invalid", rejected["error"]["code"])

        malformed = json.loads(json.dumps(payload))
        malformed["sections"]["source_snapshot"]["relative_path"] = "../paper.skimming.json"
        malformed_path = self.root / "mindset-record-malformed.json"
        malformed_path.write_text(json.dumps(malformed), encoding="utf-8")
        status, rejected = self.artifact(
            "put",
            "KAOJU:MINDSET-RECORD",
            str(malformed_path),
            "--producer",
            "isomer-ext-kaoju-entrypoint",
            "--scope-key",
            "run-mindset-1",
            "--relationships-json",
            relationships,
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_contract_invalid", rejected["error"]["code"])

        cross_topic = json.loads(json.dumps(payload))
        cross_topic["sections"]["survey_context"]["topic_id"] = "other"
        cross_topic_path = self.root / "mindset-record-cross-topic.json"
        cross_topic_path.write_text(json.dumps(cross_topic), encoding="utf-8")
        status, rejected = self.artifact(
            "put",
            "KAOJU:MINDSET-RECORD",
            str(cross_topic_path),
            "--producer",
            "isomer-ext-kaoju-entrypoint",
            "--scope-key",
            "run-mindset-1",
            "--relationships-json",
            relationships,
        )
        self.assertEqual(1, status)
        self.assertEqual("mindset_record_topic_mismatch", rejected["error"]["code"])

        terminal = json.loads(json.dumps(revision))
        for row in terminal["sections"]["source_snapshot"]["questions"]:
            if row["answer_state"] == "unanswered":
                row["answer_state"] = "unresolved"
                row["rationale"] = "No evidence was available."
        collector = terminal["sections"]["source_snapshot"]["additional_question_collector"]
        collector["answer_state"] = "answered"
        collector["answer"] = "No explicit supplemental questions."
        collector["checked"] = True
        terminal["sections"]["unresolved_questions"] = [
            row["question_id"]
            for row in terminal["sections"]["source_snapshot"]["questions"]
            if row["answer_state"] == "unresolved"
        ]
        terminal["sections"]["terminal_status"] = "complete"
        terminal_path = self.root / "mindset-record-terminal.json"
        terminal_path.write_text(json.dumps(terminal), encoding="utf-8")
        status, completed = self.artifact(
            "revise",
            "mindset-record-v2",
            str(terminal_path),
            "--producer",
            "isomer-ext-kaoju-entrypoint",
            "--relationships-json",
            relationships,
            "--id",
            "mindset-record-v3",
        )
        self.assertEqual(0, status, completed)

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
