# Read-Only Context Queries

## Query Sequence

Run these queries from the user-selected Project context, keeping the exact Research Topic selector on every applicable query:

```bash
isomer-cli --print-json project self location
isomer-cli --print-json project self check --scope topic --topic <research-topic>
isomer-cli --print-json project context show --topic <research-topic>
isomer-cli --print-json project workspaces list
isomer-cli --print-json project paths get topic.runtime --topic <research-topic>
isomer-cli --print-json project paths get topic.repos.main --topic <research-topic>
isomer-cli --print-json project topic-actors list --topic <research-topic>
isomer-cli --print-json project team-instances list --topic <research-topic>
isomer-cli --print-json project runtime inspect --topic <research-topic>
```

Run only the task-dependent subset after the first four context queries. Use `project paths get topic.actors.workspace --topic <research-topic> --topic-actor <topic-actor>` for each registered Topic Actor and `project paths get agent.workspace --topic <research-topic> --agent <agent-name>` for each selected-team Agent Name. When a selected Agent Team Instance is present, inspect it with `project team-instances show <instance-id> --topic <research-topic>` before resolving its Agent Names.

## Acceptance Rules

Canonicalize returned paths. Require the Project root, Research Topic, and Topic Workspace binding to agree. Require every nested workspace to stay inside the selected Source Topic Workspace and every publication destination to stay inside the Project but outside protected roots. Treat missing later-stage components as unavailable. Do not infer Topic Actor or Agent bindings from directory names.

Stop when the query result is unresolved, conflicting, wrong-topic, missing information required by the selected operation, or inconsistent with the canonical boundaries. Do not scan siblings, switch to a manifest default after an explicit selection, or use an Isomer mutation command to repair context.

Workspace Runtime is required only for local mutations and runtime support-file promotion. Its absence never blocks publication after Research Topic and Topic Workspace registration.
