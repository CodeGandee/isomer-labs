## Why

The project web GUI feels slow over remote access because it serves large JavaScript, CSS, and JSON responses without compression while also disabling browser caching for every response. Debug no-cache behavior is still useful during frontend iteration, so the service needs separate normal and debug launch modes instead of one global cache policy.

## What Changes

- Add an explicit backend launch cache mode for the project web service: normal launch follows ordinary production practices, while debug launch keeps no-store behavior so browser cache cannot hide frontend changes.
- Serve packaged frontend assets with production-friendly caching and compression in normal launch, including cacheable hashed assets and a fresh-enough HTML shell that points at current assets.
- Keep debug launch cache-busting behavior for HTML, static assets, and API responses.
- Reduce initial GUI data transfer by making topic overview and records list endpoints return lightweight projections by default, with raw JSON and richer detail fetched only when the user asks for it.
- Code-split heavy frontend viewers so graph, layout, markdown diagram, and detail-preview dependencies do not all load before the shell becomes usable.
- Add validation hooks for load behavior, response sizes, and cache headers so future GUI changes do not silently reintroduce large uncached first-load payloads.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `project-web-gui`: Define normal versus debug project web launch behavior, cache/compression headers, frontend asset serving, and lighter research-record list responses.
- `project-web-topic-overview`: Make the topic overview API truly load overview content first and defer topic/runtime JSON until requested.
- `project-web-research-viewer`: Require heavy viewer modules and tab resources to load on demand instead of as part of the initial shell.

## Impact

- Backend project web service launch options, app factory configuration, static file serving, cache headers, and compression middleware.
- Project web API contracts for topic overview and research-record list/detail payloads.
- Vite build output naming and frontend lazy-loading boundaries.
- Frontend tests, backend unit tests, and Playwright or equivalent performance smoke checks.
