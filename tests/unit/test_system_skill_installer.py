from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from isomer_labs.skills.installer import (
    INSTALL_MARKER_FILENAME,
    inspect_system_skills,
    install_system_skills,
    resolve_system_skill_selection,
    resolve_targets,
    uninstall_system_skills,
)


class SystemSkillInstallerTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def test_target_defaults_are_deterministic(self) -> None:
        root = self.make_root()
        codex_home = root / "codex-home"
        with patch.dict(os.environ, {"CODEX_HOME": str(codex_home)}, clear=True):
            self.assertEqual(root / ".claude" / "skills", resolve_targets("claude-code", cwd=root)[0].skill_root)
            self.assertEqual(codex_home / "skills", resolve_targets("codex", cwd=root)[0].skill_root)
            self.assertEqual(root / ".kimi-code" / "skills", resolve_targets("kimi-code", cwd=root)[0].skill_root)
            self.assertEqual(root / ".agents" / "skills", resolve_targets("generic", cwd=root)[0].skill_root)

    def test_target_all_rejects_home_override(self) -> None:
        root = self.make_root()
        with self.assertRaisesRegex(RuntimeError, "--home"):
            resolve_targets("all", home=root / "skills", cwd=root)

    def test_selection_defaults_to_core_and_extension_adds_core(self) -> None:
        core = resolve_system_skill_selection()
        self.assertIn("core", core.selected_groups)
        self.assertIn("isomer-op-entrypoint", [skill.name for skill in core.skills])
        self.assertNotIn("deepsci", core.selected_extensions)

        deepsci = resolve_system_skill_selection(extensions=("deepsci",))
        self.assertIn("core", deepsci.selected_groups)
        self.assertIn("deepsci", deepsci.selected_extensions)
        self.assertIn("isomer-deepsci-pipeline", [skill.name for skill in deepsci.skills])

    def test_copy_projection_is_flat_and_marker_owned(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)

        result = install_system_skills(target, selection)

        self.assertTrue(result.ok)
        skill_dir = target.skill_root / "isomer-op-entrypoint"
        self.assertTrue((skill_dir / "SKILL.md").is_file())
        self.assertFalse((target.skill_root / "operator" / "isomer-op-entrypoint").exists())
        marker = json.loads((skill_dir / INSTALL_MARKER_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual("isomer-system-skill-install.v1", marker["schema_version"])
        self.assertEqual("operator/isomer-op-entrypoint", marker["source_path"])

        status = inspect_system_skills(target, selection)
        self.assertEqual(["isomer-op-entrypoint"], [record.name for record in status.installed])
        self.assertEqual((), status.missing)

    def test_install_refuses_unmanaged_collision_and_uninstall_preserves_it(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        collision = target.skill_root / "isomer-op-entrypoint"
        collision.mkdir(parents=True)
        (collision / "SKILL.md").write_text("user-owned\n", encoding="utf-8")

        install_result = install_system_skills(target, selection)
        self.assertFalse(install_result.ok)
        self.assertEqual(["isomer-op-entrypoint"], [item.name for item in install_result.unmanaged_collisions])
        self.assertEqual("user-owned\n", (collision / "SKILL.md").read_text(encoding="utf-8"))

        uninstall_result = uninstall_system_skills(target, selection)
        self.assertEqual(["isomer-op-entrypoint"], [item.name for item in uninstall_result.preserved_unmanaged])
        self.assertTrue(collision.is_dir())

    def test_uninstall_removes_owned_projection(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        install_system_skills(target, selection)

        result = uninstall_system_skills(target, selection)

        self.assertEqual(["isomer-op-entrypoint"], [record.name for record in result.removed])
        self.assertFalse((target.skill_root / "isomer-op-entrypoint").exists())


if __name__ == "__main__":
    unittest.main()
