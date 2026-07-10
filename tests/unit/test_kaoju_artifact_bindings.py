from __future__ import annotations

import json
from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
KAOJU_ROOT = REPO_ROOT / "src/isomer_labs/assets/system_skills/research-paradigm/kaoju"
CATALOG_PATH = REPO_ROOT / "src/isomer_labs/artifact_formats/assets/research_record_formats/profiles/kaoju.v1.json"


class KaojuArtifactBindingTests(unittest.TestCase):
    def test_semantic_registry_bindings_and_profiles_have_exact_bidirectional_coverage(self) -> None:
        registry_text = (
            KAOJU_ROOT / "isomer-kaoju-shared/references/artifact-semantics.md"
        ).read_text(encoding="utf-8")
        registry_ids = set(re.findall(r"`(kaoju:[a-z0-9-]+)`", registry_text))
        binding_paths = sorted(KAOJU_ROOT.glob("isomer-kaoju-*/artifact-bindings.md"))
        self.assertEqual(10, len(binding_paths))
        binding_ids: list[str] = []
        for path in binding_paths:
            text = path.read_text(encoding="utf-8")
            binding_ids.extend(re.findall(r"^\| `(kaoju:[a-z0-9-]+)` \|", text, re.M))
            for term in ("--semantic-id", "--record-kind", "--format-profile", "--payload-file", "actor_metadata", "Lifecycle"):
                self.assertIn(term, text, (path, term))
        catalog = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
        catalog_ids = {f"{entry['family']}:{entry['semantic_id']}" for entry in catalog["profiles"]}
        self.assertEqual(25, len(registry_ids))
        self.assertEqual(registry_ids, set(binding_ids))
        self.assertEqual(len(binding_ids), len(set(binding_ids)))
        self.assertEqual(registry_ids, catalog_ids)

    def test_workspace_bootstrap_contract_covers_blockers_latest_reset_and_output_policy(self) -> None:
        text = (KAOJU_ROOT / "isomer-kaoju-workspace-mgr/SKILL.md").read_text(encoding="utf-8")
        for term in (
            "Effective Topic Context",
            "fresh Workspace Runtime",
            "topic.records.artifacts",
            "neutral provider",
            "artifact-bindings.md",
            "--latest-only",
            "actor posture",
            "worker output policy",
            "Topic Dataset Manifest",
            "kaoju:binding-index",
            "kaoju:workspace-readiness",
            "storage blocker",
            "topic-reset update-checkpoint",
            "subject to the accepted reset plan",
        ):
            self.assertIn(term, text)

    def test_manager_contracts_preserve_current_history_exports_and_owner_routing(self) -> None:
        survey = (KAOJU_ROOT / "isomer-kaoju-pipeline/commands/manage-survey.md").read_text(encoding="utf-8")
        for term in ("--artifact-family kaoju", "--semantic-id", "--latest-only", "--include-payload", "query lineage", "records render", "ambiguity", "without changing latest state"):
            self.assertIn(term, survey)
        dataset = (KAOJU_ROOT / "isomer-kaoju-pipeline/commands/manage-dataset.md").read_text(encoding="utf-8")
        for term in ("kaoju:topic-dataset-manifest", "Topic Workspace owner", "records revise", "Preserve the prior version", "Never mutate the external target"):
            self.assertIn(term, dataset)

    def test_bound_stages_route_writes_and_views_remain_derived(self) -> None:
        for skill_md in sorted(KAOJU_ROOT.glob("isomer-kaoju-*/SKILL.md")):
            if skill_md.parent.name == "isomer-kaoju-shared":
                continue
            text = skill_md.read_text(encoding="utf-8")
            self.assertIn("artifact-bindings.md", text, skill_md)
            self.assertIn("storage blocker", text, skill_md)
        recording = (KAOJU_ROOT / "isomer-kaoju-shared/references/artifact-recording.md").read_text(encoding="utf-8")
        self.assertIn("canonical structured state", recording)
        self.assertIn("render on demand", recording)
        self.assertIn("A repaired or adapted Run never revises a faithful Run", recording)
        self.assertIn("Only the Topic Workspace owner mutates managed links", recording)


if __name__ == "__main__":
    unittest.main()
