from __future__ import annotations

import hashlib
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
        self.assertEqual("0.6.0", content.resource_version)
        self.assertEqual("0.6.0", latex.resource_version)
        self.assertEqual(
            "sha256:6fcba33cc73a4b7a90953477714200ff375a70ca65d1be197d2bb5c4bda4ce79",
            latex.tree_digest,
        )
        self.assertTrue((content.root / str(content.authored_metadata["entrypoint"])).is_file())
        self.assertTrue((latex.root / str(latex.authored_metadata["entrypoint"])).is_file())
        self.assertEqual("template.tex", latex.authored_metadata["entrypoint"])
        self.assertEqual(
            {
                "IEEEtran.cls",
                "bare_jrnl_new_sample4.tex",
                "fig1.png",
                "metadata.json",
                "template.tex",
            },
            {path.name for path in latex.root.iterdir() if path.is_file()},
        )
        self.assertEqual(
            latex.authored_metadata,
            json.loads((latex.root / "metadata.json").read_text(encoding="utf-8")),
        )
        self.assertEqual(
            "b0eb3567b81aec7fe98144a3ad283eeac2d31035bb19e0d9dcba7da190f18d9d",
            hashlib.sha256((latex.root / "IEEEtran.cls").read_bytes()).hexdigest(),
        )
        entrypoint = (latex.root / "template.tex").read_text(encoding="utf-8")
        self.assertIn("\\documentclass[lettersize,journal]{IEEEtran}", entrypoint)
        self.assertEqual(1, entrypoint.count("% ISOMER_BODY"))
        extensions = latex.authored_metadata["extensions"]
        self.assertIsInstance(extensions, dict)
        assert isinstance(extensions, dict)
        latex_contract = extensions["latex"]
        self.assertEqual("marker", latex_contract["composition_mode"])
        self.assertEqual("% ISOMER_BODY", latex_contract["marker"])
        self.assertEqual("ieee-transactions", latex_contract["venue"])
        self.assertIn("LaTeX Project Public License 1.3", latex_contract["license_posture"])
        self.assertEqual(
            "6c315c3b6729bd7b96a6a0e7d3bb6342023413a4cd4d113fb4a193019af1c603",
            latex_contract["source_provenance"]["archive_sha256"],
        )

    def test_installed_package_resource_is_available_without_repository_lookup(self) -> None:
        root = packaged_template_root()
        self.assertIn("isomer-kaoju-write/assets/defaults/templates", root.as_posix())
        self.assertTrue((root / "manifest.json").is_file())
        self.assertTrue((root / "latex/main/IEEEtran.cls").is_file())
        self.assertTrue((root / "latex/main/fig1.png").is_file())
        self.assertNotIn("extern/", root.as_posix())
        self.assertNotIn("tmp/", root.as_posix())

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

    def test_ieee_default_rejects_missing_vendored_class_even_with_updated_digest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "templates"
            shutil.copytree(packaged_template_root(), root)
            (root / "latex/main/IEEEtran.cls").unlink()
            manifest_path = root / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["templates"]["latex"]["tree_digest"] = template_tree_digest(
                root / "latex/main"
            )
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            with patch(
                "isomer_labs.kaoju.template_defaults.packaged_template_root",
                return_value=root,
            ), self.assertRaises(KaojuServiceError) as raised:
                load_packaged_template("latex")
            self.assertEqual(
                "packaged_template_inventory_invalid",
                raised.exception.code,
            )


if __name__ == "__main__":
    unittest.main()
