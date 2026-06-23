# skill-creator

An adaptation of Anthropic's `skill-creator` skill for creating, evaluating, and packaging agent skills.

## Origin

This skill is derived from <https://github.com/anthropics/skills/tree/main/skills/skill-creator> and retains the Apache 2.0 license of the original work.

## Project Layout

The skill source lives in `skillset/skill-creator/` and is exposed to the agent runtime through the symlink `.agents/skills/skill-creator`.

## What Changed

- **Invocation model**: Rewrote instructions for explicit skill invocation rather than description-triggered skills.
- **Subagents**: Replaced platform-specific subagent mechanics with generic subagent instructions and a new `agents/executor.md` instruction file.
- **Description optimization**: Removed the automated trigger-optimization loop; skills are invoked explicitly, so description tuning is manual.
- **Benchmark orchestration**: Added `scripts/prepare_benchmark.py` to set up workspace directories and print ready-to-use subagent prompts. The actual subagent runs are launched by the parent agent.
- **Validation**: Rewrote `scripts/quick_validate.py` to parse frontmatter without PyYAML so the skill is self-contained.
- **Terminology and viewer**: Removed platform-specific branding from SKILL.md, agent instructions, and the HTML eval viewer.

## Files

- `SKILL.md` — Main skill instructions.
- `agents/` — Subagent instruction files (executor, grader, analyzer, comparator).
- `scripts/` — Validation, packaging, benchmark preparation, and aggregation scripts.
- `eval-viewer/` — Standalone HTML review viewer.
- `references/schemas.md` — JSON schemas for evals, grading, benchmark, etc.
- `assets/eval_review.html` — Template for reviewing trigger-eval queries.
- `LICENSE.txt` — Apache 2.0 license from the original Anthropic skill.

## Quick Start

Validate the skill:

```bash
cd skillset/skill-creator
python -m scripts.quick_validate .
```

Package the skill:

```bash
python -m scripts.package_skill . /tmp/dist
```

Prepare a benchmark workspace for a skill you are developing:

```bash
python -m scripts.prepare_benchmark .agents/skills/your-skill --iteration 1
```
