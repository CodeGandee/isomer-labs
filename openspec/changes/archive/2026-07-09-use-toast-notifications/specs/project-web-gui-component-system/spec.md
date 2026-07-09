## ADDED Requirements

### Requirement: Toast component foundation
The Project Web GUI SHALL provide a local toast component and provider as part of its shared component system.

#### Scenario: Toast uses local component source
- **WHEN** the GUI implements app-level toast notifications
- **THEN** the implementation uses a local copied shadcn/Radix-compatible component or an Isomer wrapper around one
- **AND** the implementation does not add a new toast library dependency when the existing frontend stack can provide the primitive

#### Scenario: Toast provider wraps Project Web
- **WHEN** the Project Web frontend starts
- **THEN** an app-level toast provider and viewport are available to panels, dialogs, and shared action handlers that need transient feedback

#### Scenario: Toast styling follows GUI tokens
- **WHEN** a toast is shown in light, dark, or system-derived theme mode
- **THEN** it uses the existing Project Web token system for background, foreground, border, focus, destructive/error, and success or neutral feedback styling
