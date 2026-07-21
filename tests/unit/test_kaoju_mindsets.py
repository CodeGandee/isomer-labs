from __future__ import annotations

from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest
from unittest.mock import Mock, patch

from isomer_labs.kaoju.contracts import load_binding_registry, load_contract, load_semantic_registry
from isomer_labs.kaoju.mindsets import (
    COLLECTOR_ANSWER_EXPECTATION,
    COLLECTOR_PROMPT,
    DEFAULT_KEYS,
    EXPECTED_DEFAULT_QUESTIONS,
    canonical_digest,
    ensure_mindset_sources,
    load_mindset_source,
    materialize_record_payload,
    mindset_source_child,
    mindset_source_diagnostics,
    packaged_default_root,
    render_mindset_record,
    render_mindset_source,
    replace_mindset_source,
    select_mindset_key,
    target_for_question,
    validate_mindset_record,
    validate_packaged_defaults,
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
            observed = tuple((item["question_id"], item["prompt"]) for item in source["questions"])
            self.assertEqual(EXPECTED_DEFAULT_QUESTIONS[key], observed)
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
        invalid_source["additional_question_collector"]["prompt"] = "Anything else?"
        codes = {item.code for item in mindset_source_diagnostics(invalid_source, filename="paper.skimming.json")}
        self.assertIn("mindset_source_schema_invalid", codes)
        self.assertIn("mindset_authority_field_forbidden", codes)
        self.assertIn("mindset_question_id_duplicate", codes)
        self.assertIn("mindset_collector_prompt_invalid", codes)

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
            self.assertEqual({"paper.deep-dive", "source-code.ingest"}, {item["mindset_key"] for item in result["created"]})
            self.assertEqual(["paper.skimming"], [item["mindset_key"] for item in result["preserved"]])
            self.assertEqual(["paper.skimming"], [item["mindset_key"] for item in result["derivation_drift"]])
            self.assertFalse(replay["mutated"])
            self.assertEqual(set(DEFAULT_KEYS), {item["mindset_key"] for item in replay["preserved"]})
            preserved, diagnostics = load_mindset_source(existing_path)
            self.assertEqual([], diagnostics)
            assert preserved is not None
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
        self.assertEqual("source-code.ingest", select_mindset_key(action="examine", source_kind="repository", depth="deep", process=process))
        self.assertIsNone(select_mindset_key(action="draft-paper", source_kind="paper", depth="deep", process=process))
        with self.assertRaisesRegex(ValueError, "does not apply"):
            select_mindset_key(action="examine", source_kind="paper", depth="skim", process=process, explicit_key="paper.deep-dive")
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
        self.assertIn("Collector Posture", rendered)
        self.assertIn("Source Update Status", rendered)

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
