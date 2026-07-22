from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict
from importlib.resources import files
import json
import unittest

from isomer_labs.core.artifact_identity import ArtifactIdentityError
from isomer_labs.artifact_formats.research_record_formats import ResearchRecordFormatProvider
from isomer_labs.kaoju.contracts import (
    describe_binding,
    load_binding_registry,
    load_contract,
    load_semantic_registry,
    resource_coverage_diagnostics,
    validate_binding_registry_document,
    validate_semantic_registry_document,
)


class KaojuContractTests(unittest.TestCase):
    def resource_json(self, name: str) -> dict[str, object]:
        resource = files("isomer_labs.kaoju").joinpath("resources", name)
        self.assertTrue(resource.is_file(), name)
        value = json.loads(resource.read_text(encoding="utf-8"))
        assert isinstance(value, dict)
        return value

    def test_checked_process_semantics_and_bindings_are_complete(self) -> None:
        contract = load_contract()
        self.assertEqual(16, len(contract.skills))
        self.assertEqual(11, len(contract.survey_intents))
        self.assertEqual(("explore",), contract.exploration_procedures)
        self.assertEqual("isomer-ext-kaoju-entrypoint", contract.entry_skill)
        self.assertEqual("isomer-ext-kaoju-entrypoint", contract.skills[0])
        self.assertEqual(15, len(contract.protected_members))
        self.assertEqual(tuple(contract.skills[1:]), tuple(item.logical_id for item in contract.protected_members))
        self.assertEqual(
            "isomer-ext-kaoju-entrypoint->trial",
            next(item.invocation_designator for item in contract.protected_members if item.logical_id == "isomer-kaoju-trial"),
        )
        self.assertEqual(
            {
                "list": "isomer-cli --print-json ext kaoju bindings list",
                "describe": "isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT",
            },
            contract.binding_queries,
        )
        self.assertNotIn("semantic_aliases", contract.raw)
        self.assertNotIn("binding_registry_resource", contract.raw)
        self.assertEqual("record-or-skip-missing-per-run", contract.raw["mindsets"]["resolution_mode"])
        self.assertNotIn("ensure_mode", contract.raw["mindsets"])

        bindings = load_binding_registry()
        semantics = load_semantic_registry()
        self.assertEqual(64, len(bindings))
        self.assertEqual(set(bindings), set(semantics))
        self.assertEqual((), resource_coverage_diagnostics())
        for semantic_id in bindings:
            self.assertRegex(semantic_id, r"^KAOJU:[A-Z0-9]+(?:-[A-Z0-9]+)*$")
            semantic = semantics[semantic_id]
            self.assertTrue(semantic.meaning)
            self.assertTrue(semantic.minimum_content)
            self.assertEqual(bindings[semantic_id].producer, semantic.producer)
            self.assertEqual(bindings[semantic_id].consumers, semantic.consumers)

    def test_joined_descriptions_preserve_exact_identity_and_binding_fields(self) -> None:
        description = describe_binding("KAOJU:SURVEY-CONTRACT")
        self.assertEqual("KAOJU:SURVEY-CONTRACT", description["semantic_id"])
        self.assertEqual("isomer-kaoju-frame", description["producer"])
        self.assertEqual("artifact", description["record_kind"])
        self.assertEqual("current_state", description["revision_mode"])
        self.assertIn("accepted question", description["meaning"])
        self.assertTrue(description["minimum_content"])
        self.assertTrue(description["update_intent"])

        for invalid in (
            "kaoju:survey-contract",
            "Kaoju:SURVEY-CONTRACT",
            "KAOJU:survey-contract",
            "<KAOJU:SURVEY-CONTRACT>",
            "[[KAOJU:SURVEY-CONTRACT]]",
            "KAOJU:SURVEY_CONTRACT",
        ):
            with self.subTest(invalid=invalid), self.assertRaises(ArtifactIdentityError):
                describe_binding(invalid)
        with self.assertRaises(ArtifactIdentityError):
            describe_binding("DEEPSCI:SURVEY-CONTRACT")
        with self.assertRaises(KeyError):
            describe_binding("KAOJU:UNKNOWN-CONTRACT")

    def test_named_template_bindings_define_mutable_state_and_exchange_evidence(self) -> None:
        bindings = load_binding_registry()
        for semantic_id in ("KAOJU:PAPER-TEMPLATE-MYST", "KAOJU:PAPER-TEMPLATE-LATEX"):
            with self.subTest(semantic_id=semantic_id):
                template = bindings[semantic_id]
                self.assertEqual("directory_manifest", template.content_mode)
                self.assertEqual("mutable_state", template.revision_mode)
                self.assertEqual("template_name", template.scope_key_policy["dimension"])
                self.assertEqual("mutable_named", template.latest_selection_policy)
                self.assertEqual((), template.relationships)

        self.assertEqual("paper-template-latex", bindings["KAOJU:PAPER-TEMPLATE-LATEX"].artifact_type)
        self.assertEqual(("paper_template_latex",), bindings["KAOJU:PAPER-TEMPLATE-TEX"].relationships)

        audit = bindings["KAOJU:PAPER-TEMPLATE-MUTATION-AUDIT"]
        self.assertEqual("append_only", audit.revision_mode)
        self.assertEqual("ordinary_file", audit.content_mode)
        self.assertEqual(("paper_template",), audit.relationships)
        for semantic_id in ("KAOJU:PAPER-TEMPLATE-EXPORT", "KAOJU:PAPER-TEMPLATE-MANIFEST"):
            binding = bindings[semantic_id]
            self.assertEqual("template_name", binding.scope_key_policy["dimension"])
            self.assertIn("paper_template", binding.relationships)

        schema = self.resource_json("bindings.v2.schema.json")
        binding_schema = schema["$defs"]["binding"]
        self.assertIn("mutable_state", binding_schema["properties"]["revision_mode"]["enum"])
        self.assertIn("mutable_named", binding_schema["properties"]["latest_selection_policy"]["enum"])

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

    def test_invalid_binding_and_semantic_fixtures_are_rejected_deterministically(self) -> None:
        raw_bindings = self.resource_json("bindings.v2.json")
        duplicate_bindings = deepcopy(raw_bindings)
        duplicate_bindings["bindings"][1]["semantic_id"] = duplicate_bindings["bindings"][0]["semantic_id"]  # type: ignore[index]
        first_binding = raw_bindings["bindings"][0]["semantic_id"]  # type: ignore[index]
        self.assertTrue(any(f"duplicate {first_binding}" in item for item in validate_binding_registry_document(duplicate_bindings)))

        invalid_binding_ids = (
            "kaoju:survey-contract",
            "Kaoju:SURVEY-CONTRACT",
            "DEEPSCI:SURVEY-CONTRACT",
            "<KAOJU:SURVEY-CONTRACT>",
            "KAOJU:PAPER-DRAFT",
        )
        for invalid in invalid_binding_ids:
            fixture = deepcopy(raw_bindings)
            fixture["bindings"][0]["semantic_id"] = invalid  # type: ignore[index]
            with self.subTest(binding=invalid):
                self.assertTrue(validate_binding_registry_document(fixture))

        raw_semantics = self.resource_json("artifact-semantics.v1.json")
        duplicate_semantics = deepcopy(raw_semantics)
        duplicate_semantics["artifacts"].append(deepcopy(duplicate_semantics["artifacts"][0]))  # type: ignore[union-attr,index]
        first_semantic = raw_semantics["artifacts"][0]["semantic_id"]  # type: ignore[index]
        self.assertTrue(any(f"duplicate {first_semantic}" in item for item in validate_semantic_registry_document(duplicate_semantics)))
        malformed_semantics = deepcopy(raw_semantics)
        malformed_semantics["artifacts"][0]["semantic_id"] = "KAOJU:WORKSPACE_READINESS"  # type: ignore[index]
        self.assertTrue(validate_semantic_registry_document(malformed_semantics))

    def test_all_five_resources_load_from_the_installed_package_namespace(self) -> None:
        for name in (
            "survey-process.v2.json",
            "bindings.v2.json",
            "bindings.v2.schema.json",
            "artifact-semantics.v1.json",
            "artifact-semantics.v1.schema.json",
        ):
            self.resource_json(name)

    def test_supersession_and_dependency_decisions_are_locked(self) -> None:
        raw = load_contract().raw
        self.assertEqual("add-kaoju-paper-writing", raw["supersession"]["source_change"])
        self.assertIn("LaTeX source is canonical paper state", raw["supersession"]["replaced_requirements"])
        decisions = raw["implementation_decisions"]
        self.assertEqual("5.1.0", decisions["myst_parser"]["locked_selection"])
        self.assertEqual("KAOJU:PAPER-TEMPLATE-LATEX", decisions["paper_templates"]["latex_identity"])
        self.assertEqual(
            "report working-copy, stocked-template, and paper-local repair drift without automatic propagation",
            decisions["paper_templates"]["drift_policy"],
        )
        self.assertEqual(["preamble", "marker", "include"], raw["template_roles"]["latex"]["composition_modes"])
        self.assertEqual("independent-compatible-implementation", decisions["wiki_viewer"]["decision"])


if __name__ == "__main__":
    unittest.main()
