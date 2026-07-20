# Science Evidence Graph Recording

Use this reference to record science evidence graph updates. It describes evidence records; it does not run computations. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Choose record action**. Create a new stable node, append an update to an existing node, link related nodes, status graph status, or request UI focus.
2. **Choose node type**. Use package check, computational run, dataset analysis, parameter sweep, validation result, or claim.
3. **Use stable node ids**. Create once for a new logical node id; append later status, evidence, validation, or interpretation updates instead of rewriting history.
4. **Fill common fields**. Record title, summary, status, domain, package id, task type, key results, inputs, logs, outputs, evidence paths, parent nodes, related nodes, metadata, and canvas hints when useful.
5. **Link claims to evidence**. Connect DEEPSCI:SCIENCE-CLAIM-RECORD to DEEPSCI:SCIENCE-RUN-RECORD, DEEPSCI:SCIENCE-VALIDATION-RESULT, package checks, or evidence paths.
6. **Record failures and blockers**. Failed or blocked package checks and runs should still become evidence when they determine the route.

## Preferences

Read these preferences as route-shaping defaults for this step, not as hard requirements. Apply the preferred path when its condition holds, and record the fallback or reason when it does not.

- Prefer append-only updates over replacing earlier evidence (if status changes, otherwise add an update).
- Prefer stable logical node ids over mutable file-slot names.
- Prefer explicit evidence paths over prose-only summaries.
- Prefer failed or blocked records when a diagnostic changes the route.

## Constraints

Read these constraints as the validity boundary for this step. Treat `must` and `must not` as hard requirements, and treat `should` and `should not` as strong defaults that need an explicit reason to override.

- DEEPSCI:SCIENCE-PACKAGE-CHECK with passed status must include environment-check evidence.
- DEEPSCI:SCIENCE-RUN-RECORD with success status must include input, log, output, or evidence paths.
- DEEPSCI:SCIENCE-VALIDATION-RESULT must reference the run, analysis, or sweep it validates.
- DEEPSCI:SCIENCE-CLAIM-RECORD must include claim type.
- Computed claims must not exist without evidence paths or related computed/validation nodes.

## Quality Gates

Read these gates after producing the step output and before handoff or completion. Use `Metrics` as directional quality signals and `Checks` as inspectable pass/fail conditions; weak metrics or failed checks should trigger revision, blocker recording, or a route change.

### Metrics

- Required-evidence coverage: fraction of science package checks, computational runs, dataset analyses, parameter sweeps, validation results, and claims with the required evidence fields for their node type; higher is better.
- Unsupported-claim count: number of science claims without claim type, evidence paths, or related computed or validation nodes when required; lower is better.

### Checks

- Type gate: node type matches the evidence being recorded.
- Evidence gate: inputs, logs, outputs, evidence paths, or related nodes support the status.
- Link gate: validation and claim records link to supporting records.
- Status gate: planned, ready, queued, running, success, failed, blocked, warning, passed, active, or superseded status is justified.
- Append gate: updates preserve prior evidence rather than overwriting it.
