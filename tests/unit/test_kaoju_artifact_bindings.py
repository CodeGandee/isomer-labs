from __future__ import annotations

from copy import deepcopy
from importlib.resources import files
from importlib.resources.abc import Traversable
import json
from pathlib import Path
import re
import unittest

from isomer_labs.kaoju.contracts import load_binding_registry, load_contract, validate_binding_registry_document
from isomer_labs.skills.system_assets import resolve_system_skill, resolve_system_skill_capability


REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / "src/isomer_labs/artifact_formats/assets/research_record_formats/profiles/kaoju.v1.json"


def resolve_kaoju_skill(identity: str) -> Traversable:
    if identity == "isomer-ext-kaoju-entrypoint":
        return resolve_system_skill("research-paradigm/kaoju/isomer-ext-kaoju-entrypoint")
    return resolve_system_skill_capability(identity)


def resource_json(name: str) -> dict[str, object]:
    raw = files("isomer_labs.kaoju").joinpath("resources", name).read_text(encoding="utf-8")
    value = json.loads(raw)
    assert isinstance(value, dict)
    return value


class KaojuArtifactBindingTests(unittest.TestCase):
    def test_registry_profiles_summaries_and_producers_have_bidirectional_coverage(self) -> None:
        bindings = load_binding_registry()
        contract = load_contract()
        summary_text = resolve_system_skill_capability("isomer-kaoju-shared").joinpath(
            "references", "artifact-semantics.md"
        ).read_text(encoding="utf-8")
        summary_ids = set(re.findall(r"`(KAOJU:[A-Z0-9-]+)`", summary_text))
        self.assertEqual(set(bindings), summary_ids)

        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        profiles = {entry["semantic_id"]: entry for entry in catalog["profiles"]}
        for semantic_id, binding in bindings.items():
            if binding.profile_ref is None:
                self.assertNotEqual("structured_file", binding.content_mode, semantic_id)
                continue
            profile = profiles[semantic_id]
            expected_ref = f"isomer:research/record-format/profile/{profile['family']}/{profile['artifact_class']}/{profile['profile_slug']}/{profile['version']}"
            self.assertEqual(expected_ref, binding.profile_ref)
            self.assertIn(binding.record_kind, profile["compatible_record_kinds"])
            self.assertTrue(profile["renderer"])
        self.assertEqual(set(profiles), {semantic_id for semantic_id, binding in bindings.items() if binding.profile_ref})

        produced_by: dict[str, set[str]] = {}
        for semantic_id, binding in bindings.items():
            produced_by.setdefault(binding.producer, set()).add(semantic_id)
            self.assertTrue(set(binding.consumers) <= set(contract.skills) | {"isomer-srv-topic-env-setup"})
        for producer, expected in produced_by.items():
            if producer not in contract.skills:
                continue
            page = resolve_kaoju_skill(producer).joinpath("artifact-bindings.md")
            text = page.read_text(encoding="utf-8")
            match = re.search(r"(?m)^Produced semantic ids:\s*(.+)$", text)
            self.assertIsNotNone(match, producer)
            assert match is not None
            self.assertEqual(expected, set(re.findall(r"KAOJU:[A-Z0-9-]+", match.group(1))))
            self.assertIn("ext kaoju bindings describe KAOJU:WHAT", text)
            self.assertNotIn("contracts/", text)
            self.assertNotIn("bindings.v2.json", text)
            self.assertNotRegex(text, r"--(?:record-kind|semantic-label|format-profile|payload-file)")

    def test_registry_invalid_fixtures_are_rejected_deterministically(self) -> None:
        raw = resource_json("bindings.v2.json")
        schema = resource_json("bindings.v2.schema.json")
        duplicate = deepcopy(raw)
        duplicate["bindings"].append(deepcopy(duplicate["bindings"][0]))
        malformed = deepcopy(raw)
        malformed["bindings"][0]["semantic_id"] = "OTHER:WRONG"
        missing_scope = deepcopy(raw)
        del missing_scope["bindings"][0]["scope_key_policy"]
        cases = (duplicate, malformed, missing_scope)
        for fixture in cases:
            with self.subTest(fixture=fixture["bindings"][0].get("semantic_id")):
                self.assertTrue(validate_binding_registry_document(fixture, schema=schema))

    def test_workspace_and_shared_contract_cover_scoped_db_only_artifacts(self) -> None:
        workspace = resolve_system_skill_capability("isomer-kaoju-workspace-mgr").joinpath("SKILL.md").read_text(encoding="utf-8")
        shared_root = resolve_system_skill_capability("isomer-kaoju-shared")
        shared = shared_root.joinpath("SKILL.md").read_text(encoding="utf-8")
        recording = shared_root.joinpath("references", "artifact-recording.md").read_text(encoding="utf-8")
        for term in ("Workspace Runtime", "state DB", "scope", "directory", "Run", "Gate"):
            self.assertIn(term.casefold(), (workspace + shared + recording).casefold(), term)
        self.assertIn("A repaired or adapted Run never revises a faithful Run", recording)
        self.assertIn("Only the Topic Workspace owner mutates managed links", recording)


if __name__ == "__main__":
    unittest.main()
