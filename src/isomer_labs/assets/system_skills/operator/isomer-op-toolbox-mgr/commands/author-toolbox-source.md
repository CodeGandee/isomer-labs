# Author Toolbox Source

## Workflow

1. **Resolve the Toolbox source root** from user input or default `skillset/toolboxes/<toolbox-id>/`.
2. **Check path safety**. Block writes outside the Project root unless the user supplied an allowed external path and the operation supports it.
3. **Create or update only requested files**: `manifest.toml`, callback instruction directories or prompt files, Runtime Param bundle files, and concise README notes.
4. **Preserve existing files** unless the user asked to update them. When replacing material, keep enough detail to report rollback hints.
5. **Return authored paths** to the caller with what changed, what was skipped, and which validation command should run next.

If the source authoring request does not map cleanly to these steps, use your native planning tool to create a file-level plan and stop before destructive edits.

## Source Layout

Use this default shape when the user did not provide a stronger local convention:

```text
skillset/toolboxes/<toolbox-id>/
  manifest.toml
  README.md
  callbacks/<callback-key>/SKILL.md
  params/<bundle-name>.toml
```

Do not create empty folders. Create only the files the Toolbox needs.

