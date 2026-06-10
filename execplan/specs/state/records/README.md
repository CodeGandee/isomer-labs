# State Record Schemas

## Purpose

JSON Schemas for `record apply` / `record validate` payloads — the ONLY write path into the platform
DB `runs/state.sqlite`. Each schema mirrors a `schema.sql` table family and enforces the field shapes,
enums (matching the SQL CHECK constraints), and discriminators the harness needs before applying a row.
Transition rules (allowed status changes, gated-decision confirmation) are enforced by the harness on
top of schema validity; idempotency is by `record_id`.

## Envelope

Every payload is `{ record_type, record_id, at, ... }`:
- `record_type` — discriminator, `"<family>.<op>"` (e.g. `quest.create`, `handoff.advance`).
- `record_id` — idempotency key (the affected row's primary key; composite keys are joined with `:`).
- `at` — caller-supplied ISO-8601 timestamp (the schema never generates time).

`_envelope.schema.json` is the authority for these common fields; family files embed them for
self-contained validation.

## Contents (record families)

- `quest.schema.json` — quest.create | quest.update
- `round.schema.json` — round.open | round.update | round.close
- `branch.schema.json` — branch.record
- `participant.schema.json` — participant.register
- `idea.schema.json` — idea.upsert
- `experiment.schema.json` — experiment.upsert
- `result.schema.json` — result.record | measurement.record
- `analysis.schema.json` — analysis.record
- `claim.schema.json` — claim.upsert | claim_evidence.link | claim_evidence.resolve
- `decision.schema.json` — decision.record | decision.confirm
- `finding.schema.json` — finding.add
- `reference.schema.json` — reference.record
- `search-space.schema.json` — search_space.define | experiment_param.record
- `handoff.schema.json` — handoff.open | handoff.advance
- `wakeup.schema.json` — wakeup.arm | wakeup.attach | wakeup.resolve
- `artifact.schema.json` — artifact.record
- `operator-event.schema.json` — operator_event.record
- `quirk.schema.json` — quirk.append
- `knowledge-pack.schema.json` — knowledge_pack.register (domain-pluggable extension)
- `intake.schema.json` — intake_asset.record (intake-audit entry path)
- `frontier.schema.json` — frontier.record (optimize stage)
- `finalize.schema.json` — finalize.record (complete | stop | park | publish_and_continue)
