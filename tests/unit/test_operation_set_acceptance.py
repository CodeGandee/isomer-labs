from __future__ import annotations

import contextlib
import io
import json
import os
import tempfile
import textwrap
import unittest
from pathlib import Path
from unittest.mock import patch

from isomer_labs import cli
from isomer_labs.core.diagnostics import has_errors
from isomer_labs.models import EffectiveTopicContext, SelectionRequest
from isomer_labs.project import discover_project
from isomer_labs.project.context import resolve_effective_topic_context
from isomer_labs.project.validation import build_project_state
from isomer_labs.records.operation_sets import (
    OPERATION_SET_CONTROL_DIR,
    OperationSetAcceptanceError,
    OperationSetAcceptanceManifest,
    OperationSetOutput,
    OperationSetRecordIntent,
    apply_operation_set_acceptance,
    canonical_json_digest,
    file_digest,
    inspect_operation_set,
    inventory_operation_set,
    plan_operation_set_acceptance,
    resolve_operation_set,
    verify_operation_set_acceptance,
    write_operation_set_manifest,
)
from isomer_labs.records.store import ResearchRecordError, ResearchRecordRequest, create_record
from isomer_labs.runtime.records import OperationSetAcceptanceItemRecord, OperationSetAcceptanceRecord
from isomer_labs.runtime.store import initialize_workspace_runtime, open_workspace_runtime


