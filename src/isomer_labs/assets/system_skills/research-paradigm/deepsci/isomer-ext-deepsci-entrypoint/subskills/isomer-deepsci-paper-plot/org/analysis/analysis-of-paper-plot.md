# paper-plot Skill Analysis

Source skill: [paper-plot](../../../extern/orphan/DeepScientist/src/skills/paper-plot/SKILL.md)

Role: companion

Purpose: turn structured numeric data into a first-pass publication-quality figure by adapting bundled plotting templates.

## Mermaid UML Workflow

```mermaid
stateDiagram-production DeepSci
    [*] --> Confirm_Chart_Question
    Confirm_Chart_Question --> Choose_Bundled_Style
    Choose_Bundled_Style --> Read_Style_Reference
    Read_Style_Reference --> Copy_Template_Script
    Copy_Template_Script --> Replace_Data_Block
    Replace_Data_Block --> Run_Copied_Script
    Run_Copied_Script --> Inspect_Render
    Inspect_Render --> Hand_To_Figure_Polish: durable or paper-facing
    Inspect_Render --> Done: first pass enough
    Hand_To_Figure_Polish --> [*]
    Done --> [*]
```

## State Step Meanings

| Step | Meaning |
| --- | --- |
| `Confirm_Chart_Question` | Clarify comparison, units, grouping, and output target. |
| `Choose_Bundled_Style` | Pick the closest existing bar, line, scatter, or radar template. |
| `Read_Style_Reference` | Read the selected style's visual and rcParams guidance. |
| `Copy_Template_Script` | Copy the script into a quest-local workspace. |
| `Replace_Data_Block` | Edit only data, labels, and needed category fields. |
| `Run_Copied_Script` | Generate the first-pass figure. |
| `Inspect_Render` | Check the actual rendered output. |
| `Hand_To_Figure_Polish` | Send durable or paper-facing figures to final QA. |
| `Done` | Stop when first-pass output is sufficient. |

## Inner Working

The skill is for standard figure families: bar, line, scatter, and radar plots. It asks or clarifies chart question, units, grouping, and output location before choosing a style.

It does not improvise a new plotting stack. The agent reads the selected reference file, copies the corresponding script into a quest-local figure workspace, edits only the data and label block, runs the copied script, and inspects the output.

The bundled templates emit a 300 dpi PNG first. If the figure becomes paper-facing or final, it should pass to `figure-polish` for final render-inspect-revise and vector export.

## Durable Outputs

- Quest-local copied plotting script.
- Source data near the script or figure output.
- First-pass rendered figure.
- Optional handoff to `figure-polish`.

## Key Constraints

- Do not use this for final QA of an already rendered figure; use `figure-polish`.
- Do not use it for disposable debug plots.
- Do not mutate the bundled template directly.
- Keep labels, legends, categories, widths, colors, and tick labels consistent when substituting data.
