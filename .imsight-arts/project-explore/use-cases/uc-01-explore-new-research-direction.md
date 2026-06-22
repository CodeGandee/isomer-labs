# Use Case 1: Explore a New Research Direction

## User Story

As a GPU systems researcher entering the Flash Attention 4 on DGX Spark GB10 topic, I want Isomer Labs to organize literature scouting, evidence synthesis, and direction selection so that I can choose a defensible follow-up Research Inquiry before investing in experiments.

## Scenario

The user has the Research Topic `flash-attention-gb10-peak-performance-optimization`: understand which DGX Spark GB10 and Blackwell execution-system features may make Flash Attention 4 faster, and identify promising intervention directions before running expensive kernel experiments. The user supplies seed papers, Flash Attention 4 or related attention-kernel code, GB10 access constraints, candidate shape families, correctness tolerances, and a rough question. Isomer Labs creates an initial Research Inquiry named `gb10-flash-attention-4-direction-selection` under that topic and decomposes the work into one Research Task for literature, feature, and factor mapping.

## Step-by-Step Description

1. The user asks the Operator Agent to open a Project, record Research Topic `flash-attention-gb10-peak-performance-optimization`, and create initial Research Inquiry `gb10-flash-attention-4-direction-selection`.
2. The Operator Agent uses `isomer-cli` to validate the Project Manifest and available Isomer built-in artifacts.
3. The Operator Agent selects the `deepsci-mini` Domain Agent Team Template and specializes a Topic Agent Team Profile with `deepsci-mini-lead`, `deepsci-mini-scout`, and `deepsci-mini-synth-reviewer` roles.
4. The Operator Agent asks the user to approve or edit the Topic Agent Team Profile, Workflow Stages, task handler, and constraints.
5. The Operator Agent creates a Research Task named `map-gb10-flash-attention-optimization-directions`.
6. The Project Manifest declares one Topic Workspace for the Research Topic and records the Research Task, task handler, and selected Topic Agent Team Profile in Workspace Runtime.
7. A Run starts; the Execution Adapter launches a `deepsci-mini` Agent Team Instance from the Topic Agent Team Profile and constructs the lead, scout, and synthesis-reviewer Agent Instances and their Agent Workspaces.
8. The `deepsci-mini-scout` Agent Instance collects seed sources, Flash Attention implementation notes, GB10 or Blackwell feature references, benchmark notes, shape-family constraints, and correctness constraints as Artifacts.
9. The `deepsci-mini-synth-reviewer` extracts Research Claims, Evidence Items, limitations, and disagreement points about attention-kernel bottlenecks, Tensor Core precision modes, memory hierarchy, asynchronous copy, warp specialization, cluster cooperation, and tiling choices.
10. The `deepsci-mini-synth-reviewer` clusters Evidence Items into candidate optimization factors and follow-up Research Inquiry options, such as baseline measurement design, precision-mode investigation, tile or pipeline search, and cluster-level cooperation experiments.
11. The `deepsci-mini-synth-reviewer` checks whether proposed inquiries are supported by Evidence Items, whether claims stay within recorded GB10 evidence, and whether weak or generic CUDA tuning claims are flagged.
12. The engine emits View Manifests for a literature matrix, claim graph, and inquiry-comparison view, all rendered with Built-in GUI Components.
13. The `deepsci-mini-lead` presents a Gate asking the user to choose a follow-up Research Inquiry for the GB10 Flash Attention 4 topic or request more scouting.
14. The Operator Agent stores the selected inquiry and rationale as a Decision Record with Evidence Item links.

## Mermaid Use Case Diagram

```mermaid
flowchart LR
  User[Human User]
  CLI[isomer-cli]
  Operator["Operator<br/>Agent Instance"]
  GUI["GUI Backend<br/>and Renderer"]

  subgraph TeamInstance["deepsci-mini Agent Team Instance"]
    Lead["deepsci-mini-lead"]
    Scout["deepsci-mini-scout"]
    Reviewer["deepsci-mini-synth-reviewer"]
  end

  subgraph Isomer["Isomer Labs"]
    UC1([Record Research<br/>Topic])
    UC2([Validate Project<br/>Manifest])
    UC3([Specialize Topic<br/>Agent Team Profile])
    UC4([Create Topic Workspace<br/>and Research Task])
    UC5([Collect Source<br/>Artifacts])
    UC6([Extract Claims<br/>and Evidence Items])
    UC7([Compare Research<br/>Inquiry Options])
    UC8([Render Claim Graph<br/>and Inquiry View])
    UC9([Resolve Inquiry<br/>Selection Gate])
    UC10([Record Decision<br/>Record])
  end

  User --> Operator
  CLI --> UC2
  Operator --> UC1
  Operator --> UC2
  Operator --> UC3
  Operator --> UC4
  Lead --> UC9
  Scout --> UC5
  Reviewer --> UC7
  Reviewer --> UC6
  GUI --> UC8
  Operator --> UC10

  UC1 --> UC3
  UC2 --> UC4
  UC4 --> UC5
  UC5 --> UC6
  UC6 --> UC7
  UC7 --> UC8
  UC8 --> UC9
  UC9 --> UC10
```

