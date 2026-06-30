# DeepScientist Quest 006 Storage Inspection

This note inspects the real DeepScientist workflow run at `tmp/deepscientist-home/quests/006`. The purpose is to understand the source system's storage organization before refactoring `isomer-rsch-*` skills and patching Isomer Labs storage support.

## Scope

- Source path inspected: `tmp/deepscientist-home/quests/006`
- Curated preservation snapshot: `../../../extern/orphan/data/deepscientist-run-006-snapshot/`
- Quest id: `006`
- Title: `fa-gb10-2`
- Request: develop a customized FlashAttention implementation for DGX Spark / NVIDIA GB10 based on the official repository.
- Observed final quest state: `quest.yaml` and `.ds/runtime_state.json` both mark the quest as `stopped`, with `stop_reason: user_stop`.
- Observed active anchor: `quest.yaml` says `active_anchor: experiment`; `.ds/research_state.json` records the promoted idea branch `idea/006-idea-97125faf`.

## Size and File Count

The quest root is about 13 GB. Most bytes are not metadata; they are duplicated local build environments and source trees.

| Path | Files | Dirs | Size | Role |
|---|---:|---:|---:|---|
| `.ds` | 3,474 | 568 | 102 MB | DeepScientist runtime state, runner records, tool logs, projections, caches, and worktrees. |
| `.ds/bash_exec` | 3,159 | 526 | 70 MB | Bash session logs, metadata, input queues, and stop requests. |
| `.ds/evidence_packets` | 100 | 3 | 924 KB | Tool-call sidecar packets keyed by run id. |
| `.ds/runs` | 12 | 3 | 12 MB | Runner command records, stdout JSONL, and run artifacts for two Claude/Kimi runs. |
| `.ds/claude_history` | 6 | 3 | 12 MB | Runner transcript history for Claude/Kimi. |
| `.ds/claude-home` | 80 | 18 | 2.6 MB | Quest-local Claude home, MCP config, settings, and session support. |
| `.ds/read_cache` | 85 | 1 | 352 KB | Cached read payloads and payload fingerprints. |
| `.ds/worktrees` | 6 | 8 | 68 KB | Branch worktree support for the promoted idea. |
| `artifacts` | 25 | 13 | 188 KB | Typed, durable DeepScientist research artifacts and artifact index. |
| `baselines` | 32,496 | 2,985 | 6.5 GB | Full official FlashAttention checkout, local Python/CUDA environment, build products, benchmark logs, metric contract, and imported baseline attachment. |
| `experiments` | 32,338 | 2,930 | 6.1 GB | Full experimental FlashAttention fork, local Python/CUDA environment, build products, benchmark/log files, and copied metric contract. |
| `literature` | 8 | 3 | 8.2 MB | Arxiv index and downloaded PDFs. |
| `memory` | 1 | 6 | 40 KB | Long-lived quest memory, mainly active user requirements. |

Top-level small or empty directories include `handoffs`, `paper`, `release`, `tmp`, and `userfiles`. They exist as workflow surfaces but this run did not use them materially.

## Top-Level Layout

```text
quests/006/
  quest.yaml
  brief.md
  plan.md
  status.md
  SUMMARY.md
  artifacts/
  baselines/
  experiments/
  literature/
  memory/
  handoffs/
  paper/
  release/
  tmp/
  userfiles/
  .ds/
  .git/
  .codex/
  .claude/
  .kimi/
  .opencode/
```

DeepScientist stores a quest as a self-contained repository-like directory. It mixes durable research outputs, source checkouts, build environments, runtime state, runner-specific state, and Git history under one quest root.

## Quest Contract Files

`quest.yaml` is the central quest manifest. It records the quest id, title, quest root, status, active anchor, confirmed baseline reference, startup contract, launch form, display hints, default runner, and timestamps. For quest `006`, it records the confirmed baseline as `flash-attention-2.8.3-gb10`, with a local baseline path `baselines/local/flash-attention` and metric contract `baselines/local/flash-attention/json/metric_contract.json`.

`brief.md` repeats the launch contract in prose. It includes the original research request, baseline policy, execution-start policy, research-paper requirement, autonomous decision policy, standard launch mode, and default working rules.

`plan.md` is a hand-maintained research plan. In this run it says the baseline was confirmed, the selected idea is `gb10-native-dispatch`, and the next intended action was to submit the idea and move into implementation.

`SUMMARY.md` is an auto-refreshed summary. It records branch, head commit, recent runs, and recent run summaries.

