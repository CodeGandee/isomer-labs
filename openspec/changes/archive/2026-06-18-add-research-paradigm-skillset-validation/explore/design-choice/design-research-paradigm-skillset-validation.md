# Research Paradigm Skillset Validation Design Choices

## Context

This exploration clarifies option points for Stage 6 of `context/plans/research-paradigm-skill-gaps.md` and the OpenSpec change `add-research-paradigm-skillset-validation`. The validator protects the accepted Isomer research-paradigm language from regression while preserving intentional migration, provenance, and resolved-surface explanation text.

Evidence inspected:

- `openspec/changes/add-research-paradigm-skillset-validation/proposal.md`
- `openspec/changes/add-research-paradigm-skillset-validation/design.md`
- `openspec/changes/add-research-paradigm-skillset-validation/specs/research-paradigm-skills/spec.md`
- `openspec/changes/add-research-paradigm-skillset-validation/tasks.md`
- `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`
- `skillset/research-paradigm/README.md`
- `skillset/research-paradigm/isomer-rsch-shared/references/source-term-mapping.md`
- `skillset/research-paradigm/isomer-rsch-shared/references/tbd-surface-registry.md`
- representative local `references/isomer-research-contract.md` files

## Accepted Choices

### 1. Strictness

Use strict active-text validation with narrow, rule-specific allow zones.

Accepted option: A.

Rationale: Active skill guidance must use current Isomer terms such as Research Topic, Research Inquiry, Research Inquiry Relationship, and Topic Workspace. Legacy terms such as Research Goal, Research Thread, Research Branch, and Isomer Workspace remain valid only where they explain source mappings, provenance, rejected runtime concepts, deferred resources, or resolved surfaces.

### 2. Rule Policy Location

Keep core forbidden and resolved terms built into the validator, and put narrow allow zones in checked-in `skillset/research-paradigm/validation.toml`.

Accepted option: B.

Rationale: Core domain safety should not depend on easily weakened local config. Allow zones still need to be reviewable and adjustable as the skillset adds golden examples and optional assets.

### 3. Active Validation Surface

Validate every Markdown and YAML file under `skillset/research-paradigm`, then classify files and sections by role.

Accepted option: B.

Rationale: The skillset has active entrypoints, local references, shared docs, root guidance, provenance, licenses, and deferred-resource notes. Validating only `SKILL.md` files or directly linked references would leave unvalidated pockets where stale guidance could accumulate.

### 4. TBD Surface Registry Lookup

Use two-tier registry lookup: the shared registry is canonical for the full subtree, and each directly loaded local contract registry must be consistent with it.

Accepted option: C.

Rationale: The shared registry preserves one source of truth. Local contract files preserve self-contained skill behavior because most stage skills load `references/isomer-research-contract.md`, `references/writing-contract.md`, `references/outline-contract.md`, or `references/audit-gate.md` directly.

### 5. Local Registry Mirror Consistency

Require exact resolved-ID coverage and normalized resolution text for local registry mirrors that appear in directly loaded contract files.

Accepted option: A.

Rationale: Local contract files should not merely mention the same former IDs; they should preserve the same accepted resolution semantics. Normalization can ignore harmless Markdown spacing differences, but not changed IDs or changed meaning.

## Resulting Validator Shape

The validator should classify the bundle roughly as:

```text
skillset/research-paradigm
  active docs: SKILL.md, README.md, operational references
  contract mirrors: directly loaded local contract files with TBD Surface Registry sections
  canonical registry: isomer-rsch-shared/references/tbd-surface-registry.md
  explanatory zones: provenance, licenses, source-term mappings, rejected runtime sections, deferred-resource notes, resolved-surface tables
```

Strict checks apply everywhere unless a rule-specific allow zone applies. Allow zones are not global exemptions.

## Implementation Notes

- Parse all Markdown and YAML files under the research-paradigm subtree.
- Keep core term sets and resolved placeholder sets in Python defaults.
- Use `validation.toml` only for allow-zone file globs, section headings, and narrowly scoped pattern allowances.
- Parse the shared TBD registry tables as canonical data.
- Parse local registry mirror tables only in directly loaded contract files.
- Normalize table cell text for whitespace and Markdown formatting before comparing mirror resolution text.
- Fail local mirror drift when a resolved ID is missing, extra, or semantically different from the shared registry.
- Add fixture tests for allowed mapping/provenance text, rejected active guidance, local mirror drift, and whole-tree scan behavior.

## Open Questions

No blocking design questions remain for this change. Exact diagnostic code names, function names, and config key names can be chosen during apply as long as they preserve these accepted choices.
