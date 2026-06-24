# Agents

## Purpose

Generated concrete Houmao agent bindings and prompt material for the DeepResearch tree-loop. Binds the
seven participant instances (one root + six specialists: scout-ideator, experimenter, analyst, writer,
reviewer, and the independent idea-level BO-reviewer) to easy profiles, generated skills, role prompts,
memo seeds, notifier wiring, and workspace policy. Live profile creation / launch is owned by the
execution subskills (`prepare-agents`, `launch-agents`), not this stage.

## Contents

- `bindings.toml`: participant-to-agent binding registry (tool, skills, prompts, workspace policy).
- `profiles/`: per-agent `definition.md` (role prompt) + `memo-seed.md`.
- `notifier-prompts/`: per-agent mail-notification prompt (wakeup → dispatch by `schema_id` → one bounded turn).
