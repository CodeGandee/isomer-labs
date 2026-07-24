from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

from isomer_labs.kaoju.artifacts import KaojuServiceError
from isomer_labs.kaoju.template_defaults import (
    load_packaged_template,
    packaged_template_root,
    validate_packaged_templates,
)
from isomer_labs.kaoju.template_support import template_tree_digest


class KaojuPackagedTemplateTests(unittest.TestCase):
    def test_inventory_roles_digests_and_metadata_are_checked(self) -> None:
        self.assertEqual([], validate_packaged_templates())
        content = load_packaged_template("content")
        latex = load_packaged_template("latex")
        self.assertEqual(("content", "main"), (content.template_kind.kind, content.name))
        self.assertEqual(("latex", "main"), (latex.template_kind.kind, latex.name))
        self.assertNotEqual(content.identity, latex.identity)
        self.assertNotEqual(content.tree_digest, latex.tree_digest)
        self.assertEqual(content.tree_digest, template_tree_digest(content.root))
        self.assertEqual(latex.tree_digest, template_tree_digest(latex.root))
        self.assertTrue((content.root / str(content.authored_metadata["entrypoint"])).is_file())
        self.assertTrue((latex.root / str(latex.authored_metadata["entrypoint"])).is_file())
        extensions = latex.authored_metadata["extensions"]
        self.assertIsInstance(extensions, dict)
        assert isinstance(extensions, dict)
        self.assertEqual("marker", extensions["latex"]["composition_mode"])

    def test_installed_package_resource_is_available_without_repository_lookup(self) -> None:
        root = packaged_template_root()
        self.assertIn("isomer-kaoju-write/assets/defaults/templates", root.as_posix())
        self.assertTrue((root / "manifest.json").is_file())
        self.assertNotIn("extern/", root.as_posix())

    def test_digest_drift_fails_with_stable_resource_diagnostic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "templates"
            shutil.copytree(packaged_template_root(), root)
            content = root / "content/main/paper.myst.md"
            content.write_text(content.read_text(encoding="utf-8") + "\nChanged.\n", encoding="utf-8")
            with patch(
                "isomer_labs.kaoju.template_defaults.packaged_template_root",
                return_value=root,
            ), self.assertRaises(KaojuServiceError) as raised:
                load_packaged_template("content")
            self.assertEqual("packaged_template_digest_mismatch", raised.exception.code)

    def test_inventory_rejects_extra_role_without_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "templates"
            shutil.copytree(packaged_template_root(), root)
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["templates"]["other"] = manifest["templates"]["content"]
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with patch(
                "isomer_labs.kaoju.template_defaults.packaged_template_root",
                return_value=root,
            ), self.assertRaises(KaojuServiceError) as raised:
                load_packaged_template("content")
            self.assertEqual("packaged_template_inventory_invalid", raised.exception.code)


if __name__ == "__main__":
    unittest.main()
