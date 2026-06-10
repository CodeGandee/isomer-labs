# Notifier Prompts

## Purpose

Per-agent mail-notification prompt appendices. On a notifier wakeup the agent inspects the in-body
`houmao-email-metadata` block, dispatches by `schema_id` to the matching generated on-event skill,
does ONE bounded turn, then stops (no in-chat waiting). In `manual` mode the same bounded-pass shape
applies, prompted by the operator instead of the notifier.

## Contents

- `<agent-id>.md`: the notifier prompt appendix for that agent.
