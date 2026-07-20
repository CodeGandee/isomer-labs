# Show System-Skill Extensions

## Workflow

1. Run `isomer-cli --print-json system-skills extensions list` to read package-owned extension metadata.
2. If one extension is named, run `isomer-cli --print-json system-skills extensions show <extension-id>`.
3. When Project declaration state matters, run `isomer-cli --print-json project system-extensions list`.
4. Report each extension's independent welcome, execution entrypoint, purpose, command summary, and evidence state from **Evidence States**.
5. Recommend the extension welcome for orientation or its entrypoint for an already concrete task.
6. Route lifecycle work through `$isomer-op-entrypoint use system-skills to <task>` without mutating state here.

If the request does not map cleanly to these steps, use the native planning tool to build a read-only discovery plan from package metadata, Project declarations, and the user's research goal, then report one public next route.

## Evidence States

| State | Meaning |
| --- | --- |
| Catalog-known | The installed Isomer package describes the welcome, entrypoint, commands, and protected inventory; this is not installation evidence. |
| Project-declared | The Project Manifest records authoritative routing intent; this is not pack-integrity proof. |
| Welcome-seen | Limited live inventory shows the public welcome name; the entrypoint and protected integrity remain unverified. |
| Entrypoint-seen | Limited live inventory shows the public entrypoint name; the welcome and protected integrity remain unverified. |
| Integrity-verified | Current receipt or explicit-root evidence verifies both public roles, versions, ownership, compatibility, and the protected entrypoint inventory. |

DeepSci learning uses `$isomer-ext-deepsci-welcome`; concrete production-research work uses `$isomer-ext-deepsci-entrypoint use <command> to <task>`. Kaoju learning uses `$isomer-ext-kaoju-welcome`; concrete survey work uses `$isomer-ext-kaoju-entrypoint use <command> to <task>`.

After installation or upgrade, recommend an agent-host refresh or new session before assuming the projected skills are discoverable.
