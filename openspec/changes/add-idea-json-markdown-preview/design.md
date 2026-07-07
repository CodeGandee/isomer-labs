## Context

The Project Web GUI already has a React/Dockview workbench, semantic openable descriptors, topic graph panels, record detail panels, Markdown rendering, and topic-scoped FastAPI read endpoints. The new UC-02 use case asks for an idea-node detail experience: when a user clicks a primary idea node, the GUI should open a focused idea tab, render the idea's exact JSON-backed content as readable Markdown, and still let the user inspect or copy the exact JSON.

Recent lineage work added canonical Research Ideas, idea realizations, generation groups, and canonical idea graph nodes. The graph nodes already carry `idea_id`, realization summaries, and detail refs, but the frontend still opens records from graph nodes by default and does not have an idea-specific viewer. The feature design also now chooses MDAST and the unified Markdown ecosystem for JSON-to-Markdown generation, so implementation should avoid ad hoc Markdown string concatenation in the idea preview path.

## Goals / Non-Goals

**Goals:**

- Treat idea nodes as first-class openable workbench items with stable `idea:<topic_id>:<idea_id>` identity.
- Add a topic-scoped read API that resolves canonical idea metadata, realization history, latest realization record detail, and exact source JSON or clear diagnostics.
- Generate Markdown preview dynamically in the frontend by converting JSON into MDAST nodes and serializing through `mdast-util-to-markdown`.
- Provide an in-app blocking JSON modal overlay with formatted exact JSON, close behavior, and copy JSON action.
- Provide copy actions for exact JSON and generated Markdown, with visible success or failure state.
- Keep ordinary browsing read-only and keep generated Markdown ephemeral in browser state.

**Non-Goals:**

- Do not edit ideas, source JSON, lifecycle records, query-index rows, or generated Markdown from the GUI.
- Do not persist generated Markdown previews into Workspace Runtime or topic files.
- Do not build schema-specific renderers for every artifact type in the first pass; generic nested-key rendering is enough.
- Do not add a physical browser popup window for JSON viewing.
- Do not replace the existing record detail tab or Markdown viewer.

## Decisions

### Use `idea:` openable items and an `ideaDetail` Dockview component

Graph node clicks should open `idea:<topic_id>:<idea_id>` when the node has `material_kind="idea"` and a source `idea_id`. The project explorer openable resolver should understand this id shape and return a descriptor with `preferred_tab_component="ideaDetail"`, `tab_id="topic-<topic_id>-idea-<idea_id>"`, and detail URLs for idea detail and graph context.

Alternative considered: continue opening the latest realization record tab. That loses the user's intent because a Research Idea can have multiple realizations and lineage edges, and it makes copy/view JSON actions feel like record internals instead of idea inspection.

### Add a dedicated idea detail read endpoint

Add `GET /api/topics/{topic_id}/ideas/{idea_id}`. The endpoint should be read-only, topic-scoped, and backed by canonical Workspace Runtime idea tables plus existing record detail helpers. Its payload should include the canonical idea, realization history, latest realization, latest record summary/detail when available, source JSON payload or source JSON fragment when resolvable, source digest/path metadata, lineage in/out refs when cheap, sibling group metadata when available, and diagnostics.

Alternative considered: compose the detail entirely in the frontend from graph export, record detail, siblings, facets, and lineage endpoints. That would duplicate resolution rules across panels and make missing JSON diagnostics inconsistent. A dedicated endpoint keeps idea-specific source selection in the backend while leaving Markdown generation in the frontend.

### Keep JSON-to-Markdown generation in the frontend

The frontend should create a small local MDAST builder module, for example `web/ui/src/markdown-doc.ts`, that turns arbitrary JSON into typed MDAST nodes and serializes them with `mdast-util-to-markdown`. The first renderer should map object keys to headings by nested level, arrays to lists or GFM tables when items are shape-compatible, primitive values to paragraphs or list items, and unsupported or oversized subtrees to fenced JSON code nodes.

Alternative considered: render Markdown from Python/Jinja on the backend. Jinja is good for known reports, but this viewer needs interactive client-side preview, copy Markdown, copy JSON, and fast iteration across evolving JSON shapes. MDAST also keeps Markdown syntax escaping and serialization in a Markdown library instead of handwritten strings.

### Adopt deterministic JSON preview policies

