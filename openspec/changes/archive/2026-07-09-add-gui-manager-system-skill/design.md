## Context

Project Web is now a visible operator surface: `isomer-cli project web serve` starts a Project-scoped GUI Backend, serves the GUI Renderer, exposes read APIs, supports normal and debug cache modes, and offers explicit record-index maintenance endpoints. Existing operator skills cover Project lifecycle, topic creation, initialized-topic storage, Topic Actors, toolbox management, and team specialization. None of those skills should become a long-lived manual for GUI lifecycle, backend route families, cache behavior, or UI troubleshooting.

The new skill should live in the active operator namespace as `isomer-op-gui-mgr`. It should be installed with the core packaged system skills and should route GUI questions through a user-facing operator workflow, while keeping canonical Project Web behavior in code and docs.

## Goals / Non-Goals

**Goals:**

- Add a core bundled operator skill named `isomer-op-gui-mgr`.
- Teach operators how to start, inspect, restart, and diagnose the GUI Backend.
- Explain normal versus debug cache modes and when to use each.
- Provide a backend API reference for the current Project Web route families.
- Provide safe refresh and maintenance guidance for record lists, graph/timeline data, recent errors, and query-index operations.
- Make the skill discoverable from both `isomer-op-entrypoint` and `isomer-op-welcome`.
- Keep GUI operation requests out of unrelated Project Manager and Topic Manager skill pages except for route handoffs.

**Non-Goals:**

- Change Project Web backend behavior or add new HTTP endpoints.
- Add a process supervisor, daemon manager, or remote deployment flow.
- Make the GUI Backend canonical research state.
- Replace Project, Topic, Workspace Runtime, or record-query CLI docs.

## Decisions

1. Name the skill `isomer-op-gui-mgr`.

   The skill is user-facing and operational, so it belongs in the `isomer-op-<purpose>` namespace. `gui-mgr` is short, matches the existing `project-mgr`, `topic-mgr`, and `toolbox-mgr` pattern, and keeps the scope broader than only `web-serve`.

   Alternative considered: `isomer-op-web-mgr`. That matches the CLI group but hides the domain terms GUI Backend and GUI Renderer, which are the user-facing concepts in the manual.

2. Make the skill command-style with bounded reference pages.

   The top-level `SKILL.md` should route to reference pages such as `help`, `launch`, `status`, `api-reference`, `refresh-records`, and `troubleshoot`. Each page should stay small and name the commands or API route families it owns. This mirrors other operator skills and lets agents load only the page they need.

   Alternative considered: one long `SKILL.md`. That would be easy to create but hard for agents to use without reading stale or irrelevant sections.

3. Treat API reference as descriptive operator guidance.

   The skill should list current backend route families, including health, Project summary, topics, explorer/openable descriptors, runtime, overview, actors, records, record detail, idea detail, graphs, recent errors, events, rendered Markdown, files, facets, and index maintenance. It should not duplicate every response schema when `docs/ui/contracts/` owns GUI payload contracts.

   Alternative considered: embed full OpenAPI-like schema text in the skill. That would quickly drift from the FastAPI implementation and UI contract docs.

4. Keep lifecycle management local and explicit.

   The launch guidance should use `isomer-cli project web serve --root <project-root>` and document `--host`, `--port`, `--reload`, `--no-browser`, and `--cache-mode normal|debug`. It should treat restart as a user or shell process action rather than a hidden daemon mutation.

   Alternative considered: add skill-specific supervisor commands. That would expand product behavior beyond the requested system skill and should be designed separately if needed.

5. Route through existing owners for non-GUI repairs.

   GUI Manager can diagnose stale records, cache issues, invalid Project roots, unsupported graph scopes, recent errors, and index maintenance needs. Project initialization belongs to `isomer-op-project-mgr`, initialized-topic storage repair belongs to `isomer-op-topic-mgr`, and canonical backend/API code changes belong to normal repository development workflows.

   Alternative considered: let GUI Manager repair Project and Topic state directly. That would duplicate existing operator owners and blur safety boundaries.

6. Add GUI Manager to both informed routing and welcome routing.

   `isomer-op-entrypoint` should route concrete GUI tasks through `references/system-skill-index.md`, because that skill is the route-and-proceed dispatcher. `isomer-op-welcome` should also list GUI Manager in `help`, `show-options`, `choose-path`, and `show-skill-map`, because users browsing the system should be able to discover GUI lifecycle and backend API guidance without already knowing the skill name.

   Alternative considered: update only the entrypoint. That would work for informed users, but the welcome menu would still hide the GUI route from first-time or option-browsing users.

## Risks / Trade-offs

- API route guidance can drift from `src/isomer_labs/web/app.py`. Mitigation: add tests or validation that the API reference mentions the current route families, and keep full payload contracts in `docs/ui/contracts/`.
- Users may expect the skill to kill or restart processes automatically. Mitigation: make lifecycle guidance explicit about start commands, foreground processes, and safe restart steps without claiming daemon control.
- GUI refresh guidance may be confused with canonical record repair. Mitigation: distinguish frontend refresh, read-only recent-errors inspection, query-index validation, and explicit rebuild/cleanup actions.
- Adding another core skill increases install surface. Mitigation: keep the skill small, routeable, listed in both welcome and entrypoint routing, and focused on GUI operations that do not fit existing managers.

## Migration Plan

Add the skill directory, register it in the core packaged system-skill manifest, update entrypoint and welcome routing references, and update tests. Existing installs will see the skill after reinstalling or updating packaged system skills through the existing system-skills installation flow.

## Open Questions

- None.
