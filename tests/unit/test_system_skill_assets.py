from __future__ import annotations

from pathlib import Path
import tempfile
import unittest

from isomer_labs.skills.system_assets import (
    SystemSkillAssetError,
    iter_system_skill_groups,
    iter_system_skill_paths,
    materialize_system_skills,
    resolve_system_skill,
    system_skills_root,
)


class SystemSkillAssetTests(unittest.TestCase):
    def test_packaged_root_contains_distributable_skillset_only(self) -> None:
        root = system_skills_root()
        for name in ("manifest.toml", "README.md", "misc", "operator", "research-paradigm", "service"):
            self.assertTrue(root.joinpath(name).exists(), name)
        self.assertFalse(root.joinpath("dev").exists())

    def test_manifest_groups_resolve_to_skills(self) -> None:
        groups = iter_system_skill_groups()
        self.assertEqual(("core", "deepsci"), tuple(group.name for group in groups))
        paths = iter_system_skill_paths()
        old_houmao_interop_path = "operator/" + "isomer-op-" + "houmao-interop"
        self.assertIn("operator/isomer-op-entrypoint", paths)
        self.assertIn("operator/isomer-op-project-mgr", paths)
        self.assertIn("service/isomer-srv-houmao-interop", paths)
        self.assertNotIn(old_houmao_interop_path, paths)
        self.assertIn("research-paradigm/deepsci/isomer-deepsci-write", paths)
        for skill_path in paths:
            skill = resolve_system_skill(skill_path)
            self.assertTrue(skill.joinpath("SKILL.md").is_file(), skill_path)

    def test_materialize_selected_group_preserves_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = materialize_system_skills(target, groups=("core",))
            self.assertEqual(("core",), result.groups)
            self.assertTrue((target / "manifest.toml").is_file())
            self.assertTrue((target / "operator" / "isomer-op-entrypoint" / "SKILL.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-entrypoint" / "agents" / "openai.yaml").is_file())
            self.assertTrue((target / "operator" / "isomer-op-entrypoint" / "references" / "extension-skill-index.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-project-mgr" / "SKILL.md").is_file())
            old_houmao_interop_name = "isomer-op-" + "houmao-interop"
            self.assertFalse((target / "operator" / old_houmao_interop_name).exists())
            self.assertTrue((target / "service" / "isomer-srv-houmao-interop" / "SKILL.md").is_file())
            self.assertTrue((target / "service" / "isomer-srv-topic-env-setup" / "SKILL.md").is_file())
            self.assertFalse((target / "research-paradigm").exists())
            self.assertFalse((target / "dev").exists())

    def test_materialize_refuses_non_empty_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "existing.txt").write_text("existing", encoding="utf-8")
            with self.assertRaises(SystemSkillAssetError):
                materialize_system_skills(target, groups=("core",))

    def test_rejects_unsafe_manifest_relative_paths(self) -> None:
        with self.assertRaises(SystemSkillAssetError):
            resolve_system_skill("../dev/isomer-dev-migrate-deepsci-skill")


if __name__ == "__main__":
    unittest.main()
