# Resume Packet Template

Use this when the Research Topic is pausing rather than ending permanently. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **State current state**. Record objective, current stage, final recommendation at pause time, and closure route.
2. **Preserve node history**. Name current active node, predecessor nodes, superseded nodes or closure paths, and why the current node is authoritative.
3. **Name accepted baseline and strongest evidence**. Record comparator status, reproducibility or comparability state, top results, evidence pointers, and caveats.
4. **List open blockers**. State each blocker, why it matters, and which stage should resolve it.
5. **Choose next action**. Name the single best next step, why it dominates alternatives, and what to read first.
6. **Add do-not-repeat notes**. Preserve failed branches, misleading metrics, comparability traps, environment hazards, and closure paths not worth retrying unchanged.
7. **Define reopen conditions**. State exact conditions that justify reopening or switching away from the checkpoint.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer a short high-signal resume packet over a long final report duplicate.
- Prefer one best next action over a list of vague possibilities.
- Prefer explicit do-not-repeat notes when old routes are tempting but stale.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- <RESUME_PACKET> must identify current state, node history, accepted baseline, strongest evidence, blockers, next action, first-read material, do-not-repeat notes, and reopen conditions.
- The packet must not leave future agents guessing which route or node is authoritative.
- A pause-ready route must not rely only on memory; it should point to durable summary, status, report, manifest, decision, or handoff records.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Resume-field coverage: fraction of current state, accepted baseline, strongest evidence, open blockers, next action, do-not-repeat notes, first-read files, and reopen condition fields completed; higher is better.
- Open-blocker count: number of unresolved blockers left without owner, evidence need, or route implication; lower is better.

### Checks

- Restart clarity: a future turn can resume from the packet without reconstructing the whole history.
- Evidence clarity: strongest evidence and caveats are named.
- Blocker clarity: open blockers have owning stages or routes.
- Reopen clarity: old routes reopen only under stated conditions.
