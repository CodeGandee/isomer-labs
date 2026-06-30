# Claim-Type Discipline

Scientific Research Claims must state how the assertion was obtained.

## `computed`

Use when the value or conclusion was produced by real execution in the current Research Task or by a durable prior Run explicitly linked as evidence.

Required support:

- Computational Run, dataset analysis, or parameter sweep Evidence Item.
- Output, log, input, script, environment, or related validation Evidence Items.
- Validation when convergence, correctness, units, schema, physics, statistics, or scientific semantics matter.

## `parsed`

Use when the claim comes from user-provided data, existing files, tables, logs, metadata, or machine-readable records.

Required support:

- Input data path or Artifact.
- Parser, query, script, or command record.
- Schema, count, checksum, or consistency checks when relevant.

## `digitized`

Use when the claim comes from a paper figure, image, PDF plot, OCR, or manual digitization.

Required support:

- Source figure, image, or PDF Artifact.
- Digitization method or script path.
- Uncertainty note and any calibration assumptions.

Never relabel digitized evidence as computed unless the underlying computation was actually rerun.

## `hypothesis`

Use when the statement is plausible but not verified by current computation or data.

Required support:

- Rationale and intended validation path.
- Wording that does not imply the result has already happened.

## Upgrade Path

To upgrade `hypothesis` to `computed`, run the needed package check and computation, record execution and validation Evidence Items, then append a new computed Research Claim or supersede the old claim through a Decision Record.
