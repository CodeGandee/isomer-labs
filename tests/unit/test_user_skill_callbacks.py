from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from isomer_labs.models import PROJECT_MANIFEST_SCHEMA_VERSION, Project, ProjectManifest, ProjectState
from isomer_labs.project.skill_callback_commands import (
    prepare_callback_source,
    resolve_user_skill_callbacks,
)
from isomer_labs.project.skill_callbacks import CallbackRegistryRef, load_callback_registry


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def codes(diagnostics: object) -> set[str]:
    return {diagnostic.code for diagnostic in diagnostics}  # type: ignore[attr-defined]


class UserSkillCallbackTests(unittest.TestCase):
    def make_project(self) -> Project:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        manifest_path = root / ".isomer-labs" / "manifest.toml"
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest = ProjectManifest(
            schema_version=PROJECT_MANIFEST_SCHEMA_VERSION,
            source_path=manifest_path,
            research_topics=[],
            topic_workspaces=[],
            user_skill_callback_registry_refs=[".isomer-labs/user-skill-callbacks/registry.toml"],
        )
        return Project(
            root=root,
            config_dir=root / ".isomer-labs",
            manifest_path=manifest_path,
            manifest=manifest,
            discovery_source="test",
        )

    def registry_ref(self, project: Project) -> CallbackRegistryRef:
        return CallbackRegistryRef(
            scope="project",
            path_input=".isomer-labs/user-skill-callbacks/registry.toml",
            path=project.root / ".isomer-labs" / "user-skill-callbacks" / "registry.toml",
            source_path=project.manifest_path,
        )

    def test_registry_parser_validates_schema_stage_status_priority_and_duplicates(self) -> None:
        project = self.make_project()
        registry = self.registry_ref(project)
        write(project.root / "prompt.md", "Use domain-specific constraints.\n")
        write(
            registry.path,
            """
            schema_version = "wrong"

            [[callbacks]]
            id = "duplicate"
            skill = "isomer-deepsci-scout"
            stage = "begin"
            scope = "project"
            status = "active"
            priority = 5
            source_type = "prompt_file"
            prompt_file = "prompt.md"

            [[callbacks]]
            id = "bad-stage"
            skill = "isomer-deepsci-scout"
            stage = "middle"
            scope = "project"
            status = "active"
            priority = -1
            source_type = "prompt_file"
            prompt_file = "prompt.md"

            [[callbacks]]
            id = "duplicate"
            skill = "isomer-deepsci-scout"
            stage = "end"
            scope = "project"
            status = "active"
            priority = 15
            source_type = "prompt_file"
            prompt_file = "prompt.md"
            """,
        )

        result = load_callback_registry(project, registry, missing_severity="error")

        self.assertIn("ISO102", codes(result.diagnostics))
        self.assertIn("ISO103", codes(result.diagnostics))
        self.assertIn("ISO104", codes(result.diagnostics))

    def test_resolve_orders_topic_before_project_priority_then_id_and_skips_inactive(self) -> None:
        project = self.make_project()
        registry = self.registry_ref(project)
        write(project.root / "prompt-a.md", "A\n")
        write(project.root / "prompt-b.md", "B\n")
        write(project.root / "prompt-inactive.md", "Inactive\n")
        write(
            registry.path,
            """
            schema_version = "isomer-user-skill-callback-registry.v1"

            [[callbacks]]
            id = "b"
            skill = "isomer-deepsci-scout"
            stage = "begin"
            scope = "project"
            status = "active"
            priority = 20
            source_type = "prompt_file"
            prompt_file = "prompt-b.md"

            [[callbacks]]
            id = "a"
            skill = "isomer-deepsci-scout"
            stage = "begin"
            scope = "project"
            status = "active"
            priority = 10
            source_type = "prompt_file"
            prompt_file = "prompt-a.md"

            [[callbacks]]
            id = "inactive"
            skill = "isomer-deepsci-scout"
            stage = "begin"
            scope = "project"
            status = "inactive"
            priority = 1
            source_type = "prompt_file"
            prompt_file = "prompt-inactive.md"
            """,
        )
        state = ProjectState(project=project, topic_configs={}, local_context=None, diagnostics=[])

        result = resolve_user_skill_callbacks(state, None, skill="isomer-deepsci-scout", stage="begin")

        self.assertTrue(result.ok, result.diagnostics)
        self.assertEqual(["a", "b"], [callback.id for callback in result.callbacks])

    def test_source_validation_checks_exactly_one_source_bounds_skill_dir_and_secrets(self) -> None:
        project = self.make_project()
        source = prepare_callback_source(
            project,
            scope="project",
            research_topic_id=None,
            callback_id="cb",
            prompt="api_key = 'SHOULD_NOT_LEAK_123'",
            prompt_file="missing.md",
            skill_dir=None,
            allow_external_source=False,
        )
        self.assertIn("ISO103", codes(source[2]))

        outside = project.root.parent / "external-skill"
        write(outside / "SKILL.md", "# External\n")
        source = prepare_callback_source(
            project,
            scope="project",
            research_topic_id=None,
            callback_id="cb",
            prompt=None,
            prompt_file=None,
            skill_dir=str(outside),
            allow_external_source=False,
        )
        self.assertIn("ISO005", codes(source[2]))

        source = prepare_callback_source(
            project,
            scope="project",
            research_topic_id=None,
            callback_id="cb",
            prompt=None,
            prompt_file=None,
            skill_dir=str(outside),
            allow_external_source=True,
        )
        self.assertEqual([], source[2])
        self.assertEqual("skill_dir", source[0])


if __name__ == "__main__":
    unittest.main()
