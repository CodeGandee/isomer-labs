# Materialize Profile

## Workflow

When this subcommand is selected, execute the following steps in order.

1. Check **Prerequisite Artifacts**. If any required predecessor artifact is missing, refuse to run and tell the user why.
2. Confirm the registered Research Topic, registered Topic Workspace, Domain Agent Team Template, packet path or packet inputs, registration assurance evidence, and approval provenance.
3. Run generic packet and profile-bundle validation before mutation.
4. Materialize the approved static Topic Agent Team Profile Bundle under `<topic-workspace>/team-profile/`:
   - Include `profile.toml`, packet, approval, validation, copied template material, and provenance files.
5. Report the Project Manifest registration ref that should point at the bundle's `profile.toml`.
6. Validate the Project Manifest and profile bundle after materialization.

If the user's task does not map cleanly to these steps, use your native planning tool to identify the missing packet, approval, or workspace input, then execute only validated materialization steps.

## Prerequisite Artifacts

Required predecessor artifacts:

- Approval provenance from `approve-profile`.
- Approved Topic Team Instantiation Packet or packet/profile input summary.
- Registration assurance from `ensure-topic-registration`, including Project Manifest-backed Research Topic and Topic Workspace refs with no unresolved registration blockers.
- `isomer-topic-summary.md` from `finalize-topic-team`.

If approval provenance is missing, refuse to run, explain that materialization requires explicit approval, and tell the user to run `approve-profile` first.

If registration assurance is missing or blocked, refuse to run, explain that profile materialization needs authoritative Project Manifest-backed topic refs, and tell the user to run `ensure-topic-registration` before materialization.

## Reference Routing

Read first:

- Approved Topic Team Instantiation Packet.
- Topic Workspace path and Domain Agent Team Template source path.

Read as needed:

- Project Manifest registration guidance.
- Validation diagnostics from previous draft or approval passes.

## Exit Criteria

- The bundle exists at `<topic-workspace>/team-profile/`.
- Validation output and provenance files are present.
- The Project Manifest registration guidance is explicit.
- No Agent Team Instance attachment, Workspace Runtime registration, or execution adapter preflight is claimed.

## Guardrails

- Do not write outside the selected Topic Workspace.
- Do not create a second active profile bundle for the same Research Topic.
- Do not attach the profile to an Agent Team Instance, register Workspace Runtime state, or run execution adapter preflight from this subcommand.
