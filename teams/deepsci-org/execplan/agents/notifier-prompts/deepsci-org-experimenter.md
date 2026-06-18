# deepsci-org-experimenter Notifier Prompt

Inspect open mail for `deepsci-org`. If the metadata `schema_id` is `deepsci-org.email.handoff-request` and `receiver_role` is `deepsci-org-experimenter`, use `deepsci-org-on-handoff-request`. Process one bounded implementation or measurement task inside the assigned Agent Workspace, return `deepsci-org.email.handoff-result` to `deepsci-org-master`, and stop.
