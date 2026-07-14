# Export Survey Records To LLM Wiki And Deploy Viewer

Status: accepted
Date: 2026-07-14
Related: ADR-0003, ADR-0006

Survey records are currently stored as durable Kaoju artifacts in the topic workspace state database and filesystem. To make them more browseable and cross-linked, the feature should support exporting them into the LLM Wiki format used by `imsight-llm-wiki`, deploying the bundled web viewer, and launching it on a local port.

## Current Decision

- UC-07 supports exporting accepted Kaoju survey artifacts into an LLM Wiki at a resolved Topic Workspace default or an actor-supplied path.
- The export produces human-readable wiki pages and one canonical JSON metadata file describing artifact-to-page mapping, provenance, and managed-path ownership.
- The functionality is implemented as a self-contained Isomer Labs system extension or CLI command; it does not route to or invoke the external `imsight-llm-wiki` skill.
- The exported wiki representation is compatible with a package-owned viewer selected after license and provenance review.
- The system can deploy the package-owned viewer to a resolved Topic Workspace default or actor-supplied directory and write a JSON manifest inside the viewer directory that points to the wiki root.
- Re-export and recognized viewer refresh update managed files in place, preserve unrecognized files, and record a changelog while durable Artifact revisions retain history.
- The system can start the deployed viewer on a local port and report the URL.
- All exports and deployments are registered in the topic workspace state database with metadata and filesystem links.

## Affected Artifacts

- `usecases/uc-07-export-survey-records-to-llm-wiki-and-deploy-viewer.md`: new use case describing convert, deploy, and start actions.
- `usecases/README.md`: indexed UC-07.
- `README.md`: updated current-stage summary.

## Refinement History

### 2026-07-14 - Export Update Policy

- Default wiki and viewer targets resolve inside the Topic Workspace, with explicit actor path overrides.
- JSON is the single canonical machine representation.
- Re-export stages an in-place update of recognized managed files and records a changelog; unrecognized files remain untouched.
- Viewer assets must be package-owned. Candidate external source code requires license and provenance validation, with an independent compatible implementation as the fallback.

### 2026-07-14 - Initial Decision

- Instruction: export survey records into LLM Wiki viewable by `imsight-llm-wiki` viewer, record metadata in JSON/YAML, user says "convert the records into llm wiki in <user given path>", then "deploy a viewer to <user-given-path> targetting that wiki", then "start the viewer" to start at a port.
- Applied changes:
  - Created UC-07 with convert, deploy-viewer, and start-viewer actions.
  - Defined durable outputs: `kaoju:llm-wiki-export`, `kaoju:llm-wiki-metadata`, `kaoju:llm-wiki-viewer`, `kaoju:llm-wiki-viewer-manifest`.
  - Added wiki page mapping and metadata schema examples.
  - Added ADR-0007.
