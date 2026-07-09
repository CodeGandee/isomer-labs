## ADDED Requirements

### Requirement: Batch mode is opt-in via explicit user phrases
The `imsight-project-explore` skill SHALL support a batch question mode that is triggered only when the user explicitly requests it with phrases such as "list all at once", "batch mode", "show all options", or "let me pick which ones to change".

#### Scenario: User requests batch mode
- **WHEN** the user invokes `imsight-project-explore` and includes "list all at once" in the prompt
- **THEN** the skill enters batch question mode instead of sequential questioning

#### Scenario: User does not request batch mode
- **WHEN** the user invokes `imsight-project-explore` without any batch-mode phrase
- **THEN** the skill uses the default sequential questioning loop

### Requirement: Mode choice is encoded as a workflow step
The workflow for `auto`, `design-choice`, and `any-open-question` modes SHALL include a numbered step that chooses between sequential and batch mode before entering the questioning loop.

#### Scenario: Agent loads design-choice workflow
- **WHEN** the agent reads the `design-choice` workflow
- **THEN** it finds a step that detects batch-mode phrases and branches accordingly

### Requirement: Batch mode lists all questions with proposed options
In batch mode, the agent SHALL present every material question at once, each with a **Proposed** option and a short **Pros/Cons** table.

#### Scenario: User invokes design-choice in batch mode
- **WHEN** the user invokes `design-choice` with "show all options"
- **THEN** the agent returns up to 5 questions, each with a proposed option and pros/cons

### Requirement: Batch mode respects the same question cap as sequential mode
Batch mode SHALL use the same maximum question count as sequential mode.

#### Scenario: More than five candidate questions exist
- **WHEN** the coverage scan produces more than five candidate questions
- **THEN** the agent selects the top five by impact and uncertainty and presents only those in batch mode

### Requirement: Batch responses are integrated in order
When the user overrides some answers and accepts the rest, the agent SHALL process overrides in the order given, apply proposed defaults to unmentioned items, and flag any downstream proposed option invalidated by an earlier override.

#### Scenario: User overrides an early answer
- **WHEN** the user overrides the answer to question 1 and accepts the rest
- **THEN** the agent applies the override to question 1, accepts defaults for questions 2–5, and re-evaluates whether any later proposed option conflicts with the new answer

### Requirement: SKILL.md documents batch-mode trigger phrases
The `SKILL.md` Invocation Contract SHALL list the phrases that trigger batch mode.

#### Scenario: Agent reads SKILL.md
- **WHEN** an agent reads the Invocation Contract
- **THEN** it finds the explicit list of batch-mode trigger phrases
