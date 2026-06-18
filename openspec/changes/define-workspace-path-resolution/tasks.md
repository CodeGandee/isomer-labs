## 1. Workspace Path Contract Documentation

- [x] 1.1 Update `.imsight-arts/project-explore/designs/2026-06-15-manifested-workspace-engine-design.md` with the Workspace Path Resolver contract, including precedence order, default layout, supported `ISOMER_*` variables, canonicalization, Project-boundary validation, and durable recording.
- [x] 1.2 Update the relevant `.imsight-arts/project-explore` ADR or add a focused ADR if the workspace path contract needs an accepted decision record separate from the design note.
- [x] 1.3 Confirm the design uses existing Isomer terms: Project Config Directory, Project Manifest, Topic Workspace, Workspace Runtime, Run, Artifact, Agent Workspace, Agent Runtime, Workspace Boundary, Operator Agent, and Execution Adapter.

## 2. Shared Skill Contract Updates

- [x] 2.1 Update `skillset/research-paradigm/isomer-rsch-shared/SKILL.md` to route ordinary file and workspace location questions through the Workspace Path Resolver contract.
- [x] 2.2 Update `skillset/research-paradigm/isomer-rsch-shared/references/tbd-surface-registry.md` so ordinary path surfaces are no longer open TBDs or are explicitly mapped to the Workspace Path Resolution contract.
- [x] 2.3 Preserve non-path TBD placeholders for unsettled APIs, schemas, providers, command surfaces, scheduler policy, branching policy, baseline waiver policy, and cost or privacy Gates.

## 3. Research Skill Reference Updates

- [x] 3.1 Update every local `isomer-research-contract.md` copy under `skillset/research-paradigm/isomer-rsch-*/references/` so its path guidance matches the shared Workspace Path Resolution contract.
- [x] 3.2 Replace ordinary path placeholder guidance in route-specific references with semantic Artifact kinds or workspace scopes, such as analysis output Artifact, experiment output Artifact, figure output Artifact, paper Artifact, run log Artifact, or Agent Workspace scratch.
- [x] 3.3 Keep source provenance notes accurate by explaining that source-specific path assumptions now map to Workspace Path Resolver surfaces, not to hard-coded Isomer paths.
- [x] 3.4 Avoid adding concrete per-skill filenames unless the file is a template shipped inside that skill bundle.

## 4. Validation

- [x] 4.1 Run a placeholder search for `[[tbd-surface:path-`, `path-topic-workspace`, `path-workspace-runtime`, `path-agent-workspace`, `path-artifact-layout`, `path-run-logs`, `path-experiment-output`, `path-analysis-output`, `path-paper-layout`, and `path-figure-output`; confirm remaining matches are either removed, mapped to the Workspace Path Resolution contract, or deliberately outside the resolver.
- [x] 4.2 Run a non-path TBD registry consistency check so every remaining `[[tbd-surface:<id>]]` in `skillset/research-paradigm` is registered in a directly linked registry.
- [x] 4.3 Run a hard-coded path scan for `context/explore/`, `extern/orphan/`, archived OpenSpec paths, local absolute paths, and DeepScientist runtime paths in active research-paradigm skill files.
- [x] 4.4 Run `openspec validate define-workspace-path-resolution` and `git diff --check`.
- [x] 4.5 Review the final diff to confirm this change does not define the unrelated command execution API, Artifact API, Finding query API, Gate API, provider contract, or final SQLite schema.
