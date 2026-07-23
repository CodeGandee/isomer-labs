# Keep Provider Execution Outside `isomer-cli`

The paper-search workflow needs external literature-provider access, but Isomer favors letting agents use provider-native or general-purpose CLI tools directly. `isomer-cli` will not wrap, proxy, or reproduce those provider operations; it will manage queries over Isomer-owned data and validate and record normalized observations and provenance produced by the agent.

## Status

Accepted.

## Considered Options

- Put direct provider calls and all recording behavior in the paper-search skill.
- Add a Kaoju-specific or generic literature-provider proxy to `isomer-cli`.
- Keep provider execution agent-driven while using `isomer-cli` for Isomer data queries and recording.

## Consequences

- The paper-search skill owns action selection, bounds, direct tool invocation, result normalization, and handoff behavior.
- The S2 approach may use an available external CLI or direct HTTPS tooling without an Isomer wrapper.
- `isomer-cli` may expose read commands for relevant Isomer context and records and write commands for provider-neutral normalized observations and provenance.
- Provider endpoints, credentials, and raw provider request bodies remain outside Isomer CLI and core Isomer schemas.
- The recording unit, normalized schema boundary, CLI namespace, and projection version are resolved by ADRs 0002 through 0005.
