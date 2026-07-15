# Repair

Use this subcommand to diagnose first, then mutate only the parts the user authorizes.

## Workflow

1. Run `status` and classify the problem as stale declaration, absent receipt, legacy receipt, malformed or future receipt, missing or invalid projection, receipt drift, obsolete version, newer-than-CLI version, partial family, missing registration, or host refresh delay.
2. Preserve a stale declaration by default. Explain that Project state is authoritative user-controlled bookkeeping. Remove it only through an explicit user request to run Project `forget`.
3. For missing registration with a complete usable family, call `remember` without reinstalling.
4. For invalid or incompatible managed projections, propose a target-and-scope installer upgrade or forced reinstall. Require user authorization before replacement and verify the resolved root reported by the mutation.
5. For a newer-than-CLI family, upgrade `isomer-cli` before replacing or routing through that family.
6. For unmanaged same-name projections, report the conflict and avoid claiming Isomer ownership. Replace only with explicit authorization.
7. After file repair, verify the explicit root, reconcile the declaration when authorized, and report host refresh requirements.

If the user's task does not map cleanly to these steps, use your native planning tool to build a diagnose-first repair plan that preserves declarations and files outside the user's authorization, then execute the plan.

Keep repair additive unless the user explicitly asks to remove a declaration or uninstall an Isomer-managed projection.
