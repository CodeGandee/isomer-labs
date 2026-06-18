## 1. Main Spec Alignment

- [x] 1.1 Create the main `research-lifecycle-state` spec from the delta spec, including Research Topic, Research Inquiry, Research Task, Run, Workflow Stage Cursor, Research Inquiry Relationship, Agent Team Instance lifecycle state, and validation requirements.
- [x] 1.2 Update the main `research-paradigm-skills` spec so Generic Research Vocabulary uses Research Topic, Research Inquiry, Research Inquiry Relationship, Research Task, Run, Topic Workspace, Workflow Stage Cursor, and Agent Team Instance lifecycle state.
- [x] 1.3 Update the main `research-paradigm-skills` spec so `schema-stage-cursor`, `schema-agent-team-state`, and `policy-branching` are no longer described as open TBD surfaces.
- [x] 1.4 Update the main `research-recording-contracts` spec so durable record lifecycle refs point to accepted Research Lifecycle State objects without redefining their state machines.

## 2. Shared Skill Contract Updates

- [x] 2.1 Update `isomer-rsch-shared/references/tbd-surface-registry.md` to map or remove resolved lifecycle TBD ids: `schema-stage-cursor`, `schema-agent-team-state`, and `policy-branching`.
- [x] 2.2 Update `isomer-rsch-shared/references/source-term-mapping.md` so Research Goal, Research Thread, Research Branch, and Isomer Workspace map to accepted lifecycle and workspace terms.
- [x] 2.3 Update `isomer-rsch-shared/SKILL.md` to name accepted lifecycle objects, accepted Workflow Stage Cursor routing state, and accepted Agent Team Instance lifecycle state.
- [x] 2.4 Keep unrelated open TBD entries for command execution, scheduler policy, Skill Binding, literature provider, baseline-waiver policy, and cost/privacy Gate policy.

## 3. Local Research Contract Copies

- [x] 3.1 Update every `skillset/research-paradigm/isomer-rsch-*/references/isomer-research-contract.md` copy to consume Research Lifecycle State.
- [x] 3.2 Remove resolved lifecycle TBD placeholders from local research contract copies without changing unrelated execution, provider, scheduler, Skill Binding, baseline-waiver, or cost/privacy placeholders.
- [x] 3.3 Replace stale active terms in local contract copies: Research Goal to Research Topic, Research Thread to Research Inquiry, Research Branch to Research Inquiry Relationship, and Isomer Workspace to Topic Workspace.
- [x] 3.4 Confirm local contract copies still preserve Workspace Path Resolution and Research Recording Contracts guidance.

## 4. Route-Specific Skill Reference Updates

- [x] 4.1 Update intake, scout, baseline, idea, optimize, experiment, analysis, decision, write, review, rebuttal, and finalize references that mention Workflow Stage, Research Inquiry Relationship, branch, pause, resume, blocker, or route state.
- [x] 4.2 Update optimize-specific references so candidate promotion uses Research Inquiry Relationship policy and does not create a relationship for every implementation attempt.
- [x] 4.3 Update routing and handoff language so Research Inquiry is treated as a question object and not as a parallel execution scope.
- [x] 4.4 Update Agent Team Instance language so Topic-level parallelism and Task-level parallelism are explicit, while Skill Binding and concrete capability binding remain out of scope.
- [x] 4.5 Preserve Gate versus Decision Record boundaries and do not turn every inquiry relationship into a Decision Record.

## 5. Plan and Registry Cleanup

- [x] 5.1 Update `context/plans/research-paradigm-skill-gaps.md` to mark Stage 2 complete after implementation and keep later stages open.
- [x] 5.2 Confirm Stage 3, Stage 4, and Stage 5 placeholders remain open in the plan and registry.
- [x] 5.3 Review docs for accidental scheduler, command execution, literature provider, Skill Binding, baseline-waiver, or cost/privacy policy definitions.

## 6. Validation and Consistency Checks

- [x] 6.1 Run `openspec validate define-research-lifecycle-state`.
- [x] 6.2 Run `openspec validate research-lifecycle-state`, `openspec validate research-paradigm-skills`, and `openspec validate research-recording-contracts` after main specs are synced.
- [x] 6.3 Search active `skillset/research-paradigm` text for `[[tbd-surface:schema-stage-cursor]]`, `[[tbd-surface:schema-agent-team-state]]`, and `[[tbd-surface:policy-branching]]` and confirm resolved placeholders are removed or mapped to Research Lifecycle State.
- [x] 6.4 Search active `skillset/research-paradigm` text for stale terms Research Goal, Research Thread, Research Branch, and Isomer Workspace and confirm remaining matches are provenance, migration notes, or source-term mapping only.
- [x] 6.5 Search active skill text for `Research Inquiry` near parallel execution language and confirm parallelism is expressed only at Topic or Task scope.
- [x] 6.6 Search remaining `[[tbd-surface:*]]` placeholders and confirm every remaining id is still registered in the shared TBD registry.
- [x] 6.7 Run `git diff --check`.

## 7. Final Review

- [x] 7.1 Confirm no application code, command runner, scheduler, provider, credential, or storage migration was introduced by this change.
- [x] 7.2 Confirm Research Recording Contracts still own Artifact, Evidence Item, Finding, Research Claim, Decision Record, Gate, and Provenance Record semantics.
- [x] 7.3 Confirm Workspace Path Resolution still owns Topic Workspace, Workspace Runtime, Agent Workspace, Agent Runtime, Run log, and Artifact path resolution.
- [x] 7.4 Summarize remaining placeholders and recommend the next contract cluster after lifecycle state.
