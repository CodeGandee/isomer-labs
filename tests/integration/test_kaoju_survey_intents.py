from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import tempfile
import textwrap
import unittest
from unittest.mock import patch

from isomer_labs import cli


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class KaojuSurveyIntentIntegrationTests(unittest.TestCase):
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
        write(self.workspace / "isomer-topic-workspace-summary.md", "# Alpha\n")
        status, result = self.run_cli("project", "--root", str(self.root), "runtime", "init", "--topic", "alpha")
        self.assertEqual(0, status, result)

    @property
    def workspace(self) -> Path:
        return self.root / "topic-workspaces/alpha"

    def run_cli(self, *arguments: str) -> tuple[int, dict[str, object]]:
        output = io.StringIO()
        with (
            contextlib.chdir(self.root),
            patch.dict(os.environ, {"HOME": str(self.root), "PATH": os.environ.get("PATH", "")}, clear=True),
            contextlib.redirect_stdout(output),
        ):
            status = cli.main(["--print-json", *arguments])
        return status, json.loads(output.getvalue())

    def artifact(self, *arguments: str) -> tuple[int, dict[str, object]]:
        return self.run_cli("project", "--root", str(self.root), "artifacts", *arguments, "--topic", "alpha")

    def put(
        self,
        semantic_id: str,
        record_id: str,
        producer: str,
        sections: dict[str, object],
        relationships: dict[str, str],
        *,
        scope: str | None = None,
        status: str = "ready",
    ) -> dict[str, object]:
        payload_path = self.root / "inputs" / f"{record_id}.json"
        write(
            payload_path,
            json.dumps(
                {
                    "title": record_id.replace("-", " ").title(),
                    "summary": f"Accepted {semantic_id} fixture.",
                    "artifact_family": "kaoju",
                    "semantic_id": semantic_id,
                    "artifact_type": semantic_id.removeprefix("kaoju:"),
                    "sections": sections,
                },
                indent=2,
            )
            + "\n",
        )
        arguments = [
            "put",
            semantic_id,
            str(payload_path),
            "--producer",
            producer,
            "--id",
            record_id,
            "--status",
            status,
            "--relationships-json",
            json.dumps([{"role": role, "target_ref": target} for role, target in relationships.items()]),
        ]
        if scope is not None:
            arguments.extend(["--scope-key", scope])
        command_status, result = self.artifact(*arguments)
        self.assertEqual(0, command_status, result)
        return result

    def direction_sections(self) -> dict[str, object]:
        proposals = []
        for identifier, title, feasibility in (
            ("mechanisms", "Memory-offload mechanisms", "available"),
            ("lineage", "Implementation lineage", "requires-environment-work"),
            ("custom-cost", "Custom cost-model direction", "requires-unavailable-hardware-or-service"),
        ):
            proposals.append(
                {
                    "id": identifier,
                    "title": title,
                    "research_question": f"What primary evidence supports {title}?",
                    "boundary": "Systems work through 2026-07-14",
                    "source_classes": ["paper", "technical_report", "framework_doc", "repository", "dataset"],
                    "coverage_date": "2026-07-14",
                    "expected_depth": "full-text and code-level",
                    "deliverables": ["reading-list", "source-digest"],
                    "empirical_feasibility": feasibility,
                    "origin": "actor-custom" if identifier.startswith("custom") else "agent-proposed",
                }
            )
        return {"proposals": proposals, "selections": ["lineage", "custom-cost"], "confirmation": {"status": "accepted", "actor_ref": "topic-actor:researcher"}}

    def reading_items(self, direction: str, *, count: int = 6) -> list[dict[str, object]]:
        source_types = ("paper", "technical_report", "framework_doc", "repository", "dataset", "model")
        items: list[dict[str, object]] = []
        for index, source_type in enumerate(source_types[:count], start=1):
            items.append(
                {
                    "item_id": f"{direction}-item-{index}",
                    "title": f"{direction.title()} source {index}",
                    "source_type": source_type,
                    "urls": [f"https://example.test/{direction}/{index}"],
                    "summary": "Bounded source summary.",
                    "relevance_rationale": f"Addresses direction {direction}.",
                    "estimated_depth": "full-text" if source_type in {"paper", "technical_report"} else "code-level",
                    "query_provenance": {"query": f"{direction} mechanisms", "provider": "configured-literature-provider", "route": "online-search", "searched_through": "2026-07-14"},
                    "status": "planned",
                    "priority": "priority" if index <= 3 else "secondary",
                    "version_family": f"{direction}-family-{index}",
                }
            )
        return items

    def test_uc01_and_uc02_multiple_custom_directions_independent_lists_and_shortage(self) -> None:
        self.put("kaoju:survey-contract", "survey-contract-1", "isomer-kaoju-frame", {"scope": {"question": "How do offload mechanisms work?"}, "status": "active"}, {}, scope="survey:main", status="active")
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
            "propose",
            "--id",
            "run-directions",
        )
        self.assertEqual(0, status, begun)
        self.put("kaoju:direction-set", "directions-1", "isomer-kaoju-frame", self.direction_sections(), {"survey_contract": "survey-contract-1"}, scope="survey:main")
        status, checkpoint = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "runs",
            "checkpoint",
            "--topic",
            "alpha",
            "run-directions",
            "--stage-id",
            "confirmed",
            "--completed-ref",
            "directions-1",
            "--resume-hint",
            "Build the first selected direction reading list.",
        )
        self.assertEqual(0, status, checkpoint)

        for direction in ("lineage", "custom-cost"):
            ledger_id = f"discovery-{direction}"
            self.put(
                "kaoju:discovery-ledger",
                ledger_id,
                "isomer-kaoju-discover",
                {"entries": [{"query": f"{direction} mechanisms", "provider": "configured-literature-provider", "route": "online-search", "searched_through": "2026-07-14", "identity_resolution": "resolved", "version_family": f"{direction}-families", "disposition": "selected", "coverage_limits": ["English-language accessible sources"]}]},
                {"survey_contract": "survey-contract-1"},
                scope=f"direction:{direction}",
            )
            result = self.put(
                "kaoju:reading-list",
                f"reading-{direction}",
                "isomer-kaoju-discover",
                {"direction_id": direction, "items": self.reading_items(direction), "approval": {"status": "approved", "actor_ref": "topic-actor:researcher"}},
                {"direction_set": "directions-1", "discovery_ledger": ledger_id},
                scope=f"direction:{direction}",
            )
            self.assertEqual([], [diagnostic for diagnostic in result["contract_diagnostics"] if diagnostic["severity"] == "warning"])  # type: ignore[index]

        short = self.put(
            "kaoju:reading-list",
            "reading-short",
            "isomer-kaoju-discover",
            {"direction_id": "short", "items": self.reading_items("short", count=4), "approval": {"status": "approved", "actor_ref": "topic-actor:researcher", "coverage_waiver": "bounded search found four reachable sources"}},
            {"direction_set": "directions-1", "discovery_ledger": "discovery-lineage"},
            scope="direction:short",
        )
        warning_codes = {diagnostic["code"] for diagnostic in short["contract_diagnostics"] if diagnostic["severity"] == "warning"}  # type: ignore[index]
        self.assertEqual({"reading_target_short"}, warning_codes)

        duplicate_path = self.root / "inputs/reading-duplicate.json"
        duplicate_items = self.reading_items("duplicate")
        duplicate_items[1]["version_family"] = duplicate_items[0]["version_family"]
        write(
            duplicate_path,
            json.dumps({"title": "Duplicate versions", "summary": "Invalid unresolved version family.", "artifact_family": "kaoju", "semantic_id": "kaoju:reading-list", "artifact_type": "reading-list", "sections": {"direction_id": "duplicate", "items": duplicate_items, "approval": {"status": "pending"}}}, indent=2) + "\n",
        )
        status, duplicate = self.artifact(
            "put",
            "kaoju:reading-list",
            str(duplicate_path),
            "--producer",
            "isomer-kaoju-discover",
            "--id",
            "reading-duplicate",
            "--scope-key",
            "direction:duplicate",
            "--relationships-json",
            '[{"role":"direction_set","target_ref":"directions-1"},{"role":"discovery_ledger","target_ref":"discovery-lineage"}]',
        )
        self.assertEqual(1, status)
        self.assertEqual("artifact_contract_invalid", duplicate["error"]["code"])  # type: ignore[index]

        status, lineage = self.artifact("latest", "kaoju:reading-list", "--scope-key", "direction:lineage")
        self.assertEqual(0, status, lineage)
        status, custom = self.artifact("latest", "kaoju:reading-list", "--scope-key", "direction:custom-cost")
        self.assertEqual(0, status, custom)
        self.assertNotEqual(lineage["records"][0]["record_id"], custom["records"][0]["record_id"])  # type: ignore[index]

    def test_uc03_local_online_ingestion_blocker_refinement_and_resume(self) -> None:
        local_paper = self.root / "actor-material/paper.pdf"
        write(local_paper, "%PDF-1.4\nfixture\n")
        self.put(
            "kaoju:material-acquisition-manifest",
            "material-acquisition-1",
            "isomer-kaoju-acquire",
            {
                "materials": [
                    {"identity": "paper:local-v1", "source_class": "paper", "file_refs": [str(local_paper)], "access_status": "available", "provenance_refs": ["actor-nomination"]},
                    {"identity": "report:online-v2", "source_class": "technical_report", "urls": ["https://example.test/report-v2.pdf"], "access_status": "available", "provenance_refs": ["configured-online-route"]},
                ]
            },
            {"source": "reading-lineage"},
            scope="source:ingestion",
        )
        self.put(
            "kaoju:artifact-library",
            "artifact-library-ingestion",
            "isomer-kaoju-acquire",
            {
                "materials": [
                    {"material_id": "paper-local", "source_identity": "paper:local-v1", "source_class": "paper", "content_ref": str(local_paper), "status": "ready", "provenance_refs": ["material-acquisition-1"]},
                    {"material_id": "report-online", "source_identity": "report:online-v2", "source_class": "technical_report", "content_ref": "https://example.test/report-v2.pdf", "status": "ready", "provenance_refs": ["material-acquisition-1"]},
                ]
            },
            {"material": "material-acquisition-1"},
        )
        self.put(
            "kaoju:source-access-blocker",
            "source-blocker-1",
            "isomer-kaoju-acquire",
            {"blocker": {"status": "blocked", "source_class": "dataset", "reason": "authentication required", "claim_impact": ["benchmark comparison"], "recovery": ["request actor-authorized credential route"]}},
            {"source": "dataset:restricted"},
            scope="source:restricted-dataset",
            status="blocked",
        )

        pending_sections = {
            "source_identity": {"source_class": "paper", "title": "Local paper", "version_family": "paper-local", "stable_id": "paper:local-v1"},
            "findings": [
                {"claim": "The method reduces transfer volume.", "source_class": "paper", "locator": "page 4, section 3.2", "source_statement": "The paper states a reduction in transferred bytes.", "interpretation": "The mechanism may reduce transfer volume under the reported workload."},
                {"claim": "Figure 2 visualizes the reduction.", "source_class": "paper", "locator": "page 5, figure 2", "source_statement": "Figure 2 plots transferred bytes.", "interpretation": "The extracted display is provisional until checked against the original.", "verification": "provisional"},
            ],
            "scope": {"direction_id": "lineage"},
            "method": {"inspection_depth": "full-text"},
            "assumptions": ["reported workload only"],
            "main_claims": ["reduced transfer volume"],
            "evidence": ["page 4, section 3.2", "page 5, figure 2"],
            "limitations": ["dataset blocker prevents benchmark comparison"],
            "relationships": ["material-acquisition-1"],
            "relevant_artifacts": ["artifact-library-ingestion"],
            "approval": {"status": "pending"},
        }
        self.put(
            "kaoju:source-digest",
            "source-digest-pending",
            "isomer-kaoju-examine",
            pending_sections,
            {"source": "paper:local-v1", "repository": "repository:not-applicable"},
            scope="source:paper-local",
        )
        status, begun = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "runs",
            "begin",
            "--topic",
            "alpha",
            "--procedure-id",
            "ingest-reading-item",
            "--stage-id",
            "examine",
            "--id",
            "run-ingest-blocked",
        )
        self.assertEqual(0, status, begun)
        status, blocked = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "runs",
            "checkpoint",
            "--topic",
            "alpha",
            "run-ingest-blocked",
            "--stage-id",
            "verify-display",
            "--completed-ref",
            "source-digest-pending",
            "--blocker-ref",
            "source-blocker-1",
            "--resume-hint",
            "Resume at figure verification after the blocker is resolved.",
            "--status",
            "blocked",
        )
        self.assertEqual(0, status, blocked)

        approved_path = self.root / "inputs/source-digest-approved.json"
        approved_sections = json.loads(json.dumps(pending_sections))
        approved_sections["findings"][1]["verification"] = "verified-against-original"
        approved_sections["approval"] = {"status": "approved", "actor_ref": "topic-actor:researcher", "requested_revision": "verify figure 2"}
        write(
            approved_path,
            json.dumps({"title": "Approved local paper digest", "summary": "Refined and actor-approved source digest.", "artifact_family": "kaoju", "semantic_id": "kaoju:source-digest", "artifact_type": "source-digest", "sections": approved_sections}, indent=2) + "\n",
        )
        status, approved = self.artifact(
            "revise",
            "source-digest-pending",
            str(approved_path),
            "--producer",
            "isomer-kaoju-examine",
            "--id",
            "source-digest-approved",
            "--scope-key",
            "source:paper-local",
            "--relationships-json",
            '[{"role":"source","target_ref":"paper:local-v1"},{"role":"repository","target_ref":"repository:not-applicable"}]',
        )
        self.assertEqual(0, status, approved)
        self.put(
            "kaoju:claim-evidence-ledger",
            "claim-ledger-1",
            "isomer-kaoju-examine",
            {"claims": [{"claim_id": "claim-transfer", "statement": "The method reduces transfer volume under the reported workload.", "evidence_refs": ["source-digest-approved"], "verdict": "supported", "contradictions": [], "limitations": ["reported workload only"]}]},
            {"source_digest": "source-digest-approved"},
            scope="survey:main",
        )
        status, resumed = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "runs",
            "begin",
            "--topic",
            "alpha",
            "--procedure-id",
            "ingest-reading-item",
            "--stage-id",
            "verify-display",
            "--input-ref",
            "source-digest-pending",
            "--id",
            "run-ingest-resumed",
            "--resume-hint",
            "Continue from the first incomplete verification stage.",
        )
        self.assertEqual(0, status, resumed)
        status, completed = self.run_cli(
            "project",
            "--root",
            str(self.root),
            "runs",
            "complete",
            "--topic",
            "alpha",
            "run-ingest-resumed",
            "--terminal-status",
            "complete",
            "--completed-ref",
            "source-digest-approved",
            "--completed-ref",
            "claim-ledger-1",
        )
        self.assertEqual(0, status, completed)
        status, latest = self.artifact("latest", "kaoju:source-digest", "--scope-key", "source:paper-local")
        self.assertEqual(0, status, latest)
        self.assertEqual(["source-digest-approved"], [record["record_id"] for record in latest["records"]])  # type: ignore[index]


if __name__ == "__main__":
    unittest.main()
