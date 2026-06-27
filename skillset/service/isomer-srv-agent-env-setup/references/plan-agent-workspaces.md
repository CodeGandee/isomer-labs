# Plan Agent Workspaces

Use this subcommand to read authoritative Agent Names from topic-team material and resolve each planned Agent Workspace through semantic labels.

## Required Inputs

Recover these before asking the user:

| Input | Resolution |
| --- | --- |
| Agent env context | Require selected Project, Research Topic, Topic Workspace, `topic.repos.main`, `topic.agents_root`, and path source evidence from `resolve-agent-env-context`. |
| Topic-team material | Read the Topic Team Instantiation Packet or Topic Agent Team Profile material derived from that packet. These are the authority for Agent Names. |
| Source agent gate summary | Use `read-agent-env-gate` output when agent plan constraints exist. |
| Explicit operator map | Optional. Treat only as corroborating evidence when it matches authoritative topic-team material. |
| Optional selected agent | Optional for direct repair subcommands. It must be one authoritative Agent Name. |

## Workflow

When this subcommand is selected, execute the following steps in order.

1. **Require selected Topic Workspace context** and semantic path evidence from `resolve-agent-env-context`.
2. **Read authoritative topic-team material** from the Topic Team Instantiation Packet or Topic Agent Team Profile material derived from that packet.
3. **Extract active role bindings only**. Read active role ids, Agent Names, optional branch plans, and compatibility `agent_workspace_ref` evidence.
4. **Reject missing Agent Names**. If no authoritative Agent Names exist for planned roles, report a blocker and route the operator back to Topic Team Specialization to repair or complete packet/profile material.
5. **Handle explicit operator maps as corroboration only**. If a provided map matches the authoritative material, record it as corroborating operator-provided evidence. If it disagrees, report `agent-plan-conflict` and do not create branches, worktrees, support paths, or gate entries from that map.
6. **Validate Agent Names**. Reject empty names, `.` or `..`, path separators, unsafe shell metacharacters, whitespace-only values, names that normalize outside a safe lowercase segment, and normalized collisions.
7. **Resolve agent labels** for each authoritative Agent Name through Workspace Path Resolution: `agent.workspace`, `agent.isomer_managed`, `agent.runtime`, `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, `agent.inbox`, `agent.topic_readonly`, `agent.topic_writable`, and `agent.links`. Include `agent.tmp` when available as local ignored disposable posture.
8. **Plan branch names** using `per-agent/<agent-name>/main` by default and keep future branches under `per-agent/<agent-name>/`.
9. **Report the agent plan** with semantic labels, resolved paths, path sources, branch plan, selected-agent partial scope when present, corroborating evidence, blockers, and next action.

If the user's task does not map cleanly to these steps, use your native planning tool to produce a read-only plan from available topic-team material, semantic path evidence, and parent guardrails, then execute the safe portion.

## Mapping Rules

An Agent Name is a topic-local Git and path namespace such as `analyst` or `experimenter-gpu`; it is not an Agent Instance id, role id, provider id, or directory name discovered by scanning.

The planned Agent Workspace path must resolve under the selected Topic Workspace unless a later accepted external-root policy explicitly permits the label. Under `isomer-default.v1`, `agent.workspace` normally binds to `<topic-workspace-dir>/agents/<agent-name>`, but a safe Topic Workspace Manifest may bind it differently.

## Guardrails

- Do not infer Agent Names from existing directories, branches, provider ids, or ad hoc maps.
- Do not create files or Git refs from this subcommand.
- Do not edit packet/profile material here; report the needed Topic Team Specialization repair route.
- Selected-agent direct subcommands may target only one authoritative Agent Name and produce partial evidence.
