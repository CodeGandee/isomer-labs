---
name: isomer-rsch-baseline-v2
description: Use when research work needs a trustworthy comparator, metric contract, accepted waiver, or blocker before hypotheses, experiments, analysis, or claims can proceed.
---

# Isomer Research Baseline V2

## Overview

Baseline secures one trustworthy comparator and comparison contract, then gets out of the way. It chooses the lightest route that can support downstream comparison, verifies evidence before acceptance, and closes the gate through confirmation, waiver, or blocker.

Placeholder definitions live in `migrate/placeholders.md`.

## When to Use

Use this skill when:

- No credible comparator exists.
- The active comparator is stale, unverified, or incomparable.
- A provided baseline package, local service, trusted output, or source repository must be attached, imported, or verified.
- A failed reproduction needs bounded repair before downstream work can compare fairly.

Do not use this skill when:

- A verified active comparator and metric contract already exist.
- The baseline gate was explicitly waived for this route.
- The real task is ideation, execution, or writing rather than comparator trust.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Choose the acceptance target**. Use <BASELINE_CONTEXT_BRIEF> to decide whether the target is comparison-ready, paper-repro-ready, registry-publishable, waived, or blocked.
2. **Select the lightest trustworthy route**. Record <COMPARATOR_ROUTE_RECORD> for attach, import, verify-local-existing, reproduce, repair, publish, waive, or block.
3. **Make comparability explicit**. Produce <COMPARABILITY_CONTRACT> for task, dataset, split, metric ids, metric directions, source identity, evaluation path, and deviations.
4. **Collect only necessary evidence**. Gather <BASELINE_VERIFICATION_EVIDENCE> sufficient for the selected acceptance target without widening into a reproduction diary.
5. **Close the baseline gate**. Record <ACCEPTED_BASELINE_RECORD>, <BASELINE_WAIVER_RECORD>, or <BASELINE_BLOCKER_RECORD> and return <BASELINE_ROUTE_DECISION>.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this skill, the referenced pages, and the user's request, then execute the plan.

## Reference Routing

Read these pages as needed:

- `references/route-selection.md` for choose the cheapest route that can make comparator trust real.
- `references/comparability-contract.md` for define the comparison basis that later work must not guess.
- `references/verification-record-template.md` for capture baseline evidence before acceptance.
- `references/operational-guidance.md` for keep comparator work bounded and evidence-first.

## Exit Criteria

This skill can end only when the relevant placeholders are explicit enough for the next route, a blocker is recorded, and later v2 skills do not need to guess what changed or why.

## Common Mistakes

- Do not continue after the route, gate, or blocker is already clear.
- Do not replace evidence requirements with optimistic prose.
- Do not bind source paths, filenames, or DeepScientist harness outputs as final Isomer storage contracts.
- Do not ask the user routine technical questions before checking durable local evidence.
- Do not hide blocked states behind vague progress language.
