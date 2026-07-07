## Why

Idea detail tabs currently render noisy source artifacts because an Idea Realization can point at a broad or invalid JSON path, and the backend falls back to the whole record payload. Users expect the main idea panel to show the selected Primary Idea itself, with source records available as provenance rather than replacing the idea content.

## What Changes

- Define a strict Primary Idea source contract: every Idea Realization that powers a default idea detail view must point to the exact JSON object for that Research Idea, not the whole source artifact, list, filter notes, route notes, or generated Markdown.
- Teach `isomer-cli` idea and record-write surfaces to validate, import, repair, and expose exact source fragments with diagnostics when the source path is missing, broad, stale, or unresolved.
- Update production DeepSci skills and placeholder-binding guidance so agents write structured idea payloads and realization metadata that distinguish idea content, slate/report context, filter notes, and provenance.
- Update the GUI/backend idea detail read model so the idea main panel renders the resolved Primary Idea fragment first, shows source-record context separately, and never silently treats a full source artifact fallback as the idea.
- Repair `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` so its existing records and runtime idea metadata look like they were produced by the latest source contract.

## Capabilities

### New Capabilities
- `primary-idea-source-contract`: Defines exact source-fragment requirements, validation, import/repair behavior, and GUI semantics for Primary Idea detail content.

### Modified Capabilities
- `research-record-query-index`: Add indexed/read-model diagnostics and export fields for exact idea source fragments, source-path validity, and fallback classification.
- `research-placeholder-bindings`: Require DeepSci structured bindings that produce ideas to name idea-bearing payload sections and source-path expectations.
- `research-paradigm-skills`: Require DeepSci idea-producing workflows to preserve exact idea content separately from slate/report notes and record Idea Realizations through the CLI.

## Impact

- Affects `isomer-cli ext research ideas`, structured record creation/import/repair paths, Workspace Runtime validation, query-index rebuild/export, and FastAPI idea detail endpoints.
- Affects DeepSci skill text, placeholder bindings, validation harnesses, and packaged system-skill assets.
- Affects GUI idea detail rendering, source-record links, diagnostics, and tests around JSON-backed Markdown previews.
- Requires a focused migration of the flash-attention topic runtime database and managed payload files so current GUI fixtures match the new contract.
