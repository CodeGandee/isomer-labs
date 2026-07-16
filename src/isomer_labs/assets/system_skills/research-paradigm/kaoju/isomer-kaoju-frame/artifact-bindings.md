# Kaoju Frame Binding Summary

The extension query `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT` is the binding authority. This bundle-local projection identifies direct producer responsibility without defining paths, profiles, record kinds, labels, or expanded command shapes.

Produced semantic ids: `KAOJU:SURVEY-CONTRACT`, `KAOJU:DIRECTION-SET`, `KAOJU:COMPARISON-INTENT`

Resolve each contract with `isomer-cli --print-json ext kaoju bindings describe KAOJU:WHAT`. Create accepted state with `isomer-cli --print-json project artifacts put`, revise current state with `isomer-cli --print-json project artifacts revise`, and supply only the binding-defined scope key, content, relationships, producer identity, and idempotency key.

The active `KAOJU:DIRECTION-SET` write binding is idea-bearing v2. Its authoritative payload must include actor-confirmed per-proposal canonical ids, exact paths, one generation, authored option outcomes and rationale, and atomic `research_idea_effects`. Legacy v1 records remain readable migration inputs, not the default shape for new writes.

Use `project artifacts latest`, `list`, and `show` for state-DB discovery and inspection. Treat an empty or ambiguous query as a blocker. The Artifact service owns managed locators, content validation, revision behavior, and recovery; producers never infer an internal subpath or scan directories for semantic state.