`status.md` is stale in this run. It still says "Quest created. Waiting for baseline setup or reuse" even though the baseline was confirmed and the quest reached experiment. This is an important source-system caveat: not every human-readable status file is authoritative.

## Runtime Store: `.ds/`

The `.ds/` directory is the DeepScientist runtime store. It is the closest source analogue to Isomer runtime state plus adapter-private material.

Key files:

- `.ds/runtime_state.json`: current runtime status, display status, stop reason, active run id, pending user-message count, continuation policy, last tool activity, last transition, and retry fields. For this run it marks the quest stopped after a user stop.
- `.ds/research_state.json`: research graph cursor state, including active idea id, current workspace branch, current workspace root, idea markdown path, draft path, and last flow type. For this run it points to `idea-97125faf` and `.ds/worktrees/idea-idea-97125faf`.
- `.ds/agent_status.json`: lightweight agent status surface. It stayed near bootstrap defaults in this run.
- `.ds/bindings.json`: source bindings, including the web UI source.
- `.ds/events.jsonl`: runtime event stream.
- `.ds/conversations/main.jsonl`: conversation transcript for the quest.
- `.ds/interaction_journal.jsonl` and `.ds/interaction_state.json`: interaction-level UI/runtime state.
- `.ds/lab_canvas_state.json` and `.ds/projections/*`: derived canvas/detail/git projections for UI views.
- `.ds/node_traces/index.json`: branch and node trace projection. It links branch-node summaries, milestones, idea submission attachment metadata, run ids, and worktree refs.

Important subdirectories:

- `.ds/runs/<run-id>/`: runner launch records. Each run has `command.json` and `stdout.jsonl`; run `run-eaf09ffb` also has `artifact.json`.
- `.ds/claude_history/<run-id>/`: Claude/Kimi runner history for each run.
- `.ds/bash_exec/<bash-id>/`: one directory per command session, with `terminal.log`, `log.jsonl`, `input.jsonl`, `meta.json`, cursor state, monitor logs, and sometimes `stop_request.json`.
- `.ds/evidence_packets/<run-id>/`: sidecar JSON files for tool calls and tool outputs, named by namespace and event id.
- `.ds/read_cache/`: cached payloads for file/tool reads, with payload hashes and source metadata.
- `.ds/cache/`: derived caches such as artifact projection, baseline comparison, and metrics timeline.
- `.ds/worktrees/idea-idea-97125faf/`: branch worktree material for the selected idea, including idea artifacts and idea memory.

This structure is append-heavy and runner-heavy. It is excellent for recovery and UI replay, but too implementation-specific to expose directly in Isomer research skills.

## Runner Records

Quest `006` had two Claude/Kimi runs:

- `run-d6fe6e49`: `turn_reason: user_message`, `turn_mode: stage_execution`.
- `run-eaf09ffb`: `turn_reason: auto_continue`, `turn_mode: monitoring`.

Both command records launch `/home/huangzhe/.bun/bin/claude` with model `kimi-for-coding`, quest-local MCP config `.ds/claude-home/mcp.json`, allowed tools `mcp__memory,mcp__artifact,mcp__bash_exec`, and disallowed direct `Bash`, `WebFetch`, `WebSearch`, and `Task`.

The run records show that DeepScientist keeps runner execution records inside the quest runtime store, not inside durable `artifacts/`. Durable summaries of runs are separately materialized under `artifacts/runs/*.json`.

## Artifact Store

`artifacts/` is the main durable typed output store.

Observed structure:

```text
artifacts/
  _index.jsonl
  baselines/baseline-4821a9e8.json
  graphs/git-graph.{json,png,svg}
  idea/
    CHECKLIST.md
    PLAN.md
    candidates.md
    current_board_packet.md
    limitations.md
    literature_survey.md
    objective_contract.md
    related_work.md
    selected_idea.md
    pre_idea_drafts/
      gb10-native-dispatch.md
      sawtooth-kv-reorder.md
  milestones/milestone-7c078a11.json
  progress/progress-*.json
  runs/run-*.json
  status/method_scoreboard.{json,md}
```

`artifacts/_index.jsonl` is an append-style index of typed artifacts. It contains `artifact_id`, `kind`, `status`, `quest_id`, absolute artifact path, summary, and `updated_at`. In this run it indexed progress artifacts, one completed run summary, one confirmed baseline artifact, one completed milestone, one idea-stage progress artifact, and one failed run summary.

The artifact bodies are mostly plain JSON and Markdown. This is the source-system pattern most relevant to Isomer: typed metadata plus body files, indexed independently of runner logs.

