# project-web-gui-component-system Specification

## Purpose
TBD - created by archiving change adopt-shadcn-ui-foundation. Update Purpose after archive.
## Requirements
### Requirement: Primary GUI Component System
The Project Web GUI SHALL use shadcn/ui copied components as the primary component source for ordinary application controls and workbench chrome.

#### Scenario: Ordinary control uses local shadcn component
- **WHEN** the GUI implements a button, input, select, checkbox, badge, dialog, tooltip, dropdown menu, scroll area, separator, tab, or table for application chrome
- **THEN** the implementation uses a local copied shadcn component or an Isomer wrapper around one instead of a raw ad hoc control

#### Scenario: Copied component remains owned source
- **WHEN** a shadcn component is added to the GUI
- **THEN** its source is committed under the frontend source tree and can be reviewed, edited, and tested as Isomer code

### Requirement: Tailwind Token Styling
The Project Web GUI SHALL use Tailwind CSS and shadcn-compatible CSS variables as the primary styling and design-token system for application UI.

#### Scenario: Global token layer exists
- **WHEN** the frontend app starts
- **THEN** global CSS defines shadcn-compatible tokens for background, foreground, card, popover, primary, secondary, muted, accent, destructive, border, input, ring, chart colors, sidebar colors, and radius

#### Scenario: Workbench radius remains restrained
- **WHEN** the component-system tokens are configured
- **THEN** default component radii remain at or below 8px unless a specialized viewer requires a different shape

#### Scenario: Theme mode supports system preference
- **WHEN** the GUI applies light or dark appearance
- **THEN** Tailwind/shadcn tokens and viewer token bridges support light, dark, and system-derived modes without hard-coding a single visual mode into components

### Requirement: Specialized Viewer Boundaries
The Project Web GUI SHALL preserve specialized renderer libraries for viewer-specific surfaces and bridge them to the app component system through wrapper components and scoped styles.

#### Scenario: Graph renderer remains specialized
- **WHEN** the GUI renders sparse idea lineage or dense artifact relationship views
- **THEN** React Flow or Sigma remains responsible for graph rendering while shadcn/Tailwind styles the surrounding controls, legends, panels, and custom node content

#### Scenario: Docking renderer remains specialized
- **WHEN** the GUI renders dockable tabs or split panes
- **THEN** Dockview remains responsible for docking behavior while shadcn/Tailwind styles app-level commands, tab content, empty states, and wrapper surfaces

#### Scenario: Content viewer remains specialized
- **WHEN** the GUI renders Markdown, Mermaid, KaTeX, JSON, PDF, terminal, or Plotly content
- **THEN** the established viewer library remains responsible for rendering that content while app tokens provide surrounding color, spacing, and focus styles

### Requirement: React Flow Theme Bridge
The Project Web GUI SHALL bridge shadcn/Tailwind theme tokens into React Flow idea lineage views without treating React Flow as a shadcn component.

#### Scenario: React Flow receives color mode
- **WHEN** the idea lineage React Flow view is rendered
- **THEN** the view passes an explicit React Flow color mode derived from the GUI theme preference

#### Scenario: React Flow variables are scoped
- **WHEN** the GUI customizes React Flow background, controls, nodes, handles, edges, labels, hover states, or selected states
- **THEN** those customizations use scoped wrapper classes or React Flow CSS variables instead of global unscoped overrides

#### Scenario: Semantic colors survive theme changes
- **WHEN** the GUI theme changes between light, dark, and system-derived modes
- **THEN** artifact-kind and status colors for idea lineage remain legible and keep their semantic meaning

### Requirement: Incremental Migration Discipline
The Project Web GUI SHALL migrate existing hand-written controls to shadcn/Tailwind incrementally while preserving existing behavior and tests.

#### Scenario: Migrated surface keeps behavior
- **WHEN** an existing surface such as the Project Explorer, toolbar, graph filters, record table, detail actions, or JSON dialog is migrated to shadcn components
- **THEN** the surface preserves its existing data fetching, route/history behavior, Dockview tab behavior, accessibility-relevant labels, and open-tab resource policy

#### Scenario: Legacy CSS is removed when replaced
- **WHEN** a migrated surface no longer depends on its old CSS selectors
- **THEN** obsolete selectors are removed or narrowed so future work does not copy stale styling patterns

#### Scenario: Generated Markdown is isolated
- **WHEN** the GUI renders generated Markdown content
- **THEN** Tailwind utility classes are not required inside the generated Markdown body, and Markdown styling stays scoped to the Markdown viewer wrapper

### Requirement: Documented GUI Styling Contract
The Project Web GUI component-system choice SHALL be documented for future GUI work.

#### Scenario: Tech stack names component foundation
- **WHEN** a developer or agent reads the GUI tech stack notes
- **THEN** the notes identify shadcn/ui as the primary app component source and Tailwind as the primary app styling and token system

#### Scenario: Viewer exceptions are documented
- **WHEN** a developer or agent reads the GUI tech stack notes
- **THEN** the notes identify Dockview, React Flow, Sigma, Plotly, Markdown, PDF, and terminal renderers as specialized libraries that use token bridges rather than shadcn replacement

