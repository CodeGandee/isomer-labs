from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import textwrap
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from isomer_labs import cli
from isomer_labs.houmao.adapter import HoumaoAdapterFacade
from isomer_labs.records.steering import ResearchIdeaSteeringRequest, steer_research_idea
from isomer_labs.runtime.store import WorkspaceRuntimeStore
from isomer_labs.web.read_model import ProjectWebReadModel


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class ResearchIdeaSteeringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        write(
            self.root / ".isomer-labs" / "manifest.toml",
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
            self.root / ".isomer-labs" / "research-topics" / "alpha.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "alpha"
            topic_statement = "Alpha topic"
            """,
        )
        (self.root / "topic-workspaces" / "alpha").mkdir(parents=True)
        status, output = self.run_main(["--print-json", "project", "--root", str(self.root), "runtime", "init", "--topic", "alpha"])
        self.assertEqual(0, status, output)
        self.env = {"HOME": str(self.root), "PATH": os.environ.get("PATH", "")}
        self.read_model = ProjectWebReadModel(self.root, env=self.env)
        context, diagnostics = self.read_model.topic_context("alpha")
        self.assertIsNotNone(context, diagnostics)
        self.context = context

    def run_main(self, args: list[str]) -> tuple[int, str]:
        stdout = io.StringIO()
        with (
            contextlib.chdir(self.root),
            patch.dict(os.environ, {"HOME": str(self.root), "PATH": os.environ.get("PATH", "")}, clear=True),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(args)
        return status, stdout.getvalue()

    def add_idea(self, idea_id: str, *, exploration: str = "unexplored", decision: str = "open", evidence: str = "unassessed") -> None:
        status, output = self.run_main(
            [
                "--print-json",
                "ext",
                "research",
                "ideas",
                "upsert",
                "--project",
                str(self.root),
                "--topic",
                "alpha",
                "--idea-id",
                idea_id,
                "--title",
                idea_id.replace("-", " ").title(),
                "--summary",
                f"Durable concept {idea_id}.",
                "--exploration-state",
                exploration,
                "--decision-state",
                decision,
                "--evidence-state",
                evidence,
            ]
        )
        self.assertEqual(0, status, output)

    def revision(self) -> str:
        graph = self.read_model.topic_graph("alpha", graph_scope="idea-lineage", preset="all-proposed")
        self.assertTrue(graph["ok"], graph)
        return str(graph["index_revision"])

    def steer(self, request: ResearchIdeaSteeringRequest, *, dispatch: bool = False) -> dict[str, object]:
        payload, diagnostics = steer_research_idea(self.context, env=self.env, request=request, dispatch=dispatch)  # type: ignore[arg-type]
        self.assertFalse(diagnostics)
        return payload

    def test_explore_alongside_is_atomic_idempotent_and_leaves_other_decisions_unchanged(self) -> None:
        self.add_idea("target")
        self.add_idea("selected", decision="selected")
        expected_revision = self.revision()
        request = ResearchIdeaSteeringRequest(
            action="explore",
            target_idea_id="target",
            actor_ref="actor:user",
            idempotency_key="steer-alongside",
            expected_index_revision=expected_revision,
            expected_states={"target": {"exploration_state": "unexplored", "decision_state": "open"}},
            user_prompt="Test the target with a bounded benchmark.",
        )
        result = self.steer(request)
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["mutated"])
        self.assertEqual("pending", result["dispatch_status"])
        self.assertNotEqual(expected_revision, result["new_index_revision"])
        ideas = {item["idea_id"]: item for item in result["resulting_ideas"]}  # type: ignore[index]
        self.assertEqual(("exploring", "open"), (ideas["target"]["exploration_state"], ideas["target"]["decision_state"]))
        selected = self.read_model.topic_graph("alpha", graph_scope="idea-lineage", preset="selected")
        self.assertEqual(["selected"], [item["idea_id"] for item in selected["nodes"]])
        self.assertIsNone(result["decision_record_ref"])
        self.assertTrue(result["research_inquiry_ref"])
        self.assertTrue(result["research_task_ref"])
        self.assertTrue(result["handoff_ref"])
        self.assertIn('"idea_id": "target"', result["planned_prompt"])

        replay = self.steer(request)
        self.assertTrue(replay["ok"])
        self.assertFalse(replay["mutated"])
        self.assertTrue(replay["replayed"])
        self.assertEqual(result["operation_id"], replay["operation_id"])

    def test_explore_instead_records_full_decision_and_defaults_replacement_to_deferred(self) -> None:
        self.add_idea("target")
        self.add_idea("current-a", exploration="exploring", decision="selected")
        self.add_idea("current-b", exploration="explored", decision="selected", evidence="supported")
        result = self.steer(
            ResearchIdeaSteeringRequest(
                action="explore_instead",
                target_idea_id="target",
                actor_ref="actor:user",
                idempotency_key="steer-instead",
                expected_index_revision=self.revision(),
                replaced_idea_ids=["current-a", "current-b"],
                rationale="The target addresses the unresolved runtime mechanism.",
                user_prompt="Explore the replacement and preserve comparator evidence.",
            )
        )
        self.assertTrue(result["ok"], result)
        ideas = {item["idea_id"]: item for item in result["resulting_ideas"]}  # type: ignore[index]
        self.assertEqual(("exploring", "selected"), (ideas["target"]["exploration_state"], ideas["target"]["decision_state"]))
        self.assertEqual("deferred", ideas["current-a"]["decision_state"])
        self.assertEqual("deferred", ideas["current-b"]["decision_state"])
        context = self.read_model.decision_context("alpha", str(result["decision_record_ref"]))
        self.assertTrue(context["ok"], context)
        self.assertEqual(["target", "current-a", "current-b"], [item["idea_id"] for item in context["decisions"][0]["options"]])
        self.assertTrue(context["decisions"][0]["option_set_complete"])

    def test_reopen_gate_stale_revision_and_idempotency_conflict_do_not_mutate(self) -> None:
        self.add_idea("closed", exploration="explored", decision="closed", evidence="mixed")
        revision = self.revision()
        no_confirmation = self.steer(
            ResearchIdeaSteeringRequest(
                action="explore",
                target_idea_id="closed",
                actor_ref="actor:user",
                idempotency_key="closed-no-confirm",
                expected_index_revision=revision,
            )
        )
        self.assertEqual("gate_required", no_confirmation["status"])
        self.assertFalse(no_confirmation["mutated"])
        self.assertEqual(revision, self.revision())

        gated = self.steer(
            ResearchIdeaSteeringRequest(
                action="explore",
                target_idea_id="closed",
                actor_ref="actor:user",
                idempotency_key="closed-gated",
                expected_index_revision=revision,
                reopen_confirmed=True,
                rationale="Reconsider new evidence.",
                gate_policy="reopen",
            )
        )
        self.assertEqual("gate_required", gated["status"])
        self.assertFalse(gated["mutated"])

        stale = self.steer(
            ResearchIdeaSteeringRequest(
                action="explore",
                target_idea_id="closed",
                actor_ref="actor:user",
                idempotency_key="closed-stale",
                expected_index_revision="qidx:stale",
                reopen_confirmed=True,
                rationale="Reconsider new evidence.",
            )
        )
        self.assertEqual("conflict", stale["status"])
        self.assertFalse(stale["mutated"])

        accepted_request = ResearchIdeaSteeringRequest(
            action="explore",
            target_idea_id="closed",
            actor_ref="actor:user",
            idempotency_key="closed-accepted",
            expected_index_revision=revision,
            reopen_confirmed=True,
            rationale="Reconsider new evidence.",
        )
        accepted = self.steer(accepted_request)
        self.assertTrue(accepted["ok"], accepted)
        conflict = self.steer(replace_request(accepted_request, user_prompt="Different input"))
        self.assertEqual("conflict", conflict["status"])

    def test_late_canonical_failure_rolls_back_lifecycle_and_idea_effects(self) -> None:
        self.add_idea("target")
        revision = self.revision()
        original = WorkspaceRuntimeStore.record_handoff

        def fail_after_lifecycle(self: WorkspaceRuntimeStore, record: object) -> None:
            original(self, record)  # type: ignore[arg-type]
            raise ValueError("forced handoff failure")

        with patch.object(WorkspaceRuntimeStore, "record_handoff", fail_after_lifecycle):
            result = self.steer(
                ResearchIdeaSteeringRequest(
                    action="explore",
                    target_idea_id="target",
                    actor_ref="actor:user",
                    idempotency_key="forced-rollback",
                    expected_index_revision=revision,
                )
            )
        self.assertFalse(result["ok"])
        self.assertEqual("steering_transaction_failed", result["error"]["code"])  # type: ignore[index]
        db_path = self.root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(db_path) as connection:
            self.assertEqual(0, connection.execute("SELECT COUNT(*) FROM lifecycle_records WHERE id LIKE '%idea-steering-%'").fetchone()[0])
            self.assertEqual(0, connection.execute("SELECT COUNT(*) FROM research_idea_operations WHERE idempotency_key = 'forced-rollback'").fetchone()[0])
        current = self.read_model.topic_graph("alpha", graph_scope="idea-lineage", preset="all-proposed")
        self.assertEqual("unexplored", current["nodes"][0]["exploration_state"])

    def test_post_commit_dispatch_success_records_delivery_without_losing_canonical_refs(self) -> None:
        self.add_idea("target")
        adapter_result = SimpleNamespace(status="sent", diagnostics=[], to_json=lambda: {"status": "sent", "dispatch_record_id": "dispatch-1"})
        with (
            patch("isomer_labs.records.steering._resolve_dispatch_routing", return_value=("team-1", "operator-1", "topic-lead-1")),
            patch.object(WorkspaceRuntimeStore, "get_agent_team_instance_summary", return_value=SimpleNamespace(id="team-1")),
            patch.object(HoumaoAdapterFacade, "dispatch_handoff", return_value=adapter_result) as dispatch_handoff,
        ):
            result = self.steer(
                ResearchIdeaSteeringRequest(
                    action="explore",
                    target_idea_id="target",
                    actor_ref="actor:user",
                    idempotency_key="dispatch-success",
                    expected_index_revision=self.revision(),
                    user_prompt="Run the bounded target experiment.",
                ),
                dispatch=True,
            )
        self.assertTrue(result["canonical_accepted"], result)
        self.assertEqual("accepted", result["dispatch_status"])
        self.assertEqual("dispatch-1", result["dispatch"]["adapter_result"]["dispatch_record_id"])  # type: ignore[index]
        prompt = dispatch_handoff.call_args.kwargs["message"]
        self.assertIn('"idea_id": "target"', prompt)
        self.assertIn(str(result["research_task_ref"]), prompt)
        db_path = self.root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(db_path) as connection:
            self.assertEqual("sent", connection.execute("SELECT status FROM handoff_records WHERE id = ?", (result["handoff_ref"],)).fetchone()[0])

    def test_post_commit_dispatch_failure_keeps_decision_and_retry_state(self) -> None:
        self.add_idea("target")
        self.add_idea("current", exploration="exploring", decision="selected")
        with (
            patch("isomer_labs.records.steering._resolve_dispatch_routing", return_value=("team-1", "operator-1", "topic-lead-1")),
            patch.object(WorkspaceRuntimeStore, "get_agent_team_instance_summary", return_value=SimpleNamespace(id="team-1")),
            patch.object(HoumaoAdapterFacade, "dispatch_handoff", side_effect=RuntimeError("adapter offline")),
        ):
            result = self.steer(
                ResearchIdeaSteeringRequest(
                    action="explore_instead",
                    target_idea_id="target",
                    actor_ref="actor:user",
                    idempotency_key="dispatch-failure",
                    expected_index_revision=self.revision(),
                    replaced_idea_ids=["current"],
                    rationale="Replace the current route with the exact target.",
                ),
                dispatch=True,
            )
        self.assertTrue(result["ok"], result)
        self.assertTrue(result["canonical_accepted"])
        self.assertEqual("accepted", result["status"])
        self.assertEqual("blocked", result["dispatch_status"])
        self.assertEqual(result["handoff_ref"], result["dispatch"]["retry_ref"])  # type: ignore[index]
        self.assertTrue(any(item["code"] == "steering_dispatch_blocked" for item in result["diagnostics"]))  # type: ignore[index]
        decision = self.read_model.decision_context("alpha", str(result["decision_record_ref"]))
        self.assertTrue(decision["ok"], decision)
        db_path = self.root / "topic-workspaces" / "alpha" / "state.sqlite"
        with sqlite3.connect(db_path) as connection:
            self.assertEqual("blocked", connection.execute("SELECT status FROM handoff_records WHERE id = ?", (result["handoff_ref"],)).fetchone()[0])

    def test_cli_steering_surface_commits_pending_handoff_and_validates_closure_reason(self) -> None:
        self.add_idea("target")
        status, output = self.run_main(
            [
                "--print-json",
                "ext",
                "research",
                "ideas",
                "steer",
                "--project",
                str(self.root),
                "--topic",
                "alpha",
                "--action",
                "explore",
                "--target-idea-id",
                "target",
                "--actor",
                "actor:user",
                "--idempotency-key",
                "cli-steering",
                "--no-dispatch",
            ]
        )
        self.assertEqual(0, status, output)
        payload = json.loads(output)
        self.assertEqual(("accepted", "pending"), (payload["status"], payload["dispatch_status"]))

        invalid, diagnostics = steer_research_idea(
            self.context,
            env=self.env,
            request=ResearchIdeaSteeringRequest(
                action="explore_instead",
                target_idea_id="target",
                actor_ref="actor:user",
                idempotency_key="missing-closure-reason",
                replaced_idea_ids=["current"],
                replacement_dispositions={"current": "closed"},
                rationale="Close the replaced idea.",
            ),
            dispatch=False,
        )
        self.assertFalse(diagnostics)
        self.assertEqual("steering_closure_reason_required", invalid["error"]["code"])


def replace_request(request: ResearchIdeaSteeringRequest, **changes: object) -> ResearchIdeaSteeringRequest:
    values = request.__dict__.copy()
    values.update(changes)
    return ResearchIdeaSteeringRequest(**values)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
