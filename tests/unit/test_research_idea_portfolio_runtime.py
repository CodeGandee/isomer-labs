from __future__ import annotations

from pathlib import Path
import sqlite3
import unittest
from unittest.mock import patch

from isomer_labs.runtime.records import (
    ResearchIdea,
    ResearchIdeaDecisionOption,
    ResearchIdeaStateTransition,
    RuntimeLifecycleRecord,
    project_research_idea_compatibility_status,
)
from isomer_labs.runtime.sqlite import _create_schema
from isomer_labs.runtime.store import WorkspaceRuntimeStore


TOPIC_ID = "topic-alpha"
WORKSPACE_ID = "workspace-alpha"
NOW = "2026-07-17T00:00:00Z"


class ResearchIdeaPortfolioRuntimeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.connection = sqlite3.connect(":memory:")
        self.store = WorkspaceRuntimeStore(Path(":memory:"), self.connection)
        _create_schema(self.connection)
        self.store.upsert_lifecycle_record(self.lifecycle("decision-1", "decision_record"))
        self.store.upsert_lifecycle_record(self.lifecycle("provenance-1", "provenance_record"))

    def tearDown(self) -> None:
        self.store.close()

    def lifecycle(
        self,
        record_id: str,
        record_kind: str,
        *,
        topic_id: str = TOPIC_ID,
        workspace_id: str = WORKSPACE_ID,
    ) -> RuntimeLifecycleRecord:
        return RuntimeLifecycleRecord(
            id=record_id,
            record_kind=record_kind,
            research_topic_id=topic_id,
            topic_workspace_id=workspace_id,
            status="ready",
            created_at=NOW,
            updated_at=NOW,
        )

    def idea(self, **overrides: object) -> ResearchIdea:
        values: dict[str, object] = {
            "id": "idea-row-1",
            "research_topic_id": TOPIC_ID,
            "topic_workspace_id": WORKSPACE_ID,
            "idea_id": "idea-1",
            "display_key": "I-1",
            "title": "Independent facets",
            "summary": "An idea whose portfolio facets can vary independently.",
            "family": None,
            "status": "selected",
            "visibility": "primary",
            "aliases": [],
            "source_record_id": None,
            "source_json_path": None,
            "metadata": {},
            "created_at": NOW,
            "updated_at": NOW,
            "exploration_state": "unexplored",
            "decision_state": "selected",
            "evidence_state": "refuted",
            "archive_state": "active",
        }
        values.update(overrides)
        return ResearchIdea(**values)  # type: ignore[arg-type]

    def transition(self, **overrides: object) -> ResearchIdeaStateTransition:
        values: dict[str, object] = {
            "id": "transition-1",
            "research_topic_id": TOPIC_ID,
            "topic_workspace_id": WORKSPACE_ID,
            "idea_id": "idea-1",
            "facet": "exploration_state",
            "previous_value": "unexplored",
            "next_value": "exploring",
            "operation_id": "operation-1",
            "actor_ref": "actor:user",
            "rationale": "Begin focused exploration.",
            "transitioned_at": "2026-07-17T00:01:00Z",
        }
        values.update(overrides)
        return ResearchIdeaStateTransition(**values)  # type: ignore[arg-type]

    def option(self, **overrides: object) -> ResearchIdeaDecisionOption:
        values: dict[str, object] = {
            "id": "option-1",
            "research_topic_id": TOPIC_ID,
            "topic_workspace_id": WORKSPACE_ID,
            "decision_record_id": "decision-1",
            "idea_id": "idea-1",
            "outcome": "selected",
            "operation_id": "operation-1",
            "created_at": NOW,
            "updated_at": NOW,
        }
        values.update(overrides)
        return ResearchIdeaDecisionOption(**values)  # type: ignore[arg-type]

    def test_independent_facet_combination_and_compatibility_projection(self) -> None:
        idea = self.idea()
        self.assertEqual([], [item for item in self.store.validate_research_idea(idea) if item["severity"] == "error"])
        self.store.upsert_research_idea(idea)
        stored = self.store.get_research_idea("idea-1", topic_workspace_id=WORKSPACE_ID)
        assert stored is not None
        self.assertEqual("unexplored", stored.exploration_state)
        self.assertEqual("selected", stored.decision_state)
        self.assertEqual("refuted", stored.evidence_state)
        self.assertEqual("selected", stored.status)
        self.assertEqual(
            "archived",
            project_research_idea_compatibility_status(
                exploration_state="explored",
                decision_state="selected",
                evidence_state="supported",
                archive_state="archived",
            ),
        )

    def test_invalid_facet_and_compatibility_conflict_are_reported(self) -> None:
        diagnostics = self.store.validate_research_idea(self.idea(exploration_state="invented"))
        self.assertTrue(any(item["code"] == "idea_exploration_state_unsupported" for item in diagnostics))
        diagnostics = self.store.validate_research_idea(self.idea(status="candidate"))
        self.assertTrue(any(item["code"] == "idea_compatibility_status_conflict" for item in diagnostics))

    def test_closure_requires_reason_and_durable_context(self) -> None:
        self.store.upsert_research_idea(self.idea())
        invalid = self.transition(
            facet="decision_state",
            previous_value="selected",
            next_value="closed",
        )
        diagnostics = self.store.validate_research_idea_state_transition(invalid)
        self.assertTrue(any(item["code"] == "idea_closure_reason_missing" for item in diagnostics))
        self.assertTrue(any(item["code"] == "idea_closure_context_missing" for item in diagnostics))
        valid = self.transition(
            facet="decision_state",
            previous_value="selected",
            next_value="closed",
            reason_code="rejection",
            decision_record_id="decision-1",
        )
        self.assertEqual([], [item for item in self.store.validate_research_idea_state_transition(valid) if item["severity"] == "error"])

    def test_transition_rejects_cross_topic_refs(self) -> None:
        self.store.upsert_research_idea(self.idea())
        self.store.upsert_lifecycle_record(self.lifecycle("decision-other", "decision_record", topic_id="topic-other", workspace_id="workspace-other"))
        transition = self.transition(decision_record_id="decision-other")
        diagnostics = self.store.validate_research_idea_state_transition(transition)
        self.assertTrue(any(item["code"] == "idea_durable_ref_cross_topic" for item in diagnostics))

    def test_atomic_mutation_rolls_back_current_state_and_history(self) -> None:
        self.store.upsert_research_idea(self.idea())
        self.connection.commit()
        transition = self.transition()
        option = self.option()
        with patch.object(self.store, "upsert_research_idea_decision_option", side_effect=sqlite3.IntegrityError("forced failure")):
            with self.assertRaises(sqlite3.IntegrityError):
                self.store.apply_research_idea_mutation(transitions=[transition], decision_options=[option])
        stored = self.store.get_research_idea("idea-1", topic_workspace_id=WORKSPACE_ID)
        assert stored is not None
        self.assertEqual("unexplored", stored.exploration_state)
        self.assertEqual([], self.store.list_research_idea_state_transitions(topic_workspace_id=WORKSPACE_ID))

    def test_additive_schema_migration_preserves_legacy_status(self) -> None:
        connection = sqlite3.connect(":memory:")
        connection.row_factory = sqlite3.Row
        connection.execute(
            """
            CREATE TABLE research_ideas (
                id TEXT PRIMARY KEY,
                research_topic_id TEXT NOT NULL,
                topic_workspace_id TEXT NOT NULL,
                idea_id TEXT NOT NULL,
                display_key TEXT,
                title TEXT NOT NULL,
                summary TEXT NOT NULL,
                family TEXT,
                status TEXT NOT NULL,
                visibility TEXT NOT NULL,
                aliases_json TEXT NOT NULL,
                source_record_id TEXT,
                source_json_path TEXT,
                metadata_json TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                provenance_refs_json TEXT NOT NULL,
                UNIQUE(topic_workspace_id, idea_id)
            )
            """
        )
        connection.execute(
            "INSERT INTO research_ideas VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("legacy-row", TOPIC_ID, WORKSPACE_ID, "legacy-idea", "I-1", "Legacy", "Legacy idea.", None, "supported", "primary", "[]", None, None, "{}", NOW, NOW, "[]"),
        )
        _create_schema(connection)
        columns = {row[1] for row in connection.execute("PRAGMA table_info(research_ideas)")}
        row = connection.execute("SELECT status, exploration_state, decision_state, evidence_state, archive_state FROM research_ideas").fetchone()
        self.assertTrue({"exploration_state", "decision_state", "evidence_state", "archive_state"}.issubset(columns))
        self.assertEqual(("supported", "unknown", "unknown", "unknown", "active"), tuple(row))
        connection.close()


if __name__ == "__main__":
    unittest.main()
