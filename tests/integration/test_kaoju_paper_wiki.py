from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import signal
import socket
import tempfile
import textwrap
import time
import unittest
from unittest.mock import patch

from isomer_labs import cli
from isomer_labs.kaoju.contracts import load_binding_registry


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class KaojuPaperWikiIntegrationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.path = os.environ.get("PATH", "")
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
            patch.dict(os.environ, {"HOME": str(self.root), "PATH": self.path}, clear=True),
            contextlib.redirect_stdout(stdout),
        ):
            status = cli.main(["--print-json", *arguments])
        return status, json.loads(stdout.getvalue())

    def artifact(self, *arguments: str) -> tuple[int, dict[str, object]]:
        return self.run_cli("project", "--root", str(self.root), "artifacts", *arguments, "--topic", "alpha")

    def paper(self, command: str, *arguments: str) -> tuple[int, dict[str, object]]:
        return self.run_cli("ext", "kaoju", "paper", command, *arguments, "--project", str(self.root), "--topic", "alpha")

    def wiki(self, command: str, *arguments: str) -> tuple[int, dict[str, object]]:
        return self.run_cli("ext", "kaoju", "wiki", command, *arguments, "--project", str(self.root), "--topic", "alpha")

    def put_structured(
        self,
        semantic_id: str,
        record_id: str,
        producer: str,
        *,
        relationships: dict[str, str],
        sections: dict[str, object] | None = None,
        scope: str | None = None,
        status: str = "ready",
    ) -> dict[str, object]:
        path = self.root / "inputs" / f"{record_id}.json"
        selected_sections = dict(sections or {"state": {"status": "accepted"}})
        required_sections: dict[str, dict[str, object]] = {
            "KAOJU:AUDIT-REPORT": {"findings": [{"check": "evidence-lineage", "status": "pass"}], "verdict": {"status": "ready"}},
            "KAOJU:SOURCE-DIGEST": {"source": {"ref": "source"}, "source_identity": {"work": "Source", "version": "v1"}, "findings": [{"locator": "section 1", "source_statement": "Observed statement.", "interpretation": "Bounded interpretation."}], "approval": {"status": "approved", "actor_ref": "topic-actor:test"}},
            "KAOJU:CITATION-MAP": {"citations": {"fixture": {"source_ref": "source"}}, "displays": {"planned": []}},
            "KAOJU:FIELD-SUMMARY": {"synthesis": {"conclusions": [{"text": "Bounded conclusion"}]}},
        }
        selected_sections = {**required_sections.get(semantic_id, {}), **selected_sections}
        payload = {
            "title": record_id.replace("-", " ").title(),
            "summary": f"Accepted {semantic_id} fixture.",
            "artifact_family": "kaoju",
            "semantic_id": semantic_id,
            "artifact_type": load_binding_registry()[semantic_id].artifact_type,
            "sections": selected_sections,
        }
        write(path, json.dumps(payload, indent=2) + "\n")
        args = [
            "put",
            semantic_id,
            str(path),
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
            args.extend(["--scope-key", scope])
        status, result = self.artifact(*args)
        self.assertEqual(0, status, result)
        return result

    def put_file(
        self,
        semantic_id: str,
        record_id: str,
        producer: str,
        path: Path,
        *,
        relationships: dict[str, str],
        scope: str,
    ) -> dict[str, object]:
        status, result = self.artifact(
            "put",
            semantic_id,
            str(path),
            "--producer",
            producer,
            "--id",
            record_id,
            "--scope-key",
            scope,
            "--relationships-json",
            json.dumps([{"role": role, "target_ref": target} for role, target in relationships.items()]),
        )
        self.assertEqual(0, status, result)
        return result

    def paper_inputs(self) -> dict[str, str]:
        self.put_structured(
            "KAOJU:AUDIT-REPORT",
            "audit-ready",
            "isomer-kaoju-audit",
            relationships={"claim_ledger": "claims-ready", "catalog": "catalog-ready"},
            scope="survey-main",
        )
        self.put_structured(
            "KAOJU:SOURCE-DIGEST",
            "source-digest-1",
            "isomer-kaoju-examine",
            relationships={"source": "paper-1", "repository": "repo-1"},
            sections={"source_identity": {"work": "Paper One", "version": "v1"}},
            scope="source-1",
        )
        display = self.root / "inputs/throughput-figure.svg"
        write(display, '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="10"><rect width="20" height="10"/></svg>\n')
        self.put_file(
            "KAOJU:PAPER-DISPLAY",
            "paper-display-1",
            "isomer-kaoju-write",
            display,
            relationships={"evidence": "source-digest-1"},
            scope="paper-main",
        )
        self.put_structured(
            "KAOJU:CITATION-MAP",
            "citation-map-1",
            "isomer-kaoju-write",
            relationships={"paper_draft": "paper-draft-1", "evidence": "source-digest-1"},
            sections={"citations": {"paper-one": {"source_ref": "source-digest-1"}}, "displays": {"throughput": {"artifact_ref": "paper-display-1", "role": "figure", "evidence_refs": ["source-digest-1"], "caption_status": "verified", "insertion_locator": "method comparison"}}},
            scope="paper-main",
        )
        structure = self.root / "inputs/paper-structure.md"
        write(
            structure,
            """
            # Title
            {{title}}

            ## Abstract
            {{abstract}}

            ## Introduction
            {{introduction}}

            ## Background
            {{background}}

            ## Related Work
            {{related work}}

            ## Method Comparison
            {{method comparison}}

            {{figure:paper-display-1}}

            ## Discussion
            {{discussion}}

            ## Conclusion
            {{conclusion}}

            ## References
            {{references}}

            ## Appendix Details
            {{appendix details}}
            """,
        )
        self.put_file(
            "KAOJU:PAPER-STRUCTURE-MYST",
            "paper-structure-1",
            "isomer-kaoju-write",
            structure,
            relationships={"paper_contract": "paper-contract-1"},
            scope="paper-main",
        )
        draft = self.root / "inputs/paper-draft.md"
        write(
            draft,
            """
            # Title
            Evidence-Led Systems Survey

            ## Abstract
            This survey summarizes accepted evidence {cite}`paper-one`.

            ## Introduction
            The question and boundary are explicit.

            ## Background
            This section defines the mechanism.

            ## Related Work
            Accepted works remain version-aware.

            ## Method Comparison
            The comparison preserves non-comparable cells.

            ## Discussion
            Contradictions and limitations remain visible.

            ## Conclusion
            The conclusion is calibrated to the evidence.

            ## References
            {cite}`paper-one`

            ## Appendix Details
            Grounded optional detail that requires orphan confirmation.
            """,
        )
        self.put_file(
            "KAOJU:PAPER-DRAFT-MYST",
            "paper-draft-1",
            "isomer-kaoju-write",
            draft,
            relationships={"paper_structure": "paper-structure-1", "paper_template": "paper-template-seed", "citation_map": "citation-map-1"},
            scope="paper-main",
        )
        return {"structure": "paper-structure-1", "draft": "paper-draft-1", "citation": "citation-map-1", "source": "source-digest-1", "display": "paper-display-1", "audit": "audit-ready"}

    def test_myst_template_exchange_derivation_tex_build_and_publication_gate(self) -> None:
        refs = self.paper_inputs()
        source_path = self.root / "inputs/paper-structure.md"
        status, validation = self.paper("validate", str(source_path))
        self.assertEqual(0, status, validation)
        self.assertEqual([], [item for item in validation["diagnostics"] if item["severity"] == "error"])

        export_one = self.root / "actor/template-export-1"
        status, exported = self.paper(
            "export-template",
            "--source-ref",
            refs["structure"],
            "--paper-line",
            "paper-main",
            "--draft-ref",
            refs["draft"],
            "--citation-map-ref",
            refs["citation"],
            "--source-digest-ref",
            refs["source"],
            "--display-ref",
            refs["display"],
            "--target",
            str(export_one),
        )
        self.assertEqual(0, status, exported)
        manifest = json.loads((export_one / "manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(refs["structure"], manifest["source_template_ref"])
        self.assertEqual([refs["display"]], manifest["display_refs"])
        self.assertTrue(str(manifest["base_digest"]).startswith("sha256:"))

        revised_structure = self.root / "inputs/paper-structure-v2.md"
        revised_structure.write_text(source_path.read_text(encoding="utf-8").replace("{{discussion}}", "{{discussion}}\n"), encoding="utf-8")
        status, revised = self.artifact(
            "revise",
            refs["structure"],
            str(revised_structure),
            "--producer",
            "isomer-kaoju-write",
            "--scope-key",
            "paper-main",
            "--id",
            "paper-structure-2",
            "--relationships-json",
            '[{"role":"paper_contract","target_ref":"paper-contract-1"}]',
        )
        self.assertEqual(0, status, revised)
        status, stale = self.paper("apply-template", str(export_one))
        self.assertEqual(1, status)
        self.assertEqual("paper_template_stale_base", stale["error"]["code"])
        status, no_template = self.artifact("latest", "KAOJU:PAPER-TEMPLATE-MYST", "--scope-key", "paper-main")
        self.assertEqual(0, status, no_template)
        self.assertEqual([], no_template["records"])

        export_two = self.root / "actor/template-export-2"
        status, exported_two = self.paper(
            "export-template",
            "--source-ref",
            "paper-structure-2",
            "--paper-line",
            "paper-main",
            "--draft-ref",
            refs["draft"],
            "--citation-map-ref",
            refs["citation"],
            "--source-digest-ref",
            refs["source"],
            "--display-ref",
            refs["display"],
            "--target",
            str(export_two),
        )
        self.assertEqual(0, status, exported_two)
        template_file = export_two / "paper-template.md"
        original = template_file.read_text(encoding="utf-8")
        template_file.write_text(original + "\n{{unregistered-placeholder}}\n", encoding="utf-8")
        status, invalid = self.paper("apply-template", str(export_two))
        self.assertEqual(1, status)
        self.assertEqual("paper_template_invalid", invalid["error"]["code"])

        without_appendix = original.split("## Appendix Details", 1)[0].rstrip() + "\n"
        template_file.write_text(without_appendix, encoding="utf-8")
        status, orphaned = self.paper("apply-template", str(export_two))
        self.assertEqual(1, status)
        self.assertEqual("paper_template_orphan_confirmation_required", orphaned["error"]["code"])
        status, applied = self.paper("apply-template", "--confirm-orphans", str(export_two))
        self.assertEqual(0, status, applied)
        self.assertIn("appendix details", applied["orphaned_sections"])

        status, markdown = self.paper(
            "derive-markdown",
            "--source-ref",
            str(applied["draft_ref"]),
            "--paper-line",
            "paper-main",
        )
        self.assertEqual(0, status, markdown)
        self.assertFalse(markdown["canonical"])

        status, initialized = self.paper(
            "init-tex",
            "--draft-ref",
            str(applied["draft_ref"]),
            "--template-myst-ref",
            str(applied["template_ref"]),
            "--paper-line",
            "paper-main",
            "--citation-ref",
            refs["citation"],
        )
        self.assertEqual(0, status, initialized)
        self.assertFalse(initialized["build_ready"])
        self.assertTrue(initialized["agent_inspection_required"])
        status, initialized_again = self.paper(
            "init-tex",
            "--draft-ref",
            str(applied["draft_ref"]),
            "--template-myst-ref",
            str(applied["template_ref"]),
            "--paper-line",
            "paper-main",
            "--citation-ref",
            refs["citation"],
        )
        self.assertEqual(0, status, initialized_again)
        self.assertTrue(initialized_again["template_reused"])

        self.put_structured(
            "KAOJU:AUDIT-REPORT",
            "audit-blocked",
            "isomer-kaoju-audit",
            relationships={"claim_ledger": "claims-blocked", "catalog": "catalog-blocked"},
            sections={"findings": [{"check": "contradiction", "status": "unresolved"}], "verdict": {"status": "blocked"}},
            scope="survey-blocked",
            status="blocked",
        )
        status, blocked_audit = self.paper(
            "build-pdf",
            "--draft-tex-ref",
            str(initialized_again["draft_ref"]),
            "--template-tex-ref",
            str(initialized_again["template_ref"]),
            "--paper-line",
            "paper-main",
            "--audit-ref",
            "audit-blocked",
            "--inspected",
        )
        self.assertEqual(1, status)
        self.assertEqual("paper_audit_not_accepted", blocked_audit["error"]["code"])

        fake_bin = self.root / "fake-bin"
        compiler = fake_bin / "pdflatex"
        write(compiler, "#!/bin/sh\nprintf '%s\\n' '%PDF-1.4' '1 0 obj' '<<>>' 'endobj' '%%EOF' > main.pdf\n")
        compiler.chmod(0o755)
        self.path = str(fake_bin)
        status, gated = self.paper(
            "build-pdf",
            "--draft-tex-ref",
            str(initialized_again["draft_ref"]),
            "--template-tex-ref",
            str(initialized_again["template_ref"]),
            "--paper-line",
            "paper-main",
            "--audit-ref",
            refs["audit"],
            "--inspected",
        )
        self.assertEqual(0, status, gated)
        self.assertEqual("preferred tectonic unavailable; selected pdflatex", gated["fallback"])
        self.assertFalse(gated["accepted"])
        self.assertEqual("required", gated["pdf_inspection"])

        status, accepted = self.paper(
            "build-pdf",
            "--draft-tex-ref",
            str(initialized_again["draft_ref"]),
            "--template-tex-ref",
            str(initialized_again["template_ref"]),
            "--paper-line",
            "paper-main",
            "--audit-ref",
            refs["audit"],
            "--inspected",
            "--pdf-inspected",
            "--publication-approved",
        )
        self.assertEqual(0, status, accepted)
        self.assertTrue(accepted["accepted"])
        self.assertEqual("approved", accepted["publication_gate"])

    def test_wiki_export_is_idempotent_preserves_human_files_and_deploys_packaged_viewer(self) -> None:
        self.put_structured(
            "KAOJU:AUDIT-REPORT",
            "wiki-audit-1",
            "isomer-kaoju-audit",
            relationships={"claim_ledger": "claims-1", "catalog": "catalog-1"},
            sections={"readiness": {"decision": "ready"}},
            scope="survey-main",
        )
        self.put_structured(
            "KAOJU:FIELD-SUMMARY",
            "wiki-summary-1",
            "isomer-kaoju-synthesize",
            relationships={"audit_report": "wiki-audit-1"},
            sections={"conclusions": [{"text": "Bounded conclusion", "status": "supported"}]},
            scope="survey-main",
        )
        target = self.root / "actor/wiki"
        status, exported = self.wiki(
            "export",
            "--artifact-ref",
            "wiki-audit-1",
            "--artifact-ref",
            "wiki-summary-1",
            "--target",
            str(target),
            "--target-policy",
            "create",
        )
        self.assertEqual(0, status, exported)
        metadata = json.loads((target / "wiki.json").read_text(encoding="utf-8"))
        self.assertEqual("isomer-kaoju-wiki-export-manifest.v1", metadata["schema_version"])
        self.assertEqual(2, len(metadata["sections"]["artifacts"]))
        self.assertTrue(metadata["sections"]["relationships"])

        human_file = target / "human-notes.md"
        write(human_file, "# Human notes\n")
        status, unchanged = self.wiki(
            "export",
            "--artifact-ref",
            "wiki-audit-1",
            "--artifact-ref",
            "wiki-summary-1",
            "--target",
            str(target),
        )
        self.assertEqual(0, status, unchanged)
        self.assertFalse(unchanged["mutated"])
        self.assertTrue(human_file.is_file())

        summary_v2 = self.root / "inputs/wiki-summary-2.json"
        payload = json.loads((self.root / "inputs/wiki-summary-1.json").read_text(encoding="utf-8"))
        payload["sections"]["conclusions"][0]["text"] = "Revised bounded conclusion"
        write(summary_v2, json.dumps(payload, indent=2) + "\n")
        status, revised = self.artifact(
            "revise",
            "wiki-summary-1",
            str(summary_v2),
            "--producer",
            "isomer-kaoju-synthesize",
            "--scope-key",
            "survey-main",
            "--id",
            "wiki-summary-2",
            "--relationships-json",
            '[{"role":"audit_report","target_ref":"wiki-audit-1"}]',
        )
        self.assertEqual(0, status, revised)
        status, refreshed = self.wiki(
            "export",
            "--artifact-ref",
            "wiki-audit-1",
            "--artifact-ref",
            "wiki-summary-2",
            "--target",
            str(target),
        )
        self.assertEqual(0, status, refreshed)
        self.assertTrue(refreshed["changelog"]["changed"])
        self.assertTrue(human_file.is_file())

        viewer = self.root / "actor/viewer"
        status, deployed = self.wiki("deploy", str(target), "--target", str(viewer), "--target-policy", "create")
        self.assertEqual(0, status, deployed)
        for name in ("index.html", "styles.css", "app.js", "viewer-manifest.json", "data/wiki.json"):
            self.assertTrue((viewer / name).is_file(), name)
        self.assertNotIn("imsight-llm-wiki", (viewer / "viewer-manifest.json").read_text(encoding="utf-8"))
        status, redeployed = self.wiki("deploy", str(target), "--target", str(viewer))
        self.assertEqual(0, status, redeployed)
        self.assertFalse(redeployed["mutated"])

        status, dry_run = self.wiki("start", str(viewer), "--port", "0", "--dry-run")
        self.assertEqual(0, status, dry_run)
        self.assertTrue(str(dry_run["url"]).startswith("http://127.0.0.1:"))
        status, network_gate = self.wiki("start", str(viewer), "--host", "0.0.0.0", "--port", "0", "--dry-run")
        self.assertEqual(1, status)
        self.assertEqual("viewer_network_gate_required", network_gate["error"]["code"])

        with socket.socket() as held:
            held.bind(("127.0.0.1", 0))
            port = held.getsockname()[1]
            status, conflict = self.wiki("start", str(viewer), "--port", str(port), "--dry-run")
        self.assertEqual(1, status)
        self.assertEqual("viewer_port_conflict", conflict["error"]["code"])

        status, launched = self.wiki("start", str(viewer), "--port", "0")
        self.assertEqual(0, status, launched)
        pid_file = Path(str(launched["pid_file"]))
        self.assertTrue(pid_file.is_file())
        pid = int(pid_file.read_text(encoding="utf-8").strip())
        os.kill(pid, signal.SIGTERM)
        for _ in range(50):
            if not pid_file.exists():
                break
            time.sleep(0.02)

        page = next(target.glob("pages/**/*.md"))
        page.unlink()
        status, stale = self.wiki("deploy", str(target), "--target", str(viewer))
        self.assertEqual(1, status)
        self.assertEqual("viewer_wiki_target_stale", stale["error"]["code"])

    def test_wiki_default_path_and_unrecognized_target_are_deterministic(self) -> None:
        self.put_structured(
            "KAOJU:AUDIT-REPORT",
            "default-audit",
            "isomer-kaoju-audit",
            relationships={"claim_ledger": "claims-default", "catalog": "catalog-default"},
            scope="survey-default",
        )
        status, exported = self.wiki("export", "--artifact-ref", "default-audit")
        self.assertEqual(0, status, exported)
        target = Path(str(exported["target"]))
        self.assertTrue(str(target).startswith(str(self.root / "topic-workspaces/alpha")))

        unrecognized = self.root / "actor/unrecognized-viewer"
        write(unrecognized / "keep.txt", "human\n")
        status, rejected = self.wiki("deploy", str(target), "--target", str(unrecognized))
        self.assertEqual(1, status)
        self.assertEqual("viewer_target_unrecognized", rejected["error"]["code"])
        self.assertEqual("human\n", (unrecognized / "keep.txt").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
