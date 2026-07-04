## Context

The v2 research-paradigm skills already use Isomer terms such as Research Topic, Topic Workspace, Workspace Runtime, and durable research records. Several skills tell agents to recover, refresh, or reconstruct context, but the wording is local to each stage. `isomer-rsch-scout-v2` has a strong Pre-Scout Gate, `isomer-rsch-workspace-mgr-v2` requires fresh runtime inspection during bootstrap, and paper-facing skills refresh paper state, yet there is no shared entry contract that says skills with durable record bindings must resolve latest Effective Topic Context before accepting durable record writes or using prompt memory as current research state.

The platform already has the needed read surfaces. `isomer-cli --print-json project context show` resolves Effective Topic Context and source metadata. `isomer-cli --print-json project self queries` advertises safe follow-up commands. `isomer-cli --print-json project runtime inspect` checks Workspace Runtime state. `isomer-cli --print-json ext research records list/show` can inspect placeholder-specific records. This change should teach agents to use those surfaces consistently instead of adding a new CLI dependency.

The archived `add-worker-output-root-policy` change now requires v2 skills that write plain generated files to resolve worker output policy and apply `commit_after_operation`. This change is complementary: worker output policy governs plain worker-local files, while latest-context preflight governs accepted durable records, record refreshes, and durable route or claim decisions.

## Goals / Non-Goals

**Goals:**

- Define one shared latest-context preflight reference for active non-shared v2 research skills with durable record bindings.
- Add a semantic object for a context snapshot or freshness verdict without forcing a concrete storage binding.
- Require stage skills to run the preflight before accepted record writes, record refreshes, or durable stage decisions when the skill depends on a Research Topic, Research Inquiry, Research Task, Topic Workspace, current route, paper state, or durable records.
- Teach agents how to handle prompt-versus-durable-context conflicts and duplicate ready records.
- Add validation so future v2 skill entrypoints keep the shared preflight visible.

**Non-Goals:**

- Do not add new `isomer-cli` commands.
- Do not make Effective Topic Context a durable lifecycle object or store it wholesale on every record.
- Do not require broad literature or web refresh when the issue is only local topic context freshness.
- Do not solve graph-index lineage selection in this change; use available record list/show behavior and conflict routing until graph queries exist.
- Do not force all skills to create a new standalone context record when their existing context brief or contract can carry the freshness verdict.
- Do not replace worker-output-root policy for plain generated files, operation output sets, `.gitignore`, Git status, or `commit_after_operation`.
- Do not require the latest-context preflight for standalone source-only reading until the skill writes or refreshes accepted Isomer records.

## Decisions

1. Add `references/latest-context-preflight.md` under `isomer-rsch-shared-v2`.

   This keeps the full procedure in one place. Stage skills should reference it in their first workflow step and keep their own wording short. The reference should define the command ladder, source priority, freshness verdict, and conflict routes.

   Alternative considered: duplicate the full command ladder in every v2 skill. That would make each skill self-contained in isolation, but it would drift quickly and make future command changes expensive.

2. Add a shared semantic object named `latest-context-snapshot`.

   The object should describe the selected Research Topic, Research Topic Config source, Topic Workspace, Workspace Runtime readiness, effective actor or agent context, checked records, and conflict verdict. It should remain semantic, not storage-bound. Stage skills can satisfy it through their existing first durable object, such as `<SCOUT_CONTEXT_BRIEF>`, `<BASELINE_CONTEXT_BRIEF>`, `<OBJECTIVE_CONTRACT>`, `<EXPERIMENT_CONTEXT_BRIEF>`, `<PAPER_CONTROL_STATE>`, or `<FINALIZE_CONTEXT_BRIEF>`.

   Alternative considered: create a new migration placeholder and binding page for every skill. That is heavier than needed and would add records that mostly duplicate stage context briefs.

   User decision: keep `latest-context-snapshot` semantic-only in this change. A later View Manifest binding can be proposed if long-running topics need a first-class context view.

