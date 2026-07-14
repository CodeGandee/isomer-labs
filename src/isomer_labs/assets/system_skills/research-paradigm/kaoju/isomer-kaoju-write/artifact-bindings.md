# Kaoju Write Binding Summary

The versioned package registry at `../contracts/bindings.v2.json` is the only physical binding authority. This generated summary identifies direct producer responsibility without defining paths, profiles, record kinds, labels, or expanded command shapes.

Produced semantic ids: `kaoju:paper-contract`, `kaoju:paper-structure-myst`, `kaoju:paper-template-myst`, `kaoju:paper-draft-myst`, `kaoju:paper-draft-md`, `kaoju:paper-display`, `kaoju:citation-map`, `kaoju:paper-template-export`, `kaoju:paper-template-manifest`, `kaoju:paper-revision-log`, `kaoju:paper-template-tex`, `kaoju:paper-draft-tex`, `kaoju:paper-pdf`, `kaoju:paper-compile-log`, `kaoju:paper-pdf-revision-log`, `kaoju:paper-build-run`, `kaoju:paper-validation-report`, `kaoju:publication-bundle`, `kaoju:survey-manuscript`, `kaoju:writing-template`

Resolve each contract with `isomer-cli --print-json project artifacts describe <semantic-id>`. Create accepted state with `isomer-cli --print-json project artifacts put`, revise current state with `isomer-cli --print-json project artifacts revise`, and supply only the binding-defined scope key, content, relationships, producer identity, and idempotency key.

Use `project artifacts latest`, `list`, and `show` for state-DB discovery and inspection. Treat an empty or ambiguous query as a blocker. The Artifact service owns managed locators, content validation, revision behavior, and recovery; producers never infer an internal subpath or scan directories for semantic state.
