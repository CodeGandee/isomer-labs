from __future__ import annotations

from pathlib import Path
import re
import tomllib
import unittest

import yaml

from isomer_labs.skills.system_assets import (
    lookup_system_skill_capability,
    resolve_system_skill_capability,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
KAOJU_PACK = (
    REPO_ROOT
    / "src"
    / "isomer_labs"
    / "assets"
    / "system_skills"
    / "research-paradigm"
    / "kaoju"
    / "isomer-ext-kaoju-entrypoint"
)
ACTIONS = (
    "resolve-paper",
    "search-papers",
    "find-citing-papers",
    "explore-cited-papers",
    "trace-citation-neighborhood",
    "find-related-papers",
)


class KaojuPaperSearchSkillTests(unittest.TestCase):
    def test_bundle_identity_metadata_actions_references_and_callbacks_are_exact(self) -> None:
        capability = lookup_system_skill_capability("isomer-kaoju-paper-search")
        self.assertEqual("kaoju", capability.pack_id)
        self.assertEqual("paper-search", capability.member_name)
        self.assertEqual(
            "isomer-ext-kaoju-entrypoint->paper-search",
            capability.invocation_designator,
        )
        self.assertEqual(("isomer-kaoju-shared",), capability.dependencies)
        self.assertEqual(("begin", "end"), capability.callback_insertion_points)

        bundle = Path(str(resolve_system_skill_capability("isomer-kaoju-paper-search")))
        main = (bundle / "SKILL-MAIN.md").read_text(encoding="utf-8")
        for action in ACTIONS:
            with self.subTest(action=action):
                self.assertIn(f"`{action}`", main)
                self.assertIn(f"commands/{action}.md", main)
                page = (bundle / "commands" / f"{action}.md").read_text(encoding="utf-8")
                for term in (
                    "## Workflow",
                    "requested",
                    "applied",
                    "provider",
                    "normalized",
                    "Gate",
                    "Blocker",
                    "Resume",
                ):
                    self.assertIn(term.casefold(), page.casefold())

        self.assertIn("Apply begin callbacks", main)
        self.assertIn("Apply end callbacks", main)
        self.assertIn("one normalized provider-output observation", main)
        for reference in (
            "provider-selection.md",
            "result-contract.md",
            "execution-and-errors.md",
        ):
            self.assertTrue((bundle / "references" / reference).is_file())
        self.assertTrue((bundle / "references" / "approaches" / "s2.md").is_file())

        project_version = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))[
            "project"
        ]["version"]
        metadata = yaml.safe_load((bundle / "agents" / "openai.yaml").read_text(encoding="utf-8"))
        self.assertEqual(project_version, metadata["metadata"]["version"])
        self.assertIn("$isomer-ext-kaoju-entrypoint", metadata["interface"]["default_prompt"])

    def test_top_level_is_provider_neutral_and_s2_reference_is_bounded(self) -> None:
        bundle = Path(str(resolve_system_skill_capability("isomer-kaoju-paper-search")))
        main = (bundle / "SKILL-MAIN.md").read_text(encoding="utf-8")
        for forbidden in (
            "api.semanticscholar.org",
            "/graph/v1/",
            "S2_API_KEY=",
            "imsight-paper-search",
            "houmao-agents",
        ):
            self.assertNotIn(forbidden, main)

        approach = (bundle / "references" / "approaches" / "s2.md").read_text(encoding="utf-8")
        for action in ACTIONS:
            self.assertIn(action, approach)
        for required in (
            "Paper detail",
            "Paper batch",
            "citations",
            "references",
            "recommendations",
            "offset pagination",
            "opaque token",
            "filtering.location",
            "general-purpose CLI",
            "direct-HTTPS",
            "S2_API_KEY",
            "redacted attachments",
            "isomer-literature-provider-observation.v1",
        ):
            self.assertIn(required.casefold(), approach.casefold())
        for excluded in (
            "author search",
            "snippet search",
            "Datasets API",
            "bulk corpus export",
        ):
            self.assertRegex(approach, re.compile(rf"excludes[^\n]*{re.escape(excluded)}", re.I))
        self.assertIn("Do not invoke an S2 search", approach)
        self.assertIn("through `isomer-cli`", approach)

    def test_known_callers_route_paper_retrieval_without_s2_mechanics(self) -> None:
        caller_paths = (
            KAOJU_PACK / "subskills" / "isomer-kaoju-discover" / "SKILL-MAIN.md",
            KAOJU_PACK / "subskills" / "isomer-kaoju-acquire" / "SKILL-MAIN.md",
            KAOJU_PACK / "commands" / "build-reading-list.md",
            KAOJU_PACK / "commands" / "landscape-pass.md",
            KAOJU_PACK / "commands" / "curated-intake-pass.md",
            KAOJU_PACK / "commands" / "direction-expansion-pass.md",
            KAOJU_PACK / "commands" / "ingest-source-code.md",
        )
        for path in caller_paths:
            with self.subTest(path=path.name):
                text = path.read_text(encoding="utf-8")
                self.assertIn("isomer-ext-kaoju-entrypoint->paper-search", text)
                self.assertNotIn("api.semanticscholar.org", text)
                self.assertNotIn("/graph/v1/", text)
                self.assertNotIn("S2_API_KEY", text)

        discover = caller_paths[0].read_text(encoding="utf-8")
        self.assertIn("sole ownership of Discovery Ledger", discover)
        self.assertIn("Reading List composition", discover)
        acquire = caller_paths[1].read_text(encoding="utf-8")
        self.assertIn("before this skill makes acquisition judgments", acquire)


if __name__ == "__main__":
    unittest.main()