3. Use existing read commands as the preflight contract.

   The preflight should prefer:

   - `isomer-cli --print-json project context show [--topic <topic>]`
   - `isomer-cli --print-json project self queries`
   - `isomer-cli --print-json project runtime inspect --topic <topic>`
   - `isomer-cli --print-json ext research records list --topic <topic> --placeholder '<PLACEHOLDER>'`
   - `isomer-cli --print-json ext research records show <record-id> --topic <topic> --include-payload --include-rendered-body`
   - `isomer-cli --print-json project paths get <semantic-label> --topic <topic>` when path labels matter

   This matches current CLI behavior and avoids teaching agents to inspect hard-coded paths or scan sibling directories. The global `isomer-cli` spelling also matches research skill binding rules.

   Alternative considered: read `.isomer-labs/manifest.toml`, Research Topic Config files, and runtime SQLite files directly. Direct reads are useful for debugging, but the agent-facing contract should use Isomer commands that preserve selector precedence and diagnostics.

4. Treat duplicate ready records as a freshness decision, not an implicit merge.

   `records list` can return several ready records for the same placeholder. The preflight should teach agents to select the newest ready record only as the default candidate, prefer explicit active/supersession metadata when available, and stop for decision or blocker routing when multiple records conflict.

   Alternative considered: always take the newest record. That is simple, but it can hide route reversals, duplicate generated views, or manual corrections.

5. Validate entrypoint adoption with a lightweight text contract.

   The research-paradigm validator should check active non-shared v2 `SKILL.md` files with durable record bindings for a reference to the shared preflight and one freshness-intent phrase. `isomer-rsch-shared-v2` owns the reference and should not be required to consume itself. Non-active `org/`, `migrate/`, and passive template material should remain outside this rule. Standalone source-only invocation text may say that preflight is skipped until the skill writes or refreshes accepted Isomer records.

   Alternative considered: validate every reference page and every stage-specific template. That would catch more omissions, but it is too brittle for the first pass.

6. Keep worker output policy and latest-context preflight separate.

   Plain generated files, including payload staging files, Markdown drafts, figures, paper builds, local reports, and previews, remain governed by the worker-output-root policy and `project outputs policy`. Those files are not durable research records merely because they exist. When a skill promotes or records such material as an accepted Artifact, Evidence Item, Run record, Decision Record, View Manifest, context brief, contract, route decision, or other durable research record, the latest-context preflight must have been run or refreshed for that acceptance boundary.

   Alternative considered: make the latest-context preflight run before every plain file write. That would blur two policies, add busywork to source-only or draft-only tasks, and conflict with the archived worker output policy's narrower file-placement contract.

## Risks / Trade-offs

- [Risk] The preflight becomes busywork for simple invocations. → Mitigation: make the minimum preflight small and allow stage-local context briefs to carry the freshness verdict instead of requiring a new artifact.
- [Risk] Agents may run expensive broad searches under the word "latest". → Mitigation: define "latest context" as Isomer topic and record state unless the stage already requires external literature, repository, benchmark, journal, or package freshness.
- [Risk] Duplicate ready records remain ambiguous until graph-index support lands. → Mitigation: require explicit conflict handling and route to decision or blocker when the active record cannot be identified responsibly.
- [Risk] Validator checks could become too textual. → Mitigation: check for the shared reference and a small set of durable-context phrases, not exact prose.
- [Risk] Agents confuse worker-local output files with accepted records. → Mitigation: reference the archived worker-output-root policy boundary and require preflight only at durable record acceptance, refresh, or decision time.

## Migration Plan

1. Add the shared latest-context preflight reference and semantic registry entry.
2. Update active non-shared v2 `SKILL.md` entry guidance for skills with durable record bindings to import the shared preflight before accepted durable record writes, record refreshes, or durable stage decisions.
3. Update selected reference pages where the first context object needs an explicit freshness verdict.
4. Add validator and unit-test coverage for v2 preflight adoption using the durable-record-binding scope and freshness-intent wording.
5. Run `pixi run validate-research-skills`.

Rollback is straightforward because the change is documentation and validation only: remove the shared reference, remove entrypoint references, and remove the validator rule.

## Deferred Follow-up

- A later change may bind `latest-context-snapshot` to a lightweight View Manifest if long-running topics need a first-class context view.
- `ext research records list --latest` or `--active` remains out of scope here and should be handled after or inside graph-index work.
- Standalone source-only reading may skip the preflight until a skill writes or refreshes accepted Isomer records.
