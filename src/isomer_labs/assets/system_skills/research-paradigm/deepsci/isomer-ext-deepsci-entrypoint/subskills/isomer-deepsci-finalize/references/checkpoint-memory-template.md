# Checkpoint Memory Template

Use this when the Research Topic is pausing, entering continue-later, or otherwise needs one compact memory card that says exactly where later turns should resume. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **State current route**. Record current route label, stage or anchor, and short closure or continue-later judgment.
2. **Name current active node**. Identify active paper line, run node, report-decision pair, or checkpoint, and why it is authoritative now.
3. **Preserve node history**. Record predecessor nodes, superseded completion, experiment, or writing paths, and why the current checkpoint replaced them.
4. **Name retained result or blocker**. State the strongest still-valid result or dominant blocker and why it matters.
5. **Mark do-not-reopen items**. List experiments, branches, or closure paths that should stay closed unless new evidence appears.
6. **Name next resume step and first reads**. Record the single best next step and the files, manifests, reports, or decisions to read first.
7. **Define reopen condition**. State the exact condition that would justify reopening an older node or switching away from this checkpoint.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer one compact checkpoint memory card when continuation remains plausible (if true completion is approved and no continuation path remains, otherwise omit it).
- Prefer checkpoint memory that mirrors DEEPSCI:RESUME-PACKET rather than inventing a second state story.
- Prefer first-read files that quickly rehydrate the current node.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:FINALIZE-CONTINUITY-UPDATE must be created when pause-ready or continue-later state would otherwise be easy to misresume.
- Checkpoint memory must not replace durable files, reports, or artifacts; it summarizes the resume path.
- Reopen conditions must be exact enough to prevent accidental reopening.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Checkpoint-field coverage: fraction of current route, active node, node history, strongest retained result or blocker, do-not-reopen list, next resume step, first-read files, and reopen condition fields completed; higher is better.
- Repeat-risk count: number of branches, closure paths, experiments, or blocker checks left without do-not-repeat or reopen guidance; lower is better.

### Checks

- Resume fidelity: the card points to the same authoritative state as DEEPSCI:RESUME-PACKET.
- History fidelity: superseded paths and do-not-reopen items are explicit.
- Restart usability: the first-read files and next step are concrete.
- Reopen control: old nodes reopen only under stated evidence or decision conditions.
