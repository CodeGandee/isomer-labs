# Use Case 1: Explore a New Research Direction

## User Story

As a researcher entering an unfamiliar topic, I want Isomer Labs to organize literature scouting, evidence synthesis, and direction selection so that I can choose a defensible Research Branch before investing in experiments.

## Scenario

The user has an Exploratory Goal: understand why a model family fails on a target data regime and identify promising intervention directions. The user supplies seed papers, a code repository, data constraints, and a rough question. Isomer Labs creates a Research Thread and decomposes the work into one Research Task for literature and factor mapping.

## Step-by-Step Description

1. The user asks the Operator Agent to open a Project and record an Exploratory Goal in a new Research Thread.
2. The Operator Agent uses `isomer-cli` to validate the Project Manifest and available Isomer built-in artifacts.
3. The Operator Agent selects an Agent Team Template and instantiates an Agent Team Instance with scout, literature reviewer, analyst, and reviewer roles.
4. The Operator Agent asks the user to approve or edit the Agent Team Instance, Workflow Stages, task handler, and constraints.
5. The Operator Agent creates a Research Task named `map-failure-factors-and-directions`.
6. The Project Manifest declares one Isomer Workspace for that Research Task, the task handler, and the selected Agent Team Instance.
7. A Run starts; the Execution Adapter constructs the Agent Team Instance's scout, literature reviewer, analyst, and reviewer Agent Instances and their Agent Workspaces.
8. The scout Agent Instance collects seed sources, related papers, datasets, and benchmark notes as Artifacts.
9. The literature reviewer extracts Research Claims, Evidence Items, limitations, and disagreement points.
10. The analyst clusters Evidence Items into candidate causal factors and Research Branch options.
11. The reviewer checks whether proposed branches are supported by Evidence Items and flags weak claims.
12. The engine emits View Manifests for a literature matrix, claim graph, and branch-comparison view.
13. The Operator Agent presents a Gate asking the user to choose a Research Branch or request more scouting.
14. The Operator Agent stores the selected branch and rationale as a Decision Record with Evidence Item links.

## Mermaid Use Case Diagram

```mermaid
flowchart LR
  User[Human User]
  CLI[isomer-cli]
  Operator["Operator<br/>Agent Instance"]
  GUI["GUI<br/>Renderer"]

  subgraph TeamInstance["Agent Team Instance"]
    Scout["Scout<br/>Agent Instance"]
    Literature["Literature Reviewer<br/>Agent Instance"]
    Analyst["Analyst<br/>Agent Instance"]
    Reviewer["Reviewer<br/>Agent Instance"]
  end

  subgraph Isomer["Isomer Labs"]
    UC1([Record Exploratory<br/>Goal])
    UC2([Validate Project<br/>Manifest])
    UC3([Instantiate Agent<br/>Team Instance])
    UC4([Create Research Task<br/>and Isomer Workspace])
    UC5([Collect Source<br/>Artifacts])
    UC6([Extract Claims<br/>and Evidence Items])
    UC7([Compare Research<br/>Branch Options])
    UC8([Render Claim Graph<br/>and Branch View])
    UC9([Resolve Branch<br/>Selection Gate])
    UC10([Record Decision<br/>Record])
  end

  User --> Operator
  CLI --> UC2
  Operator --> UC1
  Operator --> UC2
  Operator --> UC3
  Operator --> UC4
  Scout --> UC5
  Literature --> UC6
  Analyst --> UC7
  Reviewer --> UC7
  GUI --> UC8
  Operator --> UC9
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
  participant Team as Agent Team<br/>Instance
  participant Runtime as Workspace<br/>Runtime
  participant Adapter as Execution<br/>Adapter
  participant Agents as Team Agent<br/>Instances
  participant Provenance as Artifact and<br/>Provenance Service
  participant Views as View Manifest<br/>Generator
  participant GUI as GUI<br/>Renderer

  User->>Operator: Submit Exploratory Goal<br/>and Project context
  Operator->>CLI: Validate Project<br/>before setup
  CLI->>PM: Validate manifest and<br/>built-in artifact versions
  CLI-->>Operator: Report valid<br/>Project configuration
  Operator->>User: Confirm Project<br/>and setup intent
  Operator->>PM: Select Team Template<br/>and project params
  Operator->>Team: Instantiate scout,<br/>reviewer, analyst roles
  Operator->>PM: Declare Research Task,<br/>handler, Isomer Workspace
  Operator->>Runtime: Initialize Research Task<br/>and Team Instance state
  Operator->>Adapter: Construct Team Agent<br/>Instances
  Adapter->>Agents: Create Agent Workspaces<br/>and start Run
  Agents->>Provenance: Store notes, claims,<br/>Evidence Items, Artifacts
  Provenance->>Runtime: Record refs, handoffs,<br/>Research Claims, Run status
  Runtime->>Views: Request literature matrix,<br/>claim graph, branch view
  Views->>GUI: Emit View<br/>Manifests
  GUI->>Operator: Surface branch options<br/>and pending Gate
  Operator->>User: Ask branch selection<br/>or more scouting
  User->>Operator: Select Research<br/>Branch
  Operator->>Runtime: Submit Gate<br/>decision
  Runtime->>Provenance: Store Decision Record<br/>with Evidence links
```

## Durable Outputs

- Research Thread with an Exploratory Goal
- Research Task for literature and factor mapping
- Agent Team Instance instantiated from an Agent Team Template, with scout, literature reviewer, analyst, and reviewer members
- Isomer Workspace declared in the Project Manifest
- Agent Workspaces for the Agent Team Instance's scout, literature reviewer, analyst, and reviewer Agent Instances
- Literature notes, source summaries, claim graph, branch comparison, and review notes as Artifacts
- Evidence Items linked to Research Claims
- Decision Record for selected Research Branch
- View Manifests for literature matrix, claim graph, and branch decision
