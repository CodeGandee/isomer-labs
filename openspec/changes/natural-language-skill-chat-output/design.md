## Context

The active packaged catalog contains 52 skills, with another 12 repository-local development and Toolbox skills. Chat-facing guidance currently uses several overlapping forms: split Essential and Complete Output sections, literal `snake_case: value` bullet contracts, inline lists of field names, status tokens, and structured terminal-report schemas. The current validator requires the Essential and Complete split for many non-research skills but does not distinguish semantic content requirements from literal chat serialization.

Structured output remains necessary for durable research records, CLI and API responses, manifests, receipts, configuration, and explicit JSON handoffs. The presentation rule therefore cannot ban field names globally; it must distinguish the chat response from structured artifacts produced or inspected during the workflow.

## Goals / Non-Goals

**Goals:**

- Make natural-language Markdown the default presentation for every active Isomer skill's chat response.
- Preserve Essential and Complete as information-depth choices independent of presentation format.
- Keep exact machine schemas intact where another system consumes them or the user explicitly requests them.
- Remove or neutralize chat-facing instructions that cause flat pseudo-record output.
- Add validation that detects future regressions without flagging legitimate schemas and field documentation.

**Non-Goals:**

- Changing CLI, API, manifest, receipt, runtime record, or research artifact schemas.
- Removing stable internal status values or domain field names from durable records.
- Reformatting inactive `org/`, migration, analysis, or provenance copies.
- Requiring every short answer to contain the same fixed Markdown headings.

## Decisions

### Put the presentation rule in every active skill entrypoint

Each active `SKILL.md` will state that named output items describe required information rather than literal response keys. Normal chat will use natural prose, descriptive Markdown headings when multiple concerns need separation, and genuine lists. The instruction will forbid pseudo-JSON, pseudo-YAML, and `snake_case: value` presentation unless the user explicitly requests machine-readable output.

A central documentation page alone was rejected because installed skills are independently projected and an agent is not guaranteed to load a repository README or a separate policy skill. Provider-specific metadata was rejected because the rule must work across agent hosts.

### Separate information depth from presentation format

Essential Output and Complete Output remain content-depth contracts. Natural Markdown is the default presentation for both. Explicit JSON or another machine-readable request changes presentation and uses the requested serialization; it does not define the ordinary Complete Output style.

The existing wording that lists JSON beside verbose, audit, and full-output triggers will be revised so the two dimensions are unambiguous.

### Rewrite chat contracts while preserving semantic coverage

Main and directly loaded reference guidance that says `field_name: details` or “Report `field_name`” will be rewritten as natural descriptions of facts to include. The underlying concepts, allowed status values, safety evidence, blockers, and next actions remain unchanged.

Structured tables and examples will remain when they define durable artifacts, CLI or API payloads, configuration, or schemas. Those documents will explicitly state that the schema applies to the artifact and that the final chat response summarizes it naturally.

### Validate active guidance by context

The skillset validator will require the shared chat-presentation language in active skill entrypoints and inspect chat-facing Output Contract sections for machine-shaped bullet labels. It will not reject field names inside fenced code, durable-schema sections, CLI or API contracts, configuration examples, or inactive provenance material.

Tests will cover a compliant natural-language contract, a missing policy, a machine-shaped Essential Output contract, and a legitimate structured-artifact exception.

## Risks / Trade-offs

- [Repeated policy text can drift across skills] → Require a stable phrase through validation and keep the policy short.
- [A broad field-pattern check can reject legitimate schemas] → Limit the check to chat-facing output sections and provide explicit structured-artifact exemptions.
- [Rewording can accidentally drop required handoff facts] → Preserve each contract's semantic inventory while replacing literal key labels.
- [Nested skills can still over-report child details] → State that the final chat answer composes outcomes into natural sections rather than concatenating parent and child field contracts.
- [Research terminal reports may be mistaken for chat templates] → Mark them as durable artifact schemas and require a separate natural-language terminal summary.

## Migration Plan

1. Add the shared presentation instruction to every active packaged and repository-local skill entrypoint.
2. Rewrite the main chat-facing output contracts and directly loaded reference instructions found by the audit.
3. Mark durable terminal-report and structured payload templates as artifact schemas rather than chat templates.
4. Extend validator constants, checks, and focused unit tests.
5. Run skillset validation, lint, type checking, and unit tests.

Rollback consists of reverting the guidance and validator changes; no stored state or external schema migration is required.

## Open Questions

None. The user explicitly selected natural-language Markdown as the default and machine-shaped output only for explicit structured-output needs.
