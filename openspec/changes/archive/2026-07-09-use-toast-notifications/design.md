## Context

Project Web has several Markdown-first detail surfaces with copy and refresh actions. Today these transient action results are kept in local component state and rendered as `StatusBadge` tags inside status rows. That makes short-lived messages such as `Filepath copied.` look like durable record metadata, and it can shift or crowd the content users are trying to inspect.

The frontend already uses local shadcn-style components backed by Radix primitives, and `radix-ui` already brings `@radix-ui/react-toast` through the installed dependency graph. The change can therefore add a local toast component and notification provider without introducing a new dependency.

## Goals / Non-Goals

**Goals:**

- Provide one app-level toast notification surface for transient GUI feedback.
- Route copy success, copy failure, refresh completion/failure, and similar short-lived operation feedback through toast notifications.
- Cap simultaneously visible toasts at five.
- Keep durable diagnostics, record/idea metadata, selection state, and warnings inline where users can inspect them after the toast disappears.
- Use local Isomer-owned UI wrapper components consistent with the existing shadcn/Radix component system.

**Non-Goals:**

- Add a backend notification service, persistence, or event stream.
- Replace inline validation errors, query diagnostics, missing-data warnings, or status badges that describe current page state.
- Add a new third-party toast library such as `sonner`.
- Redesign all status rows or diagnostic panels.

## Decisions

1. Add a local toast component/provider using the existing Radix/shadcn-compatible stack. This matches the current `components/ui/*` pattern, keeps source reviewable inside the repo, and avoids a new dependency. Alternative considered: use browser alerts or a custom absolute-positioned div. That would weaken accessibility and duplicate behavior Radix already provides.

2. Expose a small application notification API such as `notify({ title, description, tone })` through context or a lightweight hook. Copy handlers and refresh handlers should call this API instead of maintaining local copy-status state for transient feedback. Alternative considered: keep each panel responsible for its own toast state. That would preserve the current duplication and make the five-toast cap harder to enforce.

3. Enforce the five-toast cap at the provider boundary. The provider owns the queue and visible list; when a sixth toast is added, it evicts the oldest visible toast or otherwise trims the list to five. Alternative considered: ask each caller to limit its own messages. That scatters policy across the app and will fail as new notifications are added.

4. Treat toast notifications as transient operation feedback only. Durable user-facing state remains inline: diagnostics warnings, missing overview messages, selected idea/record metadata, loading or empty states, and validation errors stay in the relevant panel. Alternative considered: move all warnings to toast. That would make important research data problems disappear too quickly.

5. Keep tests at the user-observable boundary. Tests should assert that copy actions show toast feedback and no longer add copy-status badges to detail status rows. Provider tests should assert the visible-toast limit and dismissal behavior. Alternative considered: only snapshot the provider internals. That would miss regressions in the actual detail panels.

## Risks / Trade-offs

- [Risk] Toasts could hide important diagnostics. Mitigation: route only transient operation feedback to toast; keep durable diagnostics inline.
- [Risk] A burst of copy actions could flood the screen. Mitigation: enforce a five-visible-toast cap in the provider.
- [Risk] Tests that search for copy messages will still pass even if messages move to a toast portal. Mitigation: update tests to verify toast container semantics and absence from status rows where practical.
- [Risk] Toast portal styling could overlap Dockview or modal content. Mitigation: place the viewport in a fixed app-level layer with bounded width, responsive offsets, and a z-index above workbench chrome but below blocking modal overlays when appropriate.

## Migration Plan

Implement the toast component and provider, wrap the Project Web app root, move existing transient copy notifications from topic overview, idea detail, record detail, and JSON modal copy actions to the shared notification API, then remove obsolete copy-status badges and state where they only served transient messages. Rebuild static assets and run focused frontend tests plus the normal build. Rollback removes the provider and restores local copy-status state in each panel.

## Open Questions

None.
