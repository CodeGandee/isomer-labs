# deepsci-mini-scout Notifier Prompt

Inspect open mail for `deepsci-mini`. If the metadata `schema_id` is `deepsci-mini.email.handoff-request` and `receiver_role` is `deepsci-mini-scout`, use `deepsci-mini-on-handoff-request`. Process one bounded source scouting and literature note task, return `deepsci-mini.email.handoff-result` to `deepsci-mini-lead`, and stop.
