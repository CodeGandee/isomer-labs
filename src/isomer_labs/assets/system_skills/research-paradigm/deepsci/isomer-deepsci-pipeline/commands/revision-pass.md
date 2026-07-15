# revision-pass

Self-review a draft, run needed analysis, and revise.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | audit | `isomer-deepsci-review` | `DEEPSCI:DRAFT-SECTION-SET` | `DEEPSCI:REVIEW-REPORT` | `route_decision == revise` | `route_decision != revise` | no |
| 2 | fill_gaps | `isomer-deepsci-analysis` | `DEEPSCI:REVIEW-REPORT`, `DEEPSCI:DRAFT-SECTION-SET` | `DEEPSCI:ANALYSIS-FINDING` | `route_decision` in `[write, finalize]` | blocker exists | no |
| 3 | revise | `isomer-deepsci-write` | `DEEPSCI:ANALYSIS-FINDING`, `DEEPSCI:DRAFT-SECTION-SET` | `DEEPSCI:DRAFT-SECTION-SET` | manuscript validation passes | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure `DEEPSCI:DRAFT-SECTION-SET` is available from the caller context.
2. **Execute stages sequentially**. Invoke each stage skill with automatic artifact handoffs. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Produce the terminal report**. Write ``DEEPSCI:PIPELINE-TERMINAL-REPORT`` using `references/terminal-report-template.md`.

If the user's task does not map cleanly to this pass, route back to `isomer-deepsci-pipeline` main workflow or use your native planning tool.

## Notes

- Use this pass for pre-submission self-review and revision cycles.
- If review finds no revision needs, the terminal report should say so and recommend finalization.
