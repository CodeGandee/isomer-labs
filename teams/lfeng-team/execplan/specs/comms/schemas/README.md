# Comms Schemas

## Purpose

JSON Schemas for templated-mail payloads, validated by `harness email validate` before rendering.

## Contents

- `_metadata.schema.json`: the shared `houmao-email-metadata` block (loop_id + handoff_id + continuation_lane + dispatch fields).
- `task-request.schema.json`, `receipt.schema.json`, `task-result.schema.json`, `self-wakeup.schema.json`: per-family payload schemas.
