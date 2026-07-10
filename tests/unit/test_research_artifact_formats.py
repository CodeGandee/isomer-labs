from __future__ import annotations

import json
from importlib import resources
from unittest import TestCase
from unittest.mock import patch

from isomer_labs.artifact_formats import (
    ArtifactFormatRegistry,
    ArtifactFormatResolver,
    ResearchRecordFormatProvider,
    parse_research_profile_ref,
    register_builtin_artifact_format_providers,
    render_artifact,
    research_profile_ref,
    validate_payload,
)
from isomer_labs.deepsci_ext.record_formats import (
    PROFILE_ASSETS,
    active_profile_names,
    canonical_record_format_ref,
)


SURVEY_CONTRACT_REF = "isomer:research/record-format/profile/kaoju/contract/survey-contract/v1"


def _survey_contract_payload() -> dict[str, object]:
    return {
        "title": "Survey Contract",
        "summary": "Defines a bounded literature and codebase survey.",
        "artifact_family": "kaoju",
        "semantic_id": "kaoju:survey-contract",
        "artifact_type": "survey-contract",
        "sections": {"scope": {"question": "What works exist?"}},
    }


class ResearchArtifactFormatProviderTests(TestCase):
    def test_profile_ref_round_trip_and_rejects_unsupported_versions(self) -> None:
        ref = research_profile_ref("kaoju", "contract", "survey-contract")
        parsed = parse_research_profile_ref(ref)
        self.assertIsNotNone(parsed)
        assert parsed is not None
        self.assertEqual(("kaoju", "contract", "survey-contract", "v1"), (parsed.family, parsed.artifact_class, parsed.semantic_id, parsed.version))
        self.assertIsNone(parse_research_profile_ref(ref.removesuffix("v1") + "v2"))

    def test_catalog_profiles_resolve_with_declarative_metadata(self) -> None:
        provider = ResearchRecordFormatProvider()
        self.assertEqual(25, len(provider.profile_refs()))
        registry = ArtifactFormatRegistry()
        registry.register_provider(provider)
        profile, resolution, diagnostics = ArtifactFormatResolver(registry).resolve_profile(SURVEY_CONTRACT_REF)
        self.assertEqual([], diagnostics)
        self.assertIsNotNone(resolution)
        self.assertIsNotNone(profile)
        assert profile is not None
        self.assertEqual("kaoju", profile.metadata["artifact_family"])
        self.assertEqual("kaoju:survey-contract", profile.metadata["semantic_id"])
        self.assertEqual(["artifact"], profile.metadata["compatible_record_kinds"])
        self.assertEqual(["sections.scope"], profile.validation_hints["required_paths"])

    def test_common_identity_and_required_paths_validate(self) -> None:
        registry = ArtifactFormatRegistry()
        register_builtin_artifact_format_providers(registry)
        valid = validate_payload(_survey_contract_payload(), registry=registry, format_profile_ref=SURVEY_CONTRACT_REF)
        self.assertTrue(valid.ok, [diagnostic.message for diagnostic in valid.diagnostics])

        missing = _survey_contract_payload()
        missing["sections"] = {"other": {}}
        invalid = validate_payload(missing, registry=registry, format_profile_ref=SURVEY_CONTRACT_REF)
        self.assertFalse(invalid.ok)
        self.assertTrue(any(diagnostic.field == "sections.scope" for diagnostic in invalid.diagnostics))

        mismatch = _survey_contract_payload()
        mismatch["semantic_id"] = "kaoju:field-summary"
        invalid = validate_payload(mismatch, registry=registry, format_profile_ref=SURVEY_CONTRACT_REF)
        self.assertFalse(invalid.ok)
        self.assertTrue(any(diagnostic.field == "semantic_id" for diagnostic in invalid.diagnostics))

    def test_markdown_render_reports_neutral_assets_without_mutating_payload(self) -> None:
        registry = ArtifactFormatRegistry()
        register_builtin_artifact_format_providers(registry)
        payload = _survey_contract_payload()
        original = json.dumps(payload, sort_keys=True)
        rendered = render_artifact(payload, registry=registry, format_profile_ref=SURVEY_CONTRACT_REF)
        self.assertTrue(rendered.ok, [diagnostic.message for diagnostic in rendered.diagnostics])
        self.assertIn("# Survey Contract", str(rendered.content))
        self.assertEqual("isomer:research/record-format/schema/research-structured-record/v1", rendered.schema_ref)
        self.assertEqual("isomer:research/record-format/template/markdown/research-structured-record/v1", rendered.template_ref)
        self.assertEqual(original, json.dumps(payload, sort_keys=True))

    def test_catalog_duplicate_and_family_mismatch_diagnostics_are_deterministic(self) -> None:
        catalog = {
            "schema_version": "isomer-research-record-format-catalog.v1",
            "family": "kaoju",
            "profiles": [
                {
                    "family": "kaoju",
                    "artifact_class": "report",
                    "semantic_id": "sample",
                    "artifact_type": "sample",
                    "compatible_record_kinds": ["artifact"],
                    "required_payload_paths": ["sections.sample"],
                    "relationship_paths": [],
                    "file_paths": [],
                    "facet_paths": {},
                    "renderer": "markdown",
                    "version": "v1",
                    "status": "active",
                }
            ],
        }
        with patch("isomer_labs.artifact_formats.research_record_formats._resource_text", return_value=json.dumps(catalog)):
            with self.assertRaisesRegex(ValueError, "Duplicate research format profile ref"):
                ResearchRecordFormatProvider(catalog_resources=("one.json", "two.json"))
        catalog["profiles"][0]["family"] = "other"
        with patch("isomer_labs.artifact_formats.research_record_formats._resource_text", return_value=json.dumps(catalog)):
            with self.assertRaisesRegex(ValueError, "family mismatch"):
                ResearchRecordFormatProvider(catalog_resources=("one.json",))

    def test_missing_catalog_asset_and_profile_are_diagnostic(self) -> None:
        with self.assertRaisesRegex(ValueError, "could not be loaded"):
            ResearchRecordFormatProvider(catalog_resources=("missing.json",))
        registry = ArtifactFormatRegistry()
        registry.register_provider(ResearchRecordFormatProvider())
        profile, resolution, diagnostics = ArtifactFormatResolver(registry).resolve_profile(
            "isomer:research/record-format/profile/kaoju/report/missing/v1"
        )
        self.assertIsNone(profile)
        self.assertIsNone(resolution)
        self.assertEqual("ISO201", diagnostics[0].code)

    def test_neutral_provider_assets_are_packaged(self) -> None:
        package = resources.files("isomer_labs.artifact_formats")
        for relative in (
            "assets/research_record_formats/profiles/kaoju.v1.json",
            "assets/research_record_formats/schemas/research-structured-record.v1.schema.json",
            "assets/research_record_formats/templates/markdown/research-structured-record.v1.md.j2",
        ):
            self.assertTrue(package.joinpath(relative).is_file(), relative)

    def test_all_existing_deepsci_public_refs_keep_provider_identity_and_validation(self) -> None:
        registry = ArtifactFormatRegistry()
        register_builtin_artifact_format_providers(registry)
        resolver = ArtifactFormatResolver(registry)
        self.assertEqual(
            ["isomer.deepsci.record-formats", "isomer.research.record-formats"],
            [provider.provider_id for provider in registry.providers()],
        )
        for name in active_profile_names():
            version = "v1" if name in PROFILE_ASSETS else "v2"
            profile_ref = canonical_record_format_ref(name, "profile", version=version)
            profile, resolution, diagnostics = resolver.resolve_profile(profile_ref)
            self.assertEqual([], diagnostics, profile_ref)
            self.assertIsNotNone(profile, profile_ref)
            self.assertIsNotNone(resolution, profile_ref)
            assert profile is not None
            self.assertEqual("deepsci", profile.metadata["provider"])
            for kind in ("schema", "template"):
                ref = canonical_record_format_ref(name, kind, version=version)
                resolved, ref_diagnostics = (
                    resolver.resolve_schema(ref) if kind == "schema" else resolver.resolve_template(ref)
                )
                self.assertEqual([], ref_diagnostics, ref)
                self.assertIsNotNone(resolved, ref)
            if name not in PROFILE_ASSETS:
                validation = validate_payload(
                    {"title": "Compatibility", "summary": "Existing DeepSci payload."},
                    registry=registry,
                    format_profile_ref=profile_ref,
                )
                self.assertTrue(validation.ok, profile_ref)
                self.assertTrue(str(validation.schema_ref).startswith("isomer:deepsci/"))
