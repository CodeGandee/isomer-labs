from __future__ import annotations

import contextlib
import importlib.util
import io
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


class ResearchParadigmValidatorTests(unittest.TestCase):
    def make_root(self) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        write(root / "pyproject.toml", "[project]\nname = \"fixture\"\n")
        return root

    def make_valid_skillset(self) -> tuple[Path, Path]:
        root = self.make_root()
        target = root / "skillset" / "research-paradigm"
        v1_root = target / "v1"
        v2_root = target / "v2"
        for name in sorted(validator.EXPECTED_V1_SKILLS):
            reference = "references/tbd-surface-registry.md" if name == "isomer-rsch-shared-v1" else "references/isomer-research-contract.md"
            self.write_skill(v1_root, name, reference=reference, v2=False)
            if reference == "references/isomer-research-contract.md":
                write(
                    v1_root / name / "references" / "isomer-research-contract.md",
                    "# Contract\n\nUse Research Topic, Research Inquiry, Artifacts, and Decision Records.\n",
                )
        write(
            v1_root / "isomer-rsch-shared-v1" / "references" / "tbd-surface-registry.md",
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
        for name in sorted(validator.EXPECTED_V2_SKILLS):
            self.write_skill(v2_root, name, v2=True)
        write(
            v2_root / "isomer-rsch-shared-v2" / "references" / "semantic-placeholders.md",
            """
            # V2 Semantic Placeholders

            | ID | Meaning | Required semantic content | Typical producers | Typical consumers | Storage-binding status |
            | --- | --- | --- | --- | --- | --- |
            | `research-frame` | Research frame. | Objective, metric, constraints, and next route. | `isomer-rsch-scout-v2` | Any v2 skill | Not storage-bound yet. |
            """,
        )
        return root, target

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
        load_step = f"1. **Load context**. Read `{reference}` first." if reference else "1. **Load context**. Read `isomer-rsch-shared-v2` first."
        output_step = (
            "2. **Produce semantics**. Produce [[rsch-object:research-frame]] with enough content for the next method step."
            if v2
            else "2. **Record output**. Use Research Topic, Artifacts, and Decision Records."
        )
        routing_line = f"- `{reference}` for local terminology." if reference else "- Read `isomer-rsch-shared-v2` for placeholder semantics."
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

            ## Workflow

            When this skill is invoked, execute the following steps in order.

            {load_step}
            {output_step}
            {workflow_extra}

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

    def test_research_validator_rejects_repo_local_isomer_cli_wrapper(self) -> None:
        root, target = self.make_valid_skillset()
        write(
            target / "v2" / "isomer-rsch-scout-v2" / "placeholder-bindings.md",
            "# Placeholder Bindings\n\nRun `pixi run isomer-cli ext research records list`.\n",
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS013", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("global isomer-cli directly" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_payload_first_placeholder_binding_is_allowed(self) -> None:
        root, target = self.make_valid_skillset()
        skill_dir = target / "v2" / "isomer-rsch-scout-v2"
        write(skill_dir / "migrate" / "placeholders.md", "| Placeholder | Meaning |\n| --- | --- |\n| <SCOUT_CONTEXT_BRIEF> | Context. |\n")
        write(
            skill_dir / "placeholder-bindings.md",
            """
            # Placeholder Bindings

            For structured rows, draft a JSON payload file, run `isomer-cli --print-json ext research records validate --topic <topic> --format-profile <format-profile-ref> --payload-file <payload-file>`, then create the record.

            | Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
            | --- | --- | --- | --- | --- | --- | --- |
            | <SCOUT_CONTEXT_BRIEF> | evidence | Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/scout-context-brief/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCOUT_CONTEXT_BRIEF>' --format-profile isomer:deepsci/record-format/profile/evidence/scout-context-brief/v1 --payload-file <payload-file> --render markdown --content-name scout-context-brief.md` |
            """,
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertNotIn("RPS014", codes(diagnostics), messages(diagnostics))

    def test_payload_first_placeholder_binding_rejects_body_file_and_bare_profile(self) -> None:
        root, target = self.make_valid_skillset()
        skill_dir = target / "v2" / "isomer-rsch-scout-v2"
        write(skill_dir / "migrate" / "placeholders.md", "| Placeholder | Meaning |\n| --- | --- |\n| <SCOUT_CONTEXT_BRIEF> | Context. |\n")
        write(
            skill_dir / "placeholder-bindings.md",
            """
            # Placeholder Bindings

            | Placeholder | Kind | Storage Item | Record Kind | Default Label | Profile | Create Command |
            | --- | --- | --- | --- | --- | --- | --- |
            | <SCOUT_CONTEXT_BRIEF> | evidence | Evidence Item | `evidence_item` | `topic.records.artifacts` | `isomer:deepsci/record-format/profile/evidence/scout-context-brief/v1` | `isomer-cli --print-json ext research records create --topic <topic> --record-kind evidence_item --placeholder '<SCOUT_CONTEXT_BRIEF>' --profile evidence.scout-context-brief --body-file <body-file>` |
            """,
        )

        diagnostics = validator.validate_skillset(target, root)

        self.assertIn("RPS014", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("--format-profile" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_expected_inventory_includes_expanded_v2_contract(self) -> None:
        self.assertIn("isomer-rsch-intake-v1", validator.EXPECTED_V1_SKILLS)
        self.assertIn("isomer-rsch-write-v1", validator.EXPECTED_V1_SKILLS)
        self.assertIn("isomer-rsch-write-v2", validator.EXPECTED_V2_SKILLS)
        self.assertIn("isomer-rsch-paper-outline-v2", validator.EXPECTED_V2_SKILLS)
        self.assertIn("isomer-rsch-paper-plot-v2", validator.EXPECTED_V2_SKILLS)
        self.assertIn("isomer-rsch-figure-polish-v2", validator.EXPECTED_V2_SKILLS)
        self.assertIn("isomer-rsch-review-v2", validator.EXPECTED_V2_SKILLS)
        self.assertIn("isomer-rsch-rebuttal-v2", validator.EXPECTED_V2_SKILLS)
        self.assertIn("isomer-rsch-nature-data-v2", validator.EXPECTED_V2_SKILLS)
        self.assertIn("isomer-rsch-nature-figure-v2", validator.EXPECTED_V2_SKILLS)
        self.assertIn("isomer-rsch-nature-paper2ppt-v2", validator.EXPECTED_V2_SKILLS)
        self.assertIn("isomer-rsch-nature-polishing-v2", validator.EXPECTED_V2_SKILLS)
        self.assertIn("isomer-rsch-workspace-mgr-v2", validator.EXPECTED_V2_SKILLS)

    def test_reports_core_failure_fixtures(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "v1",
            "isomer-rsch-valid-v1",
            reference="references/isomer-research-contract.md",
            workflow_extra=(
                "3. **Break rules**. Use Research Goal, /data/source/run, "
                "[[tbd-surface:path-topic-workspace]], [[tbd-surface:missing-id]], "
                "and `references/missing.md`."
            ),
            display_name="isomer-rsch-other-v1",
            prompt_skill="isomer-rsch-other-v1",
            v2=False,
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
        write(target / "v2" / "isomer-rsch-valid-v2" / "migrate" / "migration-plan.md", non_active_text)
        write(target / "v2" / "isomer-rsch-valid-v2" / "org" / "analysis" / "analysis-of-valid.md", non_active_text)
        write(target / "v2" / "isomer-rsch-valid-v2" / "org" / "src" / "SKILL.md", non_active_text)
        write(target / "v2" / "isomer-rsch-valid-v2" / "templates" / "README.md", non_active_text)

        diagnostics = validator.validate_skillset(target, root)

        self.assert_no_codes(diagnostics, {"RPS001", "RPS002", "RPS004", "RPS010"})

    def test_allows_narrow_explanatory_zones(self) -> None:
        root, target = self.make_valid_skillset()
        write(target / "PROVENANCE.md", "DeepScientist source notes mention Research Goal.\n")
        write(target / "licenses" / "NOTICE.md", "DeepScientist source license notice.\n")
        write(
            target / "v1" / "isomer-rsch-valid-v1" / "references" / "deferred-resources.md",
            "DeepScientist source scripts and /data/source copies were not imported.\n",
        )
        write(
            target / "v1" / "isomer-rsch-valid-v1" / "references" / "isomer-research-contract.md",
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
            target / "v1" / "isomer-rsch-valid-v1" / "references" / "unlinked-active.md",
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
            target / "v2",
            "isomer-rsch-valid-v2",
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
            target / "v1",
            "isomer-rsch-valid-v1",
            reference="references/isomer-research-contract.md",
            workflow_extra="3. **Mark unsettled provider**. Emit [[tbd-surface:provider-new]] when provider details remain open.",
            v2=False,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assert_no_codes(diagnostics, {"RPS002", "RPS003"})

    def test_rejects_unregistered_v2_research_placeholder(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "v2",
            "isomer-rsch-valid-v2",
            workflow_extra="3. **Break placeholder**. Produce [[rsch-object:missing-object]].",
            v2=True,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS009", codes(diagnostics), messages(diagnostics))

    def test_accepts_registered_migration_placeholder(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "v2",
            "isomer-rsch-valid-v2",
            workflow_extra="3. **Use local placeholder**. Produce `<VALID_HANDOFF>` for the next route.",
            v2=True,
        )
        write(
            target / "v2" / "isomer-rsch-valid-v2" / "migrate" / "placeholders.md",
            """
            # Migration Placeholders

            | Placeholder | Meaning |
            | --- | --- |
            | <VALID_HANDOFF> | Fixture handoff. |
            """,
        )
        self.write_placeholder_bindings(target / "v2" / "isomer-rsch-valid-v2", ["VALID_HANDOFF"])
        diagnostics = validator.validate_skillset(target, root)
        self.assert_no_codes(diagnostics, {"RPS009", "RPS012"})

    def test_rejects_unregistered_migration_placeholder(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "v2",
            "isomer-rsch-valid-v2",
            workflow_extra="3. **Break local placeholder**. Produce `<MISSING_HANDOFF>` for the next route.",
            v2=True,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS009", codes(diagnostics), messages(diagnostics))

    def test_rejects_missing_v2_placeholder_binding_page(self) -> None:
        root, target = self.make_valid_skillset()
        write(
            target / "v2" / "isomer-rsch-valid-v2" / "migrate" / "placeholders.md",
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
            target / "v2" / "isomer-rsch-valid-v2" / "migrate" / "placeholders.md",
            """
            # Migration Placeholders

            | Placeholder | Meaning |
            | --- | --- |
            | <VALID_HANDOFF> | Fixture handoff. |
            | <SECOND_HANDOFF> | Fixture handoff. |
            """,
        )
        self.write_placeholder_bindings(target / "v2" / "isomer-rsch-valid-v2", ["VALID_HANDOFF"])
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS012", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("<SECOND_HANDOFF>" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_rejects_extra_v2_placeholder_binding_row(self) -> None:
        root, target = self.make_valid_skillset()
        write(
            target / "v2" / "isomer-rsch-valid-v2" / "migrate" / "placeholders.md",
            """
            # Migration Placeholders

            | Placeholder | Meaning |
            | --- | --- |
            | <VALID_HANDOFF> | Fixture handoff. |
            """,
        )
        self.write_placeholder_bindings(
            target / "v2" / "isomer-rsch-valid-v2",
            ["VALID_HANDOFF", "EXTRA_HANDOFF"],
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS012", codes(diagnostics), messages(diagnostics))
        self.assertTrue(any("<EXTRA_HANDOFF>" in message for message in messages(diagnostics)), messages(diagnostics))

    def test_rejects_v2_storage_binding(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "v2",
            "isomer-rsch-valid-v2",
            workflow_extra="3. **Bind too early**. Create an Artifact for this output.",
            v2=True,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS010", codes(diagnostics), messages(diagnostics))

    def test_rejects_v2_support_section_without_intro(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(target / "v2", "isomer-rsch-valid-v2", v2=True)
        skill_md = target / "v2" / "isomer-rsch-valid-v2" / "SKILL.md"
        skill_md.write_text(
            skill_md.read_text(encoding="utf-8")
            + "\n## Preferences\n\n- Prefer fixture behavior (if the fixture applies, otherwise explain why).\n",
            encoding="utf-8",
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS011", codes(diagnostics), messages(diagnostics))

    def test_rejects_flat_root_skill_folder(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(target, "isomer-rsch-flat", reference="references/isomer-research-contract.md", v2=False)
        diagnostics = validator.validate_skillset(target, root)
        self.assertIn("RPS007", codes(diagnostics), messages(diagnostics))

    def test_allows_pattern_references_but_reports_concrete_missing_references(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "v2",
            "isomer-rsch-valid-v2",
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
            target / "v1" / "isomer-rsch-valid-v1" / "references" / "isomer-research-contract.md",
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
            target / "v1" / "isomer-rsch-valid-v1" / "references" / "unlinked.md",
            "# Unlinked\n\nResearch Goal appears outside linked references.\n",
        )
        write(
            target / "v1" / "isomer-rsch-valid-v1" / "agents" / "extra.yaml",
            "runtime_path: /data/local/source\n",
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertTrue({"RPS001", "RPS004"} <= codes(diagnostics), messages(diagnostics))

    def test_cli_reports_deterministic_format_and_nonzero_exit(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target / "v1",
            "isomer-rsch-valid-v1",
            reference="references/isomer-research-contract.md",
            workflow_extra="3. **Break term**. Use Research Goal as active guidance.",
            v2=False,
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = validator.main([str(target), "--repo-root", str(root)])
        self.assertEqual(1, exit_code)
        rendered = output.getvalue().strip().splitlines()
        self.assertTrue(rendered)
        self.assertRegex(
            rendered[0],
            r"^skillset/research-paradigm/v1/isomer-rsch-valid-v1/SKILL\.md:\d+: RPS001 ",
        )
