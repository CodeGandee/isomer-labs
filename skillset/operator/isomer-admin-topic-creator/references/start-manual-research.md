# Start Manual Research

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Require selected Topic Actors, ready Topic Actor Workspaces, derived actor env gate verification evidence, and research bootstrap status.
2. Delegate compatibility start-pack finalization to `isomer-admin-manual-research-session` when the existing start-pack workflow is needed.
3. Create or validate one authoritative Topic Workspace research record per selected actor using the `handoff.topic-actor-start-pack` profile and Topic Actor metadata.
4. Write or validate a small actor-local copy or pointer under the actor's resolved `topic.actors.isomer_managed` or `topic.actors.links` surface.
5. Report each actor cwd, branch, runtime kind, role kind, selected v2 skills, placeholder binding files, start-pack record refs, actor-local pointer paths, blockers, and next action.

If the user's task does not map cleanly to these steps, create a partial handoff report that names the actors that are ready, blocked, or missing bootstrap evidence.

## Guardrails

The authoritative start pack is the Topic Workspace research record. Actor-local material is startup convenience and must point back to the record ref.
