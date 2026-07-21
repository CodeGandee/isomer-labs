## Context

Kaoju already separates Research Topic intent, survey framing, reading outputs, evidence records, and Workflow authority. Topic intent source files resolve below `intent/src`, while operational and exchange material derived from that intent can resolve below `intent/derived`. The initial mindset proposal treated the reusable question list as `KAOJU:MINDSET-SOURCE`, a revisioned Artifact created by generic extension bootstrap and managed through a specialized CLI. Further exploration established that the question list expresses editable topic posture and therefore belongs in derived intent, while only its materialized Run answers belong in the Artifact system.

The repository currently has a generic operator Topic Creator and no Kaoju-specific topic-creation member. The design must keep the generic creator extension-neutral, give Kaoju an explicit creation route, preserve direct user ownership of the JSON, and retain an auditable answer record after mutable Source files change.

## Goals and Non-Goals

**Goals:**

- Define Mindset Source as directly editable topic-derived intent and Mindset Record as durable Run evidence.
- Generate topic-specific Mindset Sources when the user creates or prepares a topic through the Kaoju-specific creation workflow.
- Keep validated default JSON inside the Kaoju topic-creation skill as seed material that can also be copied directly into a Topic Workspace.
- Preserve the exact Source questions and notes used by every Run even after the user edits the Source file.
- Make applicable system-skill workflows load, answer, checkpoint, and close out the selected mindset.
- Preserve existing reading Artifacts as the default destination for ordinary paper and source-code questions.

**Non-goals:**

- Add Kaoju extension behavior to the generic Topic Creator or low-level Research Topic registration.
- Register Mindset Source as an Artifact, store it in `KAOJU:ARTIFACT-LIBRARY`, or create state-DB revision history for it.
- Add specialized mindset CRUD, bootstrap, import, export, or reset CLI commands in the first version.
- Treat mindset questions or notes as Workflow Stages, commands, tool authorization, Gates, evidence, or higher-priority instructions.
- Require every topic-derived Source to retain the packaged seed's exact fixed-question count or wording.

## Decisions

### 1. Separate the Packaged Seed, Mindset Source, and Mindset Record

A **packaged mindset default** is read-only JSON shipped inside `isomer-kaoju-topic-creator`. It is a valid neutral seed and fallback for generation, not topic state and not an Artifact.

A **Mindset Source** is one current topic-owned JSON file beneath semantic root `topic.intent.kaoju_mindsets`. It contains a reusable self-questioning list for one `mindset_key`. It is derived intent and is directly user-editable. It has no semantic Artifact id, stable Artifact ref, current-state row, or revision chain.

A **Mindset Record** is a revisioned Run-scoped Artifact with semantic id `KAOJU:MINDSET-RECORD`. It materializes the exact questions and notes used by the Run, their answers and evidence, the selected survey context, explicitly Record-targeted supplemental questions, and terminal unresolved posture.

This terminology keeps “Source” distinct from the paper, repository, or evidence source under examination. “Record” identifies the mindset-specific Artifact and does not replace the generic Artifact Core Record term.

### 2. Resolve Mindset Sources Through a Semantic Derived-Intent Root

Workspace Path Resolution adds topic-scoped directory label `topic.intent.kaoju_mindsets`. Under `isomer-default.v1` it resolves to `<topic-workspace>/intent/derived/mindsets`. It uses an owner-editable durable-directory profile and reports the selected topic, path, storage profile, source, source detail, and diagnostics.

Each Source uses deterministic child filename `<mindset_key>.json`, producing the first-version defaults `paper.deep-dive.json`, `paper.skimming.json`, and `source-code.ingest.json`. Keys match `^[a-z0-9]+(?:[.-][a-z0-9]+)*$`, form exactly one safe filename segment before `.json`, and must equal the `mindset_key` inside the file. Consumers resolve the semantic root before accessing a file and never scan sibling topics, guess `intent/derived`, or search arbitrary directories.

