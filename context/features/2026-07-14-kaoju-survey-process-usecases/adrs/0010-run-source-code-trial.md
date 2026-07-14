# Run Source Code Trial

Status: accepted
Date: 2026-07-14
Related: ADR-0003, ADR-0008, ADR-0009

Survey work often needs to verify paper claims by running the associated source code. UC-09 handles the environment preparation so that UC-10 can focus on planning and executing the trial with a chosen dataset or random data.

## Current Decision

- UC-10 supports running a source-code trial for a paper or repository.
- The actor specifies the source and whether to use data from a path or random data.
- UC-10 assumes the source code has been acquired (UC-03/UC-08) and the environment has been prepared (UC-09).
- The system produces a trial plan, implements a minimal wrapper, executes the trial, and records the run and result as durable artifacts.
- If the source code or prepared environment is missing, the system routes to the appropriate use case or reports a blocker.

## Affected Artifacts

- `usecases/uc-10-run-source-code-trial.md`: use case describing source-code trial planning and execution, assuming a prepared environment.
- `usecases/README.md`: indexed UC-10.
- `README.md`: updated current-stage summary.

## Refinement History

### 2026-07-14 - Initial Decision

- Instruction: "for this paper/<source-code-repo>, we need to test its source code, using {data in <dataset-path>, random data}".
- Originally drafted as UC-09 including environment preparation.
- Split into UC-09 (Prepare Code Run Environment) and UC-10 (Run Source Code Trial) after refinement.
- Applied changes:
  - Created UC-10 focused on planning and running the trial.
  - Removed environment-setup details from UC-10 and referenced UC-09.
  - Added ADR-0010.
