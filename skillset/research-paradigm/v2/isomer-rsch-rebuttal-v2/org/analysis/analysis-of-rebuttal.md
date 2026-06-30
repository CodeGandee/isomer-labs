# rebuttal Skill Analysis

Source skill: [rebuttal](../../../extern/orphan/DeepScientist/src/skills/rebuttal/SKILL.md)

Role: companion

Purpose: map reviewer feedback into experiments, manuscript deltas, and a durable rebuttal or revision response.

## Mermaid UML Workflow

```mermaid
stateDiagram-v2
    [*] --> Normalize_Review_Package
    Normalize_Review_Package --> Build_Reviewer_Item_Matrix
    Build_Reviewer_Item_Matrix --> Decide_Required_Changes
    Decide_Required_Changes --> Route_Literature: novelty or positioning
    Decide_Required_Changes --> Route_Baseline: comparator missing
    Decide_Required_Changes --> Launch_Analysis: new evidence needed
    Decide_Required_Changes --> Route_Write: manuscript change needed
    Decide_Required_Changes --> Assemble_Response: evidence/text ready
    Route_Literature --> Scout
    Route_Baseline --> Baseline
    Launch_Analysis --> Analysis_Campaign
    Route_Write --> Write
    Scout --> Update_Rebuttal_Matrix
    Baseline --> Update_Rebuttal_Matrix
    Analysis_Campaign --> Update_Rebuttal_Matrix
    Write --> Update_Rebuttal_Matrix
    Update_Rebuttal_Matrix --> Assemble_Response
    Assemble_Response --> Final_Revision_Handoff
    Final_Revision_Handoff --> [*]
```

## State Step Meanings

| Step | Meaning |
| --- | --- |
| `Normalize_Review_Package` | Convert reviewer material into durable, structured inputs. |
| `Build_Reviewer_Item_Matrix` | Split feedback into stable reviewer item ids. |
| `Decide_Required_Changes` | Classify each issue as text, evidence, experiment, baseline, literature, or limitation. |
| `Route_Literature` | Use scout when novelty or positioning is the real issue. |
| `Route_Baseline` | Use baseline when a comparator gap blocks the response. |
| `Launch_Analysis` | Use analysis-campaign for required new reviewer-linked evidence. |
| `Route_Write` | Use write for manuscript structure, claim, or wording changes. |
| `Update_Rebuttal_Matrix` | Refresh item status after each routed fix. |
| `Assemble_Response` | Draft the point-by-point author response. |
| `Final_Revision_Handoff` | Update response, text deltas, evidence notes, and bundle status. |

## Inner Working

The skill normalizes reviewer pressure into atomic items. Each item gets a stable id, source-faithful wording, class, severity, affected claim, evidence anchor, and route. Vague reviewer paragraphs are split into auditable work items.

It then decides whether each issue needs explanation only, evidence repackaging, new supplementary experiment, claim downgrade, explicit limitation, literature positioning, baseline recovery, or manuscript rewrite.

Experiments are launched only when genuinely needed. Reviewer-linked runs are expressed through the shared `analysis-campaign` protocol, and every slice should answer named reviewer item ids. Manuscript changes route through `write`, with text deltas and evidence basis kept explicit.

## Durable Outputs

- Review matrix.
- `paper/rebuttal/action_plan.md`.
- Reviewer-linked experiment/action TODOs.
- `paper/rebuttal/evidence_update.md`.
- Text deltas and response letter.
- Revised paper bundle when ready.

## Key Constraints

- Do not launch free-floating ablation batches.
- Do not rewrite reviewer meaning when normalizing comments.
- Do not pretend limitations are solved when only reframed.
- Do not finalize while reviewer-critical feasible matrix rows remain unresolved.
