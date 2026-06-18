# Consistency Notes

## Purpose

This generated note records consistency checks between the editable intention source and generated execplan.

## Notes

- The generated package keeps `deepsci-org` at the Domain Agent Team Template layer.
- The generated package preserves seven Agent Roles and does not create one Agent Role per Workflow Stage.
- The generated topology is `tree-loop` with `deepsci-org-master` as the internal root role.
- The generated package leaves Topic Workspace, Workspace Runtime, Agent Profile, Agent Instance, Capability Binding, Skill Binding projection, Gate Policy, Scheduler Policy, provider binding, mailbox, gateway, launch, and credential values as placeholders.
- The generated package uses Isomer domain terms and avoids treating `teams/deepsci-org/` as a Topic Workspace.
- The generated package separates platform mechanics from loop semantics.
