# Clarify Research Intent

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If `topic.intent.overview` is missing, refuse to run directly and explain that there is no topic definition to clarify. Offer targeted fast-forward recovery through `create-research-intent` when the missing artifact can be created by the canonical flow.
2. Resolve and read clarification inputs:
   - Read `topic.intent.overview`, plus any user answers, source material, or newly supplied constraints.
   - In `isomer-default.v1`, the resolved path is `<topic-workspace>/intent/src/topic-overview.md`.
   - Load the canonical template from `templates/topic-overview.md` in this skill bundle as the section checklist.
3. Run the **Coverage and Clarity Scan** against `topic-overview.md` and any newly supplied context.
4. Build a queue of at most five clarification questions from unresolved items that materially affect topic scope, objectives, assumptions, open questions, methodology, expected outcomes, or later setup.
5. Execute the **Sequential Clarification Loop**, asking exactly one focused question at a time.
6. After each accepted answer, update the resolved `topic.intent.overview` path directly through **Direct Topic Overview Integration**.
7. Stop when the topic is actionable, the user signals completion, or five clarification questions have been asked.
8. Report the clarification result:
   - Include the revised topic understanding, changed `topic.intent.overview` label and path metadata, remaining open questions, and readiness for `define-topic-env`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step clarification plan from the topic overview, user answers, and Project Config boundary, then execute the plan.

## Coverage and Clarity Scan

Before asking the user anything, inspect `topic-overview.md` and classify each category as **Clear**, **Partial**, or **Missing**:

| Category | What to Check |
| --- | --- |
| Research Topic | Is the concrete research question or investigation intent specific enough to guide later work? |
| Abstract | Does the overview summarize what the topic studies, why it matters, how the work will proceed, and what kind of result counts as useful? |
| Introduction and Background | Is the practical or scientific context clear enough for an unfamiliar reader to understand why the problem is worth investigating? |
| Research Objective | Are the primary and supporting objectives observable, and is the unresolved problem or research gap explicit? |
| Literature and Prior Work | Are the anchoring papers, repositories, benchmarks, datasets, systems, or standards named? |
| Methodology and Research Design | Is the planned approach, evidence source, tools, comparison targets, validation method, and expected analysis path described enough to start setup? |
| Expected Outcomes | Are the expected outputs and why they matter stated? |
| Additional Requirements | Are topic-specific preferences and constraints (`should`/`must`) captured, or are they still placeholder text? |
| Related Links | Are relevant references listed when known? |
| Open Questions | Do open questions affect scope, methodology, or setup rather than minor prose polish? |

Add a candidate clarification question for each **Partial** or **Missing** category only when the answer would materially change `topic-overview.md` or determine whether `define-topic-env` and later stages can proceed. Exclude questions already answered by the file, trivial style preferences, and implementation details that belong to later subcommands.

If more than five candidate questions remain, rank them by impact and uncertainty, then ask only the top five in the current clarification session. Keep lower-priority ambiguity in `## Open Questions` rather than hiding it.

## Question Format

Ask exactly one question at a time. Use a multiple-choice question when there are two to five meaningful alternatives; otherwise use a short-answer question.

For every question, include:

- **Motivation**: why this answer matters for topic scope, objectives, assumptions, open questions, methodology, expected outcomes, or readiness for `define-topic-env`.
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
| Research topic wording | `## Research Topic` |
| Abstract text | `## Abstract` |
| Background or motivation | `## Introduction and Background` |
| Objective or research gap | `## Research Objective` |
| Prior work or references | `## Literature and Prior Work` or `## Related Links` |
| Method, tools, validation | `## Methodology and Research Design` |
| Expected outputs | `## Expected Outcomes` |
| Preference or constraint | `## Additional Requirements` (`### Preferences` or `### Constraints`) |
| Resolved uncertainty | `## Open Questions` |
| Source clarification | `## Related Links` or `## Literature and Prior Work` |

Replace obsolete or contradicted text instead of duplicating it. Preserve earlier assumptions unless the user corrects them; when corrected, mark them as revised or rewrite them so the current document has one clear source of truth. Remove resolved questions from `## Open Questions`, and leave unresolved lower-priority questions there with enough context for later `clarify-research-intent` runs.

## Prerequisite Artifacts

Required predecessor artifact:

- `topic.intent.overview` from `create-research-intent` or an existing topic overview file.

If `topic.intent.overview` does not exist, refuse to run directly, explain that there is no topic definition to clarify, and offer targeted fast-forward recovery to `create-research-intent`. If the original request lacks enough topic substance for `create-research-intent`, ask for the actual Research Topic and stop before creating files.

## Guardrails

Do not derive topic env target specs, install dependencies, create Actor Workspaces, mutate Workspace Runtime, or launch live agents from this subcommand. Stop after topic intent clarification and route to `define-topic-env` when the intent is ready.

Do not create ADRs, decision logs, user-decision records, or separate clarification transcripts as durable sources of truth for user answers. The durable result of this subcommand is the revised `topic-overview.md`.

Do not silently discard earlier assumptions. Mark corrected assumptions as revised.

Do not promote a provisional topic workspace seed into authoritative Project Manifest state.

Do not invoke `clarify-research-intent` from `fast-forward`, `run-to`, `step-by-step`, or any other automatic workflow.
