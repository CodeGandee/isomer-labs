## Context

Workspace Runtime already stores topic-scoped lifecycle records in `state.sqlite`, and `isomer-cli ext research records` can create generic records with optional Markdown or file-backed bodies. The v2 research skills now expose placeholder binding pages that tell agents which record kind, semantic label, format profile, and research-record command shape to use, but those command shapes still ask the agent to author body files directly.

That write path is the problem. Markdown bodies are readable for humans, but they are a poor source of truth for a GUI or for later graph indexing. This change establishes a clean forward-only structured record layer before the graph-index change adds relationships. Current generated topic workspaces under `isomer-content/` are not migration inputs for this design and can be discarded.

The key scope expansion is that "check JSON against schema" and "fill a Jinja2 template from JSON" are not DeepScientist-specific operations. They should become a top-level Isomer artifact-format processing capability. DeepScientist remains an extension-owned provider of format profiles, JSON Schemas, and Jinja2 templates for DeepScientist-style research records.

## Goals / Non-Goals

**Goals:**

- Add a generic artifact-format processing engine that validates JSON payloads with JSON Schema and renders Jinja2 templates from JSON.
- Support format-profile refs, direct schema/template refs, topic-registered custom formats, and plain `--schema-file` / `--template-file` inputs.
- Use explicit ref naming that distinguishes Isomer-owned formats from user-registered formats: `{isomer,custom}:<topic-or-extension-slug>/<primary-group>/<subgroup>/.../<template-name>`.
- Make validated JSON payloads the authoritative source for accepted v2-produced research records.
- Let `isomer-cli ext research records validate`, `create`, and `update` use the generic artifact-format engine before storing accepted structured records.
- Store enough structured state in Workspace Runtime for future GUI surfaces to list records by format profile, schema ref, template ref, source ref kind, validation status, render status, lifecycle refs, and core metadata without parsing Markdown.
- Keep DeepScientist record-format assets under the DeepScientist extension package, while keeping the validation/rendering engine extension-neutral.
- Prepare clean input nodes for the later research record graph index without implementing graph edges in this change.

**Non-Goals:**

- Do not add graph edge tables, lineage traversal, route queries, or file attachment indexes in this change.
- Do not migrate, backfill, import, classify, or preserve current generated `isomer-content/` artifacts.
- Do not scrape Markdown bodies as authoritative structured records.
- Do not design a legacy body-file compatibility layer for v2 structured artifacts.
- Do not make Artifact Format Profiles contain executable Python validators or renderers.
- Do not design the future GUI; this change only provides the queryable record substrate it will need.
- Do not make every JSON field relational; store validated payload JSON with stable indexed summary fields.

## Decisions

### Promote Artifact Format Processing to Isomer Core

Add a core package, likely:

```text
src/isomer_labs/artifact_formats/
  models.py
  resolver.py
  registry.py
  validation.py
  rendering.py
```

Core responsibilities:

- Resolve format profiles, schema refs, and template refs from registered providers.
- Validate JSON payloads with `jsonschema`.
- Render Jinja2 templates from validated JSON payloads.
- Return deterministic diagnostics for missing refs, invalid refs, schema failures, template load failures, and render failures.
- Support direct plain-path inputs for validate/render operations.
- Snapshot plain-path schema/template inputs when a durable record is created from them.

Research records should call this engine; they should not own schema resolution or Jinja2 rendering logic. DeepScientist should call or register with this engine; it should not fork a separate validation/rendering implementation.

Alternative considered: keep validation/rendering inside `deepsci_ext` or `research_records.py`. That would solve the immediate v2 record problem, but the same machinery is useful for other Isomer artifacts, custom reports, future GUI views, and non-DeepScientist extensions. Core ownership is cleaner.

### Keep Format Content Owned by Providers

The core engine owns processing, not every format definition. Providers own profiles, schemas, and templates:

- Isomer package or extension assets use `isomer:` refs.
- User or Topic Workspace registered assets use `custom:` refs.
- Plain files can be used ad hoc and are snapshotted when they become durable record dependencies.

DeepScientist is one provider. Place its first structured record profiles, schemas, and Markdown Jinja2 templates under:

