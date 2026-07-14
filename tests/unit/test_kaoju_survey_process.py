from __future__ import annotations

import re
from pathlib import Path
import unittest

from isomer_labs.artifact_formats.research_record_formats import ResearchRecordFormatProvider
from isomer_labs.kaoju.contracts import load_binding_registry, resolve_semantic_id
from isomer_labs.kaoju.survey import (
    choose_environment_strategy,
    classify_trial_retry,
    direction_set_diagnostics,
    reading_list_diagnostics,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
USE_CASE_ROOT = REPO_ROOT / "context/features/2026-07-14-kaoju-survey-process-usecases/usecases"


def codes(diagnostics: object) -> set[str]:
    return {diagnostic.code for diagnostic in diagnostics}  # type: ignore[union-attr]


class KaojuSurveyProcessTests(unittest.TestCase):
    def test_every_use_case_semantic_id_resolves_through_binding_or_adr_alias(self) -> None:
        semantic_ids: set[str] = set()
        for path in sorted(USE_CASE_ROOT.glob("uc-*.md")):
            semantic_ids.update(re.findall(r"kaoju:[a-z0-9]+(?:-[a-z0-9]+)*", path.read_text(encoding="utf-8")))
        bindings = load_binding_registry()
        profiles = ResearchRecordFormatProvider()
        self.assertGreaterEqual(len(semantic_ids), 40)
        for named_id in sorted(semantic_ids):
            with self.subTest(semantic_id=named_id):
                canonical_id, alias = resolve_semantic_id(named_id)
                binding = bindings.get(canonical_id)
                self.assertIsNotNone(binding, f"{named_id} resolved to unbound {canonical_id}")
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
                if alias is not None:
                    self.assertFalse(alias["automatic_promotion"])
                    self.assertEqual("adr-0006-diagram-alias", alias["disposition"])

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
