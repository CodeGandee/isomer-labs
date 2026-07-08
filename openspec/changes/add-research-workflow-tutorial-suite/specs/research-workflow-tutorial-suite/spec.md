## ADDED Requirements

### Requirement: Research workflow tutorial suite
The documentation SHALL provide a research-workflow tutorial suite under `docs/tutorial/` that teaches users how to conduct a human-steered research topic through Isomer using general concepts, best practices, shortened prompt/response examples, and a concrete example workspace.

#### Scenario: Suite index exists
- **WHEN** a reader opens the research-workflow tutorial suite
- **THEN** `docs/tutorial/index.md` introduces the suite and links to all tutorial pages in the recommended order

#### Scenario: Suite uses workflow stages
- **WHEN** the tutorial suite is implemented
- **THEN** it includes pages for intent authoring, topic environment preparation, human-steered research passes, real-evidence validation, white-box model development, and paper writing/inspection

#### Scenario: Suite uses local example workspace and final public link
- **WHEN** a reader follows the research-workflow tutorials
- **THEN** the tutorials use `isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model` and `context/topic-chatlogs/merged-timeline.md` as the concrete local example material
- **AND** the tutorials keep `https://github.com/CodeGandee/isomer-example-fa4-analytical-model` in final links sections for readers who want the published copy

### Requirement: Intent authoring tutorial
The tutorial suite SHALL teach users how to author research intent by creating a Research Topic and iteratively clarifying its scope, constraints, validation standard, expected outcome, and environment gate.

#### Scenario: Intent tutorial combines topic start and clarification
- **WHEN** a reader follows `docs/tutorial/author-research-intent.md`
- **THEN** the tutorial shows how to start from a concrete research idea, create or route Research Topic creation, refine the topic overview, and stop at explicit clarification gates before environment setup

#### Scenario: Intent tutorial uses the case study safely
- **WHEN** the tutorial references the FlashAttention/B200 case
- **THEN** it presents reusable intent-authoring moves rather than requiring access to raw local chatlogs

### Requirement: Topic environment preparation tutorial
The tutorial suite SHALL teach users how to prepare a Topic Workspace environment after research intent is clear.

#### Scenario: Environment tutorial covers readiness checks
- **WHEN** a reader follows `docs/tutorial/prepare-topic-environment.md`
- **THEN** the tutorial explains how to prepare topic environment dependencies, capture host facts, acquire required repositories, handle proxy or dependency constraints, and verify readiness before research work begins

### Requirement: Human-steered research pass tutorial
The tutorial suite SHALL teach users how to run research passes as a human-steered loop instead of treating agents as unattended automation.

#### Scenario: Research pass tutorial covers steering loop
- **WHEN** a reader follows `docs/tutorial/run-a-human-steered-research-pass.md`
- **THEN** the tutorial explains how to select a research pass, inspect status and generated artifacts, decide whether to continue, stop, or redirect, and preserve the result as a research record or artifact

### Requirement: Real-evidence validation tutorial
The tutorial suite SHALL teach users to separate evidence classes and require real evidence before making real-hardware claims.

#### Scenario: Evidence tutorial separates proxy and real evidence
- **WHEN** a reader follows `docs/tutorial/validate-with-real-evidence.md`
- **THEN** the tutorial distinguishes emulator, simulator, synthetic, NCU, microbenchmark, and real-hardware evidence
- **AND** it states that real-hardware accuracy claims require matching real-hardware measurements

#### Scenario: Evidence tutorial covers failed-run diagnosis
- **WHEN** an experiment fails, runs slowly, or produces noisy measurements
- **THEN** the tutorial instructs the user to diagnose the measurement path before accepting infeasibility or treating the result as scientific evidence

### Requirement: White-box model development tutorial
The tutorial suite SHALL teach users how to develop a white-box research model as an inspectable execution-flow artifact.

#### Scenario: Model tutorial covers execution-flow refinement
- **WHEN** a reader follows `docs/tutorial/develop-a-white-box-model.md`
- **THEN** the tutorial explains how to move from formulas to an execution-flow model, use external simulator or architecture sources as references, compare candidate models, and identify saturated components and blocking paths

### Requirement: Paper writing and inspection tutorial
The tutorial suite SHALL teach users how to turn research results into a paper artifact and verify the rendered output.

#### Scenario: Paper tutorial covers rendered inspection
- **WHEN** a reader follows `docs/tutorial/write-and-inspect-a-paper.md`
- **THEN** the tutorial explains how to use the requested build tool and template, inspect rendered PDF pages, fix figures and tables based on what the reader sees, and keep central proof in the main narrative

### Requirement: Skill-first tutorial posture
The research-workflow tutorials SHALL teach users how to interact with an agent equipped with Isomer system skills, including manual skill activation as a primary user entrypoint.

#### Scenario: Tutorials show user prompts and AI responses
- **WHEN** a reader follows a research-workflow tutorial
- **THEN** the tutorial shows shortened user prompt and good AI response examples derived from the merged topic chatlog
- **AND** the examples teach how to drive, correct, approve, pause, and continue agent work
- **AND** each chat turn uses the merged-timeline style with `User Prompt:` or `AI:` labels and blockquoted turn content

#### Scenario: Tutorials show user actions for skill activation
- **WHEN** a tutorial demonstrates an Isomer workflow entrypoint
- **THEN** it includes `User Action:` examples for manual skill activation through user-facing strings such as `$<skill-name> <args>` or `/skill-name <args>`
- **AND** those examples use the merged-timeline style with blockquoted action content
- **AND** those examples do not use internal log phrasing such as `Skill activated: ...`

#### Scenario: Tutorials keep CLI mechanics under the hood
- **WHEN** docs validation scans the research-workflow tutorials
- **THEN** the tutorials do not present `pixi run isomer-cli` as normal end-user usage
- **AND** direct `isomer-cli` examples appear only in "Under the Hood" sections
