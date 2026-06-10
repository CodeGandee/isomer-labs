# Comms Specs

## Purpose

Generated templated-mail contracts for the DeepResearch loop: the message families participants
exchange, their payload schemas, and their Markdown renderers. Authority for the harness `email`
commands and the generated on-event skills.

## Contents

- `templates.toml`: the mail-family registry (name -> schema_id -> schema -> renderer -> reply expectation -> state effect).
- `schemas/_metadata.schema.json`: the shared `houmao-email-metadata` block carried by every mail (loop_id + handoff_id + continuation_lane + dispatch fields).
- `schemas/task-request.schema.json`, `schemas/receipt.schema.json`, `schemas/task-result.schema.json`, `schemas/self-wakeup.schema.json`: per-family payload schemas.
- `renderers/<family>.md.j2`: per-family Markdown renderers (emit the metadata block + a human-readable body).
