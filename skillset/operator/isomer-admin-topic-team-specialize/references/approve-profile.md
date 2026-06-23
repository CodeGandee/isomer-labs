# Approve Profile

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Read the draft profile bundle summary, packet validation report, copied material plan, proposed topic edits, and launch blockers.
2. Present review points: selected roles, inactive roles, role binding refs, policy refs, expected Artifacts, copied material, support outputs, unresolved placeholders, and provenance refs.
3. Capture approval state, approval ref, approval actor or session ref, approval mode, review summary, validation result ref, and timestamp.
4. Update packet-shaped approval provenance or request repair when approval is withheld.
5. Return whether materialization may proceed and which validation command must run next.

If the user's task does not map cleanly to these steps, use your native planning tool to review the available packet and draft evidence, then execute the smallest approval-safe path.

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
- Do not approve launch-blocking deferrals without naming launch impact and required action.
