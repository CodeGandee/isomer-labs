## MODIFIED Requirements

### Requirement: Kaoju Uses Existing Platform Owners
Kaoju skills SHALL use existing Isomer owner skills, Service Requests, and extension points for topology, environment, provider, execution, Gate, path, and recording behavior while keeping repository command selection and execution with the acting user or agent.

#### Scenario: Governed mutation routes to owner
- **WHEN** a Kaoju procedure needs Topic Workspace registration or projection, environment preparation, managed dataset links, credentials, private data, large downloads other than repository command execution, document builds, viewer launch, or accelerator execution
- **THEN** it routes the operation to the applicable project, workspace, service, provider-binding, execution-adapter, or Gate owner
- **AND** it records and consumes returned durable refs rather than bypassing the owner

#### Scenario: Repository acquisition stays outside platform execution owners
- **WHEN** a Kaoju procedure needs to clone, fetch, copy, check out, deepen, repair, or otherwise acquire repository content
- **THEN** the acting user or agent selects and executes the commands outside `isomer-cli`, Isomer services, Service Requests, and Execution Adapter Command Requests under the applicable Gate and authorization
- **AND** the procedure routes only target planning, post-verification semantic registration, Artifact recording, and provenance recording to Isomer owners

#### Scenario: Environment preparation uses a Service Request
- **WHEN** UC-09 needs to inspect or mutate Pixi environment state
- **THEN** the Project Operator Session or Operator Agent opens a Service Request for the Service Team and relates it to the active Research Task and Run
- **AND** the Kaoju skill does not represent itself as the environment owner

#### Scenario: Generic maintenance is not promoted to a survey procedure
- **WHEN** repository refresh, generic environment repair, claim tracing, or resume is needed only as an implementation step
- **THEN** Kaoju performs an authorized repository command directly or routes another owned step inside the active survey procedure
- **AND** it does not create a new top-level survey procedure for the generic task

#### Scenario: Direct user intent remains public
- **WHEN** the actor explicitly requests source-code ingestion, code-run preparation, or a source-code trial as defined by UC-08, UC-09, or UC-10
- **THEN** the pipeline exposes the corresponding bounded intent while keeping repository execution external and routing other owned mutations to platform owners
- **AND** the public intent does not make the capability skill the owner of workspace topology, environment, or trial-execution infrastructure
