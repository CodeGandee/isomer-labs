# Refresh Records

## Workflow

1. Classify the refresh need as browser refresh, debug cache restart, topic change event wait, recent-errors inspection, index validation, explicit rebuild, or explicit cleanup.
2. Use browser refresh or the GUI's Refresh action first when the user only needs to reload visible data.
3. Use `--cache-mode debug` restart when changed frontend assets or API behavior may be hidden by browser cache.
4. Query `/api/topics/{topic_id}/recent-errors` for non-interpretable graph, timeline, idea, or record data.
5. Use `GET /api/topics/{topic_id}/records/index/validate` before mutation when query-index staleness is suspected.
6. Use explicit rebuild or cleanup routes only when the user requests index maintenance or validation evidence shows derived index rows need maintenance.
7. Report the selected refresh type, routes used, diagnostics, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a refresh plan from the GUI surface, recent-errors route, and index maintenance boundaries, then execute the plan or report the missing topic id.

## Refresh Types

- Browser refresh: reloads the GUI Renderer and current API data.
- GUI Refresh button: refetches the current panel's API data.
- Topic change events: `/api/events` can notify the frontend that topic data changed.
- Debug cache restart: relaunch with `isomer-cli project web serve --root <project-root> --cache-mode debug`.
- Recent errors: `GET /api/topics/{topic_id}/recent-errors` returns bounded service-local diagnostics.
- Index validation: `GET /api/topics/{topic_id}/records/index/validate` checks derived query-index state without mutation.
- Index rebuild: `POST /api/topics/{topic_id}/records/index/rebuild` refreshes derived query-index rows from canonical records and payload files.
- Index cleanup: `POST /api/topics/{topic_id}/records/index/cleanup` previews or applies cleanup of derived query-index rows according to the request body.

## Boundaries

Frontend refresh and debug cache mode do not repair canonical records. Query-index rebuild and cleanup affect derived index state only. Record schema or payload interpretation defects should be reported as data or code defects and routed to the owner workflow.
