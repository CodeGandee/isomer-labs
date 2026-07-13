## Why

Kaoju can produce audited survey knowledge, but it has no owned workflow for turning that knowledge into a publication-facing manuscript and validated PDF. Agents therefore improvise paper files and build commands, which can bypass Kaoju's record and audit contracts and can accept visibly defective output when compilation alone succeeds. A survey paper also needs different writing gates from a hypothesis-driven paper: it should earn trust through coverage accounting, comparison soundness, source traceability, calibrated synthesis, and explicit limitations rather than through a forced novelty argument.

## What Changes

- Add a dedicated `isomer-kaoju-write` skill that converts accepted, audited Kaoju synthesis records into a paper contract, manuscript source, citation state, compile report, validation report, and publication bundle without changing the underlying evidence meaning.
- Add a `paper-pass` procedural subcommand to `isomer-kaoju-pipeline` that verifies writing prerequisites, invokes the writing skill, routes document builds through existing execution-extension and Gate contracts, validates the rendered document, and returns a bounded terminal report.
- Adapt DeepSci's evidence-first paper practices to survey reporting: separate the reader-facing paper view from the evidence view, define section jobs, preserve a claim-evidence boundary, verify citations before drafting, plan comparative displays before prose, interpret rather than narrate tables, and conduct a skeptical prepublication review.
- Define a survey-paper quality profile that reports coverage accounting, discovery and screening posture, source identity integrity, evidence-depth compliance, comparison soundness, claim and citation traceability, contradiction and limitation propagation, synthesis usefulness, reporting clarity, and document quality against contract-defined denominators and thresholds.
- Make novelty optional rather than a readiness gate: the paper may explain a grounded taxonomy, comparative insight, coverage contribution, or field-level synthesis, but it cannot invent a novelty claim merely to imitate an empirical research paper.
- Define paper-specific Kaoju semantic ids, storage bindings, family-neutral profiles, lineage, revision, and file-attachment rules for publication-facing records and outputs.
- Require a LaTeX `.tex` publication source and bibliography inputs, Tectonic-first compilation with recorded LaTeX-toolchain fallback, compiler-owned section numbering, LaTeX title metadata, appropriate unnumbered front and back matter, verified citations, reproducible build reporting, and post-render PDF inspection.
- Reject Markdown-to-PDF conversion as the publication build path and reject manually numbered LaTeX headings; Markdown may remain planning or intake material only and must be transformed into validated `.tex` before a paper build.
- Reject publication readiness when compilation succeeds but structural, textual, or visual validation fails, including duplicate section numbering, malformed hierarchy or table of contents, overflow, unreadable tables or figures, and missing build provenance.
- Extend the packaged Kaoju inventory, validation harness, extension discovery metadata, and tests for the new skill and command while preserving DeepSci behavior.

## Capabilities

### New Capabilities

- `kaoju-paper-writing`: Defines the dedicated Kaoju writing stage, `paper-pass` orchestration, `create-paper-template` template generation, publication-facing inputs and outputs, build routing, manuscript validation, and revision behavior.
- `research-templates-cli`: Defines the `isomer-cli ext research templates` surface for generating, listing, showing, refreshing, compiling, and removing derived paper-writing templates under `intent/derived/writing-template/`.

### Modified Capabilities

- `kaoju-research-extension`: Adds `isomer-kaoju-write` to the production skill family and adds `paper-pass` and `create-paper-template` to the public procedural command surface.
- `kaoju-artifact-bindings`: Adds registered paper-writing semantic ids, binding rows, profiles, lineage rules, and publication file references.
- `research-paradigm-skills`: Expands Kaoju inventory and family-specific validation for the writing skill, command pages, direct resources, and output discipline.
- `packaged-system-skills`: Packages and materializes the new Kaoju skill and its callback insertion points as part of the optional Kaoju extension.
- `system-skill-installer-cli`: Exposes the new skill, `paper-pass`, and `create-paper-template` commands through Kaoju extension discovery and inspection output.

## Impact

The change affects packaged Kaoju skill assets, the Kaoju manifest inventory and extension metadata, shared artifact semantics, producer binding pages, family-neutral format-profile assets, research-paradigm validators, system-skill discovery tests, the transitional `isomer-cli ext research` CLI surface, and Kaoju documentation. It uses the existing `document_build`, publication-facing Gate, worker-output, research-record, and execution-adapter contracts rather than adding a Kaoju-specific build runtime or PDF CLI.
