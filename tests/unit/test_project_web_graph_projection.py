from __future__ import annotations

import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from isomer_labs.web.graph import build_topic_graph_view, project_graph_neighborhood


def _node(node_id: str) -> dict[str, object]:
    return {
        "id": node_id,
        "record_id": node_id.removeprefix("idea:"),
        "material_kind": "idea",
        "density_class": "sparse",
        "title": node_id,
    }


def _edge(edge_id: str, source: str, target: str, relation_kind: str = "derived_from") -> dict[str, object]:
    return {
        "id": edge_id,
        "source": source,
        "target": target,
        "relation_kind": relation_kind,
        "canonical": True,
    }


class ProjectWebGraphProjectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.nodes = [_node(f"idea:{name}") for name in ("a", "b", "c", "d", "x")]
        self.edges = [
            _edge("a-b", "idea:a", "idea:b"),
            _edge("b-c", "idea:b", "idea:c"),
            _edge("c-d", "idea:c", "idea:d", "follow_up_to"),
            _edge("x-c", "idea:x", "idea:c"),
            _edge("cycle", "idea:c", "idea:a"),
        ]

    def project(self, seeds: list[str], radius: int, direction: str = "both", relation_kinds: set[str] | None = None, edge_mode: str = "induced") -> dict[str, object]:
        return project_graph_neighborhood(
            self.nodes,
            self.edges,
            seed_node_ids=seeds,
            hop_radius=radius,
            direction=direction,
            relation_kinds=relation_kinds,
            edge_mode=edge_mode,
        )

    def test_zero_hops_and_unknown_seeds(self) -> None:
        result = self.project(["idea:b", "idea:missing"], 0)

        self.assertTrue(result["ok"])
        self.assertEqual(["idea:b"], [node["id"] for node in result["nodes"]])  # type: ignore[index]
        self.assertEqual([], result["edges"])
        projection = result["projection"]
        self.assertEqual(["idea:b"], projection["resolved_seed_node_ids"])  # type: ignore[index]
        self.assertEqual(["idea:missing"], projection["unresolved_seed_node_ids"])  # type: ignore[index]
        self.assertEqual("graph_projection_seed_not_found", result["diagnostics"][0]["code"])  # type: ignore[index]

    def test_multiple_seeds_use_union(self) -> None:
        result = self.project(["idea:a", "idea:d"], 1)

        self.assertEqual(["idea:a", "idea:b", "idea:c", "idea:d"], [node["id"] for node in result["nodes"]])  # type: ignore[index]

    def test_direction_and_relation_filters_apply_before_traversal(self) -> None:
        outgoing = self.project(["idea:b"], 1, "outgoing", {"derived_from"})
        incoming = self.project(["idea:b"], 1, "incoming", {"derived_from"})

        self.assertEqual(["idea:b", "idea:c"], [node["id"] for node in outgoing["nodes"]])  # type: ignore[index]
        self.assertEqual(["idea:a", "idea:b"], [node["id"] for node in incoming["nodes"]])  # type: ignore[index]

    def test_induced_and_traversal_edges_differ_on_cycle(self) -> None:
        induced = self.project(["idea:a"], 2, "outgoing", edge_mode="induced")
        traversal = self.project(["idea:a"], 2, "outgoing", edge_mode="traversal")

        self.assertEqual({"a-b", "b-c", "cycle"}, {edge["id"] for edge in induced["edges"]})  # type: ignore[index]
        self.assertEqual({"a-b", "b-c"}, {edge["id"] for edge in traversal["edges"]})  # type: ignore[index]

    def test_cycles_malformed_edges_and_safety_bound(self) -> None:
        malformed_edges = [*self.edges, _edge("missing-target", "idea:a", "idea:missing")]
        with patch("isomer_labs.web.graph_projection.MAX_NEIGHBORHOOD_NODES", 2):
            result = project_graph_neighborhood(
                self.nodes,
                malformed_edges,
                seed_node_ids=["idea:a"],
                hop_radius=2,
                direction="both",
                relation_kinds=None,
                edge_mode="induced",
            )

        self.assertFalse(result["ok"])
        self.assertEqual("graph_projection_too_large", result["error"]["code"])  # type: ignore[index]

    def test_shared_projection_fixture(self) -> None:
        fixture_path = Path(__file__).parents[1] / "fixtures" / "idea_graph_neighborhood.json"
        fixture = json.loads(fixture_path.read_text(encoding="utf-8"))

        for case in fixture["cases"]:
            with self.subTest(case=case["name"]):
                result = project_graph_neighborhood(
                    fixture["nodes"],
                    fixture["edges"],
                    seed_node_ids=case["seed_node_ids"],
                    hop_radius=case["hop_radius"],
                    direction=case["direction"],
                    relation_kinds=set(case["relation_kinds"]) or None,
                    edge_mode=case["edge_mode"],
                )
                self.assertEqual(case["expected_node_ids"], [node["id"] for node in result["nodes"]])
                self.assertEqual(case["expected_edge_ids"], [edge["id"] for edge in result["edges"]])

    def test_react_flow_request_above_former_sparse_bound_is_complete(self) -> None:
        context = SimpleNamespace(research_topic=SimpleNamespace(id="alpha"), topic_workspace_id="alpha")
        ideas = [
            {
                "idea_id": f"idea-{index}",
                "display_key": f"I-{index + 1}",
                "title": f"Idea {index}",
                "visibility": "primary",
                "status": "candidate",
            }
            for index in range(121)
        ]
        edges = [
            {
                "id": f"edge-{index}",
                "parent_idea_id": f"idea-{index}",
                "child_idea_id": f"idea-{index + 1}",
                "lineage_kind": "derived_from",
            }
            for index in range(120)
        ]
        export = {"ok": True, "index_revision": "qidx:test", "canonical_ideas": ideas, "canonical_idea_edges": edges}

        complete = build_topic_graph_view(context, export, graph_scope="idea-lineage", renderer="react-flow")
        incomplete = build_topic_graph_view(context, export, graph_scope="idea-lineage", renderer="react-flow", limit=20)

        self.assertTrue(complete["ok"])
        self.assertEqual("react-flow-detail", complete["renderer_hint"])
        self.assertTrue(complete["topology_complete"])
        self.assertEqual(121, complete["total_node_count"])
        self.assertEqual(120, complete["total_edge_count"])
        self.assertEqual(121, len(complete["nodes"]))
        self.assertFalse(incomplete["topology_complete"])
        self.assertEqual(20, len(incomplete["nodes"]))
        self.assertEqual(19, len(incomplete["edges"]))
        self.assertTrue(incomplete["paging"]["truncated"])


if __name__ == "__main__":
    unittest.main()
