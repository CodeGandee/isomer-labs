# Provider Selection

## Resolution Order

1. Resolve the current Research Topic and its Literature Provider Binding.
2. Read the binding's supported operations, available approaches, credential posture, Gate policy, recording obligations, and external-tool constraints.
3. If the actor explicitly requests an approach, use it only when the binding exposes that approach and it supports the selected action under current policy.
4. Otherwise choose a compatible bound approach by declared operation coverage. Do not infer availability from a tool name, environment variable, prior Run, or local file.
5. Load only the chosen bundle-local approach reference. A future approach can add another local reference and binding mapping without changing action pages or the normalized result contract.

## Missing or Incompatible Provider

When no valid binding can execute the external action, report the missing capability and stop or continue only with an explicitly reduced scope over user-provided sources, accepted local Artifacts, or `ext research literature` local queries. Local observations never substitute for a requested fresh provider search.

An explicit provider request that cannot run remains blocked or scope-limited. Do not silently substitute another provider, anonymous access, or a different relationship operation.

## Credentials and Gates

Resolve credentials only through the binding's approved credential mechanism and apply the applicable credential-use, cost, privacy, external-upload, or data-export Gate policy. Treat approval for one provider, purpose, or Run as bounded. Never probe arbitrary environment files or copy a credential into guidance, a rendered command, normalized output, an Artifact, or a Provenance Record.

Anonymous access is allowed only when the binding and policy permit it. Record the access method and observed throttling or feature limitations.

## Terminal Posture

Report the selected binding ref, approach id, action coverage, access method, Gate posture, and any reduced scope. A missing tool or provider is an external blocker only after the declared compatible approaches and permitted direct-HTTPS fallback have been checked.
