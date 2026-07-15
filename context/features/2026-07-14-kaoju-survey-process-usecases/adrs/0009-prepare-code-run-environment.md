# Prepare Code Run Environment

Status: accepted
Date: 2026-07-14
Related: ADR-0003, ADR-0008

Running source code to verify paper claims requires a working environment with the correct dependencies. Rather than folding environment preparation into the trial-run use case, a separate use case prepares the environment, verifies it with a smoke run, and leaves the actual data-driven trial to UC-10.

## Current Decision

- UC-09 supports preparing a code-run environment for a paper or repository.
- The actor provides a paper or repository reference.
- The system ensures the source code exists in the topic workspace, inspects it for dependency hints, and updates the topic env gate (intent and derived).
- Packages are installed with Pixi using this preference order:
  1. Reuse an existing Pixi environment that already satisfies the requirements.
  2. Add required packages to an existing environment, preferring the `default` env, using `"*"` or compatible version constraints rather than exact repo-specified versions.
  3. Create a new dedicated Pixi environment if adding packages would break existing envs.
- The system creates a smoke-run script that exercises the task-critical code path and records the result.
- If source code cannot be found or dependencies are unsatisfiable, the system reports a blocker.

## Affected Artifacts

- `usecases/uc-09-prepare-code-run-environment.md`: new use case describing environment inspection, gate revision, Pixi install, and smoke-run verification.
- `usecases/README.md`: indexed UC-09.
- `README.md`: updated current-stage summary.

## Refinement History

### 2026-07-14 - Initial Decision

- Instruction: "prepare code run for paper/<repo-name-or-link>"; agent inspects repo, ensures existence, updates topic env gate (intent and derived), installs packages with pixi, creates smoke run script; preference: reuse existing pixi env, add packages to existing env (prefer `default`) without breaking, otherwise create new pixi env; use `"*"` to let pixi pick compatible versions instead of insisting on exact repo deps.
- Applied changes:
  - Created UC-09 with prepare and verify actions.
  - Defined durable outputs: `KAOJU:ENV-PREP-PLAN`, `KAOJU:ENV-GATE-REVISION`, `KAOJU:PIXI-ENV-REF`, `KAOJU:SMOKE-RUN-SCRIPT`, `KAOJU:SMOKE-RUN-RESULT`.
  - Added environment-strategy preference and version-flexibility notes.
  - Added ADR-0009.
