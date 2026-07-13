## Context

The completed but unarchived `detect-versioned-system-extensions` change introduced versioned receipts, compatibility reporting, Project-local root scanning, initialization observations, and a declaration-plus-detection routing gate. Subsequent workflow analysis exposed two different control contexts. Direct CLI users can copy skills, edit receipts, or change Project declarations arbitrarily, so the CLI can provide only bounded validation. A Project Operator Session, however, receives a live skill inventory and host-owned skill paths that are unavailable to the child `isomer-cli` process.

Provider discovery layouts are not stable Isomer contracts. Current tools can discover project roots, user roots, plugins, selected environments, or dynamically supplied roots, and those mechanisms can change independently of Isomer. Hard-coding a set of Claude, Codex, Kimi, or generic paths inside Project initialization can inspect unrelated installations while still missing the root actually loaded by the operator.

The Project Manifest, an Isomer target-root receipt, and the host-visible live inventory provide three different kinds of evidence. The Project Manifest is explicit Project state and must remain authoritative even when a user made it inconsistent. A supported Isomer receipt is managed installation evidence for one agent-supplied root. The live inventory is session evidence and naturally covers user-home, plugin, and environment-owned installations without Isomer knowing their filesystem conventions.

## Goals / Non-Goals

**Goals:**

- Put provider-aware discovery and registration orchestration in a core operator skill.
- Give agents stable CLI primitives that inspect an explicit skill root or classify an explicit live inventory without exposing receipt or catalog internals.
- Trust Project declarations first, then receipt-backed project roots, then live inventory names.
- Make operator-controlled initialization and installation converge on additive Project registration without requiring a second user request.
- Keep direct CLI commands conservative and independent of provider discovery conventions.
- Preserve deterministic diagnostics for malformed receipts, partial families, invalid projections, symlinks, and version state.

**Non-Goals:**

- Do not prevent users from breaking Project manifests or skill roots manually.
- Do not make `isomer-cli` discover the active agent host, current session inventory, plugins, or user-home roots.
- Do not treat Project declarations or receipts as security boundaries or cryptographic content integrity.
- Do not automatically forget Project declarations when one operator environment lacks an extension.
- Do not guarantee that a host reloads newly installed skills in the current session.
- Do not add provider-specific skill discovery paths to canonical Isomer domain schema.

## Decisions

### Use an Agent-Owned Trust Ladder

The system-skill manager resolves one extension in this order:

1. If the Project Manifest declares the extension, trust the declaration and route. Do not preemptively remove or override it. A later load or execution error is reported as stale user-controlled state.
2. Otherwise, ask the host-aware agent for project-scope skill roots and inspect each explicit root through the internal CLI primitive. A supported Isomer receipt with a complete projected family is managed evidence and can be registered during a mutation workflow.
3. Otherwise, classify the names in the agent's live skill inventory against the packaged catalog. A complete family is ambient session evidence and can be registered during a mutation workflow.
4. Otherwise, report availability as unknown or missing and offer the owner-managed installation route.

The evidence basis remains visible in output even though the algorithm stops at the first successful level. Alternatives considered: require declarations plus filesystem verification, which recreates the two-step failure loop; or treat live inventory as the first authority, which would let one agent environment silently override explicit Project state.

### Add Explicit-Input Commands Under `internals`

Add two read-only commands intended for version-aligned system skills rather than ordinary user workflows:

```text
isomer-cli internals inspect-system-skill-root --skill-root <path> [--category core|extensions|all] [--extension <id>] [--group <name>]
isomer-cli internals classify-system-skill-inventory --skill-name <name>... [--inventory-json <path-or-stdin>]
```

`inspect-system-skill-root` owns the receipt filename and schema, current and supported legacy parsing, catalog membership, one-level projection resolution, real-directory and symlink handling, broken-link and invalid-path diagnostics, installed metadata versions, and family aggregation. The agent supplies the root; the command never searches parents, home directories, provider configuration, or conventional tool paths.

The default inspection uses supported receipt records as managed evidence. It reports receipt absence or unsupported schema explicitly rather than silently turning arbitrary directory names into managed installation state. It may report unmanaged matching projections as diagnostics, but they do not acquire the managed-receipt evidence basis.

`classify-system-skill-inventory` accepts names, and optional host-provided paths when available, then maps them to catalog groups and complete or partial extension families. It does not scan the filesystem for missing names. Repeated `--skill-name` values provide a simple agent call shape; a versioned JSON input contract supports hosts that expose structured inventories.

Both commands return the standard CLI wrapper plus a versioned internal payload contract, `mutated: false`, evidence bases, complete and missing members, projection state where applicable, receipt status, version status where available, and deterministic diagnostics. Calling the namespace `internals` signals that system skills are the intended client; the payload remains versioned because installed skills and CLI versions can differ.

