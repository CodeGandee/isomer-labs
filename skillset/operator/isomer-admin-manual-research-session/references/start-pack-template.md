# Start Pack Template

## Workflow

When this reference is loaded, execute the following steps in order.

1. Build one start pack per selected Topic Actor after actor workspace readiness and research bootstrap readiness are known.
2. Create the authoritative start-pack record through `isomer-cli ext research records create`, using Topic Actor metadata fields and the `handoff.topic-actor-start-pack` profile.
3. Write a small actor-local copy or pointer under the actor's resolved `topic.actors.isomer_managed` or `topic.actors.links` surface. The local copy is startup convenience; the record ref is authoritative.
4. Include the actor cwd, runtime kind, role kind, selected v2 skills, placeholder binding files, semantic labels, blockers, next actions, authoritative record refs, and actor-local pointer path.
5. Tell the user to start each manually controlled coding agent from its own `topic.actors.workspace` cwd, not from `topic.repos.main`, unless the user intentionally has only one direct integration worker.

If the user's task does not map cleanly to these steps, create a partial start-pack blocker record for the affected actor instead of silently skipping it.

## Authoritative Record Command Shape

```bash
isomer-cli --print-json ext research records create \
  --topic <topic> \
  --record-kind artifact \
  --semantic-label topic.records.artifacts \
  --placeholder '<TOPIC_ACTOR_START_PACK>' \
  --profile handoff.topic-actor-start-pack \
  --skill isomer-admin-manual-research-session \
  --producer isomer-admin-manual-research-session \
  --consumer <topic-actor-name> \
  --topic-actor <topic-actor-name> \
  --actor-kind <actor-kind> \
  --runtime-kind <runtime-kind> \
  --controller-kind <controller-kind> \
  --body-file <start-pack.md> \
  --content-name start-pack.md \
  --metadata-json '{"topic_actor_name":"<topic-actor-name>","role_kind":"<role-kind>","cwd_label":"topic.actors.workspace"}'
```

## Start Pack Body

```markdown
# Topic Actor Start Pack: <topic-actor-name>

## Identity

- Research Topic: <research-topic-ref>
- Topic Workspace: <topic-workspace-ref>
- Topic Actor: <topic-actor-name>
- Actor kind: <actor-kind>
- Runtime kind: <runtime-kind>
- Role kind: <role-kind>
- Controller kind: <controller-kind>

## Cwd

- Start this worker in: <resolved-topic-actors-workspace-path>
- Cwd label: `topic.actors.workspace`
- Branch: <per-topic-actor/topic-actor-name/main>
- Integration surface: `topic.repos.main`

## Skills and Bindings

- V2 skills: <selected-skills>
- Placeholder binding files: <skill-local-placeholder-bindings>
- Topic-level binding index or readiness report: <record-ref-or-path>

## Recording Accepted Artifacts

- Use `isomer-cli ext research records` with `--topic-actor <topic-actor-name>`.
- Query existing records before scanning files.
- Treat local files as drafts until recorded or linked through Topic Workspace research records.

## Semantic Labels

- `topic.actors.workspace`: <status>
- `topic.actors.isomer_managed`: <status>
- `topic.actors.private_artifacts`: <status>
- `topic.actors.logs`: <status>
- `topic.actors.links`: <status>
- `topic.records.artifacts`: <status>
- `topic.records.views`: <status>

## Blockers

## Next Actions
```
