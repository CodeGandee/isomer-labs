# Troubleshoot GUI

## Workflow

1. Classify the symptom: service will not start, service unavailable, slow load, stale assets, stale data, unsupported graph scope, record viewer problem, non-interpretable idea or timeline data, or code defect.
2. For service availability, inspect launch command, host, port, terminal process, and `/api/health`.
3. For stale assets or debugging confusion, recommend restart with `--cache-mode debug`.
4. For stale data, distinguish browser refresh, GUI panel refresh, topic change events, recent-errors diagnostics, and index validation.
5. For unsupported graph scopes, explain that Project Web no longer serves removed dense graph scopes and route to supported Idea Graph or Idea Timeline views.
6. Route invalid Project configuration to `isomer-op-project-mgr`, initialized-topic storage or environment repair to `isomer-op-topic-mgr`, and code-level GUI defects to repository development work.
7. Report symptom, evidence, likely cause, diagnostics, blockers, owner route, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a troubleshooting plan from the symptom, Project Web routes, cache-mode behavior, recent-errors diagnostics, and owner boundaries, then execute the plan or ask for the missing evidence.

## Symptom Map

| Symptom | First Check | Usual Next Action |
| --- | --- | --- |
| Browser cannot connect | Host, port, foreground process, `/api/health` | Start `isomer-cli project web serve --root <project-root>` or use the correct tunnel URL. |
| UI shows old assets | Cache mode and browser cache | Restart with `--cache-mode debug`, then hard refresh. |
| API data seems stale | GUI panel refresh and `/api/events` | Refresh visible panel, then validate index if records are stale. |
| Graph or timeline cannot interpret data | `/api/topics/{topic_id}/recent-errors` | Inspect recent errors and route data repair to the owning workflow. |
| Old dense graph URL fails | Graph scope | Use Idea Graph or Idea Timeline; removed scopes should not render. |
| Record detail or Markdown fails | record viewer, render, files, and facets routes | Inspect route response and route schema or code defects to development work. |

## Diagnostics Boundary

Recent errors are bounded service-local diagnostics. They help explain current GUI interpretation failures, but they are not durable Workspace Runtime records and are cleared by service restart.