```text
src/isomer_labs/deepsci_ext/assets/record_formats/
  profiles/
    run.main-run-record.v1.json
    evidence.experiment-result-summary.v1.json
    decision.experiment-route-decision.v1.json
    handoff.*.v1.json
    control.*.v1.json
    figure.*.v1.json
    report.*.v1.json
    paper.*.v1.json
    nature-data.*.v1.json
    presentation.*.v1.json
    finalize.*.v1.json
  schemas/
    run.main-run-record.v1.schema.json
    evidence.experiment-result-summary.v1.schema.json
    decision.experiment-route-decision.v1.schema.json
    handoff.*.v1.schema.json
    control.*.v1.schema.json
    figure.*.v1.schema.json
    report.*.v1.schema.json
    paper.*.v1.schema.json
    nature-data.*.v1.schema.json
    presentation.*.v1.schema.json
    finalize.*.v1.schema.json
  templates/
    markdown/
      run.main-run-record.v1.md.j2
      evidence.experiment-result-summary.v1.md.j2
      decision.experiment-route-decision.v1.md.j2
      handoff.*.v1.md.j2
      control.*.v1.md.j2
      figure.*.v1.md.j2
      report.*.v1.md.j2
      paper.*.v1.md.j2
      nature-data.*.v1.md.j2
      presentation.*.v1.md.j2
      finalize.*.v1.md.j2
```

The initial DeepScientist shipping scope is the full active v2 accepted-output set, not a small pilot. The provider should cover the profile families used by active v2 placeholder bindings at implementation time, including run, evidence, decision, handoff/control, figure, report, paper, Nature-specific, presentation, and finalization outputs. Closely related placeholders may share a reusable family schema or template when that preserves the payload contract, but every active v2 structured placeholder must resolve to an explicit `isomer:deepsci/record-format/*` profile before the change is complete.

Add a DeepScientist provider module, likely `src/isomer_labs/deepsci_ext/record_formats.py`, that registers DeepScientist refs with the core artifact-format registry and loads package resources.

Alternative considered: place DeepScientist record formats under `src/isomer_labs/assets/` as generic built-ins. That would make them look platform-wide even though they encode DeepScientist research-method outputs. Keeping content under `deepsci_ext` makes ownership and future replacement clearer.

### Use Canonical Format Ref Naming

Use this recommended ref pattern:

```text
{isomer,custom}:<topic-or-extension-slug>/<primary-group>/<subgroup>/.../<template-name>
```

For DeepScientist extension-owned formats:

```text
isomer:deepsci/record-format/profile/run/main-run-record/v1
isomer:deepsci/record-format/schema/run/main-run-record/v1
isomer:deepsci/record-format/template/markdown/run/main-run-record/v1
```

For user-registered Topic Workspace formats:

```text
custom:flash-attention-gb10/record-format/profile/experiment/ablation-report/v1
custom:flash-attention-gb10/record-format/schema/experiment/ablation-report/v1
custom:flash-attention-gb10/record-format/template/markdown/experiment/ablation-report/v1
```

`isomer:` means the format is shipped or registered by Isomer package code, including extension packages. In this first release, `custom:` means the format is registered by a user into one selected Topic Workspace. The first path segment is the topic or extension slug. The remaining path segments identify the primary group, subgroups, and name.

Alternative considered: use one URI scheme per provider or per registration source. That makes each provider obvious, but it does not scale as well as a stable origin-prefix pattern with hierarchical path groups.

### Support Topic-registered Formats

Add a registration surface for custom Topic Workspace formats. A likely command shape is:

```bash
isomer-cli project artifact-formats register \
  --format-profile custom:flash-attention-gb10/record-format/profile/experiment/ablation-report/v1 \
  --schema-file ./formats/ablation.schema.json \
  --template-file ./formats/ablation.md.j2 \
  --format markdown
```

Registration should copy or snapshot the schema/template/profile material into a managed Topic Workspace runtime surface, conceptually:

```text
<topic-workspace>/runtime/artifact-formats/
  profiles/
  schemas/
  templates/markdown/
```

The persisted registration should store the chosen refs, original source paths when known, digests, timestamps, actor/provenance refs, and validation diagnostics. The engine then resolves `custom:` refs from the selected Topic Workspace's Workspace Runtime registration state and managed snapshots, not from arbitrary mutable source paths.

