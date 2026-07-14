# Use Case 07: Export Survey Records To LLM Wiki And Deploy Viewer

## Actor Goal

As a researcher or Topic Actor, I want to export the survey records into an LLM Wiki and deploy its bundled web viewer, so that I can browse the survey materials, source digests, claims, and synthesis in a cross-linked, navigable knowledge base.

## Use Case

The system reads the accepted Kaoju survey artifacts from the state database — `kaoju:direction-set`, `kaoju:reading-list`, `kaoju:source-digest`, `kaoju:claim-evidence-ledger`, `kaoju:field-summary`, `kaoju:related-work-catalog`, and `kaoju:paper-draft-myst` — and converts them into the LLM Wiki format expected by the viewer bundled with `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-llm-wiki`. The conversion is implemented as a self-contained Isomer Labs system extension or CLI command; it does **not** invoke the external `imsight-llm-wiki` skill workflow. The conversion produces both human-readable wiki pages under `wiki/` and computer-friendly metadata files (JSON/YAML) that describe the exported records so that future conversions or tooling can consume them reliably. The wiki is written to a user-given path inside or outside the topic workspace. The system then supports deploying the bundled web viewer to another user-given directory; the deployment includes a manifest file inside the viewer directory that points to the wiki root. Finally, when the user says "start the viewer," the system launches the viewer on a local port so the wiki can be browsed.

## Supported Actions

### Convert Records To LLM Wiki

Export Kaoju survey records into an LLM Wiki at a user-given path.

- context
  - Actor **has** accepted survey artifacts in the topic workspace state database.
  - System **has** the artifact records, the LLM Wiki skill conventions, and a target path.
- intent
  - Actor **wants** the survey materials converted into a browseable wiki.
  - Actor **wonders** "Convert the records into an LLM Wiki in `~/wikis/predictive-memory-tiering`."
- action
  - Actor then **provides** a target directory and asks the system to convert the records.
- result
  - Actor **gets** a populated LLM Wiki directory and a durable `kaoju:llm-wiki-export` record with metadata and a link to the wiki root.

### Deploy Viewer To Target Wiki

Deploy the bundled LLM Wiki web viewer to a user-given directory, configured to point at the wiki.

- context
  - Actor **has** an LLM Wiki export at a known path.
  - System **has** the viewer source bundled in `imsight-llm-wiki`.
- intent
  - Actor **wants** a local web viewer for the exported wiki.
  - Actor **wonders** "Deploy a viewer to `~/viewer/predictive-memory-tiering` targeting that wiki."
- action
  - Actor then **provides** a viewer installation directory and asks the system to deploy the viewer.
- result
  - Actor **gets** a deployed viewer directory with a manifest file pointing to the wiki root, plus a `kaoju:llm-wiki-viewer` record.

### Start Viewer

Launch the deployed viewer on a local port.

- context
  - Actor **has** a deployed viewer directory.
  - System **has** the viewer manifest and an available local port.
- intent
  - Actor **wants** to browse the wiki in a web browser.
  - Actor **wonders** "Start the viewer."
- action
  - Actor then **asks** the system to start the viewer.
- result
  - Actor **gets** the viewer running at a local URL (e.g., `http://127.0.0.1:8080`).

## Main Flow

1. Actor asks the system to convert the survey records into an LLM Wiki at a given path.
2. System reads the accepted survey artifacts from the topic workspace state database.
3. System creates the LLM Wiki directory structure: `README.md`, `wiki/index.md`, `wiki/concepts/`, `wiki/entities/`, `wiki/summaries/`, `raw/`, `audit/`, `log/`, `outputs/`.
4. System converts each survey artifact into wiki pages with YAML frontmatter and canonical wikilinks.
5. System writes computer-friendly metadata files (JSON/YAML) describing the exported records, their provenance, and the mapping from Kaoju artifact ids to wiki page paths.
6. System registers the export as `kaoju:llm-wiki-export` in the state database with metadata and a filesystem link.
7. Actor asks the system to deploy a viewer to a target directory, pointing at the wiki.
8. System copies the bundled viewer source to the target directory and writes a `viewer-manifest.json` (or YAML) file containing the wiki root path, viewer version, deployment timestamp, and default port.
9. System registers the deployment as `kaoju:llm-wiki-viewer` in the state database.
10. Actor asks the system to start the viewer.
11. System reads the viewer manifest, resolves an available port, and launches the viewer process.
12. System reports the local URL and process information to the actor.

