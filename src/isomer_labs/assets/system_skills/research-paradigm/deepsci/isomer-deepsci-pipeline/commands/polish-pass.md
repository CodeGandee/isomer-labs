# polish-pass

Polish figures and prose before external review.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | figures | `isomer-deepsci-figure-polish` | `draft-section-set` | `polished-figures` | `ready == true` | blocker exists | no |
| 2 | nature_polish | `isomer-deepsci-nature-polishing` | `draft-section-set`, `polished-figures` | `nature-polished-draft` | `ready == true` | blocker exists | no |
| 3 | audit | `isomer-deepsci-review` | `nature-polished-draft` | `review-report` | `route_decision` in `[finalize, revise]` | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure `draft-section-set` is available from the caller context.
2. **Execute stages sequentially**. Invoke each stage skill with automatic artifact handoffs. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Produce the terminal report**. Write ``pipeline-terminal-report`` using `references/terminal-report-template.md`.

If the user's task does not map cleanly to this pass, route back to `isomer-deepsci-pipeline` main workflow or use your native planning tool.

## Notes

- Use this pass when the draft is structurally complete and the goal is final figure and prose quality.
- If the target venue is not Nature-family, replace or skip `isomer-deepsci-nature-polishing` under external control.
