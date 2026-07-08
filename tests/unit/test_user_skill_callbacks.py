from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from isomer_labs.models import (
    PROJECT_MANIFEST_SCHEMA_VERSION,
    Project,
    ProjectManifest,
    ProjectState,
    ToolboxRegistration,
)
from isomer_labs.project.skill_callback_commands import (
    prepare_callback_source,
    resolve_user_skill_callbacks,
)
from isomer_labs.project.skill_callbacks import CallbackRegistryRef, load_callback_registry
from isomer_labs.project.toolbox_callbacks import load_toolbox_callback_manifest


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

    def test_resolve_skips_plugin_callbacks_when_toolbox_is_disabled(self) -> None:
        project = self.make_project()
        project.manifest.toolboxes.append(
            ToolboxRegistration(
                toolbox_id="demo.toolbox",
                scope="project",
                status="disabled",
                source_path_input="toolboxes/demo",
                source_path=project.manifest_path,
            )
        )
        registry = self.registry_ref(project)
        write(project.root / "prompt-a.md", "A\n")
        write(project.root / "prompt-b.md", "B\n")
        write(
            registry.path,
            """
            schema_version = "isomer-user-skill-callback-registry.v1"

            [[callbacks]]
            id = "demo.toolbox:group/a"
            skill = "isomer-deepsci-scout"
            stage = "begin"
            scope = "project"
            status = "active"
            priority = 10
            source_type = "prompt_file"
            prompt_file = "prompt-a.md"
            toolbox_id = "demo.toolbox"
            toolbox_key = "group/a"

            [[callbacks]]
            id = "manual"
            skill = "isomer-deepsci-scout"
            stage = "begin"
            scope = "project"
            status = "active"
            priority = 20
            source_type = "prompt_file"
            prompt_file = "prompt-b.md"
            """,
        )
        state = ProjectState(project=project, topic_configs={}, local_context=None, diagnostics=[])

        result = resolve_user_skill_callbacks(state, None, skill="isomer-deepsci-scout", stage="begin")

        self.assertTrue(result.ok, result.diagnostics)
        self.assertEqual(["manual"], [callback.id for callback in result.callbacks])
        self.assertEqual(("demo.toolbox:group/a",), result.gated_callback_ids)

    def test_namespaced_callback_ids_resolve_together_and_reject_duplicates(self) -> None:
        project = self.make_project()
        registry = self.registry_ref(project)
        write(project.root / "prompt-a.md", "A\n")
        write(project.root / "prompt-b.md", "B\n")
        write(
            registry.path,
            """
            schema_version = "isomer-user-skill-callback-registry.v1"

            [[callbacks]]
            id = "toolbox-a:group/a"
            skill = "isomer-deepsci-scout"
            stage = "begin"
            scope = "project"
            status = "active"
            priority = 100
            source_type = "prompt_file"
            prompt_file = "prompt-a.md"

            [[callbacks]]
            id = "toolbox-b:group/a"
            skill = "isomer-deepsci-scout"
            stage = "begin"
            scope = "project"
            status = "active"
            priority = 100
            source_type = "prompt_file"
            prompt_file = "prompt-b.md"
            """,
        )
        state = ProjectState(project=project, topic_configs={}, local_context=None, diagnostics=[])

        result = resolve_user_skill_callbacks(state, None, skill="isomer-deepsci-scout", stage="begin")

        self.assertTrue(result.ok, result.diagnostics)
        self.assertEqual(["toolbox-a:group/a", "toolbox-b:group/a"], [callback.id for callback in result.callbacks])

        write(
            registry.path,
            """
            schema_version = "isomer-user-skill-callback-registry.v1"

            [[callbacks]]
            id = "toolbox-a:group/a"
            skill = "isomer-deepsci-scout"
            stage = "begin"
            scope = "project"
            status = "active"
            priority = 100
            source_type = "prompt_file"
            prompt_file = "prompt-a.md"

            [[callbacks]]
            id = "toolbox-a:group/a"
            skill = "isomer-deepsci-scout"
            stage = "begin"
            scope = "project"
            status = "active"
            priority = 100
            source_type = "prompt_file"
            prompt_file = "prompt-b.md"
            """,
        )

        duplicate = load_callback_registry(project, registry, missing_severity="error")

        self.assertIn("ISO104", codes(duplicate.diagnostics))

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

    def test_inline_prompt_path_percent_encodes_namespaced_callback_id(self) -> None:
        project = self.make_project()

        source = prepare_callback_source(
            project,
            scope="project",
            research_topic_id=None,
            callback_id="toolbox:group/key",
            prompt="Use toolbox guidance.",
            prompt_file=None,
            skill_dir=None,
            allow_external_source=False,
        )

        self.assertEqual("prompt", source[0])
        self.assertEqual(".isomer-labs/user-skill-callbacks/prompts/toolbox%3Agroup%2Fkey.md", source[1])

    def test_toolbox_manifest_requires_toolbox_id_key_and_unique_local_keys(self) -> None:
        project = self.make_project()
        toolbox = project.root / "skillset" / "toolboxes" / "bad"
        write(toolbox / "one" / "SKILL.md", "# One\n")
        write(toolbox / "two" / "SKILL.md", "# Two\n")
        write(
            toolbox / "manifest.toml",
            """
            schema_version = "isomer-toolbox.v1"
            id = "bad"
            kind = "toolbox-callback-bundle"

            [[callbacks]]
            id = "legacy"
            target_skill = "isomer-deepsci-scout"
            stage = "begin"
            source_type = "skill_dir"
            skill_dir = "one"

            [[callbacks]]
            target_skill = "isomer-deepsci-scout"
            stage = "begin"
            source_type = "skill_dir"
            skill_dir = "two"
            """,
        )

        result = load_toolbox_callback_manifest(project, "skillset/toolboxes/bad")

        self.assertIsNone(result.manifest)
        self.assertIn("ISO103", codes(result.diagnostics))

    def test_toolbox_manifest_derives_key_and_accepts_slash_hierarchy(self) -> None:
        project = self.make_project()
        toolbox = project.root / "skillset" / "toolboxes" / "good"
        write(toolbox / "callback" / "SKILL.md", "# Callback\n")
        write(
            toolbox / "manifest.toml",
            """
            schema_version = "isomer-toolbox.v1"
            toolbox_id = "good-toolbox"
            kind = "toolbox-callback-bundle"

            [[callbacks]]
            key = "group/a"
            target_skill = "isomer-deepsci-scout"
            stage = "begin"
            source_type = "skill_dir"
            skill_dir = "callback"

            [[callbacks]]
            target_skill = "isomer-deepsci-scout"
            stage = "end"
            source_type = "skill_dir"
            skill_dir = "callback"
            """,
        )

        result = load_toolbox_callback_manifest(project, "skillset/toolboxes/good")

        self.assertIsNotNone(result.manifest)
        assert result.manifest is not None
        self.assertEqual(["group/a", "isomer-deepsci-scout/end"], [entry.toolbox_key for entry in result.manifest.callbacks])

    def test_toolbox_manifest_accepts_runtime_param_definitions_and_bundles(self) -> None:
        project = self.make_project()
        toolbox = project.root / "skillset" / "toolboxes" / "with-params"
        write(toolbox / "callback" / "SKILL.md", "# Callback\n")
        write(
            toolbox / "manifest.toml",
            """
            schema_version = "isomer-toolbox.v1"
            toolbox_id = "with-params"
            kind = "toolbox-callback-bundle"

            [[callbacks]]
            target_skill = "isomer-deepsci-scout"
            stage = "begin"
            source_type = "skill_dir"
            skill_dir = "callback"

            [[runtime_params]]
            key = "policy/mode"
            value_type = "enum"
            default = "strict"
            allowed_values = ["strict", "relaxed"]
            description = "Policy mode."

            [[runtime_param_bundles]]
            name = "strict-defaults"
            path = "params/strict.toml"
            """,
        )

        result = load_toolbox_callback_manifest(project, "skillset/toolboxes/with-params")

        self.assertIsNotNone(result.manifest)
        assert result.manifest is not None
        self.assertEqual("policy/mode", result.manifest.runtime_params[0].key)
        self.assertEqual(("strict", "relaxed"), result.manifest.runtime_params[0].allowed_values)
        self.assertEqual("strict-defaults", result.manifest.runtime_param_bundles[0].name)


if __name__ == "__main__":
    unittest.main()