Custom format registration is Topic Workspace scoped in this release. A `custom:` ref resolves only within the selected Effective Topic Context and selected Topic Workspace; another topic must register or snapshot its own copy before it can use the same format content. Project-level shared custom format registries are deferred to a later change, likely as an explicit promotion or copy workflow that preserves per-topic reproducibility.

Alternative considered: let `custom:` refs always point at user-authored files in place. That makes registration easy but weakens reproducibility: a durable record could later render differently after a local file edit.

### Support Plain Schema and Template Paths

The generic engine should support plain path inputs for ad hoc validation and rendering:

```bash
isomer-cli project artifact-formats validate \
  --schema-file ./schema.json \
  --payload-file ./payload.json

isomer-cli project artifact-formats render \
  --schema-file ./schema.json \
  --template-file ./report.md.j2 \
  --payload-file ./payload.json \
  --format markdown
```

For read-only validate/render commands, the plain paths can remain plain. Generic render commands accept an optional output path. If no output path is supplied, the command prints the rendered content to the console; when `--print-json` is used, the rendered content is carried in the deterministic JSON response. For durable research record creation, plain-path schema/template inputs must be snapshotted into Workspace Runtime and recorded with generated `custom:` refs plus digests. This keeps one-off authoring convenient without letting durable records depend on mutable ad hoc files.

Alternative considered: require every schema/template to be registered before use. That is cleaner for durable workflows, but it slows down exploratory authoring and makes quick local validation awkward.

### Keep Artifact Format Profiles Declarative

Artifact Format Profiles describe content expectations and point to schemas/templates. They remain declarative. The engine interprets profile metadata and invokes generic JSON Schema and Jinja2 processing. Profiles do not contain executable Python validators, custom render code, provider calls, or adapter-specific runtime behavior.

If a profile names an unsupported schema ref, template ref, media type, renderer hint, or schema version, the engine returns deterministic diagnostics and does not create an accepted structured payload.

Alternative considered: allow profile-local executable validators or renderers. That would make profiles powerful, but it would blur content contracts with code execution and make skills much harder to package safely.

### Use Explicit CLI Names

Prefer `--format-profile` over a bare `--profile` in new command surfaces. Isomer already has Agent Profile and Topic Agent Team Profile concepts, so `--profile` is too easy to misread. The research-record command may keep aliases only if needed for compatibility during implementation, but documentation and v2 bindings should use `--format-profile`.

Core command shapes:

```bash
isomer-cli project artifact-formats validate \
  --format-profile isomer:deepsci/record-format/profile/run/main-run-record/v1 \
  --payload-file payload.json

isomer-cli project artifact-formats render \
  --format-profile isomer:deepsci/record-format/profile/run/main-run-record/v1 \
  --payload-file payload.json \
  --format markdown
```

Research-record command shapes:

```bash
isomer-cli ext research records create \
  --record-kind run \
  --format-profile isomer:deepsci/record-format/profile/run/main-run-record/v1 \
  --payload-file payload.json \
  --render markdown
```

`create` and `update` do not render Markdown implicitly just because the selected profile has a Markdown template. Callers request Markdown materialization with `--render markdown`. When rendering is omitted, the accepted structured payload can still be stored with render status such as `not_requested`, and no generated Markdown file is written. Active v2 placeholder bindings should include `--render markdown` when the durable artifact is expected to have a human-readable Markdown view.

Alternative considered: keep `--profile` everywhere. That is shorter, but it hides the distinction between an Artifact Format Profile and the other profile concepts in the Isomer domain language.

### Use a Draft-Validate-Record-Render Flow

The intended research-record write path is:

```text
agent drafts JSON payload
isomer-cli validates the payload through the core artifact-format engine
agent fixes validation errors until the payload fits
isomer-cli records lifecycle row and structured payload row in Workspace Runtime
isomer-cli renders Markdown from the payload and profile-selected Jinja2 template
generated Markdown is written under the resolved durable semantic record surface
```

`validate` performs validation and optional render preflight without mutation. `create` and `update` perform validation and mutation in one transaction for runtime state. When `--render markdown` is present, they also render deterministic Markdown from the validated payload and materialize the generated view. If rendering fails after payload validation, the command reports the failure and does not mark the structured payload as rendered.

