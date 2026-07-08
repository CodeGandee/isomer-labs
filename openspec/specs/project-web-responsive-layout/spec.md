# project-web-responsive-layout Specification

## Purpose
TBD - created by archiving change standardize-project-web-responsive-layout. Update Purpose after archive.
## Requirements
### Requirement: Project Web adapts by viewport and input capability
The Project Web GUI SHALL adapt layout by viewport size, viewport height, pointer precision, hover availability, and safe-area insets rather than by operating system or browser user-agent labels.

#### Scenario: Desktop viewport uses dense workbench layout
- **WHEN** the GUI is opened at a desktop-sized viewport
- **THEN** the Project Explorer can remain visible beside the workbench tab area
- **AND** docked tabs, graph canvases, tables, and detail viewers keep desktop-density controls without text overlap or clipped primary actions

#### Scenario: Phone viewport uses narrow-screen layout
- **WHEN** the GUI is opened at a phone-sized viewport
- **THEN** persistent sidebars collapse into an explicit navigation surface such as a Sheet or full-height drawer
- **AND** the active viewer remains usable without requiring horizontal page scrolling for primary navigation or controls

### Requirement: Responsive shell uses mobile-first layout rules
The Project Web GUI SHALL define mobile-first layout rules and add larger-screen behavior through responsive breakpoints, container bounds, or viewport-relative sizing.

#### Scenario: Layout containers remain bounded
- **WHEN** the viewport is narrower or shorter than the preferred desktop dimensions
- **THEN** dialogs, drawers, panels, and viewer containers fit inside the visible viewport using responsive bounds such as percentages, viewport units, `min()`, `max()`, or `clamp()`
- **AND** overflowing content scrolls inside the relevant content pane instead of resizing surrounding controls

#### Scenario: Large viewport keeps comfortable maximum sizes
- **WHEN** the viewport is wider than the content's intended reading or inspection width
- **THEN** dialogs, reading panes, and tool surfaces use stable maximum sizes or constrained inner layouts rather than stretching every line or control across the full viewport

### Requirement: Touch devices have non-hover interaction paths
The Project Web GUI SHALL provide touch-compatible alternatives for interactions that use hover, precise pointer movement, or desktop double-click gestures.

#### Scenario: Hover preview has touch fallback
- **WHEN** an interaction exposes additional information through hover on desktop
- **THEN** touch users can access equivalent information through selection, tap, long-press, or an explicit open or details action

#### Scenario: Primary actions meet touch target needs
- **WHEN** a primary control is rendered in a touch-oriented viewport
- **THEN** the control has enough visual and hit-target space to be tapped reliably without overlapping adjacent controls

### Requirement: Overlays keep controls stable while content changes
The Project Web GUI SHALL keep overlay headers, tab strips, and action controls stable while dynamic content changes inside dialogs, sheets, popovers, or tabbed panes.

#### Scenario: Tabbed overlay does not jump on tab switch
- **WHEN** a user switches tabs inside an overlay with content of different lengths or shapes
- **THEN** the overlay shell keeps a stable size for the current viewport
- **AND** the tab buttons and primary actions do not move because of the active tab content

#### Scenario: Overlay status updates do not shift controls
- **WHEN** an overlay shows transient status text such as copy success, loading, or error feedback
- **THEN** the overlay reserves stable space or otherwise avoids moving the controls the user is likely to click next

### Requirement: Specialized viewers are wrapped responsively
The Project Web GUI SHALL wrap specialized viewers in responsive containers that define stable dimensions, scroll boundaries, and theme tokens without replacing the viewer library itself.

#### Scenario: Graph viewer remains inspectable
- **WHEN** a graph viewer is opened on desktop, tablet, or phone-sized viewport
- **THEN** the graph canvas or overview area has a bounded visible region, reachable controls, and a detail path that does not depend only on raw horizontal page scrolling

#### Scenario: Tabular data remains usable on narrow screens
- **WHEN** a table or dense record list is opened on a narrow viewport
- **THEN** the GUI provides a horizontal scroll region, compact card/list fallback, or another bounded presentation that keeps page-level navigation usable

### Requirement: Responsive behavior is validated across representative devices
The Project Web GUI SHALL include automated or manual browser validation for representative desktop, tablet, iPhone, and Android-sized viewports.

#### Scenario: Viewport validation checks layout stability
- **WHEN** responsive layout validation runs
- **THEN** it checks that primary navigation, active tabs, dialogs, overlay controls, and representative viewer content remain reachable and do not visibly overlap

#### Scenario: Theme validation covers responsive surfaces
- **WHEN** responsive layout validation covers a surface with theme-sensitive colors
- **THEN** it checks light and dark theme behavior where practical for that surface

