## ADDED Requirements

### Requirement: Production Research Skills Preserve Reconciled Invocation Context
Production research-paradigm skills SHALL consume the reconciled task target from context preflight and SHALL not replace a failed typed operation with an unrequested filesystem fallback.

#### Scenario: Typed operations retain explicit topic
- **WHEN** a production research skill invokes a topic-scoped CLI or owner service after preflight
- **THEN** it supplies the reconciled Research Topic selector and applicable Topic Actor or Agent selector
- **AND** it does not rely on a later command cwd to rediscover the target

#### Scenario: Context-bearing failure triggers diagnosis
- **WHEN** a typed operation reports not-found, wrong-scope, or context-conflict diagnostics for its selected Research Topic or worker
- **THEN** the skill compares the returned selected-context metadata with the pinned task target and reruns context alignment when necessary
- **AND** it does not search sibling Topic Workspaces or select a different manifest default as implicit recovery

#### Scenario: Failed export does not become unmanaged copy
- **WHEN** a typed export operation fails and the user did not request an alternate unmanaged copy
- **THEN** the skill preserves the canonical exchange surface and stops, corrects the explicit selector, or routes to the owning readiness workflow
- **AND** it does not copy the requested material into a Topic Actor Workspace, Agent Workspace, Topic Main repository, or arbitrary alternate directory

#### Scenario: Default Kaoju template edit request uses named-stock exchange surface
- **WHEN** the user asks to get, edit, or export the Kaoju LaTeX template without naming a custom output target
- **THEN** the write workflow selects named LaTeX stock `main` for the reconciled Research Topic and invokes the typed export without `--target`
- **AND** it reports the CLI-resolved writing-template exchange path rather than constructing an actor-local path

#### Scenario: Named LaTeX stock edit is not paper composition
- **WHEN** the user asks to export the LaTeX template for manual editing without selecting a paper-local TeX draft
- **THEN** the write workflow routes to `manage-paper-template()->export()` for named `KAOJU:PAPER-TEMPLATE-LATEX` stock
- **AND** it does not invoke `init-tex`, select `KAOJU:PAPER-DRAFT-TEX`, or represent the export as an agent-fill composition tree

#### Scenario: Paper-local TeX fill does not export or mutate stock
- **WHEN** the user asks to fill or repair the derived TeX for a selected paper line
- **THEN** the write workflow uses the selected `KAOJU:PAPER-DRAFT-TEX`, its fill manifest, and the agent-fill composition contract under the reconciled Research Topic
- **AND** it does not export or mutate named LaTeX stock unless the user separately requests that template operation

#### Scenario: Explicit alternate copy remains a separate operation
- **WHEN** the user explicitly requests an additional unmanaged copy outside the canonical exchange surface
- **THEN** the skill distinguishes that copy from the registered template export, preserves export provenance, and applies ordinary filesystem authorization and overwrite checks
- **AND** it does not register the alternate copy as canonical template state unless a typed owner operation accepts it