The Mindset Source schema is closed and bounded but is not an Artifact Format Profile. It contains `schema_version`, `mindset_key`, purpose, applicability, optional derivation metadata, an ordered `questions` array, and one `additional_question_collector`. Each question and collector contains a unique `question_id`, prompt, bounded `additional_notes`, answer expectation, required posture, and evidence expectation. Optional derivation metadata can identify the topic-overview semantic label and digest and the packaged seed resource version and digest used at creation; it does not make the mutable file an Artifact or immutable record.

### 3. Give Kaoju Its Own Topic-Creation Workflow

The public Kaoju entrypoint adds command `create-topic`, invoked as `$isomer-ext-kaoju-entrypoint use create-topic to <task>`, and routes it to protected member `isomer-kaoju-topic-creator` at `isomer-ext-kaoju-entrypoint->topic-creator`.

For a new or partial topic, this owner delegates generic Project setup, Research Topic and Topic Workspace registration, and creation or clarification of `topic.intent.overview` to `isomer-op-entrypoint->topic-create`. After a concrete overview and resolved Topic Workspace exist, the Kaoju owner resolves `topic.intent.kaoju_mindsets`, loads its packaged defaults, derives missing Mindset Sources, validates them, and writes them beneath the resolved root. For an existing topic, it can create missing Sources or explicitly reconcile them without repeating ready generic creation stages.

The generic Topic Creator, low-level registration, skill installer, and non-Kaoju topic workflows remain unaware of mindset resources. Installing Kaoju does not enumerate or mutate topics because installation has neither one selected topic nor topic-mutation intent. Public welcome, help, status-only management, and `explore` requests are read-only and may report missing derived intent but do not create it.

For a topic created before Kaoju was installed or created only through the generic route, the first concrete mutation-bearing Kaoju command performs an extension-local ensure preflight before beginning its research Run. The entrypoint resolves the selected topic and overview, routes `isomer-kaoju-topic-creator` in create-missing mode, preserves every existing valid Source, creates all missing default-key Sources, and then proceeds. If the overview is missing and the request authorizes generic topic-intent preparation, Kaoju delegates only that generic prerequisite to `isomer-op-entrypoint->topic-create`; it passes no mindset schema, seed, path, or generation rule into the core skill. Insufficient topic substance, ambiguous topic selection, invalid existing Sources, or absent mutation authority pauses with an exact recovery route.

### 4. Treat the Packaged 8/6/8 JSON as Seed Content

The topic-creation bundle owns three schema-valid default resources under `assets/defaults/mindsets/`. The packaged defaults use the approved fixed inventories: eight questions for `paper.deep-dive`, six for `paper.skimming`, and eight for `source-code.ingest`. Every packaged fixed question and collector sets `additional_notes` to `""`.

The exact packaged seed questions are:

