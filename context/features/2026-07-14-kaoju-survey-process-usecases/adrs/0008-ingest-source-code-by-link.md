# Ingest Source Code By Link

Status: accepted
Date: 2026-07-14
Related: ADR-0002, ADR-0003

UC-03 ingests reading-list items, which may include source-code repositories that were discovered during online collection. However, a researcher may also encounter a repository URL directly and want to ingest it without first adding it to a reading list. A separate use case is needed for this direct, focus-driven source-code ingestion.

## Current Decision

- UC-08 supports ingesting a source-code repository from a direct URL.
- The actor provides the URL and an optional focus area.
- The system clones the repository with `git clone --depth 1` into the topic workspace extern-repo location.
- The system reads the local copy, extracts code-level claims and evidence grounded in file paths and line ranges, and produces a `KAOJU:SOURCE-DIGEST`.
- The repository is added to `KAOJU:ARTIFACT-LIBRARY` and optionally to the current direction's `KAOJU:READING-LIST`.
- All artifacts are registered in the state database.

## Affected Artifacts

- `usecases/uc-08-ingest-source-code-by-link.md`: new use case describing direct repository ingestion by URL.
- `usecases/README.md`: indexed UC-08.
- `README.md`: updated current-stage summary.

## Refinement History

### 2026-07-14 - Initial Decision

- Instruction: "check this <link>, read the source code and ingest in depth, focus on <something user care about>"; agent checks out source code with `git clone --depth 1`, reads local copy, and adds to surveyed artifacts.
- Applied changes:
  - Created UC-08 with direct-URL ingestion, focus-area extraction, and artifact-library/reading-list updates.
  - Added ADR-0008.
