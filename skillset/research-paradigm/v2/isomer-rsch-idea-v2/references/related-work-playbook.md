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

- Prefer broad, purpose-driven search over confirmation search (if the direct neighborhood is saturated, otherwise add adjacent-domain mechanism search).
- Prefer strongest nearby work over weak or convenient comparisons (if the baseline paper is not the strongest neighbor, otherwise explain the stronger neighbor).
- Prefer paper discovery before claim formation (if an existing survey is sufficient, otherwise record the reuse reason).

## Constraints

- The related-work pass must not rely on one query family.
- The related-work pass must not treat recency as relevance or a title match as evidence.
- The selected candidate must have an explicit closest-prior-work comparison.
- Cross-domain imports must explain why the mechanism translates into the current codebase and metric contract.

## Quality Gates

- Search breadth: direct, failure-mode, mechanism, and adjacent-domain neighborhoods were checked when relevant.
- Prior-work table: each serious candidate has comparable prior work with mechanism, task, dataset, metric, claim, and implication fields.
- Novelty verdict: each top candidate has one of `novel`, `incremental but valuable`, or `not sufficiently differentiated`.
- Stop condition: the strongest obvious overlaps are mapped and remaining uncertainty is recorded instead of hidden.
