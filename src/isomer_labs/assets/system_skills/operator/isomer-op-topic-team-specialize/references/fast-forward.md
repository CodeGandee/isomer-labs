# Fast Forward

Use this subcommand for natural-language requests like `specialize <team-path> over topic <topic>`. Carry the supplied team path as the selected Domain Agent Team Template and the supplied topic as the Research Topic input.

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Determine whether this is full `fast-forward` or targeted fast-forward recovery:
   - Use full `fast-forward` for natural-language end-to-end requests such as `specialize <team-path> over topic <topic>`.
   - Use targeted recovery only when another selected procedural subcommand found missing predecessor artifacts and the user confirmed inclusive mode, chose exclusive mode, or already gave clear permission to proceed.
   - For full `fast-forward`, query `scripts/query_step_dependencies.py path --target finalize-topic-team --include-target`.
   - For inclusive targeted recovery, query `scripts/query_step_dependencies.py path --target <target_subcommand> --include-target`.
   - For exclusive targeted recovery, query `scripts/query_step_dependencies.py path --target <target_subcommand> --exclude-target`.
2. Determine whether the user supplied enough topic substance:
   - Accept a concrete Research Topic, an explicit registered topic ref with concrete topic material, or enough source material to seed a topic.
   - If no topic substance is supplied, ask for the actual research topic and stop before running `init-topic`.
3. Check for prepared-topic evidence:
   - If reusable evidence from `isomer-op-topic-creator`, Topic Workspace registration, or Topic Manager topology exists, consume the Research Topic ref, Topic Workspace ref, topic overview, Workspace Runtime readiness, topic environment readiness, `topic.repos.main` readiness, current Topic Actor roster, and Topic Actor Workspace refs instead of recreating those common artifacts.
   - If common preparation is missing and the request is full `fast-forward`, create or delegate topic setup before team-specific stages.
   - Preserve active Topic Actor bindings and Topic Actor Workspace refs. Do not archive, delete, or convert them into Agent Workspace material.
4. Execute the returned path in order:
   - Load each step's subcommand page before running that step.
   - Respect each step's local prerequisite evidence, produced output, mutation notes, and unrecoverable blockers.
   - Stop on the same clarification, registration, environment-binding, resource-safety, and live-runtime blockers as a direct subcommand run.
5. Stop at the targeted or full stop point:
   - In inclusive targeted recovery, stop after the target subcommand completes.
   - In exclusive targeted recovery, stop immediately before the target subcommand.
   - In full `fast-forward`, stop at final topic-team summary output from `finalize-topic-team`.
   - Run `approve-profile` or `materialize-profile` only when the user explicitly asks for that static profile-material boundary.
   - Require the needed validation or approval inputs before crossing that boundary.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the selected topic, template, procedural subcommands, output contract, and guardrails, then execute the plan.

## Targeted Recovery Form

Full `fast-forward` runs the static topic-team setup path through `finalize-topic-team`. Targeted fast-forward recovery is the bounded form used when another procedural subcommand was selected but its predecessor artifacts are missing.

Targeted recovery inputs:

- `target_subcommand`: the subcommand the user attempted to run.
- `include_target`: `true` by default for inclusive recovery, or `false` for exclusive recovery.
- Available topic, workspace, template, runnable-target, Agent Name, selected-agent, or approval context from the original request.

Use the local dependency query helper:

```bash
python scripts/query_step_dependencies.py path --target <target_subcommand> --include-target
python scripts/query_step_dependencies.py path --target <target_subcommand> --exclude-target
python scripts/query_step_dependencies.py explain --target <target_subcommand>
```

In inclusive targeted recovery, run the returned path with the target included. In exclusive targeted recovery, run the returned predecessor path and stop before the target, reporting whether the target is ready or which blocker remains. Do not continue to later specialization, validation, finalization, approval, or materialization stages unless they are the selected target or the user explicitly asks for them.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

### Essential Output

Lead with the fast-forward outcome and name the Research Topic and Topic Workspace. Summarize registration and environment binding, the selected Domain Agent Team Template and copied material, Topic and Agent environment readiness when checked, validation, important overview, gate, copied-material, or summary paths, blockers and deferrals, and the next operator action.

### Complete Output

Include semantic labels and resolved paths for topic overview, topic env source intent, topic env target spec, agent env source intent, and agent env target spec when present; also include reused common preparation refs, current Topic Actor roster, Topic Actor Workspace refs, registration status, registered topic and workspace refs, environment binding status, selected Domain Agent Team Template, copied material paths, topic environment status, Topic Main Development Repository and projection predecessor evidence, Agent Workspace paths, topic-team validation status, `isomer-topic-summary.md` path, blockers, deferrals, and next operator action.
