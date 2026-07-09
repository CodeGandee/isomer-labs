## Context

`imsight-project-explore` recently hardened its questioning loop to prevent agents from listing all questions at once without proposed options. The sequential rules are now embedded as numbered workflow steps and referenced subsections rather than side notices. This change adds an opt-in batch mode while preserving sequential as the default.

## Goals / Non-Goals

**Goals:**

- Add an explicit batch question mode to `auto`, `design-choice`, and `any-open-question`.
- Keep batch mode opt-in via clear user phrases.
- Encode the sequential-vs-batch decision as a numbered workflow step, not a side notice.
- Provide a consistent batch response format across all three modes.
- Define how batch responses are integrated when the user overrides some answers and accepts the rest.

**Non-Goals:**

- Changing the default from sequential to batch.
- Adding a CLI-style flag such as `--batch`; detection is chat-phrase based.
- Supporting batch mode in modes that do not ask clarification questions (e.g., `domain-language`, `review-decision`, `brainstorm`, `usecase-design`).

## Decisions

1. **Opt-in via explicit user phrases.** The user says something like "list all at once", "batch mode", "show all options", or "let me pick which ones to change". This keeps the safe default and makes intent unambiguous.
2. **Branch encoded as a workflow step.** In each affected mode, after the coverage scan, add a numbered step "Choose questioning mode" that sets `mode = sequential` or `mode = batch` based on the user's prompt. The next steps branch on that mode. This follows the same pattern already used for the sequential-only workflow steps.
3. **Same maximum question count.** Batch mode still caps at 5 questions, the same as sequential.
4. **Each question carries a Proposed option and short Pros/Cons.** This preserves the quality guard from sequential mode.
5. **Batch response integration order.** Process overrides in the order given, apply proposed defaults to unmentioned items, and flag any downstream proposed option that becomes invalid because of an earlier override.
6. **Update Invocation Contract in SKILL.md.** List the trigger phrases once at the top level so every mode inherits them.

## Risks / Trade-offs

- **Risk**: Batch mode loses the adaptive benefit where later questions depend on earlier answers.  
  **Mitigation**: Process overrides in order and re-evaluate downstream proposed options; flag invalidated ones and ask the user to confirm or revise them.
- **Risk**: Agents may misdetect batch mode from casual user phrasing.  
  **Mitigation**: Use a small, explicit phrase list and keep sequential as the default when detection is uncertain.
- **Risk**: Duplicated workflow branching across three mode files.  
  **Mitigation**: Keep each branch local to the affected mode; the pattern is small and the files are independent.

## Migration Plan

1. Update `SKILL.md` Invocation Contract with batch-mode trigger phrases.
2. Update `commands/auto.md` workflow to choose mode and branch.
3. Update `commands/design-choice.md` workflow to choose mode and branch.
4. Update `commands/any-open-question.md` workflow to choose mode and branch.
5. Add a shared batch response format example to each mode file.
6. Validate that default sequential behavior is unchanged and that no side-notice style guards are introduced.

## Open Questions

- Should batch mode be allowed when more than 5 candidate questions exist, or should it enforce the same 5-question cap as sequential?
- Should the agent re-run the coverage scan after a batch response and ask follow-up questions if an override opens a new ambiguity?
