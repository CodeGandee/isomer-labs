---
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Pipeline Placeholders

This page defines the control-surface objects that `isomer-ext-deepsci-entrypoint` produces or consumes. The pipeline skill does not introduce new research objects; it orchestrates the existing objects defined in `isomer-ext-deepsci-entrypoint->shared`.

| Semantic id | Meaning | Required semantic content | Typical producers | Typical consumers |
| --- | --- | --- | --- | --- |
| `DEEPSCI:PIPELINE-RECIPE-CONTEXT` | Initial context provided by the caller | Pipeline name, optional starting stage, input artifacts, parameters, budget or checkpoint preferences | External controller | `isomer-ext-deepsci-entrypoint` |
| `DEEPSCI:PIPELINE-TERMINAL-REPORT` | End-of-run summary for external controllers | Pipeline id, status, completed stages, produced artifacts, final artifact, recommended next action, blocker or pause reason, resume point | `isomer-ext-deepsci-entrypoint` | External controller, `isomer-deepsci-decision`, user |
| `DEEPSCI:PIPELINE-RUN-RECORD` | Audit log of one pipeline invocation | Recipe id, stage sequence, stage results, artifact handoffs, transition decisions, pause/block events | `isomer-ext-deepsci-entrypoint` | External controller, future resume logic |
| `DEEPSCI:PIPELINE-RESUME-PACKET` | Resume context for a paused pipeline | Pipeline id, last completed stage, current stage, pending stages, available artifacts, blocker or pause reason | `isomer-ext-deepsci-entrypoint` | External controller, future `isomer-ext-deepsci-entrypoint` resume |
