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
    install_system_skills,
    resolve_system_skill_selection,
    resolve_targets,
)


REPO_ROOT = Path(__file__).resolve().parents[2]


class SystemSkillInspectionTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def install_extension(self, root: Path, extension_id: str = "kaoju") -> None:
        target = resolve_targets("generic", home=root)[0]
        selection = resolve_system_skill_selection(extensions=(extension_id,))
        install_system_skills(target, selection)

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
        self.assertEqual("managed_legacy_receipt", legacy["evidence_basis"])

        receipt["schema_version"] = "isomer-labs-skill-manifest.v99"
        receipt_path.write_text(json.dumps(receipt), encoding="utf-8")
        future = inspect_explicit_system_skill_root(root, extension_id="kaoju").to_json()
        self.assertEqual("unsupported_schema", future["receipt"]["status"])
        self.assertEqual("unmanaged_complete", future["extensions"][0]["coverage_status"])

        receipt_path.write_text("{broken\n", encoding="utf-8")
        malformed = inspect_explicit_system_skill_root(root, extension_id="kaoju").to_json()
        self.assertEqual("malformed_receipt", malformed["receipt"]["status"])
        self.assertEqual("unmanaged_complete", malformed["extensions"][0]["coverage_status"])

    def test_projection_diagnostics_cover_broken_symlink_file_and_unmanaged_directory(self) -> None:
        root = self.make_root() / "skills"
        target = resolve_targets("generic", home=root)[0]
        selection = resolve_system_skill_selection(
            skills=("isomer-kaoju-pipeline", "isomer-kaoju-shared", "isomer-kaoju-audit"),
            default_core=False,
        )
        install_system_skills(target, selection, projection_mode="symlink")
        broken = root / "isomer-kaoju-audit"
        broken.unlink()
        broken.symlink_to(root / "missing-target", target_is_directory=True)
        invalid_file = root / "isomer-kaoju-shared"
        invalid_file.unlink()
        invalid_file.write_text("not a directory\n", encoding="utf-8")
        unmanaged = root / "isomer-kaoju-discover"
        unmanaged.mkdir()
        (unmanaged / "SKILL.md").write_text("---\nname: isomer-kaoju-discover\n---\n", encoding="utf-8")

        payload = inspect_explicit_system_skill_root(root, extension_id="kaoju").to_json()
        rows = {row["name"]: row for row in payload["skills"]}

        self.assertEqual("broken_symlink", rows["isomer-kaoju-audit"]["projection_status"])
        self.assertEqual("file", rows["isomer-kaoju-shared"]["projection_status"])
        self.assertEqual("unmanaged", rows["isomer-kaoju-discover"]["projection_status"])
        self.assertEqual("partial", payload["extensions"][0]["coverage_status"])

    def test_filters_and_payload_order_are_deterministic(self) -> None:
        root = self.make_root() / "skills"
        first = inspect_explicit_system_skill_root(root, category="extensions", group_name="kaoju").to_json()
        second = inspect_explicit_system_skill_root(root, category="extensions", group_name="kaoju").to_json()
        self.assertEqual(first, second)
        self.assertEqual(["kaoju"], [row["name"] for row in first["groups"]])
        with self.assertRaisesRegex(SystemSkillInspectionError, "Unknown packaged system-skill group"):
            inspect_explicit_system_skill_root(root, group_name="unknown")

    def test_live_inventory_classifies_complete_partial_and_unknown_skills(self) -> None:
        kaoju_names = [
            record.name
            for record in resolve_system_skill_selection(extensions=("kaoju",), default_core=False).skills
        ]
        entries = [InventorySkillEntry(name=name) for name in kaoju_names]
        entries.append(InventorySkillEntry(name="third-party-skill", path="/ambient/third-party-skill"))

        complete = classify_system_skill_inventory(entries).to_json()
        kaoju = next(row for row in complete["extensions"] if row["extension_id"] == "kaoju")
        self.assertEqual("complete", kaoju["coverage_status"])
        self.assertEqual("live_inventory", kaoju["evidence_basis"])
        self.assertEqual(["third-party-skill"], [row["name"] for row in complete["unmatched_skills"]])

        partial = classify_system_skill_inventory(entries[:-2]).to_json()
        kaoju = next(row for row in partial["extensions"] if row["extension_id"] == "kaoju")
        self.assertEqual("partial", kaoju["coverage_status"])
        self.assertTrue(kaoju["missing_members"])

    def test_structured_inventory_schema_and_cli_contract(self) -> None:
        document = json.dumps(
            {
                "schema_version": INVENTORY_INPUT_SCHEMA,
                "skills": [
                    "isomer-kaoju-pipeline",
                    {"name": "ambient-skill", "path": "/host/ambient-skill"},
                ],
            }
        )
        entries = parse_inventory_document(document)
        self.assertEqual(("isomer-kaoju-pipeline", "ambient-skill"), tuple(entry.name for entry in entries))
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
        self.assertEqual("isomer-internal-system-skill-inspection.v1", payload["internal_schema_version"])
        self.assertEqual("live_inventory", payload["inspection_kind"])

    def test_operator_workflows_preserve_trust_order_opt_out_and_additive_reconciliation(self) -> None:
        operator_root = REPO_ROOT / "skillset" / "operator"
        manager = (operator_root / "isomer-op-system-skill-mgr" / "SKILL.md").read_text(encoding="utf-8")
        project_init = (
            operator_root / "isomer-op-project-mgr" / "references" / "init-project.md"
        ).read_text(encoding="utf-8")
        entrypoint = (operator_root / "isomer-op-entrypoint" / "SKILL.md").read_text(encoding="utf-8")

        self.assertLess(manager.index("Project declaration"), manager.index("Managed explicit root"))
        self.assertLess(manager.index("Managed explicit root"), manager.index("Live inventory"))
        self.assertIn("Registration is additive and idempotent", manager)
        self.assertIn("Never call `forget`", manager)
        self.assertIn("host refresh is required", manager)
        self.assertIn("unless the user explicitly opts out", project_init.lower())
        self.assertIn("distinct partial outcome", project_init)
        self.assertIn("isomer-op-system-skill-mgr", entrypoint)
        self.assertNotIn("system-extensions detect --target", entrypoint)


if __name__ == "__main__":
    unittest.main()