## Alternative And Exception Flows

- **A1. Wiki already exists**: If the target wiki directory already exists, the system offers to overwrite, merge/update, or cancel.
- **A2. Viewer already deployed**: If the viewer directory already exists, the system offers to refresh, reconfigure, or force-redeploy.
- **A3. Port in use**: If the default port is busy, the system tries the next available port and reports the actual port.
- **A4. Partial export**: If some survey artifacts are missing, the system exports what is available and records the gaps in the metadata.
- **E1. Missing viewer dependencies**: If `node`/`npm` and `bun` are unavailable, the system reports a blocker with installation guidance.
- **E2. Viewer launch failure**: If the viewer fails to start, the system reports the error log and asks whether to retry or reconfigure.

## Mermaid Flow Diagram

```mermaid
flowchart LR
  Actor[Researcher / Topic Actor]

  subgraph System[Kaoju Survey Workflow]
    ReadRecords[Read survey records from state DB]
    CreateWiki[Create LLM Wiki structure]
    Convert[Convert records to wiki pages]
    WriteMeta[Write JSON/YAML metadata]
    RegisterExport[Register kaoju:llm-wiki-export]
    DeployViewer[Deploy viewer + manifest]
    RegisterViewer[Register kaoju:llm-wiki-viewer]
    StartViewer[Start viewer on port]
  end

  Actor --> ReadRecords
  ReadRecords --> CreateWiki
  CreateWiki --> Convert
  Convert --> WriteMeta
  WriteMeta --> RegisterExport
  RegisterExport --> Actor
  Actor --> DeployViewer
  DeployViewer --> RegisterViewer
  RegisterViewer --> Actor
  Actor --> StartViewer
  StartViewer --> Actor
```

## Mermaid Sequence Diagram

```mermaid
sequenceDiagram
  autonumber
  actor Researcher as "Researcher / Topic Actor"
  participant System as "Kaoju Survey Use Case"

  Researcher->>System: Convert the records into LLM Wiki in ~/wikis/pmt-survey
  System->>System: Read direction-set, reading-list, source-digests, synthesis records
  System->>System: Create wiki structure and pages
  System->>System: Write metadata JSON/YAML
  System-->>Researcher: kaoju:llm-wiki-export ref + wiki path
  Researcher->>System: Deploy a viewer to ~/viewer/pmt-wiki targeting that wiki
  System->>System: Copy bundled viewer and write viewer-manifest.json
  System-->>Researcher: kaoju:llm-wiki-viewer ref + viewer path
  Researcher->>System: Start the viewer
  System->>System: Launch viewer on http://127.0.0.1:8080
  System-->>Researcher: Viewer running at http://127.0.0.1:8080
```

## Durable Outputs

Each durable output below is registered as an entry in the topic workspace state database. The entry contains the artifact metadata and a link to the actual file stored in the topic workspace filesystem or the user-specified export path, so the agent can look it up by querying the state DB rather than scanning directories.

- `kaoju:llm-wiki-export` — record of the exported LLM Wiki, including wiki root path and exported artifact ids.
- `kaoju:llm-wiki-metadata` — JSON/YAML metadata describing the exported records, page mappings, and provenance.
- `kaoju:llm-wiki-viewer` — record of the deployed viewer, including viewer directory and target wiki.
- `kaoju:llm-wiki-viewer-manifest` — manifest file inside the viewer directory pointing to the wiki root and recording deployment settings.

