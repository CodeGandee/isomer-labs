from __future__ import annotations

import json
import os
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from isomer_labs.skills.installer import (
    SKILL_MANIFEST_FILENAME,
    inspect_system_skills,
    install_system_skills,
    resolve_system_skill_selection,
    resolve_targets,
    uninstall_system_skills,
    upgrade_system_skills,
)


OLD_MARKER_FILENAME = ".isomer-system-skill.json"


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
        self.assertIn("isomer-op-gui-mgr", [skill.name for skill in core.skills])
        self.assertIn("isomer-op-system-skill-mgr", [skill.name for skill in core.skills])
        self.assertNotIn("deepsci", core.selected_extensions)
        self.assertNotIn("kaoju", core.selected_extensions)

        deepsci = resolve_system_skill_selection(extensions=("deepsci",))
        self.assertIn("core", deepsci.selected_groups)
        self.assertIn("deepsci", deepsci.selected_extensions)
        self.assertIn("isomer-deepsci-pipeline", [skill.name for skill in deepsci.skills])

        kaoju = resolve_system_skill_selection(extensions=("kaoju",))
        self.assertEqual(("kaoju",), kaoju.selected_extensions)
        self.assertIn("core", kaoju.selected_groups)
        self.assertIn("isomer-kaoju-pipeline", [skill.name for skill in kaoju.skills])
        self.assertNotIn("isomer-deepsci-pipeline", [skill.name for skill in kaoju.skills])

    def test_kaoju_extension_install_status_upgrade_and_uninstall(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(extensions=("kaoju",))

        installed = install_system_skills(target, selection)

        self.assertTrue(installed.ok)
        kaoju_names = sorted(record.name for record in installed.installed if record.name.startswith("isomer-kaoju-"))
        self.assertEqual(14, len(kaoju_names))
        self.assertTrue((target.skill_root / "isomer-kaoju-pipeline" / "commands" / "comparative-pass.md").is_file())
        self.assertTrue((target.skill_root / "isomer-kaoju-shared" / "references" / "source-identity.md").is_file())
        self.assertTrue((target.skill_root / "isomer-kaoju-shared" / "references" / "artifact-semantics.md").is_file())
        self.assertTrue((target.skill_root / "isomer-kaoju-frame" / "artifact-bindings.md").is_file())
        self.assertFalse((target.skill_root / "isomer-deepsci-pipeline").exists())

        status = inspect_system_skills(target, selection)
        self.assertEqual((), status.missing)
        self.assertEqual(14, len(tuple(record for record in status.installed if record.name.startswith("isomer-kaoju-"))))

        upgraded = upgrade_system_skills(target, selection)
        self.assertEqual(14, len(tuple(record for record in upgraded.refreshed if record.name.startswith("isomer-kaoju-"))))

        removed = uninstall_system_skills(target, selection)
        self.assertEqual(14, len(tuple(record for record in removed.removed if record.name.startswith("isomer-kaoju-"))))
        self.assertFalse((target.skill_root / "isomer-kaoju-pipeline").exists())

    def test_copy_projection_is_flat_and_manifest_tracked(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)

        result = install_system_skills(target, selection)

        self.assertTrue(result.ok)
        self.assertTrue(result.mutated)
        skill_dir = target.skill_root / "isomer-op-entrypoint"
        self.assertTrue((skill_dir / "SKILL.md").is_file())
        self.assertFalse((skill_dir / OLD_MARKER_FILENAME).exists())
        self.assertFalse((target.skill_root / "operator" / "isomer-op-entrypoint").exists())
        manifest = json.loads((target.skill_root / SKILL_MANIFEST_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual("isomer-labs-skill-manifest.v2", manifest["schema_version"])
        self.assertEqual(["isomer-op-entrypoint"], [item["name"] for item in manifest["skills"]])
        self.assertEqual("operator/isomer-op-entrypoint", manifest["skills"][0]["source_path"])
        self.assertEqual(selection.skills[0].skill_version, manifest["skills"][0]["skill_version"])

        status = inspect_system_skills(target, selection)
        self.assertEqual(["isomer-op-entrypoint"], [record.name for record in status.installed])
        self.assertEqual((), status.missing)
        self.assertIsNotNone(status.manifest)
        self.assertEqual("current", status.installed[0].compatibility_status)
        self.assertTrue(status.installed[0].installation_verified)

    def test_legacy_receipt_is_read_and_classified_unversioned(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        install_system_skills(target, selection)
        receipt_path = target.skill_root / SKILL_MANIFEST_FILENAME
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["schema_version"] = "isomer-labs-skill-manifest.v1"
        receipt["skills"][0].pop("skill_version")
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

        status = inspect_system_skills(target, selection)

        self.assertEqual("unversioned", status.installed[0].compatibility_status)
        self.assertFalse(status.installed[0].installation_verified)

    def test_status_reports_receipt_drift_obsolete_and_compatible_older(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        install_system_skills(target, selection)
        record = selection.skills[0]
        yaml_path = target.skill_root / record.name / "agents" / "openai.yaml"
        yaml_text = yaml_path.read_text(encoding="utf-8")
        yaml_path.write_text(yaml_text.replace(record.skill_version, "0.2.2"), encoding="utf-8")

        drift = inspect_system_skills(target, selection)
        self.assertEqual("receipt_drift", drift.installed[0].compatibility_status)

        receipt_path = target.skill_root / SKILL_MANIFEST_FILENAME
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["skills"][0]["skill_version"] = "0.2.2"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        compatible_record = replace(record, minimum_compatible_version="0.2.0")
        compatible_selection = replace(selection, skills=(compatible_record,))

        compatible = inspect_system_skills(target, compatible_selection)
        self.assertEqual("compatible_older", compatible.installed[0].compatibility_status)
        self.assertTrue(compatible.installed[0].installation_verified)

        obsolete = inspect_system_skills(target, selection)
        self.assertEqual("obsolete_incompatible", obsolete.installed[0].compatibility_status)

    def test_symlink_projection_does_not_write_per_skill_marker(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)

        result = install_system_skills(target, selection, projection_mode="symlink")

        self.assertTrue(result.ok)
        skill_link = target.skill_root / "isomer-op-entrypoint"
        self.assertTrue(skill_link.is_symlink())
        self.assertFalse((skill_link / OLD_MARKER_FILENAME).exists())
        manifest = json.loads((target.skill_root / SKILL_MANIFEST_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual("symlink", manifest["skills"][0]["projection_mode"])

    def test_install_preserves_existing_path_without_force_and_force_replaces_it(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        existing = target.skill_root / "isomer-op-entrypoint"
        existing.mkdir(parents=True)
        (existing / "SKILL.md").write_text("user-owned\n", encoding="utf-8")

        preserved = install_system_skills(target, selection)

        self.assertTrue(preserved.ok)
        self.assertFalse(preserved.mutated)
        self.assertEqual(["isomer-op-entrypoint"], [item.name for item in preserved.preserved_existing])
        self.assertEqual("user-owned\n", (existing / "SKILL.md").read_text(encoding="utf-8"))
        self.assertFalse((target.skill_root / SKILL_MANIFEST_FILENAME).exists())

        replaced = install_system_skills(target, selection, force=True)

        self.assertTrue(replaced.mutated)
        self.assertEqual(["isomer-op-entrypoint"], [item.name for item in replaced.replaced])
        self.assertNotEqual("user-owned\n", (existing / "SKILL.md").read_text(encoding="utf-8"))
        self.assertTrue((target.skill_root / SKILL_MANIFEST_FILENAME).is_file())

    def test_force_switches_copy_and_symlink_projection_modes(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        install_system_skills(target, selection)

        to_symlink = install_system_skills(target, selection, projection_mode="symlink", force=True)

        skill_path = target.skill_root / "isomer-op-entrypoint"
        self.assertEqual(["isomer-op-entrypoint"], [item.name for item in to_symlink.replaced])
        self.assertTrue(skill_path.is_symlink())

        to_copy = install_system_skills(target, selection, projection_mode="copy", force=True)

        self.assertEqual(["isomer-op-entrypoint"], [item.name for item in to_copy.replaced])
        self.assertTrue(skill_path.is_dir())
        self.assertFalse(skill_path.is_symlink())

    def test_uninstall_removes_named_projection_and_updates_manifest(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        install_system_skills(target, selection)

        result = uninstall_system_skills(target, selection)

        self.assertEqual(["isomer-op-entrypoint"], [record.name for record in result.removed])
        self.assertFalse((target.skill_root / "isomer-op-entrypoint").exists())
        manifest = json.loads((target.skill_root / SKILL_MANIFEST_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual([], manifest["skills"])

    def test_status_reports_invalid_path_and_unreadable_manifest(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        target.skill_root.mkdir(parents=True)
        (target.skill_root / "isomer-op-entrypoint").write_text("not a directory\n", encoding="utf-8")
        (target.skill_root / SKILL_MANIFEST_FILENAME).write_text("{broken\n", encoding="utf-8")

        status = inspect_system_skills(target, selection)

        self.assertEqual(["isomer-op-entrypoint"], [item.name for item in status.invalid_projections])
        self.assertEqual({"ISOSKILL001", "ISOSKILL002"}, {diagnostic.code for diagnostic in status.diagnostics})

    def test_upgrade_refreshes_selected_and_removes_manifest_tracked_stale_paths(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        both = resolve_system_skill_selection(
            skills=("isomer-op-entrypoint", "isomer-op-gui-mgr"),
            default_core=False,
        )
        selected = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        install_system_skills(target, both)
        untracked = target.skill_root / "user-skill"
        untracked.mkdir()

        result = upgrade_system_skills(target, selected)

        self.assertEqual(["isomer-op-entrypoint"], [item.name for item in result.refreshed])
        self.assertEqual(["isomer-op-gui-mgr"], [item.name for item in result.stale_removed])
        self.assertTrue((target.skill_root / "isomer-op-entrypoint").is_dir())
        self.assertFalse((target.skill_root / "isomer-op-gui-mgr").exists())
        self.assertTrue(untracked.exists())
        manifest = json.loads((target.skill_root / SKILL_MANIFEST_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual(["isomer-op-entrypoint"], [item["name"] for item in manifest["skills"]])

    def test_upgrade_preserves_recorded_mode_and_honors_override(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", home=root / "skills")[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        install_system_skills(target, selection, projection_mode="symlink")

        preserved = upgrade_system_skills(target, selection)

        skill_path = target.skill_root / "isomer-op-entrypoint"
        self.assertTrue(skill_path.is_symlink())
        self.assertEqual("symlink", preserved.refreshed[0].projection_mode)

        overridden = upgrade_system_skills(target, selection, projection_mode="copy")

        self.assertTrue(skill_path.is_dir())
        self.assertFalse(skill_path.is_symlink())
        self.assertEqual("copy", overridden.refreshed[0].projection_mode)


if __name__ == "__main__":
    unittest.main()
