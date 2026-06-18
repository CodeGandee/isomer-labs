# Related-Work Playbook

Use this reference for literature scouting, novelty checking, and value judgment. The goal is not to collect random citations; the goal is to decide whether a candidate still has novelty, research value, and a defensible evidence path.

## Search Objective

Answer these questions:

- What has already been tried?
- What is the strongest nearby prior work?
- What remains unresolved or weakly defended?
- Does the candidate still have novelty or at least research value?
- Are there adjacent-domain methods that solve a structurally similar limitation and could translate here?

## Query Families

- task plus dataset plus metric
- task plus failure mode or bottleneck
- comparator method plus limitation keyword
- proposed mechanism plus task
- proposed mechanism plus dataset
- adjacent-domain principle plus task
- strongest recent paper title or method plus extension, robustness, ablation, or failure

## Source Order and De-Dup Protocol

1. Check durable Findings, paper notes, idea notes, Decision Records, and knowledge cards from the current Research Task.
2. Reuse validated cross-task knowledge only when the current Operator Agent policy permits it.
3. Search externally for missing neighborhoods through Literature Provider Binding refs, citation trails, open-web or repository search, and adjacent-domain mechanism search.
4. Record context-only provider results first as provider-output Artifacts, then record what was already known, what is new this pass, and what remains unresolved as Findings or Evidence Items according to evidence-use intent.

## Coverage Targets

Try to cover seminal papers, strongest recent direct competitors, nearest mechanism-level neighbors, papers focused on the same failure mode, papers with the same task but different mechanism families, and adjacent-domain papers whose mechanism or analysis logic can plausibly transfer.

For a normal selected-idea decision, durably cover at least five and usually five to ten related and usable papers. If the direct neighborhood truly contains fewer usable papers, record that shortage and fill the rest with the closest adjacent and translatable work.

## Novelty Triage

Ask in order:

1. Did prior work already use essentially the same mechanism for the same task?
2. If yes, is the claim still different because of boundary condition, evidence package, or failure-mode resolution?
3. If not, is the direction still only an obvious combination of known ingredients?
4. If the idea is incremental, is the increment important enough to justify experiments?

Use one of these verdicts: `novel`, `incremental but valuable`, or `not sufficiently differentiated`.

## Research-Value Checks

Even with limited novelty, a direction may be worth doing when it offers stronger evidence on a disputed claim, valuable transfer to a new setting, resolution of a known failure mode, a negative result that closes a tempting weak path, or reusable methodology.

## Exit Condition

The related-work search is good enough to stop when the strongest obvious nearby papers are mapped, at least one adjacent or cross-domain translation pass is complete when relevant, closest-prior-work comparison is complete enough to compare seriously, each top candidate has a verdict, and remaining uncertainty is recorded.
