# Workflows

This page describes operator-oriented workflows for the current supported paths through Isomer Labs. Examples prefer read-only commands or dry-run style steps until the guide explicitly enters a mutation section.

## Read-only Inspection

Use this workflow when you want to understand a Project without changing it.

```bash
pixi run isomer-cli --print-json project validate
pixi run isomer-cli --print-json project doctor
pixi run isomer-cli project topics list
pixi run isomer-cli project workspaces list
pixi run isomer-cli --print-json project context show --topic my-topic
pixi run isomer-cli project paths preview --topic my-topic
pixi run isomer-cli schemas list
```

None of these commands mutate Project files, Workspace Runtime records, adapter manifests, or live Houmao state.

## Project Initialization

Use this workflow when you start from an empty directory or want a new Isomer-managed Project.

```bash
pixi install
pixi run isomer-cli project init
pixi run isomer-cli project topics create my-topic --statement "Investigate the concrete research question." --set-default
pixi run isomer-cli --print-json project validate
pixi run isomer-cli --print-json project doctor
```

`project init` mutates the Project filesystem by creating the Isomer-managed Houmao overlay, Project Config Directory, Project Manifest, and selected generated content root. `project topics create` mutates the Project Manifest and Research Topic Configs, and creates the Topic Workspace directory under `isomer-content/topic-ws/<topic-id>/` by default or `<content-dir>/topic-ws/<topic-id>/` after custom content-root init. Neither command creates Workspace Runtime state or live Houmao agents.

```bash
pixi run isomer-cli project init --content-dir custom-content
pixi run isomer-cli project topics create my-topic --statement "Investigate the concrete research question."
```

## Runtime Preparation

After initialization, create and prepare the Workspace Runtime before creating Agent Team Instances.

```bash
pixi run isomer-cli --print-json project runtime init --topic my-topic
pixi run isomer-cli --print-json project runtime prepare --topic my-topic
pixi run isomer-cli --print-json project runtime validate --topic my-topic --require-ready-readiness
```

`project runtime init` creates `state.sqlite` and runtime directories. `project runtime prepare` records Topic Environment Readiness. If readiness is not `ready`, treat repair as a Service Request rather than rerunning `project runtime prepare`.

## Topic Team Specialization and Profile Validation

Before launching a team, validate the Domain Agent Team Template and the Topic Agent Team Profile produced by Topic Team Specialization.

```bash
pixi run isomer-cli project team-templates list
pixi run isomer-cli --print-json project team-templates inspect deepsci-org
pixi run isomer-cli project team-templates validate deepsci-org
pixi run isomer-cli project team-profiles validate isomer-content/topic-ws/my-topic/team-profile/profile.toml
```

To preview Topic Team Specialization without writing it:

```bash
pixi run isomer-cli --print-json project team-profiles specialize \
  --topic my-topic --use-case UC-01
```

Authoritative Topic Team Specialization records a Topic Team Instantiation Packet, persists the profile as the Research Topic's one Topic Agent Team Profile Bundle under the owning Topic Workspace, and records only the Project Manifest ref in Project Config. Preview commands may still report a `registration_suggestion` object for compatibility, but launch-facing profile identity is derived from the Research Topic and fixed `team-profile/` bundle path.

```bash
pixi run isomer-cli --print-json project team-profiles materialize \
  --topic flash-attention-gb10-peak-performance-optimization \
  --packet fixtures/uc01/topic-team-instantiation-packet.toml --write
```

## UC-01 Headless Exploration

Use this workflow to run the pinned UC-01 fixture from Project discovery through follow-up Research Inquiry selection without a GUI renderer. The fixture topic is `flash-attention-gb10-peak-performance-optimization`; the manual harness first materializes a deterministic `deepsci-mini` Topic Agent Team Profile Bundle from the packet fixture, then creates or simulates the Agent Team Instance and stops after recording the follow-up Gate and Decision Record.

```bash
pixi run isomer-cli --print-json project --root tests/fixtures/projects/uc01-headless-gb10 validate
pixi run python tests/manual/uc01_headless_vertical_slice
```

The manual harness copies the fixture Project to a temporary directory, validates it through the generic CLI, then drives reusable runtime, Topic Agent Team Profile, Agent Team Instance, handoff, normalization, and validation APIs. Its default adapter mode is simulated. It writes the same generic UC-01 record graph expected from live mode: Research Inquiry refs, Research Task refs, Run refs, handoff refs, Artifact refs, Evidence Item refs, Finding refs, a resolved follow-up Gate, a Decision Record, View Manifest refs, Provenance refs, adapter payload refs, and adapter command refs. The selected route classification may point to UC-07-style measured optimization, but UC-01 does not run GB10 measurement, baseline benchmark, candidate optimization, automatic replay, correctness checking, or compute-budget Gate work.

Live Houmao validation is explicit and gated:

```bash
ISOMER_MANUAL_LIVE_HOUMAO=1 pixi run python tests/manual/uc01_headless_vertical_slice --live-houmao
```

Without `ISOMER_MANUAL_LIVE_HOUMAO=1`, the harness reports `skipped: true`, `mutated: false` for the live check and does not create Workspace Runtime state or live Houmao state for that live copy.

## Agent Team Instance Creation

Create a record for a team before launching it. This separates design-time profile work from runtime team state.

```bash
pixi run isomer-cli --print-json project team-instances create \
  --topic my-topic \
  --id ati-my-topic-deepsci

pixi run isomer-cli project team-instances list --topic my-topic
pixi run isomer-cli --print-json project team-instances show ati-my-topic-deepsci --topic my-topic
```

