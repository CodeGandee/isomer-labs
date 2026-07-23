from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile
import unittest


class TopicGitPublicationIntegrationTests(unittest.TestCase):
    def test_same_remote_unrelated_component_histories_recursive_clone_and_push_order(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            remote = root / "publication.git"
            self._git(root, "init", "--bare", str(remote))

            main = self._fresh_branch_repo(root / "main", "topic-owner/main", "main.txt")
            agent = self._fresh_branch_repo(root / "agent", "per-agent/coder/main", "agent.txt")
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
            self._git(superproject, "add", "--", ".gitmodules", "repos/topic-main", "agents/coder")
            self._git(superproject, "commit", "-m", "publish sanitized components")
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

    def _fresh_branch_repo(self, path: Path, branch: str, filename: str) -> Path:
        path.mkdir()
        self._git(path, "init")
        self._git(path, "config", "user.name", "Isomer Test")
        self._git(path, "config", "user.email", "isomer@example.test")
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
