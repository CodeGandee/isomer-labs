# Record Normalized Literature Observations

Agents receive provider-shaped output when they invoke external paper-search tools directly. Before asking Isomer to record a result, the paper-search approach will convert that output into a provider-neutral literature observation; `isomer-cli` will validate, record, and index the normalized observation without interpreting provider-specific response fields.

## Status

Accepted.

## Considered Options

- Require normalized observations and allow redacted raw responses as optional attachments.
- Require both normalized observations and all raw provider responses.
- Store raw provider responses and normalize them later.
- Teach `isomer-cli` to normalize provider-specific responses during recording.

## Consequences

- The paper-search skill and its selected provider approach own provider-specific field mapping, missing-field handling, null-record handling, pagination consolidation, and normalization.
- The canonical provider-output Artifact uses a provider-neutral schema.
- Literature query indexes consume only normalized fields and do not depend on S2 or another provider payload shape.
- Redacted raw provider responses may be retained as optional file-backed attachments with media type, checksum, and provenance references.
- Raw attachments are not required for a valid observation and are not indexed as canonical paper metadata.
- Credentials, authorization headers, secret query values, and other sensitive material must be removed before any raw attachment is recorded.
- `isomer-cli` does not gain provider-specific normalizers or provider invocation behavior.
