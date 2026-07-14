from __future__ import annotations

from dataclasses import asdict
from importlib.resources import files
import json
import unittest

from isomer_labs.artifact_formats.research_record_formats import ResearchRecordFormatProvider
from isomer_labs.kaoju.contracts import load_binding_registry, load_contract, validate_binding_registry_document


class KaojuContractTests(unittest.TestCase):
    def test_checked_inventory_and_binding_registry_are_complete(self) -> None:
        contract = load_contract()
        self.assertEqual(14, len(contract.skills))
        self.assertEqual(10, len(contract.survey_intents))
        self.assertEqual("isomer-kaoju-pipeline", contract.skills[0])
        self.assertEqual(
            {"manage-survey", "manage-dataset", "manage-paper-template"},
            set(contract.manager_actions),
        )
        bindings = load_binding_registry()
        required = {
            "kaoju:direction-set",
            "kaoju:reading-list",
            "kaoju:artifact-library",
            "kaoju:associated-source-code",
            "kaoju:paper-structure-myst",
            "kaoju:paper-draft-myst",
            "kaoju:paper-display",
            "kaoju:paper-pdf",
            "kaoju:llm-wiki-export",
            "kaoju:llm-wiki-viewer-manifest",
            "kaoju:env-prep-plan",
            "kaoju:smoke-run-script",
            "kaoju:method-trial-plan",
            "kaoju:method-trial-wrapper",
            "kaoju:method-trial-result",
        }
        self.assertLessEqual(required, set(bindings))
        self.assertEqual(len(bindings), len(set(bindings)))

    def test_structured_bindings_resolve_and_non_structured_bindings_are_explicit(self) -> None:
        provider = ResearchRecordFormatProvider()
        for binding in load_binding_registry().values():
            with self.subTest(semantic_id=binding.semantic_id):
                if binding.content_mode == "structured_file":
                    self.assertIsNotNone(binding.profile_ref)
                    self.assertIsNotNone(provider.resolve_profile(str(binding.profile_ref)))
                elif binding.profile_ref is not None:
                    self.assertIsNotNone(provider.resolve_profile(binding.profile_ref))
                self.assertNotIn("subpath", asdict(binding))
                self.assertNotIn("path_template", asdict(binding))

    def test_invalid_registry_fixture_has_deterministic_diagnostics(self) -> None:
        resource = files("isomer_labs").joinpath(
            "assets/system_skills/research-paradigm/kaoju/contracts/bindings.v2.json"
        )
        raw = json.loads(resource.read_text(encoding="utf-8"))
        raw["bindings"][1]["semantic_id"] = raw["bindings"][0]["semantic_id"]
        raw["bindings"][2]["content_mode"] = "directory_scan"
        diagnostics = validate_binding_registry_document(raw)
        self.assertTrue(any("duplicate kaoju:workspace-readiness" in item for item in diagnostics))
        self.assertTrue(any("directory_scan" in item for item in diagnostics))

    def test_supersession_and_dependency_decisions_are_locked(self) -> None:
        raw = load_contract().raw
        self.assertEqual("add-kaoju-paper-writing", raw["supersession"]["source_change"])
        self.assertIn("LaTeX source is canonical paper state", raw["supersession"]["replaced_requirements"])
        decisions = raw["implementation_decisions"]
        self.assertEqual("5.1.0", decisions["myst_parser"]["locked_selection"])
        self.assertEqual("independent-compatible-implementation", decisions["wiki_viewer"]["decision"])


if __name__ == "__main__":
    unittest.main()
