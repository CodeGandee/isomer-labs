---
name: isomer-op-gui-mgr
description: Use when a Project Operator needs to start, inspect, refresh, debug, or troubleshoot the Project Web GUI, choose GUI cache mode, or look up GUI Backend API route families.
---

# Isomer Operator GUI Mgr

## Overview

Use this command-style operator skill as the Project Web GUI owner workflow. It keeps GUI Backend lifecycle guidance, GUI Renderer troubleshooting, backend API route reference, and safe refresh or query-index maintenance separate from Project and Topic repair workflows.

## When to Use

Use this skill when the user asks how to start, restart, inspect, refresh, debug, or troubleshoot the Project Web GUI; when they need normal versus debug cache-mode guidance; when they ask what backend APIs the GUI uses; or when they need recent-errors, graph, timeline, record, rendered Markdown, or query-index troubleshooting.

Do not use this skill for Project initialization, Project cleanup, Topic Workspace storage repair, package mutation, Topic Actor management, research record schema design, or GUI code changes. Route those to `isomer-op-project-mgr`, `isomer-op-topic-mgr`, the selected research-record owner workflow, or normal repository development work.

## Workflow

When this skill is invoked, execute the following steps in order.

1. **Default help mode**: If invoked without a prompt, select `help`, load [commands/help.md](commands/help.md), and report its output.
2. **Resolve GUI intent**. Decide whether the user needs lifecycle launch, status inspection, backend API reference, refresh or query-index maintenance, or troubleshooting.
3. **Select one subcommand** from the **Subcommands** table.
4. **Load only the selected command page** and execute that page's workflow for one bounded GUI operation.
5. **Preserve owner boundaries**. Route Project configuration repair to `isomer-op-project-mgr`, initialized-topic storage or environment repair to `isomer-op-topic-mgr`, and code-level GUI defects to repository development work.
6. **Report the GUI Manager result** using **Essential Output** by default and **Complete Output** when requested.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the Project Web CLI surface, backend API route families, owner boundaries, output contract, and guardrails in this skill, then execute the plan or report the missing decision.

## Subcommands

| Subcommand | Use For | Detail |
| --- | --- | --- |
| `help` | Print what this skill does, supported GUI routes, outputs, and guardrails | [commands/help.md](commands/help.md) |
| `launch` | Start or restart the local GUI Backend and choose normal or debug cache mode | [commands/launch.md](commands/launch.md) |
| `status` | Inspect whether a running GUI Backend responds and which Project/cache mode it serves | [commands/status.md](commands/status.md) |
| `api-reference` | Show current Project Web GUI Backend API route families and read/write posture | [commands/api-reference.md](commands/api-reference.md) |
| `refresh-records` | Refresh GUI data safely through browser refresh, events, recent-errors, index validation, rebuild, or cleanup | [commands/refresh-records.md](commands/refresh-records.md) |
| `troubleshoot` | Diagnose slow loads, stale assets, cache confusion, unsupported graph scopes, record viewer problems, or non-interpretable data | [commands/troubleshoot.md](commands/troubleshoot.md) |

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

State whether the GUI was launched, inspected, refreshed, diagnosed, routed, blocked, or unchanged. Name the Project when known and provide the relevant service URL, command, HTTP route family, or browser surface. Summarize cache posture, actions taken, health or index observations, blockers, and the next operator action.

### Complete Output

When requested, include:

- **Project and service**: resolved Project root, selected topic, backend process command, host, port, service URL, and cache mode.
- **HTTP evidence**: route family, URL path, status or response summary, cache headers, Server-Timing, and diagnostic payload summary.
- **GUI refresh evidence**: browser refresh posture, event stream posture, recent-errors summary, index validation result, rebuild or cleanup action, and truncation or stale-data diagnostics.
- **Routing evidence**: owner-boundary decision, handoff route, code-defect note, commands run, and next operator action.

## Guardrails

Use `isomer-cli project web serve --root <project-root>` as the canonical start command. Installed operators must invoke the global `isomer-cli` executable directly, not a repo-local Pixi wrapper for Isomer's own CLI.

Treat the GUI Backend as a local single-user service for one selected Project root per process. This skill does not provide daemon, supervisor, remote deployment, authentication, or process-manager authority.

Use normal cache mode for ordinary launches. Use debug cache mode when frontend or backend changes might be hidden by browser cache, because debug mode applies no-store behavior to the GUI shell, static assets, and API responses.

Treat GUI Backend APIs as read surfaces unless a route is explicitly an index maintenance action. Index rebuild and cleanup are explicit user-triggered operations; frontend refresh is not canonical record repair.

Do not claim that the GUI Backend owns canonical research state. It reads Project, Topic Workspace, Workspace Runtime, query-index, and payload-file state; canonical state stays in those owners.

Route invalid Project configuration to `isomer-op-project-mgr`. Route initialized-topic storage, package/environment, reset checkpoint, or Topic Actor problems to `isomer-op-topic-mgr`. Report record schema defects or GUI code defects as repository development work.

## Common Mistakes

- Treating `project web serve` as a daemon lifecycle manager. It starts the local service; status, stop, restart, and logs are currently handled by the user's process environment unless this skill inspects `/api/health`.
- Restarting repeatedly in normal cache mode while debugging frontend assets. Use `--cache-mode debug` when cache interference is plausible.
- Treating browser refresh as data repair. Use recent-errors and index validation to distinguish stale UI state from non-interpretable records or stale query-index rows.
- Listing backend API routes as schemas. Detailed GUI payload expectations live in `docs/ui/contracts/`.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
