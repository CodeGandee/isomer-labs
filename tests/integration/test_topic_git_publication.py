from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class TopicGitPublicationIntegrationTests(unittest.TestCase):
    def test_reproduction_outputs_same_remote_components_and_upstream_reference_clone(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            remote = root / "publication.git"
            self._git(root, "init", "--bare", str(remote))

            main = self._fresh_branch_repo(root / "main", "topic-owner/main", "main.txt")
            agent = self._fresh_branch_repo(root / "agent", "per-agent/coder/main", "agent.txt")
            reference = self._fresh_branch_repo(root / "reference", "main", "upstream.txt")
            self._git(main, "remote", "add", "origin", str(remote))
            self._git(agent, "remote", "add", "origin", str(remote))
            self._git(main, "push", "origin", "HEAD:refs/heads/topic-owner/main")
            self._git(agent, "push", "origin", "HEAD:refs/heads/per-agent/coder/main")

            superproject = self._fresh_branch_repo(root / "copy", "topic-workspace/main", "README.md")
            self._git(
                superproject,
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                "-b",
                "topic-owner/main",
                str(remote),
                "repos/topic-main",
            )
            self._git(
                superproject,
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                "-b",
                "per-agent/coder/main",
                str(remote),
                "agents/coder",
            )
            self._git(
                superproject,
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                "-b",
                "main",
                str(reference),
                "repos/extern/sources/powerinfer",
            )
            (superproject / "README.md").write_text(
                "# Reproducible topic\n\nLatest paper: [PDF](paper/latest.pdf)\n",
                encoding="utf-8",
            )
            (superproject / "research-record-index.json").write_text(
                '{"schema_version":"isomer-topic-git-research-record-index.v1","records":[]}\n',
                encoding="utf-8",
            )
            (superproject / "paper").mkdir()
            (superproject / "paper" / "latest.pdf").write_bytes(b"%PDF-1.7\n")
            self._git(
                superproject,
                "add",
                "--",
                ".gitmodules",
                "repos/topic-main",
                "agents/coder",
                "repos/extern/sources/powerinfer",
                "README.md",
                "research-record-index.json",
                "paper/latest.pdf",
            )
            self._git(superproject, "commit", "-m", "publish reproducible topic")
            self._git(superproject, "remote", "add", "origin", str(remote))
            self._git(superproject, "fetch", "origin")
            self._git(superproject, "push", "origin", "HEAD:refs/heads/topic-workspace/main")

            clone = root / "clone"
            self._git(
                root,
                "-c",
                "protocol.file.allow=always",
                "clone",
                "--branch",
                "topic-workspace/main",
                "--recurse-submodules",
                str(remote),
                str(clone),
            )
            self.assertEqual("sanitized\n", (clone / "repos" / "topic-main" / "main.txt").read_text(encoding="utf-8"))
            self.assertEqual("sanitized\n", (clone / "agents" / "coder" / "agent.txt").read_text(encoding="utf-8"))
            self.assertEqual(
                "sanitized\n",
                (clone / "repos" / "extern" / "sources" / "powerinfer" / "upstream.txt").read_text(encoding="utf-8"),
            )
            self.assertIn(
                "Latest paper: [PDF](paper/latest.pdf)",
                (clone / "README.md").read_text(encoding="utf-8"),
            )
            self.assertTrue((clone / "paper" / "latest.pdf").read_bytes().startswith(b"%PDF-"))
            self.assertFalse((clone / "repos" / "topic-main" / ".git" / "objects").is_dir())

            reconstructed = root / "reconstructed"
            reconstructed.mkdir()
            self._git(reconstructed, "init")
            self._git(reconstructed, "remote", "add", "publication", str(remote))
            self._git(
                reconstructed,
                "fetch",
                "--no-tags",
                "publication",
                "topic-workspace/main:refs/remotes/publication/topic-workspace/main",
            )
            self._git(
                reconstructed,
                "checkout",
                "-b",
                "topic-workspace/main",
                "refs/remotes/publication/topic-workspace/main",
            )
            self._git(
                reconstructed,
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "update",
                "--init",
                "--recursive",
            )
            self.assertEqual(
                "sanitized\n",
                (reconstructed / "repos" / "topic-main" / "main.txt").read_text(encoding="utf-8"),
            )
            self.assertEqual(
                "sanitized\n",
                (
                    reconstructed
                    / "repos"
                    / "extern"
                    / "sources"
                    / "powerinfer"
                    / "upstream.txt"
                ).read_text(encoding="utf-8"),
            )

    def _fresh_branch_repo(self, path: Path, branch: str, filename: str) -> Path:
        path.mkdir()
        self._git(path, "init")
        self._git(path, "config", "user.name", "Isomer Publication")
        self._git(path, "config", "user.email", "isomer-publication@invalid")
        (path / filename).write_text("sanitized\n", encoding="utf-8")
        self._git(path, "add", "--", filename)
        self._git(path, "commit", "-m", "fresh sanitized history")
        self._git(path, "branch", "-M", branch)
        return path

    @staticmethod
    def _git(cwd: Path, *args: str) -> str:
        environment = dict(os.environ)
        environment["GIT_CONFIG_NOSYSTEM"] = "1"
        result = subprocess.run(
            ("git", "-C", str(cwd), *args),
            check=True,
            capture_output=True,
            text=True,
            env=environment,
        )
        return result.stdout.strip()


if __name__ == "__main__":
    unittest.main()