## Wiki Page Mapping

Survey artifacts map to LLM Wiki pages as follows:

| Survey Artifact | Wiki Location | Page Type |
| --- | --- | --- |
| `kaoju:direction-set` | `wiki/concepts/Survey-Directions/index.md` or `wiki/concepts/Survey-Scope.md` | concept |
| `kaoju:reading-list` (per direction) | `wiki/concepts/<direction-slug>/Reading-List.md` | concept |
| `kaoju:source-digest` (per item) | `wiki/summaries/<item-slug>.md` | summary |
| `kaoju:claim-evidence-ledger` | `wiki/concepts/Claims-And-Evidence.md` | concept |
| `kaoju:field-summary` | `wiki/concepts/Field-Summary.md` | concept |
| `kaoju:related-work-catalog` | `wiki/concepts/Related-Work-Catalog.md` | concept |
| `kaoju:paper-draft-myst` | `wiki/concepts/Paper-Draft.md` or `outputs/paper-draft.md` | concept / output |

## Metadata Schema

The `kaoju:llm-wiki-metadata` file includes at minimum:

```yaml
wiki_root: "~/wikis/pmt-survey"
exported_at: "2026-07-14T12:00:00Z"
source_topic_workspace: "predictive-memory-tiering-survey"
artifact_mapping:
  - kaoju_id: "kaoju:direction-set"
    wiki_page: "wiki/concepts/Survey-Scope.md"
  - kaoju_id: "kaoju:source-digest:vllm-cacheconfig"
    wiki_page: "wiki/summaries/vllm-cacheconfig.md"
viewer:
  default_port: 8080
  manifest_path: "~/viewer/pmt-wiki/viewer-manifest.json"
```

## Example Prompt And Expected AI Response

### Event 001 - Convert Records To LLM Wiki

> Time: `2026-07-14T11:10:00Z` · Session: `topic:predictive-memory-tiering-survey`

User Prompt:

> Convert the records into LLM Wiki in `~/wikis/pmt-survey`.

AI:

> Converting the survey records into an LLM Wiki at `~/wikis/pmt-survey`.
>
> Created the wiki structure and exported 1 direction set, 2 reading lists, 6 source digests, 1 claim-evidence ledger, 1 field summary, 1 related-work catalog, and 1 paper draft.
>
> I also wrote `kaoju:llm-wiki-metadata.yaml` with the artifact-to-page mapping.
>
> Registered as `kaoju:llm-wiki-export` (`export-...`). Next, you can deploy a viewer.

### Event 002 - Deploy And Start Viewer

> Time: `2026-07-14T11:15:00Z` · Session: `topic:predictive-memory-tiering-survey`

User Prompt:

> Deploy a viewer to `~/viewer/pmt-wiki` targeting that wiki, then start it.

AI:

> Deployed the LLM Wiki viewer to `~/viewer/pmt-wiki` and wrote `viewer-manifest.json` pointing to `~/wikis/pmt-survey`.
>
> Registered as `kaoju:llm-wiki-viewer` (`viewer-...`).
>
> Started the viewer at `http://127.0.0.1:8080`.

## Assumptions And Open Questions

- Assumption: The export and viewer deployment are implemented as a self-contained Isomer Labs system extension or CLI command, not by invoking the external `imsight-llm-wiki` skill.
- Assumption: The exported wiki format is compatible with the viewer bundled in `imsight-llm-wiki`.
- Assumption: The bundled LLM Wiki viewer from `imsight-llm-wiki` can be copied to an arbitrary installation directory and started independently.
- Assumption: The target wiki path and viewer path are either user-supplied or resolved through `isomer-cli`; both are recorded in the state database.
- Open question: Should the viewer deployment be inside the topic workspace by default, or always user-specified?
- Open question: Should the metadata file be JSON, YAML, or both?
- Open question: How should the system handle re-export when the underlying survey records change — overwrite, version, or create a changelog?
