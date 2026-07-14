from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import shutil
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_PATH = REPO_ROOT / "scripts" / "validate_research_paradigm_skillset.py"
SPEC = importlib.util.spec_from_file_location("validate_research_paradigm_skillset", SCRIPT_PATH)
assert SPEC is not None
assert SPEC.loader is not None
validator = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = validator
SPEC.loader.exec_module(validator)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def codes(diagnostics: list[object]) -> set[str]:
    return {diagnostic.code for diagnostic in diagnostics}


def messages(diagnostics: list[object]) -> list[str]:
    return [diagnostic.render() for diagnostic in diagnostics]


def mutate_json(path: Path, callback: object) -> None:
    raw = json.loads(path.read_text(encoding="utf-8"))
    assert callable(callback)
    callback(raw)
    path.write_text(json.dumps(raw, indent=2) + "\n", encoding="utf-8")


class ResearchParadigmValidatorTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        write(root / "pyproject.toml", "[project]\nname = \"fixture\"\n")
        return root

    def test_workspace_manager_requires_qualified_team_specialization_gate(self) -> None:
        root = self.make_root()
        target = root / "skillset" / "research-paradigm"
        reference = (
            target
            / "deepsci"
            / "isomer-deepsci-workspace-mgr"
            / "references"
            / "validation-and-blockers.md"
        )
        write(reference, "# Validation and Blockers\n\nA missing summary always routes to Topic Team Specialization.\n")
        diagnostics: list[object] = []

        validator.validate_workspace_manager_team_specialization_gate(target, root, diagnostics)

        self.assertIn("RPS025", codes(diagnostics))
        self.assertTrue(any("Topic Team Specialization gate phrase" in message for message in messages(diagnostics)))

    def test_workspace_manager_accepts_formal_team_and_non_team_branches(self) -> None:
        root = self.make_root()
        target = root / "skillset" / "research-paradigm"
        reference = (
            target
            / "deepsci"
            / "isomer-deepsci-workspace-mgr"
            / "references"
            / "validation-and-blockers.md"
        )
        write(
            reference,
            """
            # Validation and Blockers

            When the selected topology includes a formal Agent Team layer, a missing summary is a specialization blocker.
            When no formal Agent Team layer is selected, validate base readiness without inferring specialization.
            """,
        )
        diagnostics: list[object] = []

        validator.validate_workspace_manager_team_specialization_gate(target, root, diagnostics)

        self.assertEqual([], messages(diagnostics))

    def test_release_version_metadata_rejects_missing_malformed_and_mismatched_values(self) -> None:
        root = self.make_root()
        manifest = root / "agents" / "openai.yaml"
        cases = (
            ("interface: {}\n", "metadata.version is required"),
            ('metadata:\n  version: "latest"\n', "not valid PEP 440"),
            ('metadata:\n  version: "0.2.2"\n', "must match Isomer release"),
        )
        for yaml_text, expected_message in cases:
            with self.subTest(expected_message=expected_message):
                write(manifest, yaml_text)
                diagnostics: list[object] = []
                validator.validate_release_version_metadata(
                    manifest,
                    "0.3.0rc1",
                    root,
                    diagnostics,
                    "RPS006",
                )
                self.assertTrue(any(expected_message in message for message in messages(diagnostics)))

    def make_valid_skillset(self) -> tuple[Path, Path]:
        root = self.make_root()
        target = root / "skillset" / "research-paradigm"
        deepsci_root = target / "deepsci"
        for name in sorted(validator.EXPECTED_DEEPSCI_SKILLS):
            self.write_skill(deepsci_root, name, v2=True)
        write(
            deepsci_root / "isomer-deepsci-shared" / "references" / "semantic-placeholders.md",
            """
            # V2 Semantic Placeholders

            | ID | Meaning | Required semantic content | Typical producers | Typical consumers | Storage-binding status |
            | --- | --- | --- | --- | --- | --- |
            | `research-frame` | Research frame. | Objective, metric, constraints, and next route. | `isomer-deepsci-scout` | Any production DeepSci skill | Not storage-bound yet. |
            """,
        )
        write(
            deepsci_root / "isomer-deepsci-shared" / "references" / "tbd-surface-registry.md",
            """
            # TBD Surface Registry

            ## Resolved Workspace Path Surfaces

            | Former ID | Resolution |
            | --- | --- |
            | path-topic-workspace | Use Topic Workspace through Workspace Path Resolution. |

            ## Open Surfaces

            | ID | Resolution |
            | --- | --- |
            | provider-new | Use a registered provider binding. |
            """,
        )
        return root, target

    def add_valid_kaoju(self, target: Path) -> Path:
        source = (
            REPO_ROOT
            / "src"
            / "isomer_labs"
            / "assets"
            / "system_skills"
            / "research-paradigm"
            / "kaoju"
        )
        destination = target / "kaoju"
        shutil.copytree(source, destination)
        return destination

    def write_skill(
        self,
        target: Path,
        name: str,
        *,
        reference: str = "",
        workflow_extra: str = "",
        routing_extra: str = "",
        display_name: str | None = None,
        prompt_skill: str | None = None,
        v2: bool,
    ) -> None:
        load_step = f"1. **Load context**. Read `{reference}` first." if reference else "1. **Load context**. Read `isomer-deepsci-shared` first."
        begin_step = (
            f"2. **Apply begin callbacks**. Resolve `begin` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill {name} --stage begin` after mandatory context or entry-fit checks and before the first skill-specific action. "
            "Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow."
        )
        output_step = (
            "3. **Produce semantics**. Produce [[rsch-object:research-frame]] with enough content for the next method step."
            if v2
            else "3. **Record output**. Use Research Topic, Artifacts, and Decision Records."
        )
        end_step = (
            f"4. **Apply end callbacks**. After tentative outputs exist and before final response, handoff, or treating the workflow as complete, resolve `end` callbacks with `isomer-cli --print-json project skill-callbacks resolve --skill {name} --stage end`. "
            "Follow returned instructions within this skill, `isomer-deepsci-shared`, current user request, evidence, gate, and validation constraints; empty callback results continue normally, and conflicts must be reported when they affect the workflow."
        )
        shared_worker_policy = (
            (
                "## Worker Output Policy\n\n"
                "            Resolve `project outputs policy`, write plain generated files under an operation-specific child set, respect `.gitignore`, and check `commit_after_operation`.\n"
            )
            if name == "isomer-deepsci-shared"
            else ""
        )
        routing_line = f"- `{reference}` for local terminology." if reference else "- Read `isomer-deepsci-shared` for placeholder semantics."
        write(
            target / name / "SKILL.md",
            f"""
            ---
            name: {name}
            description: Use when a valid fixture skill is needed.
            ---

            # {name}

            ## Overview

            Use this fixture for validator tests.

            Structured payloads use the supported DeepSci v2 display contract: write non-empty top-level `title` and `summary` strings, and give every idea-bearing object that can become a Research Idea its own non-empty `title` and `summary`. Use labels, candidate ids, and aliases only as extra identifiers, not as replacements for display fields.

            {shared_worker_policy}

            ## Workflow

            When this skill is invoked, execute the following steps in order.

            {load_step}
            {begin_step}
            {output_step}
            {workflow_extra}
            {end_step}

            If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

            ## Reference Routing

            {routing_line}
            {routing_extra}
            """,
        )
        write(
            target / name / "agents" / "openai.yaml",
            f"""
            interface:
              display_name: "{display_name or name}"
              short_description: "Valid fixture"
              default_prompt: "Use ${prompt_skill or name} to validate this fixture."
            """,
        )
        if reference:
            ref_path = target / name / reference
            if not ref_path.exists():
                write(ref_path, "# Reference\n\nFixture reference.\n")

    def assert_no_codes(self, diagnostics: list[object], unexpected: set[str]) -> None:
        present = codes(diagnostics) & unexpected
        self.assertFalse(present, messages(diagnostics))

    def write_placeholder_bindings(self, skill_dir: Path, placeholders: list[str]) -> None:
        rows = "".join(f"| <{placeholder}> | artifact |\n" for placeholder in placeholders)
        write(
            skill_dir / "placeholder-bindings.md",
            (
                "# Placeholder Bindings\n\n"
                "| Placeholder | Kind |\n"
                "| --- | --- |\n"
                f"{rows}"
            ),
        )

    def test_minimal_valid_research_paradigm_skillset_passes(self) -> None:
        root, target = self.make_valid_skillset()
        diagnostics = validator.validate_skillset(target, root)
        self.assertEqual([], messages(diagnostics))

    def test_valid_kaoju_family_passes_with_deepsci_fixture(self) -> None:
        root, target = self.make_valid_skillset()
        self.add_valid_kaoju(target)

        diagnostics = validator.validate_skillset(target, root)

        self.assertEqual([], messages(diagnostics))

    def test_kaoju_binding_invalid_fixtures_are_rejected(self) -> None:
        cases = {
            "missing": ("isomer-kaoju-workspace-mgr/artifact-bindings.md", lambda path: path.unlink(), "RPS022"),
            "duplicate": (
                "contracts/bindings.v2.json",
                lambda path: mutate_json(path, lambda raw: raw["bindings"].append(dict(raw["bindings"][0]))),
                "RPS021",
            ),
            "cross-family": (
                "contracts/bindings.v2.json",
                lambda path: mutate_json(path, lambda raw: raw["bindings"][0].__setitem__("semantic_id", "other:survey-contract")),
                "RPS021",
            ),
            "summary-unresolved": (
                "isomer-kaoju-frame/artifact-bindings.md",
                lambda path: path.write_text(path.read_text(encoding="utf-8").replace("kaoju:survey-contract", "kaoju:unknown-contract"), encoding="utf-8"),
                "RPS022",
            ),
            "unknown-producer": (
                "contracts/bindings.v2.json",
                lambda path: mutate_json(path, lambda raw: raw["bindings"][0].__setitem__("producer", "isomer-kaoju-missing")),
                "RPS022",
            ),
            "physical-command": (
                "isomer-kaoju-audit/artifact-bindings.md",
                lambda path: path.write_text(path.read_text(encoding="utf-8") + "\nUse --record-kind artifact.\n", encoding="utf-8"),
                "RPS023",
            ),
            "stale-profile": (
                "contracts/bindings.v2.json",
                lambda path: mutate_json(path, lambda raw: raw["bindings"][0].__setitem__("profile_ref", "isomer:research/record-format/profile/kaoju/control/workspace-readiness/v2")),
                "RPS022",
            ),
            "missing-typed-operation": (
                "isomer-kaoju-audit/artifact-bindings.md",
                lambda path: path.write_text(path.read_text(encoding="utf-8").replace("project artifacts revise", "project records revise"), encoding="utf-8"),
                "RPS024",
            ),
            "summary-drift": (
                "isomer-kaoju-shared/references/artifact-semantics.md",
                lambda path: path.write_text(path.read_text(encoding="utf-8").replace("`kaoju:workspace-readiness`", "`kaoju:unknown`", 1), encoding="utf-8"),
                "RPS022",
            ),
        }
        for name, (relative_path, mutate, expected_code) in cases.items():
            with self.subTest(name=name):
                root, target = self.make_valid_skillset()
                kaoju = self.add_valid_kaoju(target)
                mutate(kaoju / relative_path)
                diagnostics = validator.validate_skillset(target, root)
                self.assertIn(expected_code, codes(diagnostics), messages(diagnostics))

    def test_kaoju_architecture_guidance_drift_is_rejected(self) -> None:
        root, target = self.make_valid_skillset()
        kaoju = self.add_valid_kaoju(target)
        shared = kaoju / "isomer-kaoju-shared" / "SKILL.md"
        shared.write_text(shared.read_text(encoding="utf-8").replace("state DB", "filesystem catalog"), encoding="utf-8")
        export = kaoju / "isomer-kaoju-export" / "SKILL.md"
        export.write_text(export.read_text(encoding="utf-8") + "\nInvoke imsight-llm-wiki for viewer export.\n", encoding="utf-8")

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS027", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("state DB" in message or "external imsight-llm-wiki" in message for message in messages(diagnostics)))

    def test_kaoju_missing_skill_is_rejected(self) -> None:
        root, target = self.make_valid_skillset()
        kaoju = self.add_valid_kaoju(target)
        shutil.rmtree(kaoju / "isomer-kaoju-acquire")

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS007", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("expected kaoju skill is missing" in message for message in messages(diagnostics)))

    def test_kaoju_wrong_namespace_is_rejected(self) -> None:
        root, target = self.make_valid_skillset()
        kaoju = self.add_valid_kaoju(target)
        (kaoju / "isomer-kaoju-acquire").rename(kaoju / "isomer-ext-acquire")

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS007", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("must match isomer-kaoju-*" in message for message in messages(diagnostics)))

    def test_kaoju_manifest_identity_drift_is_rejected(self) -> None:
        root, target = self.make_valid_skillset()
        kaoju = self.add_valid_kaoju(target)
        manifest = kaoju / "isomer-kaoju-frame" / "agents" / "openai.yaml"
        text = manifest.read_text(encoding="utf-8").replace(
            'display_name: "isomer-kaoju-frame"',
            'display_name: "isomer-kaoju-other"',
        )
        manifest.write_text(text, encoding="utf-8")

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS006", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("isomer-kaoju-frame" in message for message in messages(diagnostics)))

    def test_kaoju_broken_direct_reference_is_rejected(self) -> None:
        root, target = self.make_valid_skillset()
        kaoju = self.add_valid_kaoju(target)
        missing = kaoju / "isomer-kaoju-shared" / "references" / "evidence-contract.md"
        missing.unlink()

        diagnostics = validator.validate_skillset(target, root)

        self.assertTrue({"RPS005", "RPS019"} <= codes(diagnostics), messages(diagnostics))

    def test_kaoju_stale_domain_term_is_rejected(self) -> None:
        root, target = self.make_valid_skillset()
        kaoju = self.add_valid_kaoju(target)
        skill = kaoju / "isomer-kaoju-frame" / "SKILL.md"
        skill.write_text(skill.read_text(encoding="utf-8") + "\nUse the Research Goal as context.\n", encoding="utf-8")

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS001", codes(diagnostics), messages(diagnostics))

    def test_kaoju_hard_coded_provider_and_local_path_are_rejected(self) -> None:
        root, target = self.make_valid_skillset()
        kaoju = self.add_valid_kaoju(target)
        skill = kaoju / "isomer-kaoju-discover" / "SKILL.md"
        skill.write_text(
            skill.read_text(encoding="utf-8") + "\nAlways use GitHub and store results under /data/kaoju/results.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertTrue({"RPS004", "RPS020"} <= codes(diagnostics), messages(diagnostics))

    def test_kaoju_command_surface_drift_is_rejected(self) -> None:
        root, target = self.make_valid_skillset()
        kaoju = self.add_valid_kaoju(target)
        write(
            kaoju / "isomer-kaoju-pipeline" / "commands" / "source-audit.md",
            """
            # Source Audit

            ## Workflow

            1. Inspect a source.
            2. Return a report.

            If the task does not map cleanly, use the native planning tool.
            """,
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS018", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("source-audit" in message for message in messages(diagnostics)))

    def test_deepsci_callback_steps_are_required(self) -> None:
        root, target = self.make_valid_skillset()
        skill_md = target / "deepsci" / "isomer-deepsci-scout" / "SKILL.md"
        text = skill_md.read_text(encoding="utf-8")
        text = "\n".join(line for line in text.splitlines() if "Apply begin callbacks" not in line)
        skill_md.write_text(text + "\n", encoding="utf-8")

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS017", codes(diagnostics), messages(diagnostics))

    def test_deepsci_callback_reminder_antipattern_is_rejected(self) -> None:
        root, target = self.make_valid_skillset()
        skill_md = target / "deepsci" / "isomer-deepsci-scout" / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8")
            + "\nUser Skill Callback reminder: resolve begin and end callbacks from outside the numbered workflow.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS017", codes(diagnostics), messages(diagnostics))

    def test_research_validator_rejects_repo_local_isomer_cli_wrapper(self) -> None:
        root, target = self.make_valid_skillset()
        write(
            target / "deepsci" / "isomer-deepsci-scout" / "placeholder-bindings.md",
            "# Placeholder Bindings\n\nRun `pixi run isomer-cli ext research records list`.\n",
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS013", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("global isomer-cli directly" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_latest_context_preflight_required_for_v2_record_binding_skill(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_placeholder_bindings(target / "deepsci" / "isomer-deepsci-scout", [])

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS016", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("latest-context" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_latest_context_preflight_accepts_concise_shared_import(self) -> None:
        root, target = self.make_valid_skillset()
        skill_dir = target / "deepsci" / "isomer-deepsci-scout"
        self.write_placeholder_bindings(skill_dir, [])
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8")
            + "\nLatest-context reminder: before accepted durable record writes, follow `isomer-deepsci-shared` Latest Context Preflight, capture `latest-context-snapshot`, and do not trust prompt memory, chat memory, prior prose, older rendered records, remembered research state, or worker-local files until checked.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertNotIn("RPS016", codes(diagnostics), messages(diagnostics))

    def test_worker_output_guidance_does_not_satisfy_latest_context_preflight(self) -> None:
        root, target = self.make_valid_skillset()
        skill_dir = target / "deepsci" / "isomer-deepsci-scout"
        self.write_placeholder_bindings(skill_dir, [])
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8")
            + "\nWorker-output reminder: resolve `project outputs policy`, write plain generated files under an operation-specific child set, and check `commit_after_operation`.\n",
            encoding="utf-8",
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS016", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("worker-output guidance does not satisfy" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_payload_first_placeholder_binding_is_allowed(self) -> None:
        root, target = self.make_valid_skillset()
        skill_dir = target / "deepsci" / "isomer-deepsci-scout"
        write(skill_dir / "migrate" / "placeholders.md", "| Placeholder | Meaning |\n| --- | --- |\n| <SCOUT_CONTEXT_BRIEF> | Context. |\n")
        write(
            skill_dir / "placeholder-bindings.md",
            """
            # Placeholder Bindings

            For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create the record with `--payload-file <payload-file>`.

            Every structured payload file must include non-empty top-level `title` and `summary` strings. If the payload contains idea-bearing entries that can become canonical Research Ideas, each accepted idea object must include its own non-empty `title` and `summary`.

            Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect stored payload data. Render Markdown on demand with `isomer-cli --print-json ext research records render <record-id> --topic <topic>`; add `--output-file <path>` only for an explicit Markdown export.

            | Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
            | --- | --- | --- | --- | --- | --- | --- |
            | <SCOUT_CONTEXT_BRIEF> | evidence | Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/scout-context-brief/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCOUT_CONTEXT_BRIEF>' --format-profile isomer:deepsci/record-format/profile/evidence/scout-context-brief/v2 --payload-file <payload-file>` |
            """,
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertNotIn("RPS014", codes(diagnostics), messages(diagnostics))

    def test_payload_first_placeholder_binding_rejects_body_file_and_bare_profile(self) -> None:
        root, target = self.make_valid_skillset()
        skill_dir = target / "deepsci" / "isomer-deepsci-scout"
        write(skill_dir / "migrate" / "placeholders.md", "| Placeholder | Meaning |\n| --- | --- |\n| <SCOUT_CONTEXT_BRIEF> | Context. |\n")
        write(
            skill_dir / "placeholder-bindings.md",
            """
            # Placeholder Bindings

            For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create the record with `--payload-file <payload-file>`.

            Every structured payload file must include non-empty top-level `title` and `summary` strings. If the payload contains idea-bearing entries that can become canonical Research Ideas, each accepted idea object must include its own non-empty `title` and `summary`.

            Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect stored payload data. Render Markdown on demand with `isomer-cli --print-json ext research records render <record-id> --topic <topic>`; add `--output-file <path>` only for an explicit Markdown export.

            | Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
            | --- | --- | --- | --- | --- | --- | --- |
            | <SCOUT_CONTEXT_BRIEF> | evidence | Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/scout-context-brief/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCOUT_CONTEXT_BRIEF>' --profile evidence.scout-context-brief --body-file <body-file>` |
            """,
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS014", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("--format-profile" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_payload_first_placeholder_binding_rejects_default_markdown_render(self) -> None:
        root, target = self.make_valid_skillset()
        skill_dir = target / "deepsci" / "isomer-deepsci-scout"
        write(skill_dir / "migrate" / "placeholders.md", "| Placeholder | Meaning |\n| --- | --- |\n| <SCOUT_CONTEXT_BRIEF> | Context. |\n")
        write(
            skill_dir / "placeholder-bindings.md",
            """
            # Placeholder Bindings

            For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create the record with `--payload-file <payload-file>`.

            Every structured payload file must include non-empty top-level `title` and `summary` strings. If the payload contains idea-bearing entries that can become canonical Research Ideas, each accepted idea object must include its own non-empty `title` and `summary`.

            Use `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload` to inspect stored payload data. Render Markdown on demand with `isomer-cli --print-json ext research records render <record-id> --topic <topic>`; add `--output-file <path>` only for an explicit Markdown export.

            | Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
            | --- | --- | --- | --- | --- | --- | --- |
            | <SCOUT_CONTEXT_BRIEF> | evidence | Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/scout-context-brief/v2` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCOUT_CONTEXT_BRIEF>' --format-profile isomer:deepsci/record-format/profile/evidence/scout-context-brief/v2 --payload-file <payload-file> --render markdown --content-name scout-context-brief.md` |
            """,
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS014", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("durable Markdown" in message for message in messages(diagnostics)), messages(diagnostics))
        self.assertTrue(any("--content-name" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_expected_inventory_includes_expanded_deepsci_contract(self) -> None:
        self.assertIn("isomer-deepsci-write", validator.EXPECTED_DEEPSCI_SKILLS)
        self.assertIn("isomer-deepsci-paper-outline", validator.EXPECTED_DEEPSCI_SKILLS)
        self.assertIn("isomer-deepsci-paper-plot", validator.EXPECTED_DEEPSCI_SKILLS)
        self.assertIn("isomer-deepsci-figure-polish", validator.EXPECTED_DEEPSCI_SKILLS)
        self.assertIn("isomer-deepsci-review", validator.EXPECTED_DEEPSCI_SKILLS)
        self.assertIn("isomer-deepsci-rebuttal", validator.EXPECTED_DEEPSCI_SKILLS)
        self.assertIn("isomer-deepsci-nature-data", validator.EXPECTED_DEEPSCI_SKILLS)
        self.assertIn("isomer-deepsci-nature-figure", validator.EXPECTED_DEEPSCI_SKILLS)

    def test_deepsci_skills_teach_canonical_lineage_recording(self) -> None:
        packaged_root = REPO_ROOT / "src" / "isomer_labs" / "assets" / "system_skills" / "research-paradigm" / "deepsci"
        shared_ref = packaged_root / "isomer-deepsci-shared" / "references" / "artifact-lineage-recording.md"
        self.assertTrue(shared_ref.exists(), shared_ref)
        shared_text = shared_ref.read_text(encoding="utf-8")
        self.assertIn("--parents-json", shared_text)
        self.assertIn("generation group", shared_text)
        for skill_name in ("isomer-deepsci-idea", "isomer-deepsci-optimize", "isomer-deepsci-experiment", "isomer-deepsci-analysis", "isomer-deepsci-decision", "isomer-deepsci-write", "isomer-deepsci-review", "isomer-deepsci-finalize"):
            skill_text = (packaged_root / skill_name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Lineage reminder", skill_text)
            self.assertTrue("--parents-json" in skill_text or "artifact-lineage-recording.md" in skill_text)
            binding_text = (packaged_root / skill_name / "placeholder-bindings.md").read_text(encoding="utf-8")
            self.assertIn("Canonical lineage metadata", binding_text)
            self.assertIn("--lineage-kind", binding_text)
        self.assertIn("isomer-deepsci-nature-paper2ppt", validator.EXPECTED_DEEPSCI_SKILLS)
        self.assertIn("isomer-deepsci-nature-polishing", validator.EXPECTED_DEEPSCI_SKILLS)
        self.assertIn("isomer-deepsci-workspace-mgr", validator.EXPECTED_DEEPSCI_SKILLS)

    def test_deepsci_skills_teach_exact_research_idea_source_paths(self) -> None:
        packaged_root = REPO_ROOT / "src" / "isomer_labs" / "assets" / "system_skills" / "research-paradigm" / "deepsci"
        shared_ref = packaged_root / "isomer-deepsci-shared" / "references" / "research-idea-recording.md"
        self.assertTrue(shared_ref.exists(), shared_ref)
        shared_text = shared_ref.read_text(encoding="utf-8")
        self.assertIn("--source-json-path", shared_text)
        self.assertIn("$.sections.raw_ideas[<index>]", shared_text)
        self.assertIn("$.sections.filter_notes", shared_text)
        for skill_name in ("isomer-deepsci-idea", "isomer-deepsci-optimize", "isomer-deepsci-experiment", "isomer-deepsci-analysis", "isomer-deepsci-decision", "isomer-deepsci-write", "isomer-deepsci-review", "isomer-deepsci-rebuttal", "isomer-deepsci-finalize"):
            skill_text = (packaged_root / skill_name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("Idea-recording reminder", skill_text)
            self.assertIn("source", skill_text.lower())
            self.assertIn("rendered Markdown", skill_text)
        for skill_name in ("isomer-deepsci-idea", "isomer-deepsci-optimize", "isomer-deepsci-experiment", "isomer-deepsci-analysis", "isomer-deepsci-decision"):
            binding_text = (packaged_root / skill_name / "placeholder-bindings.md").read_text(encoding="utf-8")
            self.assertIn("Canonical idea metadata", binding_text)
            self.assertIn("--source-json-path", binding_text)
            self.assertIn("rendered Markdown", binding_text)

    def test_reports_core_failure_fixtures(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "deepsci",
            "isomer-deepsci-valid",
            reference="references/isomer-research-contract.md",
            workflow_extra=(
                "3. **Break rules**. Use Research Goal, /data/source/run, "
                "[[tbd-surface:path-topic-workspace]], [[tbd-surface:missing-id]], "
                "and `references/missing.md`."
            ),
            display_name="isomer-deepsci-other",
            prompt_skill="isomer-deepsci-other",
            v2=True,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertTrue({"RPS001", "RPS002", "RPS003", "RPS004", "RPS005", "RPS006"} <= codes(diagnostics))

    def test_allows_non_active_migration_and_source_copy_zones(self) -> None:
        root, target = self.make_valid_skillset()
        non_active_text = """
        # Source Context

        DeepScientist source text may mention Research Goal, path-topic-workspace, /data/source/run,
        `artifact.science(...)`, `memory.read`, and instructions to Create an Artifact.
        """
        write(target / "deepscientist-migration-guide.md", non_active_text)
        write(target / "ds-analysis" / "write.md", non_active_text)
        write(target / "deepsci" / "isomer-deepsci-valid" / "migrate" / "migration-plan.md", non_active_text)
        write(target / "deepsci" / "isomer-deepsci-valid" / "org" / "analysis" / "analysis-of-valid.md", non_active_text)
        write(target / "deepsci" / "isomer-deepsci-valid" / "org" / "src" / "SKILL.md", non_active_text)
        write(target / "deepsci" / "isomer-deepsci-valid" / "templates" / "README.md", non_active_text)

        diagnostics = validator.validate_skillset(target, root)

        self.assert_no_codes(diagnostics, {"RPS001", "RPS002", "RPS004", "RPS010"})

    def test_allows_narrow_explanatory_zones(self) -> None:
        root, target = self.make_valid_skillset()
        write(target / "PROVENANCE.md", "DeepScientist source notes mention Research Goal.\n")
        write(target / "licenses" / "NOTICE.md", "DeepScientist source license notice.\n")
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "references" / "deferred-resources.md",
            "DeepScientist source scripts and /data/source copies were not imported.\n",
        )
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "references" / "isomer-research-contract.md",
            """
            # Contract

            ## Source-Term Mapping

            | Source term | Isomer framing |
            | --- | --- |
            | Research Goal | Research Topic |

            ## Rejected Source Runtime Concepts

            | Source behavior | Isomer skill text should say |
            | --- | --- |
            | `workspace_mode` | source runtime detail |
            | `auto_continue` | use Scheduler Policy refs |

            ## TBD Surface Registry

            ### Resolved Workspace Path Surfaces

            | Former ID | Resolution |
            | --- | --- |
            | path-topic-workspace | Use Topic Workspace through Workspace Path Resolution. |
            """,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assert_no_codes(diagnostics, {"RPS001", "RPS002", "RPS004", "RPS008"})

    def test_rejects_same_terms_outside_allow_zones(self) -> None:
        root, target = self.make_valid_skillset()
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "references" / "unlinked-active.md",
            """
            # Active Note

            Use Research Goal, DeepScientist, /data/source/run, and path-topic-workspace as active guidance.
            """,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertTrue({"RPS001", "RPS002", "RPS004"} <= codes(diagnostics), messages(diagnostics))

    def test_active_guidance_still_rejects_runtime_and_storage_terms(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "deepsci",
            "isomer-deepsci-valid",
            workflow_extra=(
                "3. **Break active guidance**. Use Research Goal, DeepScientist, /data/source/run, "
                "[[tbd-surface:path-topic-workspace]], and Create an Artifact for this output."
            ),
            v2=True,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertTrue({"RPS001", "RPS002", "RPS004", "RPS010"} <= codes(diagnostics), messages(diagnostics))

    def test_accepts_registered_unresolved_tbd_placeholder(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "deepsci",
            "isomer-deepsci-valid",
            reference="references/isomer-research-contract.md",
            workflow_extra="3. **Mark unsettled provider**. Emit [[tbd-surface:provider-new]] when provider details remain open.",
            v2=True,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assert_no_codes(diagnostics, {"RPS002", "RPS003"})

    def test_rejects_unregistered_v2_research_placeholder(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "deepsci",
            "isomer-deepsci-valid",
            workflow_extra="3. **Break placeholder**. Produce [[rsch-object:missing-object]].",
            v2=True,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS009", codes(diagnostics), messages(diagnostics))

    def test_accepts_registered_migration_placeholder(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "deepsci",
            "isomer-deepsci-valid",
            workflow_extra="3. **Use local placeholder**. Produce `<VALID_HANDOFF>` for the next route.",
            v2=True,
        )
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "migrate" / "placeholders.md",
            """
            # Migration Placeholders

            | Placeholder | Meaning |
            | --- | --- |
            | <VALID_HANDOFF> | Fixture handoff. |
            """,
        )
        self.write_placeholder_bindings(target / "deepsci" / "isomer-deepsci-valid", ["VALID_HANDOFF"])
        diagnostics = validator.validate_skillset(target, root)
        self.assert_no_codes(diagnostics, {"RPS009", "RPS012"})

    def test_rejects_unregistered_migration_placeholder(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "deepsci",
            "isomer-deepsci-valid",
            workflow_extra="3. **Break local placeholder**. Produce `<MISSING_HANDOFF>` for the next route.",
            v2=True,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS009", codes(diagnostics), messages(diagnostics))

    def test_rejects_missing_v2_placeholder_binding_page(self) -> None:
        root, target = self.make_valid_skillset()
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "migrate" / "placeholders.md",
            """
            # Migration Placeholders

            | Placeholder | Meaning |
            | --- | --- |
            | <VALID_HANDOFF> | Fixture handoff. |
            """,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS012", codes(diagnostics), messages(diagnostics))

    def test_rejects_missing_v2_placeholder_binding_row(self) -> None:
        root, target = self.make_valid_skillset()
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "migrate" / "placeholders.md",
            """
            # Migration Placeholders

            | Placeholder | Meaning |
            | --- | --- |
            | <VALID_HANDOFF> | Fixture handoff. |
            | <SECOND_HANDOFF> | Fixture handoff. |
            """,
        )
        self.write_placeholder_bindings(target / "deepsci" / "isomer-deepsci-valid", ["VALID_HANDOFF"])
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS012", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("<SECOND_HANDOFF>" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_rejects_extra_v2_placeholder_binding_row(self) -> None:
        root, target = self.make_valid_skillset()
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "migrate" / "placeholders.md",
            """
            # Migration Placeholders

            | Placeholder | Meaning |
            | --- | --- |
            | <VALID_HANDOFF> | Fixture handoff. |
            """,
        )
        self.write_placeholder_bindings(
            target / "deepsci" / "isomer-deepsci-valid",
            ["VALID_HANDOFF", "EXTRA_HANDOFF"],
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS012", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("<EXTRA_HANDOFF>" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_rejects_v2_storage_binding(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "deepsci",
            "isomer-deepsci-valid",
            workflow_extra="3. **Bind too early**. Create an Artifact for this output.",
            v2=True,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS010", codes(diagnostics), messages(diagnostics))

    def test_rejects_v2_support_section_without_intro(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(target / "deepsci", "isomer-deepsci-valid", v2=True)
        skill_md = target / "deepsci" / "isomer-deepsci-valid" / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8")
            + "\n## Preferences\n\n- Prefer fixture behavior (if the fixture applies, otherwise explain why).\n",
            encoding="utf-8",
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS011", codes(diagnostics), messages(diagnostics))

    def test_rejects_flat_root_skill_folder(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(target, "isomer-deepsci-flat", reference="references/isomer-research-contract.md", v2=False)
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS007", codes(diagnostics), messages(diagnostics))

    def test_allows_pattern_references_but_reports_concrete_missing_references(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "deepsci",
            "isomer-deepsci-valid",
            routing_extra=(
                "- `references/packages/<package_id>.md` documents package-specific reference shape.\n"
                "- `scripts/<script>.py` documents script-specific reference shape.\n"
                "- `references/missing.md` is a concrete broken reference."
            ),
            v2=True,
        )
        diagnostics = validator.validate_skillset(target, root)
        rendered = messages(diagnostics)
        self.assertTrue(any("references/missing.md" in message for message in rendered), rendered)
        self.assertFalse(any("references/packages/<package_id>.md" in message for message in rendered), rendered)
        self.assertFalse(any("scripts/<script>.py" in message for message in rendered), rendered)

    def test_registry_mirror_match_passes(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_local_registry_mirror(target)
        diagnostics = validator.validate_skillset(target, root)
        self.assert_no_codes(diagnostics, {"RPS008"})

    def test_registry_mirror_missing_ids_are_reported(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_local_registry_mirror(target, include_row=False)
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS008", codes(diagnostics), messages(diagnostics))

    def test_registry_mirror_extra_ids_are_reported(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_local_registry_mirror(target, extra_row=True)
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS008", codes(diagnostics), messages(diagnostics))

    def test_registry_mirror_changed_text_is_reported(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_local_registry_mirror(target, resolution="Use a different storage contract.")
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS008", codes(diagnostics), messages(diagnostics))

    def test_rejects_legacy_deepsci_namespace_in_active_guidance(self) -> None:
        root, target = self.make_valid_skillset()
        stale_skill = "isomer-" + "rsch-scout"
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "references" / "active.md",
            f"# Active\n\nUse ${stale_skill} as active guidance.\n",
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS001", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("stale term 'isomer-" + "rsch-'" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_rejects_legacy_deepsci_skill_folder(self) -> None:
        root, target = self.make_valid_skillset()
        stale_folder = "isomer-" + "rsch-scout"
        write(target / "deepsci" / stale_folder / "SKILL.md", "# Stale\n")

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS007", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("legacy isomer-" + "rsch-* skill folder" in message for message in messages(diagnostics)), messages(diagnostics))

    def write_local_registry_mirror(
        self,
        target: Path,
        *,
        include_row: bool = True,
        extra_row: bool = False,
        resolution: str = "Use Topic Workspace through Workspace Path Resolution.",
    ) -> None:
        rows = ""
        if include_row:
            rows += f"| path-topic-workspace | {resolution} |\n"
        if extra_row:
            rows += "| schema-extra-surface | Extra resolution. |\n"
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "references" / "isomer-research-contract.md",
            (
                "# Contract\n\n"
                "## TBD Surface Registry\n\n"
                "### Resolved Workspace Path Surfaces\n\n"
                "| Former ID | Resolution |\n"
                "| --- | --- |\n"
                f"{rows}"
            ),
        )

    def test_whole_subtree_scan_checks_unlinked_markdown_and_yaml(self) -> None:
        root, target = self.make_valid_skillset()
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "references" / "unlinked.md",
            "# Unlinked\n\nResearch Goal appears outside linked references.\n",
        )
        write(
            target / "deepsci" / "isomer-deepsci-valid" / "agents" / "extra.yaml",
            "runtime_path: /data/local/source\n",
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertTrue({"RPS001", "RPS004"} <= codes(diagnostics), messages(diagnostics))

    def test_cli_reports_deterministic_format_and_nonzero_exit(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "deepsci",
            "isomer-deepsci-valid",
            reference="references/isomer-research-contract.md",
            workflow_extra="3. **Break term**. Use Research Goal as active guidance.",
            v2=True,
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = validator.main([str(target), "--repo-root", str(root)])
        self.assertEqual(1, exit_code)
        rendered = output.getvalue().strip().splitlines()
        self.assertTrue(rendered)
        self.assertRegex(
            rendered[0],
            r"^skillset/research-paradigm/deepsci/isomer-deepsci-valid/SKILL\.md:\d+: RPS001 ",
        )
