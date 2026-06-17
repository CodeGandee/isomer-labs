## 1. Coordination Setup

- [x] 1.1 Inspect the worktree and preserve the existing uncommitted `isomer-rsch-analysis/SKILL.md` Imsight-formatting edit instead of overwriting it.
- [x] 1.2 Read `skillset/research-paradigm/README.md`, `isomer-rsch-analysis/SKILL.md`, the analysis references, the shared TBD registry, and the Imsight `format-skill` guidance before assigning workers.
- [x] 1.3 Launch subagents with disjoint write scopes for foundation, baseline, idea/execution, writing/review, and figures/science skill folders.
- [x] 1.4 Tell every subagent that other workers are editing the codebase, that it must not revert unrelated changes, and that it must report changed files and unresolved issues.
- [x] 1.5 Reserve shared-file integration for the main agent, including the suite README, shared TBD registry, and final validation.

## 2. Foundation Skills Worker

- [x] 2.1 Enrich `isomer-rsch-intake` from DeepScientist `intake-audit` with local references for state audit, current-board packet, asset trust taxonomy, intake routing, provenance, Imsight workflow, and manifest.
- [x] 2.2 Enrich `isomer-rsch-scout` from DeepScientist `scout` with local references for paper triage, literature scout template, evaluation contract, baseline shortlist, operational guidance, provenance, Imsight workflow, and manifest.
- [x] 2.3 Enrich `isomer-rsch-decision` from DeepScientist `decision` with local references for strategic decision records, route criteria, canonical actions, checkpoint or resume template, operational guidance, provenance, Imsight workflow, and manifest.
- [x] 2.4 Enrich `isomer-rsch-finalize` from DeepScientist `finalize` with local references for finalization checklist, claim ledger, package inventory, resume packet, closure gate guidance, provenance, Imsight workflow, and manifest.
- [x] 2.5 Validate the foundation worker output for self-containment, source-runtime term mapping, registered TBD placeholders, and `agents/openai.yaml` display names.

## 3. Baseline Worker

- [x] 3.1 Enrich `isomer-rsch-baseline` from DeepScientist `baseline` with local route-selection, comparability-contract, route-record, gate-checklist, evidence-flow, payload-template, boundary-case, codebase-audit, operational-guidance, and provenance references.
- [x] 3.2 Rewrite the `isomer-rsch-baseline` entrypoint with Imsight workflow structure and direct reference routing.
- [x] 3.3 Add or refresh `isomer-rsch-baseline/agents/openai.yaml` with `interface.display_name: "isomer-rsch-baseline"` and a default prompt invoking `$isomer-rsch-baseline`.
- [x] 3.4 Validate baseline terminology so source paths, registry publishing, `artifact.confirm_baseline(...)`, `artifact.waive_baseline(...)`, `uv`, Docker, and service endpoints are translated to Isomer Artifacts, Evidence Items, Decision Records, Gates, Capability Bindings, Execution Adapters, or TBD surfaces.

## 4. Idea and Execution Worker

- [x] 4.1 Enrich `isomer-rsch-idea` from DeepScientist `idea` with local objective-contract, current-board, literature survey, related-work, research-history, idea-sourcing, thinking-flow, brainstorming, pre-idea draft, selection-gate, provenance, Imsight workflow, and manifest resources.
- [x] 4.2 Enrich `isomer-rsch-optimize` from DeepScientist `optimize` with local method-brief, candidate-board, candidate-ranking, frontier-review, optimize-checklist, brief-shaping, operational-guidance, fusion, debug, plateau, codegen-route, optimization-memory, provenance, Imsight workflow, and manifest resources.
- [x] 4.3 Enrich `isomer-rsch-experiment` from DeepScientist `experiment` with local plan template, checklist template, evidence ladder, execution playbook, operational guidance, run-record template, provenance, Imsight workflow, and manifest resources.
- [x] 4.4 Validate idea and optimize terminology so candidate ideas, durable lines, implementation attempts, frontier records, and branch promotion map to Isomer Artifacts, View Manifests, Research Branch decisions, Decision Records, and TBD surfaces without requiring DeepScientist artifact APIs.
- [x] 4.5 Validate experiment terminology so execution, run logs, metric contracts, long-running monitoring, and evaluation summaries map to Runs, Evidence Items, Research Claims, Provenance Records, Capability Bindings, Execution Adapters, and TBD surfaces.

## 5. Writing and Review Worker

