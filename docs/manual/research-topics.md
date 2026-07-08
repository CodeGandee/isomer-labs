# Research Topics

A Research Topic is the unit of research work in an Isomer Project. It owns the topic intent, topic overview, workspace runtime, records, repositories, actor and agent workspaces, and GUI-readable artifacts.

Create a topic with the CLI:

```bash
isomer-cli project topics create my-topic \
  --statement "Investigate the concrete research question." \
  --set-default
```

Topic intent files such as `intent/src/topic-overview.md` are part of the topic contract. If they are missing, the Topic Workspace is incomplete and validation or GUI diagnostics should report that directly.

Use [Topic Workspaces](topic-workspaces.md) for the filesystem contract and [Research Records](research-records.md) for artifact indexing.
