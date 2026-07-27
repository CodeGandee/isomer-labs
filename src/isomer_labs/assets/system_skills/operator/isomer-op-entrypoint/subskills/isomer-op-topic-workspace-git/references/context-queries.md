# Read-Only Context Queries

## Query Sequence

Run these queries from the user-selected Project context, keeping the exact Research Topic selector on every applicable query:

```bash
isomer-cli --print-json project self location
isomer-cli --print-json project self check --scope topic --topic <research-topic>
isomer-cli --print-json project context show --topic <research-topic>
isomer-cli --print-json project workspaces list
isomer-cli --print-json project paths list --topic <research-topic>
isomer-cli --print-json project paths get topic.runtime --topic <research-topic>
isomer-cli --print-json project paths get topic.repos.main --topic <research-topic>
isomer-cli --print-json project topic-actors list --topic <research-topic>
isomer-cli --print-json project team-instances list --topic <research-topic>
isomer-cli --print-json project runtime inspect --topic <research-topic>
```

After the first four queries, run only the task-dependent subset:

| Need | Query |
| --- | --- |
| Registered Topic Actor Workspace | `project paths get topic.actors.workspace --topic <research-topic> --topic-actor <topic-actor>` |
| Selected-team Agent Workspace | `project paths get agent.workspace --topic <research-topic> --agent <agent-name>` |
| Selected Agent Team Instance membership | `project team-instances show <instance-id> --topic <research-topic>` before resolving Agent Names |
| Latest paper candidate | `project artifacts latest --topic <research-topic> --semantic-id KAOJU:PAPER-PDF` and linked build and validation records |
| Durable decision lineage | `project artifacts list --topic <research-topic>` followed by exact semantic-id and record-ref queries; never infer latest state from filenames |
| Canonical external repository | Resolve each registered non-main `topic.repos.*` label returned by `project paths list`, then inspect its credential-free GitHub locator and exact commit directly at that validated path |

## Acceptance Rules

| Check | Acceptance Rule |
| --- | --- |
| Identity | Project root, Research Topic, and Topic Workspace binding agree |
| Paths | Returned paths are canonical |
| Nested workspaces | Every path remains inside the selected Source Topic Workspace |
| Publication destination | Path remains inside the Project and outside protected roots |
| Missing later-stage components | Report as unavailable |
| Reference repository identity | Preserve normalized public or private GitHub organization/repository identity; keep authentication external |
| Latest paper | Require one unambiguous checksummed candidate with accepted build and validation lineage |
| Workspace Runtime | Required only for local mutation and runtime support-file promotion |

Missing Workspace Runtime never blocks publication after Research Topic and Topic Workspace registration.

Stop on unresolved, conflicting, wrong-topic, incomplete, or boundary-inconsistent results.

Do not:

- scan sibling Topic Workspaces;
- infer Topic Actor or Agent bindings from directory names;
- replace an explicit selection with a manifest default;
- use an Isomer mutation command to repair context.
