# Validate Worktrees

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require selected Topic Workspace context and expected agent plan or packet/profile material.
2. Validate that the resolved `topic.repos.main` path exists as the usable shared non-bare topic repository and report the label source.
3. Validate projection roots and metadata when topic env predecessor evidence names them:
   - Check `topic.repos.main.projections.readonly`, `topic.repos.main.projections.writable`, and `topic.repos.main.projections.manifest`.
   - Report projection blockers without materializing missing projections.
4. Validate each expected resolved `agent.workspace` path as a worktree of `topic.repos.main` on `per-agent/<agent-name>/main` unless a specific future branch is in scope.
5. Check Git worktree metadata for duplicate branch checkout and branches outside the owning `per-agent/<agent-name>/` namespace.
6. Check active role binding refs in packet or profile material:
   - Check `agent_name`, `agent_branch`, and derived compatibility `agent_workspace_ref` values.
   - Reject refs outside the selected Topic Workspace or inside another Research Topic's Topic Workspace.
7. Check required semantic support labels:
   - Include `agent.isomer_managed`, `agent.runtime`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, `agent.inbox`, `agent.topic_readonly`, `agent.topic_writable`, and `agent.links`.
   - Report missing paths without creating them silently.
8. Check local tmp posture:
   - Check `topic.repos.main.tmp` and `agent.tmp` resolved paths.
   - Check local ignored disposable semantics, Topic Main Development Repository ignore policy, and tracked tmp contents.
   - Do not delete, move, promote, or rewrite tmp contents.
9. Report static layout and policy problems without repairing them:
   - Include legacy top-level Topic Main Development Repository Isomer directories, legacy support roots, missing ignore policy, unsafe links, missing topic-owned writable policy, tracked conflict markers, and owner/reader split issues.
   - Do not delete, move, or repair files.
10. Check boundary material:
   - Confirm it names write ownership, Peer Read Access, branch rules, generated-link status, topic-owned writable policy when needed, and advisory boundary status when expected.
   - Reject boundary material that describes tmp contents as Peer Read Access, generated-link target material, handoff material, shared material, or durable readiness evidence.
11. If `isomer-srv-agent-env-setup` evidence is present, consume it as separate agent environment evidence:
   - Report the source and derived Agent environment gate paths, readiness by Agent, overall readiness, commands run, blockers, and next action in natural language.
   - Do not rerun gate commands from this Git-only validator.
12. Report validation status without crossing runtime boundaries:
   - Include ready entries, blockers, deferrals, and next operator action.
   - Do not create Agent Instances, Workspace Runtime records, Houmao agents, Execution Adapter material, or agent environment readiness claims.

If the user's task does not map cleanly to these steps, use your native planning tool to run read-only checks first, then report a partial validation status and missing inputs.

## Validation Status

Use `ready` when Git topology, refs, semantic label bindings, local tmp posture, generated links, and boundary material match the plan. Use `ready-with-deferrals` when nonblocking static notes remain. Use `blocked` for unsafe repo state, missing worktrees, missing required support paths, missing or ineffective tmp ignore policy, tracked tmp contents, unsafe generated links, duplicate checkout, unsafe path, cross-topic ref, tracked conflict markers, missing writable policy, owner/reader split issues, unresolved role mapping, or hard-coded default-only evidence where semantic label evidence is required.

Git readiness does not imply per-Agent Workspace environment readiness. When a caller explicitly needs proof that commands pass from each `agent.workspace` cwd, name `isomer-srv-agent-env-setup verify-agent-env-gate` or `setup-agent-env` as the next action, or call it only after this Git topology validation is complete, then report its output as separate service evidence.
