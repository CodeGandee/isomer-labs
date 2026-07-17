from __future__ import annotations

import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

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

    def test_project_target_roots_are_deterministic(self) -> None:
        root = self.make_root()
        self.assertEqual(
            root / ".claude" / "skills",
            resolve_targets("claude-code", scope="project", cwd=root)[0].skill_root,
        )
        self.assertEqual(root / ".agents" / "skills", resolve_targets("codex", scope="project", cwd=root)[0].skill_root)
        self.assertEqual(
            root / ".kimi-code" / "skills",
            resolve_targets("kimi-code", scope="project", cwd=root)[0].skill_root,
        )
        self.assertEqual(
            root / ".agents" / "skills",
            resolve_targets("generic", scope="project", cwd=root)[0].skill_root,
        )

    def test_user_target_roots_honor_environment_overrides_and_fallbacks(self) -> None:
        root = self.make_root()
        user_home = root / "user-home"
        claude_home = root / "claude-home"
        codex_home = root / "codex-home"
        kimi_home = user_home / "kimi-home"
        env = {
            "HOME": str(user_home),
            "CLAUDE_CONFIG_DIR": str(claude_home),
            "CODEX_HOME": str(codex_home),
            "KIMI_CODE_HOME": "~/kimi-home",
        }

        self.assertEqual(
            claude_home / "skills",
            resolve_targets("claude-code", scope="user", cwd=root, env=env)[0].skill_root,
        )
        self.assertEqual(
            codex_home / "skills",
            resolve_targets("codex", scope="user", cwd=root, env=env)[0].skill_root,
        )
        self.assertEqual(
            kimi_home / "skills",
            resolve_targets("kimi-code", scope="user", cwd=root, env=env)[0].skill_root,
        )
        self.assertEqual(
            user_home / ".agents" / "skills",
            resolve_targets("generic", scope="user", cwd=root, env=env)[0].skill_root,
        )

        fallback_env = {"HOME": str(user_home), "CLAUDE_CONFIG_DIR": "", "CODEX_HOME": "", "KIMI_CODE_HOME": ""}
        self.assertEqual(
            user_home / ".claude" / "skills",
            resolve_targets("claude-code", scope="user", env=fallback_env)[0].skill_root,
        )
        self.assertEqual(
            user_home / ".codex" / "skills",
            resolve_targets("codex", scope="user", env=fallback_env)[0].skill_root,
        )
        self.assertEqual(
            user_home / ".kimi-code" / "skills",
            resolve_targets("kimi-code", scope="user", env=fallback_env)[0].skill_root,
        )

    def test_target_all_deduplicates_shared_project_root(self) -> None:
        root = self.make_root()
        targets = resolve_targets("all", scope="project", cwd=root)

        self.assertEqual(
            [root / ".claude" / "skills", root / ".agents" / "skills", root / ".kimi-code" / "skills"],
            [target.skill_root for target in targets],
        )
        shared = targets[1]
        self.assertEqual("all", shared.target)
        self.assertEqual("project", shared.scope)
        self.assertEqual(["codex", "generic"], [binding.target for binding in shared.bindings])

    def test_project_scope_uses_exact_nested_cwd(self) -> None:
        root = self.make_root()
        nested = root / "packages" / "service"
        nested.mkdir(parents=True)

        target = resolve_targets("kimi-code", scope="project", cwd=nested)[0]

        self.assertEqual(nested / ".kimi-code" / "skills", target.skill_root)

    def test_selection_defaults_to_core_and_extension_adds_core(self) -> None:
        core = resolve_system_skill_selection()
        self.assertIn("core", core.selected_groups)
        self.assertIn("isomer-op-entrypoint", [skill.name for skill in core.skills])
        self.assertIn("isomer-op-gui-mgr", [skill.name for skill in core.skills])
        self.assertIn("isomer-op-system-skill-mgr", [skill.name for skill in core.skills])
        self.assertIn("isomer-research-idea-recording", [skill.name for skill in core.skills])
        self.assertIn("isomer-research-operation-set-recording", [skill.name for skill in core.skills])
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
        self.assertIn("isomer-research-idea-recording", [skill.name for skill in kaoju.skills])
        self.assertIn("isomer-research-operation-set-recording", [skill.name for skill in kaoju.skills])
        self.assertNotIn("isomer-deepsci-pipeline", [skill.name for skill in kaoju.skills])

    def test_kaoju_extension_install_status_upgrade_and_uninstall(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", scope="project", cwd=root)[0]
        selection = resolve_system_skill_selection(extensions=("kaoju",))

        installed = install_system_skills(target, selection)

        self.assertTrue(installed.ok)
        kaoju_names = sorted(record.name for record in installed.installed if record.name.startswith("isomer-kaoju-"))
        self.assertEqual(14, len(kaoju_names))
        self.assertTrue((target.skill_root / "isomer-kaoju-pipeline" / "commands" / "comparative-pass.md").is_file())
        self.assertTrue((target.skill_root / "isomer-kaoju-shared" / "references" / "source-identity.md").is_file())
        self.assertTrue((target.skill_root / "isomer-kaoju-shared" / "references" / "artifact-semantics.md").is_file())
        self.assertTrue((target.skill_root / "isomer-kaoju-frame" / "artifact-bindings.md").is_file())
        self.assertTrue((target.skill_root / "isomer-research-idea-recording" / "references" / "recording-contract.md").is_file())
        self.assertTrue((target.skill_root / "isomer-research-operation-set-recording" / "references" / "manifest-contract.md").is_file())
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
        target = resolve_targets("generic", scope="project", cwd=root)[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)

        result = install_system_skills(target, selection)

        self.assertTrue(result.ok)
        self.assertTrue(result.mutated)
        skill_dir = target.skill_root / "isomer-op-entrypoint"
        self.assertTrue((skill_dir / "SKILL.md").is_file())
        self.assertFalse((skill_dir / OLD_MARKER_FILENAME).exists())
        self.assertFalse((target.skill_root / "operator" / "isomer-op-entrypoint").exists())
        manifest = json.loads((target.skill_root / SKILL_MANIFEST_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual("isomer-labs-skill-manifest.v3", manifest["schema_version"])
        self.assertNotIn("target", manifest)
        self.assertEqual([{"scope": "project", "target": "generic"}], manifest["bindings"])
        self.assertEqual(["isomer-op-entrypoint"], [item["name"] for item in manifest["skills"]])
        self.assertEqual("operator/isomer-op-entrypoint", manifest["skills"][0]["source_path"])
        self.assertEqual(selection.skills[0].skill_version, manifest["skills"][0]["skill_version"])

        status = inspect_system_skills(target, selection)
        self.assertEqual(["isomer-op-entrypoint"], [record.name for record in status.installed])
        self.assertEqual((), status.missing)
        self.assertIsNotNone(status.manifest)
        self.assertEqual("current", status.installed[0].compatibility_status)
        self.assertTrue(status.installed[0].installation_verified)
        self.assertEqual("project", result.to_json()["scope"])
        self.assertEqual([{"target": "generic", "scope": "project"}], result.to_json()["bindings"])

    def test_shared_root_is_projected_once_and_records_all_bindings(self) -> None:
        root = self.make_root()
        target = resolve_targets("all", scope="project", cwd=root)[1]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)

        result = install_system_skills(target, selection)

        self.assertEqual(["isomer-op-entrypoint"], [item.name for item in result.installed])
        manifest = json.loads((target.skill_root / SKILL_MANIFEST_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual(
            [{"scope": "project", "target": "codex"}, {"scope": "project", "target": "generic"}],
            manifest["bindings"],
        )

    def test_later_mutation_merges_binding_for_same_root(self) -> None:
        root = self.make_root()
        codex = resolve_targets("codex", scope="project", cwd=root)[0]
        generic = resolve_targets("generic", scope="project", cwd=root)[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        install_system_skills(codex, selection)

        upgrade_system_skills(generic, selection)

        manifest = json.loads((generic.skill_root / SKILL_MANIFEST_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual(
            [{"scope": "project", "target": "codex"}, {"scope": "project", "target": "generic"}],
            manifest["bindings"],
        )

    def test_v2_receipt_has_unknown_scope_until_mutation_migrates_it(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", scope="project", cwd=root)[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        install_system_skills(target, selection)
        receipt_path = target.skill_root / SKILL_MANIFEST_FILENAME
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["schema_version"] = "isomer-labs-skill-manifest.v2"
        receipt["target"] = "generic"
        receipt.pop("bindings")
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")

        status = inspect_system_skills(target, selection)

        self.assertIsNotNone(status.manifest)
        assert status.manifest is not None
        self.assertEqual("isomer-labs-skill-manifest.v2", status.manifest.schema_version)
        self.assertEqual((), status.manifest.bindings)
        self.assertEqual("generic", status.manifest.legacy_target)

        upgrade_system_skills(target, selection)

        migrated = json.loads(receipt_path.read_text(encoding="utf-8"))
        self.assertEqual("isomer-labs-skill-manifest.v3", migrated["schema_version"])
        self.assertNotIn("target", migrated)
        self.assertEqual([{"scope": "project", "target": "generic"}], migrated["bindings"])

    def test_legacy_receipt_is_read_and_classified_unversioned(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", scope="project", cwd=root)[0]
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
        target = resolve_targets("generic", scope="project", cwd=root)[0]
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
        target = resolve_targets("generic", scope="project", cwd=root)[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)

        result = install_system_skills(target, selection, projection_mode="symlink")

        self.assertTrue(result.ok)
        skill_link = target.skill_root / "isomer-op-entrypoint"
        self.assertTrue(skill_link.is_symlink())
        self.assertFalse((skill_link / OLD_MARKER_FILENAME).exists())
        manifest = json.loads((target.skill_root / SKILL_MANIFEST_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual("symlink", manifest["skills"][0]["projection_mode"])

    def test_symlink_projection_exposes_system_skill_manager_scope_guidance(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", scope="project", cwd=root)[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-system-skill-mgr",), default_core=False)

        result = install_system_skills(target, selection, projection_mode="symlink")

        self.assertTrue(result.ok)
        skill_link = target.skill_root / "isomer-op-system-skill-mgr"
        self.assertTrue(skill_link.is_symlink())
        self.assertIn(
            "Direct low-level install defaults to project scope when `--scope` is omitted.",
            (skill_link / "SKILL.md").read_text(encoding="utf-8"),
        )

    def test_install_preserves_existing_path_without_force_and_force_replaces_it(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", scope="project", cwd=root)[0]
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
        target = resolve_targets("generic", scope="project", cwd=root)[0]
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
        target = resolve_targets("generic", scope="project", cwd=root)[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        install_system_skills(target, selection)

        result = uninstall_system_skills(target, selection)

        self.assertEqual(["isomer-op-entrypoint"], [record.name for record in result.removed])
        self.assertFalse((target.skill_root / "isomer-op-entrypoint").exists())
        manifest = json.loads((target.skill_root / SKILL_MANIFEST_FILENAME).read_text(encoding="utf-8"))
        self.assertEqual([], manifest["skills"])

    def test_status_reports_invalid_path_and_unreadable_manifest(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", scope="project", cwd=root)[0]
        selection = resolve_system_skill_selection(skills=("isomer-op-entrypoint",), default_core=False)
        target.skill_root.mkdir(parents=True)
        (target.skill_root / "isomer-op-entrypoint").write_text("not a directory\n", encoding="utf-8")
        (target.skill_root / SKILL_MANIFEST_FILENAME).write_text("{broken\n", encoding="utf-8")

        status = inspect_system_skills(target, selection)

        self.assertEqual(["isomer-op-entrypoint"], [item.name for item in status.invalid_projections])
        self.assertEqual({"ISOSKILL001", "ISOSKILL002"}, {diagnostic.code for diagnostic in status.diagnostics})

    def test_upgrade_refreshes_selected_and_removes_manifest_tracked_stale_paths(self) -> None:
        root = self.make_root()
        target = resolve_targets("generic", scope="project", cwd=root)[0]
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
        target = resolve_targets("generic", scope="project", cwd=root)[0]
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
