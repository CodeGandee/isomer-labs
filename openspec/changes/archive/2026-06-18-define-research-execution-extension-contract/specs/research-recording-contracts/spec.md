## ADDED Requirements

### Requirement: Research Extension Recording
The system SHALL record execution, provider, scheduler, baseline-waiver, Skill Binding, and Gate policy extension choices through existing durable research records without creating runtime-state fields on Artifact Core Records, Research Topic Config, or Effective Topic Context.

#### Scenario: Command request is linked to Run and Provenance records
- **WHEN** an Execution Adapter Command Request is created, dispatched, completed, failed, cancelled, superseded, retried, or imported from an external executor
- **THEN** the system records selected extension point refs, Capability Binding refs, Skill Binding projection refs, Execution Adapter refs, policy refs, source refs, input refs, expected output refs, outcome summary refs, and actor refs through Run records, Artifact refs, and Provenance Records

#### Scenario: Provider results are recorded by evidence-use intent
- **WHEN** a literature provider, baseline provider, renderer, exporter, service adapter, or other provider-backed extension returns results
- **THEN** the system records those results as Artifacts, Findings, Evidence Items, or Provenance Records according to the result's evidence-use intent and does not treat provider output as claim support until accepted Evidence Item links exist

#### Scenario: Context-only literature is preserved before distillation
- **WHEN** a literature provider result is collected only for orientation, source review, adjacent-work scouting, or future comparison
- **THEN** the system records the raw or provider-shaped result as a provider-output Artifact with source metadata and Provenance refs before any optional Finding or Evidence Item is derived from it

#### Scenario: Gate policy preflight records governed decisions
- **WHEN** execution preflight allows, blocks, defers, or escalates a governed operation because of cost, credential use, private data access, external upload, long compute, destructive change, publication-facing output, or baseline waiver
- **THEN** the system records the selected policy refs, operation refs, affected resources, rationale, actor refs, and outcome through Gates, Decision Records, or Provenance Records according to the Research Recording Contracts

#### Scenario: Baseline waiver preserves comparator context
- **WHEN** a baseline-waiver policy or Gate permits work to continue without an accepted active baseline
- **THEN** the system records the waiver as a Decision Record or Gate outcome, links the affected Research Topic, Research Inquiry, Research Task, Run, comparator Artifacts, Evidence Items, Findings, and known limitations, and keeps later claims from treating the waiver itself as comparator evidence

#### Scenario: Scheduler observations stay durable but not authoritative over route state
- **WHEN** scheduler policy, continuation policy, a completion watcher, or an external queue reports progress, retry, pause, resume, stale-watch, failure, or completion signals
- **THEN** the system records durable observations through Run records, Signal Observations, Artifacts, or Provenance Records while leaving Workflow Stage Cursor and Agent Team Instance lifecycle state as the authority for research route and lifecycle state

#### Scenario: Extension refs do not expand Artifact Core Record
- **WHEN** an Artifact was produced, validated, rendered, exported, imported, or superseded through an execution or provider extension
- **THEN** selected extension refs, adapter refs, command request refs, validation outcomes, provider refs, and policy refs are stored through Provenance Records, metadata records, Artifact Link Records, or other accepted attachments rather than new mandatory Artifact Core Record fields

#### Scenario: Missing recording obligations block dispatch
- **WHEN** an executable or provider-backed operation lacks the Run, Artifact, Evidence Item, Finding, Decision Record, Gate, or Provenance recording obligations required by its selected Research Operation Extension Point
- **THEN** validation blocks only the dependent dispatch or promotion and reports the missing recording obligation
