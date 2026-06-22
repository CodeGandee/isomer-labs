# Workflows

This page describes operator-oriented workflows for the current supported paths through Isomer Labs. Examples prefer read-only commands or dry-run style steps until the guide explicitly enters a mutation section.

## Read-only Inspection

Use this workflow when you want to understand a Project without changing it.

```bash
pixi run isomer-cli --print-json validate
pixi run isomer-cli --print-json doctor
pixi run isomer-cli topics list
pixi run isomer-cli workspaces list
pixi run isomer-cli --print-json context show --topic default
pixi run isomer-cli paths preview --topic default
pixi run isomer-cli schemas list
```

None of these commands mutate Project files, Workspace Runtime records, adapter manifests, or live Houmao state.

## Project Initialization

Use this workflow when you start from an empty directory or want a new Isomer-managed Project.

```bash
pixi install
pixi run isomer-cli init
pixi run isomer-cli --print-json validate
pixi run isomer-cli --print-json doctor
```

`init` mutates the Project filesystem by creating the Project Config Directory, Project Manifest, a Research Topic Config, and a Topic Workspace directory.

## Runtime Preparation

After initialization, create and prepare the Workspace Runtime before creating Agent Team Instances.

```bash
pixi run isomer-cli --print-json runtime init --topic default
pixi run isomer-cli --print-json runtime prepare --topic default
pixi run isomer-cli --print-json runtime validate --topic default --require-ready-readiness
```

`runtime init` creates `state.sqlite` and runtime directories. `runtime prepare` records Topic Environment Readiness. If readiness is not `ready`, treat repair as a Service Request rather than rerunning `runtime prepare`.

## Topic Agent Team Profile Validation

Before launching a team, validate the Domain Agent Team Template and Topic Agent Team Profile.

```bash
pixi run isomer-cli team-templates list
pixi run isomer-cli --print-json team-templates inspect deepsci-org
pixi run isomer-cli team-templates validate deepsci-org
pixi run isomer-cli team-profiles validate .isomer-labs/team-profiles/default-deepsci.toml
```

To derive a candidate profile without writing it:

```bash
pixi run isomer-cli --print-json team-profiles specialize \
  --topic default --profile-id default-deepsci --use-case UC-01
```

Add `--write` to persist the profile to the Project Config Directory. The command reports a `registration_suggestion` object that you can add to the Project Manifest.

## Agent Team Instance Creation

Create a record for a team before launching it. This separates design-time profile work from runtime team state.

```bash
pixi run isomer-cli --print-json team-instances create \
  --topic default \
  --topic-agent-team-profile default-deepsci \
  --id ati-default-deepsci

pixi run isomer-cli team-instances list --topic default
pixi run isomer-cli --print-json team-instances show ati-default-deepsci --topic default
```

This creates Agent Instance records, Agent Workspace records, and directories under `topic-workspaces/default/agents/`. It does not launch Houmao agents.

## Prepare-only Houmao Materialization

Use this workflow when you want to inspect or edit Houmao launch material before invoking Houmao directly.

```bash
pixi run isomer-cli --print-json team-instances launch-material prepare ati-default-deepsci \
  --topic default --adapter houmao
```

This writes `adapter-link.json` and `launch-material-manifest.json` under `topic-workspaces/default/runtime/adapters/houmao/ati-default-deepsci/` and records materialization state. It does not launch agents. The JSON output includes bounded manual guidance for equivalent `houmao-mgr` commands.

After direct Houmao work, use `inspect-live`, `reconcile`, or `adopt` so Isomer can compare manifests, file digests, and read-only Houmao observations.

## Quick Launch

Use this workflow when Isomer should prepare material and launch the Houmao managed agents in one command.

```bash
pixi run isomer-cli --print-json runtime validate --topic default --require-ready-readiness
pixi run isomer-cli --print-json team-instances launch ati-default-deepsci \
  --topic default --adapter houmao
```

Quick launch runs preflight, writes shared launch material, creates or updates adapter manifests, launches one Houmao managed agent per Isomer Agent Instance, writes `adapter-runtime-manifest.json`, and records command runs, payload refs, a launch attempt, and reconciliation state. This mutates live Houmao state.

## Inspect-live

After launch, inspect the adapter and Houmao state without mutation.

```bash
pixi run isomer-cli --print-json team-instances inspect-live ati-default-deepsci \
  --topic default --adapter houmao --integrity
```

`inspect-live` records a bounded inspection snapshot in Workspace Runtime but does not launch or stop agents.

## Stop

Stopping a Houmao-backed Agent Team Instance is an explicit live mutation.

```bash
pixi run isomer-cli --print-json team-instances stop ati-default-deepsci \
  --topic default --adapter houmao
```

`stop` targets known mapped Houmao agent names from manifests or launch attempts and records a stopped, partial, failed, or stale outcome.

## Reconcile

Use reconciliation when you suspect manifest drift, after direct Houmao edits, or after an externally launched team needs to be represented in Workspace Runtime.

```bash
pixi run isomer-cli --print-json team-instances reconcile ati-default-deepsci \
  --topic default
```

`reconcile` records adapter reconciliation diagnostics and writes `adapter-runtime-manifest.json`. It does not start, stop, or message Houmao-managed agents.

## Adopt

Use adoption when you launched Houmao agents outside Isomer and want Workspace Runtime to record the association.

```bash
pixi run isomer-cli --print-json team-instances adopt ati-default-deepsci \
  --topic default --yes
```

`adopt` records an explicit decision to associate externally launched Houmao runtime state with the selected Agent Team Instance. It requires `--yes`.

## Recovery Workflow

When a launch or stop ends in a partial state:

1. Run `isomer-cli runtime validate --topic <topic>` to collect Workspace Runtime diagnostics.
2. Run `isomer-cli team-instances inspect-live <id> --topic <topic> --adapter houmao --integrity` to compare file digests with `launch-material-manifest.json`.
3. Run `isomer-cli team-instances reconcile <id> --topic <topic>` to record the current reconciliation state.
4. If live agents remain and you want to clean up, run `isomer-cli team-instances stop <id> --topic <topic> --adapter houmao`.
5. If you launched agents outside Isomer and want to record them, run `isomer-cli team-instances adopt <id> --topic <topic> --yes`.

See [Troubleshooting](troubleshooting.md) for detailed diagnostics.
