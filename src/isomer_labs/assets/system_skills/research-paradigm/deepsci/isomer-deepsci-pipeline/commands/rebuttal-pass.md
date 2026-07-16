# rebuttal-pass

Turn formal reviewer feedback into revised text and new evidence.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | normalize | `isomer-deepsci-rebuttal` | `DEEPSCI:REVIEW-REPORT` | `DEEPSCI:REVIEW-PACKAGE-NORMALIZATION`, `DEEPSCI:REBUTTAL-ACTION-PLAN` | `route_decision` in `[analysis, experiment, write]` | blocker exists | no |
| 2 | fill_gaps | `isomer-deepsci-analysis` | `DEEPSCI:REBUTTAL-ACTION-PLAN`, `DEEPSCI:DRAFT-SECTION-SET` | `DEEPSCI:ANALYSIS-FINDING` | `route_decision` in `[experiment, write]` | blocker exists | no |
| 3 | run | `isomer-deepsci-experiment` | `DEEPSCI:ANALYSIS-FINDING`, `DEEPSCI:COMPARATOR-CONTRACT` | `DEEPSCI:EXPERIMENT-RESULT` | status in `[supported, refuted, inconclusive]` | `status == blocked` | yes |
| 4 | revise | `isomer-deepsci-write` | `DEEPSCI:EXPERIMENT-RESULT`, `DEEPSCI:ANALYSIS-FINDING`, `DEEPSCI:DRAFT-SECTION-SET` | `DEEPSCI:DRAFT-SECTION-SET` | manuscript validation passes | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure `DEEPSCI:REVIEW-REPORT` and `DEEPSCI:DRAFT-SECTION-SET` are available from the caller context. `DEEPSCI:COMPARATOR-CONTRACT` is required if the action plan routes through the `run` stage. For any missing input with a known producer, return `paused` prerequisite recovery with that route and the `normalize` resume point; do not invoke it inside this recipe.
2. **Execute stages sequentially**. Invoke each stage skill with automatic artifact handoffs. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Produce the terminal report**. Write ``DEEPSCI:PIPELINE-TERMINAL-REPORT`` using `references/terminal-report-template.md`.

If the user's task does not map cleanly to this pass, route back to `isomer-deepsci-pipeline` main workflow or use your native planning tool.

## Notes

- Use this pass after formal reviews arrive.
- The `run` stage is expensive; surface a checkpoint before launching it when the runtime supports cost gating.
- If a reviewer concern needs no new evidence, the rebuttal stage may route directly to writing.
- Any recommended work outside the remaining linear stages ends this pass. An explicitly authorized target-scoped run-to controller may consume it later as a separate focused-skill or pass Run.
