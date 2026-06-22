from __future__ import annotations

import importlib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src" / "isomer_labs"

REMOVED_SHIM_FILES = {
    "houmao_cli_adapter.py",
    "houmao_manifests.py",
    "runtime_models.py",
    "runtime_store.py",
    "runtime_validation.py",
}

REMOVED_MODULE_PATHS = {
    "isomer_labs.houmao_cli_adapter",
    "isomer_labs.houmao_manifests",
    "isomer_labs.runtime_models",
    "isomer_labs.runtime_store",
    "isomer_labs.runtime_validation",
}

MODULE_SIZE_EXEMPTIONS = {
    "cli/app.py",
    "doctor.py",
    "runtime/store.py",
    "runtime/validation.py",
    "houmao/adapter.py",
    "houmao/manifests.py",
}

ALLOWED_PACKAGE_NAMES = {
    "cli",
    "houmao",
    "runtime",
    "__pycache__",
}


class SourceArchitectureTests(unittest.TestCase):
    def test_cli_is_package_backed_and_command_groups_have_modules(self) -> None:
        self.assertFalse((SRC_ROOT / "cli.py").exists())
        self.assertTrue((SRC_ROOT / "cli" / "__init__.py").is_file())
        self.assertTrue((SRC_ROOT / "cli" / "app.py").is_file())
        self.assertTrue((SRC_ROOT / "cli" / "options.py").is_file())
        self.assertTrue((SRC_ROOT / "cli" / "output.py").is_file())

        command_modules = [
            "project.py",
            "doctor.py",
            "runtime.py",
            "team_templates.py",
            "team_profiles.py",
            "team_instances/commands.py",
        ]
        for relative in command_modules:
            self.assertTrue((SRC_ROOT / "cli" / "commands" / relative).is_file(), relative)

    def test_removed_non_cli_shims_are_absent(self) -> None:
        for name in REMOVED_SHIM_FILES:
            self.assertFalse((SRC_ROOT / name).exists(), name)

    def test_canonical_package_imports_work(self) -> None:
        modules = [
            "isomer_labs.houmao.adapter",
            "isomer_labs.houmao.manifests",
            "isomer_labs.runtime.models",
            "isomer_labs.runtime.store",
            "isomer_labs.runtime.validation",
        ]
        for module_name in modules:
            self.assertIsNotNone(importlib.import_module(module_name), module_name)

    def test_repository_import_surface_uses_canonical_package_paths(self) -> None:
        scanned_roots = [REPO_ROOT / name for name in ("src", "tests", "scripts", "docs")]
        ignored_paths = {Path(__file__).resolve()}
        violations: list[str] = []
        for root in scanned_roots:
            for path in sorted(root.rglob("*")):
                if not path.is_file() or path.resolve() in ignored_paths:
                    continue
                if path.suffix not in {".py", ".md"}:
                    continue
                content = path.read_text(encoding="utf-8")
                for module_path in REMOVED_MODULE_PATHS:
                    if module_path in content:
                        relative = path.relative_to(REPO_ROOT).as_posix()
                        violations.append(f"{relative}: {module_path}")
        self.assertEqual([], violations)

    def test_large_implementation_files_are_package_scoped_or_exempt(self) -> None:
        threshold = 800
        oversized: list[str] = []
        for path in sorted(SRC_ROOT.rglob("*.py")):
            relative = path.relative_to(SRC_ROOT).as_posix()
            if relative in MODULE_SIZE_EXEMPTIONS:
                continue
            line_count = len(path.read_text(encoding="utf-8").splitlines())
            if line_count > threshold:
                oversized.append(f"{relative}:{line_count}")
        self.assertEqual([], oversized)

    def test_command_registration_does_not_return_to_cli_app_monolith(self) -> None:
        app_source = (SRC_ROOT / "cli" / "app.py").read_text(encoding="utf-8")
        self.assertNotIn("@app.command(", app_source)
        self.assertNotIn("@app.group(name=\"team-instances\"", app_source)

    def test_new_package_names_keep_expected_domain_boundaries(self) -> None:
        package_names = {
            path.name
            for path in SRC_ROOT.iterdir()
            if path.is_dir() and (path / "__init__.py").is_file()
        }
        unexpected = sorted(package_names - ALLOWED_PACKAGE_NAMES)
        self.assertEqual([], unexpected)
        self.assertFalse((SRC_ROOT / "adapter" / "__init__.py").exists())


if __name__ == "__main__":
    unittest.main()
