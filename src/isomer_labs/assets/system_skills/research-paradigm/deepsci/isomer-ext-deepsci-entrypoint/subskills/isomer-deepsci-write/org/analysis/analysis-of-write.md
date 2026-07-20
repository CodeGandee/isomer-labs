# write Skill Analysis

Source skill: [write](../../../extern/orphan/DeepScientist/src/skills/write/SKILL.md)

Role: stage

Purpose: draft or refine a paper, report, or research summary from existing evidence without inventing missing support.

## Mermaid UML Workflow

```mermaid
stateDiagram-production DeepSci
    [*] --> Refresh_Control_State
    Refresh_Control_State --> Lock_Paper_Contract
    Lock_Paper_Contract --> Validate_Outline
    Validate_Outline --> Paper_Outline: outline invalid
    Validate_Outline --> Compile_Writing_Plan: outline valid
    Paper_Outline --> Validate_Outline
    Compile_Writing_Plan --> Sort_Source_Material
    Sort_Source_Material --> Refresh_Citations
    Refresh_Citations --> Plan_Displays
    Plan_Displays --> Paper_Plot: first-pass figure needed
    Plan_Displays --> Draft_Sections: no figure blocker
    Paper_Plot --> Figure_Polish
    Figure_Polish --> Draft_Sections
    Draft_Sections --> Validate_Manuscript
    Validate_Manuscript --> Submit_Draft_Checkpoint
    Validate_Manuscript --> Analysis_Campaign: evidence gap
    Validate_Manuscript --> Review: reviewable but not final
    Validate_Manuscript --> Finalize: submission-ready
    Submit_Draft_Checkpoint --> [*]
    Analysis_Campaign --> [*]
    Review --> [*]
    Finalize --> [*]
```

## State Step Meanings

| Step | Meaning |
| --- | --- |
| `Refresh_Control_State` | Read memory, quest state, conversation, and active paper surfaces. |
| `Lock_Paper_Contract` | Align outline, evidence ledger, experiment matrix, and references. |
| `Validate_Outline` | Check whether the paper idea and evidence boundaries are sound. |
| `Paper_Outline` | Repair the outline before drafting if needed. |
| `Compile_Writing_Plan` | Turn a valid outline into section jobs. |
| `Sort_Source_Material` | Separate claims, settings, reproducibility details, and artifact history. |
| `Refresh_Citations` | Verify literature and bibliography from real sources. |
| `Plan_Displays` | Decide which figures or tables are needed. |
| `Paper_Plot` | Create first-pass standard figures from structured data. |
| `Figure_Polish` | Finalize paper-facing figures. |
| `Draft_Sections` | Write section jobs within evidence limits. |
| `Validate_Manuscript` | Check coverage, language, claims, figures, and bundle readiness. |
| Route states | Submit checkpoint, launch analysis, review, or finalize. |

## Inner Working

The skill starts with control state, not prose. It checks memory, quest state, selected outline, evidence ledger, experiment matrix, references, and paper contract health. If the outline is weak, it routes through `paper-outline` instead of drafting around the problem.

It separates source material into manuscript claims, experiment settings, reproducibility details, implementation details, and artifact history. Only supported claims and relevant experiment settings belong in main text.

Writing proceeds by section jobs. It refreshes citations from real sources, plans displays before prose, uses `paper-plot` for first-pass standard figures, `figure-polish` for final visual QA, and `nature-*` companion skills only for bounded tasks after evidence rows are known.

The final route depends on validation: stronger draft, explicit blocker, analysis campaign for missing evidence, review package, or submission-ready package.

## Durable Outputs

- Updated paper sections or report text.
- Paper contract, evidence ledger, experiment matrix, references, figures, and bundle status kept aligned.
- `artifact.submit_paper_bundle(...)` for draft checkpoints, review packages, or submission packages.
- Route-back decision when evidence, outline, or coverage is insufficient.

## Key Constraints

- Do not hand-write BibTeX, citations, metrics, or method details from memory.
- Do not use polished prose to hide missing evidence.
- Do not put user/operator/agent provenance or route-control wording into manuscript text.
- Real compile, render, search, or file-inspection claims must come from `bash_exec(...)`.
