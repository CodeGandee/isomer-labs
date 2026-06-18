# deepsci-org-analyzer Notifier Prompt

Inspect open mail for `deepsci-org`. If the metadata `schema_id` is `deepsci-org.email.handoff-request` and `receiver_role` is `deepsci-org-analyzer`, use `deepsci-org-on-handoff-request`. Process one bounded analysis, ablation, robustness, error, or claim-update task, return `deepsci-org.email.handoff-result` to `deepsci-org-master`, and stop.
