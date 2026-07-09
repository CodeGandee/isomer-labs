## Why

Houmao-backed topic operators should feel like an internal Isomer Labs capability, not a separate Houmao administration workflow exposed to users or Project Operator Sessions. Current routing assumes operator-visible Houmao skill installation or implicit Houmao project discovery, but Isomer stores the Houmao project under `.isomer-labs/`, so agents need an Isomer-provided context that names the exact Houmao skill file and Houmao Project path.

## What Changes

- Add an Isomer-managed Houmao skill projection under `.isomer-labs/houmao-skills/` for Houmao-owned system-skill material that Isomer workflows may route into.
- Add Project Manifest state for enabling or disabling Houmao integration, including a disabled state that causes Houmao-aware skills to skip related work cleanly.
- Add Isomer CLI context commands that return absolute Houmao skill paths, the explicit Houmao Project path, selected Topic Workspace context, and skip diagnostics.
- Update core Isomer Houmao interop and Topic Service Agent support guidance so skills route to Houmao procedures by asking `isomer-cli` for a skill context, then instructing the agent to follow the returned skill path with `--project-dir <project-root>/.isomer-labs`.
- Avoid installing Houmao-owned system skills into the Project Operator's ordinary skill root as a user-facing prerequisite.
- Preserve the boundary that low-level Houmao credentials, tools, launch profiles, mailboxes, gateways, and runtime details remain in Houmao-owned skill material while Isomer owns discovery, policy, and context.

## Capabilities

### New Capabilities
- `isomer-managed-houmao-skill-routing`: Project-scoped Houmao integration state, Isomer-managed Houmao skill projection, and CLI skill-context discovery for internal Houmao-backed workflows.

### Modified Capabilities
- `packaged-system-skills`: Preserve Isomer-facing Houmao bridge/support skills in core while keeping Houmao-owned projected skill material Project-local and opt-in.
- `operator-system-extension-declarations`: Extend Project Manifest declarations from optional operator system extensions to explicit Houmao integration enablement and disablement semantics.
- `isomer-houmao-interop-service-skill`: Route Houmao work through Isomer-provided skill context instead of assuming direct operator use of installed Houmao system skills or implicit Houmao project discovery.
- `topic-creator-skill`: Record and report skipped Houmao-backed Topic Service Master preparation when the Project disables Houmao integration.

## Impact

- Affected code includes Project Manifest parsing/writing, Project integration CLI commands, packaged system-skill asset metadata, Houmao adapter path helpers, and system-skill guidance for `isomer-srv-houmao-interop`, `isomer-srv-topic-service-agent-support`, and topic creation.
- Affected user workflows include `isomer-cli project init`, Project system-extension/integration setup, Topic Workspace creation, Topic Actor setup, and Topic Service Master preparation.
- No breaking change is intended for existing Houmao-backed Agent Team Instance launch paths; this change adds an Isomer-owned routing layer for skill-driven Houmao agent preparation.
