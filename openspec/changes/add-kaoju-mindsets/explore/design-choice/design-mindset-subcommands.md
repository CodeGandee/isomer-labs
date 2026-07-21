# Mindset Management Surface

## Status

Revised and accepted on 2026-07-21. Supersedes the earlier eight-leaf protected and typed-CLI management design.

## Decision

The first version exposes no public `manage-mindset`, no protected `isomer-kaoju-mindsets` manager, and no `isomer-cli ext kaoju mindsets` command group. Mindset Sources are owner-editable derived-intent JSON beneath semantic root `topic.intent.kaoju_mindsets`; users and authorized agents inspect or edit the resolved files directly.

Public Kaoju command `create-topic` and protected owner `isomer-ext-kaoju-entrypoint->topic-creator` handle initial topic derivation, create-missing repair, and explicitly requested Source regeneration or replacement. The Kaoju entrypoint also invokes the same owner lazily before a concrete mutation-bearing research Run for a topic initialized before Kaoju was installed. Generic Artifact operations store Run-scoped Mindset Records. The existing public `explore` command remains a read-only planning surface that can diagnose missing Source state and recommend `create-topic` or a concrete action but does not mutate mindset files.

## Superseded Surface

The following planned operations are removed: `mindsets defaults list`, `defaults show`, `bootstrap`, `list`, `show`, `export`, `import`, and `reset`, along with their protected leaf routes. Packaged defaults remain directly readable resources inside `isomer-kaoju-topic-creator`, and a default JSON can be copied to its deterministic topic path for modification.

## Rationale

A revisioned CLI exchange loop is unnecessary for mutable derived intent. Direct files match the ownership model and make user modification transparent. Validation, safe path resolution, create-missing preservation, and immutable Run snapshots supply the required correctness boundaries without turning a question list into Artifact state.

## Consequences

Workspace Path Resolution must expose the semantic root, the topic-creation workflow must preserve existing files by default, runtime consumers must validate exact topic files without package fallback, and Mindset Records must snapshot question content rather than depend on Source revision refs.
