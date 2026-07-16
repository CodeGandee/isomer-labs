from __future__ import annotations

import tempfile
import textwrap
import unittest
from pathlib import Path

from isomer_labs.project.context import resolve_effective_topic_context
from isomer_labs.models import EffectiveTopicContext, SelectionRequest
from isomer_labs.workspace.path_resolution import resolve_effective_agent_context, resolve_effective_topic_actor_context, resolve_semantic_path
from isomer_labs.project import discover_project
from isomer_labs.workspace.manifest import (
    DEFAULT_LAYOUT_PROFILE,
    TOPIC_WORKSPACE_MANIFEST_SCHEMA_VERSION,
    catalog,
    compatibility_aliases,
    load_topic_workspace_manifest,
    materialize_default_manifest,
    parse_topic_workspace_manifest,
    record_topic_service_master_binding,
    render_topic_workspace_manifest,
    resolve_semantic_binding,
    resolve_worker_output_policy,
)
from isomer_labs.project.validation import build_project_state


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
        result, result_diagnostics = resolve_semantic_binding(context, "topic.repos.main", env={})
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
                        "path": "durable-artifacts",
                        "storage_profile": "topic_records_dir",
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
        self.assertEqual("topic.tmp", compatibility_aliases()["topic_tmp"])
        self.assertEqual("topic.repos.main.tmp", compatibility_aliases()["topic_main_tmp"])
        self.assertEqual("agent.tmp", compatibility_aliases()["agent_tmp"])
        self.assertEqual("topic.intent.overview", compatibility_aliases()["topic_intent_overview"])
        self.assertEqual("topic.intent.actor_definitions", compatibility_aliases()["topic_intent_actor_definitions"])
        self.assertEqual("topic.env.topic_setup_target_spec", compatibility_aliases()["topic_env_topic_setup_target_spec"])
        self.assertEqual("topic.env.actor_env_gates", compatibility_aliases()["topic_env_actor_env_gates"])
        self.assertEqual("topic.paper.template_exchange_root", compatibility_aliases()["topic_paper_template_exchange_root"])
        self.assertEqual("topic.workspace.summary", compatibility_aliases()["topic_workspace_summary"])
        private_surface = catalog()["agent.private_artifacts"]
        self.assertEqual("agent", private_surface.owner)
        self.assertEqual("private", private_surface.sharing)
        self.assertEqual("agent", private_surface.required_context)
        tmp_surface = catalog()["topic.repos.main.tmp"]
        self.assertEqual("disposable", tmp_surface.durability)
        self.assertEqual("private", tmp_surface.sharing)
        intent_surface = catalog()["topic.intent.topic_env_requirements"]
        self.assertEqual("topic_intent_source_file", intent_surface.storage_profile)
        self.assertEqual("file", intent_surface.path_kind)
        actor_definition_surface = catalog()["topic.intent.actor_definitions"]
        self.assertEqual("topic_intent_source_file", actor_definition_surface.storage_profile)
        self.assertEqual("file", actor_definition_surface.path_kind)
        actor_gate_surface = catalog()["topic.env.actor_env_gates"]
        self.assertEqual("topic_env_target_spec_file", actor_gate_surface.storage_profile)
        self.assertEqual("file", actor_gate_surface.path_kind)
        target_surface = catalog()["topic.env.agent_setup_target_spec"]
        self.assertEqual("topic_env_target_spec_file", target_surface.storage_profile)
        self.assertEqual("file", target_surface.path_kind)
        summary_surface = catalog()["topic.workspace.summary"]
        self.assertEqual("topic_workspace_summary_file", summary_surface.storage_profile)
        self.assertEqual("file", summary_surface.path_kind)
        self.assertEqual("topic", summary_surface.owner)
        self.assertEqual("durable", summary_surface.durability)
        exchange_surface = catalog()["topic.paper.template_exchange_root"]
        self.assertEqual("topic_durable_dir", exchange_surface.storage_profile)
        self.assertEqual("directory", exchange_surface.path_kind)
        self.assertEqual("topic", exchange_surface.owner)
        self.assertEqual("durable", exchange_surface.durability)
        readonly_projection = catalog()["topic.repos.main.projections.readonly"]
        self.assertEqual("topic_repo_readonly_projection_dir", readonly_projection.storage_profile)
        self.assertEqual("topic_read", readonly_projection.sharing)
        writable_projection = catalog()["topic.repos.main.projections.writable"]
        self.assertEqual("topic_repo_writable_projection_dir", writable_projection.storage_profile)
        self.assertEqual("topic_write", writable_projection.sharing)
        projection_manifest = catalog()["topic.repos.main.projections.manifest"]
        self.assertEqual("topic_repo_tracked_file", projection_manifest.storage_profile)
        self.assertEqual("file", projection_manifest.path_kind)
        self.assertEqual("topic.repos.main.projections.manifest", compatibility_aliases()["topic_main_projections_manifest"])
        actor_workspace = catalog()["topic.actors.workspace"]
        self.assertEqual("topic_actor", actor_workspace.scope)
        self.assertEqual("topic_actor_worktree", actor_workspace.storage_profile)
        self.assertEqual("topic_actor", actor_workspace.required_context)

    def test_topic_service_master_binding_parse_validate_and_render(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [topic_service_master]
            provider = "houmao"
            status = "prepared"
            updated_by = "isomer-srv-topic-service-agent-support"

            [topic_service_master.houmao]
            specialist_name = "isomer-tsm-default-specialist"
            launch_profile_name = "isomer-tsm-default-profile"
            managed_agent_name = "isomer-tsm-default-agent"
            specialist_ref = "houmao:specialist:isomer-tsm-default-specialist"
            """,
        )

        manifest, diagnostics = load_topic_workspace_manifest(context)

        self.assertEqual([], diagnostics)
        self.assertIsNotNone(manifest.topic_service_master)
        assert manifest.topic_service_master is not None
        self.assertEqual("prepared", manifest.topic_service_master.status)
        self.assertIsNotNone(manifest.topic_service_master.houmao)
        assert manifest.topic_service_master.houmao is not None
        self.assertEqual("isomer-tsm-default-specialist", manifest.topic_service_master.houmao.specialist_name)
        payload = manifest.to_json()["topic_service_master"]
        self.assertIsInstance(payload, dict)
        rendered = render_topic_workspace_manifest(manifest)
        self.assertIn("[topic_service_master.houmao]", rendered)
        self.assertIn('managed_agent_name = "isomer-tsm-default-agent"', rendered)

    def test_topic_service_master_binding_write_preserves_other_tables(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [custom_table]
            value = "preserve-me"
            """,
        )

        manifest, binding, diagnostics = record_topic_service_master_binding(
            context,
            status="prepared",
            specialist_name="isomer-tsm-default-specialist",
            launch_profile_name="isomer-tsm-default-profile",
            managed_agent_name="isomer-tsm-default-agent",
            updated_by="test",
        )

        self.assertEqual([], diagnostics)
        self.assertIsNotNone(manifest)
        self.assertIsNotNone(binding)
        text = (context.topic_workspace_path / "topic-workspace.toml").read_text(encoding="utf-8")
        self.assertIn("[custom_table]", text)
        self.assertIn("[topic_service_master.houmao]", text)

    def test_topic_service_master_binding_validation_rejects_drift_and_secrets(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [topic_service_master]
            provider = "houmao"
            status = "planned"

            [topic_service_master.houmao]
            specialist_name = "wrong-specialist"
            launch_profile_name = "isomer-tsm-default-profile"
            managed_agent_name = "isomer-tsm-default-agent"
            mailbox_contents = "do-not-store"
            """,
        )

        _, diagnostics = load_topic_workspace_manifest(context)

        messages = "\n".join(diagnostic.message for diagnostic in diagnostics)
        self.assertIn("status must be one of", messages)
        self.assertIn("differs from the current Topic Workspace naming contract", messages)
        self.assertIn("must not store credentials", messages)

    def test_topic_actor_binding_resolves_actor_scoped_paths(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[topic_actors]]
            topic_actor_name = "operator"
            actor_kind = "operator"
            runtime_kind = "codex"
            role_kind = "operator"
            controller_kind = "project_operator_session"
            default_cwd_label = "topic.actors.workspace"
            workspace_label = "topic.actors.workspace"
            status = "ready"

            [[topic_actors]]
            topic_actor_name = "claude-scout"
            actor_kind = "manual_worker"
            runtime_kind = "claude_code"
            role_kind = "scout"
            controller_kind = "human_user"
            default_cwd_label = "topic.actors.workspace"
            workspace_label = "topic.actors.workspace"
            status = "ready"
            """,
        )

        manifest, diagnostics = load_topic_workspace_manifest(context)
        self.assertEqual([], diagnostics)
        actor = manifest.topic_actor_binding_for("operator")
        self.assertIsNotNone(actor)
        assert actor is not None
        self.assertEqual("per-topic-actor/operator/main", actor.effective_branch)

        result, result_diagnostics = resolve_semantic_path(
            context,
            "topic.actors.workspace",
            env={},
            cwd=context.topic_workspace_path,
            topic_actor_name="operator",
            use_path_plan=False,
        )

        self.assertEqual([], result_diagnostics)
        self.assertIsNotNone(result)
        assert result is not None
        self.assertEqual(context.topic_workspace_path / "actors" / "operator", result.path)
        self.assertEqual("topic_actor:operator", result.scope_ref)
        self.assertEqual("operator", result.topic_actor_name)

        missing, missing_diagnostics = resolve_semantic_path(
            context,
            "topic.actors.workspace",
            env={},
            cwd=context.topic_workspace_path,
            use_path_plan=False,
        )
        self.assertIsNone(missing)
        self.assertTrue(any("Topic Actor-scoped command requires" in diagnostic.message for diagnostic in missing_diagnostics))

    def test_topic_actor_binding_rejects_unknown_non_extension_enum(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[topic_actors]]
            topic_actor_name = "operator"
            actor_kind = "mystery"
            runtime_kind = "codex"
            role_kind = "operator"
            controller_kind = "project_operator_session"
            status = "ready"
            """,
        )

        _, diagnostics = load_topic_workspace_manifest(context)

        self.assertTrue(any("Unsupported Topic Actor actor_kind" in diagnostic.message for diagnostic in diagnostics), diagnostics)

    def test_worker_output_policy_resolves_actor_and_agent_overrides(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[topic_actors]]
            topic_actor_name = "operator"
            actor_kind = "operator"
            runtime_kind = "codex"
            role_kind = "operator"
            controller_kind = "project_operator_session"
            output_root = "isomer-managed/worker-output/topic-actors/operator"
            commit_after_operation = true
            status = "ready"

            [agent_output_defaults]
            output_root = "isomer-managed/worker-output/agents/{agent_name}"
            commit_after_operation = false

            [[agent_output_overrides]]
            agent_name = "alice"
            output_root = "custom-output/{agent_name}"
            commit_after_operation = true
            """,
        )

        manifest, diagnostics = load_topic_workspace_manifest(context)
        self.assertEqual([], diagnostics)
        actor = manifest.topic_actor_binding_for("operator")
        self.assertIsNotNone(actor)
        assert actor is not None
        self.assertEqual("isomer-managed/worker-output/topic-actors/operator", actor.output_root)
        self.assertTrue(actor.commit_after_operation)

        actor_root, actor_root_diagnostics = resolve_semantic_path(
            context,
            "topic.actors.output_root",
            env={},
            cwd=context.topic_workspace_path,
            topic_actor_name="operator",
            use_path_plan=False,
        )
        self.assertEqual([], actor_root_diagnostics)
        self.assertIsNotNone(actor_root)
        assert actor_root is not None
        self.assertEqual(context.topic_workspace_path / "actors" / "operator" / "isomer-managed" / "worker-output" / "topic-actors" / "operator", actor_root.path)
        self.assertEqual("worker_output_policy", actor_root.source)

        agent_root, agent_root_diagnostics = resolve_semantic_path(
            context,
            "agent.output_root",
            env={},
            cwd=context.topic_workspace_path,
            agent_name="alice",
            use_path_plan=False,
        )
        self.assertEqual([], agent_root_diagnostics)
        self.assertIsNotNone(agent_root)
        assert agent_root is not None
        self.assertEqual(context.topic_workspace_path / "agents" / "alice" / "custom-output" / "alice", agent_root.path)
        self.assertEqual("worker_output_policy", agent_root.source)

        actor_context, actor_context_diagnostics = resolve_effective_topic_actor_context(
            context,
            env={},
            cwd=context.topic_workspace_path,
            explicit_topic_actor_name="operator",
        )
        self.assertEqual([], actor_context_diagnostics)
        assert actor_context is not None
        actor_policy, actor_policy_diagnostics = resolve_worker_output_policy(context, env={}, topic_actor_context=actor_context)
        self.assertEqual([], actor_policy_diagnostics)
        self.assertIsNotNone(actor_policy)
        assert actor_policy is not None
        self.assertTrue(actor_policy.commit_after_operation)
        self.assertEqual("isomer-managed/worker-output/topic-actors/operator", actor_policy.worker_relative_root)

        agent_context, agent_context_diagnostics = resolve_effective_agent_context(
            context,
            env={},
            cwd=context.topic_workspace_path,
            explicit_agent_name="alice",
        )
        self.assertEqual([], agent_context_diagnostics)
        assert agent_context is not None
        agent_policy, agent_policy_diagnostics = resolve_worker_output_policy(context, env={}, agent_context=agent_context)
        self.assertEqual([], agent_policy_diagnostics)
        self.assertIsNotNone(agent_policy)
        assert agent_policy is not None
        self.assertTrue(agent_policy.commit_after_operation)
        self.assertEqual("custom-output/alice", agent_policy.worker_relative_root)

    def test_worker_output_root_validation_rejects_escape_and_warns_on_shared_root(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[topic_actors]]
            topic_actor_name = "operator"
            actor_kind = "operator"
            runtime_kind = "codex"
            role_kind = "operator"
            controller_kind = "project_operator_session"
            output_root = "../shared"
            status = "ready"

            [[agent_output_overrides]]
            agent_name = "alice"
            output_root = "shared-output"
            """,
        )

        _, diagnostics = load_topic_workspace_manifest(context)

        self.assertTrue(any("must not contain parent traversal" in diagnostic.message for diagnostic in diagnostics), diagnostics)
        self.assertTrue(any(diagnostic.severity == "warning" and "omits the worker identity" in diagnostic.message for diagnostic in diagnostics), diagnostics)

    def test_default_profile_resolves_topic_main_projection_labels(self) -> None:
        context = self.make_context()

        readonly, readonly_diagnostics = resolve_semantic_binding(context, "topic.repos.main.projections.readonly", env={})
        writable, writable_diagnostics = resolve_semantic_binding(context, "topic.repos.main.projections.writable", env={})
        manifest, manifest_diagnostics = resolve_semantic_binding(context, "topic.repos.main.projections.manifest", env={})

        self.assertEqual([], readonly_diagnostics)
        self.assertEqual([], writable_diagnostics)
        self.assertEqual([], manifest_diagnostics)
        self.assertIsNotNone(readonly)
        self.assertIsNotNone(writable)
        self.assertIsNotNone(manifest)
        self.assertEqual(context.topic_workspace_path / "repos" / "topic-main" / "isomer-managed" / "topic-owned" / "readonly" / "extern", readonly.path)
        self.assertEqual(context.topic_workspace_path / "repos" / "topic-main" / "isomer-managed" / "topic-owned" / "writable" / "extern", writable.path)
        self.assertEqual(context.topic_workspace_path / "repos" / "topic-main" / "isomer-managed" / "tracked" / "manifests" / "extern-projections.toml", manifest.path)
        self.assertEqual("topic_repo_readonly_projection_dir", readonly.catalog.storage_profile)
        self.assertEqual("topic_repo_writable_projection_dir", writable.catalog.storage_profile)
        self.assertEqual("topic_repo_tracked_file", manifest.catalog.storage_profile)

    def test_projection_labels_follow_custom_topic_main_binding(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.repos.main"
            path = "source/main"
            storage_profile = "topic_repo"
            status = "active"
            """,
        )

        readonly, readonly_diagnostics = resolve_semantic_binding(context, "topic.repos.main.projections.readonly", env={})
        manifest, manifest_diagnostics = resolve_semantic_binding(context, "topic.repos.main.projections.manifest", env={})

        self.assertEqual([], readonly_diagnostics)
        self.assertEqual([], manifest_diagnostics)
        self.assertIsNotNone(readonly)
        self.assertIsNotNone(manifest)
        self.assertEqual(context.topic_workspace_path / "source" / "main" / "isomer-managed" / "topic-owned" / "readonly" / "extern", readonly.path)
        self.assertEqual(context.topic_workspace_path / "source" / "main" / "isomer-managed" / "tracked" / "manifests" / "extern-projections.toml", manifest.path)

    def test_template_exchange_root_default_override_and_source(self) -> None:
        context = self.make_context()

        default, default_diagnostics = resolve_semantic_binding(context, "topic.paper.template_exchange_root", env={})

        self.assertEqual([], default_diagnostics)
        self.assertIsNotNone(default)
        assert default is not None
        self.assertEqual(context.topic_workspace_path / "intent" / "derived" / "writing-template", default.path)
        self.assertEqual("default_profile", default.source)
        self.assertEqual("topic_durable_dir", default.catalog.storage_profile)

        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.paper.template_exchange_root"
            path = "user-editable/templates"
            storage_profile = "topic_durable_dir"
            status = "active"
            """,
        )
        overridden, override_diagnostics = resolve_semantic_binding(context, "topic.paper.template_exchange_root", env={})

        self.assertEqual([], override_diagnostics)
        self.assertIsNotNone(overridden)
        assert overridden is not None
        self.assertEqual(context.topic_workspace_path / "user-editable" / "templates", overridden.path)
        self.assertEqual("topic_workspace_manifest", overridden.source)
        self.assertIn("topic-workspace.toml", str(overridden.source_detail))

    def test_unknown_topic_main_sublabel_is_reserved(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.repos.main.projections.extra"
            path = "repos/topic-main/isomer-managed/topic-owned/readonly/extern/extra"
            storage_profile = "topic_repo"
            status = "active"
            """,
        )

        _, diagnostics = load_topic_workspace_manifest(context)

        self.assertTrue(any("Unknown or reserved Topic Main Development Repository semantic label" in diagnostic.message for diagnostic in diagnostics), diagnostics)

    def test_default_profile_resolves_topic_intent_file_labels(self) -> None:
        context = self.make_context()

        overview, overview_diagnostics = resolve_semantic_binding(context, "topic.intent.overview", env={})
        topic_gate, topic_gate_diagnostics = resolve_semantic_binding(context, "topic.intent.topic_env_requirements", env={})
        actor_definitions, actor_definition_diagnostics = resolve_semantic_binding(context, "topic.intent.actor_definitions", env={})
        actor_gates, actor_gate_diagnostics = resolve_semantic_binding(context, "topic.env.actor_env_gates", env={})
        agent_target, agent_target_diagnostics = resolve_semantic_binding(context, "topic.env.agent_setup_target_spec", env={})
        summary, summary_diagnostics = resolve_semantic_binding(context, "topic.workspace.summary", env={})

        self.assertEqual([], overview_diagnostics)
        self.assertEqual([], topic_gate_diagnostics)
        self.assertEqual([], actor_definition_diagnostics)
        self.assertEqual([], actor_gate_diagnostics)
        self.assertEqual([], agent_target_diagnostics)
        self.assertEqual([], summary_diagnostics)
        self.assertIsNotNone(overview)
        self.assertIsNotNone(topic_gate)
        self.assertIsNotNone(actor_definitions)
        self.assertIsNotNone(actor_gates)
        self.assertIsNotNone(agent_target)
        self.assertIsNotNone(summary)
        assert summary is not None
        self.assertEqual(context.topic_workspace_path / "intent" / "src" / "topic-overview.md", overview.path)
        self.assertEqual(context.topic_workspace_path / "intent" / "src" / "topic-env-gate.md", topic_gate.path)
        self.assertEqual(context.topic_workspace_path / "intent" / "src" / "actor-definitions.md", actor_definitions.path)
        self.assertEqual(context.topic_workspace_path / "intent" / "derived" / "actor-env-gates.md", actor_gates.path)
        self.assertEqual(context.topic_workspace_path / "intent" / "derived" / "isomer-agent-env-gate.md", agent_target.path)
        self.assertEqual(context.topic_workspace_path / "isomer-topic-workspace-summary.md", summary.path)
        self.assertEqual("default_profile", overview.source)
        self.assertEqual("topic_intent_source_file", topic_gate.catalog.storage_profile)
        self.assertEqual("topic_intent_source_file", actor_definitions.catalog.storage_profile)
        self.assertEqual("topic_env_target_spec_file", actor_gates.catalog.storage_profile)
        self.assertEqual("topic_env_target_spec_file", agent_target.catalog.storage_profile)
        self.assertEqual("topic_workspace_summary_file", summary.catalog.storage_profile)

    def test_materialize_default_intent_file_labels_creates_parent_only(self) -> None:
        context = self.make_context()

        manifest, created, diagnostics = materialize_default_manifest(
            context,
            labels=("topic.intent.overview", "topic.env.topic_setup_target_spec", "topic.workspace.summary", "topic.paper.template_exchange_root"),
            agent_name=None,
        )

        self.assertEqual([], diagnostics)
        self.assertIsNotNone(manifest)
        self.assertIn(context.topic_workspace_path / "intent" / "src", created)
        self.assertIn(context.topic_workspace_path / "intent" / "derived", created)
        self.assertIn(context.topic_workspace_path, created)
        self.assertIn(context.topic_workspace_path / "intent" / "derived" / "writing-template", created)
        self.assertTrue((context.topic_workspace_path / "intent" / "src").is_dir())
        self.assertTrue((context.topic_workspace_path / "intent" / "derived").is_dir())
        self.assertTrue((context.topic_workspace_path / "intent" / "derived" / "writing-template").is_dir())
        self.assertFalse((context.topic_workspace_path / "intent" / "src" / "topic-overview.md").exists())
        self.assertFalse((context.topic_workspace_path / "intent" / "derived" / "isomer-env-gate.md").exists())
        self.assertFalse((context.topic_workspace_path / "isomer-topic-workspace-summary.md").exists())

    def test_summary_label_supports_env_override_and_rejects_unknown_sibling(self) -> None:
        context = self.make_context()

        overridden, override_diagnostics = resolve_semantic_binding(
            context,
            "topic.workspace.summary",
            env={"ISOMER_PATH__TOPIC__WORKSPACE__SUMMARY": "custom-summary.md"},
        )
        self.assertEqual([], override_diagnostics)
        self.assertIsNotNone(overridden)
        assert overridden is not None
        self.assertEqual(context.project.root / "custom-summary.md", overridden.path)
        self.assertEqual("env", overridden.source)
        self.assertEqual("ISOMER_PATH__TOPIC__WORKSPACE__SUMMARY", overridden.source_detail)

        missing, missing_diagnostics = resolve_semantic_binding(context, "topic.workspace.missing", env={})
        self.assertIsNone(missing)
        self.assertTrue(any("Unknown or reserved Isomer-owned semantic label" in diagnostic.message for diagnostic in missing_diagnostics), missing_diagnostics)

    def test_manifest_rejects_wrong_intent_storage_profile(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.intent.overview"
            path = "intent/src/topic-overview.md"
            storage_profile = "topic_records_dir"
            status = "active"
            """,
        )

        _, diagnostics = load_topic_workspace_manifest(context)

        self.assertTrue(
            any('requires storage_profile = "topic_intent_source_file"' in diagnostic.message for diagnostic in diagnostics),
            diagnostics,
        )

    def test_manifest_validation_reports_schema_duplicate_and_unsafe_paths(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            f"""
            schema_version = "older-schema"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.repos.main"
            path = "{(context.project.root.parent / 'outside').as_posix()}"
            storage_profile = "topic_repo"
            status = "active"

            [[bindings]]
            label = "topic.repos.main"
            path = "another-main"
            storage_profile = "topic_repo"
            status = "active"
            """,
        )

        _, diagnostics = load_topic_workspace_manifest(context)

        codes = {diagnostic.code for diagnostic in diagnostics}
        self.assertIn("ISO060", codes)
        self.assertIn("ISO005", codes)
        self.assertTrue(any("Duplicate active semantic surface binding" in diagnostic.message for diagnostic in diagnostics))

    def test_tmp_surface_bindings_must_stay_inside_owning_surface(self) -> None:
        context = self.make_context()
        write(
            context.topic_workspace_path / "topic-workspace.toml",
            """
            schema_version = "isomer-topic-workspace-manifest.v1"
            research_topic_id = "default"
            topic_workspace_id = "default"

            [[bindings]]
            label = "topic.repos.main.tmp"
            path = "tmp/main"
            storage_profile = "topic_repo_disposable_dir"
            status = "active"
            """,
        )

        _, diagnostics = load_topic_workspace_manifest(context)

        self.assertTrue(any("topic.repos.main.tmp" == diagnostic.field for diagnostic in diagnostics), diagnostics)
        self.assertTrue(any("must stay inside `topic.repos.main`" in diagnostic.message for diagnostic in diagnostics), diagnostics)


if __name__ == "__main__":
    unittest.main()
