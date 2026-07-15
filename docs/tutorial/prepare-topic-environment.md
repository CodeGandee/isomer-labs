# Prepare Topic Environment

This tutorial shows how to prompt an Isomer-equipped agent to prepare a Topic Workspace after the research intent is clear. The task is to turn the environment gate into verified readiness while keeping external repository commands under user or agent control.

## Starting Point

You have a Research Topic with `intent/src/topic-overview.md` and `intent/src/topic-env-gate.md`. In the running example, the topic needs Python modeling libraries, B200 host facts, `ncu`, and an official FlashAttention source repository.

## Task

Ask the agent to read the topic environment gate, derive the setup plan, install or verify required dependencies, capture host facts, prepare required repositories, and report readiness with blockers. Use the topic-creator or topic environment setup skill as the entrypoint. Treat setup as incomplete until the agent can name what passed, what remains blocked, and what evidence supports each claim.

Repository preparation has four ordered phases:

1. Query or choose a candidate semantic target without binding it.
2. Run the user's supplied command, or select a suitable external Git, provider, copy, or extraction command.
3. Verify the source relationship and observe the immutable commit or content digest outside Isomer.
4. Register the existing directory, then record sanitized provenance and create any approved projections.

## Example Interaction

User Action:

> $isomer-op-topic-creator run-to setup-topic-env

AI:

> Routed from topic creation into topic environment setup.
>
> Read the topic environment gate before mutating the workspace.

User Prompt:

> Now setup topic env.

AI:

> Topic environment setup is complete and verified.
>
> Created the Pixi environment, topic-main guidance files, and derived environment gate.
>
> Verified Python 3.11, NumPy, SymPy, SciPy, Markdown, and `ncu`.
>
> Blockers: none.

User Prompt:

> Verify if you can use `ncu`.

AI:

> `ncu` is available on the B200 host.
>
> Reported the `ncu` version and path.
>
> Ran a tiny profiling smoke test and captured SM, L1, L2, DRAM, and occupancy counters.

User Prompt:

> Use the official FlashAttention repository as the algorithm source. Check out tag `v2.7.4.post1` with Git, verify the exact source and commit, then register it as `topic.repos.sources.flash_attention`. If authentication or checkout fails, stop and report a blocker without registering the path.

AI:

> Planned the unbound candidate for `topic.repos.sources.flash_attention` without creating or registering it.
>
> Ran the requested Git checkout outside Isomer, verified the official source locator and tag relationship, and observed the full immutable commit.
>
> Registered the existing verified directory, recorded sanitized source provenance, and verified its read-only projection.

## External Acquire, Verify, Register, and Record

The following shell sequence makes the boundary concrete. The Git commands are examples, not an Isomer policy. Replace them with the user's exact command or another suitable external method when the source, authentication, history, sparse-checkout, submodule, LFS, or provider requirements differ.

```bash
target="$(isomer-cli --print-json project paths default topic.repos.sources.flash_attention --topic flash-attention-4-whitebox-runtime-model | jq -r '.path.path')"

git clone --branch v2.7.4.post1 https://github.com/Dao-AILab/flash-attention.git "$target"
git -C "$target" remote get-url origin
git -C "$target" rev-parse --verify 'v2.7.4.post1^{commit}'
git -C "$target" rev-parse --verify 'HEAD^{commit}'

isomer-cli --print-json project repos register sources.flash_attention --topic flash-attention-4-whitebox-runtime-model --path "$target"
isomer-cli --print-json project paths get topic.repos.sources.flash_attention --topic flash-attention-4-whitebox-runtime-model --configured
```

The source and immutable-identity checks must succeed before registration. The agent should compare the requested locator with the resolved source, confirm that the selected ref resolves to the checked-out immutable identity, and apply any source-specific verification required by the topic. A local copy or extracted archive may use a content digest instead of a Git commit.

The typed repository provenance records the requested and resolved locators, semantic label, immutable commit or digest, selected external method, sanitized command evidence, verification method, observation time, access and license posture, relationship basis, limitations, and blockers. It omits credentials, signed query strings, headers, environment values, credential-helper output, stdout, stderr, and raw command text that may carry secrets. Kaoju stores successful source relationships in records such as `KAOJU:ASSOCIATED-SOURCE-CODE` and current material state in `KAOJU:ARTIFACT-LIBRARY`.

After registration and provenance recording, topic environment setup can create the approved read-only or writable external projection and update `topic.repos.main.projections.manifest`. Readiness requires the registered semantic label to resolve to the verified directory, the immutable identity to match the recorded evidence, and every required projection to resolve as declared.

## Blocker Handling

If external acquisition or verification fails, do not register the candidate. Preserve only sanitized attempt evidence: requested locator, selected method class, failure stage, filesystem posture, impact, observation time, and a concrete resume condition. The user or agent decides whether to retry, select another source, change credentials, use a provider CLI, use a local copy, or remove or quarantine partial content. Isomer does not clean content created by external commands.

If acquisition succeeds but registration conflicts with an existing binding, leave the acquired directory unchanged and report both paths. Use `project paths update` only when the user explicitly authorizes a topology change. If provenance recording or projection setup fails after registration, keep the valid binding, mark readiness blocked, and resume from the failed record or projection step.

## How to Steer

Ask the agent to show readiness evidence, not optimism. If it says a dependency is ready, ask what command proved it. If a repository appears in the filesystem but not the Topic Workspace Manifest, ask whether source and immutable identity were verified before requesting registration.

Useful steering prompts:

User Action:

> $isomer-srv-topic-env-setup verify-env-gate

User Prompt:

> Read the topic env gate and summarize the runnable target before installing anything.

User Prompt:

> Capture B200 host facts: GPU model, driver, CUDA version, memory, clocks, and `ncu` path.

User Prompt:

> Show the readiness report. Separate verified items, skipped items, and blockers.

User Prompt:

> Show the repository candidate, external method, source check, immutable identity, registration result, provenance ref, and projection status in order.

## Under the Hood

The agent usually routes through `isomer-op-topic-creator` and `isomer-srv-topic-env-setup`. For debugging, the low-level checks look like this:

```bash
isomer-cli --print-json project validate --topic flash-attention-4-whitebox-runtime-model
isomer-cli --print-json project paths list --topic flash-attention-4-whitebox-runtime-model
isomer-cli --print-json project runtime inspect --topic flash-attention-4-whitebox-runtime-model
isomer-cli --print-json project runtime validate --topic flash-attention-4-whitebox-runtime-model --require-ready-readiness
```

The local example records the derived setup plan in `intent/derived/isomer-env-gate.md` and the final readiness summary in `isomer-topic-workspace-summary.md`.

## What Good Looks Like

The Topic Workspace has a verified Pixi environment, recorded host facts, a verified Topic Main Development Repository, registered and provenanced Canonical External Repositories, resolved approved projections, and a readiness summary. The agent can explain which checks passed and which research actions are now safe.

## Common Pitfalls

Do not let the agent silently skip required tools. Do not confuse an externally created source tree with a registered Canonical External Repository. Treat completed source and immutable-identity verification as a prerequisite to binding a candidate. Do not store secrets or raw credential-bearing command output as provenance. Do not let failed setup disappear into later research claims.

## Next Tutorial

Continue to [Run a Human-Steered Research Pass](run-a-human-steered-research-pass.md).

## Links

- [FlashAttention-4 analytical model example](https://github.com/CodeGandee/isomer-example-fa4-analytical-model)
