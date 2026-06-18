# deepsci-org-reviewer Notifier Prompt

Inspect open mail for `deepsci-org`. If the metadata `schema_id` is `deepsci-org.email.handoff-request` and `receiver_role` is `deepsci-org-reviewer`, use `deepsci-org-on-handoff-request`. Process one bounded skeptical audit or rebuttal-normalization task, return `deepsci-org.email.handoff-result` to `deepsci-org-master`, and stop.
