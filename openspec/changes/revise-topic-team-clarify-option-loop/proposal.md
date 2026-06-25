## Why

The topic-team specialization skill currently tells `clarify-topic` and `clarify-topic-team` to ask for missing information, but it does not define how those clarifications should be framed, sequenced, or integrated. This makes the two subcommands inconsistent when a topic or specialized team has multiple open questions.

ImSight project exploration already has a useful option-asking pattern: scan the artifact, ask one focused decision-bearing question at a time, propose a likely answer, and integrate each accepted answer before continuing. The topic-team skill should adopt that interaction style while preserving its own static-material boundary and avoiding separate decision-log artifacts.

## What Changes

- Revise `clarify-topic` so it runs a coverage and clarity scan over `topic-overview.md`, selects the highest-impact unresolved topic questions, asks them one at a time, and writes accepted answers directly back into `topic-overview.md`.
- Revise `clarify-topic-team` so it scans specialization outputs, asks focused option or short-answer questions about role, workflow, policy, binding, copied-material, or blocker ambiguities, and writes accepted answers directly into the relevant copied topic-team artifacts.
- Require both `clarify-*` subcommands to use an ImSight-style sequential question loop with a proposed answer, rationale, downstream implication, 2-5 mutually exclusive options or a short-answer prompt, answer validation, and a maximum of five questions per clarification session.
- Explicitly prohibit separate user-decision records for these clarification flows. Durable results live in the revised topic overview, copied material, specialization plan, `Final Report`, placeholder resolutions, deferrals, and draft packet/profile inputs.
- Keep the existing predecessor-artifact refusal behavior, static-material boundary, and no-live-runtime guardrails unchanged.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `topic-team-specialization-module-skill`: define the clarification interaction contract for `clarify-topic` and `clarify-topic-team`, including direct artifact updates and no separate decision logs.

## Impact

- Affects `skillset/operator/isomer-admin-topic-team-specialize/references/clarify-topic.md`.
- Affects `skillset/operator/isomer-admin-topic-team-specialize/references/clarify-topic-team.md`.
- Affects the `topic-team-specialization-module-skill` OpenSpec capability.
- May affect operator skill validation if the repository chooses to enforce the new clarification-loop wording.
