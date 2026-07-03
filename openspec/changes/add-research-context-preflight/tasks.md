## 1. Shared Preflight Contract

- [ ] 1.1 Add `skillset/research-paradigm/v2/isomer-rsch-shared-v2/references/latest-context-preflight.md` with the Effective Topic Context, self-query, runtime inspection, record lookup, duplicate-record, conflict-routing, worker-output boundary, and storage-neutral snapshot rules.
- [ ] 1.2 Update `skillset/research-paradigm/v2/isomer-rsch-shared-v2/SKILL.md` to route latest-context questions to the new reference.
- [ ] 1.3 Add `latest-context-snapshot` to `skillset/research-paradigm/v2/isomer-rsch-shared-v2/references/semantic-placeholders.md` with required semantic content and producer/consumer guidance.

## 2. V2 Skill Entrypoint Adoption

- [ ] 2.1 Inventory active non-shared v2 research skills with durable record bindings and note any skill or invocation mode that is source-only until accepted Isomer records are written.
- [ ] 2.2 Update active non-shared durable-record-writing v2 `SKILL.md` entry guidance to run the shared latest-context preflight before accepted record writes, record refreshes, durable route decisions, prompt memory, chat memory, prior prose, route records, paper state, or remembered context is trusted as current research state.
- [ ] 2.3 Keep each skill's entrypoint concise by importing the shared reference instead of duplicating the full command ladder.
- [ ] 2.4 Preserve existing stage-specific readiness gates after the preflight, including scout framing, baseline comparator selection, idea objective and board locking, experiment contract locking, analysis boundary locking, writing control-state refresh, and finalization closure inventory.
- [ ] 2.5 Preserve archived worker-output-root guidance: plain generated files still use resolved worker output policy, operation-specific output sets, and `commit_after_operation`; latest-context preflight applies at durable record acceptance or refresh boundaries.

## 3. Stage Context Freshness

- [ ] 3.1 Update selected context-producing references so first accepted durable context objects record the Effective Topic Context, Workspace Runtime inspection, relevant placeholder records checked, and freshness verdict.
- [ ] 3.2 Add guidance for prompt-versus-durable-context conflicts, including route to scout, baseline, decision, workspace bootstrap, paper-outline, or blocker when the current stage is no longer ready.
- [ ] 3.3 Add guidance for multiple ready records for the same placeholder: newest ready is only the default candidate, explicit active or supersession metadata wins, and unresolved conflict routes to decision or blocker handling.
- [ ] 3.4 Confirm generated Markdown views remain review material and structured payload plus record metadata remain authoritative where structured records exist.

## 4. Validation

- [ ] 4.1 Add research-paradigm validator coverage that reports active non-shared v2 `SKILL.md` files with durable record bindings that omit the shared latest-context preflight reference or freshness-intent wording.
- [ ] 4.2 Exempt `isomer-rsch-shared-v2`, migration notes, source-copy material under `org/`, passive templates, non-active provenance material, and source-only invocation wording before accepted Isomer records are written from the stage-entrypoint preflight rule.
- [ ] 4.3 Add unit tests for missing preflight, accepted concise shared imports, freshness-intent wording, worker-output guidance not counting as preflight, and false-positive exemptions.
- [ ] 4.4 Ensure the validator rule uses global `isomer-cli` command wording and does not require `pixi run isomer-cli` in skill guidance.

## 5. Verification

- [ ] 5.1 Run `pixi run validate-research-skills`.
- [ ] 5.2 Run focused unit tests for the research-paradigm validator.
- [ ] 5.3 Inspect the changed shared reference and at least scout, idea, experiment, write, and finalize entrypoints to confirm the preflight appears before durable record work while worker-output policy guidance remains intact for plain file writes.
- [ ] 5.4 Run `openspec status --change add-research-context-preflight` and confirm the change is apply-ready.
