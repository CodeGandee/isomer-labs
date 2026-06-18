# Provenance

This skill adapts the DeepScientist `rebuttal` research method and rebuttal templates into a self-contained Isomer Labs skill.

The adaptation preserves reusable methodology: atomic reviewer-item normalization, comment class taxonomy, stance and route values, review matrix, item-by-item action plan, reviewer-linked evidence updates, manuscript text deltas, response letter drafting rules, supplementary evidence routing, claim-scope downgrades, and final revision handoff.

Source-runtime concepts were intentionally translated:

- lifecycle-level research work became Research Inquiry, Research Task, Research Inquiry Relationship, Run, and Workflow Stage language.
- artifact operations became Artifacts, Evidence Items, Decision Records, Gates, Provenance Records, or host Artifact APIs.
- memory operations became Findings, Evidence Items, Artifacts, or durable context queries.
- command execution became Capability Binding through an Execution Adapter.
- baseline execution policies and manuscript edit modes became Gates, Decision Records, or deliverable constraints.
- paper and rebuttal paths became paper Artifacts or semantic Artifact scopes resolved through Workspace Path Resolution when ordinary locations are needed; non-path TBD placeholders remain for unsettled APIs, schemas, providers, and policies.
- literature providers became literature search Capability Bindings with provider TBDs.

License context: the source project is licensed under Apache 2.0. Preserve this notice near this self-contained adaptation when copying, distributing, or materially revising the skill.
