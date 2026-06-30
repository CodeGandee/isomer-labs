# HPC Execution Adapter

Use this reference to handle ssh, scheduler, queue, and log evidence through isomer command surfaces. Placeholder definitions live in `../migrate/placeholders.md`.

## Workflow

When this reference is used, execute the following steps in order.

1. **Capture scheduler scripts, job ids, queue state, stdout, stderr, resource limits, module state, and output paths**.
2. **Do not treat submitted jobs as completed evidence**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this reference, the parent skill, and the available evidence, then execute the plan.

## Guidance

- Capture scheduler scripts, job ids, queue state, stdout, stderr, resource limits, module state, and output paths.
- Do not treat submitted jobs as completed evidence.
