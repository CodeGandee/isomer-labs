from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from isomer_labs.models import SelectionRequest
from isomer_labs.project import discover_project
from isomer_labs.project.context import resolve_effective_topic_context
from isomer_labs.project.toolboxes import resolve_runtime_params
from isomer_labs.project.validation import build_project_state
from isomer_labs.workspace.manifest import load_topic_workspace_manifest


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def codes(diagnostics: object) -> set[str]:
    return {diagnostic.code for diagnostic in diagnostics}  # type: ignore[attr-defined]


class ToolboxRuntimeParamTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def make_project_with_topic(self) -> tuple[Path, object, object]:
        root = self.make_root()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [defaults]
            research_topic_id = "default"

            [[research_topics]]
            id = "default"
            config_path = ".isomer-labs/research-topics/default.toml"
            topic_workspace_id = "default"

            [[topic_workspaces]]
            id = "default"
            research_topic_id = "default"
            path = "topic-workspaces/default"
            """,
        )
        write(
            root / ".isomer-labs" / "research-topics" / "default.toml",
            """
            schema_version = "isomer-research-topic-config.v1"
            research_topic_id = "default"
            topic_statement = "Default topic"
            """,
        )
        (root / "topic-workspaces" / "default").mkdir(parents=True)
        project, diagnostics = discover_project(cwd=root, env={})
        self.assertEqual([], diagnostics)
        self.assertIsNotNone(project)
        assert project is not None
        state = build_project_state(project)
        self.assertEqual([], state.diagnostics)
        context, context_diagnostics = resolve_effective_topic_context(state, SelectionRequest(), cwd=root, env={})
        self.assertEqual([], context_diagnostics)
        self.assertIsNotNone(context)
        return root, project, context

    def test_resolution_applies_project_import_project_explicit_topic_import_topic_explicit(self) -> None:
        root, project, context = self.make_project_with_topic()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [defaults]
            research_topic_id = "default"

            [[research_topics]]
            id = "default"
            config_path = ".isomer-labs/research-topics/default.toml"
            topic_workspace_id = "default"

            [[topic_workspaces]]
            id = "default"
            research_topic_id = "default"
            path = "topic-workspaces/default"

            [[toolbox_runtime_param_imports]]
            toolbox_id = "demo.toolbox"
            path = "defaults.toml"
            scope = "project"

            [[toolbox_runtime_params]]
            toolbox_id = "demo.toolbox"
            key = "mode"
            value = "project-explicit"
            value_type = "enum"
            allowed_values = ["project-import", "project-explicit", "topic-import", "agent-explicit"]
            scope = "project"
            """,
        )
        write(
            root / ".isomer-labs" / "defaults.toml",
            """
            schema_version = "isomer-toolbox-runtime-params.v1"

            [[toolbox_runtime_params]]
            toolbox_id = "demo.toolbox"
            key = "mode"
            value = "project-import"
            value_type = "enum"
            allowed_values = ["project-import", "project-explicit", "topic-import", "agent-explicit"]
            scope = "project"
            """,
        )
        write(
            context.topic_workspace_path / "topic-defaults.toml",
            """
            schema_version = "isomer-toolbox-runtime-params.v1"

            [[toolbox_runtime_params]]
            toolbox_id = "demo.toolbox"
            key = "mode"
            value = "topic-import"
            value_type = "enum"
            allowed_values = ["project-import", "project-explicit", "topic-import", "agent-explicit"]
            scope = "research_topic"
            """,
        )
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[toolbox_runtime_param_imports]]
            toolbox_id = "demo.toolbox"
            path = "topic-defaults.toml"
            scope = "research_topic"

            [[toolbox_runtime_params]]
            toolbox_id = "demo.toolbox"
            key = "mode"
            value = "agent-explicit"
            value_type = "enum"
            allowed_values = ["project-import", "project-explicit", "topic-import", "agent-explicit"]
            scope = "topic_agent"
            topic_agent_name = "coder"
            """,
        )
        project, diagnostics = discover_project(cwd=root, env={})
        self.assertEqual([], diagnostics)
        assert project is not None
        state = build_project_state(project)
        self.assertEqual([], state.diagnostics)
        context, context_diagnostics = resolve_effective_topic_context(state, SelectionRequest(), cwd=root, env={})
        self.assertEqual([], context_diagnostics)
        assert context is not None

        broad = resolve_runtime_params(project, context)
        selected = broad.get("demo.toolbox:mode")
        self.assertIsNotNone(selected)
        assert selected is not None
        self.assertEqual("topic-import", selected.value)
        self.assertEqual(["project_import", "project_explicit", "topic_import"], [candidate.layer for candidate in selected.candidates])

        agent = resolve_runtime_params(project, context, topic_agent_name="coder")
        selected = agent.get("demo.toolbox:mode")
        self.assertIsNotNone(selected)
        assert selected is not None
        self.assertEqual("agent-explicit", selected.value)
        self.assertEqual(
            ["project_import", "project_explicit", "topic_import", "topic_explicit"],
            [candidate.layer for candidate in selected.candidates],
        )

    def test_project_manifest_rejects_topic_scope_toolbox_config(self) -> None:
        root = self.make_root()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [[toolboxes]]
            toolbox_id = "demo.toolbox"
            scope = "topic_agent"
            topic_agent_name = "coder"
            status = "active"
            """,
        )
        project, diagnostics = discover_project(cwd=root, env={})
        self.assertEqual([], diagnostics)
        assert project is not None
        state = build_project_state(project)

        self.assertIn("ISO103", codes(state.diagnostics))

    def test_old_toolbox_schema_names_are_rejected(self) -> None:
        root = self.make_root()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [[user_plugins]]
            plugin_id = "demo.toolbox"
            plugin_dir = "skillset/toolboxes/demo"

            [[toolboxes]]
            plugin_id = "demo.toolbox"
            source_path = "skillset/toolboxes/demo"

            [[user_plugin_runtime_params]]
            plugin_id = "demo.toolbox"
            key = "mode"
            value = "strict"
            """,
        )

        _project, diagnostics = discover_project(cwd=root, env={})

        self.assertIn("ISO103", codes(diagnostics))

    def test_old_runtime_param_import_schema_is_rejected(self) -> None:
        root, project, _context = self.make_project_with_topic()
        write(
            root / ".isomer-labs" / "manifest.toml",
            """
            schema_version = "isomer-project-manifest.v1"

            [[toolbox_runtime_param_imports]]
            toolbox_id = "demo.toolbox"
            path = "defaults.toml"
            scope = "project"
            """,
        )
        write(
            root / ".isomer-labs" / "defaults.toml",
            """
            schema_version = "isomer-user-plugin-runtime-params.v1"

            [[user_plugin_runtime_params]]
            plugin_id = "demo.toolbox"
            key = "mode"
            value = "strict"
            """,
        )
        project, diagnostics = discover_project(cwd=root, env={})
        self.assertEqual([], diagnostics)
        assert project is not None

        resolution = resolve_runtime_params(project)

        self.assertIn("ISO102", codes(resolution.diagnostics))
        self.assertIn("ISO103", codes(resolution.diagnostics))

    def test_topic_manifest_parses_toolbox_tables(self) -> None:
        root, _project, context = self.make_project_with_topic()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[toolboxes]]
            toolbox_id = "demo.toolbox"
            scope = "topic_agent"
            topic_agent_name = "coder"
            status = "active"

            [[toolbox_runtime_params]]
            toolbox_id = "demo.toolbox"
            key = "mode"
            value = "strict"
            value_type = "enum"
            allowed_values = ["strict", "relaxed"]
            scope = "topic_agent"
            topic_agent_name = "coder"
            """,
        )

        manifest, diagnostics = load_topic_workspace_manifest(context)

        self.assertEqual([], diagnostics)
        self.assertEqual("demo.toolbox", manifest.toolboxes[0].toolbox_id)
        self.assertEqual("coder", manifest.toolbox_runtime_params[0].topic_agent_name)


if __name__ == "__main__":
    unittest.main()
