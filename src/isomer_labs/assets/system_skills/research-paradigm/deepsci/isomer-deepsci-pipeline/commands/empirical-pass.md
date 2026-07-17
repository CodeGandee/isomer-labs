# empirical-pass

Run the full empirical research pass: frame the problem, establish a comparator, select a hypothesis, run one experiment, and interpret the result.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | frame | `isomer-deepsci-scout` | — | `DEEPSCI:RESEARCH-FRAME` | `next_route` in `[baseline, idea]` | blocker exists | no |
| 2 | comparator | `isomer-deepsci-baseline` | `DEEPSCI:RESEARCH-FRAME` | `DEEPSCI:COMPARATOR-CONTRACT` | `accepted == true` | blocker exists | no |
| 3 | ideate | `isomer-deepsci-idea` | `DEEPSCI:RESEARCH-FRAME`, `DEEPSCI:COMPARATOR-CONTRACT` | `DEEPSCI:SELECTED-HYPOTHESIS` | `ready_for_experiment == true` | `route != experiment` | no |
| 4 | run | `isomer-deepsci-experiment` | `DEEPSCI:SELECTED-HYPOTHESIS`, `DEEPSCI:COMPARATOR-CONTRACT` | `DEEPSCI:EXPERIMENT-RESULT` | status in `[supported, refuted, inconclusive]` | `status == blocked` | yes |
| 5 | interpret | `isomer-deepsci-analysis` | `DEEPSCI:EXPERIMENT-RESULT`, `DEEPSCI:COMPARATOR-CONTRACT` | `DEEPSCI:ANALYSIS-FINDING` | `route_decision` exists | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure the caller provided any initial research constraints needed by the first stage (`isomer-deepsci-scout`). If a material framing choice is unresolved, return `paused` with the choice and frame resume point rather than guessing.
2. **Execute stages sequentially**. Invoke each stage skill with verified durable-record handoffs. After each stage, require queryable durable refs plus either a verified complete acceptance receipt or explicit `closeout: not_applicable`; treat plain paths and partial receipts as unavailable. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Prepare the terminal report**. Build ``DEEPSCI:PIPELINE-TERMINAL-REPORT`` using `references/terminal-report-template.md`, including stage receipts, accepted durable refs, and explicit `not_applicable` closeouts. Return it to the main pipeline workflow for end callbacks and pipeline-level Operation Set Closeout before any `status: complete` result.

If the user's task does not map cleanly to this pass, route back to `isomer-deepsci-pipeline` main workflow or use your native planning tool.

## Notes

- This pass expects an unset or loosely framed research topic.
- The `run` stage is expensive; surface a checkpoint before launching it when the runtime supports cost gating.
- If the scout stage recommends a route other than `baseline`, pause and return the terminal report. An explicitly authorized target-scoped run-to controller may consume that route as a separate focused-skill or pass invocation after refreshing current state; this recipe does not add a backward edge.
