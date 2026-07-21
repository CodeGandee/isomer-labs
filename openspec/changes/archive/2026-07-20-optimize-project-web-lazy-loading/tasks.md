## 1. Validation Hot Path

- [x] 1.1 Cache immutable parsed system-skill catalog structures and add insertion-point lookup coverage.
- [x] 1.2 Reuse callback registry load results within one Project validation pass and preserve duplicate-id diagnostics.

## 2. Reusable Project Read Context

- [x] 2.1 Add a thread-safe Project state and topic-context cache with configuration revision invalidation.
- [x] 2.2 Make collapsed Explorer topics manifest-derived and resolve only requested expanded topic branches.
- [x] 2.3 Add unit coverage for concurrent state reuse, configuration invalidation, and lazy Explorer resolution.

## 3. Lightweight Topic Events

- [x] 3.1 Add a revision-only query-index read that does not export graph or record content.
- [x] 3.2 Route topic change events through the revision-only read and offload synchronous polling from the ASGI event loop.
- [x] 3.3 Add event tests for revision payloads, duplicate suppression, and concurrent health responsiveness.

## 4. Demand-Driven Frontend

- [x] 4.1 Bootstrap Project root and topic selection from URL and Explorer data without eager Project and Topics requests.
- [x] 4.2 Keep deep-linked descriptor and panel queries independent from Explorer completion.
- [x] 4.3 Add frontend tests that assert unopened overview, runtime, actor, record, and detail surfaces do not issue requests.

## 5. Verification

- [x] 5.1 Run focused Python and frontend tests, lint, type checking, and strict OpenSpec validation.
- [x] 5.2 Rebuild packaged frontend assets and confirm the reference Idea Graph timing with Playwright.
- [x] 5.3 Audit every proposal requirement and mark the implementation checklist complete only with evidence.
