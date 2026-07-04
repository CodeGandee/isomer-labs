# rebuttal-pass

Turn formal reviewer feedback into revised text and new evidence.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | normalize | `isomer-deepsci-rebuttal` | `review-package` | `rebuttal-action-plan` | `route_decision` in `[analysis, experiment, write]` | blocker exists | no |
| 2 | fill_gaps | `isomer-deepsci-analysis` | `rebuttal-action-plan`, `draft-section-set` | `analysis-finding` | `route_decision` in `[experiment, write]` | blocker exists | no |
| 3 | run | `isomer-deepsci-experiment` | `analysis-finding`, `comparator-contract` | `experiment-result` | status in `[supported, refuted, inconclusive]` | `status == blocked` | yes |
| 4 | revise | `isomer-deepsci-write` | `experiment-result`, `analysis-finding`, `draft-section-set` | `revised-draft` | manuscript validation passes | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure `review-package` and `draft-section-set` are available from the caller context. `comparator-contract` is required if the action plan routes through the `run` stage.
2. **Execute stages sequentially**. Invoke each stage skill with automatic artifact handoffs. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Produce the terminal report**. Write ``pipeline-terminal-report`` using `references/terminal-report-template.md`.

If the user's task does not map cleanly to this pass, route back to `isomer-deepsci-pipeline` main workflow or use your native planning tool.

## Notes

- Use this pass after formal reviews arrive.
- The `run` stage is expensive; surface a checkpoint before launching it when the runtime supports cost gating.
- If a reviewer concern needs no new evidence, the rebuttal stage may route directly to writing.
