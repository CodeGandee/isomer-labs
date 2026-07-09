## 1. Toast Foundation

- [x] 1.1 Add a local toast UI component/provider using the existing Radix/shadcn-compatible frontend stack.
- [x] 1.2 Add an app-level notification API for transient messages with title, optional description, and tone/severity.
- [x] 1.3 Wrap the Project Web root with the toast provider and render a fixed toast viewport.
- [x] 1.4 Enforce a maximum of five simultaneously visible toast notifications in the provider.

## 2. Notification Routing

- [x] 2.1 Move topic overview copy Markdown and copy JSON feedback from local status badges to toast notifications.
- [x] 2.2 Move idea detail copy Markdown and copy JSON feedback from local status badges to toast notifications.
- [x] 2.3 Move record detail copy Markdown, copy JSON, and copy filepath feedback from local status badges to toast notifications.
- [x] 2.4 Preserve inline durable metadata, diagnostics, missing-content warnings, selected-item state, and loading/empty states.
- [x] 2.5 Remove obsolete component-local copy-status state and CSS selectors that only supported transient status badges.

## 3. Accessibility and Styling

- [x] 3.1 Give toast notifications live-region semantics suitable for non-blocking operation feedback.
- [x] 3.2 Ensure toast appearance uses existing Project Web theme tokens in light, dark, and system-derived modes.
- [x] 3.3 Ensure toast viewport placement does not cover primary toolbar controls, JSON modal actions, or mobile navigation controls in normal viewports.
- [x] 3.4 Keep focus on the initiating control or active dialog flow when a toast appears.

## 4. Tests and Verification

- [x] 4.1 Add provider-level tests for toast rendering, dismissal, and the five-visible-toast cap.
- [x] 4.2 Update topic overview, idea detail, and record detail tests to expect toast feedback instead of copy-status badges.
- [x] 4.3 Add or update accessibility-oriented assertions for toast live-region behavior and focus preservation where feasible.
- [x] 4.4 Run focused frontend tests for the changed panels and toast provider.
- [x] 4.5 Run `npm run build` for packaged frontend static assets.
- [x] 4.6 Run `openspec validate use-toast-notifications --strict`.
