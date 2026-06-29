# Approve Profile

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run directly and use **Targeted Fast-Forward Recovery** from the entrypoint when the missing predecessor can be created by the canonical flow.
2. Read approval inputs:
   - Include the draft profile bundle summary, registration assurance evidence, packet validation report, copied material plan, proposed topic edits, static-material blockers, later-operation blockers, and `isomer-topic-summary.md`.
3. Present review points:
   - Include registered Research Topic and Topic Workspace refs, selected roles, inactive roles, role binding refs, policy refs, expected Artifacts, copied material, support outputs, unresolved placeholders, and provenance refs.
4. Capture approval state, approval ref, approval actor or session ref, approval mode, review summary, validation result ref, and timestamp.
5. Update packet-shaped approval provenance or request repair when approval is withheld.
6. Return whether materialization may proceed and which validation command must run next.

If the user's task does not map cleanly to these steps, use your native planning tool to review the available packet and draft evidence, then execute the smallest approval-safe path.

## Prerequisite Artifacts

Required predecessor artifacts:

- `isomer-topic-summary.md` from `finalize-topic-team`.
- Draft profile or packet/profile input summary from `adapt-team-template`.
- Packet validation output or explicit validation blocker.

If the final summary or draft profile evidence is missing, refuse to run directly, explain that approval needs reviewable team material, and offer targeted fast-forward recovery to `approve-profile`. Use `python scripts/query_step_dependencies.py path --target approve-profile --include-target` for the inclusive default path and `python scripts/query_step_dependencies.py path --target approve-profile --exclude-target` for the exclusive path.

## Reference Routing

Read first:

- Packet validation output and draft profile bundle summary.
- User approval instruction or deterministic test approval fixture.

Read as needed:

- Existing support Artifact summaries.
- Domain Agent Team Template inspection summary when role or copy choices are disputed.

## Exit Criteria

- Approval provenance is complete or withheld with reasons.
- The packet state is approved, draft, rejected, or blocked.
- The next validator or materializer command is explicit.

## Guardrails

- Do not treat missing approval as implicit approval.
- Do not convert this approval into a Gate or Decision Record unless the project already asks for that separate record.
- Do not treat approval as live runtime approval, Agent Team Instance attachment, or execution adapter preflight.
- Do not approve later-operation blockers without naming their impact and required action.
