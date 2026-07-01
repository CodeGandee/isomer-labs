# Candidate Board Template

Use this reference to keep the compact candidate ledger current when the frontier changes. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **List candidate identity**. Record candidate id, level, parent, strategy, status, expected gain, observed result, and promote/archive recommendation.
2. **Separate levels**. Use `brief` for branchless method proposals and `implementation` for within-line attempts.
3. **Keep parent lineage visible**. Parent may be a branch, idea id, run id, candidate id, durable line, or frontier record.
4. **Use route strategy labels**. Prefer explore, exploit, fusion, debug, or stop as the candidate strategy.
5. **Update after each meaningful pass**. Keep <CANDIDATE_BOARD> synchronized with <OPTIMIZATION_FRONTIER> and <OPTIMIZE_CHECKLIST>.

## Preferences

- Prefer a small board with actionable status over a long stale list (if old candidates matter, otherwise archive or hold them explicitly).
- Prefer clear promote/archive recommendations over empty placeholders (if uncertain, otherwise name the evidence needed).
- Prefer one current active candidate pool over several half-started directions (if several are live, otherwise state isolation and reason).

## Constraints

- <CANDIDATE_BOARD> must not merge candidate briefs with implementation attempts.
- Candidate status must not imply promotion before ranking or route decision exists.
- Observed results must not replace expected gain unless evidence exists.
- Board updates should not create new candidates without frontier recovery.

## Quality Gates

### Metrics

- Candidate-row coverage: fraction of candidate rows with id, type, parent, strategy, status, headline, evidence, and next action completed; higher is better.
- Pending-next-action count: number of candidate rows whose next action remains unclear after frontier review; lower is better.

### Checks

- Identity gate: candidate id, level, parent, and strategy are present.
- Status gate: proposed, smoke, promoted, failed, archived, held, or stopped status is explicit.
- Evidence gate: observed result is evidence-backed or marked unavailable.
- Recommendation gate: promote, hold, fuse, debug, archive, or stop recommendation is present.

## Template

| Candidate ID | Level | Parent | Strategy | Status | Expected Gain | Observed Result | Promote / Archive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cand-001 | brief | current-frontier | explore | proposed | | n/a | pending |
| cand-002 | implementation | cand-001 | exploit | smoke_passed | | | consider promote |
