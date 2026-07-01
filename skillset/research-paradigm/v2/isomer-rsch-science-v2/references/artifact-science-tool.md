# Science Evidence Graph Recording

Use this reference to record science evidence graph updates. It describes evidence records; it does not run computations. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Choose record action**. Create a new stable node, append an update to an existing node, link related nodes, summarize graph status, or request UI focus.
2. **Choose node type**. Use package check, computational run, dataset analysis, parameter sweep, validation result, or claim.
3. **Use stable node ids**. Create once for a new logical node id; append later status, evidence, validation, or interpretation updates instead of rewriting history.
4. **Fill common fields**. Record title, summary, status, domain, package id, task type, key results, inputs, logs, outputs, evidence paths, parent nodes, related nodes, metadata, and canvas hints when useful.
5. **Link claims to evidence**. Connect <SCIENCE_CLAIM_RECORD> to <SCIENCE_RUN_RECORD>, <SCIENCE_VALIDATION_RESULT>, package checks, or evidence paths.
6. **Record failures and blockers**. Failed or blocked package checks and runs should still become evidence when they determine the route.

## Preferences

- Prefer append-only updates over replacing earlier evidence (if status changes, otherwise add an update).
- Prefer stable logical node ids over mutable file-slot names.
- Prefer explicit evidence paths over prose-only summaries.
- Prefer failed or blocked records when a diagnostic changes the route.

## Constraints

- <SCIENCE_PACKAGE_CHECK> with passed status must include environment-check evidence.
- <SCIENCE_RUN_RECORD> with success status must include input, log, output, or evidence paths.
- <SCIENCE_VALIDATION_RESULT> must reference the run, analysis, or sweep it validates.
- <SCIENCE_CLAIM_RECORD> must include claim type.
- Computed claims must not exist without evidence paths or related computed/validation nodes.

## Quality Gates

### Metrics

- Required-evidence coverage: fraction of science package checks, computational runs, dataset analyses, parameter sweeps, validation results, and claims with the required evidence fields for their node type; higher is better.
- Unsupported-claim count: number of science claims without claim type, evidence paths, or related computed or validation nodes when required; lower is better.

### Checks

- Type gate: node type matches the evidence being recorded.
- Evidence gate: inputs, logs, outputs, evidence paths, or related nodes support the status.
- Link gate: validation and claim records link to supporting records.
- Status gate: planned, ready, queued, running, success, failed, blocked, warning, passed, active, or superseded status is justified.
- Append gate: updates preserve prior evidence rather than overwriting it.
