# polish-pass

Polish figures and prose before external review.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | figures | `isomer-deepsci-figure-polish` | `DEEPSCI:DRAFT-SECTION-SET` | `DEEPSCI:FINAL-FIGURE-EXPORT` | `ready == true` | blocker exists | no |
| 2 | nature_polish | `isomer-deepsci-nature-polishing` | `DEEPSCI:DRAFT-SECTION-SET`, `DEEPSCI:FINAL-FIGURE-EXPORT` | `DEEPSCI:POLISHED-MANUSCRIPT-TEXT` | `ready == true` | blocker exists | no |
| 3 | audit | `isomer-deepsci-review` | `DEEPSCI:POLISHED-MANUSCRIPT-TEXT` | `DEEPSCI:REVIEW-REPORT` | `route_decision` in `[finalize, revise]` | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure `DEEPSCI:DRAFT-SECTION-SET` is available from the caller context. If a known writing route can produce or repair it, return `paused` prerequisite recovery with that route and the `figures` resume point; do not invoke the producer inside this recipe.
2. **Execute stages sequentially**. Invoke each stage skill with verified durable-record handoffs. After each stage, require queryable durable refs plus either a verified complete acceptance receipt or explicit `closeout: not_applicable`; treat plain paths and partial receipts as unavailable. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Prepare the terminal report**. Build ``DEEPSCI:PIPELINE-TERMINAL-REPORT`` using `references/terminal-report-template.md`, including stage receipts, accepted durable refs, and explicit `not_applicable` closeouts. Return it to the main pipeline workflow for end callbacks and pipeline-level Operation Set Closeout before any `status: complete` result.

If the user's task does not map cleanly to this pass, route back to `isomer-ext-deepsci-entrypoint` main workflow or use your native planning tool.

## Notes

- Use this pass when the draft is structurally complete and the goal is final figure and prose quality.
- If the target venue is not Nature-family, return a material route choice rather than changing the recipe silently. After the terminal report, an explicitly authorized target-scoped run-to controller may select a separate applicable polishing route.
