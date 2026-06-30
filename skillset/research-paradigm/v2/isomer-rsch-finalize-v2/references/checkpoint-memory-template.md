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

- Prefer one compact checkpoint memory card when continuation remains plausible (if true completion is approved and no continuation path remains, otherwise omit it).
- Prefer checkpoint memory that mirrors <RESUME_PACKET> rather than inventing a second state story.
- Prefer first-read files that quickly rehydrate the current node.

## Constraints

- <FINALIZE_CONTINUITY_UPDATE> must be created when pause-ready or continue-later state would otherwise be easy to misresume.
- Checkpoint memory must not replace durable files, reports, or artifacts; it summarizes the resume path.
- Reopen conditions must be exact enough to prevent accidental reopening.

## Quality Gates

- Resume fidelity: the card points to the same authoritative state as <RESUME_PACKET>.
- History fidelity: superseded paths and do-not-reopen items are explicit.
- Restart usability: the first-read files and next step are concrete.
- Reopen control: old nodes reopen only under stated evidence or decision conditions.
