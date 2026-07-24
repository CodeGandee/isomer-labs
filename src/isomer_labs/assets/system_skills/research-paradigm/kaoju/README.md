# Kaoju Research Skills

Kaoju (考据) is Isomer Labs' evidence-led survey extension. It treats papers and technical reports as primary related works, links repositories and datasets as typed materials, and supports governed first-hand code trials without confusing a capability probe with reproduction evidence.

## Public Pack and Protected Inventory

| Identity or Route | Responsibility |
| --- | --- |
| `isomer-ext-kaoju-entrypoint` | Public pack that routes one user intent or retained compatibility procedure and preserves its Run checkpoint. |
| `isomer-ext-kaoju-entrypoint->topic-creator` | Derive, preserve, inspect, regenerate, replace, or reconcile topic-owned Kaoju Mindset Sources after generic topic state exists. |
| `isomer-ext-kaoju-entrypoint->shared` | Define Artifact, evidence, identity, lineage, Gate, Service Request, and terminal contracts. |
| `isomer-ext-kaoju-entrypoint->workspace` | Validate Topic Workspace, binding registry, state DB, scoped current state, and reset readiness. |
| `isomer-ext-kaoju-entrypoint->frame` | Propose and confirm survey directions and freeze the distinct Survey Contract. |
| `isomer-ext-kaoju-entrypoint->paper-search` | Execute one bounded provider-neutral paper retrieval action through an agent-selected external approach and record one normalized provider-output observation. |
| `isomer-ext-kaoju-entrypoint->discover` | Build direction-scoped, version-aware reading lists and discovery provenance. |
| `isomer-ext-kaoju-entrypoint->explore` | Run bounded read-only evidence-led exploration before a durable survey procedure is selected. |
| `isomer-ext-kaoju-entrypoint->acquire` | Resolve materials and source relationships, orchestrate external repository acquisition, verify immutable identity, then register and record accepted evidence. |
| `isomer-ext-kaoju-entrypoint->examine` | Inspect papers and code at exact locators while separating source statements from interpretation. |
| `isomer-ext-kaoju-entrypoint->reproduce` | Handle only genuine reproduction claims under the stronger fidelity contract. |
| `isomer-ext-kaoju-entrypoint->compare` | Build source-grounded theory or governed empirical comparisons. |
| `isomer-ext-kaoju-entrypoint->audit` | Diagnose coverage, identity, evidence, contradiction, and fairness defects. |
| `isomer-ext-kaoju-entrypoint->synthesize` | Write accepted survey conclusions without exceeding the evidence boundary. |
| `isomer-ext-kaoju-entrypoint->write` | Maintain canonical MyST paper state and derived Markdown, TeX, PDF, and publication outputs. |
| `isomer-ext-kaoju-entrypoint->trial` | Prepare governed environments and run separately approved bounded source-code trials. |
| `isomer-ext-kaoju-entrypoint->export` | Export accepted state-DB records to the package-owned LLM Wiki representation and viewer. |

## User-Intent Surface

The public entrypoint accepts `$isomer-ext-kaoju-entrypoint use <subcommand> to <task>`. It exposes eleven survey intents in order: `create-topic`, `choose-directions`, `build-reading-list`, `ingest-reading-item`, `draft-paper`, `manage-paper-template`, `build-paper-pdf`, `export-survey-wiki`, `ingest-source-code`, `prepare-code-run`, and `run-code-trial`.

Retained compatibility procedures are `landscape-pass`, `curated-intake-pass`, `direction-expansion-pass`, `theory-comparison-pass`, `method-trial-pass`, `comparative-pass`, `audit-survey-pass`, `paper-pass`, and `create-paper-template`. `method-trial-pass` routes ordinary bounded trials to `isomer-kaoju-trial`; `paper-pass` composes MyST drafting with an optional PDF stage; `create-paper-template` constructs a mutable named content template. `manage-paper-template` resolves content versus LaTeX role before managing either namespace.

## Durable State and CLI Boundaries

The extension-owned resources queried by `isomer-cli ext kaoju process show`, `ext kaoju bindings list`, and `ext kaoju bindings describe KAOJU:WHAT` are the process, semantic, and binding authorities. Skills discover ordinary durable state through typed query surfaces and persist ordinary bindings through typed `put` or `revise`. Mutable named templates use only `ext kaoju paper template`. File content remains authoritative, while the Topic Workspace state DB owns semantic discovery, scope, current-state resolution, lineage, and stable refs. Producers must not infer managed subpaths, read package files directly, scan directories as a fallback, edit SQL, or mutate managed content directly.

Paper retrieval has a separate execution and ownership boundary. `paper-search` invokes a bound external provider tool directly and maps the result into one `isomer-literature-provider-observation.v1` Artifact. Semantic Scholar is one bundle-local approach. `discover` retains strategy, candidate disposition, version-family, Discovery Ledger, and Reading List ownership; `acquire` and `examine` retain material and source-evidence ownership. `isomer-cli ext research literature` only validates, records, indexes, and queries local normalized data and never invokes a provider.

