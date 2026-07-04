# list-passes

List the available pipeline passes.

## Workflow

When this subcommand is invoked, execute the following steps in order.

1. **Read the pass catalog**. Use the **Subcommands** table in `SKILL.md` to enumerate the available passes.
2. **Summarize each pass**. For each pass, record its kebab-case name, the one-line description from `commands/<pass>.md`, and the first and last stage skills from the recipe table.
3. **Return the catalog**. Present the list to the caller and stop. Do not execute any pass.

If the user's task does not map cleanly to listing passes, route back to `isomer-deepsci-pipeline` main workflow.

## Current passes

| Pass | First stage | Last stage | Description |
| --- | --- | --- | --- |
| `empirical-pass` | `isomer-deepsci-scout` | `isomer-deepsci-analysis` | Full single-pass empirical loop from framing to interpretable analysis. |
| `hypothesis-pass` | `isomer-deepsci-idea` | `isomer-deepsci-analysis` | Run a selected hypothesis through experiment and analysis. |
| `paper-pass` | `isomer-deepsci-paper-outline` | `isomer-deepsci-review` | Turn analysis findings into a reviewed paper bundle. |
| `revision-pass` | `isomer-deepsci-review` | `isomer-deepsci-write` | Self-review a draft, fill evidence gaps, and revise. |
| `rebuttal-pass` | `isomer-deepsci-rebuttal` | `isomer-deepsci-write` | Turn formal reviewer feedback into revised text and evidence. |
| `polish-pass` | `isomer-deepsci-figure-polish` | `isomer-deepsci-review` | Polish figures and prose before external review. |
| `submission-pass` | `isomer-deepsci-review` | `isomer-deepsci-finalize` | Finalize a reviewed paper bundle for submission or archive. |
