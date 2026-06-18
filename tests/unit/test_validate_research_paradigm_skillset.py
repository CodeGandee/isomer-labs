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
        self.write_skill(target, "isomer-rsch-shared", reference="references/tbd-surface-registry.md")
        write(
            target / "isomer-rsch-shared" / "references" / "tbd-surface-registry.md",
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
        self.write_skill(target, "isomer-rsch-valid")
        write(
            target / "isomer-rsch-valid" / "references" / "isomer-research-contract.md",
            """
            # Contract

            Use Research Topic, Research Inquiry, Artifacts, and Decision Records.
            """,
        )
        return root, target

    def write_skill(
        self,
        target: Path,
        name: str,
        *,
        reference: str = "references/isomer-research-contract.md",
        workflow_extra: str = "",
        routing_extra: str = "",
        display_name: str | None = None,
        prompt_skill: str | None = None,
    ) -> None:
        write(
            target / name / "SKILL.md",
            f"""
            ---
            name: {name}
            description: Valid fixture skill.
            ---

            # {name}

            ## Overview

            Use this fixture for validator tests.

            ## Workflow

            When this skill is invoked, execute the following steps in order.

            1. **Load context**. Read `{reference}` first.
            2. **Record output**. Use Research Topic, Artifacts, and Decision Records.
            {workflow_extra}

            If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the constraints, references, and user request, then execute the plan.

            ## Reference Routing

            - `{reference}` for local terminology.
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

    def assert_no_codes(self, diagnostics: list[object], unexpected: set[str]) -> None:
        present = codes(diagnostics) & unexpected
        self.assertFalse(present, messages(diagnostics))

    def test_minimal_valid_research_paradigm_skillset_passes(self) -> None:
        root, target = self.make_valid_skillset()
        diagnostics = validator.validate_skillset(target, root)
        self.assertEqual([], messages(diagnostics))

    def test_reports_core_failure_fixtures(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target,
            "isomer-rsch-valid",
            workflow_extra=(
                "3. **Break rules**. Use Research Goal, /data/source/run, "
                "[[tbd-surface:path-topic-workspace]], [[tbd-surface:missing-id]], "
                "and `references/missing.md`."
            ),
            display_name="isomer-rsch-other",
            prompt_skill="isomer-rsch-other",
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertTrue({"RPS001", "RPS002", "RPS003", "RPS004", "RPS005", "RPS006"} <= codes(diagnostics))

    def test_allows_narrow_explanatory_zones(self) -> None:
        root, target = self.make_valid_skillset()
        write(target / "PROVENANCE.md", "DeepScientist source notes mention Research Goal.\n")
        write(target / "licenses" / "NOTICE.md", "DeepScientist source license notice.\n")
        write(
            target / "isomer-rsch-valid" / "references" / "deferred-resources.md",
            "DeepScientist source scripts and /data/source copies were not imported.\n",
        )
        write(
            target / "isomer-rsch-valid" / "references" / "isomer-research-contract.md",
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
            target / "isomer-rsch-valid" / "references" / "unlinked-active.md",
            """
            # Active Note

            Use Research Goal, DeepScientist, /data/source/run, and path-topic-workspace as active guidance.
            """,
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertTrue({"RPS001", "RPS002", "RPS004"} <= codes(diagnostics), messages(diagnostics))

    def test_accepts_registered_unresolved_tbd_placeholder(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target,
            "isomer-rsch-valid",
            workflow_extra="3. **Mark unsettled provider**. Emit [[tbd-surface:provider-new]] when provider details remain open.",
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assert_no_codes(diagnostics, {"RPS002", "RPS003"})

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
            target / "isomer-rsch-valid" / "references" / "isomer-research-contract.md",
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
            target / "isomer-rsch-valid" / "references" / "unlinked.md",
            "# Unlinked\n\nResearch Goal appears outside linked references.\n",
        )
        write(
            target / "isomer-rsch-valid" / "agents" / "extra.yaml",
            "runtime_path: /data/local/source\n",
        )
        diagnostics = validator.validate_skillset(target, root)
        self.assertTrue({"RPS001", "RPS004"} <= codes(diagnostics), messages(diagnostics))

    def test_cli_reports_deterministic_format_and_nonzero_exit(self) -> None:
        root, target = self.make_valid_skillset()
        self.write_skill(
            target,
            "isomer-rsch-valid",
            workflow_extra="3. **Break term**. Use Research Goal as active guidance.",
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = validator.main([str(target), "--repo-root", str(root)])
        self.assertEqual(1, exit_code)
        rendered = output.getvalue().strip().splitlines()
        self.assertTrue(rendered)
        self.assertRegex(
            rendered[0],
            r"^skillset/research-paradigm/isomer-rsch-valid/SKILL\.md:\d+: RPS001 ",
        )