## Mermaid System Sequence Diagram

```mermaid
sequenceDiagram
  autonumber
  actor User as Human User
  participant CLI as isomer-cli
  participant PM as Project<br/>Manifest
  participant Operator as Operator<br/>Agent Instance
  participant Profile as Topic Agent Team<br/>Profile
  participant Team as Agent Team<br/>Instance
  participant Runtime as Workspace<br/>Runtime
  participant Adapter as Execution<br/>Adapter
  participant Agents as Team Agent<br/>Instances
  participant Provenance as Artifact and<br/>Provenance Service
  participant Views as View Manifest<br/>Generator
  participant GUI as GUI Backend<br/>and Renderer

  User->>Operator: Submit GB10 Flash Attention 4<br/>Research Topic and Project context
  Operator->>CLI: Validate Project<br/>before setup
  CLI->>PM: Validate manifest and<br/>built-in artifact versions
  CLI-->>Operator: Report valid<br/>Project configuration
  Operator->>User: Confirm Project<br/>and setup intent
  Operator->>PM: Select deepsci-mini<br/>Domain Agent Team Template
  Operator->>Profile: Specialize lead,<br/>scout, synth-reviewer roles
  Operator->>PM: Declare Topic Workspace<br/>for Research Topic
  Operator->>Runtime: Record Research Task,<br/>handler, and Topic Agent<br/>Team Profile state
  Operator->>Adapter: Construct Team Agent<br/>Instances
  Adapter->>Team: Launch deepsci-mini<br/>Agent Team Instance from profile
  Adapter->>Agents: Create lead, scout,<br/>and synth-reviewer workspaces<br/>and start Run
  Agents->>Provenance: Store notes, claims,<br/>Evidence Items, Artifacts
  Provenance->>Runtime: Record refs, handoffs,<br/>Research Claims, Run status
  Runtime->>Views: Request literature matrix,<br/>claim graph, inquiry view
  Views->>GUI: Emit View Manifests<br/>for built-in components
  GUI->>Operator: Surface inquiry options<br/>and pending Gate
  Operator->>User: Ask inquiry selection<br/>or more scouting
  User->>Operator: Select follow-up<br/>Research Inquiry
  Operator->>Runtime: Submit Gate<br/>decision
  Runtime->>Provenance: Store Decision Record<br/>with Evidence links
```

## Durable Outputs

- Research Topic `flash-attention-gb10-peak-performance-optimization` with initial Research Inquiry `gb10-flash-attention-4-direction-selection`
- Research Task `map-gb10-flash-attention-optimization-directions` for literature, feature, and factor mapping
- Topic Agent Team Profile specialized from the `deepsci-mini` Domain Agent Team Template, with `deepsci-mini-lead`, `deepsci-mini-scout`, and `deepsci-mini-synth-reviewer` roles
- `deepsci-mini` Agent Team Instance launched from the Topic Agent Team Profile
- Topic Workspace declared in the Project Manifest
- Agent Workspaces for the lead, scout, and synthesis-reviewer Agent Instances
- Literature notes, source summaries, GB10 or Blackwell feature notes, attention-kernel bottleneck notes, claim graph, inquiry comparison, and review notes as Artifacts
- Evidence Items linked to Research Claims
- Decision Record for selected follow-up Research Inquiry
- View Manifests for literature matrix, claim graph, and inquiry decision
- Built-in GUI Component Instances for literature matrix, claim graph, inquiry comparison, and pending Gate views

## Pass Criteria

UC-01 passes only when the Topic Workspace records the pinned Research Topic, initial Research Inquiry, Research Task, Evidence Items, inquiry-comparison Artifacts, pending Gate, and selected follow-up Decision Record without requiring a GB10 measurement run. The selected follow-up inquiry must be traceable to Evidence Items and must identify whether UC-07-style measured optimization, more scouting, or a different Flash Attention 4 investigation should happen next.
