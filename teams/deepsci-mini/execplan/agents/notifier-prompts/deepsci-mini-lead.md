# deepsci-mini-lead Notifier Prompt

Inspect open mail for `deepsci-mini`. If the metadata `schema_id` is `deepsci-mini.email.team-start`, use `deepsci-mini-on-team-start`. If the metadata `schema_id` is `deepsci-mini.email.handoff-result`, use `deepsci-mini-on-handoff-result`. After a successful event, use `deepsci-mini-on-tick` only for one bounded scheduling or closeout pass when no Gate blocks progress. Unknown or malformed mail should be reported for operator repair.
