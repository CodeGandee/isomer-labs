## Context

The v2 research skills already use semantic placeholders and local `placeholder-bindings.md` pages, and `isomer-cli ext research records` already provides a transitional CRUD surface for topic-scoped research records. The recently updated storage-support plan maps DeepScientist paper-line surfaces such as selected outlines, evidence ledgers, experiment matrices, writing plans, manuscript drafts, bundle manifests, review packets, and rebuttal packets onto Isomer record kinds, semantic labels, and paper-specific profiles.

The current binding pages still map many writing placeholders through generic profile prefixes, which loses the distinction between active paper contract views, artifact bodies, resumable writing tasks, evidence ledger indexes, and package manifests. The implementation should bring the skill files into alignment with the plan while preserving the research skills convention: workflow prose keeps placeholders, storage details live in binding pages, and agents use semantic labels rather than hard-coded Topic Workspace paths.

## Goals / Non-Goals

**Goals:**

- Bind writing-related v2 placeholders to paper-line profiles such as `paper.contract.selected-outline`, `paper.evidence-ledger`, `paper.experiment-matrix`, `paper.writing-plan`, `paper.claim-evidence-map`, `paper.validation.*`, `package.paper.bundle-manifest`, `review.*`, `rebuttal.*`, `figure.export`, and `release.open-source-*`.
- Use current semantic labels by storage class: `topic.records.views` for paper contract views and validation state, `topic.records.artifacts` for bodies and packages, `topic.records.tasks` for resumable writing or reviewer TODO work, and `topic.records.runs` or `topic.records.logs` for execution-derived material.
- Keep placeholders stable in `SKILL.md` and `migrate/placeholders.md` unless the registry has a missing or clearly wrong placeholder kind.
- Update binding commands to include explicit `--semantic-label`, paper-specific `--profile`, exact `--placeholder`, owning `--skill`, producer, consumer, and metadata fields that help later agents query paper state.
- Validate the updated skills with the existing research skillset validator and document any follow-up if the validator cannot yet express a paper-specific check.

**Non-Goals:**

- Do not add paper-specific top-level semantic labels such as `topic.paper` or `topic.paper.outlines`.
- Do not implement native `project records ...` commands or new Workspace Runtime tables.
- Do not replace placeholders in workflow prose with concrete paths, record ids, or artifact filenames.
- Do not port DeepScientist's `quest_root/paper/` layout as the Isomer storage authority.

## Decisions

1. Use paper profiles, not new semantic labels. The existing semantic labels describe lifecycle storage classes well enough, while profiles describe the paper artifact meaning. This keeps the storage layer generic and avoids one-off paper directories becoming new platform concepts.

2. Treat active paper contract state as views. Selected outline, evidence ledger index, experiment matrix, claim-evidence map, validation reports, and paper-line state should use `view_manifest` records under `topic.records.views` when they are read surfaces or control boards. Raw bodies can still be stored as artifacts when a skill needs to preserve the exact payload.

3. Treat manuscript and package bodies as artifacts. Draft sections, LaTeX snapshots, references, compile reports, PDFs, review reports, rebuttal packets, and bundle manifests should use `artifact` records under `topic.records.artifacts` until native package or evidence labels exist.

4. Treat resumable writing and reviewer work as tasks. Writing plans and reviewer-linked TODOs should use `research_task` records under `topic.records.tasks` when agents need to resume, assign, or query work. If a writing plan is only a compiled board, it can remain a `view_manifest`.

5. Add metadata only where it improves queryability. Binding command examples should include stable paper metadata such as `selected_outline_ref`, `paper_surface`, `package_type`, `section_id`, `claim_id`, `reviewer_item_id`, or `main_or_appendix` when those fields naturally belong to the placeholder. They should not invent required schema fields that the current extension cannot validate.

## Risks / Trade-offs

- Binding commands may become long and harder to scan -> Keep the same tabular binding convention and update only the writing-related rows that benefit from paper-specific profiles.
- Some Nature companion skills may have writing artifacts that are paper-adjacent but not full paper-line state -> Bind them to paper profiles only when they produce manuscript, bibliography, figure, data availability, or package artifacts that downstream paper skills consume.
- Existing validation may check placeholder coverage but not whether a profile is semantically correct -> Run current validation and leave a focused follow-up task if a paper-profile lint rule is needed.
- Future `topic.records.evidence` and `topic.records.packages` labels may change preferred labels -> Keep command shapes in binding pages so later changes can update labels without rewriting workflow prose.

## Migration Plan

1. Inventory writing-related placeholders and binding rows across `isomer-rsch-paper-outline-v2`, `isomer-rsch-write-v2`, `isomer-rsch-review-v2`, `isomer-rsch-rebuttal-v2`, `isomer-rsch-finalize-v2`, `isomer-rsch-paper-plot-v2`, `isomer-rsch-figure-polish-v2`, and Nature companion v2 skills.
2. Update rows whose durable storage role is now covered by the paper-writing artifact mapping.
3. Check whether any `migrate/placeholders.md` kind values conflict with the durable role and adjust only when the mismatch would mislead the binding page.
4. Run `pixi run validate-research-skills` and repair binding coverage, registry drift, and local reference issues.
5. Run `pixi run docs-validate` if shared plan or documentation text changes.