Alternative considered: add more behavior to `system-skills status`. That surface requires Isomer target selection and currently owns default-root resolution, while the new primitive specifically avoids target or provider inference.

### Create a Core System-Skill Manager Owner

Add `isomer-op-system-skill-mgr` to the core packaged group. It owns local subcommands for `detect-extensions`, `reconcile-extensions`, `install-extension`, `status`, and `repair`. The skill obtains project-scope roots and the live inventory from the current host context, calls safe CLI primitives, applies the trust ladder, and explains host refresh requirements.

`isomer-op-entrypoint` routes system-skill installation, detection, reconciliation, and repair to this owner. `isomer-op-project-mgr init-project` invokes its reconciliation procedure after direct Project initialization succeeds. This keeps the trust algorithm in one owner skill rather than duplicating provider-sensitive guidance across entrypoint and project-manager references.

Alternative considered: embed all logic in `isomer-op-project-mgr`. That avoids one core skill but conflates Project lifecycle ownership with user-scope and host-session skill management.

### Automate Registration Only in Operator-Controlled Mutation Workflows

The system-skill manager calls the existing idempotent `project system-extensions remember <id>` primitive after either a successful managed installation or complete fallback discovery during Project initialization, unless the user explicitly requests detection only or opts out of registration. The automation is allowed during Project initialization, extension installation, explicit reconciliation, or a concrete extension-use request that implies Project bookkeeping. Read-only help and status remain non-mutating.

Reconciliation is additive. It never calls `forget` because absence from one root or inventory does not prove absence for another operator. If installation succeeds and registration fails, the workflow reports a partial outcome and retries registration without reinstalling on the next run. Newly installed skills receive `host_refresh_required` guidance unless the agent can observe them in a refreshed live inventory.

Alternative considered: make direct `isomer-cli project init` or `system-skills install` register automatically. Those commands lack the active agent inventory and would couple safe primitives to provider discovery assumptions.

### Remove Default CLI Root Scanning From Project Workflows

Direct Project initialization creates Project state and reports no inferred extension declarations. The prior default scan of `.claude`, `.kimi-code`, `.agents`, or Codex roots is removed. The read-only `project system-extensions detect` surface, if retained, accepts explicit skill roots and delegates their interpretation to the same internal inspector; invoking it without explicit roots does not search provider locations.

This change preserves low-level target-based installation for explicit users but stops treating those defaults as proof of the active Project Operator Session. The operator skill may still use an explicit root learned from its host or its own loaded skill path.

### Keep Version and Projection Details Advisory Under Explicit Declarations

Receipt and explicit-root inspection continue to report current, compatible-older, obsolete, malformed, drifted, and newer-than-CLI states. These states guide repair when receipt or inventory discovery is the fallback. An existing Project declaration remains the highest authority: the operator can warn about known inconsistencies, but it does not silently remove the declaration or rewrite user intent.

## Risks / Trade-offs

- [A user can declare an unavailable extension] → Trust the declaration as requested, report the eventual load or execution failure with stale-state repair guidance, and never imply that declarations are verified.
- [A valid receipt can become stale after manual filesystem edits] → Inspect receipt-recorded projection shape and report discrepancies, while documenting best-effort rather than security guarantees.
- [A live inventory can contain same-name third-party skills] → Match only packaged catalog names and expose `live_inventory` as the evidence basis; user-controlled host configuration remains trusted input.
- [An agent host may omit paths or truncate inventory] → Support name-only classification, report partial or unknown state, and avoid destructive reconciliation.
- [Newly installed skills may not load immediately] → Report `host_refresh_required` and require a new turn or thread when the host cannot confirm refresh.
- [The new change contradicts an unarchived predecessor] → Archive or synchronize `detect-versioned-system-extensions` first, then apply and archive this change as the later semantic revision.
- [An `internals` contract can still become a dependency] → Version its JSON payload, test legacy receipt handling, and keep its inputs provider-neutral and explicit.

## Migration Plan

1. Land or archive `detect-versioned-system-extensions` so its versioned receipt and compatibility foundations become the predecessor state.
2. Add internal explicit-root and inventory-classification command contracts and tests.
3. Add and package `isomer-op-system-skill-mgr`, then update operator validation and indexes.
4. Update project-manager initialization and entrypoint routing to delegate to the new owner.
5. Remove CLI Project-init default root scanning and change Project extension detection to explicit-root behavior.
6. Update documentation to distinguish direct CLI safety from operator-managed automation.
7. Preserve `remember`, `forget`, target-based installer commands, receipts, and existing Project declarations for rollback compatibility.

## Open Questions

- Whether structured live inventory input should initially use repeated `--skill-name`, JSON on stdin, or both. The design allows both; implementation should choose the smallest contract that remains easy for agents to call.
- Whether `project system-extensions detect` should remain as an explicit-root wrapper or be removed before the predecessor change is archived. The internal inspector and owner skill do not require it.
