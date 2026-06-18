## 1. Main Spec and Design Alignment

- [ ] 1.1 Review the accepted `workspace-path-resolution` and `research-paradigm-skills` specs to confirm the recording contract uses Topic Workspace and Artifact path terminology consistently.
- [ ] 1.2 Update or create the main `research-recording-contracts` spec from the delta spec during archive or sync.
- [ ] 1.3 Update the main `research-paradigm-skills` spec so resolved recording surfaces are no longer described as open TBDs.

## 2. Shared Skill Contract Updates

- [ ] 2.1 Update `isomer-rsch-shared/references/tbd-surface-registry.md` to map or remove resolved recording TBD ids: `api-artifact-record`, `api-finding-query`, `api-gate`, `schema-decision-record`, `schema-evidence-item`, `schema-research-claim`, and `schema-gate`.
- [ ] 2.2 Update `isomer-rsch-shared/SKILL.md` to name accepted recording APIs and durable record types where it currently refers to unresolved recording surfaces.
- [ ] 2.3 Keep unresolved TBD entries for command execution, literature provider, scheduler policy, Stage Cursor, Agent Team State, Skill Binding, branching policy, baseline-waiver policy, and cost/privacy Gate policy.

## 3. Local Research Contract Copies

- [ ] 3.1 Update every `skillset/research-paradigm/isomer-rsch-*/references/isomer-research-contract.md` copy to consume Research Recording Contracts.
- [ ] 3.2 Remove resolved recording TBD placeholders from local research contract copies without changing unrelated execution, provider, scheduler, or policy TBD placeholders.
- [ ] 3.3 Confirm local contract copies keep the same workspace path guidance from Workspace Path Resolution.

## 4. Route-Specific Skill Reference Updates

- [ ] 4.1 Update stage skills that record Artifacts, Evidence Items, Research Claims, Decision Records, Findings, Provenance Records, or Gates to use accepted record names and APIs.
- [ ] 4.2 Update writing, review, rebuttal, paper-outline, paper-plot, figure-polish, and science references that mention resolved recording schemas or APIs.
- [ ] 4.3 Preserve skill language that distinguishes Evidence Items from raw Artifacts and Decisions from Gates.
- [ ] 4.4 Ensure skills still mark command execution, literature search, scheduler, Skill Binding, and policy surfaces as TBD where no accepted contract exists.

## 5. Validation and Consistency Checks

- [ ] 5.1 Run an OpenSpec validation for `define-research-recording-contracts`.
- [ ] 5.2 Search `skillset/research-paradigm` for the resolved recording TBD ids and confirm remaining matches are removed, mapped to the accepted contract, or confined to archive/provenance notes.
- [ ] 5.3 Search for stale ordinary path TBDs to confirm Workspace Path Resolution guidance was not regressed.
- [ ] 5.4 Search for hard-coded local paths, DeepScientist runtime APIs, and source-only command wrappers in active skill text.
- [ ] 5.5 Review the diff for accidental definitions of command execution, literature provider, scheduler, Skill Binding, Agent Team State, or full lifecycle transitions.

## 6. Final Review

- [ ] 6.1 Verify the research-paradigm skillset still has no active dependency on source-analysis paths or archived OpenSpec files.
- [ ] 6.2 Verify no skill claims a Research Claim is supported without requiring Evidence Item support.
- [ ] 6.3 Verify Gate language blocks only governed actions and does not turn every Decision Record into a human Gate.
- [ ] 6.4 Summarize remaining TBD surfaces for the next planned changes.
