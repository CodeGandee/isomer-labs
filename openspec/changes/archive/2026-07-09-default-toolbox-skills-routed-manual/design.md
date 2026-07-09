## Context

User Skill Callback resolution already treats callback material as supplemental instruction owned by the active system skill. The current Toolbox Manager guidance still leaves too much room for Toolbox skills to look like ordinary implicitly invoked skills, especially when it scaffolds callback `SKILL.md` directories or converts an existing skill into callback material.

The recently restructured GPU analytical modeling Toolbox now uses prompt-file callbacks that invoke named prior skills and subcommands. Those prior skills are meant to be routed to by those callback prompts or manually invoked, not selected implicitly by the agent host.

## Goals / Non-Goals

**Goals:**

- Make routed/manual invocation the default for Toolbox-authored skills.
- Update Toolbox Manager guidance and source layout examples so `agents/openai.yaml` with `allow_implicit_invocation: false` is part of default Toolbox skill scaffolding.
- Prefer prompt-file callback routers that name an installed Toolbox skill and subcommand for a purpose.
- Update existing project-local Toolbox skills to carry non-implicit invocation metadata.

**Non-Goals:**

- Do not change User Skill Callback resolution, Toolbox manifest parsing, installed callback registry format, or CLI behavior.
- Do not ban skill-directory callback sources; keep them as an explicit supplemental-instruction exception.
- Do not turn Toolbox skills into packaged system skills.

## Decisions

### Default Toolbox skills to routed/manual invocation

When Toolbox Manager authors a Toolbox skill directory, it should create or recommend `agents/openai.yaml` with `policy.allow_implicit_invocation: false`. The default prompt should say to use the skill when routed by a Toolbox callback prompt or manually invoked for its named purpose.

Alternative considered: rely on absence of metadata. That leaves agent-host defaults ambiguous and forces every Toolbox author to rediscover the policy.

### Prefer prompt-file callback routers

For callback entries that need a Toolbox skill, the default source should be a short `prompt_file` router that says `Invoke <toolbox-skill> subcommand <subcommand>. Purpose: <purpose>.` This keeps the callback insertion point readable while leaving reusable guidance inside the skill.

Alternative considered: direct `skill_dir` callback entries. They remain valid for supplemental instruction material, but they do not clearly identify a routed subcommand or purpose and can look like automatic execution.

### Keep runtime behavior unchanged

This change is guidance and metadata only. User Skill Callback resolution already says callbacks are not automatic hook execution, and this change should align authored Toolbox material with that contract.

Alternative considered: adding runtime enforcement that rejects Toolbox skills without non-implicit metadata. That would create migration risk and is unnecessary for the current problem.

## Risks / Trade-offs

- Existing Toolbox skills may lack agent metadata -> Add `agents/openai.yaml` to current project-local Toolbox skills during implementation.
- Some Toolbox authors may still need direct skill-directory callback material -> Keep the exception documented, but require the Toolbox Manager to label it as supplemental instructions rather than automatic skill invocation.
- Prompt routers can become repetitive -> Keep router prompts intentionally short and put reusable behavior in the Toolbox skill subcommand.

## Migration Plan

1. Update `isomer-op-toolbox-mgr` main guidance and command pages to state the routed/manual default.
2. Update Toolbox Manager source-layout examples to include `agents/openai.yaml` for Toolbox skill directories.
3. Add or update `agents/openai.yaml` files for current project-local Toolbox skills with `allow_implicit_invocation: false`.
4. Verify no current Toolbox guidance describes automatic skill invocation as the default.
