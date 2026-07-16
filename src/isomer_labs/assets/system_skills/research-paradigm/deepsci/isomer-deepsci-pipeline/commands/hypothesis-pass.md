# hypothesis-pass

Run a selected hypothesis through experiment and analysis.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | ideate | `isomer-deepsci-idea` | `DEEPSCI:RESEARCH-FRAME`, `DEEPSCI:COMPARATOR-CONTRACT` | `DEEPSCI:SELECTED-HYPOTHESIS` | `ready_for_experiment == true` | `route != experiment` | no |
| 2 | run | `isomer-deepsci-experiment` | `DEEPSCI:SELECTED-HYPOTHESIS`, `DEEPSCI:COMPARATOR-CONTRACT` | `DEEPSCI:EXPERIMENT-RESULT` | status in `[supported, refuted, inconclusive]` | `status == blocked` | yes |
| 3 | interpret | `isomer-deepsci-analysis` | `DEEPSCI:EXPERIMENT-RESULT`, `DEEPSCI:COMPARATOR-CONTRACT` | `DEEPSCI:ANALYSIS-FINDING` | `route_decision` exists | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure `DEEPSCI:RESEARCH-FRAME` and `DEEPSCI:COMPARATOR-CONTRACT` are available from the caller context. If a known focused skill can produce or repair either input, return `paused` prerequisite recovery with its producer route and the `ideate` resume point; do not invoke the producer inside this recipe.
2. **Execute stages sequentially**. Invoke each stage skill with automatic artifact handoffs. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Produce the terminal report**. Write ``DEEPSCI:PIPELINE-TERMINAL-REPORT`` using `references/terminal-report-template.md`.

If the user's task does not map cleanly to this pass, route back to `isomer-deepsci-pipeline` main workflow or use your native planning tool.

## Notes

- Use this pass when a research frame and comparator already exist but the hypothesis is not yet selected or verified.
- The `run` stage is expensive; surface a checkpoint before launching it when the runtime supports cost gating.
