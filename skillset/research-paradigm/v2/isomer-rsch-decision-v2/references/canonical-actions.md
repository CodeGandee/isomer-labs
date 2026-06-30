# Canonical Actions

Use this reference to use a stable action vocabulary so downstream stages know what changed. Placeholder definitions live in `../migrate/placeholders.md`.

## Workflow

When this reference is used, execute the following steps in order.

1. **Allowed actions include continue, launch_experiment, launch_analysis_campaign, branch, prepare_branch, activate_branch, reuse_baseline, attach_baseline, publish_baseline, write, review, finalize, iterate, reset, stop, and request_user_decision**.
2. **Choose the smallest action that genuinely resolves the state**.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from this reference, the parent skill, and the available evidence, then execute the plan.

## Guidance

- Allowed actions include continue, launch_experiment, launch_analysis_campaign, branch, prepare_branch, activate_branch, reuse_baseline, attach_baseline, publish_baseline, write, review, finalize, iterate, reset, stop, and request_user_decision.
- Choose the smallest action that genuinely resolves the state.
