## Why

Current Isomer system skills correctly stop when a requested task lacks accepted prerequisite artifacts or inputs, but they leave the user to invoke every recovery stage separately. Users need an explicit, conservative `run-to` option that authorizes the agent to satisfy the recommended prerequisite closure and then execute the original target without repeated routine confirmations.

## What Changes

- Require a missing-prerequisite preflight to pause before prerequisite mutation, explain the missing inputs, and present recommended recovery choices.
- Put prerequisite preflight and recovery-choice handling in the controlling skill's numbered `## Workflow`, with detailed run-to rules in a directly linked reference rather than a generic troubleshooting entry.
- Add an inclusive `run-to <task>` choice, also selectable through natural-language forms such as “automate everything” or “yes to all,” that executes the recommended transitive prerequisites and the original target.
- Keep ordinary requests conservative: `do <task>` alone does not authorize automatic prerequisite recovery.
- Scope run-to authorization to the selected target and its in-scope dependency closure; do not continue to unrelated or downstream work after the target.
- Preserve owner skills, separate Runs and checkpoints, evidence rules, and nondelegable Gates while avoiding repeated prompts for routine prerequisites discovered during an authorized run-to traversal.
- Distinguish a producible missing prerequisite, which pauses with recovery routes, from a true blocker that requires an external state change.
- Apply the contract consistently to the operator entrypoint and the Kaoju and DeepSci pipeline guidance, and teach it in user-facing research workflow documentation.

## Capabilities

### New Capabilities

- `run-to-prerequisite-recovery`: Defines conservative missing-prerequisite prompting, inclusive run-to authorization, dependency traversal, target resumption, and stop boundaries.

### Modified Capabilities

- `isomer-op-entrypoint-skill`: Adds prerequisite recovery choice presentation and prompt-scoped run-to orchestration across owner routes.
- `kaoju-research-extension`: Allows explicit run-to recovery to chain bounded Kaoju procedures while preserving each procedure's terminal report and Gate discipline.
- `isomer-deepsci-pipeline`: Allows the current agent to act as the external controller after explicit run-to authorization and to traverse recoverable pipeline dependencies without repeated user prompts.
- `research-workflow-tutorial-suite`: Teaches the default pause behavior, recommended recovery choices, run-to semantics, and nondelegable stopping conditions.

## Impact

The change affects packaged operator, Kaoju, and DeepSci skill workflows and directly linked references; system-skill validation and unit fixtures that assert routing or terminal behavior; and research workflow tutorials and examples. It follows the existing troubleshooting format by reserving `## Troubleshooting Guide` for concrete execution failures rather than using it for this normal prerequisite-control branch. It does not add a CLI command, weaken prerequisite validity, merge bounded procedure Runs, or redefine the Run-level Isomer Control Mode.
