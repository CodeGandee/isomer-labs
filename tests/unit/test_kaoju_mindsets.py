from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
from typing import Mapping
import unittest
from unittest.mock import Mock, patch

from isomer_labs.artifact_formats import ArtifactFormatRegistry, ResearchRecordFormatProvider, render_artifact
from isomer_labs.kaoju.contracts import load_binding_registry, load_contract, load_semantic_registry
from isomer_labs.kaoju.mindsets import (
    COLLECTOR_ANSWER_EXPECTATION,
    COLLECTOR_PROMPT,
    DEFAULT_KEYS,
    DEFAULT_QUESTION_SET_ID,
    DEFAULT_TRIGGERING_CONDITION,
    EXPECTED_DEFAULT_QUESTIONS,
    SOURCE_SCHEMA_VERSION,
    SOURCE_SCHEMA_VERSION_V1,
    canonical_digest,
    ensure_mindset_sources,
    expanded_question_ids,
    load_mindset_source,
    materialize_record_payload,
    mindset_source_child,
    mindset_source_diagnostics,
    packaged_default_root,
    question_sets_for_source,
    render_mindset_record,
    render_mindset_source,
    replace_mindset_source,
    select_mindset_key,
    target_for_question,
    validate_mindset_record,
    validate_packaged_defaults,
    validate_question_set_selection,
)


