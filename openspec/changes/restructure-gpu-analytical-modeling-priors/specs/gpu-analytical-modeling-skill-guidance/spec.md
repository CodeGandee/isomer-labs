## ADDED Requirements

### Requirement: GPU Analytical Modeling Guidance Is Organized as Stage Priors
The GPU analytical-modeling Toolbox guidance SHALL expose installed prior skills named for the DeepSci stage they guide and subcommands named for the specific prior purpose.

#### Scenario: Prior skill names identify stages
- **WHEN** the Toolbox skill directories are inspected after implementation
- **THEN** stage-prior skills use names like `gpu-analytic-scout-prior`, `gpu-analytic-idea-prior`, and `gpu-analytic-experiment-prior`
- **AND** broad domain-skill names are not the primary callback targets

#### Scenario: Subcommands preserve prior purpose
- **WHEN** an agent invokes a stage-prior subcommand from a callback prompt
- **THEN** the subcommand provides concise guidance for that insertion point without requiring the agent to infer the purpose from a broad domain skill

#### Scenario: Existing guidance remains generic
- **WHEN** stage-prior guidance discusses sources, model shape, evidence, experiments, reporting, or closure
- **THEN** it remains generic to GPU kernel analytical modeling and does not require a specific topic workspace, kernel, GPU SKU, host, paper venue, or artifact path
