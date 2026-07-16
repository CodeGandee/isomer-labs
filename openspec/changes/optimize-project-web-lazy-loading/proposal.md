# Change: Optimize Project Web Lazy Loading

## Why

Project Web takes about 53 seconds to show its Explorer and 68 seconds to show the Idea Graph for the `flash-attention-4-whitebox-runtime-model` topic. The browser transfers only about 532 KB, so the delay comes from repeated backend validation, callback-catalog parsing, and heavyweight event polling rather than network volume.

The workbench should show its shell promptly, reuse validated Project state, and fetch each viewer resource only when an open panel needs it. Topic change detection must remain cheap enough that it cannot block unrelated API requests.

## What Changes

- Reuse an unchanged validated Project state across read requests and invalidate it when relevant Project configuration changes.
- Parse the packaged system-skill callback insertion-point catalog once per process and avoid loading the same callback registry twice in one validation pass.
- Make Project Explorer startup return a lightweight skeleton, with deeper topic data loaded only when the user expands or opens the corresponding surface.
- Activate frontend queries only for mounted or explicitly opened surfaces, while preserving lightweight descriptor-first navigation.
- Replace graph-export work in topic event polling with a lightweight revision read and keep blocking filesystem or database work off the asynchronous event loop.
- Add regression and browser tests that guard request timing, request scope, cache invalidation, and unchanged functional results.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `project-web-gui`: Make the local GUI shell and selected viewer available without repeated full Project validation, with explicit cache invalidation and bounded startup work.
- `project-web-state-management`: Activate backend queries according to mounted panel and navigation demand instead of starting unrelated reads eagerly.
- `project-web-explorer-read-api`: Keep the initial Explorer response lightweight and resolve deeper topic branches only on expansion or opening.
- `project-web-research-viewer`: Fetch viewer content, supporting payloads, and expensive modules only when the relevant open tab or user action needs them.
- `project-web-idea-graph-refresh`: Detect index revisions through a lightweight, non-blocking event path that avoids full graph export work.

## Impact

The change affects `src/isomer_labs/web/`, Project and callback validation helpers, `web/ui/` query orchestration, and their Python and browser tests. Read semantics, diagnostics, explicit maintenance boundaries, URL restoration, and callback target validation remain unchanged.
