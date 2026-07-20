---
name: isomer-op-system-skill-mgr
description: Use when a Project Operator Session needs to detect, reconcile, install, upgrade, inspect, or repair Isomer system-skill extension packs, including resolving optional extension availability, registering verified receipt-backed packs, migrating legacy flat installations, installing a pack for a concrete agent host and scope, diagnosing stale Project declarations, or explaining agent-host refresh requirements.
---

# Isomer Operator System Skill Manager

## Overview

Own working-agent system-skill extension management without teaching `isomer-cli` provider discovery conventions. Use the current agent host to supply project-scope skill roots, a concrete installation target, and live inventory names, then use Isomer's explicit-input CLI primitives for catalog, scoped installation, receipt, projection, and compatibility interpretation.

## When to Use

Use this skill for operator-controlled extension discovery, additive reconciliation, scoped installation, status inspection, repair planning, and host refresh guidance.

## Workflow

1. Resolve the current Project with Project Manifest-backed CLI discovery. If no Project exists, allow read-only catalog and root inspection, but require a selected Project before registration.
2. Select exactly one subcommand from the table below and load only its detail page plus [references/evidence-and-mutation.md](references/evidence-and-mutation.md).
3. Apply the evidence ladder in order: read the Project declaration, inspect current v4 receipt evidence in each host-known project root, use explicit-root verification for pack integrity, then classify the host-visible live inventory. A declaration establishes Project routing intent but does not by itself prove current-host usability. A live-inventory name is only an observation.
4. Preserve the selected subcommand's mutation posture. Detection and status never mutate. Reconciliation, installation, and repair mutate only when the user request authorizes that operation. For installation, default a Project Operator request to project scope and require explicit user intent before selecting user scope.
5. Report the evidence basis, compatibility state when known, declaration result, partial outcomes, and host refresh guidance.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the requested extension operation, host context, evidence order, and mutation boundary, then execute the plan.

## Subcommands

| Subcommand | Posture | Use For | Detail |
| --- | --- | --- | --- |
| `detect-extensions` | Read-only | Resolve declarations, explicit roots, and live inventory without registering anything | [references/detect-extensions.md](references/detect-extensions.md) |
| `reconcile-extensions` | Additive mutation unless opted out | Remember complete current-v4 receipt-backed extension packs in the selected Project | [references/reconcile-extensions.md](references/reconcile-extensions.md) |
| `install-extension` | Authorized installation and additive registration | Install one complete public extension pack for a concrete host target and scope, verify its v4 receipt and nested inventory, and remember it | [references/install-extension.md](references/install-extension.md) |
| `status` | Read-only | Summarize declarations, supplied roots, inventory coverage, compatibility, and refresh state | [references/status.md](references/status.md) |
| `upgrade` | Authorized managed migration | Stage complete public packs, write receipt v4, and clean only receipt-tracked legacy paths | [references/upgrade.md](references/upgrade.md) |
| `repair` | Plan-first; mutation only when requested | Diagnose stale declarations, malformed receipts, invalid projections, incompatible versions, or incomplete registration | [references/repair.md](references/repair.md) |

## Evidence Order

1. **Project declaration**: If the Project Manifest declares the extension, trust it as authoritative Project routing intent. When the task requires execution, continue with the remaining levels to establish current-host usability. If loading later fails, report stale user-controlled state and offer `repair`; never remove the declaration automatically.
2. **Current v4 receipt**: Ask the host-aware agent for project-scope skill roots it actually knows. Run `isomer-cli internals inspect-system-skill-root --skill-root <root> --extension <extension-id>` for each root. Accept managed installation evidence only when the receipt is current v4, the selected public pack is receipt-tracked, nested protected coverage is complete, and compatibility is usable.
3. **Explicit-root verification**: Use the same inspector's public projection and nested member results. A complete receiptless pack may establish `explicit_root_verified` integrity, but it remains unmanaged and does not authorize registration as a managed install. Treat legacy, partial, invalid, drifted, obsolete, newer-than-CLI, unversioned, malformed, and unsupported-receipt results as migration or repair evidence.
4. **Limited live inventory**: Submit only host-visible skill names to `isomer-cli internals classify-system-skill-inventory`. A current public name yields `entrypoint_seen` with unverified protected integrity. Old protected names or pipeline aliases yield legacy observations and candidate owning packs. Neither observation proves complete coverage or authorizes automatic Project registration.
5. **Unknown or missing**: Report the missing extension and offer `install-extension` rather than guessing a provider path.

