#!/usr/bin/env python3
"""
Prepare a benchmark workspace for manual or agent-driven execution.

Most agent runtimes do not provide a CLI for programmatic skill invocation,
so this script does not run the evals itself. Instead, it:

1. Reads `evals/evals.json` from the target skill.
2. Creates the workspace directory structure under `<skill-name>-workspace/iteration-N/`.
3. Writes `eval_metadata.json` files for each eval.
4. Prints ready-to-use subagent prompts for the parent agent to spawn
   with-skill and baseline executor subagents.

Usage:
    python scripts/prepare_benchmark.py <path/to/skill-folder> [--iteration N]

Example:
    python scripts/prepare_benchmark.py .agents/skills/my-skill
"""

import argparse
import json
import sys
from pathlib import Path

from scripts.utils import parse_skill_md


def load_evals(skill_path: Path) -> dict:
    """Load evals/evals.json from the skill directory."""
    evals_file = skill_path / "evals" / "evals.json"
    if not evals_file.exists():
        raise FileNotFoundError(f"Evals file not found: {evals_file}")
    with open(evals_file) as f:
        return json.load(f)


def prepare_workspace(skill_path: Path, iteration: int) -> Path:
    """Create workspace directories for the given iteration."""
    skill_name, _, _ = parse_skill_md(skill_path)
    workspace = Path.cwd() / f"{skill_name}-workspace" / f"iteration-{iteration}"

    evals = load_evals(skill_path)
    for eval_item in evals.get("evals", []):
        eval_id = eval_item.get("id", 0)
        eval_name = eval_item.get("eval_name") or f"eval-{eval_id}"
        for config in ("with_skill", "without_skill"):
            run_dir = workspace / eval_name / config / "run-1"
            run_dir.mkdir(parents=True, exist_ok=True)

        metadata = {
            "eval_id": eval_id,
            "eval_name": eval_name,
            "prompt": eval_item.get("prompt", ""),
            "assertions": eval_item.get("assertions", []),
        }
        metadata_path = workspace / eval_name / "eval_metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2))

    return workspace


def print_subagent_prompts(skill_path: Path, workspace: Path) -> None:
    """Print subagent prompts for with-skill and baseline runs."""
    skill_name, _, _ = parse_skill_md(skill_path)
    evals = load_evals(skill_path)

    print("\n=== Subagent Prompts ===\n")
    print("Spawn these subagents in the same turn. Each prompt is self-contained.\n")

    for eval_item in evals.get("evals", []):
        eval_id = eval_item.get("id", 0)
        eval_name = eval_item.get("eval_name") or f"eval-{eval_id}"
        prompt = eval_item.get("prompt", "")
        files = eval_item.get("files", [])
        inputs = ", ".join(files) if files else "none"

        print(f"--- With-skill run for {eval_name} ---")
        print(
            f"You are an executor subagent. Read agents/executor.md from "
            f"{skill_path.parent / 'skill-creator'} and follow its instructions.\n\n"
            f"Parameters:\n"
            f"- eval_prompt: {prompt}\n"
            f"- skill_path: {skill_path}\n"
            f"- input_files: {inputs}\n"
            f"- outputs_dir: {workspace / eval_name / 'with_skill' / 'run-1' / 'outputs'}\n"
            f"- outputs_to_save: <describe what the user cares about>\n"
        )

        print(f"--- Baseline run for {eval_name} ---")
        print(
            f"You are an executor subagent. Read agents/executor.md from "
            f"{skill_path.parent / 'skill-creator'} and follow its instructions.\n\n"
            f"Parameters:\n"
            f"- eval_prompt: {prompt}\n"
            f"- skill_path: none\n"
            f"- input_files: {inputs}\n"
            f"- outputs_dir: {workspace / eval_name / 'without_skill' / 'run-1' / 'outputs'}\n"
            f"- outputs_to_save: <describe what the user cares about>\n"
        )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prepare a benchmark workspace for skill evaluation"
    )
    parser.add_argument("skill-path", help="Path to the skill directory to evaluate")
    parser.add_argument(
        "--iteration", type=int, default=1, help="Iteration number (default: 1)"
    )
    args = parser.parse_args()

    skill_path = Path(getattr(args, "skill-path")).resolve()
    if not skill_path.is_dir():
        print(f"❌ Skill directory not found: {skill_path}")
        sys.exit(1)

    try:
        workspace = prepare_workspace(skill_path, args.iteration)
    except FileNotFoundError as e:
        print(f"❌ {e}")
        print("   Create evals/evals.json in the skill directory first.")
        sys.exit(1)

    print(f"✅ Workspace prepared: {workspace}")
    print_subagent_prompts(skill_path, workspace)


if __name__ == "__main__":
    main()
