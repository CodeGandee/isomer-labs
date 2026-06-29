## Context

`isomer-admin-topic-team-specialize` now has a recovery policy for subcommands with missing predecessors. The recovery policy is useful, but the dependency paths are spread across `SKILL.md`, `references/fast-forward.md`, and multiple subcommand pages. Those repeated paths are hard to audit and easy to update inconsistently.

The skill already uses local references and scripts as self-contained execution support. A local JSON dependency manifest plus a small Python query script fits that pattern: the skill remains portable, agents can inspect the graph without guessing, and repository validation can check one source of truth.

## Goals / Non-Goals

**Goals:**

- Store Topic Team Specialization step dependencies in one machine-readable file inside the skill bundle.
- Provide a script that answers dependency and recovery questions from that file.
- Teach the skill text to query the script for inclusive and exclusive targeted recovery paths.
- Keep subcommand pages readable by preserving local purpose, local prerequisites, and blockers without repeating full path chains.
- Update validation so the dependency graph is checked structurally.

**Non-Goals:**

- Do not add a runtime service, project-wide CLI, or external Python dependency.
- Do not make the script inspect the real workspace or prove that artifacts exist.
- Do not move Workspace Path Resolution, Project Manifest logic, or service setup behavior into the dependency script.
- Do not change live team operation boundaries.

## Decisions

1. Store the graph at `references/step-dependencies.json`.

   The manifest should live with the skill references because it is an execution reference, not application state. It should be committed with the skill and copied wherever the skill is installed.

2. Use a small read-only script at `scripts/query_step_dependencies.py`.

   The script should use only the Python standard library. It should resolve the manifest relative to its own path by default, accept an explicit manifest path for tests, and never mutate workspace files.

3. Make the manifest describe step semantics, not runtime facts.

   The manifest should record step ids, display names, kinds, required predecessor artifacts, produced artifacts, dependency edges, conditions, recoverability, mutation notes, and unrecoverable blockers. The agent still checks actual files, semantic labels, service outputs, user prompt context, and blockers.

4. Support direct queries needed by the skill.

   The script should support at least:

   ```bash
   python scripts/query_step_dependencies.py path --target setup-agent-workspace --include-target
   python scripts/query_step_dependencies.py path --target setup-agent-workspace --exclude-target
   python scripts/query_step_dependencies.py prereqs --target validate-topic-team
   python scripts/query_step_dependencies.py produces --target setup-topic-env
   python scripts/query_step_dependencies.py blockers --target resolve-agent-env-gate
   python scripts/query_step_dependencies.py explain --target setup-agent-workspace
   python scripts/query_step_dependencies.py validate
   ```

   Human-readable output is enough for agent use. A `--json` output option is useful for validation and future tooling.

5. Keep prose local and remove repeated full recovery chains.

   `SKILL.md` should tell agents to query the script when targeted recovery is needed. Subcommand pages should describe what the subcommand consumes, produces, and refuses to invent. They should not each repeat long paths such as `resolve-topic-intent -> ensure-topic-registration -> setup-topic-env -> adapt-team-template -> ...`.

6. Update repository validation around the new contract.

   `scripts/validate_skillsets.py` should check that the JSON and script exist, that the script validates the graph, that all procedural subcommands appear in the manifest, and that selected docs route dependency-path questions through the query script.

## Risks / Trade-offs

- [Risk] The JSON becomes too complex for agents to understand. -> Mitigation: keep fields descriptive and domain-level, with natural-language conditions rather than a heavy execution DSL.
- [Risk] The script output could be mistaken for real readiness. -> Mitigation: state in the skill and script help that the graph only describes expected dependencies; it does not verify artifact existence.
- [Risk] Validators may become brittle if they require exact prose. -> Mitigation: validate graph structure and script commands rather than exact dependency sentence wording.
- [Risk] Multiple active OpenSpec changes touch the same skill. -> Mitigation: implement this after the targeted recovery wording is in the working tree, but add a new requirement rather than re-modifying the same baseline requirement.
