# Derived-Intent Mindset Sources

## Status

Accepted on 2026-07-21. Supersedes the earlier Artifact-backed Mindset Source and generic post-runtime extension-bootstrap design.

## Decision

A Mindset Source is a directly user-editable JSON file beneath semantic root `topic.intent.kaoju_mindsets`, which resolves by default to `<topic-workspace>/intent/derived/mindsets`. Each key maps to deterministic child `<mindset_key>.json`. Mindset Source has no Artifact semantic id, state-DB identity, or revision chain.

The protected `isomer-kaoju-topic-creator` bundle owns validated packaged defaults and teaches topic-specific generation. Public Kaoju command `create-topic` delegates generic Project, Research Topic, Topic Workspace, and `topic.intent.overview` stages to `isomer-op-entrypoint->topic-create`, then derives only missing topic Sources. Direct use of the generic Topic Creator does not generate Kaoju intent.

The same owner is triggered lazily by the Kaoju entrypoint before the first concrete mutation-bearing Kaoju research Run for one reconciled existing topic. It creates only missing Sources, then the entrypoint begins the Run and snapshots the selected Source. Installing or refreshing the Kaoju pack never scans or mutates topics. Welcome, help, `explore`, and status-only management remain read-only and only report the preparation route.

If a late-initialized topic lacks `topic.intent.overview`, Kaoju may delegate only that generic prerequisite when the request authorizes it. Mindset schemas, seeds, semantic paths, and generation rules remain entirely within the Kaoju skill family.

The packaged 8/6/8 JSON is read-only seed content. Generation preserves each key and the collector but may adapt, add, remove, or replace fixed questions and populate `additional_notes` from stable concerns in `topic.intent.overview`. It does not invent a future Direction Set or Survey Contract. An unchanged seed copy is valid when specialization adds no value.

Existing Source files remain authoritative across ordinary retry, repair, and package upgrade. Users may edit them directly or copy a packaged default to its deterministic path. Explicit regeneration or replacement revalidates the observed file and digest before atomic write. A changed topic overview produces advisory derivation drift, not automatic overwrite.

## Audit Consequence

`KAOJU:MINDSET-RECORD` snapshots every exact question, prompt, `additional_notes`, answer expectation, evidence expectation, Source path, and Source digest used by a Run. A later Source edit cannot change the active or historical Record.

## Rejected Design

The rejected design registered `KAOJU:MINDSET-SOURCE`, seeded it through generic post-runtime extension bootstrap, and managed revisions with dedicated CLI and protected subcommands. That design gave reflective topic intent unnecessary Artifact and lifecycle machinery and made the generic Topic Creator aware of extension defaults.
