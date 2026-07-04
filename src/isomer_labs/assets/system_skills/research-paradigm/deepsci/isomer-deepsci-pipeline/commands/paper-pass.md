# paper-pass

Turn analysis findings into a reviewed paper bundle.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | outline | `isomer-deepsci-paper-outline` | `analysis-finding` | `paper-outline` | `ready_for_write == true` | blocker exists | no |
| 2 | draft | `isomer-deepsci-write` | `paper-outline`, `analysis-finding` | `draft-section-set` | manuscript validation passes | blocker exists | no |
| 3 | audit | `isomer-deepsci-review` | `draft-section-set` | `review-report` | `route_decision` in `[finalize, revise]` | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure `analysis-finding` is available from the caller context.
2. **Execute stages sequentially**. Invoke each stage skill with automatic artifact handoffs. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Produce the terminal report**. Write ``pipeline-terminal-report`` using `references/terminal-report-template.md`.

If the user's task does not map cleanly to this pass, route back to `isomer-deepsci-pipeline` main workflow or use your native planning tool.

## Notes

- Use this pass when empirical results exist and the next step is a manuscript.
- If the review stage recommends major revisions or new experiments, the terminal report should route to `revision-pass` or `empirical-pass` under external control.
