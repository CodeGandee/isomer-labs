# Use Case 3: Plan and Execute a Paper Revision

## User Story

As a researcher revising a paper, I want Isomer Labs to map reviewer feedback to claims, evidence gaps, and revision tasks so that I can produce a focused response package without losing provenance.

## Scenario

The user imports a draft manuscript, reviewer comments, figure files, experiment logs, and prior notes. The Research Goal is to decide how to revise the paper and produce a supported response plan. Isomer Labs creates a Research Thread with Research Tasks for feedback mapping and targeted revision work.

## Step-by-Step Description

1. The user asks the Operator Agent to create a Research Thread and supplies the manuscript, reviews, constraints, and deadline.
2. The Operator Agent instantiates or reuses an Agent Team Instance with critique mapper, evidence auditor, experiment planner, writer, and reviewer roles.
3. The Operator Agent asks the user to edit the Agent Team Instance, task handler, and gated decisions for claim strengthening, new experiments, and final response text.
4. The Operator Agent creates the Research Task `map-review-feedback`.
5. The Project Manifest declares an Isomer Workspace for that Research Task, its task handler, and the selected Agent Team Instance.
6. A Run starts; the Agent Team Instance's critique mapper, evidence auditor, experiment planner, writer, and reviewer Agent Instances receive Agent Workspaces with advisory Workspace Boundaries.
7. The critique mapper turns reviewer comments into issue Artifacts and links them to manuscript sections.
8. The evidence auditor maps each issue to Research Claims, Evidence Items, missing support, and contradiction risks.
9. The experiment planner proposes targeted Research Tasks for missing analyses or robustness checks.
10. The GUI Backend and Renderer show a reviewer-response matrix, claim-risk view, and pending Gate list using Built-in GUI Components.
11. The Operator Agent presents a Gate asking the user to approve the revision strategy and choose which targeted analyses to run.
12. The Operator Agent records the approved plan as a Decision Record.
13. For each approved analysis, Isomer creates a new Research Task with its own Isomer Workspace.
14. The Agent Team Instance executes Runs, records result Artifacts, and updates Evidence Items.
15. The writer drafts response text and manuscript edits only for claims with enough support.
16. The reviewer audits claim strength, unsupported wording, and missing provenance.
17. The Operator Agent presents a final Gate asking the user to approve the response package or send selected items back for revision.

## Mermaid Use Case Diagram

```mermaid
flowchart LR
  User[Human User]
  Operator["Operator<br/>Agent Instance"]
  GUI["GUI Backend<br/>and Renderer"]

  subgraph TeamInstance["Agent Team Instance"]
    Mapper["Critique Mapper<br/>Agent Instance"]
    Auditor["Evidence Auditor<br/>Agent Instance"]
    Planner["Experiment Planner<br/>Agent Instance"]
    Writer["Writer<br/>Agent Instance"]
    Reviewer["Reviewer<br/>Agent Instance"]
  end

  subgraph Isomer["Isomer Labs"]
    UC1([Import Manuscript<br/>and Reviews])
    UC2([Instantiate Revision<br/>Team Instance])
    UC3([Mark Gated<br/>Decisions])
    UC4([Create Feedback<br/>Research Task])
    UC5([Map Reviewer Comments<br/>to Issues])
    UC6([Map Claims and<br/>Evidence Gaps])
    UC7([Propose Targeted<br/>Analyses])
    UC8([Render Response Matrix<br/>and Claim-Risk View])
    UC9([Resolve Revision<br/>Strategy Gate])
    UC10([Execute Approved<br/>Research Tasks])
    UC11([Draft Response<br/>Package])
    UC12([Audit Claims<br/>and Provenance])
    UC13([Approve Final<br/>Package Gate])
  end

  User --> Operator
  Operator --> UC1
  Operator --> UC2
  Operator --> UC3
  Operator --> UC4
  Mapper --> UC5
  Auditor --> UC6
  Planner --> UC7
  GUI --> UC8
  Operator --> UC9
  Planner --> UC10
  Writer --> UC11
  Reviewer --> UC12
  Operator --> UC13

  UC1 --> UC2
  UC2 --> UC3
  UC3 --> UC4
  UC4 --> UC5
  UC5 --> UC6
  UC6 --> UC7
  UC7 --> UC8
  UC8 --> UC9
  UC9 --> UC10
  UC10 --> UC11
  UC11 --> UC12
  UC12 --> UC13
```

