## Why

Kaoju currently ships an IEEE Transactions presentation as its immutable LaTeX `main`, while the validated PowerInfer survey trial shows that ACM `acmart` in neutral two-column `sigconf` form produces a denser and suitable default survey layout. The packaged fallback and the topic-owned `pwinfer-analysis` default should agree so future paper builds do not require an off-record venue conversion.

## What Changes

- Replace the packaged IEEE Transactions LaTeX `main` with a pinned ACM `acmart` 2.19 source tree and a marker-based `sigconf,nonacm` entrypoint.
- Validate ACM venue identity, required constructs, source completeness, provenance, license posture, and deterministic packaged bytes.
- Update Kaoju skill guidance, package documentation, tests, and packaged-template identity for the new default.
- Atomically replace the topic-owned `pwinfer-analysis` LaTeX `main`, refresh its clean exchange copy, and preserve prior IEEE snapshots and PDFs as historical artifacts.
- Recompose the accepted PowerInfer survey MyST through the new topic template, build a new PDF, and validate its text, tables, references, pages, and visual layout.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `kaoju-paper-production`: Change the checked packaged LaTeX default from IEEE Transactions to neutral ACM `acmart` two-column `sigconf`, including its required tree, metadata, validation, topic adoption, and derived-PDF behavior.

## Impact

- Packaged resources under the Kaoju write owner change from the IEEE tree to a pinned ACM source tree.
- `isomer_labs.kaoju.template_defaults` and `isomer_labs.kaoju.template_validation` gain ACM-specific packaged and venue checks.
- Unit and integration expectations for installation, export, default initialization, snapshot reuse, and venue validation change.
- The `pwinfer-analysis` Topic Workspace receives a new state token and digest for stable LaTeX template ref `artifact-paper-template-latex-main`; existing paper snapshots remain unchanged.
- A new derived TeX snapshot, TeX draft, build run, PDF, revision log, and validation report are created from the existing canonical MyST paper.
