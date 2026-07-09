## 1. Backend Launch Modes and Asset Delivery

- [x] 1.1 Add an explicit project web cache mode option for normal and debug launch, with normal as the default and debug preserving no-store behavior.
- [x] 1.2 Thread the selected cache mode through the project web app factory, static asset serving, middleware, and service diagnostics.
- [x] 1.3 Apply normal-mode cache headers that keep the HTML shell fresh while marking content-hashed static assets immutable.
- [x] 1.4 Add response compression for eligible HTML, JavaScript, CSS, and JSON responses above a configured size threshold.
- [x] 1.5 Add backend tests for normal-mode headers, debug-mode no-store headers, compression behavior, and launch-mode visibility.

## 2. Frontend Build and Lazy Loading

- [x] 2.1 Restore content-hashed frontend asset filenames in the packaged Vite build and update any backend assumptions about fixed asset names.
- [x] 2.2 Add lazy-load boundaries for graph viewers, graph layout engines, Markdown diagram rendering, KaTeX rendering, and other heavy detail viewers.
- [x] 2.3 Add loading states for on-demand viewer module loads without blocking shell navigation or lightweight table use.
- [x] 2.4 Update frontend tests for debug asset reload expectations, normal cached asset assumptions where applicable, and lazy viewer loading behavior.
- [x] 2.5 Run frontend build checks and record the resulting initial asset sizes.

## 3. Lightweight API Payloads

- [x] 3.1 Change the topic overview default API response to return overview Markdown, source metadata, and diagnostics without embedding full Topic or Runtime JSON.
- [x] 3.2 Add or reuse an on-demand endpoint/query path for topic overview `View JSON` that returns supporting Topic, Runtime, Source, and Diagnostics JSON.
- [x] 3.3 Update the topic overview frontend so `View JSON` fetches supporting JSON on demand and handles partial or failed JSON fetches inside the modal.
- [x] 3.4 Change records-list APIs to return a table-focused projection by default while preserving rich record detail, rendered Markdown, lineage, files, and facet endpoints.
- [x] 3.5 Update the records table frontend to request bounded list payloads and fetch rich detail data only when a record is opened.
- [x] 3.6 Add backend and frontend tests for overview projection, records projection, record-count limits, and detail/JSON follow-up fetches.

## 4. Performance Observability and Verification

- [x] 4.1 Add request timing, response-size, or `Server-Timing` visibility sufficient to separate backend time from transfer time during GUI performance checks.
- [x] 4.2 Add a Playwright or equivalent smoke check for first shell usability under a remote-like network profile.
- [x] 4.3 Compare normal and debug launch behavior with the existing topic workspace and document the observed asset sizes, response headers, and key API payload sizes.
- [x] 4.4 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, frontend tests, and frontend build checks needed for this change.
