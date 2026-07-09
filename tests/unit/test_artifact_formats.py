from __future__ import annotations

import json
import unittest

from isomer_labs.artifact_formats import (
    ArtifactFormatRegistry,
    ArtifactFormatResolver,
    StaticArtifactFormatProvider,
    parse_format_ref,
    render_artifact,
    validate_format_ref,
    validate_payload,
)
from isomer_labs.deepsci_ext.record_formats import canonical_record_format_ref, register_deepsci_record_format_provider


PROFILE_REF = "isomer:test/record-format/profile/run/main-run-record/v1"
SCHEMA_REF = "isomer:test/record-format/schema/run/main-run-record/v1"
TEMPLATE_REF = "isomer:test/record-format/template/markdown/run/main-run-record/v1"


def make_registry(*, broken_template: bool = False) -> ArtifactFormatRegistry:
    registry = ArtifactFormatRegistry()
    profile = {
        "schema_ref": SCHEMA_REF,
        "templates": {"markdown": TEMPLATE_REF},
        "media_type": "application/json",
        "schema_version": "v1",
        "status": "active",
    }
    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "required": ["title", "score"],
        "properties": {
            "title": {"type": "string"},
            "score": {"type": "number"},
        },
        "additionalProperties": False,
    }
    template = "# {{ payload.title }}\n\nScore: {{ payload.score }}\n"
    if broken_template:
        template = "{{ payload.missing.required }}"
    registry.register_provider(
        StaticArtifactFormatProvider(
            "test",
            profiles={PROFILE_REF: json.dumps(profile, sort_keys=True)},
            schemas={SCHEMA_REF: json.dumps(schema, sort_keys=True)},
            templates={TEMPLATE_REF: template},
        )
    )
    return registry


