# Analysis Campaign Evidence Flow Examples

Use this reference when the evidence question is clear but the exact durable evidence sequence is not. The examples preserve the source flow while replacing source harness calls with native Isomer evidence records. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Choose the evidence flow**. Decide whether the answer is a read-only audit, one-slice analysis, multi-slice campaign, writing-facing slice, failed or infeasible slice, or blocker route.
2. **Create only useful lineage**. Use a campaign lineage route when branch or workspace isolation, Canvas visibility, reviewability, writing traceability, or later replay matters.
3. **Record launched slices immediately**. Every launched slice should become <ANALYSIS_SLICE_RECORD> before campaign-level interpretation.
4. **Preserve non-success flows**. Failed, infeasible, partial, and superseded slices should still leave records, blockers, and route implications.
5. **Avoid false campaign claims**. Existing-output audits can produce reports or decisions, but should not be described as launched campaign slices.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer a read-only audit when existing evidence answers the question (if no new slice is launched, otherwise record it as an audit).
- Prefer one-slice lineage when reviewability or write-back matters (if lineage adds no trust, otherwise keep the route lightweight).
- Prefer multi-slice campaigns only when several slices together answer one evidence question (if one slice is decisive, otherwise stop).
- Prefer recording failed or infeasible slices as evidence about feasibility (if replacement is needed, otherwise keep the blocker visible).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Planned slices must not count as evidence before they run or are audited.
- A real launched supplementary run must not be reported only in chat.
- Campaign summaries must not be written before slice records exist.
- A failed or infeasible slice must not be silently replaced by a different successful slice.
- A read-only audit must not pretend it created new slice evidence.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Launched-slice record coverage: fraction of launched slices that have <ANALYSIS_SLICE_RECORD> before campaign-level interpretation; higher is better.
- Flow-mismatch count: number of evidence flows whose selected route does not match existing, one-slice, multi-slice, writing-facing, failed, infeasible, or audit-only status; lower is better.

### Checks

- Flow gate: the selected flow matches whether evidence is existing, one-slice, multi-slice, writing-facing, failed, infeasible, or audit-only.
- Lineage gate: campaign lineage is used when it adds durable trust, not as automatic ceremony.
- Record gate: every launched slice has <ANALYSIS_SLICE_RECORD>.
- Non-success gate: failure, infeasibility, partial evidence, and blockers remain visible.
- Summary gate: <ANALYSIS_CAMPAIGN_SUMMARY> aggregates only recorded evidence.

## Examples

### One Launched Supplementary Slice

Use when one extra slice is enough but lineage or reviewability matters.

1. Resolve unclear runtime identifiers.
2. Create <ANALYSIS_CAMPAIGN_PLAN> with one slice when lineage matters.
3. Run the returned slice in the assigned workspace or record why a different surface is used.
4. Produce <ANALYSIS_SLICE_RECORD>.
5. Record <ANALYSIS_ROUTE_DECISION>.

### Multi-Slice Evidence Package

Use when several slices together answer one evidence question.

1. Define the justified slice frontier.
2. Create <ANALYSIS_CAMPAIGN_PLAN>.
3. Execute slices one by one.
4. Produce <ANALYSIS_SLICE_RECORD> after each launched slice.
5. Aggregate only after slice-level evidence exists.

### Writing-Facing Slice

Use when the slice directly supports a paper-like contract.

1. Recover selected outline, matrix, evidence ledger, section, claim, or reviewer target when relevant.
2. Create <ANALYSIS_WRITEBACK_MAP>.
3. Run the slice.
4. Produce <ANALYSIS_SLICE_RECORD>.
5. Update the write-back target or record the stale target as a blocker.

### Failed or Infeasible Slice

Use when the slice cannot complete honestly.

1. Stop or mark the slice when blocked.
2. Keep the real blocker visible.
3. Produce <ANALYSIS_SLICE_RECORD> with non-success status.
4. Route to redesign, decision, experiment, or stop.

### Read-Only Bounded Audit

Use when existing outputs, tables, logs, or records already answer the question.

1. Inspect the existing evidence.
2. Leave a durable report or decision.
3. Do not call it a launched campaign slice.
