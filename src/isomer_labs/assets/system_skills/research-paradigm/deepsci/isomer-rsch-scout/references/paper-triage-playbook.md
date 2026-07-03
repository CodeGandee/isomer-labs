# Paper Triage Playbook

Use this reference when scout must map a paper, repository, benchmark, or provenance neighborhood before routing. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Set the triage question**. Name the route-changing uncertainty from `<SCOUT_MINIMUM_UNKNOWNS>`.
2. **Reuse local evidence**. Check `<SCOUT_CONTEXT_BRIEF>` and `<SCOUT_MEMORY_REUSE_NOTE>` before external discovery.
3. **Search the smallest useful neighborhood**. Build `<SCOUT_DISCOVERY_LEDGER>` around direct, mechanism, and bottleneck neighbors.
4. **Retain only route-changing references**. Keep papers, repositories, and benchmark docs that affect task framing, `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, or `<NEXT_ROUTE_DECISION>`.
5. **Inspect repository provenance when needed**. Check official linkage, evaluation path, dependency realism, maintenance signal, license or access blockers, and reproducibility risk.
6. **Stop on routing clarity**. Convert retained evidence into `<LITERATURE_SCOUTING_REPORT>`, `<EVALUATION_CONTRACT>`, `<BASELINE_SHORTLIST>`, or `<SCOUT_BLOCKER_RECORD>`.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer primary papers, official benchmark docs, and official repositories over secondary summaries (if official sources are missing, otherwise mark provenance risk).
- Prefer the smallest useful neighborhood over broad survey expansion (if metric, split, or comparator ambiguity remains, otherwise continue only that branch).
- Prefer disconfirming evidence as well as supportive evidence.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- Scout must not retain references that do not change task framing, evaluation contract, comparator routing, or blocker status.
- Repository triage must not ignore official linkage, evaluation path, dependency realism, maintenance signal, license, data, model weights, or benchmark access when those affect route viability.
- Discovery must stop when retained references are enough to rank comparator routes, settle metric and split ambiguity, or record a blocker.
- Scout must not use discovery to justify a route that local durable evidence already contradicts.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Route-changing retention rate: fraction of retained papers, repositories, or benchmark documents that change task framing, evaluation contract, comparator routing, or blocker status; higher is better.
- Remaining triage unknown count: number of route-changing uncertainties still open after retained references are mapped to the handoff placeholders; lower is better.

### Checks

- Triage focus: each search or inspection is tied to a route-changing unknown.
- Retention quality: retained references say why they matter and which placeholder they inform.
- Repository viability: candidate repositories are triaged for provenance, evaluation mapping, runtime realism, and access blockers.
- Stop condition: `<SCOUT_DISCOVERY_LEDGER>` shows why further search is or is not needed.