The Markdown preview should show human-facing idea content first and place ids, digests, locators, provenance refs, and other system metadata in a collapsed or visually secondary `Metadata` section. Arrays of scalar values should render as lists. Arrays of objects should render as GFM tables only when every row has the same scalar keys; mixed, deep, or incompatible arrays should render as nested sections or fenced JSON code blocks.

Alternative considered: render all metadata inline and table any array of objects. That produces noisy previews for research records and makes large or irregular payloads brittle, while the user still has exact JSON access through the modal.

### Use latest realization as preview source

The backend should choose the JSON preview source in this order: latest Idea Realization `source_json_path`, latest realization record payload, then Research Idea source metadata. The idea detail tab should use that selected latest realization for the Markdown preview and show realization history as side metadata with record links.

Alternative considered: merge all realization payloads into one preview document. That hides which record is current and makes copied Markdown ambiguous.

### Cap default source JSON payloads

The idea detail endpoint should return exact source JSON by default only up to a fixed 1 MiB serialized JSON cap. If the source JSON exceeds that cap, the default response should return source metadata, omit the full JSON body, include a `source_json_truncated` diagnostic, and expose an explicit full-fetch option such as `include_source_json=true` for the JSON modal or copy action.

Alternative considered: always return full JSON by default. That is simpler but risks making graph-to-detail navigation slow for large experiment or paper artifacts.

### Use `react-markdown` only for rendering the generated Markdown

The existing `MarkdownView` remains the rendering surface. The new idea detail panel should feed it the serialized Markdown string from the MDAST renderer. This keeps rendering behavior, GFM, math, Mermaid handling, and styling consistent with record Markdown tabs.

Alternative considered: create a second preview renderer directly from React nodes. That would make copy Markdown harder and create two document interpretations.

### Use a modal overlay for raw JSON

The JSON viewer should be an in-app modal overlay with a darkened backdrop, focus trapping or at least focus return to the trigger, Escape close, explicit close button, formatted JSON in a scrollable code region, and copy JSON action. It should not use `window.open`.

Alternative considered: show JSON in another Dockview tab. That is useful later for large JSON documents, but UC-02 specifically asks for a blocking album-style modal so the user can verify exact content without losing the idea detail context.

## Risks / Trade-offs

- Large JSON payloads could make MDAST generation or modal rendering slow → Return full JSON by default only under the 1 MiB cap, gate expensive work to the open idea tab, add bounded preview behavior, keep explicit full JSON fetch available, and add virtualization later if Playwright or manual testing shows slowdown.
- Generic nested-key rendering can produce awkward documents → Keep the renderer small and deterministic now, then add schema-specific renderers for Research Ideas, experiments, decisions, analyses, and papers using the same MDAST builder.
- Copy actions depend on the browser Clipboard API → Show explicit success/failure status and keep visible content selectable when copy fails.
- Source JSON may be missing or stale for older records → Return read-only diagnostics from the backend and disable JSON actions when exact JSON is unavailable.
- Adding MDAST packages increases frontend dependency surface → Keep dependencies narrow to `mdast-util-to-markdown`, GFM/frontmatter utilities, and `unist-builder`, with unit tests around serialization.

## Migration Plan

1. Add frontend dependencies and update lockfiles.
2. Add backend idea detail read model and route without changing existing record routes.
3. Add `idea:` openable descriptors and graph-click routing while preserving record open behavior for non-idea nodes.
4. Add MDAST JSON-to-Markdown helper, idea detail panel, JSON modal, and copy actions.
5. Add unit tests for backend payload resolution, openable descriptors, MDAST rendering, modal/copy behavior, and graph node routing.
6. Add a Playwright smoke check against the flash-attention topic idea-lineage view.

Rollback is simple because the change is additive: remove the new route, openable item shape, `ideaDetail` panel, and frontend dependency additions. Existing graph, record detail, and Markdown rendering flows remain intact.

## Resolved Defaults

- Metadata fields render in a collapsed or visually secondary `Metadata` section, while human-facing idea content stays first.
- Arrays of objects render as GFM tables only when all rows share the same scalar keys; scalar arrays render as lists; mixed or deep arrays render as nested sections or fenced JSON.
- The backend returns exact source JSON by default up to a 1 MiB serialized JSON cap and requires an explicit full-fetch flag for larger payloads.
