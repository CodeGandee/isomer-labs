# GUI Backend API Reference

## Workflow

1. Identify whether the user needs route discovery, read/write posture, payload contracts, or a specific route family.
2. Present the relevant Project Web route families from **Route Families**.
3. Mark read-only route families separately from explicit mutation route families.
4. Point detailed frontend payload questions to `docs/ui/contracts/` rather than duplicating full response schemas.
5. Preserve the canonical-state boundary: the GUI Backend reads Project, Topic Workspace, Workspace Runtime, query-index, and payload-file state; it does not own canonical research state.
6. Report the route family, example paths, read/write posture, contract docs pointer, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a route-reference answer from the current Project Web route families and UI contract docs, then answer or ask for the missing topic or record id.

## Route Families

Read-only service and Project routes:

- `GET /api/health`: health, selected Project root, and cache mode.
- `GET /api/project`: Project summary.
- `GET /api/topics`: registered Research Topics.
- `GET /api/explorer/project`: Project Explorer tree.
- `GET /api/openable/{openable_item_id}`: openable descriptor.

Read-only topic routes:

- `GET /api/topics/{topic_id}`: topic detail.
- `GET /api/topics/{topic_id}/runtime`: Workspace Runtime summary.
- `GET /api/topics/{topic_id}/overview`: rendered topic overview.
- `GET /api/topics/{topic_id}/overview/json`: topic overview supporting JSON.
- `GET /api/topics/{topic_id}/actors`: Topic Actors.

Read-only record and viewer routes:

- `GET /api/topics/{topic_id}/records`: lightweight record list with filters and limit.
- `GET /api/topics/{topic_id}/records/export`: export view data.
- `GET /api/topics/{topic_id}/records/{record_id}`: record detail, optionally including payload JSON.
- `GET /api/topics/{topic_id}/viewer/records/{record_id}`: record viewer descriptor.
- `GET /api/topics/{topic_id}/records/{record_id}/render`: rendered Markdown.
- `GET /api/topics/{topic_id}/records/{record_id}/lineage`: record lineage.
- `GET /api/topics/{topic_id}/records/{record_id}/siblings`: sibling records.
- `GET /api/topics/{topic_id}/records/{record_id}/files`: record files.
- `GET /api/topics/{topic_id}/records/{record_id}/files/{file_id}/content`: file content.
- `GET /api/topics/{topic_id}/records/{record_id}/facets`: record facets.

Read-only graph, idea, diagnostics, and event routes:

- `GET /api/topics/{topic_id}/graphs/{graph_scope}`: graph and timeline read models.
- `GET /api/topics/{topic_id}/ideas/{idea_id}`: idea detail.
- `GET /api/topics/{topic_id}/recent-errors`: bounded service-local recent errors.
- `GET /api/events`: server-sent topic change events.

Explicit mutation routes for query-index maintenance:

- `POST /api/topics/{topic_id}/records/index/rebuild`: explicit query-index rebuild.
- `POST /api/topics/{topic_id}/records/index/cleanup`: explicit query-index cleanup.

Read-only index diagnostic route:

- `GET /api/topics/{topic_id}/records/index/validate`: query-index validation without mutation.

## Payload Contracts

Detailed GUI payload expectations live under `docs/ui/contracts/`. Use those contract pages for frontend-facing response shape questions, and keep this skill focused on route discovery and operator posture.
