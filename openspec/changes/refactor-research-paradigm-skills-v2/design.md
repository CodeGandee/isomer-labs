## Context

The current research-paradigm skills are useful but too implementation-facing. They translate DeepScientist workflow concepts into Isomer storage and runtime nouns inside active skill instructions, which makes the skills harder to read and prematurely commits the research method to storage semantics.

The revised direction is to keep the core research process first. V2 skills should name the semantic research objects they produce or consume, then leave storage binding for a later change. This lets Isomer Labs refine what a "frame", "comparator", "hypothesis", "result", "analysis", or "decision" means before mapping those concepts to Artifacts, Evidence Items, Runs, Gates, paths, or database rows.

## Goals / Non-Goals

**Goals:**

- Preserve the core research loop: frame, comparator, hypothesis, experiment, analysis, decision, finalize, plus optimize and science overlays.
- Move existing DeepScientist-derived skills to a v1 generation namespace with `-v1` skill names.
- Create v2 core skills under `skillset/research-paradigm/v2/` using `isomer-rsch-<purpose>-v2` names.
- Replace storage-facing objects in v2 skill instructions with semantic placeholders whose meanings are defined in a shared v2 registry.
- Keep v2 skill entrypoints concise enough for regular agent use.
- Keep provenance and source-lineage context visible without requiring `extern/orphan`, `context/explore`, or prior plan files at runtime.

**Non-Goals:**

- Do not implement storage bindings for v2 placeholders.
- Do not add new storage labels, CLI record commands, database schemas, or runtime APIs.
- Do not port paper-specific v1 skills into v2 during the first pass.
- Do not delete v1 content or DeepScientist provenance.
- Do not require v2 skills to be standalone outside the research-paradigm subtree in this change.

## Decisions

### Decision: Use Explicit Skill Generations

Use `skillset/research-paradigm/v1/` for preserved current skills and `skillset/research-paradigm/v2/` for the new concise core skills. Rename v1 folders and frontmatter to `isomer-rsch-<purpose>-v1`; name v2 folders and frontmatter `isomer-rsch-<purpose>-v2`.

Alternative considered: keep old names active and add v2 only in documentation. That would make invocation ambiguous and would leave callers unsure whether `$isomer-rsch-experiment` means the storage-heavy or concise methodology version.

### Decision: Define a Semantic Placeholder Registry Before Storage Binding

V2 skills SHALL use placeholders of the form `[[rsch-object:<id>]]` for research objects whose semantics matter but whose storage binding is intentionally deferred. The shared v2 skill should own a registry, for example `v2/isomer-rsch-shared-v2/references/semantic-placeholders.md`, that defines each placeholder's meaning, minimum content, producer skills, consumer skills, and explicit "not storage-bound yet" status.

Alternative considered: use existing Isomer storage nouns such as Artifact, Evidence Item, Run, Gate, Decision Record, and Provenance Record in v2. That would keep continuity with current specs, but it would obscure the semantics-first rewrite the user requested and would keep implementation bookkeeping inside methodology skills.

### Decision: Keep the Initial V2 Skill Set Small

Create only the core v2 research skills: `shared`, `scout`, `baseline`, `idea`, `optimize`, `experiment`, `analysis`, `decision`, `finalize`, and `science`. These map to the process analyzed in `context/explore/deepscientist-skill-analysis/` without importing paper-production skills into the first generation.

Alternative considered: port all v1 skills to v2 immediately. That would preserve breadth, but it would slow semantic cleanup and risk recreating the v1 bookkeeping problem.

### Decision: Use a Common V2 Skill Template

Each v2 `SKILL.md` should use a compact structure: purpose, when to use, workflow, semantic inputs, semantic outputs, guardrails, and optional source lineage. Long route taxonomies should be condensed into the workflow unless they are essential to research judgment.

Alternative considered: preserve the current v1 entrypoint style with long workflow, output, recording, and validation sections. That would minimize rewrite effort, but it would not produce the concise v2 layer.

### Decision: Treat Storage Terms as Forbidden in Active V2 Guidance

Active v2 skill guidance should not require or direct creation of Artifacts, Evidence Items, Runs, Gates, Decision Records, Provenance Records, concrete paths, runtime state, or database rows. Those terms may appear only in provenance, migration notes, or rejected-storage-binding notes.

Alternative considered: allow storage terms as examples. That would make the future binding easier to imagine, but examples tend to become de facto requirements in agent skills.

## Risks / Trade-offs

- Placeholder semantics may be too abstract for agents to use consistently -> Mitigation: the shared registry must define minimum content and producer/consumer relationships for every placeholder.
- Existing callers may break because skill names become generation-suffixed -> Mitigation: update README, manifests, validation, and any role maps in the same implementation pass.
- V1 renaming may be noisy and easy to do incorrectly -> Mitigation: script or carefully validate folder names, frontmatter names, manifest display names, and default prompts.
- Removing storage nouns from v2 may hide important audit obligations -> Mitigation: v2 guardrails should still require enough semantic content to resume and judge research work, without saying where it is stored.
- Paper-facing skills will lag behind the core v2 loop -> Mitigation: preserve them under v1 and document that v2 paper skills are a later semantic pass.

## Migration Plan

1. Move current flat `isomer-rsch-*` folders into `skillset/research-paradigm/v1/` and append `-v1` to folder names, frontmatter names, manifest display names, and default prompts.
2. Create `skillset/research-paradigm/v2/` with the ten core v2 skill folders and `-v2` frontmatter names.
3. Add the v2 semantic-placeholder registry under `isomer-rsch-shared-v2/references/`.
4. Write each v2 skill against the core research process, using only registered `[[rsch-object:<id>]]` placeholders for research objects.
5. Update README, PROVENANCE, and validation configuration for generationed layout and placeholder validation.
6. Run repository validation and inspect for unsuffixed active skill names, storage-bound nouns in v2 active guidance, broken references, and missing placeholder registrations.

Rollback is straightforward because v1 preserves the current skills: callers can continue using the archived v1 names while v2 semantics settle.

## Open Questions

- Should the unsuffixed names such as `isomer-rsch-experiment` be reintroduced later as aliases to the current stable generation, or should all research-paradigm skills remain explicitly generationed?
- Which v2 placeholders are semantically distinct enough to survive later storage binding, and which should collapse into broader objects?
- Should write/review/rebuttal/paper-plot/figure-polish receive v2 versions after the core loop stabilizes, or should they become a separate paper-production skill family?