| Key | Question id | Prompt |
| --- | --- | --- |
| `paper.deep-dive` | `survey-role` | How does this paper relate to the active survey question, accepted boundary, and selected direction, and what role could it play in the survey? |
| `paper.deep-dive` | `survey-relevant-claims` | Which of the paper's claims directly answer, support, challenge, refine, or fall outside the active survey question? |
| `paper.deep-dive` | `portfolio-novelty` | Relative to works already represented in the survey, what is genuinely new, duplicative, complementary, or contradictory? |
| `paper.deep-dive` | `comparison-mechanism` | Which mechanisms, assumptions, definitions, and method components matter to the survey's comparison dimensions? |
| `paper.deep-dive` | `survey-claim-evidence` | Which exact sections, equations, figures, tables, or appendices support or challenge the survey-relevant claims, and what is my interpretation rather than a source statement? |
| `paper.deep-dive` | `evaluation-transferability` | Do the datasets, metrics, baselines, controls, and ablations test the claims under conditions that fit the survey's scope and intended comparisons? |
| `paper.deep-dive` | `boundary-limitations` | Which limitations, failure modes, contradictions, missing implementation details, or reproducibility gaps restrict how this paper can be used in the survey? |
| `paper.deep-dive` | `survey-update-and-gaps` | What updates to the survey taxonomy, comparison structure, Claim-Evidence Ledger, or reading path should I recommend, and which survey questions remain unresolved? |
| `paper.skimming` | `survey-fit` | What exact work and version am I inspecting, and how does it fit the active survey question, boundary, and selected direction? |
| `paper.skimming` | `topic-relevant-claim` | What survey-relevant problem and principal claim can I establish at the inspection depth actually achieved? |
| `paper.skimming` | `portfolio-relation` | Does this work add a new contribution, duplicate known work, complement a current category, or challenge an existing survey claim? |
| `paper.skimming` | `survey-evidence-signal` | What is the strongest visible evidence relevant to the survey, where is it located, and what evidence depth have I actually achieved? |
| `paper.skimming` | `scope-and-credibility-risk` | Which assumptions, evaluation settings, missing comparisons, contradictions, or identity and access uncertainties limit its relevance to this survey? |
| `paper.skimming` | `survey-triage` | What survey disposition should I recommend: deep dive, defer, or exclude from the current boundary, what gap would it fill, and what must be verified first? |
| `source-code.ingest` | `survey-role-and-identity` | How does this exact repository revision relate to the active survey question, selected direction, and associated works, and what are its source, license, and access posture? |
| `source-code.ingest` | `survey-relevant-architecture` | Which entrypoints and modules implement the concepts, methods, data paths, or evaluators that matter to the survey? |
| `source-code.ingest` | `claim-code-map` | Which survey-relevant paper claims, equations, or algorithms map to exact files and symbols, and what remains unmatched? |
| `source-code.ingest` | `behavior-path` | How do inputs, preprocessing, method logic, evaluation, and outputs connect for the behavior relevant to the survey? |
| `source-code.ingest` | `comparison-sensitive-configuration` | Which defaults, flags, seeds, thresholds, dependencies, hardware, datasets, or services could change the survey's interpretation or comparison? |
| `source-code.ingest` | `survey-evidence-surfaces` | What do tests, examples, benchmarks, and existing logs establish about the survey-relevant claims without executing the repository? |
| `source-code.ingest` | `paper-code-divergence` | What is missing, stale, stubbed, inconsistent, or divergent from the associated paper or the role assigned to this source in the survey? |
| `source-code.ingest` | `survey-readiness-and-risks` | What further source inspection, environment preparation, bounded trial, or reproduction should I recommend for the survey, and what blockers, side effects, or resource risks qualify that recommendation? |

Every packaged default also contains collector `additional-questions` with exact prompt “Did the user explicitly assign any additional questions to this Mindset Record that the fixed Mindset Source questions do not cover?” Its answer expectation is “Register only questions explicitly targeted to the Mindset Record. Save ordinary paper or source-code questions and findings in the applicable reading Artifacts. If no additional questions were explicitly assigned, record none.” The collector has empty `additional_notes` and does not count toward 8/6/8.

During topic creation, the agent reads `topic.intent.overview` and the relevant seed. It preserves each stable `mindset_key` and the collector contract, but it may adapt, add, remove, or replace fixed questions and may populate `additional_notes` when topic-specific concerns make that useful. Reused concepts retain seed question ids; new or concept-changing questions receive unique stable ids. Generated questions remain relative to the active survey context at use time and must not freeze a future Direction Set or Survey Contract that does not yet exist. If the overview gives no meaningful basis for specialization, copying the validated packaged default unchanged is acceptable.

### 5. Make Topic Files Directly Editable and Preserve Them by Default

A packaged default can be copied directly into the resolved mindset root and becomes a valid Mindset Source after filename, key, and schema validation. Users can view and edit the JSON with ordinary filesystem tools. No export or import round trip is required.

