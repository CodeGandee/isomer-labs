## 1. Update SKILL.md Invocation Contract

- [x] 1.1 Add batch-mode trigger phrases to the Invocation Contract in `SKILL.md`.
- [x] 1.2 State that batch mode is opt-in and the default remains sequential.

## 2. Update commands/auto.md workflow

- [x] 2.1 Insert a numbered "Choose questioning mode" step after the Coverage Scan in the workflow.
- [x] 2.2 Branch the workflow into sequential and batch paths after mode selection.
- [x] 2.3 Add a batch response format example showing multiple questions with proposed options.
- [x] 2.4 Add integration rules for batch responses.

## 3. Update commands/design-choice.md workflow

- [x] 3.1 Insert a numbered "Choose questioning mode" step after the Coverage Scan in the workflow.
- [x] 3.2 Branch the workflow into sequential and batch paths after mode selection.
- [x] 3.3 Add a batch response format example showing multiple questions with proposed options.
- [x] 3.4 Add integration rules for batch responses.

## 4. Update commands/any-open-question.md workflow

- [x] 4.1 Insert a numbered "Choose output mode" step after classification and prioritization.
- [x] 4.2 Branch the workflow into sequential (route to next mode) and batch (list all with options) paths.
- [x] 4.3 Add a batch response format example for open-question maps.
- [x] 4.4 Add integration rules for batch responses.

## 5. Validate changes

- [x] 5.1 Read the modified files to confirm the workflow branches are encoded as numbered steps and no side-notice style guards are introduced.
- [x] 5.2 Confirm default sequential behavior is unchanged when no batch-mode phrase is used.
- [x] 5.3 Confirm batch-mode trigger phrases are consistent across `SKILL.md` and the three mode files.
