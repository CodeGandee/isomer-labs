# HPC Through Execution Adapter

Isomer science skills do not embed an HPC scheduler. Operate SSH, queue, scheduler, SLURM, remote logs, and file checks through Execution Adapter Command Requests with the applicable Research Operation Extension Point, Capability Binding, Scheduler Policy, Gate Policy, workspace, and recording refs.

## Pattern

1. Verify remote access, local scheduler availability, allocation, module, license, credential, data, and Gate Policy requirements.
2. Write or identify a small job script, command file, notebook, or solver input Artifact.
3. Submit only through an approved Execution Adapter Command Request.
4. Capture job id, queue state, scheduler command, submit log, expected output paths, and remote log paths.
5. Record the job as queued or running; do not claim results from submission alone.
6. Monitor at a low-frequency cadence through status commands, log reads, file existence checks, and output schema checks.
7. On completion, record success, failure, blocked state, or warning separately from validation.
8. Record validation after outputs exist and checks pass.

## Evidence Fields

- scheduler name and version when available.
- job id or equivalent durable handle.
- submit command or script Artifact.
- input paths.
- log outputs as run log Artifacts resolved by Workspace Path Resolution.
- output paths under the accepted experiment or run-output surface.
- monitoring cadence and final status.
- validation status and caveats.

## Cautions

- Do not claim a queued job has produced results.
- Do not infer global completion from a truncated log window.
- Do not poll rapidly for multi-hour jobs.
- Treat missing modules, allocations, licenses, credentials, SSH access, or required Gate Policy decisions for private data as blockers.
- Run Gate Policy preflight when remote execution may incur cost, privacy risk, credential use, external upload, long compute, or data export, and open or record a Gate when the selected policy requires Operator Agent judgment.
