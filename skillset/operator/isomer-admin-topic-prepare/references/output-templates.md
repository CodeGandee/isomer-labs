# Output Templates

## Workflow

When this reference is loaded, use the templates below for topic preparation output. Keep blockers visible and cite semantic labels or record refs instead of raw paths when possible.

## Topic Operation Summary

```markdown
# Isomer Topic Operation Summary

## Research Topic

## Topic Workspace

## Common Preparation

## Topic Main Development Repository

## Topic Actor Roster

## Storage Bootstrap

## Optional Formal Team Material

## Blockers and Deferrals

## Next Actions
```

Fill `## Common Preparation` with Research Topic registration, Workspace Runtime readiness, topic environment readiness, and reused preparation refs. Fill `## Topic Actor Roster` with each Topic Actor name, actor kind, runtime kind, role kind, status, `topic.actors.workspace` readiness, branch, and blocker. Fill `## Optional Formal Team Material` only when a Topic Agent Team Profile, Agent Team Instance, or Agent Workspace material exists.

## Essential Chat Output

```text
status: <ready|ready-with-deferrals|blocked>
topic: <research-topic-ref>
topic_workspace: <topic-workspace-ref>
topic_main: <topic.repos.main readiness>
operator_actor: <ready|opted-out|blocked>
storage_bootstrap: <ready|pending|blocked>
blockers: <none or concise list>
next_action: <manual research session|topic team specialization|repair route>
```
