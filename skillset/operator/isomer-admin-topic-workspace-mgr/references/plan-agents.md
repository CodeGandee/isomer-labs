# Plan Agents

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require selected Topic Workspace context and a role binding source: Topic Team Instantiation Packet, Topic Agent Team Profile material, or explicit operator-provided role-to-agent-key mapping.
2. Read active role bindings only. Ignore inactive role bindings unless the operator explicitly asks to report them.
3. Normalize each `agent-key` to a path-safe lowercase kebab-case segment when possible, preserving a clear mapping back to the source role id.
4. Reject empty keys, `.` or `..`, slashes, path separators, shell metacharacters, whitespace-only values, and normalized key collisions.
5. Plan each Agent Workspace path as `<topic-workspace-dir>/agents/<agent-key>` and each default branch as `per-agent/<agent-key>/main`.
6. Plan `role_bindings.<role-id>.agent_workspace_ref` as either the absolute Agent Workspace path or an equivalent project-relative ref under the selected Topic Workspace.
7. Report proposed packet/profile edits separately from filesystem work so the operator can approve mutation.

If the user's task does not map cleanly to these steps, use your native planning tool to produce a read-only plan first, then ask for explicit mutation only when edits are needed.

## Mapping Rules

An `agent-key` is a friendly Git and path namespace such as `alice`; it is not an Agent Instance id. Agent Instance ids remain globally unique runtime records created later by Workspace Runtime.

The planned `agent_workspace_ref` must resolve under the selected Topic Workspace and normally under `<topic-workspace-dir>/agents/<agent-key>`.

## Output

Report role ids, agent keys, Agent Workspace paths, `agent_workspace_ref` values, default branches, changed packet/profile files, blockers, and `next_operator_action`.
