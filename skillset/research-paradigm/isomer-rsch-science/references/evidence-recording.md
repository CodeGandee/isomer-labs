# Evidence Recording

Scientific work should leave durable records that connect package checks, execution, validation, and claims.

## Record Types

| Work | Isomer Record |
| --- | --- |
| package or environment check | Artifact plus Evidence Item with passed, failed, or blocked status |
| solver run, simulation, model fit, numerical computation, or engineering computation | Run record plus computational Evidence Item |
| dataset parsing or analysis | Dataset-analysis Evidence Item and source data Artifact |
| parameter sweep | Sweep Artifact plus per-run Evidence Items or summary Evidence Item |
| validation | Validation Evidence Item linked to the run, analysis, or sweep |
| supported conclusion | Research Claim linked to execution and validation evidence |
| failed, blocked, or infeasible route | Evidence Item plus Decision Record, Gate, or blocker |

## Required Fields

- stable logical id or title.
- status: planned, ready, queued, running, success, failed, blocked, warning, passed, active, or superseded.
- domain and package or solver when relevant.
- task type and short summary.
- input paths, log paths, output paths, and evidence paths when applicable.
- key results with units.
- parameters, seeds, versions, modules, credentials status, hardware, and tolerance choices when relevant.
- parent or related Evidence Items, Research Claims, Decision Records, and Provenance Records.

## Append-Only Discipline

Do not overwrite an old evidence interpretation silently. If status, evidence, or interpretation changes, append a new Evidence Item, update record, Decision Record, or Provenance Record so the history remains auditable.

## Reporting Boundary

When reporting to the user, separate raw execution status from validation status and claim status. A run can succeed while validation fails; a parsed value can support a claim without being computed; a blocked package check can still be decision-relevant evidence.
