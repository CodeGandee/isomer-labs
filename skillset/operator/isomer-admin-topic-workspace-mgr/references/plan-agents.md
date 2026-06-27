# Plan Agents

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require selected Topic Workspace context and a role binding source: Topic Team Instantiation Packet, Topic Agent Team Profile material, or explicit operator-provided role-to-agent-name mapping.
2. Read active role bindings only. Ignore inactive role bindings unless the operator explicitly asks to report them.
3. Normalize each `agent-name` to a path-safe lowercase segment when possible, preserving a clear mapping back to the source role id.
4. Reject empty keys, `.` or `..`, slashes, path separators, shell metacharacters, whitespace-only values, and normalized key collisions.
5. Resolve `agent.workspace` for each Agent Name through Workspace Path Resolution, then resolve required support labels such as `agent.isomer_managed`, `agent.private_artifacts`, `agent.runtime`, `agent.scratch`, `agent.public_share`, and `agent.links`; record each label's path and source.
6. Plan `role_bindings.<role-id>.agent_name` and `role_bindings.<role-id>.agent_branch`; derive `role_bindings.<role-id>.agent_workspace_ref` only when the target packet or profile schema still needs compatibility path material.
7. Report proposed packet/profile edits separately from filesystem work so the operator can approve mutation.

If the user's task does not map cleanly to these steps, use your native planning tool to produce a read-only plan first, then ask for explicit mutation only when edits are needed.

## Mapping Rules

An `agent-name` is a friendly topic-local Git and path namespace such as `alice`; it is not an Agent Instance id. Agent Instance ids remain globally unique runtime records created later by Workspace Runtime.

The planned Agent Workspace path must resolve under the selected Topic Workspace. Under `isomer-default.v1`, it is normally `<topic-workspace-dir>/agents/<agent-name>`, but a safe Topic Workspace Manifest may bind `agent.workspace` to another template. A compatibility `agent_workspace_ref` must derive from the resolved `agent.workspace` path and the same `agent_name` plan.

## Output

Report role ids, agent names, resolved `agent.workspace` paths, path sources, required `agent.*` support paths, derived compatibility `agent_workspace_ref` values, default branches, changed packet/profile files, blockers, and `next_operator_action`.
