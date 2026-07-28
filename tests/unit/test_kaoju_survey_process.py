from __future__ import annotations

from copy import deepcopy
import re
from pathlib import Path
import unittest

from isomer_labs.artifact_formats.research_record_formats import ResearchRecordFormatProvider
from isomer_labs.kaoju.contracts import load_binding_registry
from isomer_labs.kaoju.survey import (
    choose_environment_strategy,
    classify_trial_retry,
    direction_set_diagnostics,
    field_summary_diagnostics,
    reading_list_diagnostics,
    source_digest_diagnostics,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
USE_CASE_ROOT = REPO_ROOT / "context/features/2026-07-14-kaoju-survey-process-usecases/usecases"


def codes(diagnostics: object) -> set[str]:
    return {diagnostic.code for diagnostic in diagnostics}  # type: ignore[union-attr]


def reading_items(priority_count: int, secondary_count: int) -> list[dict[str, object]]:
    source_types = ("paper", "technical_report", "framework_doc", "repository", "dataset", "model")
    items: list[dict[str, object]] = []
    for category, count in (("priority", priority_count), ("secondary", secondary_count)):
        for _ in range(count):
            index = len(items) + 1
            source_type = source_types[(index - 1) % len(source_types)]
            items.append(
                {
                    "item_id": f"item-{index}",
                    "title": f"Source {index}",
                    "source_type": source_type,
                    "urls": [f"https://example.test/{index}"],
                    "summary": "Relevant source.",
                    "relevance_rationale": "Addresses the selected direction.",
                    "estimated_depth": "full-text" if source_type in {"paper", "technical_report"} else "code-level",
                    "query_provenance": {"query": "bounded query", "provider": "provider", "route": "online-search", "searched_through": "2026-07-17"},
                    "status": "planned",
                    "priority": category,
                    "version_family": f"family-{index}",
                }
            )
    return items


class KaojuSurveyProcessTests(unittest.TestCase):
    def lecture_source_digest(self) -> dict[str, object]:
        return {
            "sections": {
                "source_identity": {"source_class": "paper", "title": "Lecture Paper", "version_family": "v1"},
                "findings": [
                    {
                        "claim": "The method follows an ordered transformation.",
                        "source_class": "paper",
                        "locator": "page 4, section 3",
                        "source_statement": "The paper defines the transformation.",
                        "interpretation": "The transformation is the method's central teaching sequence.",
                    }
                ],
                "method": {"inspection_depth": "lecture", "mindset_key": "paper.lecture"},
                "lecture_exposition": {
                    "mindset_resolution": {
                        "run_ref": "run-lecture-1",
                        "mindset_key": "paper.lecture",
                        "disposition": "recorded",
                        "record_ref": "mindset-record-lecture-1",
                    },
                    "section_role": "Teach the paper's method as a dedicated survey section.",
                    "reader_outcome": "The reader can explain the method's inputs, transformation, and output.",
                    "prerequisites": ["Basic optimization notation"],
                    "problem_setting": "Transform input x into output y under constraint C.",
                    "definitions": [{"term": "constraint C", "meaning": "The feasible transformation boundary."}],
                    "symbol_glossary": [{"symbol": "x", "meaning": "Input"}],
                    "method_intuition": "The method isolates the constrained transformation.",
                    "method_walkthrough": ["Read x.", "Apply the constrained transformation.", "Return y."],
                    "worked_trace": {"locator": "page 5, example 1", "summary": "Trace one input through the method."},
                    "equations": [
                        {
                            "locator": "page 4, equation 2",
                            "teaching_role": "Defines the constrained transformation.",
                            "source_context": "Section 3 introduces the objective and constraint.",
                            "interpretation": "The objective selects y for input x.",
                            "planned_treatment": "derive",
                            "evidence_refs": ["evidence-equation-2"],
                            "symbols": [
                                {"symbol": "x", "meaning": "Input"},
                                {"symbol": "y", "meaning": "Output"},
                            ],
                        }
                    ],
                    "displays": [
                        {
                            "kind": "figure",
                            "locator": "page 6, figure 2",
                            "teaching_role": "Shows the ordered method stages.",
                            "source_context": "Caption and surrounding section describe every stage.",
                            "interpretation": "The arrows define the method flow.",
                            "handling_posture": "redraw",
                            "attribution": "Adapted from Lecture Paper, Figure 2.",
                            "evidence_refs": ["evidence-figure-2"],
                            "provenance_refs": ["source:lecture-paper-v1"],
                            "handling_evidence": {
                                "license": "unknown",
                                "permission": "not-required-for-redraw-assessment-pending",
                                "blockers": [],
                            },
                        }
                    ],
                    "results": [{"locator": "page 8, table 1", "summary": "Reported evaluation result."}],
                    "comparisons": [{"work_ref": "paper:baseline", "summary": "Uses a different constraint."}],
                    "limitations": ["The reported evaluation covers one workload."],
                    "evidence_refs": ["evidence-equation-2", "evidence-figure-2"],
                    "proposed_section_outline": ["Problem and notation", "Method walkthrough", "Evidence and limitations"],
                    "not_applicable": {"tables": "No table is necessary for method comprehension."},
                    "status": "lecture-ready",
                    "blockers": [],
                },
                "approval": {"status": "approved", "actor_ref": "topic-actor:researcher"},
            }
        }

    def test_every_use_case_uses_an_exact_registered_semantic_id(self) -> None:
        semantic_ids: set[str] = set()
        for path in sorted(USE_CASE_ROOT.glob("uc-*.md")):
            semantic_ids.update(re.findall(r"KAOJU:[A-Z0-9]+(?:-[A-Z0-9]+)*", path.read_text(encoding="utf-8")))
        bindings = load_binding_registry()
        profiles = ResearchRecordFormatProvider()
        self.assertGreaterEqual(len(semantic_ids), 35)
        for named_id in sorted(semantic_ids):
            with self.subTest(semantic_id=named_id):
                binding = bindings.get(named_id)
                self.assertIsNotNone(binding, f"{named_id} is not registered")
                assert binding is not None
                self.assertTrue(binding.producer)
                self.assertTrue(binding.consumers)
                self.assertIn(
                    binding.content_mode,
                    {"structured_file", "ordinary_file", "directory_manifest", "external_path", "canonical_repository"},
                )
                if binding.content_mode == "structured_file":
                    self.assertIsNotNone(binding.profile_ref)
                    self.assertIsNotNone(profiles.resolve_profile(str(binding.profile_ref)))

    def test_direction_set_accepts_multiple_and_custom_actor_confirmed_directions(self) -> None:
        proposals = []
        for identifier, title, feasibility in (
            ("a", "Mechanism survey", "available"),
            ("b", "Implementation lineage", "requires-environment-work"),
            ("custom-bandwidth", "Bandwidth assumptions", "requires-unavailable-hardware-or-service"),
        ):
            proposals.append(
                {
                    "id": identifier,
                    "title": title,
                    "research_question": f"What evidence supports {title}?",
                    "boundary": "Primary evidence through 2026-07-14",
                    "source_classes": ["paper", "technical_report", "repository"],
                    "coverage_date": "2026-07-14",
                    "expected_depth": "full-text",
                    "deliverables": ["reading-list", "source-digest"],
                    "empirical_feasibility": feasibility,
                }
            )
        payload = {
            "sections": {
                "proposals": proposals,
                "selections": ["b", "custom-bandwidth"],
                "confirmation": {"status": "accepted", "actor_ref": "topic-actor:researcher"},
            }
        }
        self.assertEqual([], direction_set_diagnostics(payload))

        payload["sections"]["confirmation"] = {"status": "draft"}  # type: ignore[index]
        self.assertIn("direction_confirmation_missing", codes(direction_set_diagnostics(payload)))

    def test_lecture_source_digest_requires_complete_exposition_and_supports_blocked_missing_record(self) -> None:
        ready = self.lecture_source_digest()
        self.assertEqual([], source_digest_diagnostics(ready))

        blocked = deepcopy(ready)
        lecture = blocked["sections"]["lecture_exposition"]  # type: ignore[index]
        lecture["mindset_resolution"] = {  # type: ignore[index]
            "run_ref": "run-lecture-missing-source",
            "mindset_key": "paper.lecture",
            "disposition": "skipped_source_missing",
        }
        lecture["status"] = "blocked"  # type: ignore[index]
        lecture["blockers"] = ["Table values remain inaccessible."]  # type: ignore[index]
        self.assertEqual([], source_digest_diagnostics(blocked))

        missing = deepcopy(ready)
        missing["sections"].pop("lecture_exposition")  # type: ignore[union-attr]
        self.assertIn("lecture_exposition_missing", codes(source_digest_diagnostics(missing)))

        invalid_posture = deepcopy(ready)
        invalid_posture["sections"]["lecture_exposition"]["displays"][0]["handling_posture"] = "copy"  # type: ignore[index]
        self.assertIn("lecture_display_posture_invalid", codes(source_digest_diagnostics(invalid_posture)))

        ordinary = {
            "sections": {
                "source_identity": {"source_class": "paper", "title": "Ordinary Paper", "version_family": "v1"},
                "findings": [{"locator": "page 1", "source_statement": "Statement.", "interpretation": "Interpretation."}],
                "method": {"inspection_depth": "full-text"},
                "approval": {"status": "pending"},
            }
        }
        self.assertEqual([], source_digest_diagnostics(ordinary))

    def test_field_summary_preserves_lecture_commitments_and_requires_explicit_supersession(self) -> None:
        identity = {"stable_id": "paper:lecture-v1", "version_family": "v1"}
        basis = {"paper_identity": identity, "run_ref": "run-lecture-1", "source_digest_ref": "source-digest-lecture-1"}
        commitment = {
            **basis,
            "posture": "active",
            "readiness": "lecture-ready",
            "section_job": {
                "kind": "dedicated-detailed-section",
                "title": "Lecture Paper Method",
                "reader_outcome": "The reader can explain the method without consulting the original paper.",
            },
            "equation_jobs": [{"locator": "page 4, equation 2"}],
            "display_jobs": [{"locator": "page 6, figure 2", "handling_posture": "redraw"}],
            "blockers": [],
            "evidence_refs": ["source-digest-lecture-1"],
        }
        payload = {
            "sections": {
                "synthesis": {"conclusions": [{"text": "The method uses a constrained transformation."}]},
                "lecture_commitment_basis": [basis],
                "lecture_section_commitments": [commitment],
            }
        }
        self.assertEqual([], field_summary_diagnostics(payload))

        omitted = deepcopy(payload)
        omitted["sections"]["lecture_section_commitments"] = []  # type: ignore[index]
        self.assertIn("lecture_commitment_omitted", codes(field_summary_diagnostics(omitted)))

        shortened = deepcopy(payload)
        shortened["sections"]["lecture_section_commitments"][0]["section_job"]["kind"] = "related-work-mention"  # type: ignore[index]
        self.assertIn("lecture_section_job_invalid", codes(field_summary_diagnostics(shortened)))

        implicit_supersession = deepcopy(payload)
        row = implicit_supersession["sections"]["lecture_section_commitments"][0]  # type: ignore[index]
        row["posture"] = "superseded"  # type: ignore[index]
        row["supersession"] = {  # type: ignore[index]
            "prior_run_ref": "run-deep-dive-2",
            "replacement_posture": "related-work-mention",
            "rationale": "A later shorter reading exists.",
            "actor_ref": "topic-actor:researcher",
            "provenance_refs": ["decision:shorten"],
        }
        self.assertIn("lecture_supersession_target_mismatch", codes(field_summary_diagnostics(implicit_supersession)))

        explicit_supersession = deepcopy(implicit_supersession)
        explicit_supersession["sections"]["lecture_section_commitments"][0]["supersession"]["prior_run_ref"] = "run-lecture-1"  # type: ignore[index]
        self.assertEqual([], field_summary_diagnostics(explicit_supersession))

    def test_reading_list_is_independently_scoped_and_shortage_is_only_a_warning(self) -> None:
        items = []
        for index, source_type in enumerate(("paper", "technical_report", "framework_doc", "repository"), start=1):
            items.append(
                {
                    "item_id": f"item-{index}",
                    "title": f"Source {index}",
                    "source_type": source_type,
                    "urls": [f"https://example.test/{index}"],
                    "summary": "Relevant source.",
                    "relevance_rationale": "Addresses the selected direction.",
                    "estimated_depth": "full-text" if source_type in {"paper", "technical_report"} else "code-level",
                    "query_provenance": {"query": "bounded query", "provider": "provider", "route": "online-search", "searched_through": "2026-07-14"},
                    "status": "planned",
                    "priority": "priority" if index <= 2 else "secondary",
                    "version_family": f"family-{index}",
                }
            )
        payload = {
            "sections": {
                "direction_id": "direction-b",
                "items": items,
                "approval": {"status": "approved", "actor_ref": "topic-actor:researcher"},
            }
        }
        diagnostics = reading_list_diagnostics(payload)
        self.assertEqual({"reading_target_short"}, codes(diagnostics))
        self.assertTrue(all(diagnostic.severity == "warning" for diagnostic in diagnostics))

        payload["sections"]["items"][0]["item_id"] = "item-2"  # type: ignore[index]
        self.assertIn("reading_item_duplicate", codes(reading_list_diagnostics(payload)))

    def test_reading_list_accepts_odd_and_even_user_total_targets(self) -> None:
        for total, priority_count, secondary_count in ((5, 3, 2), (6, 3, 3)):
            with self.subTest(total=total):
                payload = {
                    "sections": {
                        "direction_id": "direction-b",
                        "target_counts": {"basis": "user-total", "requested_total": total, "priority": priority_count, "secondary": secondary_count},
                        "achieved_counts": {"priority": priority_count, "secondary": secondary_count},
                        "items": reading_items(priority_count, secondary_count),
                        "approval": {"status": "pending"},
                    }
                }
                self.assertEqual([], reading_list_diagnostics(payload))

    def test_reading_list_accepts_category_and_zero_category_targets(self) -> None:
        for priority_count, secondary_count in ((5, 3), (0, 2)):
            with self.subTest(priority=priority_count, secondary=secondary_count):
                payload = {
                    "sections": {
                        "direction_id": "direction-b",
                        "target_counts": {"basis": "user-categories", "priority": priority_count, "secondary": secondary_count},
                        "achieved_counts": {"priority": priority_count, "secondary": secondary_count},
                        "items": reading_items(priority_count, secondary_count),
                        "approval": {"status": "pending"},
                    }
                }
                self.assertEqual([], reading_list_diagnostics(payload))

    def test_reading_list_shortage_uses_effective_target(self) -> None:
        payload = {
            "sections": {
                "direction_id": "direction-b",
                "target_counts": {"basis": "user-total", "requested_total": 5, "priority": 3, "secondary": 2},
                "achieved_counts": {"priority": 2, "secondary": 2},
                "items": reading_items(2, 2),
                "approval": {"status": "pending"},
            }
        }
        diagnostics = reading_list_diagnostics(payload)
        self.assertEqual(["reading_target_short"], [diagnostic.code for diagnostic in diagnostics])
        self.assertEqual("warning", diagnostics[0].severity)
        self.assertIn("effective target of 3", diagnostics[0].message)

    def test_reading_list_rejects_invalid_target_metadata(self) -> None:
        invalid_targets = (
            ({"basis": "unknown", "priority": 3, "secondary": 3}, "reading_target_basis_invalid"),
            ({"basis": "user-categories", "priority": True, "secondary": 3}, "reading_target_count_invalid"),
            ({"basis": "user-categories", "priority": -1, "secondary": 3}, "reading_target_count_invalid"),
            ({"basis": "user-categories", "priority": 1.5, "secondary": 3}, "reading_target_count_invalid"),
            ({"basis": "user-categories", "priority": 0, "secondary": 0}, "reading_target_empty"),
            ({"basis": "user-total", "requested_total": 0, "priority": 0, "secondary": 0}, "reading_requested_total_invalid"),
            ({"basis": "user-total", "requested_total": 2.5, "priority": 2, "secondary": 1}, "reading_requested_total_invalid"),
            ({"basis": "user-total", "requested_total": 5, "priority": 2, "secondary": 3}, "reading_target_total_mismatch"),
            ({"basis": "user-categories", "requested_total": 6, "priority": 3, "secondary": 3}, "reading_requested_total_unexpected"),
            ({"basis": "default", "priority": 4, "secondary": 2}, "reading_target_default_mismatch"),
        )
        for target_counts, expected_code in invalid_targets:
            with self.subTest(expected_code=expected_code):
                payload = {
                    "sections": {
                        "direction_id": "direction-b",
                        "target_counts": target_counts,
                        "achieved_counts": {"priority": 3, "secondary": 3},
                        "items": reading_items(3, 3),
                        "approval": {"status": "pending"},
                    }
                }
                self.assertIn(expected_code, codes(reading_list_diagnostics(payload)))

    def test_reading_list_requires_matching_achieved_counts_for_configurable_targets(self) -> None:
        payload = {
            "sections": {
                "direction_id": "direction-b",
                "target_counts": {"basis": "user-total", "requested_total": 5, "priority": 3, "secondary": 2},
                "achieved_counts": {"priority": 2, "secondary": 2},
                "items": reading_items(3, 2),
                "approval": {"status": "pending"},
            }
        }
        self.assertIn("reading_achieved_count_mismatch", codes(reading_list_diagnostics(payload)))

        del payload["sections"]["achieved_counts"]
        self.assertIn("reading_achieved_counts_missing", codes(reading_list_diagnostics(payload)))

    def test_environment_strategy_uses_reuse_add_default_then_create_order(self) -> None:
        requirements = ["torch", "datasets"]
        reused = choose_environment_strategy(requirements, [{"name": "default", "packages": requirements, "usable": True}])
        self.assertEqual("reuse", reused["strategy"])

        added = choose_environment_strategy(
            requirements,
            [
                {"name": "analysis", "packages": [], "usable": True, "can_add": True},
                {"name": "default", "packages": ["torch"], "usable": True, "can_add": True},
            ],
        )
        self.assertEqual({"strategy": "add", "environment": "default", "constraints": {"datasets": "*"}, "reason": "compatible additions to preferred existing environment"}, added)

        created = choose_environment_strategy(requirements, [{"name": "default", "packages": [], "usable": False}])
        self.assertEqual("create", created["strategy"])
        self.assertEqual({"datasets": "*", "torch": "*"}, created["constraints"])

    def test_retry_classifier_preserves_bound_and_requires_gate_for_material_change(self) -> None:
        baseline = {
            "source_commit": "a" * 40,
            "environment_lock": "sha256:lock",
            "data_identity": "dataset:v1",
            "wrapper_semantics": "upstream-command",
            "evaluator": "exact",
            "metrics": ["throughput"],
            "resource_limits": {"seconds": 60},
            "fidelity": "upstream-faithful",
            "interpretation_policy": "compare-compatible-only",
        }
        retry = classify_trial_retry(baseline, dict(baseline), failure_class="temporary_io", attempts_completed=1, attempt_bound=3)
        self.assertEqual("retry_identical", retry["decision"])
        self.assertFalse(retry["requires_gate"])

        changed = dict(baseline)
        changed["metrics"] = ["latency"]
        revision = classify_trial_retry(baseline, changed, failure_class="temporary_io", attempts_completed=1, attempt_bound=3)
        self.assertEqual("revise_plan", revision["decision"])
        self.assertEqual(["metrics"], revision["changed_fields"])
        self.assertTrue(revision["requires_gate"])

        exhausted = classify_trial_retry(baseline, dict(baseline), failure_class="temporary_io", attempts_completed=3, attempt_bound=3)
        self.assertEqual("blocked", exhausted["decision"])


if __name__ == "__main__":
    unittest.main()
