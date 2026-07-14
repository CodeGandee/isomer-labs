## ADDED Requirements

### Requirement: Wiki Export Selects Accepted Artifacts from the State DB
The system SHALL build an LLM Wiki export from explicit accepted Kaoju artifact revisions resolved through the Topic Workspace state DB.

#### Scenario: Default survey export is requested
- **WHEN** the actor requests an LLM Wiki export without enumerating individual records
- **THEN** the exporter queries accepted current survey artifacts and their required lineage through Workspace Runtime
- **AND** it reports ambiguities, missing content, stale locators, and excluded non-accepted records before writing the export

#### Scenario: Actor selects an explicit subset
- **WHEN** the actor supplies artifact ids, semantic ids, or a bounded paper or direction scope
- **THEN** the exporter resolves the exact selected revisions and their permitted relationship context
- **AND** it does not replace the selection with newer or broader records without disclosure and actor approval

#### Scenario: Export discovery avoids directory scanning
- **WHEN** the exporter needs source artifacts or relationships
- **THEN** it uses state-DB queries and registered content locators
- **AND** unregistered files found in the Topic Workspace are not silently included

### Requirement: Wiki Export Contains Human and Machine Representations
The system SHALL export human-readable Markdown pages and one versioned-schema JSON mapping manifest to a resolved Topic Workspace default or actor-selected wiki root.

#### Scenario: Export succeeds
- **WHEN** all selected artifacts and the target path pass preflight
- **THEN** the exporter writes cross-linked Markdown pages and canonical JSON metadata
- **AND** it registers `kaoju:llm-wiki-export` and `kaoju:llm-wiki-metadata`

#### Scenario: Actor omits the target paths
- **WHEN** the actor requests wiki export or viewer deployment without an explicit target
- **THEN** the CLI resolves the applicable managed target inside the Topic Workspace through Semantic Workspace Surface Labels
- **AND** an actor-supplied authorized path overrides the default and retains its external or managed locator posture

#### Scenario: Mapping metadata preserves provenance
- **WHEN** the export manifest is inspected
- **THEN** it records schema and exporter versions, topic identity, generation time, target root, artifact ids, semantic ids, revisions, checksums, page paths, relationship edges, provenance refs, and source content locators
- **AND** each generated page can be traced back to the exact artifact revisions that produced it

#### Scenario: Export is repeated
- **WHEN** an export is rerun for the same target and selection
- **THEN** the exporter stages and applies an in-place update of paths owned by the recognized prior manifest and reports created, changed, unchanged, stale, and removed managed paths in a changelog
- **AND** it preserves unrecognized files, registers a new checksummed export revision, and exposes the current export at the same target root

### Requirement: Wiki Functionality Is Self-Contained in Isomer
The wiki exporter, deployer, and launcher SHALL be implemented as package-owned Isomer Labs code and assets.

#### Scenario: Export command runs without external skill
- **WHEN** `isomer-cli ext kaoju wiki export` executes
- **THEN** it does not load, route to, invoke, or require the external `imsight-llm-wiki` skill
- **AND** it remains functional from an installed Isomer Labs package without a repository checkout

#### Scenario: Viewer compatibility is validated
- **WHEN** the packaged viewer is tested against an exported wiki
- **THEN** it consumes the versioned Isomer wiki and viewer manifests and renders the required page and relationship navigation
- **AND** compatibility does not depend on undocumented files in an external skill checkout

#### Scenario: Candidate viewer code lacks accepted license provenance
- **WHEN** implementation considers bundling viewer code from another source
- **THEN** packaging remains blocked until license and provenance validation passes
- **AND** an independently implemented compatible viewer remains the fallback

### Requirement: Viewer Deployment Is Managed and Registered
The system SHALL deploy a package-owned compatible viewer to a resolved Topic Workspace default or actor-selected directory and SHALL write a JSON viewer manifest that points to the target wiki.

#### Scenario: Viewer is deployed
- **WHEN** the actor supplies an authorized viewer target and a registered wiki export
- **THEN** the deployer writes the viewer assets and `kaoju:llm-wiki-viewer-manifest` with viewer version, wiki root, wiki metadata ref, deployment time, expected start command ref, and checksums
- **AND** it registers `kaoju:llm-wiki-viewer` and `kaoju:llm-wiki-viewer-manifest` with filesystem locators

#### Scenario: Viewer target contains another deployment
- **WHEN** the selected target contains a recognized viewer manifest
- **THEN** the deployer refreshes its managed assets in place and preserves deployment lineage and a change summary
- **AND** an unrecognized non-empty target requires clarification or an explicit overwrite decision

#### Scenario: Wiki target becomes stale
- **WHEN** the deployed viewer manifest points to a missing, moved, or superseded wiki export
- **THEN** viewer status reports the stale target and the required redeploy or manifest-update route
- **AND** it does not silently select another wiki root

### Requirement: Viewer Launch Uses a Recorded Local Run
The system SHALL launch the deployed viewer through registered command execution and SHALL bind to a local interface by default.

#### Scenario: Viewer starts on a local port
- **WHEN** the actor requests viewer start and the deployment passes validation
- **THEN** the system selects or validates an available loopback port, starts the viewer through an Execution Adapter Command Request, and reports the local URL
- **AND** the Run records viewer and wiki refs, bind address, port, process handle, logs, start time, and terminal or active status

#### Scenario: Requested port is unavailable
- **WHEN** the requested port is occupied or disallowed
- **THEN** the system reports the conflict and either selects another authorized port or waits for actor direction
- **AND** it does not terminate the unrelated process

#### Scenario: Non-loopback binding is requested
- **WHEN** the actor asks to expose the viewer beyond loopback
- **THEN** the configured network-exposure Gate policy applies before launch
- **AND** the resulting bind address and authorization decision are recorded in the Run provenance
