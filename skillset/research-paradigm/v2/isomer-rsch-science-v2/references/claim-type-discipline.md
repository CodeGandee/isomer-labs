# Claim Type Discipline

Use this reference to calibrate scientific claims to evidence type. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Classify computed claims**. Use computed only when the value or conclusion was produced by real execution in the current workspace and is linked to <SCIENCE_RUN_RECORD> or <SCIENCE_VALIDATION_RESULT>.
2. **Classify parsed claims**. Use parsed when the claim comes from user-provided data, existing files, tables, metadata parsing, or schema inspection.
3. **Classify digitized claims**. Use digitized when the claim comes from a paper figure, image, PDF plot, OCR, or manual extraction.
4. **Classify hypotheses**. Use hypothesis when the statement is plausible but not verified by current computation or data.
5. **Upgrade only through evidence**. To upgrade hypothesis to computed, run the package check and computation, record run and validation evidence, then append or supersede the old claim.

## Preferences

- Prefer hypothesis when evidence is not yet present (if the claim is plausible but unverified, otherwise do not overstate it).
- Prefer parsed over computed for existing data or metadata interpretation (if the computation was not rerun, otherwise keep the source clear).
- Prefer digitized for figure extraction even when values look numeric (if the underlying computation was not rerun, otherwise do not call it computed).

## Constraints

- <SCIENCE_CLAIM_RECORD> must state computed, parsed, digitized, or hypothesis.
- Computed claims must link to current-run evidence, outputs, or validation records.
- Parsed claims must include input data and parser or inspection evidence.
- Digitized claims must include source figure/image/PDF, extraction method, and uncertainty note.
- Hypotheses must not be phrased as if the result already happened.

## Quality Gates

### Metrics

- Claim-support coverage: fraction of computed, parsed, digitized, and hypothesis claims with the source-required support for their claim type; higher is better.
- Misclassified-claim count: number of digitized, parsed, or hypothesis assertions mislabeled as computed; lower is better.

### Checks

- Type gate: claim type matches how the assertion was obtained.
- Support gate: required evidence for the claim type is present.
- Calibration gate: language strength matches evidence strength.
- Upgrade gate: claim upgrades happen through new evidence, not wording changes.
