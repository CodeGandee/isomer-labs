from __future__ import annotations

import unittest

from isomer_labs.skills.system_assets import resolve_system_skill, resolve_system_skill_capability


class ResearchIdeaRecordingSkillTests(unittest.TestCase):
    def test_neutral_contract_is_facet_first_atomic_and_verifiable(self) -> None:
        skill = resolve_system_skill_capability("isomer-research-idea-recording")
        text = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
        contract = skill.joinpath("references", "recording-contract.md").read_text(encoding="utf-8")
        for token in (
            "exploration_state",
            "decision_state",
            "evidence_state",
            "archive_state",
            "visibility",
            "research_idea_effects",
            "atomic=true",
            "decision option",
            "exact object-valued JSON path",
            "ext research ideas validate",
        ):
            self.assertIn(token, contract)
        self.assertIn("Do not use the deprecated one-value `status` as the source of truth.", text)
        self.assertNotIn("isomer-deepsci", text)

    def test_deepsci_idea_producers_route_to_neutral_contract_without_status_only_completion(self) -> None:
        for name in (
            "isomer-deepsci-idea",
            "isomer-deepsci-decision",
            "isomer-deepsci-analysis",
            "isomer-deepsci-experiment",
            "isomer-deepsci-optimize",
            "isomer-deepsci-scout",
            "isomer-ext-deepsci-entrypoint",
        ):
            with self.subTest(skill=name):
                skill = (
                    resolve_system_skill("research-paradigm/deepsci/isomer-ext-deepsci-entrypoint")
                    if name == "isomer-ext-deepsci-entrypoint"
                    else resolve_system_skill_capability(name)
                )
                text = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
                self.assertIn("isomer-op-entrypoint->research-ideas", text)
                self.assertNotIn("idea status changes require", text.lower())
                self.assertNotIn("update selected, rejected, or deferred Research Idea status", text)
        shared_mapping = resolve_system_skill_capability("isomer-deepsci-shared").joinpath(
            "references", "research-idea-recording.md"
        ).read_text(encoding="utf-8")
        self.assertIn("authoritative contract", shared_mapping)
        self.assertIn("terminal result refs", shared_mapping)
        self.assertIn("running `isomer-cli --print-json ext research ideas validate`", shared_mapping)

    def test_kaoju_mapping_is_deepsci_independent_and_rejects_non_concept_material(self) -> None:
        shared = resolve_system_skill_capability("isomer-kaoju-shared")
        mapping = shared.joinpath("references", "research-idea-recording.md").read_text(encoding="utf-8")
        self.assertNotIn("isomer-deepsci", mapping)
        self.assertIn("Direction Set v2", mapping)
        self.assertIn("A merely unselected proposal remains `open`", mapping)
        self.assertIn("papers, repositories, datasets, search routes", mapping)
        for name in (
            "isomer-kaoju-frame",
            "isomer-ext-kaoju-entrypoint",
            "isomer-kaoju-discover",
            "isomer-kaoju-trial",
            "isomer-kaoju-compare",
            "isomer-kaoju-audit",
            "isomer-kaoju-synthesize",
            "isomer-kaoju-write",
        ):
            with self.subTest(skill=name):
                skill = (
                    resolve_system_skill("research-paradigm/kaoju/isomer-ext-kaoju-entrypoint")
                    if name == "isomer-ext-kaoju-entrypoint"
                    else resolve_system_skill_capability(name)
                )
                text = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
                self.assertIn("isomer-op-entrypoint->research-ideas", text)
                self.assertNotIn("isomer-deepsci", text)

    def test_choose_directions_requires_atomic_v2_effects_and_verification(self) -> None:
        command = resolve_system_skill("research-paradigm/kaoju/isomer-ext-kaoju-entrypoint").joinpath("commands", "choose-directions.md").read_text(encoding="utf-8")
        for token in (
            "canonical semantic `idea_id`",
            "active v2",
            "research_idea_effects",
            "atomic=true",
            "every Decision Record option",
            "run `ext research ideas validate`",
        ):
            self.assertIn(token, command)


if __name__ == "__main__":
    unittest.main()
