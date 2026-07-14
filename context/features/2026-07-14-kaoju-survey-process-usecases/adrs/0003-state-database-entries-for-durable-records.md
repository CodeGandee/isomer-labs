# State Database Entries For Durable Records

Status: accepted
Date: 2026-07-14
Related: ADR-0001, ADR-0002

The use cases currently describe durable outputs as filesystem artifacts with semantic ids such as `kaoju:direction-set`, `kaoju:reading-list`, and `kaoju:source-digest`. For an agent to find these artifacts reliably across a Topic Workspace, each durable record should also have an entry in the topic workspace state database. The DB entry holds the artifact metadata and a link to the actual file stored in the topic workspace filesystem.

## Current Decision

- Every Kaoju durable record described in the survey-process use cases is registered as an entry in the topic workspace state database.
- The state DB entry contains at minimum: the semantic artifact id, artifact kind, creation/refresh timestamp, status, a stable filesystem path or workspace label, and a link to the actual stored file.
- Agents look up artifacts by querying the state database rather than scanning the topic workspace directory tree.
- The filesystem remains the source of truth for file contents; the state database is the source of truth for artifact metadata, existence, and discoverability.

## Affected Artifacts

- `feature-requirement.md`: added state-DB registration to the structured-records functional requirement.
- `usecases/uc-01-survey-direction-from-topic.md`: added state-DB registration note to durable outputs.
- `usecases/uc-02-collect-online-info-and-build-reading-list.md`: added state-DB registration note to durable outputs.
- `usecases/uc-03-ingest-reading-item-in-depth.md`: added state-DB registration note to durable outputs.

## Refinement History

### 2026-07-14 - Initial Decision

- Instruction: "for context/features/2026-07-14-kaoju-survey-process-usecases/usecases/*, durable records should have entry in state db so that when agent look for things it will look into the db which contains metadata and links to actual filesystem stored files"
- Applied changes:
  - Added a state-database registration preamble to the durable outputs sections of UC-01, UC-02, and UC-03.
  - Updated `feature-requirement.md` to require state-DB registration for structured records.
