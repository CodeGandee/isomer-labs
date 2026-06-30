---
name: isomer-rsch-finalize-v2
description: Use when a Research Topic or Research Inquiry is ready to close, pause, archive, publish, or hand off with final claims, limitations, recommendations, and a clean resume path.
---

# Isomer Research Finalize V2

## Overview

Finalize closes or pauses work responsibly. It consolidates accepted evidence, records claim status and limitations, chooses stop, park, publish, or continue-later routing, and refuses closure when evidence or writing gates still block it.

Placeholder definitions live in `migrate/placeholders.md`.

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

1. **Gather closure context**. Build <FINALIZE_CONTEXT_BRIEF> from accepted comparator state, runs, analysis, writing state, decisions, blockers, and package or paper manifests.
2. **Check closure legitimacy**. If required evidence, writing, review, proofing, or submission gates fail, create <FINALIZE_BLOCKER_RECORD> or route to decision instead of forcing closure.
3. **Build the claim ledger**. Classify every important claim in <CLAIM_LEDGER> as supported, partially supported, unsupported, or deferred with evidence and caveats.
4. **State limitations and failures**. Create <FINAL_LIMITATIONS_REPORT> including data, metric, implementation, resource, literature, and unsupported-claim limits.
5. **Write final state**. Produce <FINAL_SUMMARY> and <RESUME_PACKET> when continuation is plausible.
6. **Choose closure route**. Record <CLOSURE_DECISION> and preserve <FINALIZE_CONTINUITY_UPDATE> for stop, park-and-continue-later, publish-and-continue, archive, or route-back decisions.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/closure-gate.md` for prevent premature finalization.
- `references/claim-ledger-template.md` for classify final claim status.
- `references/final-summary-template.md` for write the responsible end-state summary.
- `references/resume-packet-template.md` for leave a clean continuation path.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later v2 skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or DeepScientist harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
