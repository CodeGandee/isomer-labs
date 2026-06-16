# Intake-audit methodology (ported from DeepScientist `intake-audit`)

For quests that do NOT start from a blank state: audit, trust-rank, and reconcile pre-existing assets
(baselines, results, drafts, review materials) before choosing the next anchor. Record findings via Houmao
records (`intake_asset.record`, `decision.record`) — the DB stays canonical; this is methodology only.

## Four intake questions
1. What exists? 2. What is trustworthy? 3. What is directly reusable? 4. Which stage takes over next?

## Trust ranking (maps onto Houmao `intake_asset.trust`)
DeepScientist 5-value vocabulary → Houmao's schema-enforced 4-value enum: `trusted` · `usable_with_verification`→`suspect` · `reference_only`/`stale_or_conflicting`→`untrusted` · `missing_context`/reject→`rejected`. Adopt (`adopt_as`) ONLY a `trusted` asset (invariant `intake_adopt_trusted`).

## Manuscript-visibility ranking (for paper-facing assets)
`main_text_candidate` · `appendix_or_reproducibility` · `comparator_or_negative_evidence` · `reference_only` · `internal_only`.

## State buckets
`baseline_ready` · `baseline_partial` · `main_result_ready` · `analysis_ready` · `draft_ready` · `paper_bundle_ready` · `review_package_ready` · `unclear_state`.

## Adoption / reconciliation rules
- Existing baseline → adopt then confirm the gate ONLY when trust justifies it; existing main result → record ONLY if it is genuinely the accepted main run; existing analysis → record per finished slice.
- **Legacy-method separation:** before adopting any pre-existing paper/draft asset as *current-method support*, separate its role (legacy / comparator / negative-evidence / appendix / current). Do not import an old draft as current support.
- **Provenance ≠ manuscript content:** never treat requests, branch names, or command logs as paper content. If the task is really a review of an existing package, route to `rebuttal`.
- If evidence is insufficient, RECORD the insufficiency — do not invent cleaned-up history.

## Current-board packet (report to the Orchestrator)
`current_mainline` · `incumbent` · `latest_decisive_result` · `active_blocker` · `stale_routes_to_ignore` · `next_decision_scope` · `budget_class`. Then recommend the next anchor; the Orchestrator records the `decision`.

See `state-audit-template.md` for the asset-matrix layout (area × current-asset × trust × why × missing-proof × recommended-action).
