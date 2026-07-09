## 1. Create the design-skill command file

- [x] 1.1 Create `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-project-design/commands/design-skill.md` with the full skill-design workflow copied from `references/skill-design.md`.
- [x] 1.2 Update the output contract in `design-skill.md` to state it reuses the feature directory resolved by the entry workflow.
- [x] 1.3 Add an explicit intent-capture step so the agent asks the user for the proposed skill name and purpose when not already clear.

## 2. Remove skill routing from design-interface

- [x] 2.1 Edit `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-project-design/commands/design-interface.md` to remove the `## Skill Target Routing` section and all skill-detection rules.
- [x] 2.2 Remove the skill-design reference line and any language that tells the agent to load `references/skill-design.md`.
- [x] 2.3 Verify `design-interface.md` still describes normal interface design for commands, routes, models, files, events, and storage contracts.

## 3. Update SKILL.md

- [x] 3.1 Add `design-skill` to the subcommands table in `SKILL.md` with purpose and detail path `commands/design-skill.md`.
- [x] 3.2 Update the artifact contracts list to mention `design/<slug>/design-overview.md` as a skill-design artifact.
- [x] 3.3 Add a note in `## Common Mistakes` warning against using `design-interface` for skill design.

## 4. Update help.md

- [x] 4.1 Edit `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-project-design/commands/help.md` to list `design-skill` alongside other subcommands.
- [x] 4.2 Include a one-line description of when to use `design-skill`.

## 5. Clean up old reference file

- [x] 5.1 Delete `extern/orphan/houmao-agents/skillset/imsight-skills/imsight-project-design/references/skill-design.md`.
- [x] 5.2 Verify no other file in the skill references `references/skill-design.md`.

## 6. Validate the skill structure

- [x] 6.1 Read the modified files to confirm internal consistency.
- [x] 6.2 Confirm `design-interface` no longer mentions skill routing and `design-skill` no longer re-resolves the feature directory.
