## Context

Topic Actor and Agent Workspace material already has semantic labels for workspace roots, private artifacts, logs, tmp, and sharing surfaces. In practice, manual research runs can still write plain JSON payloads, Markdown drafts, paper PDFs, previews, scripts, and CSV outputs directly into the actor workspace root. That makes the worker branch hard to review, makes generated material hard to find, and creates avoidable merge conflicts when several workers use the same conventional filenames.

This change introduces a worker output root policy for plain generated outputs. It does not replace owner-preserved `topic.records.*` records or Git-tracked source work. It gives skills a standard way to ask Isomer where worker-local plain outputs should go and whether the user prefers a Git commit after each research operation.

## Goals / Non-Goals

**Goals:**

- Provide configurable output roots for Topic Actors and Agent Workspaces, expressed relative to the worker private workspace.
- Provide conflict-safe default output roots under `isomer-managed/worker-output/...` when no user override exists.
- Keep generated output sets namespaced by worker kind, worker name, and operation id so worker branches can merge without filename collisions.
- Let generated `.gitignore` and normal Git behavior determine tracked versus untracked output state.
- Add a per-actor and per-agent `commit_after_operation` preference that skills query and apply after research operations.
- Teach v2 research skills to resolve output policy through `isomer-cli` before writing plain files.

**Non-Goals:**

- Do not make plain worker outputs equivalent to accepted research records.
- Do not add a separate Isomer tracking policy for generated files beyond `.gitignore` and Git status.
- Do not require agents to commit when `commit_after_operation` is false.
- Do not move existing scattered files as part of the core feature; legacy cleanup can be a separate migration or manual repair.
- Do not let output roots escape the selected worker workspace unless a later external-root policy explicitly permits that.

## Decisions

1. Add worker output roots as actor-scoped and agent-scoped path surfaces.

   The default roots should resolve beneath the worker workspace:

   - Topic Actor: `<actor-workspace>/isomer-managed/worker-output/topic-actors/{topic_actor_name}/`
   - Agent: `<agent-workspace>/isomer-managed/worker-output/agents/{agent_name}/`

   This keeps output material close to the worker that produced it while making the purpose explicit. The path should be queryable through `isomer-cli`, with selector requirements matching other actor-scoped and agent-scoped labels.

   Alternative considered: reuse `topic.actors.private_artifacts` and `agent.private_artifacts` directly. That would avoid new labels, but it would not distinguish general worker-local plain output from durable private artifacts, and it would preserve the current ambiguity.

2. Store user overrides as workspace-relative policy, not arbitrary absolute paths.

   Topic Actor bindings and agent workspace defaults or overrides may specify a relative output root. Validation rejects absolute paths, `..`, Project Config Directory targets, cross-topic targets, and paths outside the selected worker workspace. The effective path is still resolved through Workspace Path Resolution so skills do not assemble paths by hand.

   Alternative considered: allow project-relative output roots. That would support central output folders, but it weakens worker ownership and makes branch conflict avoidance harder.

3. Use per-operation output sets inside the root.

   Skills should write generated plain outputs into a child such as `sets/<timestamp>-<operation>-<shortid>/` and include a small manifest or summary when useful. The output root itself should not accumulate stage files such as `paper.pdf`, `experiment-plan.json`, or `summary.md` directly.

   Alternative considered: let each skill choose its own subfolder. That keeps skills flexible but recreates the root-scatter problem one level down.

4. Treat `.gitignore` and Git status as the tracking authority.

   The CLI should not return a separate tracked/untracked flag as policy. Generated `.gitignore` files and user edits determine which files Git can see. When skills need to decide whether files are committable, they should inspect Git status after writing.

   Alternative considered: model `tracking = tracked | untracked` in Isomer config. The user rejected this because Git ignore rules already encode the tracking decision.

5. Add only `commit_after_operation` as a post-action behavior preference.

   The user can set this per Topic Actor or per Agent, with defaults normally false. After a research operation writes files, a skill checks the policy. If true, it runs Git status and commits committable changes according to normal Git behavior. If false, it leaves the workspace dirty and reports the output location.

   Alternative considered: always commit generated outputs. That is too noisy for exploratory research and can commit material that `.gitignore` intentionally hides.

6. Prefer an output-policy query over path-only lookup when skills need behavior.

   `project paths get` is sufficient for a path answer, but a skill also needs `commit_after_operation` and the relative path. A dedicated query such as `project outputs resolve` can return the resolved root, relative root, worker identity, operation set recommendation, and post-action commit preference. If implementation chooses to extend existing path commands instead, the output must still be available through `isomer-cli` in one agent-friendly query.

   Alternative considered: teach skills to read `topic-workspace.toml`. That bypasses current path precedence, actor or agent context inference, and diagnostics.

## Risks / Trade-offs

- [Risk] Skills continue to write to root because the policy is optional guidance. -> Mitigation: update v2 research skill entrypoints and validation to require output policy resolution before plain file writes.
- [Risk] `commit_after_operation=true` commits too much. -> Mitigation: rely on `.gitignore`, use a generated operation-set path, require Git status inspection, and keep the preference disabled by default.
- [Risk] Users configure two workers to the same output root. -> Mitigation: validation should warn or reject configured roots that omit a worker identity segment unless the user explicitly accepts the collision risk.
- [Risk] A worker output set is mistaken for durable evidence. -> Mitigation: specs and skill text must distinguish plain worker outputs from accepted records under `topic.records.*`.
- [Risk] Multiple ways to query path and policy confuse agents. -> Mitigation: document one preferred `isomer-cli` query in skills and keep lower-level path commands for debugging.

## Migration Plan

1. Add semantic labels or output-policy resolver support for Topic Actor and Agent output roots.
2. Extend Topic Workspace Manifest parsing and validation with output root and `commit_after_operation` policy fields.
3. Materialize default output roots under `isomer-managed/worker-output/...` during Topic Actor and Agent Workspace setup.
4. Add CLI query output that returns resolved output root, relative root, worker identity, operation-set recommendation, and `commit_after_operation`.
5. Update v2 research skill guidance and validation so plain file writes use the resolved output policy.
6. Optionally provide a diagnostic or cleanup helper for legacy root-scattered files after the core contract lands.

Rollback is straightforward for behavior: disable skill guidance and stop querying the output policy. Existing generated output directories remain ordinary workspace files and should not block topic operation.

## Open Questions

- Should `commit_after_operation=true` commit the entire worker workspace or only paths under the latest operation set plus explicitly related tracked changes?
- Should configured output roots that omit `{agent_name}` or `{topic_actor_name}` be rejected, warned, or allowed with an explicit `allow_shared_output_root` flag?
- Should the preferred CLI be a new `project outputs resolve` command or an extension of `project self paths` / `project paths get`?