## Mermaid System Sequence Diagram

```mermaid
sequenceDiagram
  autonumber
  actor User as Human User
  participant PM as Project<br/>Manifest
  participant Operator as Operator<br/>Agent Instance
  participant Team as Agent Team<br/>Instance
  participant Runtime as Workspace<br/>Runtime
  participant Adapter as Execution<br/>Adapter
  participant Agents as Team Agent<br/>Instances
  participant Provenance as Artifact and<br/>Provenance Service
  participant Views as View Manifest<br/>Generator
  participant GUI as GUI Backend<br/>and Renderer

  User->>Operator: Import manuscript, reviews,<br/>constraints, deadline
  Operator->>Team: Instantiate or reuse<br/>Team Instance
  Operator->>User: Present Team Instance<br/>and gated decisions
  User->>Operator: Approve Team Instance,<br/>handler, Gate policy
  Operator->>PM: Declare feedback Task,<br/>handler, Workspace
  Operator->>Runtime: Initialize feedback mapping<br/>Workspace Runtime
  Operator->>Adapter: Construct Team Agent<br/>Instances
  Adapter->>Agents: Start feedback<br/>mapping Run
  Agents->>Provenance: Store issues, claim links,<br/>Evidence Items, risks
  Provenance->>Runtime: Record handoffs,<br/>support gaps, risks
  Runtime->>Views: Request response matrix<br/>and claim-risk view
  Views->>GUI: Emit feedback View Manifests<br/>for built-in components
  GUI->>Operator: Surface revision strategy<br/>and analysis Gate
  Operator->>User: Ask for revision strategy<br/>and analysis approval
  User->>Operator: Approve selected<br/>analyses
  Operator->>Runtime: Submit revision strategy<br/>Gate decision
  Runtime->>Provenance: Store revision strategy<br/>Decision Record
  loop For each approved targeted analysis
    Operator->>PM: Declare Research Task,<br/>handler, Workspace
    Operator->>Runtime: Initialize analysis<br/>Workspace Runtime
    Adapter->>Agents: Start analysis<br/>Run
    Agents->>Provenance: Store result Artifacts<br/>and Evidence Items
    Provenance->>Runtime: Update Research Claims<br/>and Run status
  end
  Operator->>Agents: Request response draft<br/>and manuscript edits
  Agents->>Provenance: Store response package<br/>and reviewer audit
  Runtime->>Views: Request final<br/>approval view
  Views->>GUI: Emit final package View Manifest<br/>for built-in components
  GUI->>Operator: Surface final<br/>approval Gate
  Operator->>User: Ask for final<br/>approval Gate
  User->>Operator: Approve or return<br/>items for revision
  Operator->>Runtime: Submit final<br/>Gate decision
```

## Durable Outputs

- Research Thread for paper revision
- Research Tasks for feedback mapping and approved targeted analyses
- Agent Team Instance instantiated from an Agent Team Template, with critique mapper, evidence auditor, experiment planner, writer, and reviewer members
- Isomer Workspaces scoped to each Research Task, task handler, and selected Agent Team Instance
- Reviewer-response matrix, issue list, claim-risk map, experiment plan, result summaries, and response draft as Artifacts
- Evidence Items linked to revised Research Claims
- Gates for revision strategy, claim strengthening, new analyses, and final package approval
- Decision Records for approved revision strategy and final response package
- View Manifests for response matrix, claim-risk view, Run timeline, and final approval view
- Built-in GUI Component Instances for response matrix, claim-risk view, Run timeline, and final approval views