- [x] 5.1 Enrich `isomer-rsch-write` from DeepScientist `write` with local writing-contract, citation and bibliography, manuscript-cleanliness, oral package, oral writing, experiments-analysis, section-rewrite, provenance, Imsight workflow, and manifest resources.
- [x] 5.2 Decide whether venue LaTeX templates from `write/templates/` are sanitized enough for this change; import directly useful templates under `assets/` or record a deferred follow-up task.
- [x] 5.3 Enrich `isomer-rsch-review` from DeepScientist `review` with local audit gate, evidence authenticity checklist, literature benchmark, review-report template, revision-log template, experiment-todo template, follow-up routing, provenance, Imsight workflow, and manifest resources.
- [x] 5.4 Enrich `isomer-rsch-rebuttal` from DeepScientist `rebuttal` with local reviewer-item contract, review matrix, action plan, response letter, evidence update, text delta, rebuttal routing, provenance, Imsight workflow, and manifest resources.
- [x] 5.5 Enrich `isomer-rsch-paper-outline` from DeepScientist `paper-outline` with local outline contract, paper-outline template, mature-outline checklist, claim-evidence boundary, analysis-plan roles, outline patterns, provenance, Imsight workflow, and manifest resources.
- [x] 5.6 Validate writing and review terminology so paper paths, review policies, response matrices, citation providers, `artifact.*`, `memory.*`, and `bash_exec(...)` are translated to Isomer Artifacts, Evidence Items, Decision Records, Gates, provider TBDs, Capability Bindings, or Execution Adapters.

## 6. Figures and Science Worker

- [x] 6.1 Enrich `isomer-rsch-paper-plot` from DeepScientist `paper-plot` with local style-routing, data-substitution, per-style references, provenance, Imsight workflow, and manifest resources.
- [x] 6.2 Decide whether paper-plot template scripts are sanitized enough for this change; import directly useful scripts under `scripts/` or record a deferred follow-up task.
- [x] 6.3 Enrich `isomer-rsch-figure-polish` from DeepScientist `figure-polish` with local surface-class, chart-selection, style-contract, self-review, export-recording, provenance, optional style asset, Imsight workflow, and manifest resources.
- [x] 6.4 Resolve the unregistered `[[tbd-surface:schema-figure-output]]` placeholder by registering it in the shared TBD registry or replacing it with existing registered placeholders.
- [x] 6.5 Enrich `isomer-rsch-science` from DeepScientist `science` with local package-check, claim-type discipline, HPC via Execution Adapter, science-task brief, evidence-recording, domain-index, package-index, provenance, Imsight workflow, and manifest resources.
- [x] 6.6 Decide whether the large science package-card catalog should be imported now or deferred to a follow-up resource-focused change.
- [x] 6.7 Validate figure and science terminology so plotting workspaces, export schemas, style assets, package catalogs, HPC/SSH/SLURM guidance, and Science Evidence Graph language map to Isomer Artifacts, Evidence Items, Research Claims, Provenance Records, Capability Bindings, Execution Adapters, Gates, and TBD surfaces.

## 7. Integration and Shared Files

- [x] 7.1 Review all subagent diffs and resolve any conflicts without reverting unrelated work.
- [x] 7.2 Update shared suite docs only where needed to reflect the enriched self-contained bundle pattern and any deferred large-resource decisions.
- [x] 7.3 Update the shared TBD registry for any newly used placeholders and remove or replace unregistered placeholders.
- [x] 7.4 Confirm every active `isomer-rsch-*` skill either has local references for source-derived detail or records an explicit rationale for deferring source resources.
- [x] 7.5 Confirm every enriched `agents/openai.yaml` uses the skill name itself as `interface.display_name` and invokes the same skill in `default_prompt`.

## 8. Validation

- [x] 8.1 Run the skill-creator quick validator for every `skillset/research-paradigm/isomer-rsch-*` folder.
- [x] 8.2 Run a search for active dependencies on `context/explore/`, `extern/orphan/`, archived OpenSpec paths, and local absolute paths from enriched skill entrypoints and linked references.
- [x] 8.3 Run a coupling search for `DeepScientist`, `artifact.`, `memory.`, `bash_exec`, `DeepXiv`, `quest`, `worktree`, `workspace_mode`, `continuation_policy`, `auto_continue`, `wait_for_user_or_resume`, source provider names, and source runtime paths, then verify remaining matches are provenance, mapping, or rejection notes.
- [x] 8.4 Run a placeholder search for `[[tbd-surface:` and verify every id is registered in a directly linked TBD registry.
- [x] 8.5 Inspect each enriched `SKILL.md` for near-top `## Workflow`, numbered steps, concise reference routing, and freeform fallback.
- [x] 8.6 Run `git diff --check` and review the final diff for accidental source runtime assumptions, hard-coded source paths, or unsanitized copied assets/scripts.
- [x] 8.7 Run `openspec status --change "enrich-isomer-rsch-skills"` and confirm the change is apply-ready or complete according to OpenSpec.
