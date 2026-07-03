## Why

V2 research skills currently ask agents to write Markdown or other body files directly, then attach those files to generic Workspace Runtime records. That leaves future GUI and query surfaces without an authoritative structured payload: they must either parse prose or accept that important fields, validation state, and renderable views are scattered across `.md`, `.json`, logs, and transition metadata.

The useful primitive is broader than research records: Isomer needs a reusable way to validate JSON against a schema and render Jinja2 templates from that JSON. Research records should consume that core artifact-format processing engine, while DeepScientist supplies one extension-owned set of format profiles, schemas, and templates.

## What Changes

- Make structured research record payloads the primary write path for v2-produced durable research records.
- Add a top-level artifact-format processing capability for JSON Schema validation, Jinja2 rendering, format-profile resolution, topic-registered formats, and plain schema/template path inputs.
- Add schema-backed validation before a research record can be stored as an accepted structured record.
- Store the validated payload, selected Artifact Format Profile, schema ref, template ref, validation outcome, render outcome, and rendered Markdown locator in Workspace Runtime.
- Add CLI behavior for validate, create, update, show, list, and render operations that works from a JSON payload and produces deterministic diagnostics when validation fails.
- Render Markdown artifacts from validated JSON payloads and DeepScientist extension-owned Jinja2 templates, treating Markdown as a generated view rather than the source of truth.
- Ship the first DeepScientist provider bundle for the full active v2 accepted-output set, including run, evidence, decision, handoff/control, figure, report, paper, Nature-specific, presentation, and finalization record families.
- Support user-registered custom format refs in Topic Workspaces using the `{isomer,custom}:<topic-or-extension-slug>/<primary-group>/<subgroup>/.../<template-name>` naming pattern.
- Support plain `--schema-file` and `--template-file` inputs for ad hoc validate/render use, and snapshot plain-path schemas/templates when they are used to create durable records.
- Make direct `--body` and `--body-file` authoring outside the accepted v2 structured-artifact path; v2 structured placeholder guidance must use payload-first command shapes for accepted generated artifacts.
- Prepare the ground for the later graph-index change by giving every future record a stable structured payload that graph edges and GUI views can reference.

## Capabilities

### New Capabilities

- `artifact-format-processing`: Core Isomer engine for resolving format profiles, validating JSON payloads with JSON Schema, rendering Jinja2 templates from JSON, registering custom topic formats, accepting plain schema/template path inputs, and returning deterministic diagnostics.

### Modified Capabilities

- `research-recording-contracts`: Make payload-first research record CRUD consume the generic artifact-format processing engine while keeping Artifact Format Profiles declarative.
- `workspace-runtime-persistence`: Persist validated structured payload records, validation outcomes, profile refs, schema refs, template refs, source ref kinds, plain-path snapshots when needed, and generated Markdown locators in Workspace Runtime.
- `research-placeholder-bindings`: Require active v2 placeholder binding guidance to create accepted research artifacts from JSON payloads through schema validation and rendering instead of direct Markdown body writes.
- `research-paradigm-skills`: Require v2 skills to treat accepted durable artifact output as structured JSON payloads that are validated and recorded before Markdown is generated.

## Impact

- Adds top-level artifact format modules, likely under `src/isomer_labs/artifact_formats/`, for profile resolution, JSON Schema validation, Jinja2 rendering, registration, and diagnostics.
- Affects `src/isomer_labs/research_records.py`, Workspace Runtime schema/model/store APIs, CLI argument parsing, deterministic JSON output, and validation behavior.
- Uses existing `jsonschema` and `jinja2` dependencies to validate payloads and render Markdown from package-owned DeepScientist extension templates.
- Adds DeepScientist extension format assets under `src/isomer_labs/deepsci_ext/assets/record_formats/` and a provider/resolver that registers `isomer:deepsci/...` refs with the core engine for the full active v2 accepted-output set.
- Affects v2 research skill `placeholder-bindings.md` command shapes and any validation harness rules that inspect those bindings.
- No migration, backfill, import, or compatibility rescue is required for current `isomer-content/` topic artifacts; those generated topic artifacts are outside the implementation scope and may be discarded.
