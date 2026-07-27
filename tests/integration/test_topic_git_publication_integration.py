from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class TopicGitPublicationIntegrationTests(unittest.TestCase):
    def test_recursive_clone_preserves_paths_and_uses_ordinary_component_submodules(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = root / "source-topic-workspace"
            source.mkdir()
            component_paths = {
                "topic-main": Path("code/custom-topic-main"),
                "reviewer": Path("people/topic-actors/reviewer"),
                "coder": Path("people/agents/coder"),
                "powerinfer": Path("references/upstream/powerinfer"),
            }
            self._write_source_fixture(source, component_paths)

            remote = root / "publication.git"
            self._git(root, "init", "--bare", str(remote))
            reference = root / "powerinfer-reference"
            component_specs = (
                ("topic-main", "components/topic-main", "main.txt"),
                ("reviewer", "components/topic-actors/reviewer", "reviewer.txt"),
                ("coder", "components/agents/coder", "coder.txt"),
            )
            component_commits: dict[str, str] = {}
            for name, branch, filename in component_specs:
                repository = self._fresh_branch_repo(
                    root / f"publication-{name}",
                    branch,
                    filename,
                    (source / component_paths[name] / filename).read_bytes(),
                )
                self._git(repository, "remote", "add", "publication", str(remote))
                self._git(repository, "push", "publication", f"HEAD:refs/heads/{branch}")
                component_commits[name] = self._git(repository, "rev-parse", "HEAD")

            self._fresh_branch_repo(
                reference,
                "main",
                "upstream.txt",
                (source / component_paths["powerinfer"] / "upstream.txt").read_bytes(),
            )
            reference_commit = self._git(reference, "rev-parse", "HEAD")

            publication = root / "topic-publication-copy"
            publication.mkdir()
            self._git(publication, "init")
            self._git(publication, "config", "user.name", "Isomer Publication")
            self._git(publication, "config", "user.email", "isomer-publication@invalid")
            self._git(publication, "switch", "-c", "main")
            for relative_path in (
                "pixi.toml",
                "pixi.lock",
                "topic-workspace.toml",
                ".gitignore",
                ".gitattributes",
                "intent/topic-overview.md",
                "records/readiness.md",
                "records/artifacts/paper/pwinfer-analysis.pdf",
            ):
                destination = publication / relative_path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source / relative_path, destination)
            (publication / "README.md").write_text(
                (source / "README.md").read_text(encoding="utf-8")
                + "\n<!-- BEGIN ISOMER PUBLICATION NAVIGATION v1 -->\n"
                + "## Publication Snapshot\n\n"
                + "Latest paper: [PDF](records/artifacts/paper/pwinfer-analysis.pdf)\n\n"
                + "This clone preserves evidence paths but does not restore operational worktrees.\n"
                + "<!-- END ISOMER PUBLICATION NAVIGATION v1 -->\n",
                encoding="utf-8",
            )
            self._git(publication, "remote", "add", "publication", str(remote))
            for name, branch, _filename in component_specs:
                self._git(
                    publication,
                    "-c",
                    "protocol.file.allow=always",
                    "submodule",
                    "add",
                    "-b",
                    branch,
                    str(remote),
                    component_paths[name].as_posix(),
                )
            self._git(
                publication,
                "-c",
                "protocol.file.allow=always",
                "submodule",
                "add",
                "-b",
                "main",
                str(reference),
                component_paths["powerinfer"].as_posix(),
            )

            overlay = publication / ".isomer-publication"
            overlay.mkdir()
            projection = {
                "schema_version": "isomer-topic-git-projection-manifest.v2",
                "components": [
                    {
                        "component_id": name,
                        "kind": "main" if name == "topic-main" else ("actor" if name == "reviewer" else "agent"),
                        "relative_path": component_paths[name].as_posix(),
                        "branch": branch,
                        "commit": component_commits[name],
                        **({"git_anchor_component_id": "topic-main"} if name != "topic-main" else {}),
                    }
                    for name, branch, _filename in component_specs
                ],
                "references": [
                    {
                        "reference_id": "powerinfer",
                        "relative_path": component_paths["powerinfer"].as_posix(),
                        "commit": reference_commit,
                    }
                ],
            }
            (overlay / "topic-workspace-projection.json").write_text(
                json.dumps(projection, indent=2, sort_keys=True) + "\n",
                encoding="utf-8",
            )
            (overlay / "research-record-index.json").write_text(
                '{"schema_version":"isomer-topic-git-research-record-index.v1","records":[]}\n',
                encoding="utf-8",
            )
            (overlay / "topic-workspace-version.toml").write_text(
                'canonical_branch = "main"\nsnapshot_mode = "exclusive_snapshot"\n',
                encoding="utf-8",
            )
            exact_superproject_paths = (
                "README.md",
                "pixi.toml",
                "pixi.lock",
                "topic-workspace.toml",
                ".gitignore",
                ".gitattributes",
                "intent/topic-overview.md",
                "records/readiness.md",
                "records/artifacts/paper/pwinfer-analysis.pdf",
                ".gitmodules",
                ".isomer-publication/research-record-index.json",
                ".isomer-publication/topic-workspace-projection.json",
                ".isomer-publication/topic-workspace-version.toml",
                *(path.as_posix() for path in component_paths.values()),
            )
            self._git(publication, "add", "--", *exact_superproject_paths)
            self._git(publication, "commit", "-m", "publish current topic snapshot", "--", *exact_superproject_paths)
            self._git(publication, "push", "--force", "publication", "HEAD:refs/heads/main")

            clone = root / "clone"
            self._git(
                root,
                "-c",
                "protocol.file.allow=always",
                "clone",
                "--branch",
                "main",
                "--recurse-submodules",
                str(remote),
                str(clone),
            )

            source_paths = {
                path.relative_to(source).as_posix()
                for path in source.rglob("*")
                if path.is_file() and ".git" not in path.relative_to(source).parts
            }
            cloned_source_paths = {
                path.relative_to(clone).as_posix()
                for path in clone.rglob("*")
                if path.is_file()
                and ".git" not in path.relative_to(clone).parts
                and ".isomer-publication" not in path.relative_to(clone).parts
                and path.name != ".gitmodules"
            }
            self.assertEqual(source_paths, cloned_source_paths)
            self.assertTrue((clone / "records/artifacts/paper/pwinfer-analysis.pdf").read_bytes().startswith(b"%PDF-"))
            self.assertFalse((clone / "paper/latest.pdf").exists())
            self.assertIn(
                "Latest paper: [PDF](records/artifacts/paper/pwinfer-analysis.pdf)",
                (clone / "README.md").read_text(encoding="utf-8"),
            )

            cloned_projection = json.loads(
                (clone / ".isomer-publication/topic-workspace-projection.json").read_text(encoding="utf-8")
            )
            anchors = {
                component["component_id"]: component.get("git_anchor_component_id")
                for component in cloned_projection["components"]
            }
            self.assertEqual({"topic-main": None, "reviewer": "topic-main", "coder": "topic-main"}, anchors)

            for path in component_paths.values():
                tree_entry = self._git(clone, "ls-tree", "HEAD", "--", path.as_posix())
                self.assertTrue(tree_entry.startswith("160000 commit "), tree_entry)
            for name in ("topic-main", "reviewer", "coder"):
                git_file = clone / component_paths[name] / ".git"
                self.assertTrue(git_file.is_file())
                self.assertNotIn("/worktrees/", git_file.read_text(encoding="utf-8"))

            remote_branches = set(
                self._git(
                    root,
                    "--git-dir",
                    str(remote),
                    "for-each-ref",
                    "--format=%(refname:short)",
                    "refs/heads",
                ).splitlines()
            )
            self.assertEqual(
                {
                    "main",
                    "components/topic-main",
                    "components/topic-actors/reviewer",
                    "components/agents/coder",
                },
                remote_branches,
            )

    def _write_source_fixture(self, source: Path, component_paths: dict[str, Path]) -> None:
        text_files = {
            "README.md": "# Pwinfer Analysis\n",
            "pixi.toml": "[workspace]\nchannels = []\n",
            "pixi.lock": "version: 6\n",
            "topic-workspace.toml": 'topic_id = "pwinfer-analysis"\n',
            ".gitignore": "tmp/\n",
            ".gitattributes": "*.pdf binary\n",
            "intent/topic-overview.md": "# Topic Overview\n",
            "records/readiness.md": "# Readiness\n",
        }
        for relative_path, content in text_files.items():
            path = source / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        paper = source / "records/artifacts/paper/pwinfer-analysis.pdf"
        paper.parent.mkdir(parents=True, exist_ok=True)
        paper.write_bytes(b"%PDF-1.7\n")
        component_files = {
            "topic-main": ("main.txt", b"sanitized topic main\n"),
            "reviewer": ("reviewer.txt", b"sanitized topic actor\n"),
            "coder": ("coder.txt", b"sanitized agent\n"),
            "powerinfer": ("upstream.txt", b"registered upstream reference\n"),
        }
        for name, (filename, content) in component_files.items():
            component_root = source / component_paths[name]
            component_root.mkdir(parents=True)
            (component_root / filename).write_bytes(content)
            if name in {"reviewer", "coder"}:
                (component_root / ".git").write_text(
                    f"gitdir: /private/topic-main/.git/worktrees/{name}\n",
                    encoding="utf-8",
                )

    def _fresh_branch_repo(self, path: Path, branch: str, filename: str, content: bytes) -> Path:
        path.mkdir()
        self._git(path, "init")
        self._git(path, "config", "user.name", "Isomer Publication")
        self._git(path, "config", "user.email", "isomer-publication@invalid")
        (path / filename).write_bytes(content)
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