Explicit `create-topic`, lazy extension-local ensure, repair, retry, and package upgrade behavior is create-missing and preserve-existing. It never overwrites, deletes, or silently regenerates an existing Source, even when its content differs from the current packaged seed. A user can explicitly ask the Kaoju topic-creation owner to regenerate, replace, or reconcile one Source. Agent-directed replacement re-reads and validates the current file and digest before an atomic write and reports the changed path and digests. Direct manual edits become authoritative once validation succeeds.

Changing `topic.intent.overview` does not automatically regenerate Mindset Sources because that would overwrite later user intent. A status or applicable workflow may report derivation drift when stored optional overview provenance no longer matches, but drift is advisory until the user requests reconciliation. An invalid existing Source blocks generation or use with exact file and field diagnostics; the system does not hide it by substituting a package default.

### 6. Snapshot Mutable Sources in Run-Scoped Mindset Records

Before an applicable Run begins, the entrypoint completes the extension-local create-missing ensure described above. It then begins the Run, re-resolves and validates the selected Source, computes its digest, and creates `KAOJU:MINDSET-RECORD`. The Record stores `mindset_key`, source semantic label, safe relative path, content digest, optional derivation metadata, selected action, canonical Research Topic ref, exact current `KAOJU:SURVEY-CONTRACT` revision ref, and other present survey-context refs.

Every materialized source-question row snapshots the exact `question_id`, prompt, `additional_notes`, answer expectation, required posture, and evidence expectation before storing answer state, answer or rationale, and evidence refs. This duplication is intentional: after the mutable Source changes, the historical Record remains independently readable and auditable. Answer state is `answered`, `unresolved`, or `not_applicable`. Revisions checkpoint progress and preserve earlier states.

A Source edit after Run start does not change the active Record's snapshot or required inventory. The new Source content applies to later Runs unless the current Run is explicitly restarted. Runtime selection never falls back from a missing or invalid topic Source to the packaged seed.

### 7. Keep Explicit Supplemental Targeting and Reading-Artifact Routing

A Mindset Record can contain bounded `supplemental_questions` only after an explicit user instruction targets the Record or both the Record and Source. Each row has a Record-local id, exact prompt, empty-by-default `additional_notes`, origin of `user` or explicitly authorized `agent`, explicit association basis, introduction stage, disposition, answer state, answer or rationale, and evidence refs.

An ordinary paper or source-code question without a mindset target updates the applicable `KAOJU:SOURCE-DIGEST`, `KAOJU:CLAIM-EVIDENCE-LEDGER`, `KAOJU:ASSOCIATED-SOURCE-CODE`, or other reading Artifact. It changes neither mindset object.

An explicit Record-only request adds or revises a supplemental row with disposition `record_only`. An explicit Source-only request edits the derived-intent file and adds no row to the current Record. An explicit request for both first records `source_update_requested`; after the Source file is safely updated and validated, the row changes to `source_updated` and records the new Source digest and path. The active Run still uses its original question snapshot. A bare request to “update the mindset” pauses for Source-versus-Record clarification.

### 8. Inject Mindset Records Through Existing Workflows

Process-route metadata maps deep or full-text paper examination to `paper.deep-dive`, skim or triage examination to `paper.skimming`, and repository or source-tree examination to `source-code.ingest`. Ambiguous paper depth pauses before selection. Actions without a declared mindset requirement continue unchanged.

The mandatory injection points are:

1. `isomer-ext-kaoju-entrypoint/SKILL.md` runs extension-local create-missing ensure before the selected research Run, then begins the Run, revalidates and snapshots the selected Source, creates the Mindset Record, includes its ref in Run inputs and owner handoff, and performs the fail-closed terminal check.
2. `commands/ingest-reading-item.md` resolves inspection depth and requires the matching Mindset Record before dispatch to `isomer-kaoju-examine`.
3. `commands/ingest-source-code.md` requires the `source-code.ingest` Record before repository or source-tree examination.
4. `isomer-kaoju-examine/SKILL-MAIN.md` loads the Record snapshot, answers and checkpoints source questions during existing inspection stages, adds supplemental rows only under explicit targeting, and checks the collector at closeout.

