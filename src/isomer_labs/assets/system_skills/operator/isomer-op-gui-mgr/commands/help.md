# GUI Manager Help

## Workflow

1. Print a concise description of `isomer-op-gui-mgr` as the operator owner for Project Web GUI lifecycle guidance, backend API reference, refresh, and troubleshooting.
2. List the public subcommands `help`, `launch`, `status`, `api-reference`, `refresh-records`, and `troubleshoot`.
3. Name the canonical launch command `isomer-cli project web serve --root <project-root>`.
4. State that GUI Backend APIs read Project and Topic data, while index rebuild and cleanup are explicit mutation routes.
5. Report the supported output fields and guardrails.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded GUI Manager help response from the subcommands and guardrails, then recommend one safe subcommand or ask for the missing decision.

## Public Subcommands

| Subcommand | Purpose | Typical Result |
| --- | --- | --- |
| `launch` | Start or restart the local GUI Backend. | Command, URL, cache mode, blockers. |
| `status` | Inspect `/api/health` or explain the status check route. | Project root, cache mode, HTTP health summary. |
| `api-reference` | Show backend API route families. | Read-only routes, explicit mutation routes, contract docs pointer. |
| `refresh-records` | Refresh visible GUI data or query-index state safely. | Refresh type, recent errors, validation or maintenance action. |
| `troubleshoot` | Diagnose slow loads, cache issues, stale data, or unsupported views. | Diagnostic path, owner route, next action. |

## Output Guidance

Essential Output naturally summarizes the outcome, Project, GUI surface, cache posture, important commands or routes, diagnostics, blockers, and next action.

Complete Output adds resolved Project root, selected topic, backend process command, route family, response summary, cache headers, recent-errors summary, index action, diagnostics, and handoff route.
