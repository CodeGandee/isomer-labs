# Kaoju Examine Binding Summary

The extension query `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT` is the binding authority. This bundle-local projection identifies direct producer responsibility without defining paths, profiles, record kinds, labels, or expanded command shapes.

Produced semantic ids: `KAOJU:SOURCE-DIGEST`, `KAOJU:CLAIM-EVIDENCE-LEDGER`

Consumed semantic id: `KAOJU:MINDSET-RECORD`. The public entrypoint produces and hands off this Run-scoped Record. Examine revises it through the binding-permitted current-state path while preserving its immutable Source snapshot.

Resolve each contract with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`. Create accepted state with `isomer-cli --print-json project artifacts put`, revise current state with `isomer-cli --print-json project artifacts revise`, and supply only the binding-defined scope key, content, relationships, producer identity, and idempotency key.

Use `project artifacts latest`, `list`, and `show` for state-DB discovery and inspection. Treat an empty or ambiguous query as a blocker. The Artifact service owns managed locators, content validation, revision behavior, and recovery; producers never infer an internal subpath or scan directories for semantic state.
