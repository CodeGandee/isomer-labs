from __future__ import annotations

import unittest

from pydantic import ValidationError

from isomer_labs.web.contracts import (
    IdeaDetailResponseContract,
    TopicGraphResponseContract,
    TopicOverviewResponseContract,
    ensure_gui_payload,
    validate_gui_payload,
)


class ProjectWebContractTests(unittest.TestCase):
    def test_topic_overview_contract_accepts_extra_fields(self) -> None:
        payload = {
            "ok": True,
            "mutated": False,
            "topic_id": "alpha",
            "topic_workspace_id": "alpha",
            "overview": {
                "semantic_label": "topic.intent.overview",
                "exists": True,
                "content_markdown": "# Alpha",
                "agent_extra": {"round": 3},
            },
            "topic_payload": {"ok": True, "extra": "kept"},
            "runtime_payload": {"ok": True},
            "diagnostics": [],
            "future_viewer_hint": {"mode": "compact"},
        }

        model = validate_gui_payload(payload, TopicOverviewResponseContract)

        self.assertEqual("alpha", model.topic_id)
        self.assertEqual({"mode": "compact"}, model.__pydantic_extra__["future_viewer_hint"])

    def test_topic_graph_contract_rejects_missing_required_node_field(self) -> None:
        payload = {
            "ok": True,
            "mutated": False,
            "topic_id": "alpha",
            "topic_workspace_id": "alpha",
            "graph_scope": "idea-lineage",
            "renderer_hint": "react-flow-detail",
            "generated_at": "2026-07-08T00:00:00Z",
            "nodes": [
                {
                    "id": "idea:idea-a",
                    "record_id": "record-a",
                    "material_kind": "idea",
                    "density_class": "sparse",
                }
            ],
            "edges": [],
            "groups": [],
            "facets": {},
            "diagnostics": [],
        }

        with self.assertRaises(ValidationError) as raised:
            validate_gui_payload(payload, TopicGraphResponseContract)

        self.assertIn("nodes.0.title", str(raised.exception))

    def test_idea_detail_contract_accepts_nested_agent_metadata(self) -> None:
        payload = {
            "ok": True,
            "mutated": False,
            "topic_id": "alpha",
            "topic_workspace_id": "alpha",
            "idea_id": "idea-a",
            "idea": {"idea_id": "idea-a", "title": "Idea A", "agent_rank": 1},
            "realizations": [{"idea_id": "idea-a", "record_id": "record-a", "latest": True}],
            "generation_groups": [],
            "incoming_edges": [],
            "outgoing_edges": [],
            "source": {
                "source_kind": "latest_realization_source_path",
                "source_json_available": True,
                "source_json_truncated": False,
                "source_json_bytes": 64,
                "source_json": {"title": "Idea A", "agent_notes": ["extra"]},
            },
            "diagnostics": [],
            "agent_specific": {"trace": "extra"},
        }

        model = validate_gui_payload(payload, IdeaDetailResponseContract)

        self.assertEqual("idea-a", model.idea_id)
        self.assertEqual({"trace": "extra"}, model.__pydantic_extra__["agent_specific"])

    def test_ensure_gui_payload_returns_diagnostic_safe_payload(self) -> None:
        payload = {
            "ok": True,
            "mutated": False,
            "topic_id": "alpha",
            "diagnostics": [],
        }

        safe = ensure_gui_payload(payload, TopicOverviewResponseContract, contract_name="topic-overview")

        self.assertFalse(safe["ok"])
        self.assertEqual("gui_contract_validation_failed", safe["diagnostics"][0]["code"])


if __name__ == "__main__":
    unittest.main()
