# Publish Plan

## Workflow

1. Resolve the Source Topic Workspace, Topic Main, every registered Topic Actor Workspace, every selected-team Agent Workspace, every intent and environment surface, all `topic.records.*` surfaces, and every registered non-main `topic.repos.*` repository through read-only Isomer queries. Record unavailable topology and explicit exclusions; do not scan sibling directories to invent it.
2. Validate or prepare the binding and ignored destination. Inventory current source filesystem content through resolved semantic surfaces, including relevant untracked or uncommitted root content.
3. Classify semantic content before format. Select sanitizable intent, environment declarations, every typed durable research record revision, topic-owned components, and registered GitHub references by default. Keep downloaded material bytes and raw experiment-output bytes excluded unless the current plan explicitly enables the applicable class.
4. Assign every considered path `track`, `template`, `exclude`, `component`, or `block`. Preserve raw-material identities, immutable versions or digests, locators, retrieval observations, access, license, evidence links, normalized results, and limitations even when their attached raw bytes remain excluded.
5. Sanitize individual identity: local usernames, home paths, local Git authors and emails, personal contact fields, workstation hostnames and IPs, identity-bearing actor or agent names, and hardware serials. Preserve credential-free public or private GitHub owner/repository identities, cited researchers, organizations, public source locators, exact commits, and reproducibility-relevant hardware and software versions. Block credentials, private keys, signed URLs, authenticated locators, unresolved identity metadata, and unsupported transformations without sensitive excerpts.
6. Resolve the latest paper only through the unambiguous typed `KAOJU:PAPER-PDF` record and its accepted build and validation lineage. Permit a checksummed `%PDF-` output only after size, license, and identity-metadata review; never select it by filename or modification time.
7. Generate structured placeholders or explicitly reviewed sanitized text only in the Topic Publication Copy. Always generate root `README.md`, a portable sanitized research-record index, the projection manifest, and `topic-workspace-version.toml`. Link an eligible latest paper at `paper/latest.pdf`; otherwise use `Latest paper: not yet available.` Never edit source material.
8. Validate each selected GitHub reference's normalized credential-free locator, exact commit, semantic label, relative path, visibility, license posture, and access limitation. Treat reference checkouts as upstream submodules, not copied topic-owned components.
9. Rescan every eligible output, including README, research index, structured records, component projections, `.gitmodules`, and typed PDF metadata.
10. Compare expected output, the last projection manifest, current copy content, and stored or freshly fetched remote refs. If remote compatibility evidence is needed, fetch only into validated publication repositories:

```bash
git -C <publication-repository> fetch --no-tags publication <branch>:refs/remotes/publication/<branch>
git -C <publication-repository> merge-base --is-ancestor <fetched-commit> <planned-commit>
```

11. Report safe updates, safe deletions, destination-only or simultaneous conflicts, semantic class counts, raw-byte settings, identity substitutions, selected and unavailable components and references, access and reproduction limitations, absent or compatible refs, incompatible refs, component-first push order, and blockers.
12. Fingerprint source content, expected outputs, current copy, binding identity, semantic selections, raw-byte settings, README, research index, component topology and commits, reference locators and commits, reproduction limitations, and remote refs. Persist the schema-valid plan in the applicable support root and obtain separate privacy, conflict, raw-byte, remote-mutation, and destructive-branch approvals.

A newly available component or reference, changed source or copy content, changed binding, changed semantic or raw-byte selection, changed identity transformation, changed generated navigation, changed component or reference commit, changed limitation, or changed remote ref stales the plan.

If the request does not map cleanly to these steps, use the native planning tool to build a privacy-first publication plan and stop at the first unresolved disposition, topology, conflict, or remote boundary.
