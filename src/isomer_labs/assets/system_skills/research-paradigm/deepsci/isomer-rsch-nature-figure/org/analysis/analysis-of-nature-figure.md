# nature-figure Skill Analysis

Source skill: [nature-figure](../../../extern/orphan/DeepScientist/src/skills/nature-figure/SKILL.md)

Role: companion

Purpose: create, revise, audit, or polish submission-grade Nature or high-impact journal figures using a single selected backend: Python or R.

## Mermaid UML Workflow

```mermaid
stateDiagram-production DeepSci
    [*] --> Check_Backend_Selection
    Check_Backend_Selection --> Ask_Python_Or_R: backend missing
    Check_Backend_Selection --> Define_Figure_Contract: backend selected
    Ask_Python_Or_R --> [*]
    Define_Figure_Contract --> Check_Runtime
    Check_Runtime --> Blocked: selected runtime unavailable
    Check_Runtime --> Map_Evidence_Chain
    Map_Evidence_Chain --> Choose_Archetype
    Choose_Archetype --> Set_Journal_Export_Contract
    Set_Journal_Export_Contract --> Generate_With_Selected_Backend
    Generate_With_Selected_Backend --> Preview_And_QA
    Preview_And_QA --> Revise: visual or evidence defect
    Revise --> Generate_With_Selected_Backend
    Preview_And_QA --> Export_Final
    Export_Final --> [*]
    Blocked --> [*]
```

## State Step Meanings

| Step | Meaning |
| --- | --- |
| `Check_Backend_Selection` | Confirm whether Python or R has been chosen. |
| `Ask_Python_Or_R` | Stop and ask when backend choice is missing. |
| `Define_Figure_Contract` | Define conclusion, evidence chain, panels, dimensions, and exports. |
| `Check_Runtime` | Verify the selected backend and needed packages exist. |
| `Map_Evidence_Chain` | Link each panel to a unique piece of evidence. |
| `Choose_Archetype` | Pick figure structure such as quantitative grid or mixed-modality composite. |
| `Set_Journal_Export_Contract` | Fix format, editable text, statistics, and integrity requirements. |
| `Generate_With_Selected_Backend` | Draw only with the selected backend. |
| `Preview_And_QA` | Inspect exported previews for scientific and visual defects. |
| `Export_Final` | Save journal-ready outputs. |

## Inner Working

The first gate is backend selection. If the user has not chosen Python or R and no language-specific input makes it obvious, the skill must ask "Python or R?" and stop. After selection, all drawing, previewing, exporting, and visual QA must use that same backend.

Before plotting, the skill defines the figure contract: one-sentence conclusion, evidence chain, panel roles, archetype, dimensions, editable text, source data, statistics, image-integrity notes, and export formats.

The scientific logic outranks the template. Panels that do not carry unique evidence should be dropped, and missing runtime/package state should be reported rather than bypassed with the other language.

## Durable Outputs

- Backend-specific plotting script.
- SVG/PDF/TIFF/PNG exports as required.
- QA render or preview evidence.
- Figure contract and source-data/statistics notes.

## Key Constraints

- Do not choose Python or R by default when the user has not chosen.
- Do not cross-render with the unselected backend.
- Do not create mock data.
- Do not disclose private local paths or internal reference filenames in figure text or user-facing prose.
