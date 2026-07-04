## Context

Isomer already models Topic Actor Workspaces and Agent Workspaces as the worker-visible cwd surfaces inside a Topic Workspace. Project Operators can manually move into those directories, but no operator skill currently standardizes how to switch the operator's working identity posture, how long the switch should last, or how to keep provenance clear.

The canonical skill source is `src/isomer_labs/assets/system_skills/`, with `skillset/operator` symlinked to the packaged operator assets. The new skill should therefore be created in packaged assets and listed in the system-skill manifest. It should follow `$imsight-agent-skill-handling create` conventions: minimal skill folder, required `SKILL.md`, recommended `agents/openai.yaml`, no empty resource directories, concise numbered workflow, and command detail pages only when they reduce complexity.

## Goals / Non-Goals

**Goals:**

- Add `isomer-op-switch-identity` as an active operator skill.
- Let the Project Operator switch to a selected Topic Actor or Agent identity posture.
- Make the selected identity's resolved workspace the default cwd for commands.
- Support one-task and persistent session switches.
- Require persistent switches to be remembered by the Project Operator in the current conversation/session until reset or replaced.
- Preserve clear provenance that the Project Operator is operating in a switched posture.
- Validate the new skill through existing skillset validation.

**Non-Goals:**

- Do not add OS-level user impersonation.
- Do not launch or simulate a Houmao agent.
- Do not create or modify Agent Instance records.
- Do not add a durable identity-switch registry, database table, or CLI command.
- Do not grant permission to overwrite another worker's uncommitted work without explicit user instruction.

## Decisions

### Session-posture skill, not runtime identity

`isomer-op-switch-identity` will define an instruction-level Project Operator posture. A persistent switch means the operator must remember the active switched identity within the current session and use that identity's workspace as cwd by default until the user resets or switches again.

Alternative considered: store persistent switches in Workspace Runtime. That would make a conversation-level operator instruction look like durable runtime state and create cleanup semantics the user did not ask for.

### Collection-of-routines subcommand shape

The skill should use the Imsight collection-of-routines flavor with peer commands:

- `switch`: resolve a target identity, choose persistence, and establish the active cwd posture.
- `act-as`: execute the following user prompt once under a target identity, then restore the previous Project Operator identity posture.
- `status`: report the active switched identity and cwd posture when known.
- `reset`: return to normal Project Operator identity.
- `help`: explain usage and examples.

These commands are independent enough that the complex-procedure three-group split is unnecessary. Following Imsight local conventions, command detail pages should live under `commands/`.

### Target resolution through existing Isomer surfaces

The skill should resolve target workspaces with existing CLI/API surfaces:

- Topic Actor target: `isomer-cli --print-json project paths get topic.actors.workspace --topic <topic> --topic-actor <topic-actor-name>`
- Agent target: `isomer-cli --print-json project paths get agent.workspace --topic <topic> --agent <agent-name>`

Readiness checks should route through existing owner skills or commands:

- Topic Actor readiness: `isomer-op-topic-mgr actors-diagnose` or `project topic-actors diagnose`.
- Agent workspace readiness: `isomer-op-topic-mgr team-validate-workspaces` or available Agent Workspace setup evidence.

### Cwd is the primary effect

The most important behavior is command cwd. When switched, shell commands and file operations should default to the resolved target workspace, not the project root or `topic.repos.main`. The skill may still resolve and reference other paths, but it must explicitly explain why any command runs outside the switched cwd.

### Provenance is explicit, not disguised

Outputs should say the Project Operator acted under the selected identity posture. For formal Agents, the skill must not claim a launched Agent Instance produced the work unless verified runtime context exists. For Topic Actors, it must not pretend an independent Topic Actor process ran.

## Risks / Trade-offs

- [Risk] Agents may overstate the identity switch as real Agent Instance execution. → Mitigation: require explicit provenance wording and forbid fabricated Agent Instance or Topic Actor process claims.
- [Risk] Persistent switch state can be forgotten across context compaction or new sessions. → Mitigation: define persistence as current operator session memory only and require `status` or re-resolution when uncertain.
- [Risk] The operator may run commands from the project root out of habit. → Mitigation: make switched cwd the dominant rule in `SKILL.md`, command pages, tests, and validation required terms.
- [Risk] Command detail pages under `commands/` differ from older operator `references/` conventions. → Mitigation: this skill intentionally follows the user-requested Imsight create convention; update validator expectations for this skill only.

## Migration Plan

1. Add the new skill folder under `src/isomer_labs/assets/system_skills/operator/isomer-op-switch-identity/`.
2. Add `SKILL.md`, `agents/openai.yaml`, and command pages under `commands/`.
3. Add the skill to `src/isomer_labs/assets/system_skills/manifest.toml` in the `core` group.
4. Update operator README or skill-map surfaces that list active operator skills.
5. Update `scripts/validate_skillsets.py` and tests so the new operator skill is required and validated.
6. Run skill validation, lint, typecheck, and unit tests.
