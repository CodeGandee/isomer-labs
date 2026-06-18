# deepsci-org-master Notifier Prompt

Inspect open mail for `deepsci-org`. If the metadata `schema_id` is `deepsci-org.email.team-start`, use `deepsci-org-on-team-start`. If the metadata `schema_id` is `deepsci-org.email.handoff-result`, use `deepsci-org-on-handoff-result`. After successful event processing, use `deepsci-org-on-tick` only for one bounded follow-up pass when no Gate, pause, stop, or missing policy blocks progress. Do not wait in chat for later mail.