NOW = "2026-07-17T00:00:00Z"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class OperationSetAcceptanceFoundationTests(unittest.TestCase):
    def make_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def make_context(self) -> EffectiveTopicContext:
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
        workspace = root / "topic-workspaces" / "alpha"
        workspace.mkdir(parents=True)
        write(
            workspace / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "alpha"
            topic_workspace_id = "alpha"

            [[topic_actors]]
            topic_actor_name = "operator"
            actor_kind = "operator"
            runtime_kind = "codex"
            role_kind = "operator"
            controller_kind = "project_operator_session"
            output_root = "isomer-managed/worker-output/topic-actors/operator"
            commit_after_operation = false
            status = "ready"

            [agent_output_defaults]
            output_root = "isomer-managed/worker-output/agents/{agent_name}"
            commit_after_operation = false
            """,
        )
        project, project_diagnostics = discover_project(cwd=root, env={})
        self.assertEqual([], project_diagnostics)
        assert project is not None
        state = build_project_state(project)
        self.assertEqual([], state.diagnostics)
        context, context_diagnostics = resolve_effective_topic_context(state, SelectionRequest(), cwd=root, env={})
        self.assertEqual([], context_diagnostics)
        assert context is not None
        result, runtime_diagnostics = initialize_workspace_runtime(context, env={})
        self.assertIsNotNone(result, runtime_diagnostics)
        return context

    def actor_operation_set(self, context: EffectiveTopicContext, name: str = "run-1") -> Path:
        root = context.topic_workspace_path / "actors" / "operator" / "isomer-managed" / "worker-output" / "topic-actors" / "operator" / "sets" / name
        root.mkdir(parents=True, exist_ok=True)
        return root

    def resolved_actor_set(self, context: EffectiveTopicContext, operation_set: Path):
        resolved, diagnostics = resolve_operation_set(
            context,
            operation_set,
            env={},
            cwd=context.project.root,
            topic_actor_name="operator",
        )
        self.assertFalse(has_errors(diagnostics), diagnostics)
        assert resolved is not None
        return resolved

    def run_operation_sets_cli(
        self,
        context: EffectiveTopicContext,
        args: list[str],
    ) -> tuple[int, dict[str, object]]:
        stdout = io.StringIO()
        with (
            contextlib.chdir(context.project.root),
            patch.dict(
                os.environ,
                {"HOME": str(context.project.root), "PATH": os.environ.get("PATH", "")},
                clear=True,
            ),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(
                [
                    "ext",
                    "research",
                    "operation-sets",
                    *args,
                    "--project",
                    str(context.project.root),
                    "--topic",
                    "alpha",
                ]
            )
        return status, json.loads(stdout.getvalue())

    def manifest(
        self,
        context: EffectiveTopicContext,
        operation_set: Path,
        *,
        outputs: list[OperationSetOutput],
        intents: list[OperationSetRecordIntent],
        revision: int = 1,
        supersedes_receipt_id: str | None = None,
    ) -> tuple[Path, OperationSetAcceptanceManifest]:
        resolved = self.resolved_actor_set(context, operation_set)
        manifest = OperationSetAcceptanceManifest(
            operation_set_id=resolved.operation_set_id,
            revision=revision,
            research_topic_id=context.research_topic.id,
            topic_workspace_id=context.topic_workspace_id,
            worker_kind="topic_actor",
            worker_name="operator",
            outputs=tuple(outputs),
            record_intents=tuple(intents),
            supersedes_receipt_id=supersedes_receipt_id,
        )
        path = operation_set / OPERATION_SET_CONTROL_DIR / "manifest.json"
        write_operation_set_manifest(path, manifest)
        return path, manifest

    def test_manifest_is_strict_versioned_and_canonical(self) -> None:
        value = {
            "schema_version": "isomer-operation-set-acceptance.v1",
            "operation_set_id": "set-1",
            "revision": 1,
            "research_topic_id": "alpha",
            "topic_workspace_id": "alpha",
            "worker": {"kind": "topic_actor", "name": "operator"},
            "outputs": [
                {
                    "key": "report",
                    "path": "report.md",
                    "digest": "a" * 64,
                    "size_bytes": 3,
                    "disposition": "disposable",
                    "reason": "test scratch",
                }
            ],
            "record_intents": [],
        }
        manifest = OperationSetAcceptanceManifest.from_json(value)
        self.assertEqual("sha256:" + "a" * 64, manifest.outputs[0].digest)
        self.assertEqual(manifest.digest, canonical_json_digest(manifest.to_json()))
        with self.assertRaises(OperationSetAcceptanceError) as raised:
            OperationSetAcceptanceManifest.from_json({**value, "invented": True})
        self.assertEqual("operation_set_manifest_unknown_field", raised.exception.code)
        invalid_path = json.loads(json.dumps(value))
        invalid_path["outputs"][0]["path"] = "../escape.md"
        with self.assertRaises(OperationSetAcceptanceError) as raised:
            OperationSetAcceptanceManifest.from_json(invalid_path)
        self.assertEqual("operation_set_path_escape", raised.exception.code)
        duplicate = json.loads(json.dumps(value))
        duplicate["outputs"].append({**duplicate["outputs"][0], "key": "report-copy"})
        with self.assertRaises(OperationSetAcceptanceError) as raised:
            OperationSetAcceptanceManifest.from_json(duplicate)
        self.assertEqual("operation_set_output_path_duplicate", raised.exception.code)

    def test_receipt_store_round_trips_additive_headers_and_items(self) -> None:
        context = self.make_context()
        store, diagnostics = open_workspace_runtime(context, env={}, read_only=False)
        self.assertFalse(has_errors(diagnostics), diagnostics)
        assert store is not None
        try:
            receipt = OperationSetAcceptanceRecord(
                id="receipt-1",
                research_topic_id="alpha",
                topic_workspace_id="alpha",
                operation_set_id="set-1",
                revision=1,
                worker_kind="topic_actor",
                worker_name="operator",
                canonical_root="/tmp/set-1",
                manifest_path="/tmp/set-1/.isomer-operation-set/manifest.json",
                manifest_digest="sha256:" + "b" * 64,
                manifest={"schema_version": "isomer-operation-set-acceptance.v1"},
                status="applying",
                output_summary={"total": 1},
                diagnostics=[],
                created_at=NOW,
                updated_at=NOW,
            )
            item = OperationSetAcceptanceItemRecord(
                id="item-1",
                acceptance_id="receipt-1",
                intent_key="report",
                intent_digest="sha256:" + "c" * 64,
                action="create",
                status="pending",
                record_id=None,
                managed_files=[],
                lineage_refs=[],
                idea_effect_refs=[],
                diagnostics=[],
                created_at=NOW,
                updated_at=NOW,
            )
            with store.connection:
                store.upsert_operation_set_acceptance(receipt)
                store.upsert_operation_set_acceptance_item(item)
            self.assertEqual(receipt, store.get_operation_set_acceptance("receipt-1"))
            self.assertEqual([item], store.list_operation_set_acceptance_items("receipt-1"))
        finally:
            store.close()

    def test_actor_and_agent_operation_sets_resolve_through_worker_policy(self) -> None:
        context = self.make_context()
        actor_set = self.actor_operation_set(context)
        actor, actor_diagnostics = resolve_operation_set(context, actor_set, env={}, cwd=context.project.root, topic_actor_name="operator")
        self.assertFalse(has_errors(actor_diagnostics), actor_diagnostics)
        assert actor is not None
        self.assertEqual("topic_actor", actor.worker_kind)
        self.assertEqual("sets/run-1", actor.relative_path)

        agent_set = context.topic_workspace_path / "agents" / "alice" / "isomer-managed" / "worker-output" / "agents" / "alice" / "sets" / "run-2"
        agent_set.mkdir(parents=True)
        agent, agent_diagnostics = resolve_operation_set(context, agent_set, env={}, cwd=context.project.root, agent_name="alice")
        self.assertFalse(has_errors(agent_diagnostics), agent_diagnostics)
        assert agent is not None
        self.assertEqual("agent", agent.worker_kind)
        ambiguous, ambiguous_diagnostics = resolve_operation_set(
            context,
            actor_set,
            env={},
            cwd=context.project.root,
            agent_name="alice",
            topic_actor_name="operator",
        )
        self.assertIsNone(ambiguous)
        self.assertTrue(any(item.code == "operation_set_worker_ambiguous" for item in ambiguous_diagnostics))
        outside = context.topic_workspace_path / "outside"
        outside.mkdir()
        escaped, escape_diagnostics = resolve_operation_set(context, outside, env={}, cwd=context.project.root, topic_actor_name="operator")
        self.assertIsNone(escaped)
        self.assertTrue(any(item.code == "operation_set_root_escape" for item in escape_diagnostics))

    def test_inventory_is_deterministic_git_independent_and_rejects_special_entries(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "z.log", "ignored by policy, not by inventory")
        write(operation_set / "nested" / "a.txt", "alpha")
        write(operation_set / OPERATION_SET_CONTROL_DIR / "plan.json", "{}")
        outside = context.topic_workspace_path / "secret.txt"
        write(outside, "secret")
        (operation_set / "escape-link").symlink_to(outside)
        if hasattr(os, "mkfifo"):
            os.mkfifo(operation_set / "debug.pipe")
        inventory, diagnostics = inventory_operation_set(operation_set)
        self.assertEqual(["nested/a.txt", "z.log"], [item.path for item in inventory])
        self.assertEqual(file_digest(operation_set / "nested" / "a.txt"), inventory[0].digest)
        codes = {item["code"] for item in diagnostics}
        self.assertIn("operation_set_symlink_escape", codes)
        if hasattr(os, "mkfifo"):
            self.assertIn("operation_set_special_file_unsupported", codes)

    def test_inspect_writes_explicit_incomplete_scaffold_only(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "report.md", "report")
        payload, diagnostics = inspect_operation_set(
            context,
            operation_set,
            env={},
            cwd=context.project.root,
            topic_actor_name="operator",
            write_scaffold=True,
        )
        self.assertFalse(has_errors(diagnostics), diagnostics)
        self.assertTrue(payload["mutated"])
        self.assertFalse(payload["reconciled"])
        manifest_path = Path(str(payload["manifest_path"]))
        self.assertTrue(manifest_path.exists())
        stored = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertNotIn("disposition", stored["outputs"][0])
        self.assertEqual([], stored["record_intents"])

    def test_plan_orders_local_dependencies_and_does_not_mutate_runtime(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "parent.md", "parent")
        write(operation_set / "child.md", "child")
        outputs = [
            OperationSetOutput(key="parent-output", path="parent.md", digest=file_digest(operation_set / "parent.md"), size_bytes=6, disposition="record_payload", record_key="parent"),
            OperationSetOutput(key="child-output", path="child.md", digest=file_digest(operation_set / "child.md"), size_bytes=5, disposition="record_payload", record_key="child"),
        ]
        intents = [
            OperationSetRecordIntent(key="child", action="create", record_kind="artifact", root_reason=None, parents=[{"local_record_key": "parent", "lineage_kind": "derived_from"}]),
            OperationSetRecordIntent(key="parent", action="create", record_kind="artifact", root_reason="First durable result."),
        ]
        manifest_path, _manifest = self.manifest(context, operation_set, outputs=outputs, intents=intents)
        store, store_diagnostics = open_workspace_runtime(context, env={}, read_only=True)
        self.assertFalse(has_errors(store_diagnostics), store_diagnostics)
        assert store is not None
        try:
            before = len(store.list_lifecycle_records())
        finally:
            store.close()
        plan, diagnostics = plan_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(diagnostics), diagnostics)
        self.assertTrue(plan["ok"], plan)
        self.assertFalse(plan["mutated"])
        self.assertEqual(["parent", "child"], [item["intent_key"] for item in plan["actions"]])
        store, _ = open_workspace_runtime(context, env={}, read_only=True)
        assert store is not None
        try:
            self.assertEqual(before, len(store.list_lifecycle_records()))
            self.assertEqual([], store.list_operation_set_acceptances(topic_workspace_id="alpha"))
        finally:
            store.close()

    def test_plan_reports_disposable_reason_and_file_drift_without_mutation(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "scratch.log", "first")
        output = OperationSetOutput(
            key="scratch",
            path="scratch.log",
            digest=file_digest(operation_set / "scratch.log"),
            size_bytes=5,
            disposition="disposable",
        )
        manifest_path, _manifest = self.manifest(context, operation_set, outputs=[output], intents=[])
        write(operation_set / "scratch.log", "changed")
        plan, diagnostics = plan_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(diagnostics), diagnostics)
        self.assertFalse(plan["ok"])
        codes = {item["code"] for item in plan["diagnostics"]}
        self.assertIn("operation_set_output_drift", codes)
        self.assertIn("operation_set_disposable_reason_missing", codes)

    def test_apply_copies_attachments_records_lineage_and_replays_without_duplicates(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "parent.md", "parent")
        write(operation_set / "child.md", "child")
        write(operation_set / "measurements.csv", "name,value\nlatency,3\n")
        outputs = [
            OperationSetOutput(key="parent-body", path="parent.md", digest=file_digest(operation_set / "parent.md"), size_bytes=6, disposition="record_payload", record_key="parent"),
            OperationSetOutput(key="child-body", path="child.md", digest=file_digest(operation_set / "child.md"), size_bytes=5, disposition="record_payload", record_key="child"),
            OperationSetOutput(key="measurements", path="measurements.csv", digest=file_digest(operation_set / "measurements.csv"), size_bytes=21, media_type="text/csv", disposition="record_attachment", record_key="child"),
        ]
        intents = [
            OperationSetRecordIntent(key="child", action="create", record_kind="artifact", parents=[{"local_record_key": "parent", "lineage_kind": "derived_from"}]),
            OperationSetRecordIntent(key="parent", action="create", record_kind="artifact", root_reason="First durable result."),
        ]
        manifest_path, _manifest = self.manifest(context, operation_set, outputs=outputs, intents=intents)

        first, diagnostics = apply_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(diagnostics), diagnostics)
        self.assertTrue(first["ok"], first)
        self.assertEqual("complete", first["acceptance"]["status"])
        self.assertFalse(first["replayed"])
        items = {item["intent_key"]: item for item in first["items"]}
        parent_id = items["parent"]["record_id"]
        child_id = items["child"]["record_id"]
        self.assertEqual(1, len(items["child"]["managed_files"]))
        managed = items["child"]["managed_files"][0]
        self.assertNotEqual(str(operation_set / "measurements.csv"), managed["path"])
        self.assertTrue(Path(managed["path"]).is_relative_to(context.topic_workspace_path))
        self.assertEqual(file_digest(operation_set / "measurements.csv"), file_digest(Path(managed["path"])))

        store, store_diagnostics = open_workspace_runtime(context, env={}, read_only=True)
        self.assertFalse(has_errors(store_diagnostics), store_diagnostics)
        assert store is not None
        try:
            records_before = len(store.list_lifecycle_records())
            edges = store.list_research_record_lineage_edges(topic_workspace_id="alpha", child_record_id=child_id)
            self.assertEqual([(parent_id, "derived_from")], [(edge.parent_record_id, edge.lineage_kind) for edge in edges])
            files = list(
                store.connection.execute(
                    "SELECT * FROM research_record_files WHERE record_id = ? AND file_role = 'attachment'",
                    (child_id,),
                )
            )
            self.assertEqual(1, len(files))
            self.assertEqual(managed["digest"], files[0]["digest"])
        finally:
            store.close()

        second, second_diagnostics = apply_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(second_diagnostics), second_diagnostics)
        self.assertTrue(second["ok"], second)
        self.assertTrue(second["replayed"])
        store, _ = open_workspace_runtime(context, env={}, read_only=True)
        assert store is not None
        try:
            self.assertEqual(records_before, len(store.list_lifecycle_records()))
            self.assertEqual(1, len(store.list_research_record_lineage_edges(topic_workspace_id="alpha", child_record_id=child_id)))
        finally:
            store.close()

    def test_partial_apply_resumes_from_item_receipts(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "first.md", "first")
        write(operation_set / "second.md", "second")
        outputs = [
            OperationSetOutput(key="first-output", path="first.md", digest=file_digest(operation_set / "first.md"), size_bytes=5, disposition="record_payload", record_key="first"),
            OperationSetOutput(key="second-output", path="second.md", digest=file_digest(operation_set / "second.md"), size_bytes=6, disposition="record_payload", record_key="second"),
        ]
        intents = [
            OperationSetRecordIntent(key="first", action="create", record_kind="artifact", root_reason="First root."),
            OperationSetRecordIntent(key="second", action="create", record_kind="artifact", parents=[{"local_record_key": "first", "lineage_kind": "follow_up_to"}]),
        ]
        manifest_path, _manifest = self.manifest(context, operation_set, outputs=outputs, intents=intents)

        from isomer_labs.records.operation_sets import application as operation_sets_module

        real_create = operation_sets_module.create_record
        calls = 0

        def fail_second(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise ResearchRecordError("injected failure", code="injected_operation_set_failure")
            return real_create(*args, **kwargs)

        with patch.object(operation_sets_module, "create_record", side_effect=fail_second):
            partial, diagnostics = apply_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(diagnostics), diagnostics)
        self.assertFalse(partial["ok"])
        self.assertTrue(partial["mutated"])
        self.assertEqual("partial", partial["acceptance"]["status"])
        self.assertEqual(["complete", "failed"], [item["status"] for item in partial["items"]])

        resumed, resumed_diagnostics = apply_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(resumed_diagnostics), resumed_diagnostics)
        self.assertTrue(resumed["ok"], resumed)
        self.assertEqual("complete", resumed["acceptance"]["status"])
        verified, verify_diagnostics = verify_operation_set_acceptance(context, resumed["acceptance"]["id"], env={})
        self.assertFalse(has_errors(verify_diagnostics), verify_diagnostics)
        self.assertTrue(verified["verified"], verified)

    def test_revision_inherits_record_kind_and_reference_requires_matching_managed_digest(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "original.md", "original")
        created, create_diagnostics = create_record(
            context,
            ResearchRecordRequest(record_kind="artifact", record_id="existing-record", body_file=operation_set / "original.md"),
            env={},
            cwd=context.project.root,
        )
        self.assertFalse(has_errors(create_diagnostics), create_diagnostics)
        self.assertTrue(created["ok"], created)

        reference_path = self.actor_operation_set(context, "reference")
        write(reference_path / "original.md", "original")
        reference_manifest, _ = self.manifest(
            context,
            reference_path,
            outputs=[OperationSetOutput(key="legacy-body", path="original.md", digest=file_digest(reference_path / "original.md"), size_bytes=8, disposition="record_payload", record_key="legacy")],
            intents=[OperationSetRecordIntent(key="legacy", action="reference", target_record_id="existing-record")],
        )
        reference, reference_diagnostics = apply_operation_set_acceptance(context, reference_manifest, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(reference_diagnostics), reference_diagnostics)
        self.assertTrue(reference["ok"], reference)
        self.assertEqual("existing-record", reference["items"][0]["record_id"])

        revision_path = self.actor_operation_set(context, "revision")
        write(revision_path / "revised.md", "revised")
        revision_manifest, _ = self.manifest(
            context,
            revision_path,
            outputs=[OperationSetOutput(key="revision-body", path="revised.md", digest=file_digest(revision_path / "revised.md"), size_bytes=7, disposition="record_payload", record_key="revision")],
            intents=[OperationSetRecordIntent(key="revision", action="revise", target_record_id="existing-record")],
        )
        preview, preview_diagnostics = plan_operation_set_acceptance(context, revision_manifest, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(preview_diagnostics), preview_diagnostics)
        self.assertTrue(preview["ok"], preview)
        revised, revise_diagnostics = apply_operation_set_acceptance(context, revision_manifest, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(revise_diagnostics), revise_diagnostics)
        self.assertTrue(revised["ok"], revised)
        revised_id = revised["items"][0]["record_id"]
        store, _ = open_workspace_runtime(context, env={}, read_only=True)
        assert store is not None
        try:
            record = store.get_lifecycle_record(revised_id)
            assert record is not None
            self.assertEqual("artifact", record.record_kind)
            edges = store.list_research_record_lineage_edges(topic_workspace_id="alpha", child_record_id=revised_id)
            self.assertEqual([("existing-record", "revision_of")], [(edge.parent_record_id, edge.lineage_kind) for edge in edges])
        finally:
            store.close()

    def test_preflight_collects_dependency_binding_and_reference_errors_without_receipt(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "one.md", "one")
        write(operation_set / "two.md", "two")
        write(operation_set / "invalid.json", "{}")
        outputs = [
            OperationSetOutput(key="one-output", path="one.md", digest=file_digest(operation_set / "one.md"), size_bytes=3, disposition="record_payload", record_key="one"),
            OperationSetOutput(key="two-output", path="two.md", digest=file_digest(operation_set / "two.md"), size_bytes=3, disposition="record_payload", record_key="two"),
            OperationSetOutput(key="invalid-output", path="invalid.json", digest=file_digest(operation_set / "invalid.json"), size_bytes=2, disposition="record_payload", record_key="invalid"),
        ]
        intents = [
            OperationSetRecordIntent(key="one", action="create", record_kind="not-a-kind", parents=[{"local_record_key": "two"}]),
            OperationSetRecordIntent(key="two", action="create", record_kind="artifact", parents=[{"local_record_key": "one"}]),
            OperationSetRecordIntent(
                key="invalid",
                action="create",
                record_kind="decision_record",
                semantic_id="KAOJU:DIRECTION-SET",
                format_profile_ref="isomer:research/record-format/profile/kaoju/decision/direction-set/v2",
                root_reason="Invalid payload preflight fixture.",
            ),
        ]
        manifest_path, _ = self.manifest(context, operation_set, outputs=outputs, intents=intents)
        store, _ = open_workspace_runtime(context, env={}, read_only=True)
        assert store is not None
        try:
            record_ids_before = {item.id for item in store.list_lifecycle_records()}
        finally:
            store.close()
        plan, diagnostics = plan_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(diagnostics), diagnostics)
        self.assertFalse(plan["ok"])
        codes = {item["code"] for item in plan["diagnostics"]}
        self.assertIn("operation_set_local_dependency_cycle", codes)
        self.assertIn("unsupported_record_kind", codes)
        self.assertIn("display_title_missing", codes)
        store, _ = open_workspace_runtime(context, env={}, read_only=True)
        assert store is not None
        try:
            self.assertEqual([], store.list_operation_set_acceptances(topic_workspace_id="alpha"))
            self.assertEqual(record_ids_before, {item.id for item in store.list_lifecycle_records()})
        finally:
            store.close()

    def test_preflight_rejects_managed_attachment_destination_collision(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "report.md", "report")
        write(operation_set / "data.csv", "value\n1\n")
        manifest_path, _ = self.manifest(
            context,
            operation_set,
            outputs=[
                OperationSetOutput(key="report", path="report.md", digest=file_digest(operation_set / "report.md"), size_bytes=6, disposition="record_payload", record_key="report"),
                OperationSetOutput(key="data", path="data.csv", digest=file_digest(operation_set / "data.csv"), size_bytes=8, disposition="record_attachment", record_key="report"),
            ],
            intents=[OperationSetRecordIntent(key="report", action="create", record_kind="artifact", root_reason="Root report.")],
        )
        first, diagnostics = plan_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(diagnostics), diagnostics)
        self.assertTrue(first["ok"], first)
        managed_path = Path(first["actions"][0]["managed_files"][0]["path"])
        write(managed_path, "collision")
        second, second_diagnostics = plan_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(second_diagnostics), second_diagnostics)
        self.assertFalse(second["ok"])
        self.assertIn("operation_set_attachment_destination_conflict", {item["code"] for item in second["diagnostics"]})

    def test_changed_manifest_conflicts_and_explicit_revision_supersedes_history(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "report.md", "report")
        output = OperationSetOutput(key="report-output", path="report.md", digest=file_digest(operation_set / "report.md"), size_bytes=6, disposition="record_payload", record_key="report")
        intent = OperationSetRecordIntent(key="report", action="create", record_kind="artifact", root_reason="Initial accepted report.")
        manifest_path, first_manifest = self.manifest(context, operation_set, outputs=[output], intents=[intent])
        first, first_diagnostics = apply_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(first_diagnostics), first_diagnostics)
        self.assertTrue(first["ok"], first)
        first_receipt_id = first["acceptance"]["id"]
        first_record_id = first["items"][0]["record_id"]

        changed_same_revision = OperationSetAcceptanceManifest(
            **{**first_manifest.__dict__, "metadata": {"changed": True}}
        )
        write_operation_set_manifest(manifest_path, changed_same_revision)
        conflict, conflict_diagnostics = apply_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(conflict_diagnostics), conflict_diagnostics)
        self.assertFalse(conflict["ok"])
        self.assertFalse(conflict["mutated"])
        self.assertIn("operation_set_acceptance_revision_conflict", {item["code"] for item in conflict["diagnostics"]})

        revision = OperationSetAcceptanceManifest(
            **{
                **first_manifest.__dict__,
                "revision": 2,
                "supersedes_receipt_id": first_receipt_id,
                "record_intents": (
                    OperationSetRecordIntent(key="report", action="reference", target_record_id=first_record_id),
                ),
            }
        )
        write_operation_set_manifest(manifest_path, revision)
        second, second_diagnostics = apply_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(second_diagnostics), second_diagnostics)
        self.assertTrue(second["ok"], second)
        self.assertEqual(2, second["acceptance"]["revision"])
        store, _ = open_workspace_runtime(context, env={}, read_only=True)
        assert store is not None
        try:
            history = store.list_operation_set_acceptances(topic_workspace_id="alpha", operation_set_id=first_manifest.operation_set_id)
            self.assertEqual([2, 1], [item.revision for item in history])
            self.assertEqual(["complete", "superseded"], [item.status for item in history])
            self.assertEqual(first_receipt_id, history[0].supersedes_receipt_id)
            self.assertEqual([first_record_id], [item.id for item in store.list_lifecycle_records() if item.record_kind == "artifact"])
        finally:
            store.close()

    def test_verify_reports_staged_managed_and_canonical_lineage_drift_without_repair(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        write(operation_set / "parent.md", "parent")
        write(operation_set / "child.md", "child")
        write(operation_set / "data.csv", "x\n1\n")
        outputs = [
            OperationSetOutput(key="parent-output", path="parent.md", digest=file_digest(operation_set / "parent.md"), size_bytes=6, disposition="record_payload", record_key="parent"),
            OperationSetOutput(key="child-output", path="child.md", digest=file_digest(operation_set / "child.md"), size_bytes=5, disposition="record_payload", record_key="child"),
            OperationSetOutput(key="attachment", path="data.csv", digest=file_digest(operation_set / "data.csv"), size_bytes=4, disposition="record_attachment", record_key="child"),
        ]
        intents = [
            OperationSetRecordIntent(key="parent", action="create", record_kind="artifact", root_reason="Root."),
            OperationSetRecordIntent(key="child", action="create", record_kind="artifact", parents=[{"local_record_key": "parent", "lineage_kind": "derived_from"}]),
        ]
        manifest_path, _ = self.manifest(context, operation_set, outputs=outputs, intents=intents)
        applied, diagnostics = apply_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(diagnostics), diagnostics)
        self.assertTrue(applied["ok"], applied)
        receipt_id = applied["acceptance"]["id"]
        child = next(item for item in applied["items"] if item["intent_key"] == "child")
        managed_path = Path(child["managed_files"][0]["path"])
        write(operation_set / "child.md", "changed")
        write(managed_path, "changed")
        store, _ = open_workspace_runtime(context, env={}, read_only=False)
        assert store is not None
        try:
            with store.connection:
                store.connection.execute("DELETE FROM research_record_lineage_edges WHERE child_record_id = ?", (child["record_id"],))
        finally:
            store.close()

        verified, verify_diagnostics = verify_operation_set_acceptance(context, receipt_id, env={})
        self.assertFalse(has_errors(verify_diagnostics), verify_diagnostics)
        self.assertFalse(verified["ok"])
        codes = {item["code"] for item in verified["diagnostics"]}
        self.assertIn("operation_set_output_drift", codes)
        self.assertIn("operation_set_managed_file_drift", codes)
        self.assertIn("operation_set_record_lineage_missing", codes)
        self.assertIn("operation_set_lineage_ref_missing", codes)
        store, _ = open_workspace_runtime(context, env={}, read_only=True)
        assert store is not None
        try:
            receipt = store.get_operation_set_acceptance(receipt_id)
            assert receipt is not None
            self.assertEqual("complete", receipt.status)
        finally:
            store.close()

    def test_idea_bearing_acceptance_delegates_atomic_effects_and_verifies_missing_effects(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context)
        idea_id = "operation-set-stage-pipeline"
        generation_id = "operation-set-generation"
        actor_ref = "topic-actor:operator"
        proposal = {
            "id": "direction-stage",
            "idea_id": idea_id,
            "title": "Stage pipeline",
            "summary": "Model runtime as an explicit stage pipeline.",
            "research_question": "Which explicit stages dominate runtime?",
            "boundary": "One supported attention kernel family.",
            "source_classes": ["paper", "repository", "measurement"],
            "coverage_date": "2026-07-17",
            "expected_depth": "white-box",
            "deliverables": ["model", "validation"],
            "empirical_feasibility": "available",
            "source_json_path": "$.sections.proposals[0]",
            "generation_id": generation_id,
            "decision_outcome": "selected",
            "disposition_rationale": "Selected for focused development.",
        }
        effects = {
            "atomic": True,
            "artifact_family": "kaoju",
            "actor_ref": actor_ref,
            "ideas": [
                {
                    "idea_id": idea_id,
                    "title": proposal["title"],
                    "summary": proposal["summary"],
                    "source_json_path": proposal["source_json_path"],
                    "exploration_state": "unexplored",
                    "decision_state": "selected",
                    "evidence_state": "unassessed",
                    "archive_state": "active",
                    "visibility": "primary",
                    "aliases": [proposal["id"]],
                }
            ],
            "generation_groups": [
                {
                    "generation_id": generation_id,
                    "purpose": "Candidate direction generation.",
                    "member_idea_ids": [idea_id],
                    "parent_idea_ids": [],
                }
            ],
            "decision_options": [
                {
                    "idea_id": idea_id,
                    "outcome": "selected",
                    "ordinal": 0,
                    "generation_id": generation_id,
                    "rationale": "Selected for focused development.",
                    "actor_ref": actor_ref,
                }
            ],
            "transitions": [
                {
                    "idea_id": idea_id,
                    "facet": "decision_state",
                    "previous_value": "open",
                    "next_value": "selected",
                    "actor_ref": actor_ref,
                    "rationale": "Selected for focused development.",
                }
            ],
        }
        payload = {
            "title": "Direction Set",
            "summary": "One actor-confirmed direction.",
            "artifact_family": "kaoju",
            "semantic_id": "KAOJU:DIRECTION-SET",
            "artifact_type": "direction-set",
            "sections": {
                "proposals": [proposal],
                "selections": ["direction-stage"],
                "confirmation": {"status": "accepted", "actor_ref": actor_ref},
            },
            "research_idea_effects": effects,
        }
        write(operation_set / "direction-set.json", json.dumps(payload, indent=2) + "\n")
        manifest_path, _ = self.manifest(
            context,
            operation_set,
            outputs=[
                OperationSetOutput(
                    key="direction-set",
                    path="direction-set.json",
                    digest=file_digest(operation_set / "direction-set.json"),
                    size_bytes=(operation_set / "direction-set.json").stat().st_size,
                    media_type="application/json",
                    disposition="record_payload",
                    record_key="directions",
                )
            ],
            intents=[
                OperationSetRecordIntent(
                    key="directions",
                    action="create",
                    record_kind="decision_record",
                    semantic_id="KAOJU:DIRECTION-SET",
                    format_profile_ref="isomer:research/record-format/profile/kaoju/decision/direction-set/v2",
                    idea_effects=effects,
                    idea_effects_required=True,
                    root_reason="Actor-confirmed direction set.",
                )
            ],
        )
        applied, diagnostics = apply_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(diagnostics), diagnostics)
        self.assertTrue(applied["ok"], applied)
        item = applied["items"][0]
        self.assertTrue(any(ref.startswith("research-idea:") for ref in item["idea_effect_refs"]))
        self.assertTrue(any(ref.startswith("research-idea-state-transition:") for ref in item["idea_effect_refs"]))
        replayed, replay_diagnostics = apply_operation_set_acceptance(context, manifest_path, env={}, cwd=context.project.root)
        self.assertFalse(has_errors(replay_diagnostics), replay_diagnostics)
        self.assertTrue(replayed["replayed"], replayed)

        store, _ = open_workspace_runtime(context, env={}, read_only=False)
        assert store is not None
        try:
            self.assertEqual(1, len(store.list_research_idea_state_transitions(topic_workspace_id="alpha")))
            with store.connection:
                store.connection.execute("DELETE FROM research_idea_state_transitions WHERE idea_id = ?", (idea_id,))
        finally:
            store.close()
        verified, verify_diagnostics = verify_operation_set_acceptance(context, applied["acceptance"]["id"], env={})
        self.assertFalse(has_errors(verify_diagnostics), verify_diagnostics)
        self.assertFalse(verified["ok"])
        codes = {item["code"] for item in verified["diagnostics"]}
        self.assertIn("operation_set_idea_effect_ref_missing", codes)
        self.assertIn("operation_set_idea_transition_missing", codes)

    def test_fresh_topic_end_to_end_blocks_unclassified_and_replays_all_durable_effects(self) -> None:
        context = self.make_context()
        operation_set = self.actor_operation_set(context, "e2e-closeout")
        write(operation_set / "hypothesis.md", "Stage-pipeline hypothesis.")
        write(operation_set / "direction-set.json", json.dumps({
            "title": "Direction Set",
            "summary": "One selected direction derived from the durable hypothesis.",
            "artifact_family": "kaoju",
            "semantic_id": "KAOJU:DIRECTION-SET",
            "artifact_type": "direction-set",
            "sections": {
                "proposals": [{
                    "id": "direction-e2e",
                    "idea_id": "e2e-stage-pipeline",
                    "title": "Stage pipeline",
                    "summary": "Model runtime as explicit stages.",
                    "research_question": "Which stages dominate runtime?",
                    "boundary": "One supported kernel family.",
                    "source_classes": ["paper", "repository", "measurement"],
                    "coverage_date": "2026-07-17",
                    "expected_depth": "white-box",
                    "deliverables": ["model", "validation"],
                    "empirical_feasibility": "available",
                    "source_json_path": "$.sections.proposals[0]",
                    "generation_id": "e2e-generation",
                    "decision_outcome": "selected",
                    "disposition_rationale": "Selected for focused development.",
                }],
                "selections": ["direction-e2e"],
                "confirmation": {"status": "accepted", "actor_ref": "topic-actor:operator"},
            },
            "research_idea_effects": {
                "atomic": True,
                "artifact_family": "kaoju",
                "actor_ref": "topic-actor:operator",
                "ideas": [{
                    "idea_id": "e2e-stage-pipeline",
                    "title": "Stage pipeline",
                    "summary": "Model runtime as explicit stages.",
                    "source_json_path": "$.sections.proposals[0]",
                    "exploration_state": "unexplored",
                    "decision_state": "selected",
                    "evidence_state": "unassessed",
                    "archive_state": "active",
                    "visibility": "primary",
                    "aliases": ["direction-e2e"],
                }],
                "generation_groups": [{
                    "generation_id": "e2e-generation",
                    "purpose": "End-to-end candidate generation.",
                    "member_idea_ids": ["e2e-stage-pipeline"],
                    "parent_idea_ids": [],
                }],
                "decision_options": [{
                    "idea_id": "e2e-stage-pipeline",
                    "outcome": "selected",
                    "ordinal": 0,
                    "generation_id": "e2e-generation",
                    "rationale": "Selected for focused development.",
                    "actor_ref": "topic-actor:operator",
                }],
                "transitions": [{
                    "idea_id": "e2e-stage-pipeline",
                    "facet": "decision_state",
                    "previous_value": "open",
                    "next_value": "selected",
                    "actor_ref": "topic-actor:operator",
                    "rationale": "Selected for focused development.",
                }],
            },
        }, indent=2) + "\n")
        write(operation_set / "scratch.log", "temporary")
        payload = operation_set / "direction-set.json"
        effects = json.loads(payload.read_text(encoding="utf-8"))["research_idea_effects"]
        durable_outputs = [
            OperationSetOutput(key="hypothesis", path="hypothesis.md", digest=file_digest(operation_set / "hypothesis.md"), size_bytes=(operation_set / "hypothesis.md").stat().st_size, disposition="record_payload", record_key="hypothesis"),
            OperationSetOutput(key="directions", path="direction-set.json", digest=file_digest(payload), size_bytes=payload.stat().st_size, media_type="application/json", disposition="record_payload", record_key="directions"),
        ]
        intents = [
            OperationSetRecordIntent(key="hypothesis", action="create", record_kind="artifact", semantic_id="DEEPSCI:SELECTED-HYPOTHESIS", root_reason="Fresh end-to-end root."),
            OperationSetRecordIntent(
                key="directions",
                action="create",
                record_kind="decision_record",
                semantic_id="KAOJU:DIRECTION-SET",
                format_profile_ref="isomer:research/record-format/profile/kaoju/decision/direction-set/v2",
                parents=[{"local_record_key": "hypothesis", "lineage_kind": "derived_from"}],
                idea_effects=effects,
                idea_effects_required=True,
            ),
        ]
        manifest_path, _ = self.manifest(context, operation_set, outputs=durable_outputs, intents=intents)

        status, unclassified = self.run_operation_sets_cli(context, ["inspect", str(operation_set), "--topic-actor", "operator"])
        self.assertEqual(1, status, unclassified)
        self.assertIn("operation_set_output_unclassified", {item["code"] for item in unclassified["diagnostics"]})

        final_outputs = [
            *durable_outputs,
            OperationSetOutput(key="scratch", path="scratch.log", digest=file_digest(operation_set / "scratch.log"), size_bytes=(operation_set / "scratch.log").stat().st_size, disposition="disposable", reason="Transient end-to-end fixture trace."),
        ]
        manifest_path, _ = self.manifest(context, operation_set, outputs=final_outputs, intents=intents)
        status, preview = self.run_operation_sets_cli(context, ["accept", str(manifest_path), "--topic-actor", "operator"])
        self.assertEqual(0, status, preview)
        self.assertTrue(preview["ok"], preview)
        self.assertFalse(preview["mutated"])

        status, applied = self.run_operation_sets_cli(context, ["accept", str(manifest_path), "--topic-actor", "operator", "--apply"])
        self.assertEqual(0, status, applied)
        self.assertEqual("complete", applied["acceptance"]["status"])
        items = {item["intent_key"]: item for item in applied["items"]}
        parent_id = items["hypothesis"]["record_id"]
        child_id = items["directions"]["record_id"]

        store, _ = open_workspace_runtime(context, env={}, read_only=True)
        assert store is not None
        try:
            records_before = len(store.list_lifecycle_records())
            lineage_before = len(store.list_research_record_lineage_edges(topic_workspace_id="alpha", child_record_id=child_id))
            transitions_before = len(store.list_research_idea_state_transitions(topic_workspace_id="alpha"))
            self.assertIsNotNone(store.get_lifecycle_record(parent_id))
            self.assertIsNotNone(store.get_lifecycle_record(child_id))
            self.assertEqual(1, lineage_before)
            self.assertIsNotNone(store.get_research_idea("e2e-stage-pipeline", topic_workspace_id="alpha"))
            self.assertTrue(any(item.record_id == child_id for item in store.list_research_idea_realizations(topic_workspace_id="alpha", idea_id="e2e-stage-pipeline")))
        finally:
            store.close()

        status, replayed = self.run_operation_sets_cli(context, ["accept", str(manifest_path), "--topic-actor", "operator", "--apply"])
        self.assertEqual(0, status, replayed)
        self.assertTrue(replayed["replayed"], replayed)
        status, verified = self.run_operation_sets_cli(context, ["verify", applied["acceptance"]["id"]])
        self.assertEqual(0, status, verified)
        self.assertTrue(verified["verified"], verified)

        store, _ = open_workspace_runtime(context, env={}, read_only=True)
        assert store is not None
        try:
            self.assertEqual(records_before, len(store.list_lifecycle_records()))
            self.assertEqual(lineage_before, len(store.list_research_record_lineage_edges(topic_workspace_id="alpha", child_record_id=child_id)))
            self.assertEqual(transitions_before, len(store.list_research_idea_state_transitions(topic_workspace_id="alpha")))
        finally:
            store.close()

    def test_cli_preview_apply_replay_verify_and_selector_errors(self) -> None:
        context = self.make_context()
        help_output = io.StringIO()
        with (
            contextlib.chdir(context.project.root),
            contextlib.redirect_stdout(help_output),
        ):
            help_status = cli.main(["ext", "research", "operation-sets", "accept", "--help"])
        self.assertEqual(0, help_status)
        self.assertIn("Preview a complete acceptance plan", help_output.getvalue())
        self.assertIn("--apply", help_output.getvalue())
        operation_set = self.actor_operation_set(context)
        write(operation_set / "report.md", "report")
        manifest_path, _ = self.manifest(
            context,
            operation_set,
            outputs=[
                OperationSetOutput(
                    key="report",
                    path="report.md",
                    digest=file_digest(operation_set / "report.md"),
                    size_bytes=6,
                    disposition="record_payload",
                    record_key="report",
                )
            ],
            intents=[
                OperationSetRecordIntent(
                    key="report",
                    action="create",
                    record_kind="artifact",
                    root_reason="Standalone report.",
                )
            ],
        )
        status, inspected = self.run_operation_sets_cli(
            context,
            ["inspect", str(operation_set), "--topic-actor", "operator"],
        )
        self.assertEqual(0, status, inspected)
        self.assertTrue(inspected["reconciled"])

        status, ambiguous = self.run_operation_sets_cli(
            context,
            [
                "inspect",
                str(operation_set),
                "--topic-actor",
                "operator",
                "--agent",
                "alice",
            ],
        )
        self.assertEqual(1, status, ambiguous)
        self.assertIn(
            "operation_set_worker_ambiguous",
            {item["code"] for item in ambiguous["diagnostics"]},
        )

        status, preview = self.run_operation_sets_cli(
            context,
            ["accept", str(manifest_path), "--topic-actor", "operator"],
        )
        self.assertEqual(0, status, preview)
        self.assertEqual("preview", preview["mode"])
        self.assertFalse(preview["mutated"])

        status, applied = self.run_operation_sets_cli(
            context,
            ["accept", str(manifest_path), "--topic-actor", "operator", "--apply"],
        )
        self.assertEqual(0, status, applied)
        self.assertEqual("complete", applied["acceptance"]["status"])
        self.assertTrue(applied["mutated"])
        status, replayed = self.run_operation_sets_cli(
            context,
            ["accept", str(manifest_path), "--topic-actor", "operator", "--apply"],
        )
        self.assertEqual(0, status, replayed)
        self.assertTrue(replayed["replayed"])

        status, verified = self.run_operation_sets_cli(
            context,
            ["verify", applied["acceptance"]["id"]],
        )
        self.assertEqual(0, status, verified)
        self.assertTrue(verified["verified"])
        status, missing = self.run_operation_sets_cli(context, ["verify", "missing-receipt"])
        self.assertEqual(1, status, missing)
        self.assertEqual("operation_set_acceptance_not_found", missing["error"]["code"])

if __name__ == "__main__":
    unittest.main()