Kaoju topic creation keeps packaged 8/6/8 mindset defaults inside the protected topic-creator bundle and copies or specializes them into `topic.intent.kaoju_mindsets` only after one concrete `topic.intent.overview` exists. These directly editable JSON files are Mindset Sources, a derived-intent question list with `additional_notes`, not Artifacts or Workflows. An applicable paper or source-code examination records one immutable Run mindset resolution before focused work. A present valid Source becomes a Run-scoped `KAOJU:MINDSET-RECORD` that preserves exact questions, notes, survey context, answers, evidence, collector posture, and unresolved state after later Source edits. A missing deterministic Source becomes Run database disposition `skipped_source_missing`; no placeholder Record is created, and the workflow proceeds without mindset reflection. Installation, read-only routes, and concrete research actions never create missing Sources implicitly; use explicit Kaoju `create-topic` when those files are wanted.

`isomer-cli project runs` owns resumable procedure checkpoints. The acting user or agent runs prompt-sensitive repository commands outside Isomer, verifies the resulting source and immutable identity, then uses `project repos register` for topology and typed Artifacts for research provenance. `project service-requests` records and synchronously dispatches Service Team work. Pixi, smoke, code-trial, document-build, and viewer operations use provider-neutral Execution Adapter Command Requests.

Houmao may implement Service Dispatch Forms, launch, mailboxes, or inspection behind those boundaries. Houmao terms and payloads do not appear in the Kaoju schema, skill-facing Artifact contract, or public CLI language.

## Canonical Paper Graph

```text
accepted audit and synthesis
            |
 content template main or explicit name
 stable ref + state token + observed digest
            |
   paper-structure-myst
            |
      paper-draft-myst ----------------> paper-draft-md
            |                               derived review view
            |
 independent LaTeX template main or explicit name
 stable ref + state token + observed digest
            |
 exact paper-template-tex snapshot
            |
   self-contained paper-draft-tex
                          |
                 agent inspection and repair
                          |
                      paper-pdf
```

MyST is the only canonical paper source. Content templates define MyST authoring structure; independent multi-file LaTeX templates define presentation. Each role owns its own `main`, stable refs, state tokens, exports, and updates. Figures and tables remain separate file-backed `KAOJU:PAPER-DISPLAY` Artifacts. TeX snapshots, composed drafts, compile logs, PDFs, and viewer directories retain checksummed manifests and lineage to exact content and presentation inputs.

## Reset and Resume Semantics

A reset is a checkpoint decision, not a filesystem cleanup. The pipeline queries the state DB and retains accepted selected directions, direction-scoped reading lists, approved source digests, canonical paper revisions, wiki manifests, exact Pixi environment refs, and immutable trial results unless the actor explicitly archives or revises them. It resumes at the first incomplete stage after validating content links, current scope, pending Gates, blockers, Service Requests, and prior Run terminal state. Failed and rejected attempts remain visible; a later repair never overwrites their evidence or verdict.

## Prerequisite Recovery Example

Suppose the user asks, “Build the survey PDF,” but the Topic has no accepted audit, synthesis, or canonical MyST draft. The ordinary request pauses before those producers run. The response identifies the missing refs, recommends audit followed by any bounded repair, synthesis, drafting, and local PDF construction, then offers four choices: run to the PDF target, execute only the next prerequisite, inspect or choose another route, or stop.

If the user chooses “run to the PDF target,” the current agent maintains a prompt-scoped dependency plan. Audit, each required repair, a fresh audit, synthesis, drafting, and PDF construction retain separate procedure Runs, callbacks, checkpoints, Artifacts, and terminal reports. The controller consumes routine in-closure recovery routes only after refreshing durable state. It still pauses for evidence-scope choices, structure acceptance, unexpected dependencies or resource use, build authorization, the publication Gate, and any external publication or submission. Once the validated local PDF target completes, traversal stops; it does not publish or start later recommended work.

## Migration

Legacy `KAOJU:SURVEY-MANUSCRIPT`, `KAOJU:WRITING-TEMPLATE`, and historical `KAOJU:PAPER-TEMPLATE-TEX` records remain readable and never redefine canonical MyST. New named stock uses `ext kaoju paper template --kind content|latex`. Each role-local name owns one stable record and managed tree. Updates require the current opaque token and emit kind-qualified audit evidence. Working copies resolve to `<topic.paper.template_exchange_root>/content/<name>/` or `/latex/<name>/`. Contract migration annotates existing content records in place and adopts LaTeX only by copying one exact actor-selected historical tree with checked composition metadata. The source and all paper-line snapshots remain unchanged. The independently implemented wiki exporter and viewer are package resources and never invoke an external `imsight-llm-wiki` skill.

## Installation

Install the optional extension with `isomer-cli system-skills install --target <target> --extension kaoju`. The selector installs the public core pack and the complete Kaoju public pack with all 16 protected members. Installation does not enumerate Research Topics or initialize Mindset Sources. DeepSci stays absent unless selected separately or all extensions are requested. Refresh the agent host or start a new session before claiming current-session availability.
