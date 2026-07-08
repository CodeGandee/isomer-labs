# Create a Research Topic

A Research Topic holds the intent, records, repositories, actor or agent workspaces, and generated views for one research effort. Create a topic with a concrete statement that an agent or operator can act on.

```bash
isomer-cli project topics create my-topic \
  --statement "Compare runtime prediction strategies for the target system." \
  --set-default
```

Check the topic workspace after creation:

```bash
isomer-cli --print-json project validate --topic my-topic
isomer-cli --print-json project paths list --topic my-topic
```

The default Topic Workspace layout follows the semantic path contract in [Topic Workspaces](../manual/topic-workspaces.md). Use path commands instead of memorizing directory names.