Rendering during `create` or `update` is explicit. A valid create or update request without `--render markdown` records the structured payload but does not write a Markdown view. This keeps durable storage separate from file materialization while still letting v2 bindings request both steps in one command.

Alternative considered: let agents write Markdown first and have the CLI extract JSON from front matter. That keeps the visible authoring format familiar, but it recreates the parsing problem and makes schema repair vague. JSON-first authoring gives precise diagnostics.

### Let Placeholder Bindings Name Generated Views

Generated Markdown file naming for durable structured research records is controlled by the active placeholder binding row. The binding owns the default generated content name because the placeholder knows the domain role, skill, producer/consumer context, and expected human-facing artifact name. Artifact Format Profiles stay reusable across placeholders and topics; they should not hard-code topic-workspace file names.

The CLI may accept an explicit generated-output name or path only when the binding permits an override. When an override is accepted, Workspace Runtime records the final rendered path, naming source, and override provenance. When a structured binding expects durable Markdown and no binding default or permitted override can resolve a content name, the command returns a deterministic diagnostic instead of inventing a filename.

Standalone render/preview commands are different from durable `create` or `update` materialization. For generic `project artifact-formats render` and standalone research-record render previews, if the caller does not provide an output file path, the command prints the rendered content to the console. If the caller provides an output file path, the command writes the rendered content there and reports the path in deterministic output.

### Add Structured Payload State Beside Lifecycle Records

Keep `lifecycle_records` as the durable node identity and add a structured payload layer keyed by lifecycle record id. The conceptual table is:

```text
research_record_payloads
  id
  record_id
  research_topic_id
  topic_workspace_id
  format_profile_ref
  schema_ref
  schema_version
  schema_source_kind
  template_ref
  template_source_kind
  payload_json
  payload_digest
  validation_status
  validation_diagnostics_json
  render_status
  render_diagnostics_json
  rendered_markdown_path
  rendered_markdown_digest
  created_at
  updated_at
  provenance_refs_json
```

The payload row should be written in the same transaction as the lifecycle record on create or update. `lifecycle_records` stays the source for record kind, status, lifecycle refs, content path, and generic transition metadata. The payload table stores the validated record-specific body data and render state.

Alternative considered: store the payload only inside `transition_metadata_json`. That avoids a new table, but it makes payload queries, validation status, digest checks, and future GUI listing depend on unbounded metadata JSON scans. A dedicated table keeps the generic lifecycle envelope small and makes structured records visible.

### Make Markdown a Generated View

For structured records, Markdown is a generated view from the validated payload. The generated file can still be stored in `content_path` so existing `show --include-body` behavior remains useful, but the payload row is the source of truth. Generated Markdown should carry enough marker metadata, such as format profile ref, schema ref, payload digest, and generated timestamp, to make stale generated views diagnosable.

Manual edits to generated Markdown should not silently update the structured payload. Validation can report digest mismatch or stale rendered view. A later repair command can re-render from the payload.

Alternative considered: keep Markdown and JSON as equal peers. That invites disagreement and forces every reader to decide which one wins. Treating Markdown as derived keeps the model clear.

### Make Direct Body Authoring Outside the Structured Path

Accepted v2 structured artifacts should not be created from direct Markdown or generic body files. The structured path is payload-first: format profile or schema/template refs plus JSON payload, validation, runtime payload state, and generated Markdown. If the generic record API keeps `--body` or `--body-file` for unrelated unstructured use, those records are outside this change's structured record contract and do not need migration, import classification, or GUI-ready typed fields.

Alternative considered: keep a first-class legacy body mode and label records as `legacy_body` or `mixed_import`. That would spend design and implementation effort preserving artifacts the project intends to discard. The cleaner choice is to define the accepted v2 path and leave non-structured body writes outside it.

### Query Structured Records Without Parsing Markdown

`records list` returns compact structured summaries by default: lifecycle identity and status fields plus format profile ref, schema ref, template ref, source kind, validation status, render status, payload digest, generated Markdown locator when available, placeholder, skill, producer, consumer, and core timestamps. It does not include full payload JSON, validation diagnostics, render diagnostics, or rendered Markdown content unless a caller requests those through `show` or explicit include flags.

