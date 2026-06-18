# Provenance

This skill adapts the DeepScientist `review` research method and review templates into a self-contained Isomer Labs skill.

The adaptation preserves reusable methodology: independent skeptical audit, evidence authenticity checks, manuscript coverage gates, literature benchmarking, review-report structure, revision-log structure, follow-up evidence TODOs, publishability stop-loss, and route discipline.

Source-runtime concepts were intentionally translated:

- lifecycle-level research work became Research Inquiry, Research Task, Research Inquiry Relationship, Run, and Workflow Stage Cursor language.
- artifact operations became Artifacts, Evidence Items, Decision Records, Gates, Provenance Records, or host Artifact APIs.
- memory operations became Findings, Evidence Items, Artifacts, or durable context queries.
- command execution became Capability Binding through an Execution Adapter.
- review follow-up policies became Gates or Decision Records.
- paper paths, review packet paths, and generated layouts became paper Artifacts or semantic Artifact scopes resolved through Workspace Path Resolution when ordinary locations are needed; non-path TBD placeholders remain for unsettled APIs, schemas, providers, and policies.
- literature providers became literature search Capability Bindings with provider TBDs.

License context: the source project is licensed under Apache 2.0. Preserve this notice near this self-contained adaptation when copying, distributing, or materially revising the skill.
