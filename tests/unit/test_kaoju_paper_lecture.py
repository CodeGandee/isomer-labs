from __future__ import annotations

from copy import deepcopy
import unittest

import yaml  # type: ignore[import-untyped]

from isomer_labs.kaoju.paper import LECTURE_SECTION_COMPONENTS, validate_lecture_sections


def diagnostic_codes(diagnostics: list[object]) -> set[str]:
    return {str(getattr(diagnostic, "code")) for diagnostic in diagnostics}


class KaojuPaperLectureValidationTests(unittest.TestCase):
    def fixture(self) -> tuple[str, dict[str, object], dict[str, object]]:
        commitment = {
            "paper_identity": {"stable_id": "paper:lecture-v1", "version_family": "v1"},
            "run_ref": "run-lecture-1",
            "source_digest_ref": "source-digest-lecture-1",
            "posture": "active",
            "readiness": "lecture-ready",
            "section_job": {
                "kind": "dedicated-detailed-section",
                "title": "Lecture Paper Method",
                "reader_outcome": "The reader can explain the method without consulting the paper.",
            },
            "equation_jobs": [{"locator": "page 4, equation 2"}],
            "display_jobs": [{"locator": "page 6, figure 2", "handling_posture": "redraw"}],
            "blockers": [],
            "evidence_refs": ["source-digest-lecture-1"],
        }
        field_summary = {
            "sections": {
                "synthesis": {"conclusions": [{"text": "The method uses a constrained transformation."}]},
                "lecture_commitment_basis": [
                    {
                        "paper_identity": commitment["paper_identity"],
                        "run_ref": commitment["run_ref"],
                        "source_digest_ref": commitment["source_digest_ref"],
                    }
                ],
                "lecture_section_commitments": [commitment],
            }
        }
        components = {
            name: {
                "status": "covered",
                "myst_locator": "Lecture coverage marker",
                "citation_map_refs": ["claim-method"],
            }
            for name in LECTURE_SECTION_COMPONENTS
        }
        lecture_section = {
            "run_ref": "run-lecture-1",
            "source_digest_ref": "source-digest-lecture-1",
            "heading": "Lecture Paper Method",
            "section_job_kind": "dedicated-detailed-section",
            "reader_outcome": "The reader can explain the method without consulting the paper.",
            "evidence_refs": ["source-digest-lecture-1"],
            "claim_refs": ["claim-method"],
            "components": components,
            "equation_jobs": [
                {
                    "source_locator": "page 4, equation 2",
                    "status": "covered",
                    "myst_locator": "Equation coverage marker",
                    "symbols": [
                        {"symbol": "x", "meaning": "input"},
                        {"symbol": "T", "meaning": "transformation"},
                    ],
                    "citation_map_refs": ["equation-method"],
                }
            ],
            "display_jobs": [
                {
                    "source_locator": "page 6, figure 2",
                    "status": "covered",
                    "handling_posture": "redraw",
                    "artifact_ref": "paper-display-1",
                    "citation_map_refs": ["display-method"],
                }
            ],
        }
        frontmatter = yaml.safe_dump({"lecture_sections": [lecture_section]}, sort_keys=False)
        text = (
            f"---\n{frontmatter}---\n\n"
            "# Survey\n\n"
            "## Lecture Paper Method\n\n"
            "Lecture coverage marker.\n\n"
            "Equation coverage marker: $T(x)$ maps the input, where $x$ is the input and $T$ is the transformation.\n\n"
            "{{figure:paper-display-1}}\n"
        )
        citation_map = {
            "sections": {
                "citations": {
                    "paper-one": {
                        "cite_key": "paper-one",
                        "source_digest_ref": "source-digest-lecture-1",
                    }
                },
                "claims": {
                    "claim-method": {
                        "claim_id": "claim-method",
                        "evidence_refs": ["source-digest-lecture-1"],
                    }
                },
                "equations": {
                    "equation-method": {
                        "equation_id": "equation-method",
                        "source_digest_ref": "source-digest-lecture-1",
                        "source_locator": "page 4, equation 2",
                    }
                },
                "displays": {
                    "display-method": {
                        "display_id": "display-method",
                        "artifact_ref": "paper-display-1",
                        "evidence_refs": ["source-digest-lecture-1"],
                        "source_locator": "page 6, figure 2",
                        "teaching_role": "Show the method data flow.",
                        "transformation_posture": "redraw",
                        "attribution": "Adapted from Paper One, Figure 2.",
                        "insertion_locator": "Lecture Paper Method",
                    }
                },
            }
        }
        return text, field_summary, citation_map

    def test_accepts_complete_active_lecture_section(self) -> None:
        text, field_summary, citation_map = self.fixture()

        self.assertEqual([], validate_lecture_sections(text, field_summary=field_summary, citation_map=citation_map))

    def test_accepts_evidence_backed_not_applicable_media_without_fixed_counts(self) -> None:
        text, field_summary, citation_map = self.fixture()
        commitment = field_summary["sections"]["lecture_section_commitments"][0]  # type: ignore[index]
        commitment["equation_jobs"] = []  # type: ignore[index]
        commitment["display_jobs"] = []  # type: ignore[index]
        frontmatter = yaml.safe_load(text.split("---", 2)[1])
        section = frontmatter["lecture_sections"][0]
        section["equation_jobs"] = []
        section["display_jobs"] = []
        for name in ("worked_trace", "equations", "displays"):
            section["components"][name] = {
                "status": "not-applicable",
                "rationale": f"Accepted evidence establishes no necessary {name}.",
                "citation_map_refs": ["claim-method"],
            }
        body = text.split("---", 2)[2]
        text = f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---{body}"

        self.assertEqual([], validate_lecture_sections(text, field_summary=field_summary, citation_map=citation_map))

    def test_rejects_missing_display_artifact_and_equation_symbols(self) -> None:
        text, field_summary, citation_map = self.fixture()
        text = text.replace("{{figure:paper-display-1}}", "")
        frontmatter = yaml.safe_load(text.split("---", 2)[1])
        frontmatter["lecture_sections"][0]["equation_jobs"][0]["symbols"] = []
        body = text.split("---", 2)[2]
        text = f"---\n{yaml.safe_dump(frontmatter, sort_keys=False)}---{body}"

        codes = diagnostic_codes(validate_lecture_sections(text, field_summary=field_summary, citation_map=citation_map))

        self.assertIn("lecture_display_placeholder_missing", codes)
        self.assertIn("lecture_equation_symbols_missing", codes)

    def test_rejects_blocked_commitment_and_unknown_citation_lineage(self) -> None:
        text, field_summary, citation_map = self.fixture()
        blocked = deepcopy(field_summary)
        commitment = blocked["sections"]["lecture_section_commitments"][0]  # type: ignore[index]
        commitment["posture"] = "blocked"  # type: ignore[index]
        commitment["readiness"] = "blocked"  # type: ignore[index]
        commitment["blockers"] = ["Equation context is inaccessible."]  # type: ignore[index]
        self.assertIn(
            "lecture_commitment_blocked",
            diagnostic_codes(validate_lecture_sections(text, field_summary=blocked, citation_map=citation_map)),
        )

        unresolved = deepcopy(citation_map)
        unresolved["sections"]["claims"] = {}  # type: ignore[index]
        self.assertIn(
            "lecture_citation_ref_unknown",
            diagnostic_codes(validate_lecture_sections(text, field_summary=field_summary, citation_map=unresolved)),
        )

    def test_explicit_supersession_removes_section_obligation_but_preserves_exact_reconciliation(self) -> None:
        text, field_summary, citation_map = self.fixture()
        superseded = deepcopy(field_summary)
        commitment = superseded["sections"]["lecture_section_commitments"][0]  # type: ignore[index]
        commitment["posture"] = "superseded"  # type: ignore[index]
        commitment["supersession"] = {  # type: ignore[index]
            "prior_run_ref": "run-lecture-1",
            "replacement_posture": "related-work-mention",
            "rationale": "The accepted survey scope changed.",
            "actor_ref": "topic-actor:researcher",
            "provenance_refs": ["decision:scope-change"],
        }
        plain_text = "# Survey\n\n## Related Work\n\nThe method remains cited.\n"

        self.assertEqual([], validate_lecture_sections(plain_text, field_summary=superseded, citation_map=citation_map))
        self.assertIn(
            "lecture_section_unbound",
            diagnostic_codes(validate_lecture_sections(text, field_summary=superseded, citation_map=citation_map)),
        )


if __name__ == "__main__":
    unittest.main()
