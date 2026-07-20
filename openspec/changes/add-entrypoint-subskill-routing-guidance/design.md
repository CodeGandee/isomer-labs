## Context

The protected-pack layout leaves only three public Isomer skills in ordinary host discovery: the core operator entrypoint and the DeepSci and Kaoju extension entrypoints. Those entrypoints must select among 54 protected members before loading a member's detailed instructions. The core table currently provides short category phrases, while the DeepSci and Kaoju tables provide only member identities and internal designators. Each protected member already has richer trigger evidence in its `SKILL.md` frontmatter, `## When to Use` section, workflow handoffs, and `agents/openai.yaml`, but copying that text wholesale would repeat pack context and produce noisy routing tables. The shared Imsight style guide currently requires parents to list bundled subskills, but it does not require enough trigger information for the parent to select among them.

## Goals / Non-Goals

**Goals:**

- Give every protected member one concise sentence that tells its public entrypoint when to select that route.
- Preserve enough distinction between adjacent members for task-only routing without loading every protected `SKILL.md`.
- Derive the sentences from authoritative member instructions while adapting them to context already established by the parent entrypoint.
- Make missing, malformed, or mechanically copied routing guidance detectable by repository validation.
- Encode the same rule in `imsight-agent-skill-handling` so newly created, designed, migrated, or formatted skills do not reproduce the routing gap.

**Non-Goals:**

- Change public subcommands, invocation notation, internal designators, logical ids, callback lookup, or protected resource ownership.
- Expose protected members as independent host-discoverable skills.
- Replace the full trigger, guardrail, handoff, or workflow guidance inside protected subskills.
- Add routing summaries to the packaged manifest or generate entrypoint prose at installation time.
- Make the Isomer validator responsible for validating files inside the separate `houmao-agents` repository.

## Decisions

### Use One Parent-Oriented Routing Column

Each `## Protected Subskills` table will contain a `When to Route Here` column. The operator table will replace its terse `Use For` column, while the DeepSci and Kaoju tables will add the new column without removing identity or designator columns. Each cell will contain one sentence framed as a parent selection condition rather than a direct user invocation instruction.

This keeps the decision at the point where it is needed. A separate reference page would require another load before route selection, and a second boundary column would make already-wide tables harder to scan.

### Synthesize Rather Than Copy Member Metadata

Authors will inspect the protected member's frontmatter `description`, `agents/openai.yaml` `short_description`, `## When to Use`, and explicit route or handoff boundaries. The entrypoint sentence will retain the decisive trigger and, when routes overlap, name the distinction that changes ownership. It will omit phrases already implied by the parent, such as repeatedly identifying every row as an Isomer, DeepSci, or Kaoju request.

The sentence must not equal the protected member's frontmatter description or short description after superficial normalization. This deterministic check prevents direct copying, while review and focused tests cover contextual quality that a validator cannot fully assess.

### Keep Detailed Contracts in the Protected Member

The parent sentence is a routing introduction, not a substitute contract. Gates, callbacks, inputs, output records, execution steps, and complete negative boundaries remain in the protected subskill. After selecting a row, the entrypoint continues to load that member and follow its full instructions.

### Validate Coverage and Sentence Shape

The manifest remains the source of membership and identity. Packaged-skill validation will find each public entrypoint with protected members, parse its `## Protected Subskills` table, require the `When to Route Here` column, and verify one populated row per declared member. Each routing cell must be a single logical Markdown sentence, must meet a small deterministic substance threshold, and must not duplicate the member's frontmatter description or agent short description.

Unit fixtures will cover missing columns, missing or duplicate members, empty or phrase-only cells, multiple sentences, verbatim metadata copies, and valid context-aware sentences. Pack-specific assertions will protect important distinctions such as Project versus Topic lifecycle, DeepSci scouting versus baseline or idea work, and Kaoju trial versus reproduction.

### Make the Imsight Convention Apply at Authoring Time

The bundled Imsight style guide will define `When to Route Here` as required information for each row in a parent's subskill inventory. The sentence will be synthesized from the child subskill's trigger metadata and `## When to Use` guidance, rewritten to account for context already established by the parent, and kept distinct from the child's full contract. This rule applies recursively whenever a subskill owns further subskills.

The `create` workflow will author and validate the sentence when creating a skill with subskills. The `format` workflow will detect and repair missing, phrase-only, redundant, or copied descriptions in existing parent tables. The layout guidance will explain why the parent needs the information, while the design workflow and output template will capture the routing sentence before file creation. These coordinated edits prevent the canonical guide, creator, formatter, and design output from disagreeing.

The Houmao checkout remains a separate repository. Isomer implementation work may edit the ignored `extern/orphan/houmao-agents` symlink target as explicitly requested, but it will inspect, validate, and report those edits independently from the Isomer worktree.

## Risks / Trade-offs

- [Routing prose can drift from protected instructions] → Keep sentences short, retain protected instructions as authoritative, validate table membership from the manifest, and review the protected source when changing either trigger boundary.
- [Sentence-shape validation can reject legitimate punctuation] → Use a deliberately narrow Markdown convention and avoid abbreviations in routing cells; test inline code and command names explicitly.
- [A concise sentence can hide nuanced boundaries] → Put only the decisive selection boundary in the table and require the entrypoint to load the selected protected member before execution.
- [Parallel active changes touch the same capability specs] → Treat this change as dependent on `regroup-system-skills` and apply or archive changes in that order.
- [The Imsight convention and Isomer tables can drift] → Use the same parent-oriented wording rule in both repositories and verify both diffs during implementation without making either repository consume the other's files at runtime.

## Migration Plan

1. Add context-aware sentences to the core operator table and verify all 20 protected members.
2. Add context-aware sentences to the DeepSci table and verify all 21 protected members.
3. Add context-aware sentences to the Kaoju table and verify all 13 protected members.
4. Update the canonical Imsight style, creation, formatting, layout, and design guidance in the separate `houmao-agents` checkout and validate that skill independently.
5. Add Isomer validator logic and unit fixtures, then run packaged-skill validation and the repository test suite.

Rollback consists of reverting the table and validator edits together; no persisted data, manifest identity, or runtime migration is involved.

## Open Questions

None.
