from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from isomer_labs.context import resolve_effective_topic_context
from isomer_labs.models import EffectiveTopicContext, SelectionRequest
from isomer_labs.project import discover_project
from isomer_labs.topic_workspace_manifest import (
    DEFAULT_LAYOUT_PROFILE,
    TOPIC_WORKSPACE_MANIFEST_SCHEMA_VERSION,
    catalog,
    compatibility_aliases,
    load_topic_workspace_manifest,
    parse_topic_workspace_manifest,
    render_topic_workspace_manifest,
    resolve_semantic_binding,
)
from isomer_labs.validation import build_project_state


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


class TopicWorkspaceManifestTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        return Path(tmp.name)

    def make_context(self) -> EffectiveTopicContext:
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
        project, project_diagnostics = discover_project(cwd=root, env={})
        self.assertEqual([], project_diagnostics)
        self.assertIsNotNone(project)
        state = build_project_state(project)
        self.assertEqual([], state.diagnostics)
        context, context_diagnostics = resolve_effective_topic_context(state, SelectionRequest(), cwd=root, env={})
        self.assertEqual([], context_diagnostics)
        self.assertIsNotNone(context)
        return context

    def test_missing_manifest_synthesizes_default_profile_bindings(self) -> None:
        context = self.make_context()

        manifest, diagnostics = load_topic_workspace_manifest(context)

        self.assertEqual([], diagnostics)
        self.assertFalse(manifest.exists)
        self.assertEqual(TOPIC_WORKSPACE_MANIFEST_SCHEMA_VERSION, manifest.schema_version)
        self.assertEqual(DEFAULT_LAYOUT_PROFILE, manifest.layout_profile)
        result, result_diagnostics = resolve_semantic_binding(context, "topic.main_repo", env={})
        self.assertEqual([], result_diagnostics)
        self.assertIsNotNone(result)
        self.assertEqual(context.topic_workspace_path / "repos" / "topic-main", result.path)
        self.assertEqual("default_profile", result.source)

    def test_manifest_parse_render_and_catalog_classification(self) -> None:
        path = Path("topic-workspace.toml")
        manifest = parse_topic_workspace_manifest(
            path,
            {
                "schema_version": TOPIC_WORKSPACE_MANIFEST_SCHEMA_VERSION,
                "research_topic_id": "default",
                "topic_workspace_id": "default",
                "bindings": [
                    {
                        "label": "topic.records.artifacts",
                        "path_template": "durable-artifacts",
                        "owner": "topic",
                        "durability": "durable",
                        "sharing": "topic",
                    }
                ],
            },
        )

        self.assertTrue(manifest.exists)
        self.assertEqual("durable-artifacts", manifest.binding_for("topic.records.artifacts").path_template)
        rendered = render_topic_workspace_manifest(manifest)
        self.assertIn('schema_version = "isomer-topic-workspace-manifest.v1"', rendered)
        self.assertIn('label = "topic.records.artifacts"', rendered)
        self.assertEqual("topic.records.artifacts", compatibility_aliases()["records_artifacts"])
        private_surface = catalog()["agent.private_artifacts"]
        self.assertEqual("agent", private_surface.owner)
        self.assertEqual("private", private_surface.sharing)
        self.assertEqual("agent", private_surface.required_context)

    def test_manifest_validation_reports_schema_duplicate_and_unsafe_paths(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            f"""
            schema_version = "older-schema"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.main_repo"
            path_template = "{(context.project.root.parent / 'outside').as_posix()}"
            owner = "topic"
            durability = "git"
            sharing = "topic"
            status = "active"

            [[bindings]]
            label = "topic.main_repo"
            path_template = "another-main"
            owner = "topic"
            durability = "git"
            sharing = "topic"
            status = "active"
            """,
        )

        _, diagnostics = load_topic_workspace_manifest(context)

        codes = {diagnostic.code for diagnostic in diagnostics}
        self.assertIn("ISO060", codes)
        self.assertIn("ISO005", codes)
        self.assertTrue(any("Duplicate active semantic surface binding" in diagnostic.message for diagnostic in diagnostics))


if __name__ == "__main__":
    unittest.main()
