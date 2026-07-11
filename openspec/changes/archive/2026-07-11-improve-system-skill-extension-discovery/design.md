## Context

The packaged system-skill manifest already identifies `deepsci` and `kaoju` as optional extension groups, and `system-skills list` includes both in a broad inventory. A user who does not already know the `kaoju` id must read that inventory, infer the entry skill, and discover the installation and invocation model elsewhere. The top-level `ext` group adds ambiguity because it hosts research-record runtime commands and a DeepScientist compatibility adapter, not every packaged system-skill extension.

The discovery contract must remain package-resource based, deterministic in text and JSON modes, and usable from an installed wheel without a repository checkout.

## Goals / Non-Goals

**Goals:**

- Give packaged extensions a focused list and show surface under `system-skills`.
- Describe each extension's purpose, public entry skill, named commands, install command, status command, and invocation form from manifest-owned metadata.
- Expose valid extension ids in selection help and shell completion.
- Explain the difference between runtime `ext` commands and installable system-skill extensions.
- Preserve existing installation, status, upgrade, and uninstall semantics.

**Non-Goals:**

- Add `isomer-cli ext kaoju` or make the CLI execute Kaoju survey procedures.
- Change the existing `ext research` or `ext deepsci` behavior.
- Detect whether an extension is installed without an explicit target and target root.
- Add a plugin loader, runtime provider, persistence model, or Project declaration mechanism.

## Decisions

### 1. Put Agent-Skill Extension Discovery under `system-skills extensions`

Add `isomer-cli system-skills extensions list` and `isomer-cli system-skills extensions show <extension-id>`. The parent namespace owns package discovery and installation, so it can explain the complete lifecycle without implying that every skill extension has a runtime CLI adapter.

Adding `ext kaoju` was rejected because Kaoju's public procedures are agent skill commands. A CLI group with no native runtime implementation would duplicate skill documentation and reinforce the existing namespace ambiguity.

### 2. Keep Discovery Metadata in the Packaged Manifest

Each extension group declares an `entry_skill` and ordered `commands` list. The parser validates that the entry skill belongs to the group, each command is a stable command id, and core groups do not declare extension-only metadata. `SystemSkillExtension` exposes the fields to CLI and other catalog consumers.

The manifest remains the source of truth because inspecting command directories would depend on layout conventions and could expose internal support pages. Hardcoding Kaoju in the CLI was rejected because future extension families would require Python changes merely to become discoverable.

### 3. Return Commands and Ready-to-Run Guidance

Both discovery commands return structured extension objects. Each object contains `extension_id`, `group`, `description`, `entry_skill`, `commands`, `skills`, `install_command`, `status_command`, and `invocation`. Human output shows the same essential information. `show` rejects an unknown id before any mutation.

The commands are guidance strings, not executable callbacks. `invocation` uses `$<entry-skill>`, while each named command is shown as an argument to that skill.

### 4. Use Catalog-Derived Click Choices for Existing Selectors

The shared `--extension` option uses the ordered extension ids returned by the packaged catalog. This makes help and shell completion advertise `deepsci` and `kaoju`, while the selection layer retains its deterministic validation.

### 5. Clarify the `ext` Namespace in Help and Documentation

The `ext` help states that it contains native runtime and compatibility command surfaces and points users to `system-skills extensions` for installable agent-skill extensions. The system-skill documentation includes focused discovery and Kaoju show examples.

## Risks / Trade-offs

- [Manifest command metadata can drift from skill command pages] → Validate the known extension entry skill and command inventory in package-asset tests, and keep the metadata ordered and explicit.
- [Import-time Click choices depend on packaged assets] → Use the same package resources required by the command registration and cover CLI help from installed-package-compatible tests.
- [The word extension remains overloaded] → Put a direct cross-reference in both namespaces and describe their distinct ownership.
- [Future extensions may have no single coordinator] → Allow an empty command list, but require one entry skill for optional packaged extensions until a concrete multi-entry use case appears.

## Migration Plan

Add metadata to the existing DeepSci and Kaoju groups, extend parsing, register the focused CLI commands, update help and docs, then run package and CLI tests. Existing manifests and target-root installation manifests do not change. Rollback removes the new commands and metadata fields without touching installed skills.

## Open Questions

None.
