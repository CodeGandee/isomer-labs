# Core Isomer Bridge Skills with Project-Local Houmao Projection

Status: accepted

`isomer-srv-houmao-interop` and `isomer-srv-topic-service-agent-support` will remain in the core Isomer system-skill set as Isomer-facing bridge and support skills. The opt-in boundary is the Project-local Houmao skill projection under `.isomer-labs/houmao-skills/` plus Project Manifest integration policy, not whether the operator has the Isomer bridge skills installed.

## Considered Options

- Keep Isomer-facing bridge and support skills in core while making projected Houmao-owned skill material Project-local and opt-in.
- Move both bridge and support skills into an optional Isomer `houmao` extension.
- Keep Topic Service Agent support in core and move only Houmao interop into an optional extension.

## Consequences

Basic Isomer skill installation can always report disabled, not-configured, or blocked Houmao integration in Isomer language. Houmao-specific procedures still do not become user-facing operator prerequisites because the projected Houmao skill material is prepared only inside an enabled Project.
