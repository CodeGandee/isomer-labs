---
name: isomer-rsch-finalize-v2
description: Use when a Research Topic or Research Inquiry is ready to close, pause, archive, publish, or hand off with final claims, limitations, recommendations, and a clean resume path.
---

# Isomer Research Finalize V2

## Overview

Finalize closes or pauses work responsibly. It consolidates accepted evidence, records claim status and limitations, chooses stop, park, publish, or continue-later routing, and refuses closure when evidence or writing gates still block it.

Placeholder definitions live in `migrate/placeholders.md`; storage bindings live in `placeholder-bindings.md`.

## When to Use

Use this skill when:

- The evidence base is stable enough for a final recommendation.
- The user asks for final summary, closure, archive, or handoff.
- A paper, report, or long-running route needs final claim and limitation status.
- A topic should pause with a clean resume packet.

Do not use this skill when:

- Major evidence gaps remain unresolved.
- The current line obviously needs another experiment, analysis, baseline, or idea pass.
- The paper or bundle gates are not submission-ready but finalization is being used to avoid repair.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Gather closure context**. Build <FINALIZE_CONTEXT_BRIEF> from accepted comparator state, runs, analysis, writing state, decisions, blockers, and package or paper manifests. Read `references/closure-gate.md` and `references/finalization-checklist.md` for the inventory gates.
2. **Check closure legitimacy**. If required evidence, writing, review, proofing, or submission gates fail, create <FINALIZE_BLOCKER_RECORD> or route to decision instead of forcing closure. Read `references/closure-gate.md`.
3. **Build the claim ledger**. Classify every important claim in <CLAIM_LEDGER> as supported, partially supported, unsupported, or deferred with evidence and caveats. Read `references/claim-ledger-template.md`.
4. **State limitations and failures**. Create <FINAL_LIMITATIONS_REPORT> including data, metric, implementation, resource, literature, and unsupported-claim limits. Read `references/final-summary-template.md` and `references/finalization-checklist.md`.
5. **Write final state**. Produce <FINAL_SUMMARY> and <RESUME_PACKET> when continuation is plausible. Read `references/final-summary-template.md` and `references/resume-packet-template.md`.
6. **Choose closure route**. Record <CLOSURE_DECISION> and preserve <FINALIZE_CONTINUITY_UPDATE> for stop, park-and-continue-later, publish-and-continue, archive, or route-back decisions. Read `references/resume-packet-template.md` and `references/checkpoint-memory-template.md`.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/closure-gate.md` for prevent premature finalization.
- `references/claim-ledger-template.md` for classify final claim status.
- `references/final-summary-template.md` for write the responsible end-state summary.
- `references/resume-packet-template.md` for leave a clean continuation path.
- `references/finalization-checklist.md` for closure checklist, package inventory, and anti-pattern gates.
- `references/checkpoint-memory-template.md` for pause-ready or continue-later checkpoint continuity notes.

## Cross-Step Quality Gates

Read these gates before claiming the skill output is ready for handoff. Use `Metrics` to judge directional quality across the workflow and `Checks` to decide whether the output must be revised, blocked, or rerouted.

### Metrics

- Closure blocker count: number of unresolved evidence, writing, review, proofing, submission, package, or route blockers that still prevent honest closure; lower is better.
- Claim-ledger coverage: fraction of important outcomes classified as supported, partially supported, unsupported, or deferred with evidence paths and caveats; higher is better.

### Checks

- Context check: <FINALIZE_CONTEXT_BRIEF> inventories accepted comparator state, runs, analysis, writing state, decisions, blockers, and package or paper manifests before closure judgment.
- Legitimacy check: <FINALIZE_BLOCKER_RECORD> or route-back decision exists whenever required evidence, writing, review, proofing, or submission gates fail.
- Claim check: <CLAIM_LEDGER> preserves important claims, caveats, evidence, and downgrade history instead of silently deleting weakened beliefs.
- Limitation check: <FINAL_LIMITATIONS_REPORT> records data, metric, implementation, resource, literature, reproducibility, and unsupported-claim limits.
- Recommendation check: <CLOSURE_DECISION> states stop, park-and-continue-later, publish-and-continue, archive, or route-back with the evidence and reopen condition.
- Resume check: <RESUME_PACKET> or <FINALIZE_CONTINUITY_UPDATE> tells a later agent what to read first, what not to repeat, and which route remains open.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later v2 skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or source harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
