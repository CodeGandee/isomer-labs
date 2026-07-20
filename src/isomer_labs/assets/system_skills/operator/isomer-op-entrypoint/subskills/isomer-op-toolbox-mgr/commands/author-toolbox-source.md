# Author Toolbox Source

## Workflow

1. **Resolve the Toolbox source root** from user input or default `skillset/toolboxes/<toolbox-id>/`.
2. **Check path safety**. Block writes outside the Project root unless the user supplied an allowed external path and the operation supports it.
3. **Create or update only requested files**: `manifest.toml`, prompt router files, Toolbox skill directories, Toolbox skill `agents/openai.yaml` metadata, Runtime Param bundle files, and concise README notes.
4. **Preserve existing files** unless the user asked to update them. When replacing material, keep enough detail to report rollback hints.
5. **Return authored paths** to the caller with what changed, what was skipped, and which validation command should run next.

If the source authoring request does not map cleanly to these steps, use your native planning tool to create a file-level plan and stop before destructive edits.

## Source Layout

Use this default shape when the user did not provide a stronger local convention:

```text
skillset/toolboxes/<toolbox-id>/
  manifest.toml
  README.md
  callbacks/<target-stage-purpose>.md
  <toolbox-skill-name>/SKILL.md
  <toolbox-skill-name>/agents/openai.yaml
  params/<bundle-name>.toml
```

Do not create empty folders. Create only the files the Toolbox needs.

## Invocation Metadata

For each Toolbox skill directory, default `agents/openai.yaml` to this posture:

```yaml
interface:
  display_name: "<toolbox-skill-name>"
  short_description: "<brief routed/manual purpose>"
  default_prompt: "Use $<toolbox-skill-name> when routed by a Toolbox callback prompt or manually invoked for <purpose>."
policy:
  allow_implicit_invocation: false
```

Use prompt files in `callbacks/` as routers when a callback should apply a Toolbox skill subcommand. A router prompt should name the installed skill, subcommand, and purpose; the durable behavior stays in the Toolbox skill.
