from __future__ import annotations

from pathlib import Path
import re
import unittest


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_ROOT = (
    REPO_ROOT
    / "src"
    / "isomer_labs"
    / "assets"
    / "system_skills"
    / "operator"
    / "isomer-op-entrypoint"
    / "subskills"
    / "isomer-op-topic-workspace-git"
)


def shell_commands(path: Path) -> tuple[str, ...]:
    commands: list[str] = []
    in_shell = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_shell:
                in_shell = False
            else:
                in_shell = stripped.removeprefix("```").strip() in {"bash", "sh", "shell"}
            continue
        if in_shell and stripped:
            commands.append(stripped)
    return tuple(commands)


class TopicGitSkillContractTests(unittest.TestCase):
    def test_required_progressive_disclosure_pages_exist(self) -> None:
        required = (
            "SKILL-MAIN.md",
            "agents/openai.yaml",
            "references/context-queries.md",
            "references/direct-git-safety.md",
            "references/local-safety.md",
            "references/publication-safety.md",
            "references/privacy-projection.md",
            "references/persistence.md",
            "commands/status.md",
            "commands/local/status.md",
            "commands/local/init.md",
            "commands/local/plan.md",
            "commands/local/ignore.md",
            "commands/local/commit.md",
            "commands/publish/status.md",
            "commands/publish/init.md",
            "commands/publish/plan.md",
            "commands/publish/sync.md",
        )
        for relative in required:
            with self.subTest(relative=relative):
                self.assertTrue((SKILL_ROOT / relative).is_file())

    def test_local_shell_commands_have_no_remote_or_publication_side_effect(self) -> None:
        commands = tuple(
            command
            for path in sorted((SKILL_ROOT / "commands" / "local").glob("*.md"))
            for command in shell_commands(path)
        )
        self.assertTrue(commands)
        for command in commands:
            with self.subTest(command=command):
                self.assertTrue(command.startswith("git -C "))
                self.assertIsNone(re.search(r"\s(?:remote|fetch|pull|push)\s", command))
                self.assertNotIn("topic-publication-copy", command)

    def test_publish_init_has_no_push_and_publication_git_stays_copy_scoped(self) -> None:
        init_commands = shell_commands(SKILL_ROOT / "commands" / "publish" / "init.md")
        self.assertFalse(any(re.search(r"\bpush\b", command) for command in init_commands))
        publication_commands = tuple(
            command
            for path in sorted((SKILL_ROOT / "commands" / "publish").glob("*.md"))
            for command in shell_commands(path)
            if command.startswith("git ")
        )
        self.assertTrue(publication_commands)
        for command in publication_commands:
            with self.subTest(command=command):
                self.assertTrue(command.startswith("git -C "))
                self.assertNotIn("<source-topic-workspace>", command)

    def test_isomer_queries_are_read_only_and_no_topic_git_cli_family_exists(self) -> None:
        commands = tuple(
            command
            for path in sorted(SKILL_ROOT.rglob("*.md"))
            for command in shell_commands(path)
            if command.startswith("isomer-cli ")
        )
        self.assertTrue(commands)
        self.assertTrue(all(command.startswith("isomer-cli --print-json ") for command in commands))
        all_text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(SKILL_ROOT.rglob("*.md")))
        self.assertNotIn("isomer-cli project topic-git", all_text)

    def test_direct_git_commands_are_path_scoped_exact_and_avoid_unsafe_operations(self) -> None:
        commands = tuple(
            command
            for path in sorted(SKILL_ROOT.rglob("*.md"))
            for command in shell_commands(path)
            if command.startswith("git ")
        )
        for command in commands:
            with self.subTest(command=command):
                self.assertTrue(command.startswith("git -C "))
                self.assertIsNone(re.search(r"\badd\s+(?:--\s+)?(?:\.|-A)(?:\s|$)", command))
                self.assertIsNone(re.search(r"\s(?:pull|merge|rebase|reset|clean)(?:\s|$)", command))
                self.assertNotIn("--all", command)
                self.assertNotIn("--mirror", command)
                self.assertNotIn("--delete", command)

    def test_non_git_helpers_do_not_execute_processes(self) -> None:
        helper_root = REPO_ROOT / "src" / "isomer_labs" / "topic_git"
        text = "\n".join(path.read_text(encoding="utf-8") for path in sorted(helper_root.rglob("*.py")))
        for forbidden in ("import subprocess", "from subprocess", "os.system", "os.popen", "Popen("):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, text)


if __name__ == "__main__":
    unittest.main()
