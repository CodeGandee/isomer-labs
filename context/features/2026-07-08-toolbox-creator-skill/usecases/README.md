# Use Cases

This directory contains feature-specific use cases for Toolbox Manager Skill.

## Index

| ID | Use Case | Status |
| --- | --- | --- |
| `UC-01` | [Identify Toolbox Callback Insertion Points](uc-01-identify-toolbox-callback-insertion-points.md) | Draft |
| `UC-02` | [Insert Toolbox Callback at Chosen Insertion Point](uc-02-insert-toolbox-callback-at-chosen-insertion-point.md) | Draft |
| `UC-03` | [Define Custom Runtime Params for Toolbox Skills](uc-03-define-custom-runtime-params-for-toolbox-skills.md) | Draft |
| `UC-04` | [Install Toolbox Directory](uc-04-install-toolbox-directory.md) | Draft |
| `UC-05` | [Author Toolbox Skill from Task Description](uc-05-author-toolbox-skill-from-task-description.md) | Draft |
| `UC-06` | [Convert Existing Skill to Toolbox Style](uc-06-convert-existing-skill-to-toolbox-style.md) | Draft |
| `UC-07` | [Initialize Toolbox from User Intent (Prompt or File)](uc-07-initialize-toolbox-from-user-intent.md) | Draft |

## Notes

- `UC-01` assumes the user invokes the Toolbox Manager Skill before authoring or installing callback entries and wants the skill to explain valid User Skill Callback targets, stages, and scope choices.
- `UC-02` assumes the user has chosen or can confirm one listed insertion point and now wants the skill to author, install, and verify a Toolbox callback for that point.
- `UC-03` assumes the user wants Toolbox callback skills to query configurable runtime params and needs the skill to design, set, import, and verify those params across Project and Topic Workspace manifest layers.
- `UC-04` assumes the user already has a Toolbox directory and wants the skill to install it into the current Isomer Labs Project for all topics or into one selected Topic Workspace.
- `UC-05` assumes the user describes a task in ordinary language and wants the skill to author a Toolbox callback skill, choose insertion points, design runtime params, write installable Toolbox files, and verify effective behavior.
- `UC-06` assumes the user has an existing skill and wants the skill converted into Toolbox-owned callback source with runtime params for dynamic decisions and Topic Workspace storage labels for output artifacts.
- `UC-07` assumes the user supplies a freeform intent prompt or an intent file and wants the skill to scaffold a complete Toolbox source tree in one go.
