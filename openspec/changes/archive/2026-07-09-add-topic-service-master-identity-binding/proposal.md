## Why

Houmao requires concrete specialist, launch profile, and managed-agent names before its system skills can create or launch a Topic Service Master. The current Isomer-routed Houmao integration returns Topic Workspace context and projected skill paths, but it leaves those names and the durable binding to the agent, which makes repeated preparation ambiguous and hard to inspect.

## What Changes

- Add a canonical Isomer CLI naming contract for Topic Service Master Houmao entities derived from a Project Manifest-backed Topic Workspace id.
- Extend Houmao skill-context output so agents receive stable `specialist_name`, `launch_profile_name`, and `managed_agent_name` values for the selected Topic Workspace.
- Persist the binding between a Topic Workspace and its Houmao specialist/profile/agent refs in the Topic Workspace Manifest.
- Add CLI read/write support for querying suggested Topic Service Master names and recording or inspecting the Topic Workspace binding.
- Revise Topic Service Master system skill guidance so `prepare-topic-service-master` passes the suggested names to Houmao-owned procedures and records the resulting binding before launch.
- Ensure topic-local agents and Topic Actors can query their selected Topic Workspace id and Topic Service Master identity context from `isomer-cli`.

## Capabilities

### New Capabilities

- `topic-service-master-identity-binding`: Canonical Topic Service Master name derivation, Houmao entity binding, and CLI context for Topic Workspace-scoped Houmao specialist/profile/agent refs.

### Modified Capabilities

- `topic-workspace-manifest`: Store Topic Service Master Houmao entity bindings as topic-owned configuration.
- `cli-topic-context-resolution`: Include Topic Workspace id and Topic Service Master identity context in agent/actor self and topic-context queries.
- `topic-creator-skill`: Route Topic Service Master preparation with stable Isomer-provided names and record skipped or bound state in readiness output.
- `isomer-houmao-interop-service-skill`: Require projected Houmao procedure routing to use Isomer-provided Topic Service Master names and binding refs.

## Impact

- Affected code includes Topic Workspace Manifest parsing/writing, workspace self/context CLI payloads, Houmao integration skill-context payloads, Topic Service Master naming helpers, and system skill assets.
- Affected workflows include Topic Workspace creation, Topic Service Master preparation, launch, inspect, stop, repair, and agent/actor startup context inside a Topic Workspace.
- This change does not require `isomer-cli` to own Houmao credential or launch-profile procedure details; it owns stable Isomer names and durable binding refs that Houmao-owned skills consume.
