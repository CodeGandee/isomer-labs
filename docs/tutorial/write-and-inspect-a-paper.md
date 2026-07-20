# Write and Inspect a Paper

This tutorial shows how to prompt the agent to turn research records into a readable paper and then repair the rendered artifact. The task is not "generate a PDF"; it is to make the paper explain the claim, evidence, figures, tables, and proof placement clearly.

## Starting Point

You have model records, experiment evidence, and a research claim. In the running example, the user repeatedly inspected the rendered PDF, asked for layout fixes, changed the paper template, improved notation, and promoted important evidence from appendix to main text.

## Task

Ask the agent to write or revise the paper from accepted evidence, then inspect the rendered output. The main entrypoint is often a manual `isomer-ext-deepsci-entrypoint` skill invocation, followed by ordinary prompts that correct the paper as you inspect it.

## Example Interaction

User Action:

> $isomer-ext-deepsci-entrypoint use paper-pass to finalize and write the paper from accepted evidence

AI:

> Ran paper, revision, and submission passes.
>
> Reported review blockers, fixed evidence gaps, and produced a paper bundle.

User Prompt:

> Restructure the paper. Use the model most relevant to the goal as the proposed method. Put the others in Alternative Models in the appendix.

AI:

> Reframed the paper around component and path bottleneck prediction.
>
> Moved runtime-focused and secondary models to appendices.
>
> Updated abstract, method, results, limitations, and conclusion.
>
> Rebuilt the PDF.

User Prompt:

> Use math symbols instead of long programming variable names, and explain notation near its usage.

AI:

> Replaced code-like names with symbols such as predicted runtime, saturated component, and blocking path notation.
>
> Added local notation explanations near the formulas.
>
> Rebuilt the PDF.

User Prompt:

> Appendix D is important proof of model correctness. Promote it into the main experiment section.

AI:

> Moved the full NCU validation protocol into the main text.
>
> Kept the counter mapping, per-round tables, interpretation, and model-refinement discussion visible in Section 5.
>
> Rebuilt and checked the PDF.

User Prompt:

> The NCU activity figure layout is bad. Check the image and fix it.

AI:

> Regenerated the figure with better spacing and labels.
>
> Rebuilt the PDF and inspected the affected page.
>
> Confirmed the layout is readable.

## Run to a Local PDF

When the current state is incomplete, a target-scoped run-to request can cover only the prerequisite work the requested output needs.

User Prompt:

> Run to a validated local survey PDF. Satisfy the evidence prerequisites, but do not publish or submit it.

AI:

> Ran the required audit and recorded its terminal report. The audit found a bounded source-lineage defect, so I ran the named repair as a separate procedure, refreshed the accepted refs, and completed a fresh audit.
>
> Used the accepted audit to synthesize the missing paper inputs, drafted canonical paper state, and constructed and inspected the local PDF. Each prerequisite retained its own Run, checkpoint, and terminal report.
>
> The validated local PDF target is complete. I stopped before publication and submission.

The exact traversal depends on current durable state. If the audit, synthesis, or draft already satisfies the consumer contract, the agent reuses it instead of repeating that work. A non-ready audit ends its bounded procedure before repair; the prompt-level controller may consume the repair route only under the explicit run-to authorization, then starts a fresh audit. Structure acceptance, material evidence choices, unexpected dependencies or build resources, destructive changes, build authorization, publication, and submission remain human Gates.

## How to Steer

Give page numbers, figure numbers, table numbers, and the exact reader problem. If the agent says the PDF built, ask whether it inspected the rendered pages. If important proof is hidden in an appendix, ask it to promote the proof into the main narrative.

Useful steering prompts:

User Action:

> $isomer-ext-deepsci-entrypoint use paper-pass to write or update the PDF paper and select the applicable workflow

User Prompt:

> Inspect the rendered PDF, not only the build log. Report any clipped text, overlapping labels, or unreadable tables.

User Prompt:

> Explain every column in these tables in the main text before the reader sees them.

User Prompt:

> This figure lost semantics. Revert or redesign it so the connections remain clear.

## Under the Hood

The write skill should use accepted records and evidence as inputs, build the paper with the requested toolchain, and store generated drafts and PDFs under the Topic Workspace output policy. For TeX manuscripts, the skill should prefer Tectonic first, then record a concrete blocker before falling back to another LaTeX workflow. Run-to is agent-controller authorization for prerequisite recovery, not a shell or `isomer-cli` command.

## What Good Looks Like

The paper states one central claim, supports it with visible evidence, explains notation near use, renders figures and tables cleanly, and keeps the proof in the main text when the proof is essential.

## Common Pitfalls

Do not accept "PDF generated" as proof that the paper is readable. Do not let appendices carry the only proof of the central claim. Do not make diagrams prettier by removing the semantic connections the paper needs.

## Next Tutorial

You have completed the research-workflow suite. Return to [Research Workflow Tutorials](index.md) to pick a specific stage again.

## Links

- [FlashAttention-4 analytical model example](https://github.com/CodeGandee/isomer-example-fa4-analytical-model)
