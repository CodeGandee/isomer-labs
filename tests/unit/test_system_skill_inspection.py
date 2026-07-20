from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from click.testing import CliRunner

from isomer_labs import cli
from isomer_labs.skills.inspection import (
    INVENTORY_INPUT_SCHEMA,
    InventorySkillEntry,
    SystemSkillInspectionError,
    classify_system_skill_inventory,
    inspect_explicit_system_skill_root,
    parse_inventory_document,
)
from isomer_labs.skills.installer import (
    SKILL_MANIFEST_FILENAME,
    SystemSkillTarget,
    SystemSkillTargetBinding,
    install_system_skills,
    resolve_system_skill_selection,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


class SystemSkillInspectionTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def install_extension(self, root: Path, extension_id: str = "kaoju") -> None:
        target = self.make_target(root)
        selection = resolve_system_skill_selection(extensions=(extension_id,))
        install_system_skills(target, selection)

    def make_target(self, root: Path) -> SystemSkillTarget:
        binding = SystemSkillTargetBinding(target="generic", scope="project")
        return SystemSkillTarget(target="generic", scope="project", skill_root=root, bindings=(binding,))

    def test_explicit_root_reports_managed_complete_extension(self) -> None:
        root = self.make_root() / "skills"
        self.install_extension(root)

        result = inspect_explicit_system_skill_root(root, category="extensions", extension_id="kaoju")
        payload = result.to_json()

        self.assertTrue(payload["ok"])
        self.assertFalse(payload["mutated"])
        self.assertEqual("managed_receipt", payload["evidence_basis"])
        self.assertEqual("current", payload["receipt"]["status"])
        self.assertEqual("complete", payload["extensions"][0]["coverage_status"])
        self.assertEqual("managed_receipt", payload["extensions"][0]["evidence_basis"])

    def test_absent_root_is_not_created_or_replaced_by_implicit_search(self) -> None:
        parent = self.make_root()
        installed = parent / ".agents" / "skills"
        self.install_extension(installed)
        absent = parent / "explicitly-absent"

        payload = inspect_explicit_system_skill_root(absent, extension_id="kaoju").to_json()

        self.assertEqual("absent", payload["root_status"])
        self.assertEqual("absent", payload["receipt"]["status"])
        self.assertEqual("missing", payload["extensions"][0]["coverage_status"])
        self.assertFalse(absent.exists())

    def test_legacy_future_and_malformed_receipts_are_distinguished(self) -> None:
        root = self.make_root() / "skills"
        self.install_extension(root)
        receipt_path = root / SKILL_MANIFEST_FILENAME
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        receipt["schema_version"] = "isomer-labs-skill-manifest.v1"
        for record in receipt["skills"]:
            record.pop("skill_version")
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        legacy = inspect_explicit_system_skill_root(root, extension_id="kaoju").to_json()
        self.assertEqual("legacy", legacy["receipt"]["status"])
        self.assertEqual("explicit_root_verified", legacy["evidence_basis"])
        self.assertEqual("managed_legacy_receipt", legacy["legacy_flat_paths"][0]["evidence_basis"])
        self.assertEqual("unverified", legacy["legacy_flat_paths"][0]["nested_integrity_status"])

        receipt["schema_version"] = "isomer-labs-skill-manifest.v99"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        future = inspect_explicit_system_skill_root(root, extension_id="kaoju").to_json()
        self.assertEqual("unsupported_schema", future["receipt"]["status"])
        self.assertEqual("unmanaged_complete", future["extensions"][0]["coverage_status"])

        receipt_path.write_text("{broken\n", encoding="utf-8")
        malformed = inspect_explicit_system_skill_root(root, extension_id="kaoju").to_json()
        self.assertEqual("malformed_receipt", malformed["receipt"]["status"])
        self.assertEqual("unmanaged_complete", malformed["extensions"][0]["coverage_status"])

    def test_v3_flat_receipt_reports_candidate_pack_without_nested_integrity(self) -> None:
        root = self.make_root() / "skills"
        legacy = root / "isomer-kaoju-trial"
        legacy.mkdir(parents=True)
        (legacy / "SKILL.md").write_text("---\nname: isomer-kaoju-trial\n---\n", encoding="utf-8")
        (root / SKILL_MANIFEST_FILENAME).write_text(
            json.dumps(
                {
                    "schema_version": "isomer-labs-skill-manifest.v3",
                    "bindings": [{"target": "generic", "scope": "project"}],
                    "skill_root": str(root),
                    "package_name": "isomer-labs",
                    "package_version": "0.1.0",
                    "installed_by": "isomer-cli",
                    "updated_at": "2026-07-19T00:00:00Z",
                    "skills": [
                        {
                            "name": "isomer-kaoju-trial",
                            "source_path": "research-paradigm/kaoju/isomer-kaoju-trial",
                            "projection_mode": "copy",
                            "skill_version": "0.1.0",
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )

        payload = inspect_explicit_system_skill_root(root, extension_id="kaoju").to_json()

        self.assertEqual("legacy", payload["receipt"]["status"])
        self.assertEqual("missing", payload["extensions"][0]["coverage_status"])
        row = payload["legacy_flat_paths"][0]
        self.assertEqual("isomer-kaoju-trial", row["logical_id"])
        self.assertEqual("kaoju", row["candidate_pack_id"])
        self.assertEqual("unverified", row["nested_integrity_status"])
        self.assertEqual([], payload["ambient_paths"])

    def test_projection_diagnostics_cover_broken_symlink_file_and_ambient_directory(self) -> None:
        root = self.make_root() / "skills"
        target = self.make_target(root)
        selection = resolve_system_skill_selection(groups=("core", "deepsci", "kaoju"), default_core=False)
        install_system_skills(target, selection, projection_mode="symlink")
        broken = root / "isomer-ext-kaoju-entrypoint"
        broken.unlink()
        broken.symlink_to(root / "missing-target", target_is_directory=True)
        invalid_file = root / "isomer-ext-deepsci-entrypoint"
        invalid_file.unlink()
        invalid_file.write_text("not a directory\n", encoding="utf-8")
        ambient = root / "third-party-skill"
        ambient.mkdir()

        payload = inspect_explicit_system_skill_root(root).to_json()
        rows = {row["name"]: row for row in payload["skills"]}

        self.assertEqual("broken_symlink", rows["isomer-ext-kaoju-entrypoint"]["projection_status"])
        self.assertEqual("file", rows["isomer-ext-deepsci-entrypoint"]["projection_status"])
        self.assertEqual(["third-party-skill"], [row["name"] for row in payload["ambient_paths"]])
        self.assertEqual({"partial"}, {row["coverage_status"] for row in payload["extensions"]})

    def test_current_receipt_with_missing_nested_member_is_partial(self) -> None:
        root = self.make_root() / "skills"
        self.install_extension(root)
        missing = root / "isomer-ext-kaoju-entrypoint" / "subskills" / "isomer-kaoju-audit"
        missing.rename(root.parent / "removed-isomer-kaoju-audit")

        payload = inspect_explicit_system_skill_root(root, extension_id="kaoju").to_json()
        kaoju = payload["extensions"][0]

        self.assertEqual("current", payload["receipt"]["status"])
        self.assertEqual("partial", kaoju["coverage_status"])
        self.assertEqual("incomplete", kaoju["protected_integrity_status"])
        self.assertIn("isomer-kaoju-audit", kaoju["missing_members"])
        self.assertNotEqual("managed_receipt", kaoju["evidence_basis"])

    def test_filters_and_payload_order_are_deterministic(self) -> None:
        root = self.make_root() / "skills"
        first = inspect_explicit_system_skill_root(root, category="extensions", group_name="kaoju").to_json()
        second = inspect_explicit_system_skill_root(root, category="extensions", group_name="kaoju").to_json()
        self.assertEqual(first, second)
        self.assertEqual(["kaoju"], [row["name"] for row in first["groups"]])
        with self.assertRaisesRegex(SystemSkillInspectionError, "Unknown packaged system-skill group"):
            inspect_explicit_system_skill_root(root, group_name="unknown")

    def test_live_inventory_distinguishes_entrypoint_legacy_member_and_unknown_names(self) -> None:
        entries = [
            InventorySkillEntry(name="isomer-ext-kaoju-entrypoint"),
            InventorySkillEntry(name="isomer-kaoju-trial"),
            InventorySkillEntry(name="isomer-deepsci-pipeline"),
            InventorySkillEntry(name="third-party-skill", path="/ambient/third-party-skill"),
        ]

        payload = classify_system_skill_inventory(entries).to_json()
        kaoju = next(row for row in payload["extensions"] if row["extension_id"] == "kaoju")
        deepsci = next(row for row in payload["extensions"] if row["extension_id"] == "deepsci")
        self.assertEqual("entrypoint_seen", kaoju["coverage_status"])
        self.assertEqual("unverified", kaoju["protected_integrity_status"])
        self.assertEqual(["isomer-kaoju-trial"], kaoju["observed_members"])
        self.assertEqual("legacy_observed", deepsci["coverage_status"])
        self.assertEqual(["isomer-deepsci-pipeline"], deepsci["legacy_aliases_seen"])
        self.assertEqual(["isomer-ext-kaoju-entrypoint"], [row["name"] for row in payload["entrypoint_observations"]])
        self.assertEqual(["isomer-kaoju-trial"], [row["logical_id"] for row in payload["legacy_member_observations"]])
        self.assertEqual(["third-party-skill"], [row["name"] for row in payload["unmatched_skills"]])

    def test_all_public_inventory_names_remain_entrypoint_only(self) -> None:
        payload = classify_system_skill_inventory(
            [
                InventorySkillEntry(name="isomer-op-entrypoint"),
                InventorySkillEntry(name="isomer-ext-deepsci-entrypoint"),
                InventorySkillEntry(name="isomer-ext-kaoju-entrypoint"),
            ]
        ).to_json()

        self.assertEqual(
            {"entrypoint_seen"},
            {row["coverage_status"] for row in payload["groups"]},
        )
        self.assertEqual(
            {"unverified"},
            {row["protected_integrity_status"] for row in payload["groups"]},
        )

    def test_structured_inventory_schema_and_cli_contract(self) -> None:
        document = json.dumps(
            {
                "schema_version": INVENTORY_INPUT_SCHEMA,
                "skills": [
                    "isomer-ext-kaoju-entrypoint",
                    {"name": "ambient-skill", "path": "/host/ambient-skill"},
                ],
            }
        )
        entries = parse_inventory_document(document)
        self.assertEqual(("isomer-ext-kaoju-entrypoint", "ambient-skill"), tuple(entry.name for entry in entries))
        with self.assertRaisesRegex(SystemSkillInspectionError, "Unsupported inventory schema"):
            parse_inventory_document('{"schema_version":"future","skills":[]}')

        runner = CliRunner()
        result = runner.invoke(
            cli.app,
            ["--print-json", "internals", "classify-system-skill-inventory", "--inventory-json", "-"],
            input=document,
            standalone_mode=False,
        )
        if result.exception is not None:
            raise result.exception
        payload = json.loads(result.output)
        self.assertEqual(0, int(result.return_value or 0))
        self.assertFalse(payload["mutated"])
        self.assertEqual("isomer-internal-system-skill-inspection.v2", payload["internal_schema_version"])
        self.assertEqual("live_inventory", payload["inspection_kind"])

    def test_operator_workflows_preserve_trust_order_opt_out_and_additive_reconciliation(self) -> None:
        operator_root = REPO_ROOT / "skillset" / "operator" / "isomer-op-entrypoint"
        manager = (operator_root / "subskills" / "isomer-op-system-skill-mgr" / "SKILL.md").read_text(encoding="utf-8")
        project_init = (
            operator_root / "subskills" / "isomer-op-project-mgr" / "references" / "init-project.md"
        ).read_text(encoding="utf-8")
        entrypoint = (operator_root / "SKILL.md").read_text(encoding="utf-8")
        welcome_root = operator_root / "subskills" / "isomer-op-welcome"
        welcome = "\n".join(
            path.read_text(encoding="utf-8")
            for path in sorted((welcome_root / "references").glob("*.md"))
        )

        self.assertLess(manager.index("Project declaration"), manager.index("Current v4 receipt"))
        self.assertLess(manager.index("Current v4 receipt"), manager.index("Explicit-root verification"))
        self.assertLess(manager.index("Explicit-root verification"), manager.index("Limited live inventory"))
        self.assertIn("Registration is additive and idempotent", manager)
        self.assertIn("Never call `forget`", manager)
        self.assertIn("host refresh or new session", manager)
        self.assertIn("Neither observation proves complete coverage", manager)
        self.assertIn("references/upgrade.md", manager)
        self.assertIn("unless the user explicitly opts out", project_init.lower())
        self.assertIn("distinct partial outcome", project_init)
        self.assertIn("isomer-op-entrypoint->system-skills", entrypoint)
        self.assertNotIn("system-extensions detect --target", entrypoint)
        self.assertIn("$isomer-ext-deepsci-entrypoint use <subcommand> to <task>", welcome)
        self.assertIn("$isomer-ext-kaoju-entrypoint use <subcommand> to <task>", welcome)
        self.assertNotIn("$isomer-op-system-skill-mgr", welcome)
        self.assertNotIn("$isomer-kaoju-workspace-mgr", welcome)


if __name__ == "__main__":
    unittest.main()
