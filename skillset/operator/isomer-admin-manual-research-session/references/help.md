# Isomer Admin Manual Research Session Help

## Deprecation Warning

Direct user invocation of this skill is deprecated. Use `isomer-admin-topic-creator create` or `isomer-admin-topic-creator start-manual-research` for manual-research-ready topic setup. This skill remains available for compatibility and delegated start-pack finalization.

## What This Skill Does

This skill starts or repairs a human-orchestrated research session over a prepared Topic Workspace. It selects Topic Actors, delegates actor workspace readiness to the Topic Workspace Manager, runs v2 research workspace bootstrap, writes per-actor start packs, and reports the cwd and research-skill entrypoints each manually controlled worker should use.

## Required Inputs

- Prepared-topic evidence from `isomer-admin-topic-prepare`, or permission to run common topic preparation first.
- Requested Topic Actor names, runtime kinds, and roles when the user wants additional workers beyond `operator`.
- Selected v2 research skill set or the first intended research route.
- Operator permission before registering actors, materializing workspaces, running research bootstrap, or writing start packs.

## Subcommand Functionalities

| Subcommand | Functionality |
| --- | --- |
| `help` | Print what this skill does, required inputs, and subcommand functionalities. |
| `start-manual-session` | Run the full manual research session workflow from prepared-topic evidence through per-actor start packs. |
| `consume-prepared-topic` | Verify selected topic refs, Workspace Runtime, topic environment readiness, topic-main readiness, topic record labels, and default `operator` Topic Actor status. |
| `resolve-actor-roster` | Build the selected Topic Actor roster from requested workers and existing Topic Actor bindings. |
| `prepare-actor-workspaces` | Delegate Topic Actor registration, update, materialization, repair, archive, and diagnostics to `isomer-admin-topic-workspace-mgr`. |
| `bootstrap-research-workspace` | Invoke `isomer-rsch-workspace-mgr-v2` for base topic readiness, selected Topic Actor readiness, and optional formal team readiness when present. |
| `write-start-packs` | Create authoritative Topic Workspace research records and actor-local copies or pointers for each selected actor. |