class KaojuMindsetSourceTests(unittest.TestCase):
    def test_packaged_defaults_have_exact_checked_inventories_and_collectors(self) -> None:
        contract = load_contract()
        self.assertEqual([], validate_packaged_defaults(process=contract.raw))
        digests: dict[str, str] = {}
        for key in DEFAULT_KEYS:
            source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), key), expected_key=key)
            self.assertEqual([], diagnostics)
            assert source is not None
            self.assertEqual(SOURCE_SCHEMA_VERSION, source["schema_version"])
            observed = tuple((item["question_id"], item["prompt"]) for item in source["questions"])
            self.assertEqual(EXPECTED_DEFAULT_QUESTIONS[key], observed)
            self.assertEqual(
                [
                    {
                        "question_set_id": DEFAULT_QUESTION_SET_ID,
                        "triggering_condition": DEFAULT_TRIGGERING_CONDITION,
                        "question_ids": "all",
                    }
                ],
                source["question_sets"],
            )
            self.assertEqual(
                [question_id for question_id, _prompt in EXPECTED_DEFAULT_QUESTIONS[key]],
                expanded_question_ids(source, source["question_sets"][0]),
            )
            self.assertTrue(all(item["additional_notes"] == "" for item in source["questions"]))
            collector = source["additional_question_collector"]
            self.assertEqual("additional-questions", collector["question_id"])
            self.assertEqual(COLLECTOR_PROMPT, collector["prompt"])
            self.assertEqual(COLLECTOR_ANSWER_EXPECTATION, collector["answer_expectation"])
            self.assertEqual("", collector["additional_notes"])
            self.assertTrue(collector["repeatable"])
            digests[key] = canonical_digest(source)
        self.assertEqual(digests, {key: canonical_digest(load_mindset_source(mindset_source_child(packaged_default_root(), key))[0] or {}) for key in DEFAULT_KEYS})

    def test_safe_child_and_closed_source_validation_fail_closed(self) -> None:
        root = Path("/tmp/topic/intent/derived/mindsets")
        self.assertEqual(root / "paper.deep-dive.json", mindset_source_child(root, "paper.deep-dive"))
        for invalid in ("../other", "Paper.Deep", "paper/deep", "paper..deep", "paper_deep"):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError):
                mindset_source_child(root, invalid)
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        invalid_source = deepcopy(source)
        invalid_source["command"] = "run arbitrary code"
        invalid_source["questions"][1]["question_id"] = invalid_source["questions"][0]["question_id"]
        invalid_source["questions"][0]["triggering_condition"] = "Questions cannot select themselves."
        invalid_source["additional_question_collector"]["prompt"] = "Anything else?"
        codes = {item.code for item in mindset_source_diagnostics(invalid_source, filename="paper.skimming.json")}
        self.assertIn("mindset_source_schema_invalid", codes)
        self.assertIn("mindset_authority_field_forbidden", codes)
        self.assertIn("mindset_question_id_duplicate", codes)
        self.assertIn("mindset_collector_prompt_invalid", codes)

    def test_v2_question_sets_support_all_and_many_to_many_explicit_membership(self) -> None:
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        source["question_sets"].extend(
            [
                {
                    "question_set_id": "evaluation-focused",
                    "triggering_condition": "Use when evaluation evidence is central.",
                    "question_ids": ["survey-fit", "survey-evidence-signal"],
                },
                {
                    "question_set_id": "credibility-focused",
                    "triggering_condition": "Use when credibility risks are central.",
                    "question_ids": ["survey-fit", "scope-and-credibility-risk"],
                },
            ]
        )
        self.assertEqual([], mindset_source_diagnostics(source, filename="paper.skimming.json"))
        self.assertEqual(
            ["survey-fit", "survey-evidence-signal"],
            expanded_question_ids(source, source["question_sets"][1]),
        )
        rendered = render_mindset_source(source)
        self.assertIn("Questions: `all`", rendered)
        self.assertIn("### evaluation-focused", rendered)
        self.assertIn("`survey-fit`, `survey-evidence-signal`", rendered)

    def test_v2_question_set_validation_rejects_invalid_fallback_and_membership(self) -> None:
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None

        missing_default = deepcopy(source)
        missing_default["question_sets"][0]["question_set_id"] = "specialized"
        missing_codes = {item.code for item in mindset_source_diagnostics(missing_default)}
        self.assertIn("mindset_source_schema_invalid", missing_codes)
        self.assertIn("mindset_default_question_set_invalid", missing_codes)

        duplicate_default = deepcopy(source)
        duplicate_default["question_sets"].append(deepcopy(duplicate_default["question_sets"][0]))
        duplicate_codes = {item.code for item in mindset_source_diagnostics(duplicate_default)}
        self.assertIn("mindset_question_set_id_duplicate", duplicate_codes)
        self.assertIn("mindset_default_question_set_invalid", duplicate_codes)

        unresolved = deepcopy(source)
        unresolved["question_sets"][0]["question_ids"] = ["missing-question"]
        unresolved_codes = {item.code for item in mindset_source_diagnostics(unresolved)}
        self.assertIn("mindset_question_set_reference_unresolved", unresolved_codes)
        self.assertIn("mindset_question_unassigned", unresolved_codes)

        repeated = deepcopy(source)
        repeated["question_sets"][0]["question_ids"] = ["survey-fit", "survey-fit"]
        repeated_codes = {item.code for item in mindset_source_diagnostics(repeated)}
        self.assertIn("mindset_question_set_reference_duplicate", repeated_codes)

        invalid_all = deepcopy(source)
        invalid_all["question_sets"][0]["question_ids"] = "everything"
        invalid_all_codes = {item.code for item in mindset_source_diagnostics(invalid_all)}
        self.assertIn("mindset_source_schema_invalid", invalid_all_codes)
        self.assertIn("mindset_question_unassigned", invalid_all_codes)

        too_many_sets = deepcopy(source)
        too_many_sets["question_sets"].extend(
            {
                "question_set_id": f"set-{index}",
                "triggering_condition": f"Use for bounded case {index}.",
                "question_ids": ["survey-fit"],
            }
            for index in range(16)
        )
        self.assertIn(
            "mindset_source_schema_invalid",
            {item.code for item in mindset_source_diagnostics(too_many_sets)},
        )

    def test_v1_source_normalizes_to_implicit_default_without_mutation(self) -> None:
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        legacy = deepcopy(source)
        legacy["schema_version"] = SOURCE_SCHEMA_VERSION_V1
        legacy.pop("question_sets")
        before = deepcopy(legacy)
        self.assertEqual([], mindset_source_diagnostics(legacy, filename="paper.skimming.json"))
        self.assertEqual(
            [
                {
                    "question_set_id": "default",
                    "triggering_condition": None,
                    "question_ids": "all",
                }
            ],
            question_sets_for_source(legacy),
        )
        self.assertEqual(before, legacy)

    def test_source_rendering_escapes_user_content_and_stays_non_artifact(self) -> None:
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        source["purpose"] = "<script>alert('x')</script>"
        rendered = render_mindset_source(source, path=Path("mindsets/paper.skimming.json"))
        self.assertIn("&lt;script&gt;", rendered)
        self.assertNotIn("<script>", rendered)
        self.assertIn("Topic-Derived Mindset Source", rendered)
        self.assertNotIn("KAOJU:MINDSET-SOURCE", load_binding_registry())
        self.assertNotIn("KAOJU:MINDSET-SOURCE", load_semantic_registry())

    def test_create_missing_preserves_edits_copies_defaults_and_reports_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            overview = root / "intent/src/topic-overview.md"
            overview.parent.mkdir(parents=True)
            overview.write_text("# Topic\nSurvey reliable compilers.\n", encoding="utf-8")
            mindset_root = root / "intent/derived/mindsets"
            mindset_root.mkdir(parents=True)
            existing_seed, _ = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
            assert existing_seed is not None
            existing_seed["schema_version"] = SOURCE_SCHEMA_VERSION_V1
            existing_seed.pop("question_sets")
            existing_seed["questions"][0]["additional_notes"] = "Prioritize compiler reliability."
            existing_seed["derivation"] = {
                "overview_semantic_label": "topic.intent.overview",
                "overview_digest": "0" * 64,
                "seed_version": "1",
                "seed_digest": "1" * 64,
            }
            existing_path = mindset_source_child(mindset_root, "paper.skimming")
            existing_path.write_text(json.dumps(existing_seed), encoding="utf-8")

            def resolve(_context: object, label: str, **_kwargs: object) -> tuple[SimpleNamespace, list[object]]:
                return (SimpleNamespace(path=overview if label == "topic.intent.overview" else mindset_root), [])

            with patch("isomer_labs.kaoju.mindsets.resolve_semantic_path", side_effect=resolve):
                result = ensure_mindset_sources(Mock(), env={}, cwd=root)
                replay = ensure_mindset_sources(Mock(), env={}, cwd=root)
            self.assertTrue(result["ok"], result)
            self.assertEqual({"paper.deep-dive", "paper.lecture", "source-code.ingest"}, {item["mindset_key"] for item in result["created"]})
            self.assertEqual(["paper.skimming"], [item["mindset_key"] for item in result["preserved"]])
            self.assertEqual(["paper.skimming"], [item["mindset_key"] for item in result["derivation_drift"]])
            self.assertFalse(replay["mutated"])
            self.assertEqual(set(DEFAULT_KEYS), {item["mindset_key"] for item in replay["preserved"]})
            preserved, diagnostics = load_mindset_source(existing_path)
            self.assertEqual([], diagnostics)
            assert preserved is not None
            self.assertEqual(SOURCE_SCHEMA_VERSION_V1, preserved["schema_version"])
            self.assertNotIn("question_sets", preserved)
            self.assertEqual("Prioritize compiler reliability.", preserved["questions"][0]["additional_notes"])
            copied, diagnostics = load_mindset_source(mindset_source_child(mindset_root, "paper.deep-dive"))
            self.assertEqual([], diagnostics)
            default, _ = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.deep-dive"))
            self.assertEqual(default, copied)

    def test_invalid_existing_source_blocks_without_overwrite(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            overview = root / "overview.md"
            overview.write_text("Concrete topic", encoding="utf-8")
            mindset_root = root / "mindsets"
            mindset_root.mkdir()
            invalid = mindset_source_child(mindset_root, "paper.deep-dive")
            invalid.write_text('{"mindset_key":"wrong"}', encoding="utf-8")
            before = invalid.read_bytes()

            def resolve(_context: object, label: str, **_kwargs: object) -> tuple[SimpleNamespace, list[object]]:
                return (SimpleNamespace(path=overview if label == "topic.intent.overview" else mindset_root), [])

            with patch("isomer_labs.kaoju.mindsets.resolve_semantic_path", side_effect=resolve):
                result = ensure_mindset_sources(Mock(), env={}, cwd=root)
            self.assertFalse(result["ok"])
            self.assertEqual(["paper.deep-dive"], [item["mindset_key"] for item in result["invalid"]])
            self.assertEqual(before, invalid.read_bytes())

    def test_create_missing_rejects_specialization_that_emits_legacy_v1(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            overview = root / "overview.md"
            overview.write_text("Concrete topic", encoding="utf-8")
            mindset_root = root / "mindsets"

            def resolve(_context: object, label: str, **_kwargs: object) -> tuple[SimpleNamespace, list[object]]:
                return (SimpleNamespace(path=overview if label == "topic.intent.overview" else mindset_root), [])

            def legacy_specialization(seed: Mapping[str, object], _overview_text: str) -> Mapping[str, object]:
                candidate = dict(deepcopy(seed))
                candidate["schema_version"] = SOURCE_SCHEMA_VERSION_V1
                candidate.pop("question_sets")
                return candidate

            with patch("isomer_labs.kaoju.mindsets.resolve_semantic_path", side_effect=resolve):
                result = ensure_mindset_sources(
                    Mock(),
                    env={},
                    cwd=root,
                    specialize=legacy_specialization,
                )
            self.assertFalse(result["ok"])
            self.assertFalse(result["mutated"])
            self.assertEqual(set(DEFAULT_KEYS), {item["mindset_key"] for item in result["invalid"]})
            self.assertTrue(
                all(
                    any(diagnostic["code"] == "mindset_created_source_version_invalid" for diagnostic in item["diagnostics"])
                    for item in result["invalid"]
                )
            )
            self.assertTrue(all(not mindset_source_child(mindset_root, key).exists() for key in DEFAULT_KEYS))

    def test_explicit_replacement_checks_observed_digest_and_preserves_key(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "paper.skimming.json"
            source, _ = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
            assert source is not None
            path.write_text(json.dumps(source), encoding="utf-8")
            observed = canonical_digest(source)
            candidate = deepcopy(source)
            candidate["questions"][0]["additional_notes"] = "Emphasize the topic boundary."
            result = replace_mindset_source(path, candidate, observed_digest=observed)
            self.assertEqual(observed, result["old_digest"])
            self.assertNotEqual(observed, result["new_digest"])
            with self.assertRaisesRegex(ValueError, "changed after"):
                replace_mindset_source(path, source, observed_digest=observed)

            legacy = deepcopy(source)
            legacy["schema_version"] = SOURCE_SCHEMA_VERSION_V1
            legacy.pop("question_sets")
            path.write_text(json.dumps(legacy), encoding="utf-8")
            legacy_observed = canonical_digest(legacy)
            upgraded = replace_mindset_source(path, candidate, observed_digest=legacy_observed)
            self.assertEqual(legacy_observed, upgraded["old_digest"])
            upgraded_source, upgraded_diagnostics = load_mindset_source(path)
            self.assertEqual([], upgraded_diagnostics)
            assert upgraded_source is not None
            self.assertEqual(SOURCE_SCHEMA_VERSION, upgraded_source["schema_version"])

            path.write_text('{"mindset_key":"paper.skimming"}', encoding="utf-8")
            invalid_digest = sha256(path.read_bytes()).hexdigest()
            repaired = replace_mindset_source(path, candidate, observed_digest=invalid_digest)
            self.assertEqual(invalid_digest, repaired["old_digest"])
            repaired_source, diagnostics = load_mindset_source(path, expected_key="paper.skimming")
            self.assertEqual([], diagnostics)
            self.assertEqual(candidate, repaired_source)

    def test_checked_route_selection_and_question_targeting(self) -> None:
        process = load_contract().raw
        self.assertEqual("paper.deep-dive", select_mindset_key(action="examine", source_kind="paper", depth="full-text", process=process))
        self.assertEqual("paper.skimming", select_mindset_key(action="ingest-reading-item", source_kind="report", depth="triage", process=process))
        self.assertEqual("paper.lecture", select_mindset_key(action="examine", source_kind="paper", depth="lecture", process=process))
        self.assertEqual(
            "paper.lecture",
            select_mindset_key(
                action="ingest-reading-item",
                source_kind="report",
                depth="lecture",
                process=process,
                explicit_key="paper.lecture",
            ),
        )
        self.assertEqual("source-code.ingest", select_mindset_key(action="examine", source_kind="repository", depth="deep", process=process))
        self.assertIsNone(select_mindset_key(action="draft-paper", source_kind="paper", depth="deep", process=process))
        with self.assertRaisesRegex(ValueError, "does not apply"):
            select_mindset_key(action="examine", source_kind="paper", depth="skim", process=process, explicit_key="paper.deep-dive")
        ambiguous = deepcopy(process)
        ambiguous["mindsets"]["routes"].append(
            {
                "mindset_key": "paper.deep-dive",
                "actions": ["examine"],
                "source_kinds": ["paper"],
                "depths": ["lecture"],
            }
        )
        with self.assertRaisesRegex(ValueError, "ambiguous"):
            select_mindset_key(action="examine", source_kind="paper", depth="lecture", process=ambiguous)
        self.assertEqual("reading_artifact", target_for_question(explicit_target=None, asks_to_persist=False))
        self.assertEqual("clarify", target_for_question(explicit_target=None, asks_to_persist=True))
        self.assertEqual("source", target_for_question(explicit_target="source", asks_to_persist=True))
        self.assertEqual("record", target_for_question(explicit_target="record", asks_to_persist=True))
        self.assertEqual("both", target_for_question(explicit_target="both", asks_to_persist=True))


class KaojuMindsetRecordTests(unittest.TestCase):
    def make_payload(self) -> dict[str, object]:
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        return materialize_record_payload(
            source,
            relative_path="paper.skimming.json",
            topic_id="alpha",
            run_ref="run-1",
            survey_contract_ref="survey-contract-1",
            survey_context_refs=("direction-1",),
            question_set_id="default",
            question_set_selection_kind="default-fallback",
            question_set_selection_rationale="The packaged Source declares no specialized question sets.",
        )

    def test_materialization_validation_terminal_posture_and_rendering(self) -> None:
        payload = self.make_payload()
        self.assertEqual([], validate_mindset_record(payload))
        sections = payload["sections"]
        assert isinstance(sections, dict)
        snapshot = sections["source_snapshot"]
        assert isinstance(snapshot, dict)
        for row in snapshot["questions"]:
            row["answer_state"] = "unresolved"
            row["rationale"] = "Pending deeper evidence."
        collector = snapshot["additional_question_collector"]
        collector["answer_state"] = "answered"
        collector["answer"] = "No explicitly assigned supplemental questions."
        collector["checked"] = True
        sections["terminal_status"] = "paused"
        sections["unresolved_questions"] = [row["question_id"] for row in snapshot["questions"]]
        self.assertEqual([], validate_mindset_record(payload))
        rendered = render_mindset_record(payload)
        self.assertIn("Materialized Source Questions", rendered)
        self.assertIn("Snapshotted digest", rendered)
        self.assertIn("Question set: `default`", rendered)
        self.assertIn("Selection kind: `default-fallback`", rendered)
        self.assertIn("Collector Posture", rendered)
        self.assertIn("Source Update Status", rendered)

    def test_specialized_selection_materializes_only_explicit_order(self) -> None:
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        source["question_sets"].extend(
            [
                {
                    "question_set_id": "evidence-focused",
                    "triggering_condition": "Use when the task asks for the strongest evidence signal.",
                    "question_ids": ["survey-evidence-signal", "survey-fit"],
                },
                {
                    "question_set_id": "overlapping-focus",
                    "triggering_condition": "Use when the task also asks about evidence.",
                    "question_ids": ["survey-fit", "scope-and-credibility-risk"],
                },
            ]
        )
        payload = materialize_record_payload(
            source,
            relative_path="paper.skimming.json",
            topic_id="alpha",
            run_ref="run-specialized",
            survey_contract_ref="survey-contract-1",
            survey_context_refs=("direction-1",),
            question_set_id="evidence-focused",
            question_set_selection_kind="matched",
            question_set_selection_rationale="Evidence strength is the primary task.",
        )
        snapshot = payload["sections"]["source_snapshot"]
        self.assertEqual(
            ["survey-evidence-signal", "survey-fit"],
            [row["question_id"] for row in snapshot["questions"]],
        )
        self.assertEqual("evidence-focused", snapshot["question_set_selection"]["question_set_id"])
        self.assertEqual(
            "Use when the task asks for the strongest evidence signal.",
            snapshot["question_set_selection"]["triggering_condition"],
        )
        self.assertEqual([], validate_mindset_record(payload))

    def test_selection_boundary_rejects_invalid_set_kind_and_rationale(self) -> None:
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        source["question_sets"].append(
            {
                "question_set_id": "evidence-focused",
                "triggering_condition": "Use for evidence-focused tasks.",
                "question_ids": ["survey-evidence-signal"],
            }
        )
        with self.assertRaisesRegex(ValueError, "does not exist"):
            validate_question_set_selection(
                source,
                question_set_id="missing",
                selection_kind="matched",
                rationale="A reason.",
            )
        with self.assertRaisesRegex(ValueError, "default-fallback"):
            validate_question_set_selection(
                source,
                question_set_id="default",
                selection_kind="matched",
                rationale="A reason.",
            )
        with self.assertRaisesRegex(ValueError, "requires selection kind 'matched'"):
            validate_question_set_selection(
                source,
                question_set_id="evidence-focused",
                selection_kind="default-fallback",
                rationale="A reason.",
            )
        with self.assertRaisesRegex(ValueError, "nonempty"):
            validate_question_set_selection(
                source,
                question_set_id="evidence-focused",
                selection_kind="matched",
                rationale=" ",
            )

    def test_legacy_default_and_historical_record_compatibility(self) -> None:
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        source["schema_version"] = SOURCE_SCHEMA_VERSION_V1
        source.pop("question_sets")
        payload = materialize_record_payload(
            source,
            relative_path="paper.skimming.json",
            topic_id="alpha",
            run_ref="run-legacy",
            survey_contract_ref="survey-contract-1",
            survey_context_refs=("direction-1",),
        )
        snapshot = payload["sections"]["source_snapshot"]
        self.assertEqual("legacy-default", snapshot["question_set_selection"]["selection_kind"])
        self.assertIsNone(snapshot["question_set_selection"]["triggering_condition"])
        self.assertEqual(6, len(snapshot["questions"]))
        self.assertEqual([], validate_mindset_record(payload))

        historical = deepcopy(payload)
        historical_snapshot = historical["sections"]["source_snapshot"]
        historical_snapshot.pop("source_schema_version")
        historical_snapshot.pop("question_set_selection")
        self.assertEqual([], validate_mindset_record(historical))
        registry = ArtifactFormatRegistry()
        registry.register_provider(ResearchRecordFormatProvider())
        rendered = render_artifact(
            historical,
            registry=registry,
            format_profile_ref="isomer:research/record-format/profile/kaoju/reflection/mindset-record/v1",
        )
        self.assertTrue(rendered.ok, [diagnostic.message for diagnostic in rendered.diagnostics])
        self.assertIn("Source schema: `historical`", str(rendered.content))

    def test_question_set_selection_is_immutable_and_semantically_validated(self) -> None:
        prior = self.make_payload()
        changed = deepcopy(prior)
        selection = changed["sections"]["source_snapshot"]["question_set_selection"]
        selection["selection_kind"] = "matched"
        selection["triggering_condition"] = "Changed after materialization."
        codes = {item.code for item in validate_mindset_record(changed, prior_payload=prior)}
        self.assertIn("mindset_record_question_set_selection_invalid", codes)
        self.assertIn("mindset_record_snapshot_changed", codes)

    def test_materialization_requires_valid_source_and_selected_survey_context(self) -> None:
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        with self.assertRaisesRegex(ValueError, "Direction Set"):
            materialize_record_payload(
                source,
                relative_path="paper.skimming.json",
                topic_id="alpha",
                run_ref="run-1",
                survey_contract_ref="survey-contract-1",
                survey_context_refs=(),
            )
        source["tool"] = "execute"
        with self.assertRaisesRegex(ValueError, "invalid Mindset Source"):
            materialize_record_payload(
                source,
                relative_path="paper.skimming.json",
                topic_id="alpha",
                run_ref="run-1",
                survey_contract_ref="survey-contract-1",
                survey_context_refs=("direction-1",),
            )

    def test_malformed_locator_changed_snapshot_and_unfinished_terminal_are_rejected(self) -> None:
        prior = self.make_payload()
        changed = deepcopy(prior)
        sections = changed["sections"]
        assert isinstance(sections, dict)
        snapshot = sections["source_snapshot"]
        assert isinstance(snapshot, dict)
        snapshot["relative_path"] = "other.json"
        snapshot["questions"][0]["prompt"] = "Changed after Run start?"
        sections["terminal_status"] = "complete"
        codes = {item.code for item in validate_mindset_record(changed, prior_payload=prior)}
        self.assertIn("mindset_record_locator_mismatch", codes)
        self.assertIn("mindset_record_snapshot_changed", codes)
        self.assertIn("mindset_record_terminal_unanswered", codes)
        self.assertIn("mindset_record_collector_unchecked", codes)

    def test_record_rejects_changed_context_invalid_answers_evidence_and_supplemental_updates(self) -> None:
        prior = self.make_payload()
        changed = deepcopy(prior)
        sections = changed["sections"]
        assert isinstance(sections, dict)
        sections["survey_context"]["context_refs"] = ["direction-2"]
        first = sections["source_snapshot"]["questions"][0]
        first["answer_state"] = "answered"
        first["evidence_refs"] = ["../cross-topic"]
        sections["supplemental_questions"] = [
            {
                **deepcopy(first),
                "question_id": first["question_id"],
                "origin": "user",
                "association_basis": "The user explicitly assigned this question to the Record.",
                "introduction_stage": "examination",
                "disposition": "source_updated",
            }
        ]
        codes = {item.code for item in validate_mindset_record(changed, prior_payload=prior)}
        self.assertIn("mindset_record_snapshot_changed", codes)
        self.assertIn("mindset_record_answer_missing", codes)
        self.assertIn("mindset_record_question_id_duplicate", codes)
        self.assertIn("mindset_record_source_update_mismatch", codes)
        self.assertIn("mindset_record_schema_invalid", codes)

    def test_record_accepts_explicit_record_only_requested_and_completed_source_updates(self) -> None:
        payload = self.make_payload()
        sections = payload["sections"]
        assert isinstance(sections, dict)
        source_row = deepcopy(sections["source_snapshot"]["questions"][0])
        source_row.update(
            {
                "question_id": "user-supplement",
                "prompt": "Which compiler failure mode should this survey track?",
                "additional_notes": "",
                "origin": "user",
                "association_basis": "The user explicitly assigned this question to the active Mindset Record.",
                "introduction_stage": "paper-examination",
                "disposition": "record_only",
            }
        )
        sections["supplemental_questions"] = [source_row]
        self.assertEqual([], validate_mindset_record(payload))

        requested = deepcopy(payload)
        requested["sections"]["supplemental_questions"][0]["disposition"] = "source_update_requested"
        requested["sections"]["source_update"]["disposition"] = "source_update_requested"
        self.assertEqual([], validate_mindset_record(requested, prior_payload=payload))

        updated = deepcopy(requested)
        updated["sections"]["supplemental_questions"][0]["disposition"] = "source_updated"
        updated["sections"]["source_update"] = {
            "disposition": "source_updated",
            "new_relative_path": "paper.skimming.json",
            "new_digest": "a" * 64,
        }
        self.assertEqual([], validate_mindset_record(updated, prior_payload=requested))

    def test_active_record_keeps_source_snapshot_after_topic_source_mutation(self) -> None:
        payload = self.make_payload()
        snapshot_before = deepcopy(payload["sections"]["source_snapshot"])
        source, diagnostics = load_mindset_source(mindset_source_child(packaged_default_root(), "paper.skimming"))
        self.assertEqual([], diagnostics)
        assert source is not None
        source["questions"][0]["prompt"] = "A later-Run question"
        self.assertNotEqual(canonical_digest(source), snapshot_before["digest"])
        self.assertEqual(snapshot_before, payload["sections"]["source_snapshot"])
        self.assertEqual([], validate_mindset_record(payload))

    def test_binding_is_run_scoped_current_state_with_required_relationships(self) -> None:
        binding = load_binding_registry()["KAOJU:MINDSET-RECORD"]
        self.assertEqual("structured_file", binding.content_mode)
        self.assertEqual("topic.records.artifacts", binding.semantic_label)
        self.assertEqual("current_state", binding.revision_mode)
        self.assertEqual({"mode": "required", "dimension": "run"}, binding.scope_key_policy)
        self.assertEqual("scoped_current", binding.latest_selection_policy)
        self.assertEqual(("run", "survey_contract"), binding.relationships)
        self.assertEqual("isomer-ext-kaoju-entrypoint", binding.producer)


if __name__ == "__main__":
    unittest.main()
