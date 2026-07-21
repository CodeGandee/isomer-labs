## Why

Kaoju procedures encode action order and evidence rules, but a topic does not yet carry a user-editable set of reflective questions for how an agent should think while reading a paper, skimming a paper, or ingesting source code. These questions belong with the topic's derived intent because they express topic-specific research posture, not accepted research output or generic platform lifecycle state. A later Run still needs durable evidence of the exact questions, notes, answers, and evidence that the agent used.

## What Changes

- Add a Kaoju-specific public `create-topic` workflow owned by protected member `isomer-kaoju-topic-creator`. It delegates generic Project, Research Topic, Topic Workspace, and `topic.intent.overview` creation to the existing core Topic Creator, then derives Kaoju mindset files without adding Kaoju behavior to the core skill. The same protected owner runs in create-missing mode as a lazy extension-local preflight before the first concrete mutation-bearing Kaoju action for an existing topic.
- Add semantic directory surface `topic.intent.kaoju_mindsets`, resolving by default to `<topic-workspace>/intent/derived/mindsets`, and store one directly user-editable Mindset Source JSON file per `mindset_key` beneath that root.
- Package the approved survey-relative `paper.deep-dive`, `paper.skimming`, and `source-code.ingest` default JSON inside `isomer-kaoju-topic-creator` as read-only seed resources. The defaults retain the approved 8/6/8 question inventories, empty `additional_notes`, and explicit-Record-targeting collector, while topic-derived Sources may adapt the fixed questions and notes from `topic.intent.overview`.
- Define **Mindset Source** as the current derived-intent question file and **Mindset Record** as the Run-scoped `KAOJU:MINDSET-RECORD` Artifact that snapshots the exact Source questions and notes and records materialized answers and evidence.
- Let users inspect and modify Mindset Sources directly or copy a packaged default into the derived-intent root. Topic creation, repair, and package upgrades preserve existing Source files unless the user explicitly requests regeneration or replacement.
- Add deterministic Source resolution and validation, mandatory workflow injection, handoff, checkpoint, and closeout rules for applicable reading-item, source-code, and examination workflows. Before a research Run begins, a concrete mutation-bearing Kaoju action automatically creates missing Sources through the extension-local topic-creation owner; invalid existing Sources pause for repair, and runtime workflows never silently substitute the packaged default.
- Keep ordinary follow-up paper and source-code questions in existing Source Digest, Claim-Evidence Ledger, Associated Source Code, and related reading Artifacts unless the user explicitly targets the Mindset Source, Mindset Record, or both.
- Remove the previously proposed `KAOJU:MINDSET-SOURCE` Artifact, generic post-runtime extension bootstrap, core Topic Creator changes, protected mindset-management command tree, and specialized `ext kaoju mindsets` list, show, export, import, reset, and bootstrap operations.

## Capabilities

### New Capabilities

- `kaoju-mindsets`: Defines topic-derived Mindset Sources, packaged seeds, topic-specific generation, direct editing, Run-scoped Mindset Records, explicit supplemental-question targeting, runtime selection, and mandatory workflow injection.

### Modified Capabilities

- `packaged-system-skills`: Adds protected `isomer-kaoju-topic-creator` and its validated default mindset resources to the Kaoju package.
- `kaoju-research-extension`: Adds public `create-topic`, routes it to the Kaoju-specific owner, and requires applicable actions to resolve, inject, answer, and close out a Mindset Record without changing Workflow authority or the default destination for ordinary reading results.
- `kaoju-artifact-bindings`: Registers only the Run-scoped `KAOJU:MINDSET-RECORD` Artifact, including its derived-intent Source snapshot, answers, supplemental questions, context, and evidence relationships.
- `workspace-path-resolution`: Adds the topic-scoped semantic root for owner-editable Kaoju mindset derived intent.

## Impact

This change is based on the completed `add-kaoju-explore-subskill` artifacts and implementation state. It affects the packaged Kaoju member inventory and public command map; the new Kaoju topic-creation owner and its default JSON resources; Workspace Path Resolution; the public entrypoint, reading-item and source-code command pages, and examination guidance; `isomer_labs.kaoju` Source validators, process routes, record bindings, and renderers; canonical Isomer domain-language documentation; and unit and integration tests. It does not modify the generic Topic Creator, add a generic extension-bootstrap protocol, make skill installation scan or mutate existing topics, or add a specialized mindset-management CLI. Existing topic Mindset Source files remain authoritative across retries and package upgrades, while each Mindset Record preserves an immutable snapshot of the exact mutable Source content used by its Run.
