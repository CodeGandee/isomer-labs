from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from isomer_labs.skills.versioning import inspect_skill_version, require_skill_version


class SkillVersioningTests(unittest.TestCase):
    def make_skill(self, yaml_text: str) -> Path:
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        root = Path(tmp.name)
        agents = root / "agents"
        agents.mkdir()
        (agents / "openai.yaml").write_text(yaml_text, encoding="utf-8")
        return root

    def test_accepts_pep440_release_candidate(self) -> None:
        root = self.make_skill('metadata:\n  version: "0.3.0rc1"\n')

        observation = inspect_skill_version(root)

        self.assertEqual("valid", observation.status)
        self.assertEqual("0.3.0rc1", observation.normalized_version)
        self.assertEqual("0.3.0rc1", require_skill_version(root))

    def test_reports_missing_and_malformed_versions(self) -> None:
        missing = inspect_skill_version(self.make_skill("interface: {}\n"))
        malformed = inspect_skill_version(self.make_skill('metadata:\n  version: "latest"\n'))

        self.assertEqual("unversioned", missing.status)
        self.assertEqual("malformed_version", malformed.status)
