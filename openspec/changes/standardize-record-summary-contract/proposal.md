## Why

Research records and Research Ideas do not share one reliable display contract today. Some payloads expose `title` and `summary`, idea records expose `title` and `one_liner`, and import paths sometimes duplicate the same text into both display slots, which forces GUI parsers and agents to guess.

This should be fixed before the idea graph and timeline grow further, because the GUI needs short, consistent display fields and agents need schema-backed instructions that make those fields parsable.

## What Changes

- Introduce `structured-record.v2` as the supported structured Research Record display contract, requiring non-empty top-level `title` and `summary`; `summary` is the brief display description.
- Treat `structured-record.v1` usage as unsupported for new writes; v1 may be read only by validation, repair, or migration code.
- **BREAKING** Replace Research Idea `one_liner` with `summary` in runtime models, DB schema/read models, CLI/API payloads, GUI contracts, query-index idea facets, and source-fragment import logic.
- Require idea-bearing payload objects that can become canonical Research Ideas to include `title` and `summary`, with legacy source aliases handled only by migration or repair code.
- Update DeepSci placeholder-binding and skill guidance so agents write `title` and `summary` for payloads and idea entries before records are accepted.
- Add validation and repair diagnostics for missing or duplicated display fields instead of silently copying one text field into another.
- Migrate `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` only after the code can read and write the new `summary` interpretation, scanning all records and fixing stored summaries directly.

## Capabilities

### New Capabilities
- `record-display-contract`: Canonical display fields for structured records and idea-bearing payload objects.

### Modified Capabilities
- `artifact-format-processing`: Generic DeepSci structured payload validation requires `title` and `summary`.
- `research-recording-contracts`: Research record create, update, validate, show, list, and repair paths enforce and expose the display contract.
- `research-record-query-index`: Query-index extraction and facets use `summary` consistently and stop deriving idea display text from `one_liner`.
- `research-idea-lineage`: Canonical Research Ideas store and expose `summary` instead of `one_liner`.
- `primary-idea-source-contract`: Exact idea source fragments resolve `title` and `summary` as the idea content contract.
- `research-placeholder-bindings`: DeepSci binding pages teach agents to author the required display fields for payloads and idea entries.
- `research-paradigm-skills`: Skill validation detects missing or stale `title` and `summary` guidance.
- `project-web-data-contracts`: GUI graph, timeline, hover, and detail read contracts expose `summary` and remove `one_liner` as a first-class field.

## Impact

- Runtime and storage: `ResearchIdea`, clean Workspace Runtime SQLite schema/migrations, idea validation, import/repair, and flash-attention topic data.
- CLI/API: `ext research ideas`, `ext research records`, query-index exports, Project Web graph/detail endpoints, and generated TypeScript types with `one_liner` removed from graph/read contracts.
- Skills and docs: DeepSci system skill guidance, placeholder bindings, artifact schemas, UI contracts, and validation tests.
- Migration: existing topic payload files and SQLite rows need a one-time direct data migration after code-level compatibility is in place.
