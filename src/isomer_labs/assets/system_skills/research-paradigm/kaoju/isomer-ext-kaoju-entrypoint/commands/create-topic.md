---
skill_invocation_notation: >
  Invoke this direct public command as `isomer-ext-kaoju-entrypoint->create-topic()`.
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
