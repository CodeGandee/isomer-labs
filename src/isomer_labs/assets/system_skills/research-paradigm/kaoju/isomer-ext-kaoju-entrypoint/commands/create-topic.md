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
3. After generic state is ready, invoke `isomer-ext-kaoju-entrypoint->topic-creator` in create-missing mode to derive the three topic-owned Mindset Sources and run `isomer-cli --print-json ext kaoju paper template ensure-defaults --topic TOPIC --actor agent`.
4. Preserve every existing valid Source and ready named template record. Create only missing state. Export absent safe working copies to `<topic.paper.template_exchange_root>/content/main/` and `/latex/main/`, while preserving edited, stale, identity-invalid, or unrecognized existing targets for explicit reconciliation.
5. Report one resumable result with every mindset key and each template role classified as created, preserved, exported, invalid, drifted, or conflicting.
6. Inventory the actual recognized `intent/derived` material. Explain that Mindset Sources directly control future Run reflection; `writing-templates/content/main/` is a non-canonical editable MyST structure copy; `writing-templates/latex/main/` is a non-canonical editable presentation copy; and generated environment target specifications must be regenerated from source intent rather than applied directly.
7. Tell the user which adjustments each material supports and that they may edit before the next initialization stage or after later use. For writing-template edits, explain that the agent must promote them through typed create or optimistic-concurrency update. Tell the user to say “I have modified the derived materials, now apply them” after editing.
8. Stop after the derived-material handoff. Do not begin environment setup, actor setup, a research Run, acquisition, examination, paper drafting, or Mindset Record materialization unless the original request explicitly included that later target.

If the user's task does not map cleanly to these steps, use the native planning tool to separate generic topic prerequisites from Kaoju derived-intent creation, then execute only the authorized stages.

## Owner, Inputs, and Outputs

Owner: `isomer-ext-kaoju-entrypoint->topic-creator`. Generic prerequisite owner: `isomer-op-entrypoint->topic-create`. Template mutation owner: `isomer-ext-kaoju-entrypoint->write`. Input: one concrete `topic.intent.overview` and ready Workspace Runtime. Outputs: validated topic-owned `paper.deep-dive`, `paper.skimming`, and `source-code.ingest` Mindset Sources beneath `topic.intent.kaoju_mindsets`; canonical content and LaTeX `main` stock; and non-canonical plural-path working copies.

## Gates, Blockers, and Resume

Topic selection, topic creation, and user-authored intent choices retain their existing Gates. Missing generic state pauses at the generic owner. Invalid Source JSON, invalid template state, or conflicting exchange content pauses at Kaoju repair without overwrite. Retry preserves completed roles and resumes only missing work. Resume at generic topic readiness, create-missing, ensure-defaults, explicit Source reconciliation, or state-checked template reconciliation.
