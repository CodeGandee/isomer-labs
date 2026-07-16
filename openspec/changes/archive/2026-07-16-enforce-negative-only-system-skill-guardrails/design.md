## Context

The active packaged system-skill manifest declares 55 skill roots. Across their active entrypoints and behavioral pages, 148 pages contain 666 Guardrails bullets: 546 begin with `DO NOT` and 120 begin with `MUST`. The current Isomer specification and validator intentionally accept both prefixes, but the upstream Imsight creation and formatting contract now permits only concise `DO NOT ...` prohibitions and directs positive operations into substantive sections.

The migration crosses packaged Markdown, validator behavior, tests, and two current OpenSpec capabilities. Historical source copies under `org/`, migration material under `migrate/`, passive output templates, and archived OpenSpec changes remain outside the active template scope.

## Goals / Non-Goals

**Goals:**

- Make every active Guardrails section negative-only without weakening a skill's behavioral contract.
- Keep each retained Guardrails bullet concise and limited to one prohibited action.
- Put required commands, ordering, routing, evidence, and output behavior where agents execute or consume that guidance.
- Enforce the `DO NOT ...` prefix through the manifest-aware validator and unit tests.
- Preserve public skill names, subcommands, paths, domain language, approval boundaries, stop conditions, and output requirements.

**Non-Goals:**

- Redesigning skill workflows or changing ownership boundaries.
- Rewriting immutable provenance, passive templates, migration notes, or archived OpenSpec history.
- Adding a natural-language semantic parser for every possible positive clause.
- Renaming public commands or changing runtime behavior.

## Decisions

### Classify Before Rewriting

Each positive Guardrails bullet will receive one of three treatments:

1. Convert it to one or more `DO NOT ...` bullets only when a lossless negative formulation directly prevents the underlying risk, such as replacing identity-separation requirements with a prohibition against conflation.
2. Remove it when an existing Workflow, subcommand procedure, command boundary, domain reference, or Output Contract already states the same authoritative behavior.
3. Move it into an existing substantive section or a narrowly named contract section when it carries unique operational guidance.

This preserves meaning more reliably than mechanically negating every `MUST` sentence. Mechanical replacement was rejected because rules such as command recipes, stage order, required evidence, and routing maps become awkward or misleading when phrased as prohibitions.

### Use Existing Sections Before Adding New Ones

Command selection and ordering belong in `## Workflow` or the selected subcommand page. Required inputs belong in `## Required Inputs`; output fields belong in `## Output Contract`; domain invariants belong in an existing concepts or boundary section. A new section such as `## Operational Contract`, `## Routing Contract`, `## Topology Contract`, or `## Verification Evidence` is added only when no existing section provides a clear home.

This keeps Guardrails sparse and avoids duplicating the same instruction in several sections.

### Audit Existing DO NOT Bullets Semantically

The migration will inspect existing `DO NOT` bullets that append positive imperatives such as “use”, “route”, or “report”. When the positive clause is necessary to understand the prohibition, the page will move that clause to the relevant workflow or contract and retain a concise prohibition. When the clause merely identifies the safe alternative, it may remain only if the resulting bullet still states one prohibited action rather than acting as an operation step.

### Keep Validation Deterministic

The validator will require every top-level Guardrails bullet to match `^- DO NOT(?:\s|$)` and will reject `MUST`, loose imperatives, and other prefixes with a file-specific diagnostic. It will continue enforcing one Guardrails section for entrypoints, concise top-level bullets, active manifest scope, and excluded historical zones.

The validator will not attempt broad natural-language classification of every secondary clause. Unit tests and the migration audit provide coverage for known positive forms, while review remains responsible for semantic concision.

### Preserve Historical Records

Current specs receive delta requirements, but archived changes retain the former `DO NOT`/`MUST` wording as historical evidence. Rewriting archive contents was rejected because it would falsify what earlier changes specified and implemented.

## Risks / Trade-offs

- [A positive rule is removed as a duplicate but its authoritative copy is incomplete] → Compare the full behavioral meaning before removal and place missing detail in the owning substantive section.
- [A negative rewrite changes meaning] → Prefer relocation over negation whenever the original sentence describes a required operation rather than a prohibited risk.
- [Long existing `DO NOT` bullets still contain workflow content] → Audit mixed-clause candidates across the entire active manifest scope, not only the 120 `MUST` bullets.
- [Validator enforcement is syntactic rather than semantic] → Keep the syntax deterministic and use explicit migration review plus focused tests for content placement.
- [Concurrent uncommitted edits overlap validator, tests, or skill pages] → Apply narrow patches, preserve unrelated content, and review diffs before validation.

## Migration Plan

1. Update the two current capability contracts through delta specs.
2. Change validator fixtures and prefix enforcement from `DO NOT|MUST` to `DO NOT`.
3. Migrate affected entrypoints, command pages, and reference pages by skill family using the classification rules above.
4. Audit mixed `DO NOT` bullets and relocate positive operational clauses where needed.
5. Run the packaged-skill validator, focused unit tests, repository lint, type checking, unit tests, and strict OpenSpec validation.

Rollback consists of reverting the change-scoped edits. No data or runtime migration is involved.

## Open Questions

None. The upstream template and active manifest scope provide a complete implementation boundary.
