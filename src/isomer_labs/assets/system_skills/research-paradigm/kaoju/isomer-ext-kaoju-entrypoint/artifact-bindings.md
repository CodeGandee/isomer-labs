# Kaoju Pipeline Binding Summary

The extension query `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT` is the binding authority. This bundle-local projection identifies direct producer responsibility without defining paths, profiles, record kinds, labels, or expanded command shapes.

Produced semantic ids: `KAOJU:PROCEED-DECISION`, `KAOJU:MINDSET-RECORD`, `KAOJU:SURVEY-TERMINAL-REPORT`

`KAOJU:MINDSET-RECORD` is Run-scoped current state produced only for a `recorded` Run mindset resolution. It requires `run` and `survey_contract` relationships, exact Source snapshot fields, terminal answer states, collector posture, and optimistic revisions that preserve the immutable snapshot. A `skipped_source_missing` Run records Source and Record absence in Run state and creates no placeholder Artifact. A topic Mindset Source is not a produced semantic id or Artifact.

Resolve each contract with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`. Create accepted state with `isomer-cli --print-json project artifacts put`, revise current state with `isomer-cli --print-json project artifacts revise`, and supply only the binding-defined scope key, content, relationships, producer identity, and idempotency key.

Use `project artifacts latest`, `list`, and `show` for state-DB discovery and inspection. Treat an empty or ambiguous query as a blocker. The Artifact service owns managed locators, content validation, revision behavior, and recovery; producers never infer an internal subpath or scan directories for semantic state.
