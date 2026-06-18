# `shared/` — OPTIONAL staging / templates only (NOT canonical)

This directory is **not** the canonical source for any quest input. As of the per-quest convention:

- **Objective** → canonical at **`runs/<quest-id>/objective/{objective.md, acceptance.md}`**
- **Baseline** (comparator + metric contract) → canonical at **`runs/<quest-id>/baseline/`**

Each quest keeps its own objective and baseline under `runs/<quest-id>/`, so quests never overwrite each
other's inputs and stay self-contained alongside their results.

`shared/objective/` and `shared/baseline/` remain only as **optional staging / template areas** — e.g. to
draft or reuse a brief/baseline across quests before copying it into a new quest's `runs/<q>/…`. Agents do
**not** read from `shared/` as a canonical source.

Knowledge packs live under **`execplan/packs/`** (enabled via `seed.toml` / `knowledge_pack.register`) —
**not** under `shared/`.

## Per-quest folder & `outputs/` (legacy)

**Every quest** keeps everything it produces — objective, baseline, code repo, worktrees, rounds, report,
figures, refs, findings — under **`runs/<quest-id>/`**, with the quest's code repo (`quest.workspace_ref`) at
**`runs/<quest-id>/repo/`**. The only shared, cross-quest state is the control plane: the single DB
`runs/state.sqlite` and the `.houmao/mailbox` messaging infra.

**`outputs/` is an unused legacy top-level location.** **Do not use `outputs/` for any quest** — all materials
live under `runs/<quest-id>/`.

Authority: `execplan/specs/workspace/workspace.toml` (`[shared]`, `[meta]` LEGACY note), `execplan/docs/start-runbook.md` (Step 3/4).
