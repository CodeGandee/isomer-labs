---
name: isomer-op-system-skill-mgr
description: Use when a Project Operator Session needs to detect, reconcile, install, inspect, or repair Isomer system-skill extensions, including resolving optional extension availability, registering receipt-backed or live-inventory extensions, installing an extension for a concrete agent host and scope, diagnosing stale Project declarations, or explaining agent-host refresh requirements.
---

# Isomer Operator System Skill Manager

## Overview

Own working-agent system-skill extension management without teaching `isomer-cli` provider discovery conventions. Use the current agent host to supply project-scope skill roots, a concrete installation target, and live inventory names, then use Isomer's explicit-input CLI primitives for catalog, scoped installation, receipt, projection, and compatibility interpretation.

## When to Use

Use this skill for operator-controlled extension discovery, additive reconciliation, scoped installation, status inspection, repair planning, and host refresh guidance.

## Workflow

1. Resolve the current Project with Project Manifest-backed CLI discovery. If no Project exists, allow read-only catalog and root inspection, but require a selected Project before registration.
2. Select exactly one subcommand from the table below and load only its detail page plus [references/evidence-and-mutation.md](references/evidence-and-mutation.md).
3. Apply the evidence ladder in order: trust the Project declaration, inspect each host-known project root, then classify the host-visible live inventory. Stop at the first evidence level that establishes the requested extension.
4. Preserve the selected subcommand's mutation posture. Detection and status never mutate. Reconciliation, installation, and repair mutate only when the user request authorizes that operation. For installation, default a Project Operator request to project scope and require explicit user intent before selecting user scope.
5. Report the evidence basis, compatibility state when known, declaration result, partial outcomes, and host refresh guidance.

If the user's task does not map cleanly to these steps, use your native planning tool to build a step-by-step plan from the requested extension operation, host context, evidence order, and mutation boundary, then execute the plan.

## Subcommands

| Subcommand | Posture | Use For | Detail |
| --- | --- | --- | --- |
| `detect-extensions` | Read-only | Resolve declarations, explicit roots, and live inventory without registering anything | [references/detect-extensions.md](references/detect-extensions.md) |
| `reconcile-extensions` | Additive mutation unless opted out | Remember complete receipt-backed or live-inventory extensions in the selected Project | [references/reconcile-extensions.md](references/reconcile-extensions.md) |
| `install-extension` | Authorized installation and additive registration | Install one extension for a concrete host target and scope, verify its resolved root, and remember it | [references/install-extension.md](references/install-extension.md) |
| `status` | Read-only | Summarize declarations, supplied roots, inventory coverage, compatibility, and refresh state | [references/status.md](references/status.md) |
| `repair` | Plan-first; mutation only when requested | Diagnose stale declarations, malformed receipts, invalid projections, incompatible versions, or incomplete registration | [references/repair.md](references/repair.md) |

## Evidence Order

1. **Project declaration**: If the Project Manifest declares the extension, trust it and route without preflight filesystem verification. If loading later fails, report stale user-controlled state and offer `repair`; never remove the declaration automatically.
2. **Managed explicit root**: Ask the host-aware agent for project-scope skill roots it actually knows. Run `isomer-cli internals inspect-system-skill-root --skill-root <root> --extension <extension-id>` for each root. Accept only a complete receipt-backed family whose compatibility state is usable; treat obsolete, newer-than-CLI, drifted, malformed, unversioned, partial, unmanaged, and invalid results as repair evidence.
3. **Live inventory**: Submit host-visible skill names to `isomer-cli internals classify-system-skill-inventory`. A complete extension family establishes ambient `live_inventory` evidence. Do not inspect submitted paths or invent missing inventory entries.
4. **Unknown or missing**: Report the missing extension and offer `install-extension` rather than guessing a provider path.

## Host Context Boundary

Use only roots the current host exposes or that can be derived from the loaded Isomer skill's own discovery location. Do not encode `.claude/skills`, `.codex/skills`, `.kimi-code/skills`, `.agents/skills`, plugin directories, or user-home paths as universal discovery rules. A tool may load project, user, plugin, environment, symlinked, or dynamically supplied roots.

For installation, require the host to identify one supported concrete target. If the target is unknown, report a blocker without guessing a target or path. Select `--scope project` by default for a Project Operator installation; this scope is anchored to the current working directory and applies to the current agent-host project context. Select `--scope user` only after an explicit user request or confirmation, and state that the installation can affect the selected host across Projects.

Direct low-level install defaults to project scope when `--scope` is omitted. This manager still always passes `--scope <selected-scope>` so its recorded operator decision remains explicit; an explicit `user` selection is the only manager route to user-wide installation.

Run `isomer-cli --print-json system-skills install --target <host-known-target> --scope <selected-scope> --extension <extension-id>`. Read the resolved skill root from the installation result and pass that exact root to the explicit-root inspector. The scoped installer supports only target-defined project and user roots; for an arbitrary plugin, extra, or custom destination, explain the boundary and use host-native installation guidance instead of reconstructing a path override.

## Mutation Rules

Registration is additive and idempotent through `isomer-cli project system-extensions remember <extension-id>`. Never call `forget` because one operator root or inventory lacks an extension. Detection, status, internal inspection, and user opt-out remain non-mutating.

If installation succeeds but registration fails, explain that the extension files are installed while Project registration remains incomplete. On retry, inspect first and finish registration without reinstalling a complete compatible family. After a new installation, state that a host refresh is required unless the host can confirm the skills in a refreshed live inventory.

## Output Contract

Default to **Essential Output** in chat. Use **Complete Output** when the user asks for complete, verbose, audit, debug, full handoff, or full output. Present either depth in natural-language Markdown. If the user explicitly requests JSON or another machine-readable format, serialize the applicable information in that format.

Lead with whether the requested extension work is ready, detected, reconciled, installed, partial, stale, missing, or blocked. Name the selected Project and extension, summarize declared state and member coverage, explain whether the evidence came from the Project Manifest, a managed receipt, or live inventory, and state compatibility. Mention installed files or declarations only when they changed, explain any host refresh requirement, and end with the next action.

## Operational Contract

- Treat Project declarations and Isomer receipts as trusted bookkeeping, not cryptographic verification. Keep direct `isomer-cli project init`, low-level `system-skills install`, and internal inspectors conservative; this owner skill supplies the agent-host context they lack.

## Operational Notes

- Live inventory evidence means only that the host exposed every package-catalog name.
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
- [references/repair.md](references/repair.md): plan-first repair routes and stale declaration handling.

## Chat Response

Present normal chat responses in natural-language Markdown. Lead with the outcome, use descriptive headings when they improve readability, and use lists only for genuinely distinct items. Treat named output items as information to cover, not as literal response keys. Do not emit `snake_case: value`, pseudo-JSON, pseudo-YAML, or a flat program-style record unless the user explicitly requests machine-readable output. Keep exact schemas in durable artifacts and summarize them naturally in chat.
