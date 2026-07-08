## Why

Idea nodes now carry enough structured metadata and realization links for meaningful inspection, but the GUI still risks showing raw JSON or record internals where the user wants a readable idea document. UC-02 needs an idea detail experience that previews structured JSON as Markdown while preserving exact JSON access for verification and copying.

## What Changes

- Add a topic-scoped idea detail tab that opens from an idea-lineage node and preserves graph context.
- Add frontend JSON-to-MDAST conversion that maps nested JSON keys into Markdown document nodes and serializes with the unified Markdown ecosystem.
- Add actions to view exact JSON in an in-app blocking modal overlay, copy exact JSON, and copy generated Markdown.
- Add read-only backend payload resolution needed by the detail tab, including diagnostics for missing, stale, unsupported, or oversized source JSON.
- Keep generated Markdown ephemeral in the browser; do not write generated preview Markdown back to Workspace Runtime or topic files.

## Capabilities

### New Capabilities

- `idea-node-content-preview`: GUI behavior for opening an idea node, rendering its JSON-backed content as Markdown, viewing exact JSON in a modal, and copying JSON or Markdown.

### Modified Capabilities

- `research-record-query-index`: Ensure topic-scoped read APIs can resolve canonical idea realizations and source JSON payload data needed by the idea detail viewer without mutating Workspace Runtime.

## Impact

- Frontend work in `web/ui` for idea detail tabs, JSON modal overlay, copy actions, MDAST document-builder helpers, and tests.
- Backend work in `src/isomer_labs/web/` and related read-model code to expose idea detail and exact source JSON data through read-only topic-scoped APIs.
- Dependency updates for the TypeScript Markdown generation stack: `mdast-util-to-markdown`, `mdast-util-gfm`, `mdast-util-frontmatter`, and `unist-builder`.
- Tests should cover JSON-to-Markdown conversion, modal behavior, copy-action states, read-only backend diagnostics, and a Playwright smoke path from an idea node to preview and JSON modal.
