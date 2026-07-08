from __future__ import annotations

import importlib
import re
import tomllib
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SRC_ROOT = REPO_ROOT / "src" / "isomer_labs"
PACKAGE_ASSET_CODE_ROOTS = {
    Path("assets/system_skills"),
}

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

ROOT_FILE_ALLOWLIST = {
    "__init__.py",
    "__main__.py",
}

PACKAGE_SIZE_TRANSITIONS = {
    "cli/handlers/project.py",
    "cli/commands/project.py",
    "models/__init__.py",
    "project/doctor.py",
    "project/user_plugins.py",
    "records/store.py",
    "houmao/adapter.py",
    "houmao/manifests.py",
    "deepsci_ext/tools.py",
    "teams/instantiation.py",
    "teams/profiles.py",
    "teams/templates.py",
    "workspace/manifest.py",
    "workspace/path_resolution.py",
    "workspace/reset.py",
}

CANONICAL_RUNTIME_FILES = {
    "__init__.py",
    "records.py",
    "sqlite.py",
    "store.py",
    "validation.py",
}

CANONICAL_LARGE_RUNTIME_FILES = {
    f"runtime/{name}"
    for name in ("records.py", "sqlite.py", "store.py", "validation.py")
}

OBSOLETE_RUNTIME_FILES = {
    "adapter_handoff_validation.py",
    "adapter_handoffs.py",
    "agent_identity.py",
    "identifiers.py",
    "models.py",
    "readiness.py",
    "reset_schema.py",
    "rows.py",
    "schema.py",
    "semantic_file_locator.py",
    "serialization.py",
    "transactions.py",
    "validation_checks.py",
    "validation_utils.py",
    "workspace_layout_validation.py",
    "workspace_visibility.py",
}

REMOVED_RUNTIME_MODULE_PATHS = {
    f"isomer_labs.runtime.{Path(name).stem}"
    for name in OBSOLETE_RUNTIME_FILES
}

CANONICAL_DOMAIN_PACKAGE_FILES = {
    "artifact_formats": {
        "__init__.py",
        "models.py",
        "processing.py",
        "registry.py",
        "workspace_provider.py",
    },
    "deepsci_ext": {
        "__init__.py",
        "record_formats.py",
        "store.py",
        "tools.py",
    },
    "teams": {
        "__init__.py",
        "instantiation.py",
        "profile_bundles.py",
        "profiles.py",
        "repositories.py",
        "templates.py",
    },
    "workspace": {
        "__init__.py",
        "actors.py",
        "guidance.py",
        "manifest.py",
        "path_resolution.py",
        "pixi.py",
        "reset.py",
        "self_query.py",
        "surfaces.py",
    },
}

OBSOLETE_DOMAIN_HELPER_MODULES = {
    "isomer_labs.artifact_formats.resolver",
    "isomer_labs.artifact_formats.validation",
    "isomer_labs.artifact_formats.rendering",
    "isomer_labs.deepsci_ext.registry",
    "isomer_labs.deepsci_ext.rendering",
    "isomer_labs.deepsci_ext.service",
    "isomer_labs.teams.template_harness",
    "isomer_labs.teams.packet_validation",
    "isomer_labs.teams.profile_bundle_validation",
    "isomer_labs.workspace.layout",
    "isomer_labs.workspace.semantic_surfaces",
    "isomer_labs.workspace.tmp",
    "isomer_labs.workspace.paths",
    "isomer_labs.workspace.refs",
}

ALLOWED_PACKAGE_NAMES = {
    "artifact_formats",
    "cli",
    "core",
    "deepsci_ext",
    "houmao",
    "models",
    "project",
    "records",
    "runtime",
    "skills",
    "teams",
    "web",
    "workspace",
    "__pycache__",
}


