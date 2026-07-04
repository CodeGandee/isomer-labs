# nature-paper2ppt Skill Analysis

Source skill: [nature-paper2ppt](../../../extern/orphan/DeepScientist/src/skills/nature-paper2ppt/SKILL.md)

Role: companion

Purpose: build a complete Chinese PPTX presentation from a scientific paper, preprint, PDF, article text, abstract, figure legends, or reading notes.

## Mermaid UML Workflow

```mermaid
stateDiagram-production DeepSci
    [*] --> Extract_Source_Material
    Extract_Source_Material --> Classify_Paper_Type
    Classify_Paper_Type --> Choose_Presentation_Logic
    Choose_Presentation_Logic --> Build_Chinese_Plan
    Build_Chinese_Plan --> Select_Evidence_Figures
    Select_Evidence_Figures --> Extract_Selected_Assets
    Extract_Selected_Assets --> Write_Slide_Content
    Write_Slide_Content --> Build_PPTX
    Build_PPTX --> Verify_Package
    Verify_Package --> Render_Inspect: renderer available
    Verify_Package --> QA_Report: renderer unavailable
    Render_Inspect --> Revise: defects found
    Revise --> Build_PPTX
    Render_Inspect --> QA_Report
    QA_Report --> [*]
```

## State Step Meanings

| Step | Meaning |
| --- | --- |
| `Extract_Source_Material` | Pull paper metadata, claims, methods, results, figures, and limitations. |
| `Classify_Paper_Type` | Identify the paper category before planning slides. |
| `Choose_Presentation_Logic` | Pick claim-first, question-to-evidence, problem-to-solution, or similar logic. |
| `Build_Chinese_Plan` | Create the Chinese slide sequence and story spine. |
| `Select_Evidence_Figures` | Choose only figures that carry the argument. |
| `Extract_Selected_Assets` | Crop or render needed figures and record provenance. |
| `Write_Slide_Content` | Write titles, bullets, captions, takeaways, and speaker notes. |
| `Build_PPTX` | Create the actual editable deck. |
| `Verify_Package` | Reopen and inspect slide/media/package structure. |
| `Render_Inspect` | Check rendered previews when a renderer exists. |
| `QA_Report` | Record checks and remaining limitations. |

## Inner Working

The skill is deck-first. It should produce an actual `.pptx`, not only an outline. The default path uses Python tooling: PyMuPDF for paper extraction and page rendering, Pillow for crops and previews, python-pptx for slide authoring, and zipfile/python-pptx reopen checks for validation.

It reads the source in two passes: metadata, abstract, headings, figure legends, and table captions first; then only the result and method pages needed for slides. It classifies the paper type and chooses presentation logic such as claim-first, question-to-evidence, problem-to-solution, workflow-to-validation, or evidence-map.

Figures are selected as evidence, not decoration. The deck normally uses a 10-16 slide Chinese structure, extracts only needed assets, writes concise slide content and speaker notes, builds the PPTX, then verifies package structure or rendered previews.

## Durable Outputs

- `output/final_presentation_cn.pptx`.
- `output/qa_report.md`.
- `output/assets/figures/`.
- `output/asset_manifest.md`.
- Optional outline, figure plan, script, and rendered previews.

## Key Constraints

- Do not stop at an outline or script.
- Do not invent missing numbers, mechanisms, datasets, or figure details.
- Avoid full OCR, full supplement extraction, and all-slide rendered QA unless justified.
- Keep figures readable; prefer fewer key panels over many cramped graphics.
