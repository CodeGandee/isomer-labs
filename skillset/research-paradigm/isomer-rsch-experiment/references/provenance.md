# Provenance

This skill adapts the DeepScientist `experiment` research method and reference material into a self-contained Isomer Labs skill.

The adaptation preserves reusable methodology: main experiment plans, checklists, evidence ladder, run contracts, preflight checks, smoke and pilot discipline, long-running monitoring, output validation, run records, evaluation summaries, failure handling, and next-route decisions.

Source-runtime concepts were intentionally translated:

- execution became Runs through Capability Bindings and Execution Adapters.
- run logs became Run log Artifacts, Evidence Items, or Provenance Records.
- metric contracts became metric contract Artifacts, Evidence Items, or Gates.
- long-running monitoring became Signal Observations, Completion Watcher Contract notes, and Provenance Records.
- evaluation summaries became Research Claim updates, Evidence Items, and Decision Record summaries.
- artifact operations became Artifacts, Evidence Items, Decision Records, Gates, Provenance Records, or host APIs.
- memory operations became Findings, Evidence Items, Artifacts, or durable context queries.
- command execution became Capability Binding through an Execution Adapter with `[[tbd-surface:api-execution-command]]`.

License context: the source project is licensed under Apache 2.0. Preserve this notice near this self-contained adaptation when copying, distributing, or materially revising the skill.
