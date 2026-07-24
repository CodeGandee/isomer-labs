from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import shutil
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

    def paper_inputs(self, template_ref: str = "paper-template-seed") -> dict[str, str]:
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
            sections={"citations": [{"cite_key": "paper-one", "title": "Paper One", "source_identity": "arxiv:0000.00001", "source_digest_ref": "source-digest-1", "display_role": "primary_source"}], "displays": {"throughput": {"artifact_ref": "paper-display-1", "role": "figure", "evidence_refs": ["source-digest-1"], "caption_status": "verified", "insertion_locator": "method comparison"}}},
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
            """---
title: "Evidence-Led Systems Survey"
authors:
  - name: "Integration Agent"
---

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
            relationships={"paper_structure": "paper-structure-1", "paper_template": template_ref, "citation_map": "citation-map-1"},
            scope="paper-main",
        )
        return {"structure": "paper-structure-1", "draft": "paper-draft-1", "citation": "citation-map-1", "source": "source-digest-1", "display": "paper-display-1", "audit": "audit-ready"}

    def test_myst_template_exchange_derivation_tex_build_and_publication_gate(self) -> None:
        prepared = self.root / "inputs/named-paper-template"
        write(
            prepared / "paper/index.md",
            """
            # {{title}}

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

            ## Discussion
            {{discussion}}

            ## Conclusion
            {{conclusion}}

            ## References
            {{references}}
            """,
        )
        write(prepared / "myst.yml", "project:\n  title: Integration template\n")
        metadata_path = self.root / "inputs/template-metadata.json"
        write(metadata_path, '{"entrypoint":"paper/index.md","use_guidance":"Use the paper entrypoint."}\n')
        status, created_template = self.paper(
            "template",
            "create",
            "--name",
            "main",
            "--from",
            str(prepared),
            "--metadata-file",
            str(metadata_path),
            "--actor",
            "agent:integration",
        )
        self.assertEqual(0, status, created_template)
        refs = self.paper_inputs(str(created_template["stable_ref"]))
        source_path = self.root / "inputs/paper-structure.md"
        status, validation = self.paper("validate", str(source_path))
        self.assertEqual(0, status, validation)
        self.assertEqual([], [item for item in validation["diagnostics"] if item["severity"] == "error"])

        status, exported = self.paper("template", "export", "--actor", "agent:integration")
        self.assertEqual(0, status, exported)
        export_path = Path(str(exported["target"]))
        self.assertEqual(self.root / "topic-workspaces/alpha/intent/derived/writing-templates/content/main", export_path)
        export_metadata = json.loads((export_path / ".isomer-template-export.json").read_text(encoding="utf-8"))
        self.assertEqual("main", export_metadata["template_name"])
        self.assertEqual(created_template["stable_ref"], export_metadata["canonical_ref"])

        exported_entrypoint = export_path / "paper/index.md"
        exported_entrypoint.write_text(exported_entrypoint.read_text(encoding="utf-8") + "\n## Appendix Details\n{{appendix details}}\n", encoding="utf-8")
        status, edited = self.paper("template", "exports")
        self.assertEqual(0, status, edited)
        self.assertEqual("edited", edited["exports"][0]["posture"])
        status, refused = self.paper("template", "export", "--actor", "agent:integration")
        self.assertEqual(1, status)
        self.assertEqual("template_export_edited", refused["error"]["code"])

        candidate = self.root / "actor/agent-prepared-template"
        write(candidate / "paper/index.md", exported_entrypoint.read_text(encoding="utf-8"))
        write(candidate / "myst.yml", (export_path / "myst.yml").read_text(encoding="utf-8"))
        status, updated_template = self.paper(
            "template",
            "update",
            "--name",
            "main",
            "--from",
            str(candidate),
            "--expected-state",
            str(created_template["state_token"]),
            "--actor",
            "agent:integration",
            "--source-ref",
            refs["structure"],
            "--change-summary",
            "Reconcile the user-edited appendix into a clean template tree.",
        )
        self.assertEqual(0, status, updated_template)
        status, observed = self.paper("template", "export", "--name", "main", "--target", str(export_path), "--observe", "--actor", "agent:integration")
        self.assertEqual(0, status, observed)
        self.assertFalse(observed["canonical"])

        status, packaged_latex = self.paper(
            "init-tex",
            "--draft-ref",
            refs["draft"],
            "--content-template-ref",
            str(updated_template["stable_ref"]),
            "--paper-line",
            "paper-main",
        )
        self.assertEqual(0, status, packaged_latex)
        self.assertEqual("packaged-default", packaged_latex["latex_template"]["selection_source"])
        self.assertIsNone(packaged_latex["latex_template"].get("stable_ref"))
        self.assertIn("packaged_identity", packaged_latex["latex_template"])
        status, latex_stock_after_fallback = self.paper(
            "template",
            "list",
            "--kind",
            "latex",
        )
        self.assertEqual(0, status, latex_stock_after_fallback)
        self.assertEqual(0, latex_stock_after_fallback["count"])

        latex_tree = self.root / "inputs/latex-template"
        write(latex_tree / "template.tex", "\\documentclass{fixture}\n\\usepackage{surveyfixture}\n")
        write(latex_tree / "fixture.cls", "\\NeedsTeXFormat{LaTeX2e}\n\\ProvidesClass{fixture}\n\\LoadClass{article}\n")
        write(latex_tree / "surveyfixture.sty", "\\ProvidesPackage{surveyfixture}\n")
        latex_metadata = self.root / "inputs/latex-template-metadata.json"
        write(
            latex_metadata,
            json.dumps(
                {
                    "entrypoint": "template.tex",
                    "use_guidance": "Use the fixture class and style as presentation stock.",
                    "extensions": {
                        "latex": {
                            "composition_mode": "preamble",
                            "generated_entrypoint": "paper.tex",
                            "build_profile": "pdflatex",
                            "source_provenance": {"kind": "integration-fixture", "ref": "fixture:latex-template"},
                            "license_posture": "test-only",
                        }
                    },
                },
                indent=2,
            )
            + "\n",
        )
        status, latex_template = self.paper(
            "template",
            "create",
            "--kind",
            "latex",
            "--from",
            str(latex_tree),
            "--metadata-file",
            str(latex_metadata),
            "--actor",
            "agent:integration",
        )
        self.assertEqual(0, status, latex_template)

        status, markdown = self.paper(
            "derive-markdown",
            "--source-ref",
            refs["draft"],
            "--paper-line",
            "paper-main",
        )
        self.assertEqual(0, status, markdown)
        self.assertFalse(markdown["canonical"])

        status, explicit_initialized = self.paper(
            "init-tex",
            "--draft-ref",
            refs["draft"],
            "--content-template-ref",
            str(updated_template["stable_ref"]),
            "--latex-template-name",
            "main",
            "--paper-line",
            "paper-explicit-latex",
            "--citation-ref",
            refs["citation"],
        )
        self.assertEqual(0, status, explicit_initialized)
        self.assertEqual(latex_template["stable_ref"], explicit_initialized["latex_template"]["stable_ref"])

        status, initialized = self.paper(
            "init-tex",
            "--draft-ref",
            refs["draft"],
            "--content-template-ref",
            str(updated_template["stable_ref"]),
            "--paper-line",
            "paper-main",
            "--citation-ref",
            refs["citation"],
        )
        self.assertEqual(0, status, initialized)
        self.assertEqual("artifact-paper-template-latex-main", initialized["latex_template"]["stable_ref"])
        self.assertEqual("paper.tex", initialized["entrypoint"])
        self.assertFalse(initialized["build_ready"])
        self.assertTrue(initialized["agent_inspection_required"])
        status, composed_record = self.artifact("show", str(initialized["draft_ref"]))
        self.assertEqual(0, status, composed_record)
        composed_root = Path(str(composed_record["record"]["content_path"])).parent
        self.assertTrue((composed_root / "fixture.cls").is_file())
        self.assertTrue((composed_root / "surveyfixture.sty").is_file())
        composed_text = (composed_root / "paper.tex").read_text(encoding="utf-8")
        self.assertFalse(any(line.strip() == "---" for line in composed_text.splitlines()))
        self.assertIn("% ISOMER_FILL_TITLE: Evidence-Led Systems Survey", composed_text)
        self.assertNotIn("\\title{Survey Paper}", composed_text)
        self.assertNotIn("\\section{Title}", composed_text)
        self.assertNotIn("\\section{Abstract}", composed_text)
        fill_manifest = json.loads((composed_root / ".isomer-kaoju-tex-fill.json").read_text(encoding="utf-8"))
        self.assertEqual("isomer-kaoju-tex-fill.v1", fill_manifest["schema_version"])
        self.assertEqual("Evidence-Led Systems Survey", fill_manifest["frontmatter"]["title"])
        self.assertEqual("This survey summarizes accepted evidence {cite}`paper-one`.", fill_manifest["abstract"])
        obligations = {item["id"]: item for item in fill_manifest["obligations"]}
        self.assertEqual({"title", "authors", "abstract", "keywords", "bibliography"}, set(obligations))
        self.assertEqual("paper-one", obligations["bibliography"]["entries"][0]["cite_key"])
        status, initialized_again = self.paper(
            "init-tex",
            "--draft-ref",
            refs["draft"],
            "--content-template-ref",
            str(updated_template["stable_ref"]),
            "--paper-line",
            "paper-main",
            "--citation-ref",
            refs["citation"],
        )
        self.assertEqual(0, status, initialized_again)
        self.assertTrue(initialized_again["template_reused"])

        status, content_baseline = self.paper(
            "init-tex",
            "--draft-ref",
            refs["draft"],
            "--content-template-ref",
            str(updated_template["stable_ref"]),
            "--paper-line",
            "paper-content-drift",
            "--citation-ref",
            refs["citation"],
        )
        self.assertEqual(0, status, content_baseline)
        self.assertFalse(content_baseline["template_reused"])
        revised_content = self.root / "inputs/content-template-revised"
        shutil.copytree(candidate, revised_content)
        with (revised_content / "myst.yml").open("a", encoding="utf-8") as handle:
            handle.write("# content-only revision\n")
        status, revised_content_stock = self.paper(
            "template",
            "update",
            "--kind",
            "content",
            "--from",
            str(revised_content),
            "--expected-state",
            str(updated_template["state_token"]),
            "--actor",
            "agent:integration",
        )
        self.assertEqual(0, status, revised_content_stock)
        status, content_stale = self.paper("tex-status", "--draft-tex-ref", str(content_baseline["draft_ref"]))
        self.assertEqual(0, status, content_stale)
        self.assertEqual("content-stale", content_stale["content_template_posture"])
        self.assertEqual("current", content_stale["stocked_template_posture"])
        status, content_recomposed = self.paper(
            "init-tex",
            "--draft-ref",
            refs["draft"],
            "--content-template-ref",
            str(revised_content_stock["stable_ref"]),
            "--paper-line",
            "paper-content-drift",
            "--citation-ref",
            refs["citation"],
        )
        self.assertEqual(0, status, content_recomposed)
        self.assertTrue(content_recomposed["template_reused"])
        self.assertEqual(content_baseline["template_ref"], content_recomposed["template_ref"])
        self.assertEqual(content_baseline["compatibility_fingerprint"], content_recomposed["compatibility_fingerprint"])
        self.assertEqual(content_baseline["latex_template"]["state_token"], content_recomposed["latex_template"]["state_token"])

        status, mismatch = self.paper(
            "build-pdf",
            "--draft-tex-ref",
            str(initialized_again["draft_ref"]),
            "--template-tex-ref",
            "artifact-unrelated-template",
            "--paper-line",
            "paper-main",
            "--audit-ref",
            refs["audit"],
            "--inspected",
        )
        self.assertEqual(1, status)
        self.assertEqual("paper_template_ref_mismatch", mismatch["error"]["code"])

        status, unfilled = self.paper(
            "build-pdf",
            "--draft-tex-ref",
            str(initialized_again["draft_ref"]),
            "--paper-line",
            "paper-main",
            "--audit-ref",
            refs["audit"],
            "--inspected",
        )
        self.assertEqual(1, status)
        self.assertEqual("paper_tex_unfilled_obligations", unfilled["error"]["code"])

        status, unfilled_status = self.paper("tex-status", "--draft-tex-ref", str(initialized_again["draft_ref"]))
        self.assertEqual(0, status, unfilled_status)
        unfilled_codes = {item["code"] for item in unfilled_status["diagnostics"]}
        self.assertIn("tex_unfilled_marker", unfilled_codes)
        self.assertIn("tex_unfilled_title", unfilled_codes)
        self.assertIn("tex_unfilled_bibliography", unfilled_codes)

        revised_latex = self.root / "inputs/latex-template-revised"
        write(revised_latex / "template.tex", "\\documentclass{fixture}\n\\usepackage{surveyfixture}\n% revised stock\n")
        write(revised_latex / "fixture.cls", (latex_tree / "fixture.cls").read_text(encoding="utf-8"))
        write(revised_latex / "surveyfixture.sty", (latex_tree / "surveyfixture.sty").read_text(encoding="utf-8"))
        status, revised_stock = self.paper(
            "template",
            "update",
            "--kind",
            "latex",
            "--from",
            str(revised_latex),
            "--expected-state",
            str(latex_template["state_token"]),
            "--actor",
            "agent:integration",
        )
        self.assertEqual(0, status, revised_stock)
        status, stale_status = self.paper("tex-status", "--draft-tex-ref", str(initialized_again["draft_ref"]))
        self.assertEqual(0, status, stale_status)
        self.assertEqual("presentation-stale", stale_status["stocked_template_posture"])
        self.assertFalse(stale_status["paper_local_repair"])

        repaired_tree = self.root / "actor/repaired-tex-draft"
        shutil.copytree(composed_root, repaired_tree, ignore=shutil.ignore_patterns(".isomer-artifact-manifest.json"))
        repaired_entrypoint = repaired_tree / "paper.tex"
        filled_text = "\n".join(
            line for line in repaired_entrypoint.read_text(encoding="utf-8").splitlines() if not line.startswith("% ISOMER_FILL")
        )
        filled_text = filled_text.replace("\\title{}", "\\title{Evidence-Led Systems Survey}").replace("\\author{}", "\\author{Integration Agent}")
        filled_text = filled_text.replace(
            "\\end{document}",
            "\\begin{thebibliography}{9}\n\\bibitem{paper-one} Paper One, arXiv:0000.00001.\n\\end{thebibliography}\n\\end{document}",
        )
        repaired_entrypoint.write_text(filled_text + "% paper-local inspected repair\n", encoding="utf-8")
        status, repaired = self.artifact(
            "revise",
            str(initialized_again["draft_ref"]),
            str(repaired_tree),
            "--producer",
            "isomer-kaoju-write",
            "--scope-key",
            "paper-main",
            "--relationships-json",
            json.dumps(
                [
                    {"role": "paper_draft_myst", "target_ref": refs["draft"]},
                    {"role": "paper_template_tex", "target_ref": initialized_again["template_ref"]},
                ]
            ),
        )
        self.assertEqual(0, status, repaired)
        repaired_ref = str(repaired["record"]["id"])
        status, repaired_status = self.paper("tex-status", "--draft-tex-ref", repaired_ref)
        self.assertEqual(0, status, repaired_status)
        self.assertTrue(repaired_status["paper_local_repair"])

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
        write(compiler, "#!/bin/sh\ntest -f fixture.cls || exit 7\ntest -f surveyfixture.sty || exit 8\nprintf '%s\\n' '%PDF-1.4' '1 0 obj' '<<>>' 'endobj' '%%EOF' > paper.pdf\n")
        compiler.chmod(0o755)
        self.path = str(fake_bin)
        status, gated = self.paper(
            "build-pdf",
            "--draft-tex-ref",
            repaired_ref,
            "--template-tex-ref",
            str(initialized_again["template_ref"]),
            "--paper-line",
            "paper-main",
            "--audit-ref",
            refs["audit"],
            "--inspected",
        )
        self.assertEqual(0, status, gated)
        self.assertIsNone(gated["fallback"])
        self.assertFalse(gated["accepted"])
        self.assertEqual("required", gated["pdf_inspection"])
        status, revision_record = self.artifact("show", str(gated["revision_log_ref"]))
        self.assertEqual(0, status, revision_record)
        revision_path = Path(str(revision_record["record"]["content_path"]))
        revision_payload = json.loads(revision_path.read_text(encoding="utf-8"))
        self.assertEqual("paper-local", revision_payload["sections"]["builds"][0]["repair_class"])

        status, accepted = self.paper(
            "build-pdf",
            "--draft-tex-ref",
            repaired_ref,
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
