# Related-Work Playbook

Use this reference during idea work when literature scouting, novelty checking, and value judgment need an explicit process. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Set the search objective**. State what must be learned about prior attempts, strongest nearby work, unresolved edges, and adjacent mechanisms.
2. **Check durable records first**. Inspect relevant Workspace Runtime paper, idea, decision, and knowledge records before opening new external search.
3. **Issue query families**. Search across task, dataset, metric, baseline, limitation, proposed mechanism, adjacent principle, and strongest known paper names.
4. **Run history and cross-domain passes**. Use direct, failure-mode, mechanism, and adjacent-domain neighborhoods instead of one narrow keyword cluster.
5. **Read papers in layers**. Start with abstract, introduction, conclusion, figures, claims, method, experiments, ablations, limitations, and failure cases, deep-reading only papers that affect the verdict.
6. **Build comparison tables**. Record task, dataset, metric, mechanism, claim, evidence strength, weakness, and implication for each serious candidate.
7. **Triage novelty and value**. Decide whether the route is novel, incremental but valuable, or not sufficiently differentiated.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer broad, purpose-driven search over confirmation search (if the direct neighborhood is saturated, otherwise add adjacent-domain mechanism search).
- Prefer strongest nearby work over weak or convenient comparisons (if the baseline paper is not the strongest neighbor, otherwise explain the stronger neighbor).
- Prefer paper discovery before claim formation (if an existing survey is sufficient, otherwise record the reuse reason).

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- The related-work pass must not rely on one query family.
- The related-work pass must not treat recency as relevance or a title match as evidence.
- The selected candidate must have an explicit closest-prior-work comparison.
- Cross-domain imports must explain why the mechanism translates into the current codebase and metric contract.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Coverage-bucket count: number of relevant coverage buckets represented before final selection, including direct task overlap, failure-mode work, baseline limitations, adjacent mechanisms, and closest extensions; higher is better.
- Cross-domain pass count: number of deliberate cross-domain mechanism passes when the bottleneck may transfer; higher is better until at least one credible pass is complete.

### Checks

- Search breadth: direct, failure-mode, mechanism, and adjacent-domain neighborhoods were checked when relevant.
- Prior-work table: each serious candidate has comparable prior work with mechanism, task, dataset, metric, claim, and implication fields.
- Novelty verdict: each top candidate has one of `novel`, `incremental but valuable`, or `not sufficiently differentiated`.
- Stop condition: the strongest obvious overlaps are mapped and remaining uncertainty is recorded instead of hidden.
