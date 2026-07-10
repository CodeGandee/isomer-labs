# Design

This directory contains skill-family interface and contract design notes for the Kaoju Research Extension.

## Index

| Design Doc | Purpose | Status |
| --- | --- | --- |
| [Kaoju Pipeline and Skill Family Design Overview](isomer-kaoju-pipeline/design-overview.md) | Define the public pipeline subcommands, direct peer-skill interfaces, evidence contracts, routing boundaries, external owner calls, and visible response contract. | Draft |

## Module Map

- `isomer-kaoju-pipeline`: Public named-pass coordinator; executes one bounded pass and returns one terminal report.
- `isomer-kaoju-shared`: Internal family vocabulary, context, lineage, evidence-state, and worker-output contract.
- `isomer-kaoju-workspace-mgr`: Kaoju-specific bootstrap, record-binding, material-storage, and access readiness.
- `isomer-kaoju-frame`, `discover`, `acquire`, `examine`, `reproduce`, `compare`, `audit`, and `synthesize`: Directly invokable peer skills with one primary procedure each.
- Existing operator, service, misc, Literature Provider Binding, Research Operation Extension Point, Execution Adapter, and research-record surfaces: External authorities used rather than reimplemented by Kaoju.

## Open Questions

- Whether Kaoju format profiles should be registered by a new family provider or by a family-neutral research-record provider that preserves existing DeepSci refs.
- Whether direct exploratory synthesis may waive audit, and how that waiver limits readiness language.
- Which large-material locator and cache contract should be considered sufficient for model and dataset reproducibility.
