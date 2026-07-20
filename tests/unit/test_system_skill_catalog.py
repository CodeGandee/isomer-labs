from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import re
import shutil
import tempfile
import unittest

import tomlkit

from isomer_labs.skills.system_assets import (
    SystemSkillAssetError,
    iter_system_skill_callback_insertion_points,
    load_system_skill_manifest,
    lookup_system_skill_capability,
    lookup_system_skill_pack,
    materialize_system_skill_private_projection,
    normalize_system_skill_identity,
    parse_system_skill_manifest,
    resolve_system_skill_binding_projection,
    resolve_system_skill_dependency_closure,
    resolve_system_skill_private_projection,
    system_skills_root,
    system_skill_catalog,
)


FIXTURE_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "system_skills"


class SystemSkillCatalogTests(unittest.TestCase):
    def test_v4_catalog_declares_public_pairs_and_protected_members(self) -> None:
        catalog = system_skill_catalog()

        self.assertEqual("isomer-skillset-manifest.v4", catalog.schema_version)
        self.assertEqual((19, 21, 13), tuple(len(pack.protected_members) for pack in catalog.packs))
        self.assertEqual(53, len(catalog.capabilities))
        for pack in catalog.packs:
            self.assertEqual(("welcome", "entrypoint"), tuple(public.role for public in pack.public_skills))
            self.assertEqual(pack.entry_skill, pack.entrypoint.name)
            self.assertTrue(pack.welcome.name.endswith("-welcome"))  # type: ignore[union-attr]
            self.assertEqual((), pack.welcome.callback_insertion_points)  # type: ignore[union-attr]
            for capability in catalog.capabilities:
                if capability.pack_id != pack.pack_id:
                    continue
                self.assertEqual(
                    f"{pack.source_path}/subskills/{capability.logical_id}",
                    capability.source_path,
                )
                self.assertEqual(
                    f"{pack.entry_skill}->{capability.member_name}",
                    capability.invocation_designator,
                )

    def test_catalog_lookup_keeps_identity_layers_separate(self) -> None:
        pack = lookup_system_skill_pack("isomer-kaoju-pipeline")
        self.assertEqual("kaoju", pack.pack_id)
        self.assertEqual("isomer-ext-kaoju-entrypoint", pack.entry_skill)
        self.assertEqual(("pack", "isomer-ext-kaoju-entrypoint", True), normalize_system_skill_identity("isomer-kaoju-pipeline"))

        by_logical = lookup_system_skill_capability("isomer-kaoju-trial")
        by_member = lookup_system_skill_capability("trial", pack_id="kaoju")
        by_invocation = lookup_system_skill_capability("isomer-ext-kaoju-entrypoint->trial")
        self.assertEqual(by_logical, by_member)
        self.assertEqual(by_logical, by_invocation)
        self.assertEqual("isomer-kaoju-trial", by_logical.logical_id)
        self.assertEqual("trial", by_logical.member_name)

    def test_dependency_closure_is_deterministic_and_cross_pack(self) -> None:
        first = resolve_system_skill_dependency_closure(("isomer-kaoju-trial", "isomer-kaoju-write"))
        second = resolve_system_skill_dependency_closure(("isomer-kaoju-trial", "isomer-kaoju-write"))
        self.assertEqual(first, second)
        logical_ids = tuple(capability.logical_id for capability in first)
        self.assertLess(logical_ids.index("isomer-kaoju-shared"), logical_ids.index("isomer-kaoju-trial"))
        self.assertLess(logical_ids.index("isomer-srv-topic-env-setup"), logical_ids.index("isomer-kaoju-trial"))
        self.assertIn("isomer-research-idea-recording", logical_ids)

        projections = resolve_system_skill_private_projection(("isomer-kaoju-trial",))
        self.assertEqual(tuple(item.logical_id for item in projections), logical_ids[:-1])
        trial = projections[-1]
        self.assertEqual("kaoju", trial.pack_id)
        self.assertEqual("isomer-ext-kaoju-entrypoint", trial.public_skill)
        self.assertEqual("isomer-kaoju-trial", trial.projected_path)
        self.assertIn("/subskills/isomer-kaoju-trial", trial.source_path)

    def test_private_projection_is_flat_self_contained_and_dependency_closed(self) -> None:
        projections = resolve_system_skill_private_projection(("isomer-kaoju-trial",))
        projected_ids = {projection.logical_id for projection in projections}
        packaged_root = Path(str(system_skills_root()))
        link_re = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
        root_relative_prefixes = ("assets/", "commands/", "references/", "scripts/", "templates/")

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            for projection in projections:
                shutil.copytree(packaged_root / projection.source_path, target / projection.projected_path)

            self.assertEqual(projected_ids, {path.name for path in target.iterdir()})
            for projection in projections:
                bundle = target / projection.projected_path
                self.assertTrue((bundle / "SKILL.md").is_file())
                self.assertTrue((bundle / "agents" / "openai.yaml").is_file())
                self.assertTrue(set(projection.dependencies).issubset(projected_ids))
                self.assertFalse(any(path.is_symlink() for path in bundle.rglob("*")))
                for page in bundle.rglob("*.md"):
                    if any(part in {"org", "migrate", "templates"} for part in page.relative_to(bundle).parts):
                        continue
                    for match in link_re.finditer(page.read_text(encoding="utf-8")):
                        destination = match.group(1).split()[0].strip("<>").split("#", 1)[0]
                        if not destination or "://" in destination:
                            continue
                        resolved = (
                            (bundle / destination).resolve()
                            if destination.startswith(root_relative_prefixes)
                            else (page.parent / destination).resolve()
                        )
                        self.assertTrue(
                            resolved.is_relative_to(bundle.resolve()),
                            f"{page.relative_to(bundle)} escapes its private projection through {destination}",
                        )

    def test_binding_projection_resolves_logical_ids_without_persisting_pack_layout(self) -> None:
        projections = resolve_system_skill_binding_projection(("isomer-kaoju-trial",))
        self.assertEqual("isomer-kaoju-trial", projections[-1].logical_id)
        self.assertEqual("isomer-kaoju-trial", projections[-1].projected_path)
        self.assertNotEqual(projections[-1].source_path, projections[-1].projected_path)
        with self.assertRaisesRegex(SystemSkillAssetError, "protected logical id"):
            resolve_system_skill_binding_projection(("isomer-ext-kaoju-entrypoint",))

        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "projected"
            result = materialize_system_skill_private_projection(target, ("isomer-kaoju-trial",))
            self.assertEqual(projections, result.projections)
            self.assertEqual(
                {projection.logical_id for projection in projections},
                {path.name for path in target.iterdir()},
            )
            self.assertFalse((target / "isomer-ext-kaoju-entrypoint").exists())

    def test_v2_manifest_fixture_remains_read_only_parseable(self) -> None:
        manifest = dict(tomlkit.parse((FIXTURE_ROOT / "manifest.v2.toml").read_text(encoding="utf-8")))
        catalog = parse_system_skill_manifest(manifest)
        self.assertTrue(catalog.is_legacy)
        self.assertEqual(("core", "deepsci"), tuple(group.name for group in catalog.legacy_groups))
        self.assertEqual("isomer-deepsci-pipeline", catalog.legacy_groups[1].entry_skill)
        self.assertEqual((), catalog.packs)
        self.assertEqual((), catalog.capabilities)

    def test_v3_manifest_remains_read_only_parseable(self) -> None:
        manifest = deepcopy(load_system_skill_manifest())
        manifest["schema_version"] = "isomer-skillset-manifest.v3"
        public_records = {
            record["name"]: record
            for record in manifest.pop("public_skills")
            if record["role"] == "entrypoint"
        }
        for pack in manifest["packs"]:
            entrypoint = public_records[pack["entry_skill"]]
            pack["source_path"] = entrypoint["source_path"]
            pack["public_commands"] = entrypoint["public_commands"]
            pack["legacy_aliases"] = entrypoint["legacy_aliases"]
            pack["callback_insertion_points"] = entrypoint["callback_insertion_points"]
            pack.pop("public_skills")
        catalog = parse_system_skill_manifest(manifest)
        self.assertEqual("isomer-skillset-manifest.v3", catalog.schema_version)
        self.assertEqual(("entrypoint",), tuple(public.role for public in catalog.packs[0].public_skills))

    def test_v3_allows_same_name_command_and_protected_member(self) -> None:
        catalog = parse_system_skill_manifest(load_system_skill_manifest())
        core = catalog.pack_by_id("core")
        self.assertIn("gui", core.public_commands)
        self.assertEqual("isomer-op-gui-mgr", catalog.capability_for_member("core", "gui").logical_id)

    def test_v4_rejects_invalid_public_roles_identity_path_alias_and_dependency_graph(self) -> None:
        def pack(manifest: dict[str, object], pack_id: str) -> dict[str, object]:
            return next(item for item in manifest["packs"] if item["pack_id"] == pack_id)  # type: ignore[index, union-attr]

        def public(manifest: dict[str, object], name: str) -> dict[str, object]:
            return next(item for item in manifest["public_skills"] if item["name"] == name)  # type: ignore[index, union-attr]

        def capability(manifest: dict[str, object], logical_id: str) -> dict[str, object]:
            return next(item for item in manifest["capabilities"] if item["logical_id"] == logical_id)  # type: ignore[index, union-attr]

        def remove_kaoju_welcome(manifest: dict[str, object]) -> None:
            manifest["public_skills"] = [  # type: ignore[index]
                item
                for item in manifest["public_skills"]  # type: ignore[index, union-attr]
                if item["name"] != "isomer-ext-kaoju-welcome"
            ]

        def rename_kaoju_welcome(manifest: dict[str, object]) -> None:
            record = public(manifest, "isomer-ext-kaoju-welcome")
            record["name"] = "isomer-ext-survey-welcome"
            record["source_path"] = "research-paradigm/kaoju/isomer-ext-survey-welcome"
            pack(manifest, "kaoju")["public_skills"] = [
                "isomer-ext-survey-welcome",
                "isomer-ext-kaoju-entrypoint",
            ]

        mutations = (
            (
                "duplicate pack",
                lambda manifest: pack(manifest, "deepsci").__setitem__("pack_id", "core"),
                "Duplicate pack ids",
            ),
            (
                "invalid extension entrypoint",
                lambda manifest: pack(manifest, "kaoju").__setitem__("entry_skill", "isomer-kaoju-entrypoint"),
                "entry_skill must resolve to its entrypoint-role record",
            ),
            (
                "missing welcome role",
                remove_kaoju_welcome,
                "exactly one welcome and one entrypoint",
            ),
            (
                "duplicate entrypoint role",
                lambda manifest: public(manifest, "isomer-ext-kaoju-welcome").__setitem__("role", "entrypoint"),
                "exactly one welcome and one entrypoint",
            ),
            (
                "invalid extension welcome name",
                rename_kaoju_welcome,
                "welcome skill must be isomer-ext-kaoju-welcome",
            ),
            (
                "public identity collision",
                lambda manifest: public(manifest, "isomer-ext-kaoju-welcome").__setitem__(
                    "legacy_aliases", ["isomer-op-welcome"]
                ),
                "identity or alias conflict",
            ),
            (
                "escaped path",
                lambda manifest: capability(manifest, "isomer-kaoju-trial").__setitem__(
                    "source_path", "../isomer-kaoju-trial"
                ),
                "safe relative path",
            ),
            (
                "callable protected member",
                lambda manifest: capability(manifest, "isomer-kaoju-trial").__setitem__(
                    "invocation_designator", "isomer-ext-kaoju-entrypoint->trial()"
                ),
                "bare canonical path",
            ),
            (
                "alias conflict",
                lambda manifest: public(manifest, "isomer-ext-kaoju-entrypoint").__setitem__(
                    "legacy_aliases", ["isomer-kaoju-trial"]
                ),
                "identity or alias conflict",
            ),
            (
                "unknown dependency",
                lambda manifest: capability(manifest, "isomer-kaoju-trial").__setitem__(
                    "dependencies", ["isomer-kaoju-missing"]
                ),
                "unknown dependency",
            ),
            (
                "dependency cycle",
                lambda manifest: capability(manifest, "isomer-kaoju-shared").__setitem__(
                    "dependencies", ["isomer-kaoju-trial"]
                ),
                "dependency cycle",
            ),
        )
        for label, mutate, diagnostic in mutations:
            with self.subTest(label=label):
                manifest = deepcopy(load_system_skill_manifest())
                mutate(manifest)
                with self.assertRaisesRegex(SystemSkillAssetError, diagnostic):
                    parse_system_skill_manifest(manifest)

    def test_callback_discovery_reports_pack_member_path_and_invocation(self) -> None:
        points = iter_system_skill_callback_insertion_points(
            include_core=False,
            extension_ids=("kaoju",),
            skill="isomer-kaoju-trial",
            stage="begin",
        )
        self.assertEqual(1, len(points))
        point = points[0]
        self.assertEqual("kaoju", point.pack_id)
        self.assertEqual("isomer-ext-kaoju-entrypoint", point.public_skill)
        self.assertEqual("trial", point.member_name)
        self.assertEqual("isomer-ext-kaoju-entrypoint->trial", point.invocation_designator)
        self.assertTrue(point.skill_path.endswith("/subskills/isomer-kaoju-trial"))


if __name__ == "__main__":
    unittest.main()
