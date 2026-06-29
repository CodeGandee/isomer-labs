# Clarify Topic

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Resolve and read `topic.intent.overview`, plus any user answers, source material, or newly supplied constraints. In `isomer-default.v1`, the resolved path is `<topic-workspace>/intent/src/topic-overview.md`.
3. Run the **Coverage and Clarity Scan** against `topic-overview.md` and any newly supplied context.
4. Build a queue of at most five clarification questions from unresolved items that materially affect topic scope, objectives, assumptions, open questions, or template selection.
5. Execute the **Sequential Clarification Loop**, asking exactly one focused question at a time.
6. After each accepted answer, update the resolved `topic.intent.overview` path directly through **Direct Topic Overview Integration**.
7. Stop when the topic is actionable, the user signals completion, or five clarification questions have been asked.
8. Report the revised topic understanding, changed `topic.intent.overview` label and path metadata, remaining open questions, provisional registration status, and whether `ensure-topic-registration` can proceed.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step clarification plan from the topic overview, user answers, and Project Config boundary, then execute the plan.

## Coverage and Clarity Scan

Before asking the user anything, inspect `topic-overview.md` and classify each category as **Clear**, **Partial**, or **Missing**:

| Category | What to Check |
| --- | --- |
| Research Topic | Is the concrete research question or investigation intent specific enough to guide a team? |
| Scope | Are domain, dataset, system, exclusions, and boundaries clear enough to avoid over-specializing the team? |
| Initial Objectives | Are success criteria and initial research objectives observable enough to inform task decomposition? |
| Assumptions | Are assumptions explicit, still valid, and not contradicted by newer user input or source material? |
| Open Questions | Do open questions affect specialization, template selection, or later setup rather than minor prose polish? |
| Template Selection Signals | Does the topic imply a needed Domain Agent Team Template, domain level, capability, or workflow style? |
| Source Material | Does the source prompt or supplied material contain unresolved conflicts or unsupported claims? |

Add a candidate clarification question for each **Partial** or **Missing** category only when the answer would materially change `topic-overview.md` or determine whether `ensure-topic-registration` and later `specialize-team` can proceed. Exclude questions already answered by the file, trivial style preferences, and implementation details that belong to later subcommands.

If more than five candidate questions remain, rank them by impact and uncertainty, then ask only the top five in the current clarification session. Keep lower-priority ambiguity in `## Open Questions` rather than hiding it.

## Question Format

Ask exactly one question at a time. Use a multiple-choice question when there are two to five meaningful alternatives; otherwise use a short-answer question.

For every question, include:

- **Motivation**: why this answer matters for topic scope, objectives, assumptions, open questions, template selection, registration readiness, or readiness for `specialize-team`.
- **Example**: a concrete example when it helps the user see how different answers change the topic overview.
- **Proposed**: the agent's recommended option or short answer, with brief rationale.
- **Implication**: what will change in `topic-overview.md` if the user accepts the proposed answer.

For multiple-choice questions, present two to five mutually exclusive options and a `Short` row for a custom answer. The user may reply with an option letter, `yes`, `proposed`, or their own answer.

For short-answer questions, provide the proposed answer and tell the user they may reply with `yes`, `proposed`, or a custom short answer.

## Sequential Clarification Loop

After the user answers:

1. If the user replies with `yes`, `proposed`, `recommended`, or `suggested`, use the previously stated proposal as the answer.
2. Otherwise, validate that the answer maps to one option or is a usable custom answer.
3. If the answer is ambiguous, ask a quick disambiguation question and do not advance the question count.
4. Once the answer is clear, integrate it into `topic-overview.md` before asking the next queued question.
5. Re-scan the affected categories and drop queued questions that the accepted answer made unnecessary.

Stop asking when all critical ambiguity is resolved, the user says to stop or proceed, or five clarification questions have been asked in the current session.

## Direct Topic Overview Integration

Update the resolved `topic.intent.overview` path directly after each accepted answer. Apply the answer to the most relevant sections:

| Answer Type | Update Target |
| --- | --- |
| Research topic wording | `## Research Topic` and `## Agent Understanding` |
| Scope boundary | `## Scope` |
| Objective or success criterion | `## Initial Objectives` |
| Corrected or new assumption | `## Assumptions` |
| Resolved uncertainty | `## Open Questions` |
| Source clarification | `## Source Prompt or Source Material` |

Replace obsolete or contradicted text instead of duplicating it. Preserve earlier assumptions unless the user corrects them; when corrected, mark them as revised or rewrite them so the current document has one clear source of truth. Remove resolved questions from `## Open Questions`, and leave unresolved lower-priority questions there with enough context for later `clarify-topic` runs.

## Prerequisite Artifacts

Required predecessor artifact:

- `topic.intent.overview` from `resolve-topic-intent`.

If `topic.intent.overview` does not exist, refuse to run, explain that there is no topic definition to clarify, and tell the user to run `resolve-topic-intent` first.

## Guardrails

Do not specialize the team from this subcommand. Stop after topic clarification and route to `ensure-topic-registration` when the topic is ready but not registered, then to `specialize-team` after registration blockers are resolved.

Do not create ADRs, decision logs, user-decision records, or separate clarification transcripts as durable sources of truth for user answers. The durable result of this subcommand is the revised `topic-overview.md`.

Do not silently discard earlier assumptions. Mark corrected assumptions as revised.

Do not promote a provisional topic workspace seed into authoritative Project Manifest state.
