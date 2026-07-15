# Clarify Topic Team

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run directly and use **Targeted Fast-Forward Recovery** from the entrypoint when the missing predecessor can be created by the canonical flow.
2. Read specialization outputs:
   - Include topic overview, copied template root, `team-specialization-guide.md`, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, deferrals, and draft profile summary.
3. Run the **Coverage and Clarity Scan** across the specialization outputs.
4. Build a queue of at most five clarification questions from unresolved role, workflow, assumption, policy, binding, copied-material, setup, validation, or blocker ambiguity.
5. Execute the **Sequential Clarification Loop**, asking exactly one focused question at a time.
6. After each accepted answer, update the relevant copied topic-team artifacts directly through **Direct Topic Team Material Integration**.
7. Stop when the specialized team is clear enough for the next static setup or validation step, the user signals completion, or five clarification questions have been asked.
8. Report the Topic Team revision outcome, changed paths, remaining blockers, validation refs, and whether setup or validation can proceed in natural language.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step revision plan from the specialization outputs, requested changes, and guardrails, then execute the plan.

## Coverage and Clarity Scan

Before asking the user anything, inspect the specialization outputs and classify each category as **Clear**, **Partial**, or **Missing**:

| Category | What to Check |
| --- | --- |
| Topic Fit | Do copied team instructions and examples reflect the current `topic-overview.md`? |
| Role Responsibilities | Are topic-specific role goals, boundaries, handoffs, and expected Artifacts clear? |
| Workflow Stages | Are stage order, ownership, inputs, outputs, and review points clear enough for setup and validation? |
| Placeholder Resolutions | Are all template placeholders resolved, explicitly deferred, or blocked with an actionable reason? |
| Policy and Binding Choices | Are policy refs, skill bindings, capability bindings, provider refs, and required constraints explicit enough for static material readiness? |
| Copied Material Edits | Are copied template files consistently adapted without modifying the source Domain Agent Team Template? |
| Setup and Workspace Needs | Are environment and Agent Workspace requirements clear enough for `setup-topic-env` and `setup-agent-workspace`? |
| Deferrals and Blockers | Are unresolved static-material blockers and later-operation blockers explicit and placed where later subcommands will read them? |
| Draft Packet/Profile Inputs | Are draft Topic Team Instantiation Packet and Topic Agent Team Profile Bundle inputs complete enough for later approval or materialization boundaries? |

Add a candidate clarification question for each **Partial** or **Missing** category only when the answer would materially change copied material, `team-specialization-plan.md`, `Final Report`, placeholder resolutions, deferrals, draft packet/profile inputs, setup readiness, or validation readiness. Exclude questions already answered by the artifacts, minor wording choices, and live-runtime choices outside this skill.

If more than five candidate questions remain, rank them by impact and uncertainty, then ask only the top five in the current clarification session. Keep lower-priority ambiguity in deferrals, blockers, `Final Report`, or draft packet/profile inputs rather than hiding it.

## Question Format

Ask exactly one question at a time. Use a multiple-choice question when there are two to five meaningful alternatives; otherwise use a short-answer question.

For every question, include:

- **Motivation**: why this answer matters for role design, workflow, policy, binding, copied material, setup readiness, validation readiness, or blockers.
- **Example**: a concrete example when it helps the user see how different answers change the specialized team.
- **Proposed**: the agent's recommended option or short answer, with brief rationale.
- **Implication**: what copied material, plan section, `Final Report`, placeholder resolution, deferral, or draft packet/profile input will change if the user accepts the proposed answer.

For multiple-choice questions, present two to five mutually exclusive options and a `Short` row for a custom answer. The user may reply with an option letter, `yes`, `proposed`, or their own answer.

For short-answer questions, provide the proposed answer and tell the user they may reply with `yes`, `proposed`, or a custom short answer.

## Sequential Clarification Loop

After the user answers:

1. If the user replies with `yes`, `proposed`, `recommended`, or `suggested`, use the previously stated proposal as the answer.
2. Otherwise, validate that the answer maps to one option or is a usable custom answer.
3. If the answer is ambiguous, ask a quick disambiguation question and do not advance the question count.
4. Once the answer is clear, integrate it into the relevant copied topic-team artifacts before asking the next queued question.
5. Re-scan the affected categories and drop queued questions that the accepted answer made unnecessary.

Stop asking when all critical ambiguity is resolved, the user says to stop or proceed, or five clarification questions have been asked in the current session.

## Direct Topic Team Material Integration

Update the relevant static specialization artifacts directly after each accepted answer. Apply the answer to the most appropriate target:

| Answer Type | Update Target |
| --- | --- |
| Role responsibility or handoff | Copied role instructions, `team-specialization-guide.md`, and `team-specialization-plan.md` |
| Workflow stage or artifact contract | Copied workflow material, `team-specialization-guide.md`, and `Final Report` |
| Placeholder value | Placeholder resolutions and any copied material that contains the placeholder-derived text |
| Policy, skill, capability, or provider binding | Draft packet/profile inputs, copied binding notes, and deferrals if still unresolved |
| Setup or Agent Workspace need | `team-specialization-plan.md`, setup notes, deferrals, or blockers that later setup subcommands will read |
| Static-material blocker | `Final Report`, deferrals, and validation-facing blocker notes |
| Draft packet/profile input | Draft Topic Team Instantiation Packet or Topic Agent Team Profile Bundle input summary |

Replace obsolete or contradicted copied-material text instead of duplicating it. Keep all unresolved static-material blockers and later-operation blockers explicit. If an accepted answer resolves a deferral or blocker, update the deferral or blocker in place so later subcommands do not treat it as still open.

## Prerequisite Artifacts

Required predecessor artifacts from `adapt-team-template`:

- `<topic-workspace>/team-profile/execplan/team-specialization-guide.md`.
- `<topic-workspace>/team-profile/execplan/team-specialization-plan.md` with a filled or pending `Final Report`.
- Draft profile or packet/profile input summary from `draft-profile`.

If any required specialization output is missing, refuse to run directly, explain which artifact is missing, and offer targeted fast-forward recovery to `clarify-topic-team`. Use `python scripts/query_step_dependencies.py path --target clarify-topic-team --include-target` for the inclusive default path and `python scripts/query_step_dependencies.py path --target clarify-topic-team --exclude-target` for the exclusive path.

## Guardrails

- DO NOT approve, materialize, or run the team from this subcommand.

- DO NOT create ADRs, decision logs, user-decision records, or separate clarification transcripts as durable sources of truth for user answers. The durable result of this subcommand is the revised copied topic-team material, specialization plan, `Final Report`, placeholder resolutions, deferrals, and draft packet/profile inputs.

- DO NOT change the source Domain Agent Team Template.

- DO NOT hide unresolved static-material blockers or later-operation blockers. Keep deferrals explicit.
