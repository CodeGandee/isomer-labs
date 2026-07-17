from __future__ import annotations

import tempfile
import tomllib
import unittest
from pathlib import Path

import yaml

from isomer_labs.skills.system_assets import materialize_system_skills, resolve_system_skill


class OperationSetRecordingSkillTests(unittest.TestCase):
    def test_core_skill_has_bounded_workflow_and_required_references(self) -> None:
        skill = resolve_system_skill("research/isomer-research-operation-set-recording")
        text = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
        for reference_name in (
            "manifest-contract.md",
            "command-reference.md",
            "recovery.md",
            "legacy-repair.md",
        ):
            self.assertTrue(skill.joinpath("references", reference_name).is_file(), reference_name)
        for token in (
            "## Workflow",
            "operation-sets inspect",
            "operation-sets accept",
            "operation-sets verify",
            "record_payload",
            "record_attachment",
            "disposable",
            "complete` receipt",
            "$isomer-research-idea-recording",
            "DO NOT guess record kinds",
            "DO NOT index a worker-staging path",
        ):
            self.assertIn(token, text)

    def test_manifest_recovery_and_legacy_guidance_preserve_canonical_boundaries(self) -> None:
        skill = resolve_system_skill("research/isomer-research-operation-set-recording")
        manifest = skill.joinpath("references", "manifest-contract.md").read_text(encoding="utf-8")
        recovery = skill.joinpath("references", "recovery.md").read_text(encoding="utf-8")
        legacy = skill.joinpath("references", "legacy-repair.md").read_text(encoding="utf-8")
        for token in (
            "isomer-operation-set-acceptance.v1",
            "supersedes_receipt_id",
            "local_record_key",
            "root_reason",
            "Record lineage in `parents` does not imply Idea Lineage",
        ):
            self.assertIn(token, manifest)
        self.assertIn("Retry the same `accept <manifest-path> --apply` command", recovery)
        self.assertIn("Do not hand-edit the query index", recovery)
        self.assertIn("Do not scan all worker directories", legacy)
        self.assertIn("`reference` intent", legacy)
        self.assertIn("do not reconstruct historical semantics", legacy.lower())

    def test_metadata_version_matches_project_and_operator_routes_to_focused_owner(self) -> None:
        root = Path(__file__).resolve().parents[2]
        project = tomllib.loads(root.joinpath("pyproject.toml").read_text(encoding="utf-8"))
        expected_version = project["project"]["version"]
        skill = resolve_system_skill("research/isomer-research-operation-set-recording")
        metadata = yaml.safe_load(skill.joinpath("agents", "openai.yaml").read_text(encoding="utf-8"))
        self.assertEqual(expected_version, metadata["metadata"]["version"])
        self.assertEqual("isomer-research-operation-set-recording", metadata["interface"]["display_name"])
        self.assertIn("$isomer-research-operation-set-recording", metadata["interface"]["default_prompt"])

        entrypoint = resolve_system_skill("operator/isomer-op-entrypoint")
        system_index = entrypoint.joinpath("references", "system-skill-index.md").read_text(encoding="utf-8")
        cli_index = entrypoint.joinpath("references", "cli-index.md").read_text(encoding="utf-8")
        input_surfaces = entrypoint.joinpath("references", "input-surfaces.md").read_text(encoding="utf-8")
        routing = entrypoint.joinpath("references", "routing-rules.md").read_text(encoding="utf-8")
        self.assertIn("isomer-research-operation-set-recording", system_index)
        self.assertIn("ext research operation-sets", cli_index)
        self.assertIn("acceptance manifest", input_surfaces)
        self.assertIn("operation set needs durable closeout", routing)
        self.assertNotIn("generic Project lifecycle management", system_index)

    def test_core_materialization_includes_complete_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary)
            materialize_system_skills(target, groups=("core",))
            skill = target / "research" / "isomer-research-operation-set-recording"
            self.assertTrue(skill.joinpath("SKILL.md").is_file())
            self.assertTrue(skill.joinpath("agents", "openai.yaml").is_file())
            self.assertTrue(skill.joinpath("references", "manifest-contract.md").is_file())
            self.assertTrue(skill.joinpath("references", "recovery.md").is_file())


if __name__ == "__main__":
    unittest.main()
