# paper-pass

Turn analysis findings into a reviewed paper bundle.

## Recipe

| Order | Stage | Skill | Consumes | Produces | Continue if | Pause if | Expensive |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | outline | `isomer-deepsci-paper-outline` | `DEEPSCI:ANALYSIS-FINDING` | `DEEPSCI:PAPER-OUTLINE` | `ready_for_write == true` | blocker exists | no |
| 2 | draft | `isomer-deepsci-write` | `DEEPSCI:PAPER-OUTLINE`, `DEEPSCI:ANALYSIS-FINDING` | `DEEPSCI:DRAFT-SECTION-SET` | manuscript validation passes | blocker exists | no |
| 3 | audit | `isomer-deepsci-review` | `DEEPSCI:DRAFT-SECTION-SET` | `DEEPSCI:REVIEW-REPORT` | `route_decision` in `[finalize, revise]` | blocker exists | no |

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Check entry context**. Ensure `DEEPSCI:ANALYSIS-FINDING` is available from the caller context. If a known analysis or experiment route can produce or repair it, return `paused` prerequisite recovery with that route and the `outline` resume point; do not invoke the producer inside this recipe.
2. **Execute stages sequentially**. Invoke each stage skill with verified durable-record handoffs. After each stage, require queryable durable refs plus either a verified complete acceptance receipt or explicit `closeout: not_applicable`; treat plain paths and partial receipts as unavailable. Use the **Recipe** table above for stage order, inputs, outputs, and transition conditions.
3. **Enforce paper compile preference**. When the pass reaches paper writing, validation, review, or bundle readiness for a LaTeX/TeX manuscript, the wrapped skills must try Tectonic first or record why Tectonic is unavailable, blocked by the template, or disallowed by the venue before using TeX Live, `latexmk`, `pdflatex`, `xelatex`, `lualatex`, BibTeX, or Biber.
4. **Apply transition rules**. After each stage, use `references/transition-rules.md` to decide continue, pause, or block.
5. **Prepare the terminal report**. Build ``DEEPSCI:PIPELINE-TERMINAL-REPORT`` using `references/terminal-report-template.md`, including stage receipts, accepted durable refs, and explicit `not_applicable` closeouts. Return it to the main pipeline workflow for end callbacks and pipeline-level Operation Set Closeout before any `status: complete` result.

If the user's task does not map cleanly to this pass, route back to `isomer-deepsci-pipeline` main workflow or use your native planning tool.

## Notes

- Use this pass when empirical results exist and the next step is a manuscript.
- For paper writing, prefer Tectonic first; use LaTeX engine workflows only as a recorded fallback after a Tectonic attempt or a concrete Tectonic blocker.
- If the review stage recommends major revisions or new experiments, the terminal report should route to `revision-pass` or `empirical-pass`. Only an explicitly authorized target-scoped run-to controller may consume that route as a separate pass Run; the paper recipe remains complete and linear.