## Baseline Store

`baselines/` stores both baseline registry metadata and the actual baseline source/build tree.

Observed structure:

```text
baselines/
  imported/flash-attention-2.8.3-gb10/attachment.yaml
  local/flash-attention/
    .source_identity.txt
    README.md
    LICENSE
    setup.py
    build.log
    benchmark_results.log
    benchmark_results.json
    usage.md
    json/metric_contract.json
    .venv/
    build/
    flash_attn/
    csrc/
    hopper/
    benchmarks/
    tests/
```

`baselines/imported/.../attachment.yaml` is a quest-local attachment record. It captures baseline id, status `quest_local`, path, summary, primary metric, metric summary, metric contract, metric details, and confirmation metadata.

`baselines/local/flash-attention/.source_identity.txt` records the source identity: commit `a8aa52b`, repo `https://github.com/Dao-AILab/flash-attention.git`, and tag `v2.8.3.post1`.

`baselines/local/flash-attention/json/metric_contract.json` is the main baseline metric contract. It records baseline id `flash-attention-2.8.3-gb10`, primary metric `fwd_tflops_s`, metrics `fwd_tflops_s`, `bwd_tflops_s`, and `fwbw_tflops_s`, all sourced from `baselines/local/flash-attention/benchmark_results.json`.

The baseline directory is large because it includes a full checkout, submodules, a local `.venv`, installed CUDA/PyTorch dependencies, and build outputs. The `.venv` alone is about 5.5 GB.

## Experiment Store

`experiments/` stores the experimental implementation and its execution material.

Observed structure:

```text
experiments/
  analysis/
  main/
  gb10-native-dispatch/
    .source_identity.txt
    README.md
    LICENSE
    setup.py
    build.log
    benchmark_results.log
    benchmark_results.json
    usage.md
    json/metric_contract.json
    .venv/
    build/
    flash_attn/
    csrc/
    hopper/
    benchmarks/
    tests/
```

`experiments/gb10-native-dispatch/` is a full fork/copy of the official FlashAttention source tree used for the selected idea. It also carries `.source_identity.txt` pointing to the same upstream commit and tag as the baseline. It has its own `.venv` and build products, again about 5.5 GB for the environment plus build output.

The experiment metric contract currently duplicates the baseline metric contract and still has kind `baseline_metric_contract` and baseline root `baselines/local/flash-attention`. That suggests DeepScientist copied the baseline contract into the experiment tree before a completed experiment-specific metric contract was recorded.

`experiments/analysis/` and `experiments/main/` exist but were not materially populated in this run.

## Literature Store

`literature/` contains:

```text
literature/
  arxiv/index.json
  arxiv/pdfs/*.pdf
```

The run downloaded seven PDFs and an arxiv index. Literature synthesis lives mainly in `artifacts/idea/literature_survey.md`, `related_work.md`, and selected-idea materials rather than only under `literature/`.

## Memory Store

`memory/knowledge/active-user-requirements.md` records the launch request and long-lived user requirements. The top-level `memory/decisions`, `memory/episodes`, `memory/ideas`, and `memory/papers` directories exist, but this run's submitted idea memory lives under the idea worktree:

```text
.ds/worktrees/idea-idea-97125faf/memory/ideas/idea-97125faf/
  draft.md
  idea.md
```

This means DeepScientist sometimes stores durable-looking research memory under `.ds/worktrees`, not only under top-level `memory/`.

## Git and Branch State

The quest root is a Git repository. At inspection time:

- Current branch: `idea/006-idea-97125faf`.
- Recent commits: `f252591` confirmed baseline and idea artifacts, `4533910` recorded a milestone, and `7a2c566` recorded baseline run `run-eaf09ffb`.
- Git status had modified runtime/projection files and graph artifacts, an untracked `baselines/local/flash-attention` path marker, stop-request files for terminated bash sessions, and `.ds/runs/run-eaf09ffb/artifact.json`.

DeepScientist therefore uses Git as a quest-local branch and checkpoint mechanism, while still keeping large source/build directories and mutable runtime logs inside the same root.

## Observed Status Inconsistencies

The source run demonstrates several consistency hazards:

- `status.md` is stale compared with `quest.yaml`, `SUMMARY.md`, `.ds/runtime_state.json`, and `artifacts/_index.jsonl`.
- `.ds/bash_exec/summary.json` still reports `running_count: 2` and includes many recent sessions with stale `running` status, even though the DeepScientist service and quest processes were stopped later from outside the daemon.
- The experiment metric contract is still a copied baseline metric contract.
- Runtime logs, projections, and graph artifacts can remain dirty after a stop.

