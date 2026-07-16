from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace
import unittest

from pydantic import ValidationError

from isomer_labs.records.idea_index import unprojected_idea_bearing_record_diagnostics
from isomer_labs.web.contracts import (
    CanonicalIdeaPortfolioNodeContract,
    IdeaDecisionContextResponseContract,
    IdeaPortfolioMetadataContract,
    IdeaTraversalResponseContract,
    validate_gui_payload,
)
from isomer_labs.web.graph import build_topic_graph_view
from isomer_labs.web.idea_portfolio import PORTFOLIO_PRESET_REGISTRY, facet_counts


class ProjectWebIdeaPortfolioTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture_path = Path(__file__).parents[1] / "fixtures" / "research_idea_portfolio.json"
        cls.fixture = json.loads(fixture_path.read_text(encoding="utf-8"))
        cls.context = SimpleNamespace(
            research_topic=SimpleNamespace(id=cls.fixture["topic_id"]),
            topic_workspace_id=cls.fixture["topic_id"],
        )

    def graph(self, *, preset: str, **filters: object) -> dict[str, object]:
        return self.graph_for(self.fixture, preset=preset, **filters)

    def graph_for(self, fixture: dict[str, object], *, preset: str, **filters: object) -> dict[str, object]:
        export = {
            "ok": True,
            "index_revision": fixture["index_revision"],
            "canonical_ideas": fixture["canonical_ideas"],
            "canonical_idea_realizations": fixture["canonical_idea_realizations"],
            "canonical_idea_edges": fixture["canonical_idea_edges"],
            "canonical_idea_transitions": fixture["canonical_idea_transitions"],
            "canonical_idea_decision_options": fixture["canonical_idea_decision_options"],
            "diagnostics": [],
        }
        context = SimpleNamespace(
            research_topic=SimpleNamespace(id=fixture["topic_id"]),
            topic_workspace_id=fixture["topic_id"],
        )
        return build_topic_graph_view(
            context,
            export,
            graph_scope="idea-lineage",
            preset=preset,
            **filters,
        )

    def test_every_fixed_preset_matches_shared_cross_paradigm_fixture(self) -> None:
        self.assertEqual(set(self.fixture["expected_presets"]), {item["id"] for item in PORTFOLIO_PRESET_REGISTRY})
        for preset, expected in self.fixture["expected_presets"].items():
            with self.subTest(preset=preset):
                graph = self.graph(preset=preset)
                self.assertTrue(graph["ok"], graph)
                self.assertFalse(graph["mutated"])
                self.assertEqual(expected, [node["idea_id"] for node in graph["nodes"]])
                self.assertEqual(preset, graph["portfolio"]["preset"]["id"])
                self.assertEqual(len(self.fixture["canonical_ideas"]), graph["portfolio"]["source_counts"]["ideas"])
                visible_ids = {node["id"] for node in graph["nodes"]}
                self.assertTrue(all(edge["source"] in visible_ids and edge["target"] in visible_ids for edge in graph["edges"]))

    def test_independent_facets_and_decision_summary_remain_explicit(self) -> None:
        graph = self.graph(preset="all-proposed")
        nodes = {node["idea_id"]: node for node in graph["nodes"]}
        self.assertEqual(("unexplored", "selected", "unassessed"), self._facets(nodes["kaoju-selected-unexplored"]))
        self.assertEqual(("explored", "deferred", "supported"), self._facets(nodes["deepsci-explored-deferred"]))
        self.assertEqual(("exploring", "open", "refuted"), self._facets(nodes["kaoju-refuted-open"]))
        self.assertEqual(["exploration_state", "decision_state", "evidence_state"], nodes["legacy-unknown"]["needs_classification"])
        self.assertTrue(nodes["kaoju-selected-unexplored"]["backend_selected"])
        self.assertEqual("decision-direction-set", nodes["kaoju-selected-unexplored"]["decision_summary"]["latest_decision_record_id"])
        self.assertEqual("duplication", nodes["deepsci-closed"]["decision_summary"]["reason_code"])
        self.assertNotIn("source_json", nodes["kaoju-selected-unexplored"])

    def test_explicit_filters_compose_and_report_contradictions(self) -> None:
        composed = self.graph(preset="all-proposed", exploration_state="explored", decision_state="selected,deferred")
        self.assertEqual(["deepsci-explored-deferred", "deepsci-archived-selected"], [node["idea_id"] for node in composed["nodes"]])
        self.assertEqual(["explored"], composed["portfolio"]["explicit_filters"]["exploration_state"])
        self.assertEqual("preset AND explicit_filters", composed["portfolio"]["applied_predicate"]["composition"])

        contradiction = self.graph(preset="selected", decision_state="closed")
        self.assertTrue(contradiction["ok"])
        self.assertEqual([], contradiction["nodes"])
        self.assertTrue(any(item["code"] == "portfolio_filter_contradiction" for item in contradiction["diagnostics"]))

        invalid = self.graph(preset="not-a-preset")
        self.assertFalse(invalid["ok"])
        self.assertEqual("portfolio_preset_unsupported", invalid["error"]["code"])

    def test_facet_counts_cover_source_and_visible_scopes(self) -> None:
        graph = self.graph(preset="current")
        source_counts = graph["portfolio"]["source_counts"]["facets"]
        self.assertEqual(facet_counts(self.fixture["canonical_ideas"]), source_counts)
        self.assertEqual(1, source_counts["visibility"]["supporting"])
        self.assertEqual(1, source_counts["visibility"]["hidden"])
        self.assertEqual(1, graph["portfolio"]["visible_counts"]["facets"]["decision_state"]["selected"])
        self.assertGreaterEqual(graph["portfolio"]["omitted_cross_boundary_edge_count"], 1)

    def test_canonical_contract_requires_facets_and_accepts_unknown_classification(self) -> None:
        graph = self.graph(preset="all-proposed")
        for node in graph["nodes"]:
            validate_gui_payload(node, CanonicalIdeaPortfolioNodeContract)
        unknown = next(node for node in graph["nodes"] if node["idea_id"] == "legacy-unknown")
        self.assertEqual(["exploration_state", "decision_state", "evidence_state"], unknown["needs_classification"])
        missing = dict(unknown)
        missing.pop("evidence_state")
        with self.assertRaises(ValidationError):
            validate_gui_payload(missing, CanonicalIdeaPortfolioNodeContract)
        validate_gui_payload(graph["portfolio"], IdeaPortfolioMetadataContract)

    def test_shared_decision_and_traversal_contract_fixture(self) -> None:
        expected_decision = self.fixture["expected_decision_context"]
        decision_id = expected_decision["decision_record_id"]
        ideas = {item["idea_id"]: item for item in self.fixture["canonical_ideas"]}
        options = [
            {**item, "idea": ideas[item["idea_id"]]}
            for item in self.fixture["canonical_idea_decision_options"]
            if item["decision_record_id"] == decision_id
        ]
        decision_payload = {
            "ok": True,
            "mutated": False,
            "topic_id": self.fixture["topic_id"],
            "topic_workspace_id": self.fixture["topic_id"],
            "operation": "ideas.decision-context",
            "decision_record_id": decision_id,
            "decisions": [{**expected_decision, "options": options, "missing_fields": []}],
            "ideas": [ideas[item["idea_id"]] for item in options],
            "transitions": [item for item in self.fixture["canonical_idea_transitions"] if item.get("decision_record_id") == decision_id],
            "reopen_history": [],
            "index_revision": self.fixture["index_revision"],
            "diagnostics": [],
        }
        validate_gui_payload(decision_payload, IdeaDecisionContextResponseContract)
        self.assertEqual([tuple(item) for item in expected_decision["options"]], [(item["idea_id"], item["outcome"]) for item in options])

        expected_traversal = self.fixture["expected_traversal"]
        graph = self.graph(preset="all-proposed")
        node_ids = set(expected_traversal["complete_node_ids"])
        edge_ids = set(expected_traversal["complete_edge_ids"])
        traversal_payload = {
            "ok": True,
            "mutated": False,
            "topic_id": self.fixture["topic_id"],
            "topic_workspace_id": self.fixture["topic_id"],
            "operation": "ideas.traverse",
            "roots": expected_traversal["root_idea_ids"],
            "resolved_roots": expected_traversal["root_idea_ids"],
            "unresolved_roots": [],
            "direction": expected_traversal["direction"],
            "relation_kinds": ["alternative_to", "derived_from", "follow_up_to"],
            "nodes": [node for node in graph["nodes"] if node["idea_id"] in node_ids],
            "edges": [edge for edge in graph["edges"] if edge["id"] in edge_ids],
            "topology_complete": True,
            "limiting_bounds": [],
            "maximum_observed_depth": 2,
            "counts": {"nodes": len(node_ids), "edges": len(edge_ids)},
            "bounds": {"max_depth": 8, "max_nodes": 500, "max_edges": 1000},
            "continuation": None,
            "index_revision": self.fixture["index_revision"],
            "diagnostics": [],
        }
        validate_gui_payload(traversal_payload, IdeaTraversalResponseContract)
        incomplete = {
            **traversal_payload,
            "topology_complete": False,
            "limiting_bounds": expected_traversal["incomplete_limiting_bounds"],
            "continuation": {"action": "increase_max_depth", "suggested_max_depth": 2},
            "diagnostics": [{"severity": "warning", "code": "idea_traversal_incomplete", "message": "Increase max depth."}],
        }
        validate_gui_payload(incomplete, IdeaTraversalResponseContract)

    def test_kaoju_only_fixture_uses_the_generic_portfolio_contract(self) -> None:
        fixture = self.fixture["kaoju_only"]
        self.assertEqual(set(fixture["expected_presets"]), {item["id"] for item in PORTFOLIO_PRESET_REGISTRY})
        for preset, expected in fixture["expected_presets"].items():
            graph = self.graph_for(fixture, preset=preset)
            self.assertEqual(expected, [node["idea_id"] for node in graph["nodes"]], preset)
        all_proposed = self.graph_for(fixture, preset="all-proposed")
        self.assertTrue(all(node["steering_eligibility"]["eligible"] for node in all_proposed["nodes"]))
        self.assertEqual(
            ["$.research_idea_effects.ideas[0]", "$.research_idea_effects.ideas[1]", "$.research_idea_effects.ideas[2]", "$.research_idea_effects.ideas[3]"],
            [node["source"]["latest_realization"]["source_json_path"] for node in all_proposed["nodes"]],
        )
        self.assertTrue(all(item["semantic_id"] == "KAOJU:DIRECTION-SET" for item in fixture["canonical_idea_realizations"]))

    def test_unprojected_legacy_kaoju_direction_set_remains_diagnostic_only(self) -> None:
        fixture = self.fixture["legacy_unprojected"]
        diagnostics = unprojected_idea_bearing_record_diagnostics(fixture["records"], fixture["canonical_idea_realizations"])
        self.assertEqual([fixture["diagnostic_code"]], [item["code"] for item in diagnostics])
        self.assertEqual(fixture["repair_action"], diagnostics[0]["repair"]["action"])
        self.assertFalse(diagnostics[0]["portfolio_complete"])

    @staticmethod
    def _facets(node: dict[str, object]) -> tuple[object, object, object]:
        return node["exploration_state"], node["decision_state"], node["evidence_state"]


if __name__ == "__main__":
    unittest.main()
