# GUI Status

## Workflow

1. Resolve the service URL from the prompt or default to `http://127.0.0.1:8765` when no host or port is supplied.
2. Inspect `/api/health` when the user wants a live status check and network access to the local service is appropriate.
3. Interpret the health payload for `ok`, `project_root`, and `cache_mode`.
4. If the service is unavailable, report whether the likely issue is not running, wrong host or port, remote tunnel, firewall, or invalid Project launch.
5. Route invalid Project configuration to `isomer-op-project-mgr`; do not repair it from this skill.
6. Report status, Project root, service URL, cache mode, diagnostics, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded GUI status plan from `/api/health`, the launch command, and owner boundaries, then execute the plan or report the missing service URL.

## Health Route

Read-only status route:

```text
GET /api/health
```

Expected evidence includes:

- `ok`: service health flag.
- `project_root`: Project root selected when the GUI Backend started.
- `cache_mode`: `normal` or `debug`.

`/api/health` confirms the selected GUI Backend process. It does not validate every Topic Workspace, record, graph, or frontend route.