For Isomer, this argues for treating typed refs and lifecycle records as authority, while deriving human-readable status files from them rather than letting each file become a competing truth source.

## Storage Pattern Summary

DeepScientist quest storage combines five layers:

1. **Quest contract layer:** `quest.yaml`, `brief.md`, `plan.md`, `SUMMARY.md`, and `status.md`.
2. **Durable research artifact layer:** `artifacts/`, with `_index.jsonl` and typed JSON/Markdown bodies.
3. **Research material layer:** `baselines/`, `experiments/`, `literature/`, and `memory/`, which include source code, logs, benchmark outputs, PDFs, and long-lived requirement memory.
4. **Runtime and replay layer:** `.ds/`, with runner commands, transcripts, tool evidence packets, bash logs, projections, caches, conversations, and worktrees.
5. **Repository/checkpoint layer:** `.git/`, branch names, commits, worktrees, and generated graph artifacts.

The cleanest reusable idea is the typed artifact index plus artifact bodies. The riskiest source pattern is mixing runtime internals, large build products, source checkouts, accepted research evidence, and branch worktrees under one quest root without a strong promotion boundary.

## Implications for Isomer Storage Design

Isomer should not copy the whole quest-root layout. The DeepScientist run is useful as a source-system specimen, but Isomer's topic workspace design should keep accepted topic records separate from agent working directories and adapter-private runtime material.

Recommended Isomer mappings:

| DeepScientist surface | Isomer target |
|---|---|
| `artifacts/_index.jsonl` and typed bodies | Typed records plus `topic.records.artifacts`; keep an index/query API rather than requiring agents to scan JSONL manually. |
| `baselines/imported/*/attachment.yaml` | Baseline Artifact, Evidence Items, Decision Record, Provenance Record, and metric contract records under topic records. |
| `baselines/local/<repo>` | Agent/workspace execution material until promoted; durable source identity, metric contract, logs, and benchmark outputs should be promoted to topic records. |
| `experiments/<experiment-id>` | Topic Main Development Repository or Agent Workspace worktree for code; Run records and Evidence Items for execution outputs. |
| `literature/arxiv/*` | Literature provider-output Artifact profiles and Evidence Items, with provider identity and citation metadata. |
| `memory/knowledge/*` | Durable requirement/context Artifacts or Research Task records, not private runner memory. |
| `.ds/runs`, `.ds/bash_exec`, `.ds/evidence_packets` | Adapter-private runtime plus promoted Run records, command refs, logs, outputs, and provenance refs. |
| `.ds/research_state.json` | Workflow Stage Cursor, Research Inquiry Relationship, current branch/worktree refs, and lifecycle graph records. |
| `.ds/worktrees/*` | Agent Workspace or Topic Main Development Repository worktree; accepted idea records should be promoted out of worktree-local memory. |
| `.git` quest branch state | Isomer repository/worktree state, with durable decisions and evidence stored outside Git-only truth. |

Concrete support this inspection reinforces:

- Isomer needs a typed record API for Artifact, Evidence Item, Decision Record, Gate, Provenance Record, Run, Workflow Stage Cursor, and Research Inquiry Relationship so skills do not recreate DeepScientist's path-scanning behavior.
- Isomer needs promotion from working trees and agent-private outputs into topic records. Baseline and experiment build trees should not automatically become accepted evidence.
- Run storage needs command records, logs, metric contracts, outputs, environment notes, and source identity, but should distinguish adapter-private replay logs from promoted evidence.
- Large environments and build products need a policy. The DeepScientist run duplicated two 5.5 GB virtual environments; Isomer should avoid making these canonical topic records unless explicitly packaged or retained as evidence.
- Human-readable status files should be derived views. The authoritative state should be typed lifecycle records and stable refs.
- Literature provider output needs its own profile or metadata schema. PDFs alone are not enough; the survey and related-work claims need citation, provider, and Evidence Item links.

## Useful Source-System Lessons

- A research workflow needs both file bodies and typed metadata; neither alone is enough.
- A single run can easily create thousands of small runtime files and tens of gigabytes of execution material, so storage labels need retention and promotion semantics.
- Branch/worktree state is helpful for experimental code, but accepted research state needs stable refs that survive branch changes.
- Metric contracts are central. The baseline contract in this run is the most concrete bridge between source code, benchmark outputs, and research decisions.
- Recovery logs are valuable, but skills should not depend on them as the ordinary query path.