## Host Context Boundary

Use only roots the current host exposes or that can be derived from the loaded Isomer skill's own discovery location. Do not encode `.claude/skills`, `.codex/skills`, `.kimi-code/skills`, `.agents/skills`, plugin directories, or user-home paths as universal discovery rules. A tool may load project, user, plugin, environment, symlinked, or dynamically supplied roots.

For installation, require the host to identify one supported concrete target. If the target is unknown, report a blocker without guessing a target or path. Select `--scope project` by default for a Project Operator installation; this scope is anchored to the current working directory and applies to the current agent-host project context. Select `--scope user` only after an explicit user request or confirmation, and state that the installation can affect the selected host across Projects.

Direct low-level install defaults to project scope when `--scope` is omitted. This manager still always passes `--scope <selected-scope>` so its recorded operator decision remains explicit; an explicit `user` selection is the only manager route to user-wide installation.

Run `isomer-cli --print-json system-skills install --target <host-known-target> --scope <selected-scope> --extension <extension-id>`. Read the resolved skill root from the installation result and pass that exact root to the explicit-root inspector. The scoped installer supports only target-defined project and user roots; for an arbitrary plugin, extra, or custom destination, explain the boundary and use host-native installation guidance instead of reconstructing a path override.

## Mutation Rules

Registration is additive and idempotent through `isomer-cli project system-extensions remember <extension-id>`. Never call `forget` because one operator root or inventory lacks an extension. Detection, status, internal inspection, and user opt-out remain non-mutating.

If installation or upgrade succeeds but registration fails, explain that the complete public pack is installed while Project registration remains incomplete. On retry, inspect the v4 receipt and nested inventory first, then finish registration without reinstalling a verified compatible pack. After an installation or upgrade, state that the current agent session may cache old discovery and require a host refresh or new session before claiming live usability.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

Lead with whether the requested extension work is ready, detected, reconciled, installed, partial, stale, missing, or blocked. Name the selected Project and extension, summarize declared state and member coverage, explain whether the evidence came from the Project Manifest, a managed receipt, or live inventory, and state compatibility. Mention installed files or declarations only when they changed, explain any host refresh requirement, and end with the next action.

## Operational Contract

- Treat Project declarations and Isomer receipts as trusted bookkeeping, not cryptographic verification. Keep direct `isomer-cli project init`, low-level `system-skills install`, and internal inspectors conservative; this owner skill supplies the agent-host context they lack.

## Operational Notes

- Live inventory evidence means only that the host exposed a recognized name. It never verifies the nested protected inventory.
- Keep that evidence basis visible.
- Recommend a new turn, thread, or host-native reload when required.
- Preserve Project declarations and existing projections when a supported concrete host target cannot be established.

## Guardrails

- DO NOT claim that an ambient same-name skill is package-authentic.
- DO NOT claim current-session availability after installation unless the host inventory refresh confirms it.
- DO NOT translate a custom destination request into a guessed target or private installer escape hatch.
## Local References

- [references/evidence-and-mutation.md](references/evidence-and-mutation.md): shared command contracts, evidence interpretation, and mutation boundary.
- [references/detect-extensions.md](references/detect-extensions.md): read-only ordered detection.
- [references/reconcile-extensions.md](references/reconcile-extensions.md): additive Project registration.
- [references/install-extension.md](references/install-extension.md): selected-root installation, verification, registration, and refresh.
- [references/status.md](references/status.md): read-only status reporting.
- [references/upgrade.md](references/upgrade.md): staged v1-v3 to v4 migration and bounded stale cleanup.
- [references/repair.md](references/repair.md): plan-first repair routes and stale declaration handling.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
