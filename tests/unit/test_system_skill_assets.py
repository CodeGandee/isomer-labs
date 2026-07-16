from __future__ import annotations

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import isomer_labs.skills.system_assets as system_assets
from isomer_labs.skills.system_assets import (
    SystemSkillAssetError,
    callback_insertion_point_stage_names,
    has_system_skill_callback_insertion_point,
    iter_system_skill_callback_insertion_points,
    iter_system_skill_extensions,
    iter_system_skill_groups,
    iter_system_skill_paths,
    load_system_skill_manifest,
    materialize_system_skills,
    resolve_system_skill,
    system_skills_root,
)
from isomer_labs.kaoju.contracts import load_contract


class SystemSkillAssetTests(unittest.TestCase):
    def test_packaged_root_contains_distributable_skillset_only(self) -> None:
        root = system_skills_root()
        for name in ("manifest.toml", "README.md", "misc", "operator", "research", "research-paradigm", "service"):
            self.assertTrue(root.joinpath(name).exists(), name)
        self.assertFalse(root.joinpath("dev").exists())

    def test_manifest_groups_resolve_to_skills(self) -> None:
        groups = iter_system_skill_groups()
        self.assertEqual(("core", "deepsci", "kaoju"), tuple(group.name for group in groups))
        self.assertEqual(("core", "extension", "extension"), tuple(group.kind for group in groups))
        self.assertEqual((True, False, False), tuple(group.always_available for group in groups))
        self.assertEqual((None, "deepsci", "kaoju"), tuple(group.extension_id for group in groups))
        paths = iter_system_skill_paths()
        old_houmao_interop_path = "operator/" + "isomer-op-" + "houmao-interop"
        self.assertIn("operator/isomer-op-entrypoint", paths)
        self.assertIn("operator/isomer-op-gui-mgr", paths)
        self.assertIn("operator/isomer-op-project-mgr", paths)
        self.assertIn("operator/isomer-op-toolbox-mgr", paths)
        self.assertNotIn("operator/isomer-op-toolbox-creator", paths)
        self.assertIn("service/isomer-srv-houmao-interop", paths)
        self.assertIn("research/isomer-research-idea-recording", paths)
        self.assertNotIn(old_houmao_interop_path, paths)
        self.assertIn("research-paradigm/deepsci/isomer-deepsci-write", paths)
        self.assertIn("research-paradigm/kaoju/isomer-kaoju-pipeline", paths)
        self.assertIn("research-paradigm/kaoju/isomer-kaoju-synthesize", paths)
        for skill_path in paths:
            skill = resolve_system_skill(skill_path)
            self.assertTrue(skill.joinpath("SKILL.md").is_file(), skill_path)

    def test_manifest_lists_system_extensions(self) -> None:
        extensions = iter_system_skill_extensions()
        self.assertEqual(("deepsci", "kaoju"), tuple(extension.extension_id for extension in extensions))
        self.assertEqual(("deepsci", "kaoju"), tuple(extension.group for extension in extensions))
        self.assertEqual(("isomer-deepsci-pipeline", "isomer-kaoju-pipeline"), tuple(extension.entry_skill for extension in extensions))
        self.assertEqual("empirical-pass", extensions[0].commands[0])
        contract = load_contract()
        expected_commands = (*contract.survey_intents, *contract.compatibility_procedures, *(name for name in contract.manager_actions if name not in contract.survey_intents))
        self.assertEqual(expected_commands, extensions[1].commands)
        self.assertIn("research-paradigm/deepsci/isomer-deepsci-scout", extensions[0].skills)
        self.assertEqual(14, len(extensions[1].skills))
        self.assertIn("research-paradigm/kaoju/isomer-kaoju-pipeline", extensions[1].skills)

    def test_extension_pipeline_entrypoints_require_upfront_planning(self) -> None:
        for skill_path in (
            "research-paradigm/deepsci/isomer-deepsci-pipeline",
            "research-paradigm/kaoju/isomer-kaoju-pipeline",
        ):
            with self.subTest(skill_path=skill_path):
                text = resolve_system_skill(skill_path).joinpath("SKILL.md").read_text(encoding="utf-8")
                self.assertIn("## Plan First", text)
                self.assertIn("Pipeline execution is a complex process.", text)
                self.assertIn("use your internal todo list or planning tool to create a plan", text)
                self.assertLess(text.index("## Plan First"), text.index("## Overview"))

    def test_manifest_declares_callback_insertion_points(self) -> None:
        self.assertEqual(("begin", "end"), callback_insertion_point_stage_names())
        points = iter_system_skill_callback_insertion_points(include_core=True, include_all_extensions=True)
        self.assertEqual(72, len(points))
        self.assertEqual(
            ("isomer-deepsci-analysis", "begin"),
            (points[0].target_skill, points[0].stage),
        )
        self.assertEqual(
            ("isomer-kaoju-export", "end"),
            (points[-1].target_skill, points[-1].stage),
        )
        scout_begin = iter_system_skill_callback_insertion_points(
            include_core=False,
            extension_ids=("deepsci",),
            skill="isomer-deepsci-scout",
            stage="begin",
        )
        self.assertEqual(1, len(scout_begin))
        self.assertTrue(has_system_skill_callback_insertion_point("isomer-deepsci-scout", "begin"))
        kaoju_begin = iter_system_skill_callback_insertion_points(
            include_core=False,
            extension_ids=("kaoju",),
            skill="isomer-kaoju-pipeline",
            stage="begin",
        )
        self.assertEqual(1, len(kaoju_begin))
        self.assertTrue(has_system_skill_callback_insertion_point("isomer-kaoju-pipeline", "begin"))
        self.assertFalse(has_system_skill_callback_insertion_point("isomer-op-entrypoint", "begin"))

    def test_manifest_parse_and_callback_lookup_are_process_cached(self) -> None:
        system_assets._load_system_skill_manifest_cached.cache_clear()
        system_assets._all_system_skill_callback_insertion_points.cache_clear()
        system_assets._system_skill_callback_insertion_point_keys.cache_clear()
        with patch.object(system_assets.tomlkit, "parse", wraps=system_assets.tomlkit.parse) as parse:
            first = load_system_skill_manifest()
            second = load_system_skill_manifest()
            self.assertIsNot(first, second)
            self.assertEqual(first, second)
            self.assertTrue(has_system_skill_callback_insertion_point("isomer-deepsci-scout", "begin"))
            self.assertTrue(has_system_skill_callback_insertion_point("isomer-deepsci-scout", "begin"))
        self.assertEqual(1, parse.call_count)

    def test_callback_insertion_point_filters_reject_unknown_extension(self) -> None:
        with self.assertRaises(SystemSkillAssetError):
            iter_system_skill_callback_insertion_points(extension_ids=("unknown",))
        with self.assertRaises(SystemSkillAssetError):
            iter_system_skill_callback_insertion_points(extension_ids=("deepsci",), include_all_extensions=True)

    def test_manifest_rejects_invalid_group_metadata(self) -> None:
        manifest = deepcopy(load_system_skill_manifest())
        del manifest["groups"]["core"]["kind"]
        with patch.object(system_assets, "load_system_skill_manifest", return_value=manifest):
            with self.assertRaisesRegex(SystemSkillAssetError, "kind"):
                iter_system_skill_groups()

    def test_manifest_rejects_invalid_extension_discovery_metadata(self) -> None:
        mutations = (
            ("missing entry", lambda manifest: manifest["groups"]["kaoju"].pop("entry_skill"), "entry_skill"),
            (
                "unknown entry",
                lambda manifest: manifest["groups"]["kaoju"].__setitem__("entry_skill", "isomer-kaoju-missing"),
                "entry_skill",
            ),
            (
                "invalid command",
                lambda manifest: manifest["groups"]["kaoju"].__setitem__("commands", ["Not A Command"]),
                "commands",
            ),
            (
                "duplicate command",
                lambda manifest: manifest["groups"]["kaoju"].__setitem__("commands", ["landscape-pass", "landscape-pass"]),
                "duplicate commands",
            ),
            (
                "core metadata",
                lambda manifest: manifest["groups"]["core"].__setitem__("entry_skill", "isomer-op-entrypoint"),
                "must not define extension entry metadata",
            ),
        )
        for label, mutate, diagnostic in mutations:
            with self.subTest(label=label):
                manifest = deepcopy(load_system_skill_manifest())
                mutate(manifest)
                with patch.object(system_assets, "load_system_skill_manifest", return_value=manifest):
                    with self.assertRaisesRegex(SystemSkillAssetError, diagnostic):
                        iter_system_skill_groups()

    def test_materialize_selected_group_preserves_relative_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = materialize_system_skills(target, groups=("core",))
            self.assertEqual(("core",), result.groups)
            self.assertTrue((target / "manifest.toml").is_file())
            self.assertTrue((target / "operator" / "isomer-op-entrypoint" / "SKILL.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-entrypoint" / "agents" / "openai.yaml").is_file())
            self.assertTrue((target / "operator" / "isomer-op-entrypoint" / "references" / "extension-skill-index.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-gui-mgr" / "SKILL.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-gui-mgr" / "agents" / "openai.yaml").is_file())
            self.assertTrue((target / "operator" / "isomer-op-gui-mgr" / "commands" / "help.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-gui-mgr" / "commands" / "api-reference.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-project-mgr" / "SKILL.md").is_file())
            system_skill_manager = target / "operator" / "isomer-op-system-skill-mgr" / "SKILL.md"
            self.assertTrue(system_skill_manager.is_file())
            self.assertIn(
                "Direct low-level install defaults to project scope when `--scope` is omitted.",
                system_skill_manager.read_text(encoding="utf-8"),
            )
            self.assertTrue((target / "operator" / "isomer-op-toolbox-mgr" / "SKILL.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-toolbox-mgr" / "agents" / "openai.yaml").is_file())
            self.assertTrue((target / "operator" / "isomer-op-toolbox-mgr" / "commands" / "help.md").is_file())
            self.assertTrue((target / "operator" / "isomer-op-toolbox-mgr" / "commands" / "author-toolbox.md").is_file())
            self.assertFalse((target / "operator" / "isomer-op-toolbox-creator").exists())
            old_houmao_interop_name = "isomer-op-" + "houmao-interop"
            self.assertFalse((target / "operator" / old_houmao_interop_name).exists())
            self.assertTrue((target / "service" / "isomer-srv-houmao-interop" / "SKILL.md").is_file())
            self.assertTrue((target / "service" / "isomer-srv-topic-env-setup" / "SKILL.md").is_file())
            self.assertTrue((target / "research" / "isomer-research-idea-recording" / "SKILL.md").is_file())
            self.assertTrue((target / "research" / "isomer-research-idea-recording" / "references" / "recording-contract.md").is_file())
            self.assertFalse((target / "research-paradigm").exists())
            self.assertFalse((target / "dev").exists())

    def test_materialize_kaoju_group_includes_support_files_without_deepsci(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            result = materialize_system_skills(target, groups=("core", "kaoju"))
            self.assertEqual(("core", "kaoju"), result.groups)
            kaoju = target / "research-paradigm" / "kaoju"
            self.assertEqual(
                14,
                len(tuple(path for path in kaoju.glob("isomer-kaoju-*") if path.is_dir())),
            )
            self.assertTrue((kaoju / "isomer-kaoju-pipeline" / "commands" / "landscape-pass.md").is_file())
            self.assertTrue((kaoju / "isomer-kaoju-shared" / "references" / "evidence-contract.md").is_file())
            self.assertTrue((kaoju / "isomer-kaoju-shared" / "references" / "artifact-semantics.md").is_file())
            self.assertTrue((kaoju / "isomer-kaoju-shared" / "references" / "artifact-recording.md").is_file())
            self.assertTrue((kaoju / "isomer-kaoju-shared" / "references" / "research-idea-recording.md").is_file())
            neutral_recording = target / "research" / "isomer-research-idea-recording" / "SKILL.md"
            self.assertTrue(neutral_recording.is_file())
            self.assertNotIn("isomer-deepsci", neutral_recording.read_text(encoding="utf-8"))
            binding_pages = tuple(kaoju.glob("isomer-kaoju-*/artifact-bindings.md"))
            self.assertEqual(13, len(binding_pages))
            self.assertFalse((kaoju / "contracts").exists())
            for skill_dir in kaoju.glob("isomer-kaoju-*"):
                self.assertFalse(skill_dir.is_symlink(), skill_dir)
                self.assertTrue((skill_dir / "SKILL.md").is_file(), skill_dir)
            for path in kaoju.rglob("*.md"):
                text = path.read_text(encoding="utf-8")
                self.assertNotIn("../contracts", text, path)
                self.assertNotIn("contracts/bindings.v2.json", text, path)
            self.assertFalse((target / "research-paradigm" / "deepsci").exists())

    def test_research_idea_recording_contract_is_producer_neutral_and_facet_first(self) -> None:
        skill = resolve_system_skill("research/isomer-research-idea-recording")
        skill_text = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
        contract = skill.joinpath("references", "recording-contract.md").read_text(encoding="utf-8")
        self.assertIn("$isomer-research-idea-recording", skill.joinpath("agents", "openai.yaml").read_text(encoding="utf-8"))
        self.assertIn("research_idea_effects", contract)
        self.assertIn("exploration_state", contract)
        self.assertIn("decision options", contract.lower())
        self.assertIn("exact object-valued JSON path", contract)
        self.assertIn("Accepted-Output Verification", contract)
        self.assertNotIn("idea status changes require", skill_text.lower())
        self.assertNotIn("isomer-deepsci", skill_text)

    def test_gui_mgr_skill_identity_commands_and_api_reference(self) -> None:
        skill = resolve_system_skill("operator/isomer-op-gui-mgr")
        skill_md = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
        agent_yaml = skill.joinpath("agents", "openai.yaml").read_text(encoding="utf-8")
        self.assertIn("name: isomer-op-gui-mgr", skill_md)
        self.assertIn("description: Use when", skill_md)
        self.assertIn("## Workflow", skill_md)
        self.assertIn("## Output Contract", skill_md)
        self.assertIn("## Guardrails", skill_md)
        self.assertIn("isomer-cli project web serve --root <project-root>", skill_md)
        self.assertNotIn("pixi run isomer-cli", skill_md)
        self.assertIn('display_name: "isomer-op-gui-mgr"', agent_yaml)
        self.assertIn("$isomer-op-gui-mgr", agent_yaml)

        for command_name in (
            "help",
            "launch",
            "status",
            "api-reference",
            "refresh-records",
            "troubleshoot",
        ):
            command = skill.joinpath("commands", f"{command_name}.md")
            self.assertTrue(command.is_file(), command_name)
            command_text = command.read_text(encoding="utf-8")
            self.assertIn("## Workflow", command_text, command_name)
            self.assertIn("does not map cleanly", command_text, command_name)
            self.assertNotIn("pixi run isomer-cli", command_text, command_name)

        launch = skill.joinpath("commands", "launch.md").read_text(encoding="utf-8")
        for option in ("--host", "--port", "--reload", "--no-browser", "--cache-mode normal", "--cache-mode debug"):
            self.assertIn(option, launch)

        api_reference = skill.joinpath("commands", "api-reference.md").read_text(encoding="utf-8")
        for route_family in (
            "/api/health",
            "/api/project",
            "/api/topics",
            "/api/explorer/project",
            "/api/openable/{openable_item_id}",
            "/api/topics/{topic_id}/runtime",
            "/api/topics/{topic_id}/overview",
            "/api/topics/{topic_id}/actors",
            "/api/topics/{topic_id}/records",
            "/api/topics/{topic_id}/records/export",
            "/api/topics/{topic_id}/graphs/{graph_scope}",
            "/api/topics/{topic_id}/recent-errors",
            "/api/events",
            "/api/topics/{topic_id}/records/{record_id}",
            "/api/topics/{topic_id}/ideas/{idea_id}",
            "/api/topics/{topic_id}/viewer/records/{record_id}",
            "/api/topics/{topic_id}/records/{record_id}/render",
            "/api/topics/{topic_id}/records/{record_id}/lineage",
            "/api/topics/{topic_id}/records/{record_id}/siblings",
            "/api/topics/{topic_id}/records/{record_id}/files",
            "/api/topics/{topic_id}/records/{record_id}/facets",
            "/api/topics/{topic_id}/records/index/validate",
            "/api/topics/{topic_id}/records/index/rebuild",
            "/api/topics/{topic_id}/records/index/cleanup",
        ):
            self.assertIn(route_family, api_reference)
        self.assertIn("docs/ui/contracts/", api_reference)
        self.assertIn("Read-only", api_reference)
        self.assertIn("Explicit mutation", api_reference)

    def test_gui_mgr_is_discoverable_from_welcome_and_entrypoint(self) -> None:
        entrypoint = resolve_system_skill("operator/isomer-op-entrypoint")
        system_index = entrypoint.joinpath("references", "system-skill-index.md").read_text(encoding="utf-8")
        self.assertIn("isomer-op-gui-mgr", system_index)
        self.assertIn("Project Web GUI lifecycle", system_index)
        self.assertIn("backend API reference", system_index)

        welcome = resolve_system_skill("operator/isomer-op-welcome")
        for reference_name in ("help", "show-options", "choose-path", "show-skill-map"):
            reference = welcome.joinpath("references", f"{reference_name}.md").read_text(encoding="utf-8")
            self.assertIn("isomer-op-gui-mgr", reference, reference_name)
        welcome_skill = welcome.joinpath("SKILL.md").read_text(encoding="utf-8")
        self.assertIn("Project Web GUI", welcome_skill)
        self.assertIn("isomer-op-gui-mgr", welcome_skill)

    def test_extensions_and_entrypoint_are_discoverable_from_welcome(self) -> None:
        welcome = resolve_system_skill("operator/isomer-op-welcome")
        skill_text = welcome.joinpath("SKILL.md").read_text(encoding="utf-8")
        for term in (
            "start-deepsci-research",
            "start-kaoju-survey",
            "show-extensions",
            "isomer-op-entrypoint",
            "isomer-op-system-skill-mgr",
            "isomer-deepsci-pipeline",
            "isomer-kaoju-pipeline",
        ):
            self.assertIn(term, skill_text)

        extension_reference = welcome.joinpath("references", "show-extensions.md").read_text(encoding="utf-8")
        for term in (
            "system-skills extensions list",
            "project system-extensions list",
            "catalog-known",
            "Project-declared",
            "Host-usable",
            "isomer-op-system-skill-mgr",
        ):
            self.assertIn(term, extension_reference)

        deepsci_path = welcome.joinpath("references", "start-deepsci-research.md").read_text(encoding="utf-8")
        kaoju_path = welcome.joinpath("references", "start-kaoju-survey.md").read_text(encoding="utf-8")
        self.assertIn("isomer-deepsci-pipeline", deepsci_path)
        self.assertIn("isomer-kaoju-pipeline", kaoju_path)
        self.assertIn("execution topology", deepsci_path)
        self.assertIn("execution topology", kaoju_path)

    def test_kaoju_is_discoverable_from_operator_entrypoint(self) -> None:
        entrypoint = resolve_system_skill("operator/isomer-op-entrypoint")
        skill_text = entrypoint.joinpath("SKILL.md").read_text(encoding="utf-8")
        input_surfaces = entrypoint.joinpath("references", "input-surfaces.md").read_text(encoding="utf-8")
        routing_rules = entrypoint.joinpath("references", "routing-rules.md").read_text(encoding="utf-8")
        extension_index = entrypoint.joinpath("references", "extension-skill-index.md").read_text(encoding="utf-8")
        self.assertIn("isomer-kaoju-workspace-mgr", skill_text)
        self.assertIn("$isomer-kaoju-*", input_surfaces)
        self.assertIn("isomer-kaoju-pipeline", routing_rules)
        for name in (
            "isomer-kaoju-pipeline",
            "isomer-kaoju-shared",
            "isomer-kaoju-workspace-mgr",
            "isomer-kaoju-frame",
            "isomer-kaoju-discover",
            "isomer-kaoju-acquire",
            "isomer-kaoju-examine",
            "isomer-kaoju-reproduce",
            "isomer-kaoju-trial",
            "isomer-kaoju-compare",
            "isomer-kaoju-audit",
            "isomer-kaoju-synthesize",
            "isomer-kaoju-write",
            "isomer-kaoju-export",
        ):
            self.assertIn(name, extension_index)

    def test_toolbox_mgr_skill_identity_and_command_pages(self) -> None:
        skill_path = "operator/isomer-op-toolbox-mgr"
        skill = resolve_system_skill(skill_path)
        skill_md = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: isomer-op-toolbox-mgr", skill_md)
        self.assertNotIn("name: isomer-op-toolbox-creator", skill_md)
        self.assertIn("description: Use when", skill_md)
        self.assertIn("## Workflow", skill_md)
        self.assertIn("### Procedural Subcommands", skill_md)
        self.assertIn("### Helper Subcommands", skill_md)
        for command_name in (
            "author-toolbox",
            "convert-skill",
            "insert-callback",
            "define-runtime-params",
            "manage-toolbox",
            "identify-insertion-points",
            "author-toolbox-source",
            "edit-callback-declarations",
            "edit-runtime-params",
            "inspect-effective-state",
            "help",
        ):
            command = skill.joinpath("commands", f"{command_name}.md")
            self.assertTrue(command.is_file(), command_name)
            self.assertIn("## Workflow", command.read_text(encoding="utf-8"), command_name)

    def test_topic_service_agent_support_declares_lifecycle_routes(self) -> None:
        skill = resolve_system_skill("service/isomer-srv-topic-service-agent-support")
        skill_md = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
        for route_name in (
            "prepare-topic-service-master",
            "launch-topic-service-master",
            "inspect-topic-service-master",
            "stop-topic-service-master",
            "repair-topic-service-master",
        ):
            reference = skill.joinpath("references", f"{route_name}.md")
            self.assertTrue(reference.is_file(), route_name)
            reference_text = reference.read_text(encoding="utf-8")
            self.assertIn(f"skill-context {route_name}", reference_text)
            self.assertIn("--project-dir <houmao_project_path>", reference_text)
            self.assertIn("implicit `.houmao/` discovery", reference_text)
            self.assertIn(route_name, skill_md)

    def test_houmao_interop_routes_through_isomer_skill_context(self) -> None:
        skill = resolve_system_skill("service/isomer-srv-houmao-interop")
        skill_md = skill.joinpath("SKILL.md").read_text(encoding="utf-8")
        self.assertIn("isomer-cli --print-json project integrations houmao skill-context <route-name>", skill_md)
        self.assertIn("houmao_skill_path", skill_md)
        self.assertIn("--project-dir <houmao_project_path>", skill_md)
        self.assertTrue(skill.joinpath("references", "skill-context.md").is_file())

    def test_topic_creator_reports_disabled_houmao_skip(self) -> None:
        skill = resolve_system_skill("operator/isomer-op-topic-creator")
        setup_actors = skill.joinpath("references", "setup-actors.md").read_text(encoding="utf-8")
        finalize = skill.joinpath("references", "finalize.md").read_text(encoding="utf-8")
        status = skill.joinpath("references", "status.md").read_text(encoding="utf-8")
        self.assertIn("record skipped Topic Service Master preparation", setup_actors)
        self.assertIn("prepare-topic-service-master", setup_actors)
        self.assertIn("Project Manifest Houmao integration evidence", finalize)
        self.assertIn("disabled Houmao integration as a skip state", status)

    def test_pixi_wrapper_tool_command_shape_guidance_is_packaged(self) -> None:
        topic_env = resolve_system_skill("service/isomer-srv-topic-env-setup")
        derive = topic_env.joinpath("references", "derive-env-gate.md").read_text(encoding="utf-8")
        verify = topic_env.joinpath("references", "verify-env-gate.md").read_text(encoding="utf-8")
        bounded = resolve_system_skill("misc/isomer-misc-bounded-run-tips").joinpath("SKILL.md").read_text(encoding="utf-8")
        nvidia = resolve_system_skill("misc/isomer-misc-nvidia-tools").joinpath("SKILL.md").read_text(encoding="utf-8")

        for text in (derive, verify, bounded):
            self.assertIn("wrapper tools", text)
            self.assertIn("pixi run", text)
            self.assertIn("<wrapper-tool> pixi run", text)
            self.assertIn("ncu", text)
            self.assertIn("valgrind", text)
            self.assertIn("gdb", text)

        self.assertIn("pixi run ncu", bounded)
        self.assertIn("pixi run valgrind", bounded)
        self.assertIn("pixi run gdb --args", bounded)
        self.assertIn("ncu pixi run", bounded)

        self.assertIn("pixi run ncu", nvidia)
        self.assertIn("pixi run nsys profile", nvidia)
        self.assertIn("pixi run cuda-gdb --args", nvidia)
        self.assertIn("ncu pixi run", nvidia)

    def test_materialize_refuses_non_empty_target(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / "existing.txt").write_text("existing", encoding="utf-8")
            with self.assertRaises(SystemSkillAssetError):
                materialize_system_skills(target, groups=("core",))

    def test_rejects_unsafe_manifest_relative_paths(self) -> None:
        with self.assertRaises(SystemSkillAssetError):
            resolve_system_skill("../dev/isomer-dev-migrate-deepsci-skill")


if __name__ == "__main__":
    unittest.main()
