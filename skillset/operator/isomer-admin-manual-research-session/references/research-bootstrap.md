# Research Bootstrap

## Workflow

When this reference is loaded, execute the following steps in order.

1. Run or validate `isomer-rsch-workspace-mgr-v2` over the prepared topology.
2. Require base topic readiness: registered Topic Workspace, valid Workspace Runtime, topic overview, topic environment readiness, ready `topic.repos.main`, materialized record labels, selected v2 skill `placeholder-bindings.md`, and a topic-level placeholder binding index or readiness report.
3. Require Topic Actor readiness for every selected actor: Topic Actor binding, `topic.actors.workspace`, `topic.actors.isomer_managed` or pointer location, runtime kind, role kind, actor recording metadata, and actor cwd instructions.
4. Add formal team readiness only when the selected topology includes a Topic Agent Team Profile or Agent Team Instance: final topic summary, profile material, formal Agent Workspace access, and worker-visible storage boundaries.
5. Treat missing actor or team layer checks as topology-specific blockers, not as proof that the whole topic is unusable.
6. Record the bootstrap output through the workspace manager's `placeholder-bindings.md` rows, preserving exact placeholder names and actor metadata.

If the user's task does not map cleanly to these steps, name which topology layer is blocked: base topic, Topic Actor, or formal team.

## Topology Layers

- Base topic layer: common preparation and durable storage surfaces.
- Topic Actor layer: human-orchestrated worker bindings and actor workspaces.
- Formal team layer: Topic Team Specialization, Topic Agent Team Profile material, Agent Workspace access, and Agent Team Instance context when selected.