An applicable Run cannot report `complete` or present claim-bearing examination output for acceptance until every materialized source-question and explicitly assigned supplemental row has a terminal answer state, the collector is checked, and the terminal Mindset Record ref appears in the terminal report and applicable lineage. Paused or blocked Runs preserve incomplete and unresolved rows.

### 9. Do Not Add a Mindset Management Command Tree

The first version adds no public `manage-mindset` command, protected `isomer-kaoju-mindsets` manager, or `isomer-cli ext kaoju mindsets` group. Users inspect and edit Mindset Sources at the resolved semantic path; the Kaoju `create-topic` workflow owns initial derivation, create-missing repair, and explicitly requested regeneration. Generic Artifact operations continue to store Mindset Records.

The existing public `explore` command and protected `isomer-kaoju-explore` member remain read-only planning surfaces. Welcome, help, status-only managers, and `explore` can explain the `create-topic` route or diagnose missing mindset intent, but they do not trigger lazy ensure or mutate Sources or Records.

### 10. Keep Mindset Content Low Authority and Bounded

Source and supplemental prompts and `additional_notes` are topic-owned data. They cannot authorize acquisition, execution, mutation, Gate satisfaction, evidence acceptance, provider behavior, or instruction override. Consumers apply higher-priority instructions and checked Workflow contracts first and record conflicting or impossible questions as unresolved or not applicable with rationale.

Source validation bounds file size, question count, ids, prompt and note length, answer and evidence expectations, and serialized content. It rejects executable or authority-bearing fields, unsafe filenames, key mismatch, undeclared properties, and duplicate ids. Rendering escapes user content. Mindset Record validation checks source locator fields, snapshot inventory, Run and survey context, answer states, supplemental association, path and digest syntax, and evidence relationships.

## Risks and Trade-offs

- **Mutable files lack Artifact revision history:** Mindset Records snapshot exact question content, locator, and digest so completed Runs remain auditable. Filesystem or repository history can provide additional history but is not required for correctness.
- **Agentic generation can drift from useful defaults:** packaged JSON stays schema-valid and directly copyable; generation preserves keys and the collector, validates bounded output, and can fall back to an unchanged seed when topic specialization adds no value.
- **Direct edits can create invalid JSON:** applicable workflows validate before use and fail with exact diagnostics instead of guessing or falling back.
- **A topic created before Kaoju installation or through the generic route lacks mindsets:** the first concrete mutation-bearing Kaoju command runs extension-local create-missing ensure before its research Run, while read-only requests report the state without mutation.
- **Question snapshots duplicate Source text in Records:** the duplication preserves historical meaning after mutable direct edits and is therefore required rather than denormalization to remove.

## Migration Plan

The prior Artifact-backed Mindset Source design has not been implemented, so no deployed Source records require migration. Implementation replaces those planned contracts before release:

1. Add `topic.intent.kaoju_mindsets` to Workspace Path Resolution.
2. Add `isomer-kaoju-topic-creator`, public `create-topic`, generation guidance, schema validation, and packaged default resources.
3. Add only the `KAOJU:MINDSET-RECORD` binding and renderer with exact Source snapshots.
4. Add process routes and mandatory workflow injection.
5. Update canonical domain language and documentation, then validate package and cross-skill inventories.

## Open Questions

None. The accepted first-version posture is explicit `create-topic` plus lazy extension-local create-missing ensure, no install-time or core-skill leakage, topic-adapted generation from stable packaged seeds, direct Source editing, immutable Run snapshots, and no specialized mindset management CLI.
