## Context

`isomer-admin-topic-team-specialize` already exposes `clarify-topic` and `clarify-topic-team` as public procedural subcommands. Each page currently says to identify open questions, ask the user, and revise the relevant docs, but neither page defines a concrete interaction pattern. That leaves room for broad multi-question prompts, hidden assumptions, or a transcript-style answer log that does not update the artifacts the later workflow actually reads.

The ImSight project exploration skill has a useful option-asking pattern in its `auto`, `design-choice`, `brainstorm`, and `usecase-design` flows. The reusable parts are the coverage scan, one-question-at-a-time loop, proposed answer, implications, answer validation, and incremental integration after each accepted answer. The parts that do not fit are ADR creation and separate design-choice notes, because Topic Team Specialization should produce static topic-team material, not a decision-log side channel.

The operator skill validator currently allowlists the topic-team specialization reference pages. Adding a shared `option-clarification-pattern.md` support reference would require validator and unit-test changes. This change can stay smaller by documenting the loop directly in the two existing `clarify-*` pages.

## Goals / Non-Goals

**Goals:**

- Make `clarify-topic` and `clarify-topic-team` ask focused, decision-bearing questions instead of broad open-ended batches.
- Give each question a proposed answer, rationale, and downstream implication so the user can accept, choose, or override quickly.
- Update the owning static artifacts directly after each accepted answer.
- Keep the existing predecessor-artifact refusal rule, static-material scope, and no-live-runtime boundary intact.

**Non-Goals:**

- Do not add new public or helper subcommands.
- Do not add a new shared reference page unless implementation discovers the validator should be expanded.
- Do not create ADRs, decision logs, or separate user-decision files for these clarification subcommands.
- Do not change `fast-forward`, `step-by-step`, approval, materialization, or live runtime behavior beyond their existing use of `clarify-*` when needed.

## Decisions

### Embed the clarification loop in the two subcommand pages

The implementation will add compact sections to `clarify-topic.md` and `clarify-topic-team.md` for coverage scanning, question constraints, sequential questioning, and integration after each answer. This avoids changing the reference-page allowlist and keeps the behavior visible where the agent loads it.

Alternative considered: add a local support reference and link both pages to it. That would reduce duplicated wording, but it would also require validator and test edits for a small prose-level behavior change.

### Update artifacts directly instead of recording user decisions

Accepted answers will revise the artifact that later workflow steps consume. For `clarify-topic`, that artifact is `topic-overview.md`. For `clarify-topic-team`, it can be copied template material, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, deferrals, or draft packet/profile inputs.

Alternative considered: record each answer as a separate clarification log. That matches some exploration workflows, but it would create a second source of truth and force later steps to merge logs back into the topic-team material.

### Use a bounded one-question loop

Each clarification session will ask one question at a time, with a maximum of five questions. Questions must be either 2-5 mutually exclusive options plus a custom short-answer escape hatch, or a short-answer prompt with a proposed answer. The agent stops when critical ambiguity is resolved, the user stops, or the question limit is reached.

Alternative considered: ask all open questions at once. That is faster on paper, but it tends to produce shallow answers and makes it harder to update artifacts incrementally after each clarification.

## Risks / Trade-offs

- [Risk] The two pages may drift because the shared loop is duplicated. → Mitigation: keep the shared wording short and task-specific, and validate both pages together during implementation.
- [Risk] A maximum of five questions may leave lower-priority ambiguity unresolved. → Mitigation: require remaining ambiguities to stay in `Open Questions`, `deferrals`, blockers, or `Final Report` as appropriate.
- [Risk] Direct artifact updates can overwrite useful earlier assumptions. → Mitigation: require obsolete or corrected assumptions to be replaced or marked revised, not silently discarded.
- [Risk] Agents may treat every uncertainty as user-facing. → Mitigation: require the coverage scan to ask only questions whose answers materially affect scope, objectives, template selection, role design, workflow, policy, bindings, copied material, setup, validation, or blockers.
