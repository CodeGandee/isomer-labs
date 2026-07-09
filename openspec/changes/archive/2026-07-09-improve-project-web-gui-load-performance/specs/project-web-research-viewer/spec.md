## MODIFIED Requirements

### Requirement: Open-tab Resource Policy
The Project Web GUI SHALL scope expensive data fetching, module loading, and rendering to open relevant workbench tabs.

#### Scenario: Closed tabs stop expensive work
- **WHEN** a graph, Markdown, PDF, table, diagnostics, AG-UI, or future tmux tab is closed
- **THEN** the GUI stops polling, SSE-triggered refetches, graph layout work, graph rendering, Mermaid rendering, PDF rendering, and session attachment for that tab

#### Scenario: Live events invalidate relevant open views
- **WHEN** a topic change event arrives
- **THEN** the GUI invalidates only mounted queries whose topic id, graph scope, material kind, record id, or diagnostics interest intersects the event

#### Scenario: User context survives refresh
- **WHEN** the selected topic read model refreshes after terminal-side work creates or revises records
- **THEN** the GUI preserves topic selection, filters, layout mode, and selected detail when the selected record still exists

#### Scenario: Initial shell avoids heavy viewer modules
- **WHEN** the user opens the Project Web GUI shell before opening a graph, detail Markdown preview, Mermaid diagram, KaTeX content, PDF preview, or graph-layout-heavy panel
- **THEN** the initial browser bundle SHALL NOT synchronously load the modules used only by those unopened viewers

#### Scenario: Heavy viewer opens on demand
- **WHEN** the user opens a graph, Markdown preview, Mermaid diagram, KaTeX content, PDF preview, or graph-layout-heavy panel
- **THEN** the GUI SHALL load the needed viewer module on demand and show a non-blocking loading state while that module loads

### Requirement: Responsive Research Workbench
The Project Web GUI SHALL remain usable across desktop, tablet, and mobile browser sizes and SHALL respect the service cache mode when loading local static assets.

#### Scenario: Browser size changes
- **WHEN** the browser viewport changes size
- **THEN** the workbench layout, graph viewport, tables, detail panels, and diagnostics remain usable without text overlap or hidden primary controls

#### Scenario: Debug launch loads latest static assets
- **WHEN** the local web service serves the GUI shell, static assets, or API responses in debug launch mode
- **THEN** cache headers prevent stale browser assets from hiding the latest local build during development and manual testing

#### Scenario: Normal launch remains responsive on remote links
- **WHEN** the local web service serves the GUI in normal launch mode over a constrained remote connection
- **THEN** compressed responses, cacheable hashed static assets, lightweight initial API payloads, and lazy-loaded heavy viewers keep the workbench shell usable before unopened viewer details finish loading
