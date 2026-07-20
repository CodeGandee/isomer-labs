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

1. **Check entry context**. Ensure `DEEPSCI:DRAFT-SECTION-SET` is available from the caller context. If a known writing route can produce or repair it, return `paused` prerequisite recovery with that route and the `audit` resume point; do not invoke the producer inside this recipe.
2. **Execute stages sequentially**. Invoke each stage skill with verified durable-record handoffs. After each stage, require queryable durable refs plus either a verified complete acceptance receipt or explicit `closeout: not_applicable`; treat plain paths and partial receipts as unavailable. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
4. **Prepare the terminal report**. Build ``DEEPSCI:PIPELINE-TERMINAL-REPORT`` using `references/terminal-report-template.md`, including stage receipts, accepted durable refs, and explicit `not_applicable` closeouts. Return it to the main pipeline workflow for end callbacks and pipeline-level Operation Set Closeout before any `status: complete` result.

If the user's task does not map cleanly to this pass, route back to `isomer-ext-deepsci-entrypoint` main workflow or use your native planning tool.

## Notes

- Use this pass for pre-submission self-review and revision cycles.
- If review finds no revision needs, the terminal report should say so and recommend finalization. Only an explicitly authorized target-scoped run-to controller may consume the recommendation after recording this pass report; it stops after the original target.
