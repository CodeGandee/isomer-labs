from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import isomer_labs.skills.system_assets as system_assets
from isomer_labs.skills.system_assets import (
    SystemSkillAssetError,
    callback_insertion_point_stage_names,
    has_system_skill_callback_insertion_point,
    iter_system_skill_callback_insertion_points,
    iter_system_skill_extensions,
    iter_system_skill_groups,
    iter_system_skill_paths,
    load_system_skill_manifest,
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
        self.assertEqual(("core", "extension"), tuple(group.kind for group in groups))
        self.assertEqual((True, False), tuple(group.always_available for group in groups))
        self.assertEqual((None, "deepsci"), tuple(group.extension_id for group in groups))
        paths = iter_system_skill_paths()
        old_houmao_interop_path = "operator/" + "isomer-op-" + "houmao-interop"
        self.assertIn("operator/isomer-op-entrypoint", paths)
        self.assertIn("operator/isomer-op-project-mgr", paths)
        self.assertIn("operator/isomer-op-toolbox-mgr", paths)
        self.assertNotIn("operator/isomer-op-toolbox-creator", paths)
        self.assertIn("service/isomer-srv-houmao-interop", paths)
        self.assertNotIn(old_houmao_interop_path, paths)
        self.assertIn("research-paradigm/deepsci/isomer-deepsci-write", paths)
        for skill_path in paths:
            skill = resolve_system_skill(skill_path)
            self.assertTrue(skill.joinpath("SKILL.md").is_file(), skill_path)

    def test_manifest_lists_system_extensions(self) -> None:
        extensions = iter_system_skill_extensions()
        self.assertEqual(("deepsci",), tuple(extension.extension_id for extension in extensions))
        self.assertEqual(("deepsci",), tuple(extension.group for extension in extensions))
        self.assertIn("research-paradigm/deepsci/isomer-deepsci-scout", extensions[0].skills)

    def test_manifest_declares_callback_insertion_points(self) -> None:
        self.assertEqual(("begin", "end"), callback_insertion_point_stage_names())
        points = iter_system_skill_callback_insertion_points(include_core=True, include_all_extensions=True)
        self.assertEqual(44, len(points))
        self.assertEqual(
            ("isomer-deepsci-analysis", "begin"),
            (points[0].target_skill, points[0].stage),
        )
        self.assertEqual(
            ("isomer-deepsci-write", "end"),
            (points[-1].target_skill, points[-1].stage),
        )
        scout_begin = iter_system_skill_callback_insertion_points(
            include_core=False,
            extension_ids=("deepsci",),
            skill="isomer-deepsci-scout",
            stage="begin",
        )
        self.assertEqual(1, len(scout_begin))
        self.assertTrue(has_system_skill_callback_insertion_point("isomer-deepsci-scout", "begin"))
        self.assertFalse(has_system_skill_callback_insertion_point("isomer-op-entrypoint", "begin"))

    def test_callback_insertion_point_filters_reject_unknown_extension(self) -> None:
        with self.assertRaises(SystemSkillAssetError):
            iter_system_skill_callback_insertion_points(extension_ids=("unknown",))
        with self.assertRaises(SystemSkillAssetError):
            iter_system_skill_callback_insertion_points(extension_ids=("deepsci",), include_all_extensions=True)

    def test_manifest_rejects_invalid_group_metadata(self) -> None:
        manifest = deepcopy(load_system_skill_manifest())
        del manifest["groups"]["core"]["kind"]
        with patch.object(system_assets, "load_system_skill_manifest", return_value=manifest):
            with self.assertRaisesRegex(SystemSkillAssetError, "kind"):
                iter_system_skill_groups()

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
            self.assertTrue((target / "operator" / "isomer-op-toolbox-mgr" / "SKILL.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-toolbox-mgr" / "agents" / "openai.yaml").is_file())
            self.assertTrue((target / "operator" / "isomer-op-toolbox-mgr" / "commands" / "help.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-toolbox-mgr" / "commands" / "author-toolbox.md").is_file())
            self.assertFalse((target / "operator" / "isomer-op-toolbox-creator").exists())
            old_houmao_interop_name = "isomer-op-" + "houmao-interop"
            self.assertFalse((target / "operator" / old_houmao_interop_name).exists())
            self.assertTrue((target / "service" / "isomer-srv-houmao-interop" / "SKILL.md").is_file())
            self.assertTrue((target / "service" / "isomer-srv-topic-env-setup" / "SKILL.md").is_file())
            self.assertFalse((target / "research-paradigm").exists())
            self.assertFalse((target / "dev").exists())

    def test_toolbox_mgr_skill_identity_and_command_pages(self) -> None:
        skill_path = "operator/isomer-op-toolbox-mgr"
        skill = resolve_system_skill(skill_path)
        skill_md = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: isomer-op-toolbox-mgr", skill_md)
        self.assertNotIn("name: isomer-op-toolbox-creator", skill_md)
        self.assertIn("description: Use when", skill_md)
        self.assertIn("## Workflow", skill_md)
        self.assertIn("### Procedural Subcommands", skill_md)
        self.assertIn("### Helper Subcommands", skill_md)
        for command_name in (
            "author-toolbox",
            "convert-skill",
            "insert-callback",
            "define-runtime-params",
            "manage-toolbox",
            "identify-insertion-points",
            "author-toolbox-source",
            "edit-callback-declarations",
            "edit-runtime-params",
            "inspect-effective-state",
            "help",
        ):
            command = skill.joinpath("commands", f"{command_name}.md")
            self.assertTrue(command.is_file(), command_name)
            self.assertIn("## Workflow", command.read_text(encoding="utf-8"), command_name)

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
