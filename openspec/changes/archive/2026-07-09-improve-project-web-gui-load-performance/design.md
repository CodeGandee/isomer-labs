## Context

The project web GUI currently uses one launch behavior for both local development and normal browsing. That behavior applies `Cache-Control: no-store, no-cache, must-revalidate, max-age=0` to static assets and API responses, serves the built JavaScript and CSS without content encoding, and uses stable non-hashed asset names.

Local Playwright and curl checks on the running GUI showed the first-load bottleneck clearly. The main JavaScript asset is about 3.9 MB uncompressed, the CSS asset is about 229 KB uncompressed, and neither receives gzip or Brotli encoding. Under a simulated 5 Mbps and 80 ms connection, the shell became visible after about 7 seconds, with the JavaScript transfer alone taking about 6.7 seconds. CPU time was much smaller than transfer time, so the primary first-load problem is bytes over the wire and the inability to reuse static assets.

Some API payloads are also too large for their initial views. The topic overview response includes runtime payload data even when the user only needs Markdown. The records list response returns rich metadata and path fields for every row, although the table initially needs a smaller projection. These payloads make refresh feel heavier and hide whether a slow interaction comes from backend work, network transfer, or frontend rendering.

## Goals / Non-Goals

**Goals:**

- Split project web launch behavior into normal and debug cache modes.
- Keep debug launch cache-busting semantics for frontend iteration and manual testing.
- Make normal launch use production-style compression and static asset caching.
- Reduce default topic overview and records-list payloads without removing detail or JSON inspection paths.
- Lazy-load heavy frontend modules so the shell is usable before graph, layout, diagram, and detail-preview dependencies load.
- Add validation that makes response size, cache headers, and remote-like load behavior visible during development.

**Non-Goals:**

- Redesign the left-panel navigation or research graph information architecture.
- Change canonical Workspace Runtime record storage or query-index ownership.
- Require an external frontend development server for normal project web browsing.
- Guarantee hard performance budgets for very large future Topic Workspaces before those datasets exist.

## Decisions

### Launch cache mode is explicit

The project web service will accept an explicit cache mode, with normal as the default and debug as the opt-in development mode. Normal launch will use ordinary production practices: compressed responses, immutable caching for content-hashed assets, and a non-stale HTML shell. Debug launch will keep no-store behavior for HTML, assets, and API responses so the browser cannot hide frontend changes.

The main alternative was a single global no-store policy because it is simple and safe during development. That policy made every remote load pay the full transfer cost and prevented the browser from reusing unchanged assets. Another alternative was environment-variable-only behavior, but an explicit CLI option is easier to discover, document, and test.

### Normal launch uses hashed assets and compression

The frontend build will stop forcing fixed output names such as `assets/app.js` for normal packaged assets. Content-hashed JavaScript and CSS assets can receive `Cache-Control: public, max-age=31536000, immutable` because a changed build produces a new URL. The HTML shell will remain no-cache or short-cache so it can point at the newest hashed assets after rebuilds. JSON and static assets will receive gzip compression at minimum when the client advertises support.

The practical first step can use FastAPI/Starlette gzip middleware because it is small and fits the current stack. Precompressed Brotli and gzip assets can follow later if measurements show runtime compression cost matters.

### Initial API responses use view projections

The topic overview endpoint will return overview Markdown, source metadata, and diagnostics by default. Topic and runtime JSON will move to an on-demand path used by `View JSON`. The records list endpoint will return the table projection needed for browsing, filtering, sorting, and opening details. Full metadata, payload JSON, lineage, file facets, and rendered Markdown remain available through detail endpoints.

This keeps existing inspection capability but changes the default read path from "everything the page might ever need" to "what the current view needs now." The frontend can still fetch richer data when the user opens a modal, detail tab, or JSON view.

### Heavy frontend viewers load at use sites

The shell and lightweight tables should not synchronously import graph renderers, graph layout engines, Mermaid, KaTeX, or large Markdown extras before the user opens a view that needs them. The implementation will introduce dynamic imports and suspense/loading states around graph panels, Markdown diagram rendering, and other heavy viewers.

The alternative was to optimize only backend and transfer behavior. That would help remote first load, but the bundle would still grow as new views are added. Lazy boundaries make future heavy viewers cheaper to add.

### Measure the path users feel

Validation will include cache header checks, compressed-response checks, and a Playwright or equivalent smoke test under a remote-like profile. Backend tests should assert that default API responses omit large on-demand fields, while detail and JSON paths still return them. The service should expose enough request timing or size information, through logs or `Server-Timing`, to separate backend time from transfer and frontend rendering during future investigations.

## Risks / Trade-offs

- **Risk: Debug users accidentally run normal launch and see stale assets.** Mitigation: document the debug flag in CLI help and make debug mode visibly reported by the service or diagnostics endpoint.
- **Risk: Hashed asset caching serves stale HTML references after a rebuild.** Mitigation: keep the HTML shell no-cache or short-cache in normal mode and test that it references existing built assets.
- **Risk: Splitting overview and records payloads causes missing data in existing UI paths.** Mitigation: add contract tests for default projections and detail/JSON follow-up fetches, then update the frontend fetch sequence with explicit loading states.
- **Risk: Dynamic imports add brief loading states inside views.** Mitigation: place lazy boundaries at tab or panel boundaries and keep shell navigation responsive while heavy modules load.
- **Risk: Compression adds CPU work on the local backend.** Mitigation: use a response-size threshold, keep it measurable, and consider precompressed assets if runtime compression becomes visible in timings.

## Migration Plan

1. Add the backend cache-mode option with normal as the default and debug preserving the current no-store behavior.
2. Update static asset serving and build output so normal launch can safely cache hashed assets while keeping the HTML shell fresh.
3. Add compression and tests for normal/debug response headers.
4. Change topic overview and records-list APIs to return default projections, then update frontend `View JSON` and detail paths to fetch rich data on demand.
5. Add frontend lazy-load boundaries and build-size checks.
6. Run unit tests, frontend tests, build checks, and a remote-like Playwright smoke measurement.

Rollback is straightforward: run the service in debug cache mode to restore current no-store behavior while keeping the new code paths available for targeted fixes.

## Open Questions

None.
