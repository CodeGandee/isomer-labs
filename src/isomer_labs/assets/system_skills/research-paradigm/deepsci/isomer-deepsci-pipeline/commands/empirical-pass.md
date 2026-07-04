# empirical-pass

Run the full empirical research pass: frame the problem, establish a comparator, select a hypothesis, run one experiment, and interpret the result.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | frame | `isomer-deepsci-scout` | — | `research-frame` | `next_route` in `[baseline, idea]` | blocker exists | no |
| 2 | comparator | `isomer-deepsci-baseline` | `research-frame` | `comparator-contract` | `accepted == true` | blocker exists | no |
| 3 | ideate | `isomer-deepsci-idea` | `research-frame`, `comparator-contract` | `selected-hypothesis` | `ready_for_experiment == true` | `route != experiment` | no |
| 4 | run | `isomer-deepsci-experiment` | `selected-hypothesis`, `comparator-contract` | `experiment-result` | status in `[supported, refuted, inconclusive]` | `status == blocked` | yes |
| 5 | interpret | `isomer-deepsci-analysis` | `experiment-result`, `comparator-contract` | `analysis-finding` | `route_decision` exists | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure the caller provided any initial research frame or constraints needed by the first stage (`isomer-deepsci-scout`).
2. **Execute stages sequentially**. Invoke each stage skill with automatic artifact handoffs. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Produce the terminal report**. Write ``pipeline-terminal-report`` using `references/terminal-report-template.md`.

If the user's task does not map cleanly to this pass, route back to `isomer-deepsci-pipeline` main workflow or use your native planning tool.

## Notes

- This pass expects an unset or loosely framed research topic.
- The `run` stage is expensive; surface a checkpoint before launching it when the runtime supports cost gating.
- If the scout stage recommends a route other than `baseline`, pause and return the terminal report to the external controller.
