# project-web-explorer-read-api Specification

## Purpose
TBD - created by archiving change redesign-project-web-ide-workbench. Update Purpose after archive.
## Requirements
### Requirement: Project Explorer Tree API
The Project Web API SHALL expose a read-only semantic Project Explorer tree for the GUI.

#### Scenario: Project tree request returns semantic nodes
- **WHEN** the GUI requests the Project Explorer tree for an Isomer Project
- **THEN** the response includes `ok`, `mutated: false`, a deterministic revision token, root node ids, tree nodes, optional openable item descriptors, and diagnostics
- **AND** nodes represent Isomer semantic objects such as Project Manifest, Research Topics, Topic Workspaces, intent material, graphs, record collections, runtime views, Topic Actors, Agent Workspaces, repositories, and diagnostics

#### Scenario: Diagnostic details are separate from navigation
- **WHEN** semantic refs cannot be opened because they are missing, stale, unresolved, outside accepted surfaces, or unsupported
- **THEN** the Project Explorer tree exposes diagnostic counts and warning state on the owning semantic nodes
- **AND** the response keeps detailed non-openable refs in diagnostics or descriptor errors rather than adding them as Explorer leaf nodes solely because they failed

#### Scenario: Initial tree is a quiet semantic skeleton
- **WHEN** the GUI requests the initial Project Explorer tree
- **THEN** the response includes Project, Project Manifest, Research Topics, Project diagnostics, and collapsed Research Topic nodes
- **AND** deeper topic children such as graphs, record collections, runtime views, Topic Actors, Agent Workspaces, and repositories can be loaded or revealed when the user expands a Research Topic node

#### Scenario: Topic tree is not sample-specific
- **WHEN** the Project contains any registered Research Topic
- **THEN** the Project Explorer derives topic nodes from Project Manifest and Effective Topic Context
- **AND** it does not require Flash Attention-specific filenames, fixed record counts, or hard-coded Topic Workspace paths

#### Scenario: Project tree browsing is read-only
- **WHEN** the Project Explorer tree is requested
- **THEN** the backend does not rebuild, cleanup, repair, migrate, backfill, or write Workspace Runtime records or query-index rows

### Requirement: No Files Explorer API
The Project Web API SHALL avoid exposing a filesystem browsing tree for the GUI.

#### Scenario: Filesystem browsing is out of scope
- **WHEN** the GUI builds its left Explorer pane
- **THEN** it uses the Project Explorer tree only
- **AND** it does not request or render a separate Files Explorer tree

#### Scenario: File-backed content opens only through semantic refs
- **WHEN** a semantic record, artifact, Markdown document, PDF, image, or table descriptor references file-backed content
- **THEN** the descriptor may expose safe content or detail URLs for that semantic item
- **AND** the API does not offer general project-root directory traversal or raw filesystem browsing

### Requirement: Openable Item Descriptor API
The Project Web API SHALL expose lightweight descriptors for items that the GUI can open in tabs.

#### Scenario: Descriptor selects tab component
- **WHEN** the GUI resolves an openable item id
- **THEN** the response includes `ok`, `mutated: false`, `openable_item_id`, `tab_id`, `item_kind`, title, preferred tab component, topic id when relevant, record id when relevant, graph scope when relevant, content URL when relevant, detail URLs when relevant, and diagnostics

#### Scenario: Descriptor avoids heavy content
- **WHEN** an openable item descriptor is returned
- **THEN** it does not include full structured payload JSON, rendered Markdown bodies, PDF bytes, image bytes, terminal input, terminal output, credentials, authorization headers, or local file contents

#### Scenario: Missing or stale item is reported
- **WHEN** an openable item no longer exists or its backing record/file is stale
- **THEN** the descriptor reports a stable error code and diagnostics
- **AND** the operation does not mutate Project, Workspace Runtime, query-index, or filesystem state

### Requirement: Explorer Invalidation Hints
The Project Web API SHALL provide freshness hints so Explorer views can refresh without broad polling.

#### Scenario: Explorer responses include revision data
- **WHEN** the GUI receives a Project Explorer response
- **THEN** it can compare a deterministic revision token or equivalent freshness metadata with cached data

#### Scenario: Topic events refresh relevant tree nodes
- **WHEN** a topic change event indicates record, file, runtime, or diagnostic changes
- **THEN** the GUI can invalidate only mounted Explorer queries and open tabs whose topic id or item kind intersects the event

### Requirement: Explorer Topic Branches Resolve on Demand
The Project Explorer API SHALL resolve Effective Topic Context only for Research Topic branches requested as expanded or opened.

#### Scenario: Initial Explorer request
- **WHEN** the GUI requests the Project Explorer with no expanded Research Topic ids
- **THEN** the response SHALL derive collapsed topic nodes from Project Manifest registrations
- **AND** it SHALL NOT resolve every topic's Effective Topic Context

#### Scenario: One topic expands
- **WHEN** the GUI requests the Project Explorer with one expanded Research Topic id
- **THEN** the response SHALL resolve that topic and include its deeper semantic children
- **AND** it SHALL leave other collapsed topic branches unresolved

#### Scenario: Deep link bypasses tree expansion
- **WHEN** the GUI resolves a valid topic-scoped openable item directly
- **THEN** the descriptor API SHALL resolve only the requested topic
- **AND** the user SHALL NOT need to expand the matching Explorer branch first

#### Scenario: Collapsed topic configuration is damaged
- **WHEN** one collapsed topic has damaged deeper configuration
- **THEN** the initial skeleton SHALL retain its manifest-derived topic node
- **AND** expansion or opening SHALL report the detailed diagnostic for that topic

