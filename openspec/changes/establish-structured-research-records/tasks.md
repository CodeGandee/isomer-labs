## 1. Core Artifact Format Engine

- [x] 1.1 Add `src/isomer_labs/artifact_formats/` modules for models, resolver, registry, JSON Schema validation, Jinja2 rendering, deterministic diagnostics, and public Python APIs.
- [x] 1.2 Implement canonical format ref parsing and validation for `{isomer,custom}:<topic-or-extension-slug>/<primary-group>/<subgroup>/.../<template-name>`.
- [x] 1.3 Implement provider registration and resolution for format profiles, schema refs, and template refs independent of DeepScientist or research records.
- [x] 1.4 Implement JSON Schema validation using `jsonschema`, including deterministic diagnostics for schema load errors and payload validation errors.
- [x] 1.5 Implement Jinja2 rendering using resolved templates, including deterministic diagnostics for template load and render failures.
- [x] 1.6 Add generic artifact-format Python API tests for ref parsing, provider resolution, successful validation, failed validation, successful render, and render failure.

## 2. Format Providers and Custom Formats

- [x] 2.1 Add DeepScientist extension record-format assets under `src/isomer_labs/deepsci_ext/assets/record_formats/` with `profiles/`, `schemas/`, and `templates/markdown/*.md.j2` for the full active v2 accepted-output set, including run, evidence, decision, handoff/control, figure, report, paper, Nature-specific, presentation, and finalization record families.
- [x] 2.2 Add a DeepScientist record-format provider module for `isomer:deepsci/record-format/*` refs and register it with the core artifact-format engine.
- [x] 2.3 Add Workspace Runtime persistence for custom Topic Workspace artifact-format registrations, managed schema/template snapshots, digests, source paths, diagnostics, and provenance refs.
- [x] 2.4 Add `isomer-cli project artifact-formats register` for selected-Topic-Workspace-scoped custom `custom:` refs from schema files, template files, profile metadata, and output format.
- [x] 2.5 Add plain `--schema-file` and `--template-file` support for ad hoc validate/render without registration.
- [x] 2.6 Add snapshot behavior that turns plain schema/template paths into managed `custom:` snapshot refs before durable record creation depends on them.

## 3. Generic CLI Surface

- [x] 3.1 Add `isomer-cli project artifact-formats validate` with `--format-profile`, `--schema-ref`, or `--schema-file` plus `--payload-file`.
- [x] 3.2 Add `isomer-cli project artifact-formats render` with `--format-profile`, direct schema/template refs, or schema/template files plus `--payload-file`, `--format markdown`, optional output file path, stdout rendering when no output path is supplied, and deterministic render diagnostics.
- [x] 3.3 Ensure generic artifact-format commands emit deterministic JSON output under the existing `isomer-cli-output.v1` wrapper when `--print-json` is used.
- [x] 3.4 Add command tests for built-in DeepScientist refs, custom registered refs, plain path validation, plain path rendering, and missing-ref diagnostics.

## 4. Structured Research Record Persistence

- [x] 4.1 Add structured research payload runtime models for payload JSON, format profile ref, schema ref, template ref, source kinds, validation state, render state, digests, timestamps, and provenance refs.
- [x] 4.2 Extend Workspace Runtime schema setup to create structured payload storage idempotently for future structured records.
- [x] 4.3 Add runtime store methods to create, update, fetch, list, and validate structured payload rows linked to lifecycle record ids.
- [x] 4.4 Ensure structured payload writes are topic scoped and reject payload rows whose lifecycle record, Research Topic id, or Topic Workspace id does not match the selected Effective Topic Context.
- [x] 4.5 Extend Workspace Runtime validation to report invalid stored payloads, missing generated Markdown files, stale generated views, broken payload-to-lifecycle links, missing custom snapshots, and cross-topic payload leakage without deleting records.

## 5. Research Records CLI and API

- [x] 5.1 Extend research record request objects and APIs to accept payload file, `--format-profile`, direct schema/template refs, plain schema/template files, render mode, source kind metadata, generated content name source, optional binding-permitted output overrides, and structured output options.
- [x] 5.2 Add `isomer-cli ext research records validate` for artifact-format-engine-backed payload validation without Workspace Runtime mutation or Markdown file writes.
- [x] 5.3 Extend `records create` so valid payload-first requests create the lifecycle record, structured payload row, snapshots when needed, and explicitly requested generated Markdown view using placeholder-binding naming as one accepted structured record.
- [x] 5.4 Extend `records update` so valid replacement payloads preserve lifecycle identity, update structured payload state, snapshot plain paths when needed, re-render Markdown when requested, and preserve provenance history.
- [x] 5.5 Extend `records show` and `records list` JSON output with bounded compact structured payload summaries, Project Manifest `defaults.ext.research.records_list_limit` support with built-in fallback 20, caller-controlled list limits, optional payload JSON, format refs, source kinds, validation diagnostics, render diagnostics, generated Markdown locator, and render status.
- [x] 5.6 Reject `--body` and `--body-file` as accepted structured-artifact sources when structured format inputs require a payload file.

## 6. V2 Skill and Binding Updates

- [x] 6.1 Update active v2 `placeholder-bindings.md` command guidance for structured formats to use payload-first validate/create/update flows, `--format-profile`, binding-owned generated Markdown naming, and explicit naming override policy.
- [x] 6.2 Replace direct `--body` or `--body-file` accepted-artifact command shapes in active v2 bindings with payload-first commands for structured formats.
- [x] 6.3 Update active v2 skill guidance so accepted durable outputs route through skill-local payload-first placeholder bindings while methodology prose stays storage-light.
- [x] 6.4 Extend `scripts/validate_skillsets.py` and related tests to allow payload-first research record commands in binding pages, require `--format-profile` for format profile refs, and report direct Markdown body authoring as the normal source for structured formats.
- [x] 6.5 Run `pixi run lint`, `pixi run typecheck`, `pixi run test`, and the repository skillset validation command after implementation.
