# Use Case 2: Reproduce a Baseline and Optimize It

## User Story

As a researcher improving an existing method, I want Isomer Labs to reproduce the baseline, run controlled optimization experiments, and preserve evidence so that I can trust any reported improvement.

## Scenario

The user has a Measurable Objective: improve inference latency as much as possible while preserving baseline accuracy within an accepted tolerance. The Project already contains code, data-loading scripts, and previous notes. Isomer Labs creates a Research Thread with two Research Tasks: one for baseline reproduction and one for the first optimization pass.

## Step-by-Step Description

1. The user asks the Operator Agent to record the Measurable Objective, metric, tolerance, available hardware, and runtime constraints.
2. The Operator Agent uses `isomer-cli` to validate the Project Manifest and reject undeclared workspace paths.
3. The Operator Agent instantiates or reuses an Agent Team Instance with implementation, experimenter, analyst, and reviewer roles.
4. The Operator Agent asks the user to approve the Agent Team Instance, task handler, and a Gate requiring human approval before accepting or waiving the baseline.
5. The Operator Agent creates the Research Task `reproduce-baseline`.
6. The Project Manifest declares an Isomer Workspace for `reproduce-baseline`, its task handler, and the selected Agent Team Instance.
7. A Run starts; the Agent Team Instance's implementation, experimenter, analyst, and reviewer Agent Instances receive separate Agent Workspaces.
8. The implementation Agent Instance prepares the environment and records setup commands.
9. The experimenter Agent Instance runs the baseline and writes metrics, logs, and result tables as Artifacts.
10. The analyst compares observed metrics with expected metrics and creates Evidence Items.
11. The reviewer checks repeatability, missing controls, and unsupported Research Claims.
12. The Operator Agent presents a Gate asking the user to accept the reproduced baseline, request repair, or record a waiver.
13. After acceptance, the Operator Agent creates a second Research Task named `first-optimization-pass`.
14. A new Isomer Workspace is declared for the optimization Research Task.
15. The Agent Team Instance runs candidate optimizations, records tool calls and outputs, and updates Research Claims.
16. The GUI Backend and Renderer show a Run timeline, result table, and Gate for continue, branch, or stop.
17. The user selects the next action through the Operator Agent; Isomer records the choice as a Decision Record.

## Mermaid Use Case Diagram

```mermaid
flowchart LR
  User[Human User]
  CLI[isomer-cli]
  Operator["Operator<br/>Agent Instance"]
  GUI["GUI Backend<br/>and Renderer"]

  subgraph TeamInstance["Agent Team Instance"]
    Implementation["Implementation<br/>Agent Instance"]
    Experimenter["Experimenter<br/>Agent Instance"]
    Analyst["Analyst<br/>Agent Instance"]
    Reviewer["Reviewer<br/>Agent Instance"]
  end

  subgraph Isomer["Isomer Labs"]
    UC1([Record Measurable<br/>Objective])
    UC2([Validate Project<br/>Manifest])
    UC3([Instantiate Experiment<br/>Team Instance])
    UC4([Create Baseline<br/>Research Task])
    UC5([Prepare<br/>Environment])
    UC6([Run Baseline<br/>Measurements])
    UC7([Compare Metrics<br/>and Evidence])
    UC8([Resolve Baseline<br/>Gate])
    UC9([Create Optimization<br/>Research Task])
    UC10([Run Candidate<br/>Optimizations])
    UC11([Render Result Table<br/>and Run Timeline])
    UC12([Record Continue,<br/>Branch, or Stop])
  end

  User --> Operator
  CLI --> UC2
  Operator --> UC1
  Operator --> UC2
  Operator --> UC3
  Operator --> UC4
  Implementation --> UC5
  Experimenter --> UC6
  Analyst --> UC7
  Reviewer --> UC7
  Operator --> UC8
  Operator --> UC9
  Experimenter --> UC10
  GUI --> UC11
  Operator --> UC12

  UC1 --> UC3
  UC2 --> UC4
  UC4 --> UC5
  UC5 --> UC6
  UC6 --> UC7
  UC7 --> UC8
  UC8 --> UC9
  UC9 --> UC10
  UC10 --> UC11
  UC11 --> UC12
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
  participant GUI as GUI Backend<br/>and Renderer

  User->>Operator: Submit Measurable Objective<br/>and constraints
  Operator->>CLI: Validate Project before<br/>baseline work
  CLI->>PM: Check workspace declarations<br/>and schema versions
  CLI-->>Operator: Return validation<br/>result
  Operator->>Team: Instantiate or reuse<br/>Team Instance
  Operator->>PM: Declare baseline Task,<br/>handler, Workspace
  Operator->>Runtime: Initialize baseline<br/>Workspace Runtime
  Operator->>Adapter: Construct Team Agent<br/>Instances
  Adapter->>Agents: Start baseline Run<br/>in Agent Workspaces
  Agents->>Provenance: Store setup logs,<br/>metrics, Evidence Items
  Agents-->>GUI: Publish optional baseline<br/>AG-UI Render Payloads
  GUI-->>Runtime: Persist AG-UI<br/>Event Envelopes
  Provenance->>Runtime: Update Run status<br/>and Research Claims
  Runtime->>Views: Request result table<br/>and Gate view
  Views->>GUI: Emit baseline<br/>View Manifests
  GUI->>Operator: Surface accept, repair,<br/>or waiver Gate
  Operator->>User: Ask accept, repair,<br/>or waive baseline
  User->>Operator: Accept reproduced<br/>baseline
  Operator->>Runtime: Submit baseline<br/>Gate decision
  Runtime->>Provenance: Store baseline<br/>Decision Record
  Operator->>PM: Declare optimization Task,<br/>handler, Workspace
  Operator->>Runtime: Initialize optimization<br/>Workspace Runtime
  Operator->>Adapter: Construct or reuse<br/>Team Agent Instances
  Adapter->>Agents: Start optimization<br/>Run
  Agents->>Provenance: Store candidate changes,<br/>metrics, result Artifacts
  Agents-->>GUI: Publish optional optimization<br/>AG-UI Render Payloads
  GUI-->>Runtime: Persist AG-UI<br/>Event Envelopes
  Provenance->>Runtime: Update Evidence Items<br/>and improvement claims
  Runtime->>Views: Request Run timeline<br/>and decision view
  Views->>GUI: Emit optimization<br/>View Manifests
  GUI->>Operator: Surface continue,<br/>branch, or stop Gate
  Operator->>User: Ask continue, branch,<br/>or stop decision
  User->>Operator: Select next<br/>action
  Operator->>Runtime: Submit final<br/>Gate decision
```

## Durable Outputs

- Research Thread with a Measurable Objective
- Research Tasks for baseline reproduction and optimization
- Agent Team Instance instantiated from an Agent Team Template, with implementation, experimenter, analyst, and reviewer members
- Two Isomer Workspaces, each scoped to one Research Task, one task handler, and the selected Agent Team Instance
- Environment setup logs, baseline metrics, optimization metrics, result tables, and reviewer notes as Artifacts
- Evidence Items supporting or contradicting improvement claims
- Research Claims about baseline reproduction and optimization gains
- Gate result for baseline acceptance or waiver
- Decision Record for continue, branch, or stop
- View Manifests for Run timeline, result table, and experiment decision view
- AG-UI Render Payloads and AG-UI Event Envelopes when team agents publish live GUI updates
