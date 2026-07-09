## Context

Project discovery already walks from the current directory upward and returns the first `.isomer-labs/manifest.toml` it finds. That is a nearest-ancestor algorithm, which naturally matches Git-like nested repository behavior.

The conflicting behavior lives in Project initialization: `_cmd_init` calls `find_ancestor_manifest(project_root)` and rejects the command if the selected root has an ancestor Project. This prevents legitimate nested sandboxes under paths such as `tmp/test-projects/fa4-whitebox-model`, even though future commands from that nested tree would resolve correctly once a nested manifest exists.

## Goals / Non-Goals

**Goals:**
- Allow `isomer-cli project init` to create a Project inside an existing Project tree.
- Preserve nearest Project discovery for cwd-based commands.
- Preserve explicit selector precedence for `--root` and `--manifest`.
- Keep existing overwrite refusal when the selected target root already has its own `.isomer-labs/manifest.toml`.
- Add tests for nested init, nearest nested discovery, and parent discovery outside the nested Project.

**Non-Goals:**
- Do not introduce a new workspace nesting registry.
- Do not make parent Projects aware of child Projects in their manifests.
- Do not change Topic Workspace registration semantics.
- Do not redesign cleanup beyond confirming that cleanup authority remains scoped to the selected or discovered Project root.

## Decisions

1. Treat nested Isomer Projects like nested Git repositories.

   Cwd-based Project discovery resolves the nearest manifest. The parent Project does not own the nested Project merely because the child lives below the parent directory. This is the simplest mental model for users and matches the existing discovery algorithm.

2. Remove ancestor rejection from Project init.

   The current ancestor check is the only hard blocker. `initialize_project` already owns the selected-root manifest overwrite refusal, content-root creation, and Houmao bootstrap behavior. Letting it run for the selected nested root preserves the ordinary init contract.

3. Keep explicit selectors authoritative.

   `project --root <root>` and `project --manifest <manifest>` must continue to select exactly the requested Project. Nested discovery should not override explicit input.

4. Keep cleanup and content-root relocation scoped by selected authority.

   Cleanup and content-root relocation already resolve a single Project root through explicit selectors or nearest cwd discovery. The implementation should not add child Project scanning in this change. Regression coverage should confirm that a command run in the parent resolves the parent and a command run in the nested Project resolves the child.

## Risks / Trade-offs

- Parent cleanup could still remove arbitrary directories if the user explicitly chooses destructive filesystem targets that contain a nested Project. Mitigation: this change does not broaden cleanup authority; future cleanup safety work can add nested boundary preservation if needed.
- Users may expect parent Project topic commands to see nested Project topics. Mitigation: nested Projects are independent Project roots, not child records in the parent manifest.
- Existing tests and specs encode the old rejection. Mitigation: replace them with positive nested init and nearest discovery tests.

## Migration Plan

No data migration is required. Existing Projects remain valid. Scripts that previously relied on nested init failing will now create the nested Project; this is an intentional behavior correction.

## Open Questions

- Should a future cleanup change explicitly detect nested `.isomer-labs/manifest.toml` boundaries before deleting parent-generated content trees? This is useful, but not required to fix init and nearest discovery.