List results are bounded by recency. The default limit is configurable in the Project Manifest TOML under the extension-scoped defaults table for the current `ext research` CLI namespace, using `defaults.ext.research.records_list_limit`. When the Project Manifest omits that setting, the built-in fallback is the most recent 20 records for the selected topic and filters, ordered by updated or created time. The limit is also caller-controllable, for example with `--limit <n>`, so CLI and GUI callers can page or widen the slice without changing the project default.

Example Project Manifest setting:

```toml
[defaults.ext.research]
records_list_limit = 50
```

Useful filters include format profile ref, schema ref, template ref, source kind, validation status, render status, placeholder, skill, record kind, status, and lifecycle refs. The CLI is not expected to become a full analytical query language over every payload field. For complex ad hoc analysis, advanced users may query the Workspace Runtime database directly, using the documented runtime tables and stable indexed columns from this change.

`records show` should be able to return payload JSON, generated Markdown path, validation diagnostics, render diagnostics, and rendered Markdown content separately.

Alternative considered: wait for the graph index to add query APIs. The graph index will answer relationship questions, but the GUI needs basic record listing and inspection first.

### Update V2 Placeholder Bindings and Skill Guidance

Active v2 placeholder binding pages should stop presenting direct body-file creation as the normal accepted-artifact path. The new command examples should ask the agent to write a JSON payload file for the format profile and then use `validate` and `create --payload-file ... --render markdown`. The active skill instructions should keep research-method prose but route durable output through those binding pages.

Alternative considered: keep placeholder bindings as body-file examples and rely on agents to infer schemas from profile names. That leaves the most important source of truth outside the system that will later query it.

## Risks / Trade-offs

- [Risk] Early schemas may be too rigid for exploratory research records. Mitigation: keep schemas profile-specific and allow explicit draft or blocked validation statuses where the contract permits them.
- [Risk] Plain path inputs can undermine reproducibility. Mitigation: allow them for ad hoc validate/render, but snapshot them into managed runtime assets before durable record creation.
- [Risk] Agents may still write Markdown directly out of habit. Mitigation: update binding examples, add validation harness rules for active v2 bindings, and make structured commands the copied path.
- [Risk] Generated Markdown can become stale if edited manually. Mitigation: store payload and Markdown digests and report stale generated views in validation.
- [Risk] Storing large payload JSON in SQLite can become heavy. Mitigation: keep payloads to structured record data, leave large tables/logs/files as file-backed Artifacts or later file attachments, and add size diagnostics when needed.
- [Risk] Format ref resolution can become ambiguous. Mitigation: record the resolved format profile ref, schema ref, template ref, source kind, digests, and resolution source with each structured payload.
- [Risk] This adds another persistence layer before graph indexing. Mitigation: keep lifecycle identity unchanged and make payload rows strictly dependent on lifecycle records.

## Implementation Plan

1. Add core artifact-format models, resolver, registry, JSON Schema validation, Jinja2 rendering, deterministic diagnostics, and unit tests.
2. Add DeepScientist extension record-format assets and a provider for `isomer:deepsci/record-format/*` refs.
3. Add topic-registered custom format storage and registration commands for `custom:<topic-or-extension-slug>/record-format/*` refs.
4. Add plain `--schema-file` and `--template-file` support for ad hoc validate/render, plus snapshot behavior for durable record creation.
5. Extend Workspace Runtime schema preparation with structured payload storage and any format-registration or snapshot storage needed by Topic Workspaces.
6. Add payload dataclasses, store methods, deterministic diagnostics, and validation/render calls behind the existing research records extension.
7. Add CLI options and commands for generic `project artifact-formats validate/register/render` and research-record `validate`, `create --payload-file`, `update --payload-file`, `show --include-payload`, `show --include-rendered-body`, and `render`.
8. Store generated Markdown under durable semantic record labels, with the lifecycle `content_path` pointing at the generated view when that keeps existing inspection behavior useful.
9. Update active v2 placeholder binding command shapes and validation harness rules so new accepted artifacts use payload-first writes with `--format-profile`.
10. Do not migrate or backfill current `isomer-content/` artifacts.

Rollback is straightforward for future structured records: code can ignore `research_record_payloads` and keep reading `lifecycle_records` plus generated Markdown content paths. Existing structured records would lose typed payload display under older code, but their lifecycle rows and generated Markdown bodies would still be available.
