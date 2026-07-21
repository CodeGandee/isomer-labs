## Context

The measured browser trace for `flash-attention-4-whitebox-runtime-model` transferred about 532 KB, but lightweight API calls completed after roughly 52 seconds. The Idea Graph summary appeared after roughly 68 seconds. A CPU profile showed repeated full Project validation, duplicate callback-registry loads, and repeated TOML parsing of the packaged callback insertion-point catalog.

The frontend starts Project, Topics, Explorer, descriptor, and event requests close together. Each request currently builds its own Project state. The event stream also exports the full graph every two seconds to obtain one index revision, and it runs synchronous work inside the asynchronous stream generator.

The workbench already uses React lazy modules and panel-owned TanStack queries in several places. This change preserves those mechanisms and removes the eager backend work that prevents them from helping startup.

## Goals / Non-Goals

**Goals:**

- Show the Project Web shell, initial Explorer skeleton, and a deep-linked Idea Graph within bounded local startup time.
- Reuse one validated Project state across concurrent and subsequent reads for the same configuration revision.
- Invalidate cached state when Project Web configuration changes or when an explicit refresh clears it.
- Resolve only expanded Explorer topic branches and fetch only mounted viewer data.
- Produce topic events from lightweight index revision metadata without blocking the ASGI event loop.
- Preserve read-only behavior, diagnostics, URL restoration, callback validation, and explicit index maintenance.

**Non-Goals:**

- Do not cache graph, record, or runtime payloads outside TanStack Query.
- Do not watch the 5.4 GB Topic Workspace tree or its `.pixi` environment.
- Do not change Workspace Runtime schemas, callback resolution order, or Project validation rules.
- Do not add a general filesystem watcher or an external cache service.

## Decisions

### Cache Parsed Packaged Catalog Structures

The packaged system-skill manifest is immutable for one installed process. Internal cached helpers will parse it once and retain immutable groups, stages, metadata, insertion points, and a target-stage lookup set. Public manifest loading will preserve caller isolation, while catalog consumers use the cached structures.

This approach replaces caching inside callback validation. The catalog is package-owned, so process-lifetime caching has a precise invalidation boundary: a new package process loads the new resource.

### Reuse Project State Behind a Single-Flight Cache

`ProjectWebReadModel` will own a lock-protected cache for discovery, full validation, and resolved topic contexts. Concurrent cold requests will share one validation pass. Returned diagnostic lists remain request-local so callers cannot append to cached lists.

The cache key will use a deterministic metadata revision over the Project configuration directory and explicit configuration inputs known to the cached Project state. The signature uses paths, existence, file size, and nanosecond modification time. It will not hash file contents or traverse Topic Workspaces.

An explicit cache-clear method will support deterministic tests and future refresh wiring. A changed signature clears resolved topic contexts before the next read.

An alternative was a short time-to-live cache. That would repeat expensive work during a long browser session and could reintroduce periodic CPU stalls. Another alternative was caching every API response, which would risk stale runtime and graph data.

### Treat Collapsed Explorer Topics as Manifest Summaries

The initial Explorer request will build Research Topic nodes from Project Manifest registrations. It will resolve Effective Topic Context only for topic ids supplied as expanded. An expanded request will add that topic's deeper semantic children and resolved metadata.

This keeps the initial tree useful while making its work proportional to visible branches. The openable descriptor path remains independent, so a deep link can open its viewer while the Explorer request is still pending.

### Bootstrap from Explorer and URL State

The workbench will use the initial Explorer response for Project root and topic ids. It will not start separate Project and Topics queries solely to bootstrap the shell. A topic id present in the URL remains immediately authoritative.

Each Dockview panel continues to own its query. Supporting JSON, runtime, actor, record, and detail queries stay disabled until the corresponding panel or action is active.

The alternative was a new combined bootstrap endpoint. The Explorer already carries the required semantic skeleton, so another contract would duplicate data and add migration work.

### Add a Revision-Only Query-Index Read

The records layer will expose a read-only revision operation that opens the Workspace Runtime and computes `index_revision_payload` without selecting graph records or validating every exported row. Topic events will use this operation.

The asynchronous event generator will run the synchronous revision read through a worker thread. A slow filesystem or SQLite call therefore cannot block health checks, assets, or unrelated API handlers on the event loop.

The revision remains uncached because it represents live Workspace Runtime state. The frontend will continue suppressing invalidation when the revision has not changed.

## Risks / Trade-offs

- [A configuration file changes without metadata changing] → Include size and nanosecond modification time, provide explicit invalidation, and cover normal editor replacement and rewrite cases in tests.
- [A caller mutates cached diagnostics] → Store tuples internally and return fresh lists from public read methods.
- [The cache lock serializes cold requests] → The first request performs the required validation once; warm reads hold the lock only for signature comparison and lookup.
- [Revision queries still inspect several SQLite tables] → They perform bounded aggregate queries and avoid graph rows, canonical idea payloads, and source diagnostics.
- [Explorer metadata is less detailed while collapsed] → Resolve and return the richer metadata when the user expands the topic or opens its descriptor.
- [Browser timing varies across hosts] → Keep deterministic unit assertions about work performed, and use the named topic workspace for a manual Playwright acceptance trace.

## Migration Plan

No data migration is required. Deploy the backend and rebuilt frontend assets together. A process restart restores the previous behavior if rollback is needed because all new caches are in memory.

## Open Questions

None. The Playwright acceptance run will confirm whether the five-second Idea Graph target needs further query-index optimization.