class SourceArchitectureTests(unittest.TestCase):
    def _is_package_asset_path(self, relative: Path) -> bool:
        return any(relative == root or root in relative.parents for root in PACKAGE_ASSET_CODE_ROOTS)

    def test_cli_is_package_backed_and_command_groups_have_modules(self) -> None:
        self.assertFalse((SRC_ROOT / "cli.py").exists())
        self.assertTrue((SRC_ROOT / "cli" / "__init__.py").is_file())
        self.assertTrue((SRC_ROOT / "cli" / "app.py").is_file())
        self.assertTrue((SRC_ROOT / "cli" / "handlers" / "main.py").is_file())
        self.assertTrue((SRC_ROOT / "cli" / "options.py").is_file())
        self.assertTrue((SRC_ROOT / "cli" / "output.py").is_file())
        handler_modules = [
            "project.py",
            "workspace.py",
            "workspace_paths.py",
            "teams.py",
            "runtime.py",
            "team_instances.py",
            "team_instance_support.py",
            "records.py",
            "self.py",
            "schemas.py",
        ]
        for relative in handler_modules:
            self.assertTrue((SRC_ROOT / "cli" / "handlers" / relative).is_file(), relative)

        command_modules = [
            "artifact_formats.py",
            "deepsci_ext.py",
            "project.py",
            "doctor.py",
            "runtime.py",
            "handoffs.py",
            "team_templates.py",
            "team_repositories.py",
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
            "isomer_labs.deepsci_ext",
            "isomer_labs.houmao.adapter",
            "isomer_labs.houmao.manifests",
            "isomer_labs.runtime.records",
            "isomer_labs.runtime.store",
            "isomer_labs.runtime.validation",
            "isomer_labs.artifact_formats.processing",
            "isomer_labs.deepsci_ext.tools",
            "isomer_labs.teams.repositories",
            "isomer_labs.teams.instantiation",
            "isomer_labs.teams.profiles",
            "isomer_labs.teams.templates",
            "isomer_labs.project.context",
            "isomer_labs.workspace.path_resolution",
            "isomer_labs.workspace.surfaces",
            "isomer_labs.records.store",
            "isomer_labs.core.diagnostics",
            "isomer_labs.skills.system_assets",
        ]
        for module_name in modules:
            self.assertIsNotNone(importlib.import_module(module_name), module_name)

    def test_system_skill_assets_are_package_owned(self) -> None:
        asset_root = SRC_ROOT / "assets" / "system_skills"
        self.assertTrue(asset_root.is_dir())
        self.assertTrue((asset_root / "manifest.toml").is_file())
        self.assertTrue((asset_root / "README.md").is_file())
        for name in ("misc", "operator", "research-paradigm", "service"):
            self.assertTrue((asset_root / name).is_dir(), name)
        self.assertFalse((asset_root / "dev").exists())

    def test_skillset_authoring_view_points_to_package_assets(self) -> None:
        skillset_root = REPO_ROOT / "skillset"
        self.assertTrue((skillset_root / "dev").is_dir())
        self.assertFalse((skillset_root / "dev").is_symlink())
        for name in ("README.md", "manifest.toml", "misc", "operator", "research-paradigm", "service"):
            path = skillset_root / name
            self.assertTrue(path.is_symlink(), name)
            self.assertTrue(path.resolve(strict=True).is_relative_to((SRC_ROOT / "assets" / "system_skills").resolve()))

    def test_hatch_wheel_targets_isomer_package(self) -> None:
        pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        wheel = pyproject["tool"]["hatch"]["build"]["targets"]["wheel"]
        self.assertEqual(["src/isomer_labs"], wheel["packages"])

    def test_runtime_package_uses_canonical_internal_modules(self) -> None:
        runtime_root = SRC_ROOT / "runtime"
        runtime_files = {
            path.name
            for path in runtime_root.iterdir()
            if path.is_file() and path.suffix == ".py"
        }
        self.assertEqual(CANONICAL_RUNTIME_FILES, runtime_files)
        for name in OBSOLETE_RUNTIME_FILES:
            self.assertFalse((runtime_root / name).exists(), name)

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
                for module_path in (*REMOVED_MODULE_PATHS, *REMOVED_RUNTIME_MODULE_PATHS, *OBSOLETE_DOMAIN_HELPER_MODULES):
                    if module_path in content:
                        relative = path.relative_to(REPO_ROOT).as_posix()
                        violations.append(f"{relative}: {module_path}")
        self.assertEqual([], violations)

    def test_consolidated_domain_packages_use_canonical_internal_modules(self) -> None:
        for package_name, expected_files in CANONICAL_DOMAIN_PACKAGE_FILES.items():
            package_root = SRC_ROOT / package_name
            package_files = {
                path.name
                for path in package_root.iterdir()
                if path.is_file() and path.suffix == ".py"
            }
            self.assertEqual(expected_files, package_files, package_name)

        for module_path in OBSOLETE_DOMAIN_HELPER_MODULES:
            relative = Path(*module_path.removeprefix("isomer_labs.").split(".")).with_suffix(".py")
            self.assertFalse((SRC_ROOT / relative).exists(), module_path)

    def test_package_root_only_contains_bootstrap_files(self) -> None:
        root_files = {path.name for path in SRC_ROOT.iterdir() if path.is_file() and path.suffix == ".py"}
        self.assertEqual(set(), root_files - ROOT_FILE_ALLOWLIST)

    def test_large_implementation_files_are_package_scoped_or_transition_tracked(self) -> None:
        threshold = 800
        oversized: list[str] = []
        for path in sorted(SRC_ROOT.rglob("*.py")):
            relative = path.relative_to(SRC_ROOT).as_posix()
            if self._is_package_asset_path(Path(relative)):
                continue
            if relative in CANONICAL_LARGE_RUNTIME_FILES:
                continue
            if relative in PACKAGE_SIZE_TRANSITIONS:
                continue
            line_count = len(path.read_text(encoding="utf-8").splitlines())
            if line_count > threshold:
                oversized.append(f"{relative}:{line_count}")
        self.assertEqual([], oversized)

    def test_command_registration_does_not_return_to_cli_app_monolith(self) -> None:
        app_source = (SRC_ROOT / "cli" / "app.py").read_text(encoding="utf-8")
        handler_main_source = (SRC_ROOT / "cli" / "handlers" / "main.py").read_text(encoding="utf-8")
        self.assertNotIn("@app.command(", app_source)
        self.assertNotIn("@app.group(name=\"team-instances\"", app_source)
        self.assertNotIn("def _cmd_", app_source)
        self.assertNotIn("def _cmd_", handler_main_source)
        self.assertLessEqual(len(app_source.splitlines()), 300)
        self.assertLessEqual(len(handler_main_source.splitlines()), 80)

    def test_new_package_names_keep_expected_domain_boundaries(self) -> None:
        package_names = {
            path.name
            for path in SRC_ROOT.iterdir()
            if path.is_dir() and (path / "__init__.py").is_file()
        }
        unexpected = sorted(package_names - ALLOWED_PACKAGE_NAMES)
        self.assertEqual([], unexpected)
        self.assertFalse((SRC_ROOT / "adapter" / "__init__.py").exists())

    def test_named_use_case_orchestration_stays_out_of_src(self) -> None:
        forbidden_names = {"uc01", "uc02", "uc03", "uc04", "uc05", "uc06", "uc07"}
        violations: list[str] = []
        for path in sorted(SRC_ROOT.rglob("*.py")):
            relative = path.relative_to(SRC_ROOT)
            if self._is_package_asset_path(relative):
                continue
            parts = {Path(part).stem for part in relative.parts}
            if "workflows" in relative.parts or parts & forbidden_names:
                violations.append(relative.as_posix())
        self.assertEqual([], violations)

    def test_src_does_not_derive_checkout_root(self) -> None:
        violations: list[str] = []
        patterns = (
            re.compile(r"Path\(__file__\)\.resolve\(\)\.parents\[[0-9]+\]"),
        )
        for path in sorted(SRC_ROOT.rglob("*.py")):
            relative = path.relative_to(SRC_ROOT).as_posix()
            if self._is_package_asset_path(Path(relative)):
                continue
            content = path.read_text(encoding="utf-8")
            for pattern in patterns:
                if pattern.search(content):
                    violations.append(f"{relative}: {pattern.pattern}")
        self.assertEqual([], violations)

    def test_src_does_not_reference_checkout_only_dirs_at_runtime(self) -> None:
        forbidden_fragments = (
            '"teams/',
            "'teams/",
            '"skillset/',
            "'skillset/",
            '"tests/',
            "'tests/",
            '"openspec/',
            "'openspec/",
            '".imsight-arts/',
            "'.imsight-arts/",
            '"extern/',
            "'extern/",
        )
        allowed_fragments = {
            "cli/handlers/workspace_paths.py": ('"repos/extern/"',),
        }
        violations: list[str] = []
        for path in sorted(SRC_ROOT.rglob("*.py")):
            relative = path.relative_to(SRC_ROOT).as_posix()
            if self._is_package_asset_path(Path(relative)):
                continue
            content = path.read_text(encoding="utf-8")
            for fragment in forbidden_fragments:
                if fragment in allowed_fragments.get(relative, ()):
                    continue
                if fragment in content:
                    violations.append(f"{relative}: {fragment}")
        self.assertEqual([], violations)


if __name__ == "__main__":
    unittest.main()
