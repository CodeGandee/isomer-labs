---
skill_invocation_notation: >
  Top-level skill entrypoints use SKILL.md. Parent-scoped subskill entrypoints use
  SKILL-MAIN.md and are loaded explicitly through their parent; nested SKILL.md is
  accepted only as legacy input when SKILL-MAIN.md is absent.
  Skill and subskill entrypoints use bare object paths: `X` invokes skill X and
  `X->Y->Z` invokes subskill Z. Subcommands use parenthesized components:
  `X->cmd()` invokes a direct subcommand, `X->Y->cmd()` invokes a subcommand of
  subskill Y, and `X->parent()->child()` invokes child subcommand child exposed
  by parent subcommand parent. Intermediate subcommands act as object generators.
  Forms such as `X()` and `X->Y()` are invalid for skill or subskill entrypoints.
---

# Help

## Workflow

1. Print the public commands `switch`, `act-as`, `status`, `reset`, and `help`.
2. Explain that Topic Actor targets resolve to `topic.actors.workspace` and Agent targets resolve to `agent.workspace`.
3. Explain persistence modes: one-task by default, one-prompt restore for `act-as`, persistent session switch only when explicit, and `reset` to clear persistence.
4. Explain the complete session-local posture envelope: target kind, Research Topic, worker name, resolved workspace cwd, persistence mode, target-resolution source, and provenance wording. Persistent means current operator session only and never writes Project, local-context, Topic Workspace, Workspace Runtime, or cross-session state.
5. Explain cwd and selector discipline: run commands from the resolved target workspace cwd with explicit `--topic` plus `--topic-actor` or `--agent` selectors, and state why while retaining selectors before using any other semantic path.
6. Explain that `project self location` plus the matching `project self check --scope topic-actor|agent` validates the selected worker before mutation, while a manifest default or sole manifest actor never activates a switch.
7. Explain provenance: the Project Operator acts as or on behalf of the selected identity and must not claim OS-level impersonation, independent Topic Actor process execution, launched Agent Instance execution, Houmao launch, or Execution Adapter execution without verified runtime evidence.

If the user's task does not map cleanly to these steps, use your native planning tool to print the smallest useful command map and identify the missing target fields.

## Public Commands

| Command | Purpose | Produces |
| --- | --- | --- |
| `switch` | Switch to a Topic Actor or Agent identity posture for one task or the current session | Target, cwd, persistence mode, blockers, and provenance |
| `act-as` | Execute the following prompt once as a selected identity | One-prompt result, restore confirmation, cwd, blockers, and provenance |
| `status` | Inspect active switched posture | Active identity, cwd, persistence mode, uncertainty, and next action |
| `reset` | Clear persistent switched posture | Restore confirmation and previous identity summary |
| `help` | Show usage and guardrails | Command map and examples |

## Examples

- `Use isomer-op-entrypoint->identity switch to Topic Actor codex-exp-a for topic flash-attention and persist.`
- `Use isomer-op-entrypoint->identity act-as Agent deepsci-scout for topic flash-attention: inspect the failing benchmark and summarize blockers.`
- `Use isomer-op-entrypoint->identity status.`
- `Use isomer-op-entrypoint->identity reset.`
