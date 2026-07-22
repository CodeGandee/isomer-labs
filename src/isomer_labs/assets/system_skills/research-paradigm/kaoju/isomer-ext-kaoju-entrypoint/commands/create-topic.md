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

# Create Kaoju Topic Intent

## Workflow

1. Resolve one Project, Research Topic, and Topic Workspace through the public Kaoju entrypoint.
2. Delegate missing generic topic creation, Workspace Runtime initialization, and concrete `topic.intent.overview` work to `isomer-op-entrypoint->topic-create`. Do not pass Kaoju mindset data, paths, schemas, seeds, or generation instructions into that core skill.
3. After generic state is ready, invoke `isomer-ext-kaoju-entrypoint->topic-creator` in create-missing mode to derive the three topic-owned Mindset Sources.
4. Preserve every existing valid Source, block on every invalid existing Source, and report created, preserved, invalid, missing, and advisory derivation-drift results by key.
5. Stop after Kaoju derived intent is ready. This command does not begin a research Run, acquire material, examine a source, or materialize a Mindset Record.

If the user's task does not map cleanly to these steps, use the native planning tool to separate generic topic prerequisites from Kaoju derived-intent creation, then execute only the authorized stages.

## Owner, Inputs, and Outputs

Owner: `isomer-ext-kaoju-entrypoint->topic-creator`. Generic prerequisite owner: `isomer-op-entrypoint->topic-create`. Input: one concrete `topic.intent.overview`. Outputs: validated topic-owned `paper.deep-dive`, `paper.skimming`, and `source-code.ingest` Mindset Sources beneath `topic.intent.kaoju_mindsets`.

## Gates, Blockers, and Resume

Topic selection, topic creation, and user-authored intent choices retain their existing Gates. Missing generic state pauses at the generic owner. Invalid Source JSON pauses at Kaoju repair without overwrite. Resume at generic topic readiness, create-missing, or explicit Source reconciliation.
