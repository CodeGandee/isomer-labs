# Research History Playbook

Use this reference when idea work needs broad, history-aware literature search rather than a shallow scan of recent papers. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Build a field map**. Identify the main problem, major subproblems, representative paradigms, common datasets and metrics, disputes, and recurring failure modes.
2. **Find paper roles**. Identify seminal or foundational papers, turning-point papers, and current mainstream or strongest papers.
3. **Use citation chaining**. Follow backward and forward citation trails to reconstruct how assumptions changed or survived.
4. **Keep a lineage table**. Track problem, assumption or mechanism, method and data, conclusion, explicit limitation, and implicit limitation for the strongest papers.
5. **Search by ladder**. Move from direct neighborhood to failure-mode neighborhood, mechanism neighborhood, and cross-domain neighborhood.
6. **Choose review intent**. Use narrative review for viewpoint formation, scoping review for boundary mapping, and targeted comparison for narrowed candidate selection.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer lineage views over isolated paper titles (if the field is broad, otherwise still identify the paper roles).
- Prefer citation chaining when novelty or history is unclear (if the route is narrow and well-covered, otherwise record why chaining can be abbreviated).
- Prefer mapping assumptions over only summarizing methods (if an assumption was never tested, otherwise mark it as a possible opportunity).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- The history pass must not confuse recent fashion with structural importance.
- The history pass must identify the field's mainline, strongest assumptions, and unresolved breakpoints before supporting novelty claims.
- The history pass should not deep-read one narrow cluster before mapping the wider landscape.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Field-map coverage: number of strong reviews or tutorials, recent representative papers, and seminal or foundational papers covered relative to the source targets of 3, about 10, and about 5; higher is better until those targets are satisfied.
- Lineage-table coverage: number of strongest active-neighborhood papers tracked with paradigm, assumption, dataset, metric, limitation, and inheritance notes; higher is better until the 20-40 paper source range is covered.

### Checks

- Field map: the major subproblems, paradigms, datasets, metrics, and failure modes are visible.
- Paper roles: foundational, turning-point, and current strongest papers are named or their absence is justified.
- Lineage clarity: the pass shows which assumptions survived, changed, or were never tested.
- Breakpoint clarity: the current candidate still matters despite the strongest nearby work.
