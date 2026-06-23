# Use Cases for Agent-Mediated Topic-Team Instantiation

These use cases define the behavior expected by `openspec/changes/add-operator-agent-topic-team-instantiation`. They are scoped to the change, not to the permanent project-wide use-case catalog.

- [UC-01: Project Operator Discovers Topic Service Support](uc-01-project-operator-discovers-topic-service-support.md) — an Isomer-skilled agent becomes project-aware, finds topics and service surfaces, and routes bounded support through a Topic Service Agent.
- [UC-02: Topic Service Agent Drafts an Instantiation Packet](uc-02-topic-service-agent-drafts-instantiation-packet.md) — a Houmao-backed Topic Service Agent inspects `deepsci-mini`, resolves topic placeholders, and returns a reviewable Topic Team Instantiation Packet.
- [UC-03: Approved Packet Materializes and Launches a Topic Team](uc-03-approved-packet-materializes-and-launches-topic-team.md) — the Project Operator Session approves packet-backed profile bundle materialization, creates runtime records, and launches or simulates the Agent Team Instance with provenance.

## Scope

The use cases assume the canonical domain terms in `.imsight-arts/project-explore/domain-concepts/dc-isomer-platform-language.md`, especially Project Operator Session, Topic Service Agent, Topic Service Master, Service Request, Topic Team Instantiation Packet, Topic Agent Team Profile, Agent Team Instance, and Execution Adapter.

## Evidence

- `openspec/changes/add-operator-agent-topic-team-instantiation/proposal.md`
- `openspec/changes/add-operator-agent-topic-team-instantiation/design.md`
- `openspec/changes/add-operator-agent-topic-team-instantiation/specs/operator-agent-topic-team-instantiation/spec.md`
- `openspec/changes/add-operator-agent-topic-team-instantiation/specs/houmao-cli-adapter-layer/spec.md`
- `openspec/changes/add-operator-agent-topic-team-instantiation/specs/workspace-runtime-persistence/spec.md`
