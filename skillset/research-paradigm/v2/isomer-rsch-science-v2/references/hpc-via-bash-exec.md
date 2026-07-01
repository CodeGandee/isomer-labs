# HPC Execution Adapter

Use this reference for HPC, SSH, scheduler, queue, and remote-log discipline through Isomer execution surfaces. Placeholder definitions live in `../migrate/placeholders.md`.

## Guidance

When performing this step, execute these substeps in order.

1. **Verify access and scheduler availability**. Check remote access, scheduler command, queue visibility, module state, allocation, license, and data availability before submitting work.
2. **Write a durable job script or command file**. Keep input paths, parameters, modules, environment, launch command, and expected outputs inspectable.
3. **Submit through the execution surface**. Capture scheduler job id, queue state, stdout path, stderr path, log path, and expected output paths.
4. **Record queued or running state**. Create <SCIENCE_RUN_RECORD> with queued or running status and metadata before waiting for completion.
5. **Monitor from durable logs**. Use low-frequency queue and log checks; do not infer completion from a truncated live window.
6. **Record completion and validation**. Update <SCIENCE_RUN_RECORD> with success, failed, or blocked status, then create <SCIENCE_VALIDATION_RESULT> when correctness matters.

## Preferences

- Prefer saved job ids and log paths over chat-only status.
- Prefer low-frequency monitoring for multi-hour jobs (if the job is short, otherwise still preserve logs).
- Prefer blocked package or environment records when modules, licenses, credentials, data, or allocations are missing.

## Constraints

- Queued or running jobs must not be reported as completed evidence.
- Scheduler facts, resource limits, module state, logs, and outputs must be recorded when they affect interpretation.
- Rapid polling should be avoided for long jobs.
- Completion must be checked from logs, scheduler status, and output files, not from submission success alone.

## Quality Gates

### Metrics

- HPC lifecycle coverage: fraction of remote access, scheduler availability, job script, submission, job id, queue state, log path, monitoring, completion, and validation-record steps completed; higher is better.
- Unmonitored job count: number of submitted or queued jobs without a status-reading plan and log path; lower is better.

### Checks

- Access gate: scheduler, remote access, modules, license, data, and allocation are available or blocked explicitly.
- Submission gate: job id, queue state, logs, resources, and expected outputs are recorded.
- Monitoring gate: status is read from durable scheduler and log evidence.
- Completion gate: success or failure is backed by logs and outputs.
- Validation gate: correctness checks are recorded separately when scientific validity matters.