class ArtifactFormatApiTests(unittest.TestCase):
    def test_ref_parsing_accepts_canonical_shape(self) -> None:
        parsed = parse_format_ref(PROFILE_REF)
        self.assertEqual("isomer", parsed.origin)
        self.assertEqual("test", parsed.owner_slug)
        self.assertEqual(PROFILE_REF, parsed.text)

    def test_ref_validation_rejects_missing_origin(self) -> None:
        diagnostics = validate_format_ref("test/record-format/profile/run")
        self.assertEqual(1, len(diagnostics))
        self.assertEqual("ISO200", diagnostics[0].code)

    def test_provider_resolution_returns_profile_schema_and_template(self) -> None:
        resolver = ArtifactFormatResolver(make_registry())
        profile, profile_resolution, diagnostics = resolver.resolve_profile(PROFILE_REF)
        self.assertEqual([], diagnostics)
        self.assertIsNotNone(profile)
        self.assertIsNotNone(profile_resolution)
        assert profile is not None
        self.assertEqual(SCHEMA_REF, profile.schema_ref)
        self.assertEqual(TEMPLATE_REF, profile.templates["markdown"])

    def test_payload_validation_succeeds(self) -> None:
        result = validate_payload({"title": "Run", "score": 1.5}, registry=make_registry(), format_profile_ref=PROFILE_REF)
        self.assertTrue(result.ok)
        self.assertEqual("valid", result.status)
        self.assertEqual(SCHEMA_REF, result.schema_ref)
        self.assertEqual(PROFILE_REF, result.profile_ref)

    def test_payload_validation_failure_is_deterministic(self) -> None:
        result = validate_payload({"title": "Run"}, registry=make_registry(), format_profile_ref=PROFILE_REF)
        self.assertFalse(result.ok)
        self.assertEqual("invalid", result.status)
        self.assertEqual("ISO204", result.diagnostics[0].code)
        self.assertIn("required", result.diagnostics[0].message)

    def test_render_succeeds(self) -> None:
        result = render_artifact({"title": "Run", "score": 1.5}, registry=make_registry(), format_profile_ref=PROFILE_REF)
        self.assertTrue(result.ok)
        self.assertEqual("rendered", result.status)
        self.assertEqual("# Run\n\nScore: 1.5", str(result.content).strip())
        self.assertEqual(TEMPLATE_REF, result.template_ref)

    def test_render_failure_is_deterministic(self) -> None:
        result = render_artifact({"title": "Run", "score": 1.5}, registry=make_registry(broken_template=True), format_profile_ref=PROFILE_REF)
        self.assertFalse(result.ok)
        self.assertEqual("error", result.status)
        self.assertEqual("ISO205", result.diagnostics[0].code)

    def test_deepsci_structured_v2_requires_title_and_summary(self) -> None:
        registry = ArtifactFormatRegistry()
        register_deepsci_record_format_provider(registry)
        profile_ref = canonical_record_format_ref("report.raw-idea-slate", "profile")

        valid = validate_payload({"title": "Raw ideas", "summary": "Candidate idea slate."}, registry=registry, format_profile_ref=profile_ref)
        self.assertTrue(valid.ok, [diagnostic.message for diagnostic in valid.diagnostics])
        self.assertEqual(canonical_record_format_ref("report.raw-idea-slate", "schema"), valid.schema_ref)
        self.assertTrue(profile_ref.endswith("/v2"))

        missing_summary = validate_payload({"title": "Raw ideas"}, registry=registry, format_profile_ref=profile_ref)
        self.assertFalse(missing_summary.ok)
        self.assertEqual("invalid", missing_summary.status)
        self.assertTrue(any("summary" in diagnostic.message for diagnostic in missing_summary.diagnostics))

        empty_summary = validate_payload({"title": "Raw ideas", "summary": "   "}, registry=registry, format_profile_ref=profile_ref)
        self.assertFalse(empty_summary.ok)
        self.assertEqual("invalid", empty_summary.status)

    def test_deepsci_structured_v2_template_renders_summary(self) -> None:
        registry = ArtifactFormatRegistry()
        register_deepsci_record_format_provider(registry)
        rendered = render_artifact(
            {"title": "Raw ideas", "summary": "Candidate idea slate."},
            registry=registry,
            format_profile_ref=canonical_record_format_ref("report.raw-idea-slate", "profile"),
        )
        self.assertTrue(rendered.ok, [diagnostic.message for diagnostic in rendered.diagnostics])
        self.assertIn("Raw ideas", str(rendered.content))
        self.assertIn("Candidate idea slate.", str(rendered.content))

    def test_deepsci_structured_v1_resolves_as_legacy_unsupported(self) -> None:
        registry = ArtifactFormatRegistry()
        register_deepsci_record_format_provider(registry)
        resolver = ArtifactFormatResolver(registry)
        profile_ref = canonical_record_format_ref("report.raw-idea-slate", "profile", version="v1")

        profile, _resolution, diagnostics = resolver.resolve_profile(profile_ref)
        self.assertEqual([], diagnostics)
        self.assertIsNotNone(profile)
        assert profile is not None
        self.assertEqual("legacy_unsupported", profile.status)
        self.assertEqual("v1", profile.compatibility_version)

    def test_topic_reset_profiles_resolve_validate_and_render(self) -> None:
        registry = ArtifactFormatRegistry()
        register_deepsci_record_format_provider(registry)
        profile_ref = "isomer:deepsci/record-format/profile/control/topic-reset-checkpoint/v1"
        payload = {
            "title": "Topic Reset Checkpoint",
            "summary": "Checkpoint summary",
            "status": "ready",
            "research_topic_id": "alpha",
            "topic_workspace_id": "alpha",
            "checkpoint_id": "topic-reset-checkpoint-alpha",
            "created_at": "2026-07-02T00:00:00Z",
            "workspace_runtime_schema_version": "isomer-workspace-runtime.v1",
            "source_readiness_evidence": None,
            "topic_workspace_summary_ref": None,
            "summary_paths": [],
            "semantic_path_inventory": [],
            "preserved_record_ids": ["research-topic:alpha"],
            "preserved_structured_payload_ids": [],
            "preserved_generated_view_paths": [],
            "preserved_artifact_format_registration_ids": [],
            "preserved_readiness_record_ids": [],
            "preserved_semantic_labels": [],
            "preserved_support_paths": [],
            "runtime_high_watermarks": {},
            "blockers": [],
            "extensions": [],
            "no_git_operations": True,
        }
        validation = validate_payload(payload, registry=registry, format_profile_ref=profile_ref)
        self.assertTrue(validation.ok, [diagnostic.message for diagnostic in validation.diagnostics])
        rendered = render_artifact(payload, registry=registry, format_profile_ref=profile_ref)
        self.assertTrue(rendered.ok, [diagnostic.message for diagnostic in rendered.diagnostics])
        self.assertIn("Topic Reset Checkpoint", str(rendered.content))

    def test_topic_reset_schema_rejects_git_operation_fields(self) -> None:
        registry = ArtifactFormatRegistry()
        register_deepsci_record_format_provider(registry)
        payload = {
            "title": "Topic Reset Checkpoint",
            "summary": "Checkpoint summary",
            "status": "ready",
            "research_topic_id": "alpha",
            "topic_workspace_id": "alpha",
            "checkpoint_id": "topic-reset-checkpoint-alpha",
            "workspace_runtime_schema_version": "isomer-workspace-runtime.v1",
            "semantic_path_inventory": [],
            "preserved_record_ids": [],
            "preserved_structured_payload_ids": [],
            "runtime_high_watermarks": {},
            "blockers": [],
            "no_git_operations": True,
            "git_stash_id": "stash@{0}",
        }
        validation = validate_payload(
            payload,
            registry=registry,
            format_profile_ref="isomer:deepsci/record-format/profile/control/topic-reset-checkpoint/v1",
        )
        self.assertFalse(validation.ok)
        self.assertEqual("invalid", validation.status)


if __name__ == "__main__":
    unittest.main()
