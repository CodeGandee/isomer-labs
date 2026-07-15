# Finalization Checklist

Use this checklist before closing, pausing, archiving, publishing, or handing off a Research Topic. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Answer closure questions**. Confirm what is genuinely supported, partially supported, failed, unresolved, and recommended next.
2. **Check final report contents**. Ensure DEEPSCI:FINAL-SUMMARY includes executive state, strongest findings, negative results, limitations, packaging status, recommendation, and reopen conditions.
3. **Check claim ledger minimums**. Ensure each major claim has text or id, status, evidence, caveats, and safe-to-surface status.
4. **Check package inventory**. Identify baseline package, decisive runs, reports, analysis outputs, drafts, outlines, review or proofing outputs, summary, and status files when present.
5. **Check reopen conditions**. State exactly what would justify reopening the Research Topic.
6. **Run anti-pattern scan**. Reject closure that erases negative evidence, omits claim statuses, skips package inventory, or relies on chat-only recollection.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer checklist-backed closure over a polished but unverifiable summary.
- Prefer package inventory when code, experiments, or writing outputs exist (if no package exists, otherwise state that explicitly).
- Prefer concrete reopen conditions over generic future-work language.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Finalization must not call a Research Topic successful without claim statuses.
- Finalization must not omit package inventory when outputs exist.
- Finalization must not rely on chat memory instead of durable files, artifacts, or records.
- Finalization must not erase negative evidence or failed branches.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Final-report component coverage: fraction of supported claims, partial claims, failed branches, unresolved blockers, limitations, recommendation, and reopen condition components included; higher is better.
- Package-inventory coverage: fraction of required paper or release manifest paths checked when a paper-like deliverable exists; higher is better.

### Checks

- Checklist coverage: closure questions, report contents, claim ledger, package inventory, and reopen conditions are all checked.
- Anti-pattern gate: none of the source anti-patterns remain true.
- Inventory gate: package, run, report, analysis, writing, summary, and status records are named when present.
- Closure confidence: the checklist supports DEEPSCI:CLOSURE-DECISION or identifies DEEPSCI:FINALIZE-BLOCKER-RECORD.
