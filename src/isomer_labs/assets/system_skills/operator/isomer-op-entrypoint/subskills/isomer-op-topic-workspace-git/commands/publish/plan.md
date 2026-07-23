# Publish Plan

## Workflow

1. Resolve the Source Topic Workspace and every currently available Topic Main, registered Topic Actor Workspace, and selected-team Agent Workspace through read-only Isomer queries. Record unavailable components and explicit exclusions; do not scan directories to invent topology.
2. Validate or prepare the binding and ignored destination. Inventory current source filesystem content through semantic surfaces, including relevant untracked or uncommitted root content.
3. Assign every considered path `track`, `template`, `exclude`, `component`, or `block`. Diagnose size, format, credential, private-key, signed-URL, license, and ambiguity risks without sensitive excerpts.
4. Generate structured placeholders or explicitly reviewed sanitized text only in the Topic Publication Copy. Never edit source material. Block unsupported binary or archive masking.
5. Rescan every eligible output. Render the sanitized projection manifest and `topic-workspace-version.toml` without absolute source paths, source remotes, credentials, or sensitive content.
6. Compare expected output, the last projection manifest, current copy content, and stored or freshly fetched remote refs. If remote compatibility evidence is needed, fetch only into validated publication repositories:

```bash
git -C <publication-repository> fetch --no-tags publication <branch>:refs/remotes/publication/<branch>
git -C <publication-repository> merge-base --is-ancestor <fetched-commit> <planned-commit>
```

7. Report safe updates, safe deletions, destination-only or simultaneous conflicts, selected and unavailable components, absent or compatible refs, incompatible refs, component-first push order, and blockers.
8. Fingerprint source content, expected outputs, current copy, binding identity, component topology and commits, and remote refs. Persist the schema-valid plan in the applicable support root and obtain separate privacy, conflict, remote-mutation, and destructive-branch approvals.

A newly available component, changed source or copy content, changed binding, changed component commit, or changed remote ref stales the plan.

If the request does not map cleanly to these steps, use the native planning tool to build a privacy-first publication plan and stop at the first unresolved disposition, topology, conflict, or remote boundary.