This creates Agent Instance records and Agent Workspace records that point at the resolved `agent.workspace` paths prepared earlier by agent environment setup. For Git-backed topics, each Agent Workspace path should already be a worktree of `topic.repos.main` on an agent-owned branch. This command does not create topic-main, create worktrees, verify cwd commands, or launch Houmao agents.

## Prepare-only Houmao Materialization

Use this workflow when you want to inspect or edit Houmao launch material before invoking Houmao directly.

```bash
pixi run isomer-cli --print-json project team-instances launch-material prepare ati-my-topic-deepsci \
  --topic my-topic --adapter houmao
```

This writes `adapter-link.json` and `launch-material-manifest.json` under `isomer-content/topic-ws/my-topic/runtime/adapters/houmao/ati-my-topic-deepsci/` and records materialization state. It does not launch agents. The JSON output includes bounded manual guidance for equivalent `houmao-mgr` commands.

After direct Houmao work, use `inspect-live`, `reconcile`, or `adopt` so Isomer can compare manifests, file digests, and read-only Houmao observations.

## Quick Launch

Use this workflow when Isomer should prepare material and launch the Houmao managed agents in one command.

```bash
pixi run isomer-cli --print-json project runtime validate --topic my-topic --require-ready-readiness
pixi run isomer-cli --print-json project team-instances launch ati-my-topic-deepsci \
  --topic my-topic --adapter houmao
```

Quick launch runs preflight, writes shared launch material, creates or updates adapter manifests, launches one Houmao managed agent per Isomer Agent Instance, writes `adapter-runtime-manifest.json`, and records command runs, payload refs, a launch attempt, and reconciliation state. This mutates live Houmao state.

## Inspect-live

After launch, inspect the adapter and Houmao state without mutation.

```bash
pixi run isomer-cli --print-json project team-instances inspect-live ati-my-topic-deepsci \
  --topic my-topic --adapter houmao --integrity
```

`inspect-live` records a bounded inspection snapshot in Workspace Runtime but does not launch or stop agents.

## Manual Handoff Round

After quick launch, adoption, or another linked Houmao context, dispatch one bounded handoff from the Operator or master Agent Instance to a specialist Agent Instance.

```bash
pixi run isomer-cli --print-json project handoffs dispatch \
  --topic my-topic \
  --agent-team-instance ati-my-topic-deepsci \
  --source-agent-instance ati-my-topic-deepsci-deepsci-org-master \
  --target-agent-instance ati-my-topic-deepsci-deepsci-org-experimenter \
  --run run-default-first-handoff \
  --message "Draft the first experiment execution plan." \
  --expected-output artifact:default:first-handoff
```

Observe adapter output as a Signal Observation. Mail and gateway observations invoke Houmao; file and inspection observations are useful for replay, recovery, and bounded manual validation.

```bash
pixi run isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source mail
pixi run isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source gateway
pixi run isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source file --payload-json handoff-observation.json
pixi run isomer-cli --print-json project handoffs observe <handoff-id> --topic my-topic --source inspection
```

Normalize only after the Operator Agent has reviewed the candidate result. Observations alone do not complete Runs or promote returned claims into Evidence Items.

```bash
pixi run isomer-cli --print-json project handoffs normalize <handoff-id> \
  --topic my-topic \
  --status accepted \
  --signal-observation <signal-observation-id> \
  --output-artifact artifact:default:first-handoff \
  --rationale "Accepted after Operator review."
```

For failed results, use `--status rejected`, `--status blocked`, `--status superseded`, `--status repair_routed`, or `--status follow_up`, and include corrective refs when the next action has a durable Service Request or follow-up handoff.

## Stop

Stopping a Houmao-backed Agent Team Instance is an explicit live mutation.

```bash
pixi run isomer-cli --print-json project team-instances stop ati-my-topic-deepsci \
  --topic my-topic --adapter houmao
```

`stop` targets known mapped Houmao agent names from manifests or launch attempts and records a stopped, partial, failed, or stale outcome.

## Reconcile

Use reconciliation when you suspect manifest drift, after direct Houmao edits, or after an externally launched team needs to be represented in Workspace Runtime.

```bash
pixi run isomer-cli --print-json project team-instances reconcile ati-my-topic-deepsci \
  --topic my-topic
```

`reconcile` records adapter reconciliation diagnostics and writes `adapter-runtime-manifest.json`. It does not start, stop, or message Houmao-managed agents.

## Adopt

Use adoption when you launched Houmao agents outside Isomer and want Workspace Runtime to record the association.

```bash
pixi run isomer-cli --print-json project team-instances adopt ati-my-topic-deepsci \
  --topic my-topic --yes
```

`adopt` records an explicit decision to associate externally launched Houmao runtime state with the selected Agent Team Instance. It requires `--yes`.

## Recovery Workflow

When a launch or stop ends in a partial state:

1. Run `isomer-cli project runtime validate --topic <topic>` to collect Workspace Runtime diagnostics.
2. Run `isomer-cli project team-instances inspect-live <id> --topic <topic> --adapter houmao --integrity` to compare file digests with `launch-material-manifest.json`.
3. Run `isomer-cli project team-instances reconcile <id> --topic <topic>` to record the current reconciliation state.
4. If live agents remain and you want to clean up, run `isomer-cli project team-instances stop <id> --topic <topic> --adapter houmao`.
5. If you launched agents outside Isomer and want to record them, run `isomer-cli project team-instances adopt <id> --topic <topic> --yes`.

See [Troubleshooting](troubleshooting.md) for detailed diagnostics.
