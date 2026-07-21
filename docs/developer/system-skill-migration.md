# System Skill Migration

Isomer 0.4 groups the former flat system-skill installation into three atomic packs. Each pack now has a read-only public welcome sibling and a public execution entrypoint sibling: core, DeepSci, and Kaoju. Former top-level operator, service, misc, research-recording, DeepSci stage, and Kaoju stage skills are protected members below the owning entrypoint. The old `isomer-deepsci-pipeline` and `isomer-kaoju-pipeline` names remain aliases for selection and callback normalization, not installed compatibility folders.

Current public roots use `SKILL.md`, while protected members use `SKILL-MAIN.md` so recursive host discovery does not register them independently. Preserved source entrypoints use `SKILL-SOURCE.md`. A complete pack keeps those protected filenames nested below its public execution entrypoint; only a deliberately flattened Agent Role private projection promotes a selected `SKILL-MAIN.md` to its destination `SKILL.md`.

## Managed Upgrade

Upgrade a supported receipt v1, v2, or v3 root with the same target and scope that own the existing installation:

```bash
isomer-cli system-skills status --target codex --scope project
isomer-cli system-skills upgrade --target codex --scope project
isomer-cli system-skills status --target codex --scope project
```

Select an extension when only one public extension pack is needed:

```bash
isomer-cli system-skills upgrade --target codex --scope project --extension deepsci
isomer-cli system-skills upgrade --target codex --scope project --extension kaoju
```

An extension selector includes the core pack. A deprecated `--skill <protected-logical-id>` or old pipeline alias also selects the complete owner pack and emits a diagnostic. It does not install or migrate one protected member independently.

Upgrade follows a bounded order:

1. Read and validate the old receipt.
2. Resolve selected complete public packs.
3. Reject destination conflicts before mutation.
4. Stage and validate every new pack and protected member.
5. Commit both public projections for each selected pack and receipt v5.
6. Remove only exact obsolete top-level paths tracked by the old receipt.
7. Report removed and retained stale paths.

If staging or validation fails, upgrade preserves the old receipt and projections. It does not start stale cleanup. If cleanup later fails, the new packs and v5 receipt remain valid while output reports `migration_status=partial_cleanup`, exact `stale_retained` paths, and repair guidance. Receipt v5 keeps bounded legacy path evidence until cleanup completes.

Untracked directories are never deleted because their names resemble old protected skills. Inspect and resolve such conflicts explicitly.

## Unmanaged or Malformed Roots

Use the explicit-root inspector before repair:

```bash
isomer-cli --print-json internals inspect-system-skill-root --skill-root /explicit/agent/skill/root
```

A complete receiptless pack can report `unmanaged_complete`, but that does not establish Isomer ownership. A legacy receipt reports tracked flat paths and candidate owner packs without claiming nested integrity. Malformed and future receipts block mutation because the installer cannot prove ownership safely.

Use `$isomer-op-entrypoint use system-skills to repair the installation` for a plan that preserves Project declarations and untracked paths. A stale Project declaration remains authoritative user-controlled routing intent until the user explicitly removes it.

## Refresh the Agent Host

After a successful install or upgrade, refresh the coding-agent host or start a new session. The current process may cache old top-level skills and may not discover the public welcome and entrypoint pair until reload. A live inventory may report `welcome_seen`, `entrypoint_seen`, or `public_pair_seen`; name-only inventory cannot verify receipt ownership or nested protected members.

Use the public entrypoints after refresh:

```text
$isomer-op-entrypoint use help to show the available workflows
$isomer-ext-deepsci-entrypoint use hypothesis-pass to evaluate the selected idea
$isomer-ext-kaoju-entrypoint use choose-directions to frame the survey
```
