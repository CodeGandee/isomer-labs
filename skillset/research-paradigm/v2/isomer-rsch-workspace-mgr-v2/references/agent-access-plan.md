# Agent Access Plan

## Workflow

1. Start from the selected Topic Actors and optional formal Agent Names reported in common preparation output, Topic Actor start packs, or `isomer-topic-summary.md`.
2. Resolve Topic Actor Workspace context for human-orchestrated workers and Agent Workspace context for formal team agents that will participate in the v2 research loop.
3. Confirm pre-promotion surfaces for each Topic Actor: `topic.actors.workspace`, `topic.actors.private_artifacts`, `topic.actors.logs`, `topic.actors.links`, and `topic.actors.tmp`.
4. Confirm pre-promotion surfaces for each formal agent when selected: `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.links`.
5. Explain which surfaces are private, disposable, peer-readable, advisory, or promotion candidates.
6. Prepare <RSCH_AGENT_ACCESS_PLAN> that tells Topic Actors and formal agents where to place draft outputs before promotion and how to cite durable semantic refs after promotion.
7. Treat generated links as convenience paths only. Do not let a link target replace semantic labels or typed refs in durable reports.

If the user's task does not map cleanly to these steps, use your native planning tool to build an agent-by-agent access summary and mark missing context as a blocker.

## Access Rules

- `topic.actors.private_artifacts` is for Topic Actor-owned outputs before promotion.
- `topic.actors.logs` is for Topic Actor-local diagnostics before logs are promoted or summarized.
- `topic.actors.links` is advisory convenience material and should point actors back to semantic labels or typed refs.
- `topic.actors.tmp` is local, ignored, disposable, and not durable evidence.
- `agent.private_artifacts` is for formal agent-owned outputs before promotion.
- `agent.scratch` is disposable and must not become durable evidence.
- `agent.logs` is for local diagnostics before logs are promoted or summarized.
- `agent.public_share` is peer-readable pre-promotion material, not accepted research truth by itself.
- `agent.links` is advisory convenience material and should point agents back to semantic labels or typed refs.

## Promotion Boundary

A Topic Actor may draft or stage material inside its Topic Actor Workspace, and a formal agent may draft or stage material inside its Agent Workspace, but later research skills should depend on durable semantic refs after promotion. If promotion support is missing, the manager should record the blocker and the pre-promotion location separately.
