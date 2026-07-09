## ADDED Requirements

### Requirement: Transient GUI notifications use toast
The Project Web GUI SHALL route transient operation feedback through toast notifications instead of rendering that feedback as durable status-row tags or inline metadata.

#### Scenario: Copy success shows toast
- **WHEN** a user copies Markdown, JSON, or an artifact filepath from a Project Web panel or dialog
- **THEN** the GUI shows a toast notification confirming the copy result
- **AND** the GUI does not add the copy-success message as a status badge in the panel metadata row

#### Scenario: Copy failure shows toast
- **WHEN** a user attempts to copy Markdown, JSON, or an artifact filepath and the clipboard write fails or no copyable content exists
- **THEN** the GUI shows a toast notification describing the failure
- **AND** the relevant panel remains usable without crashing

#### Scenario: Durable state remains inline
- **WHEN** the GUI reports selected item metadata, missing content warnings, query diagnostics, validation errors, loading state, empty state, or relationship status
- **THEN** the GUI keeps that durable state in the relevant panel, dialog, table, or diagnostics surface instead of relying only on a toast notification

### Requirement: Toast visibility is bounded
The Project Web GUI SHALL show no more than five toast notifications at the same time.

#### Scenario: Sixth toast is queued or shown
- **WHEN** a user action or system operation creates a sixth toast while five toasts are already visible
- **THEN** the GUI removes or replaces an older visible toast so that no more than five toasts are visible
- **AND** the GUI continues accepting later toast notifications

#### Scenario: Toast can be dismissed
- **WHEN** a toast notification is visible
- **THEN** the user can dismiss it or wait for it to expire
- **AND** dismissal does not affect the underlying Project Web panel state

### Requirement: Toast notifications are accessible
The Project Web GUI SHALL expose toast notifications through accessible live-region semantics appropriate for non-blocking operation feedback.

#### Scenario: Screen reader receives copy feedback
- **WHEN** a copy operation succeeds or fails
- **THEN** assistive technology can receive the notification text without moving focus away from the current control

#### Scenario: Toast does not steal focus
- **WHEN** a toast appears after a toolbar or dialog action
- **THEN** keyboard focus remains on the initiating control or active dialog flow unless the user explicitly moves focus
