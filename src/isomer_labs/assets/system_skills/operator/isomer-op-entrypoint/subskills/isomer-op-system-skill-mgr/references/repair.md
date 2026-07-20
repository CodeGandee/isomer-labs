# Repair

Use this subcommand to diagnose first, then mutate only the parts the user authorizes.

## Workflow

1. Run `status` and classify the problem as stale declaration, absent receipt, supported legacy receipt, malformed or future receipt, missing or invalid public pack, missing or invalid nested member, receipt drift, obsolete version, newer-than-CLI version, unmanaged complete pack, missing registration, legacy live observation, entrypoint-only observation, or host refresh delay.
2. Preserve a stale declaration by default. Explain that Project state is authoritative user-controlled bookkeeping. Remove it only through an explicit user request to run Project `forget`.
3. For missing registration with a current v5 receipt and verified complete usable pack, call `remember` without reinstalling.
4. For a supported legacy receipt, propose or run the authorized `upgrade` workflow. Stage and validate both public roles and protected members, write receipt v5, and remove only exact obsolete top-level paths tracked by the legacy receipt. Preserve untracked lookalike directories. Report every stale path retained after partial cleanup.
5. For invalid or incompatible managed public packs, propose a target-and-scope installer upgrade or forced reinstall. Require user authorization before replacement and verify the resolved root reported by the mutation.
6. For a newer-than-CLI pack, upgrade `isomer-cli` before replacing or routing through that pack.
7. For unmanaged same-name public packs or legacy protected projections, report the conflict and avoid claiming Isomer ownership. Replace only with explicit authorization.
8. After file repair, verify the v5 receipt and complete public-pair and nested inventory, reconcile the Project declaration when authorized, and report that a host refresh or new session is required before claiming live usability.

If the user's task does not map cleanly to these steps, use your native planning tool to build a diagnose-first repair plan that preserves declarations and files outside the user's authorization, then execute the plan.

Keep repair additive unless the user explicitly asks to remove a declaration or uninstall an Isomer-managed projection.
