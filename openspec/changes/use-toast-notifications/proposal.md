## Why

Project Web currently reports transient actions such as copy success by adding temporary text into status rows, which mixes durable metadata with momentary feedback. Toast notifications give users consistent, accessible feedback without changing the meaning or layout of detail panels.

## What Changes

- Add a Project Web toast notification surface for transient GUI feedback.
- Route copy success, copy failure, refresh notices, and similar short-lived GUI notifications through toast notifications instead of status badges or inline tags.
- Cap simultaneously visible toasts at five; additional notifications replace or evict older toasts rather than growing an unbounded stack.
- Preserve durable warnings, diagnostics, selected-item metadata, and record/idea status as inline UI where those messages are part of the page state.
- Use the existing Radix/shadcn-style frontend component stack rather than adding a new toast dependency.

## Capabilities

### New Capabilities

- `project-web-toast-notifications`: Defines app-level toast behavior, notification routing, visible-toast limits, accessibility expectations, and transient versus durable message boundaries.

### Modified Capabilities

- `project-web-gui-component-system`: Extends the shared GUI component foundation to include a local toast component/provider built from the existing Radix/shadcn-compatible stack.

## Impact

- Affected frontend: shared UI components, top-level Project Web provider wiring, copy/refresh handlers, JSON modal copy feedback, topic overview, idea detail, and record detail panels.
- Affected tests: frontend component tests that currently assert inline copy-status badges, plus new toast queue and accessibility coverage.
- Affected docs/specs: Project Web GUI component-system contract and notification behavior.
- No backend API, storage, or data migration is expected.
