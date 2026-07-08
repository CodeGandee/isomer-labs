# idea-node-content-preview Specification

## Purpose
TBD - created by archiving change add-idea-json-markdown-preview. Update Purpose after archive.
## Requirements
### Requirement: Idea Node Detail Tab
The GUI SHALL open a topic-scoped idea detail tab when the user opens a canonical Research Idea node from the idea-lineage graph or semantic openable item system.

#### Scenario: Idea node opens idea detail
- **WHEN** the user clicks an idea-lineage node with canonical `idea_id` metadata
- **THEN** the GUI opens or focuses an `ideaDetail` workbench tab for that topic and idea id
- **AND** the existing graph topic, filters, and layout context remain available when the user returns to the graph tab

#### Scenario: Non-idea node keeps existing behavior
- **WHEN** the user clicks a graph node that does not identify a canonical Research Idea
- **THEN** the GUI keeps the existing record or artifact open behavior for that node

### Requirement: JSON-backed Markdown Preview
The idea detail tab SHALL render a readable Markdown preview generated dynamically from the selected idea's exact JSON source content when that content is available.

#### Scenario: JSON converts through MDAST
- **WHEN** the idea detail payload includes source JSON content
- **THEN** the frontend converts the JSON into MDAST document nodes and serializes those nodes to Markdown with the unified Markdown ecosystem
- **AND** feature code does not hand-concatenate Markdown syntax for headings, lists, tables, code blocks, or frontmatter

#### Scenario: Nested keys become readable structure
- **WHEN** the JSON contains nested objects, arrays, scalar values, and unsupported subtrees
- **THEN** the preview maps object keys to nested headings or sections, scalar values to readable text, scalar arrays to lists, compatible arrays of objects to GFM tables, and unsupported subtrees to fenced JSON code blocks

#### Scenario: Metadata is secondary
- **WHEN** the JSON contains ids, digests, locators, provenance refs, source paths, or other system metadata
- **THEN** the preview places those fields in a collapsed or visually secondary `Metadata` section
- **AND** human-facing idea content appears before metadata

#### Scenario: Table rendering is deterministic
- **WHEN** an array contains objects whose rows all share the same scalar keys
- **THEN** the preview renders that array as a GFM table
- **AND** mixed, deep, or incompatible object arrays render as nested sections or fenced JSON instead of malformed tables

#### Scenario: Missing JSON shows diagnostic
- **WHEN** the idea detail payload cannot provide exact source JSON
- **THEN** the tab shows canonical idea metadata and realization history
- **AND** the Markdown preview area shows a diagnostic or empty state instead of a raw JSON placeholder

### Requirement: Raw JSON Modal
The idea detail tab SHALL provide a raw JSON viewer as an in-app blocking modal overlay.

#### Scenario: User opens JSON modal
- **WHEN** the user clicks the view JSON action on an idea detail tab with source JSON
- **THEN** the GUI darkens the rest of the workbench and shows formatted exact JSON in a scrollable modal overlay
- **AND** it does not open a separate browser window or navigate away from the tab

#### Scenario: User closes JSON modal
- **WHEN** the JSON modal is open and the user presses Escape, clicks the close control, or uses the supported backdrop close interaction
- **THEN** the modal closes and focus returns to the idea detail context

### Requirement: Copy JSON And Markdown
The idea detail tab SHALL let the user copy both exact JSON content and generated Markdown content.

#### Scenario: Copy exact JSON
- **WHEN** the user clicks copy JSON from the idea detail tab or JSON modal
- **THEN** the GUI writes the normalized exact JSON string to the clipboard
- **AND** it shows a visible success or failure state without closing the tab or modal

#### Scenario: Copy generated Markdown
- **WHEN** the user clicks copy Markdown from the idea detail tab
- **THEN** the GUI writes the Markdown string produced by the MDAST serializer to the clipboard
- **AND** it shows a visible success or failure state without changing source JSON or Workspace Runtime state

### Requirement: Read-only Inspection Behavior
The idea detail inspection workflow SHALL NOT mutate research state, generated files, query-index rows, or source payload files during ordinary browsing.

#### Scenario: Preview is ephemeral
- **WHEN** the idea detail tab generates Markdown from JSON for preview or copy
- **THEN** the generated Markdown remains browser-side ephemeral state
- **AND** no Workspace Runtime record, topic file, query-index row, or generated Markdown artifact is created or updated

#### Scenario: Refresh preserves selected idea
- **WHEN** topic read-model invalidation occurs while an idea detail tab is open
- **THEN** the GUI keeps the selected idea id and refreshes only the active idea detail query
- **AND** it reports source payload digest changes when the backend exposes them

