# Convert Skill

## Workflow

1. **Resolve the source skill** from the path or named skill in the request. Confirm the directory contains `SKILL.md`.
2. **Classify the conversion target**: prompt-file callback, skill-directory callback, copied callback skill, or a rewritten Toolbox-local callback instruction file.
3. **Choose Toolbox identity and local key**. Derive a path-safe Toolbox ID and a toolbox-local callback key, then report the installed callback id shape.
4. **Map target insertion point** by identifying target packaged system skill and stage. If missing, run or suggest `identify-insertion-points` first.
5. **Create Toolbox source** with [author-toolbox-source.md](author-toolbox-source.md) and add callback manifest material with [edit-callback-declarations.md](edit-callback-declarations.md).
6. **Map configuration** by moving user-tunable values into Runtime Params when the source skill contains topic-specific constants, paths, thresholds, or prompt settings.
7. **Validate and report** the source path, conversion choices, callback ids, Runtime Param ids, blockers, and next install or review command.

If the conversion does not map cleanly to these steps, use your native planning tool to build a conversion plan that preserves the source skill's visible behavior while separating Toolbox source, callback declarations, and Runtime Params.

## Conversion Rules

- Preserve source skill ownership: a copied or referenced skill directory becomes supplemental callback instruction material, not a packaged system skill.
- Do not copy secrets, credentials, private environment values, or user-specific local paths into Toolbox source.
- Keep broad behavioral rewrites explicit. If a source skill needs redesign before conversion, stop and report the redesign blocker.

