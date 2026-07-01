# Agent Access Plan

## Workflow

1. Start from the Agent Names and Agent Workspace evidence reported in `isomer-topic-summary.md`.
2. Resolve Agent Workspace context for the working agents that will participate in the v2 research loop.
3. Confirm pre-promotion surfaces for each agent: `agent.private_artifacts`, `agent.scratch`, `agent.logs`, `agent.public_share`, and `agent.links`.
4. Explain which surfaces are private, disposable, peer-readable, advisory, or promotion candidates.
5. Prepare <RSCH_AGENT_ACCESS_PLAN> that tells agents where to place draft outputs before promotion and how to cite durable semantic refs after promotion.
6. Treat generated links as convenience paths only. Do not let a link target replace semantic labels or typed refs in durable reports.

If the user's task does not map cleanly to these steps, use your native planning tool to build an agent-by-agent access summary and mark missing context as a blocker.

## Access Rules

- `agent.private_artifacts` is for agent-owned outputs before promotion.
- `agent.scratch` is disposable and must not become durable evidence.
- `agent.logs` is for local diagnostics before logs are promoted or summarized.
- `agent.public_share` is peer-readable pre-promotion material, not accepted research truth by itself.
- `agent.links` is advisory convenience material and should point agents back to semantic labels or typed refs.

## Promotion Boundary

A working agent may draft or stage material inside its Agent Workspace, but later research skills should depend on durable semantic refs after promotion. If promotion support is missing, the manager should record the blocker and the pre-promotion location separately.
