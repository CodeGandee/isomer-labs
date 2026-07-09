# Identify Insertion Points

## Workflow

1. **Resolve filters** from the user request: target skill name, stage, core skills, optional extension id, or all visible insertion points.
2. **Use read-only discovery** through the packaged callback insertion-point catalog, normally via `isomer-cli project skill-callbacks insertion-points` or the matching read-only CLI surface.
3. **Explain each result** with target skill, stage, stage label, group, extension id when relevant, and what kind of callback material would fit.
4. **Recommend the next subcommand**: `insert-callback` when the user has callback content, `author-toolbox` when they want a full Toolbox, or `convert-skill` when they have existing skill material.
5. **Report blockers** when no insertion point matches the requested target skill and stage.

If the insertion-point request does not map cleanly to these steps, use your native planning tool to run the smallest read-only catalog query and explain the result.

## Output

Report `target_skill`, `stage`, `group`, `extension_id`, `description`, `available`, `diagnostics`, and `next_action`.

