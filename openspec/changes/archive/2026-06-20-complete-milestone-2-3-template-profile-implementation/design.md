## Context

Milestone 2 and 3 now have a first pass in the codebase: `team_templates.py` discovers and validates `teams/deepsci-org/execplan/`, `team_profiles.py` derives and validates design-time Topic Agent Team Profiles, the Click CLI exposes `team-templates` and `team-profiles`, and the main specs for template registration and profile specialization are synced. The roadmap, however, still treats Milestone 2 and 3 as unfinished because the implementation relies heavily on in-test generated fixture strings, has limited custom-template negative coverage, and has not yet converted the use-case profile fixtures into durable Project material that future milestones can reuse.

The completion pass should turn the current proof into a stable milestone boundary. Milestone 2 must prove `deepsci-org` is a reusable Domain Agent Team Template, not a running team. Milestone 3 must prove multiple Research Topics can specialize that template into isolated Topic Agent Team Profiles without launching Agent Team Instances, creating Workspace Runtime state, or leaking Houmao launch details into generic Isomer records.

## Goals / Non-Goals

**Goals:**

- Promote UC-01, UC-02, UC-03, and UC-05 Topic Agent Team Profile examples from temporary test strings into repo fixtures that can be validated through public CLI commands.
- Add project-local Domain Agent Team Template fixtures so template validation is not only tested against the built-in `deepsci-org` package.
- Strengthen negative validation around missing template artifacts, concrete template boundary leaks, cross-topic profile refs, duplicate profile ids regardless of status, missing role bindings, fanout omissions, automatic-mode policy omissions, reviewer read-access omissions, runtime truth, launch refs, Houmao refs, and secrets.
- Clarify the side-effect contract for `team-profiles specialize`: preview by default, explicit file write with `--write`, and no implicit Project Manifest mutation.
- Update docs and roadmap checkboxes only after the same validation gate used by contributors passes.

**Non-Goals:**

- Do not launch Houmao managed agents, create launch dossiers, inspect live mailboxes, open gateways, or create Agent Team Instances.
- Do not create Workspace Runtime state, Run records, Agent Workspace directories, View Manifests, Evidence Items, Gates, or Provenance Records.
- Do not introduce a persistent database, execution adapter, service team, or GUI surface.
- Do not rename canonical Isomer domain concepts to Houmao-specific terms.

## Decisions

1. Treat this as a completion and hardening change, not a new architecture. The first pass already established the main module boundaries and CLI shape. This change should harden behavior, add durable fixtures, and close roadmap exit criteria rather than move the system toward launch. Alternative considered: immediately start Milestone 4 Workspace Runtime work. That would blur whether template/profile records are trustworthy before runtime state depends on them.

2. Store reusable fixture Projects under `tests/fixtures/projects/`. Each fixture Project should be readable by the same parser and CLI used for user Projects. The positive fixture should include at least two Research Topics, distinct Topic Workspaces, four use-case profile files, and Project Manifest registrations. Negative fixtures can be smaller and targeted. Document these as contributor/test fixtures rather than stable user examples; defer `docs/examples/` until runtime shape is less fluid. Alternative considered: keep generating profile TOML inside tests. That is fast, but it hides real file layout regressions and does not give future milestones a stable acceptance-test substrate.

3. Keep template fixtures minimal but structurally real. Custom project-local templates should reuse small TOML/JSON fixture packages rather than copying the whole generated `deepsci-org` package. They need enough files to exercise manifest parsing, participant parsing, binding path checks, workspace contract checks, and boundary scanning. Alternative considered: copy `teams/deepsci-org/execplan/` into fixtures. That would make tests slower and brittle while still not proving the generic parser handles smaller templates.

4. Make `team-profiles specialize --write` write only a profile file. It should not silently modify Project Manifest or Research Topic Config because that would turn a preview command into a project-mutating workflow with unclear rollback. The command should return the written path and deterministic registration guidance: text output should include a concise guidance line, and JSON output should include a structured `registration_suggestion` object. A future explicit `--register` or separate registration command can mutate the Project Manifest after we design that operation. Alternative considered: make `--write` auto-register the profile. That is convenient but too surprising for a design-time command.

5. Split fixture validation from temporary negative construction. Positive use-case fixtures should live on disk and be validated through CLI commands. Focused negative tests can still create small temporary Projects when the failure is easier to express directly, such as an injected runtime-truth key or a cross-topic Agent Workspace ref. Alternative considered: store every negative case as a file fixture. That can become noisy and make tests harder to read.

6. Keep `team-templates validate` as the full validation command with harness checks. Lighter validation remains an internal validator choice for `list`, `inspect`, or focused unit tests, not a public `--no-harness` CLI flag. Alternative considered: expose `--no-harness` for fixture speed. That would expose an implementation distinction before user demand is clear.

7. Preserve Houmao as an adapter detail. Validation should reject launch dossiers, mailbox state, gateway state, live managed-agent ids, and adapter launch facts in Topic Agent Team Profile files. It may allow neutral refs such as Capability Binding refs or provider refs when they remain declarative. Alternative considered: allow opaque adapter payloads in profiles. That belongs later in the Houmao Execution Adapter and Agent Team Instance layer, not Milestone 3.

8. Reject duplicate Topic Agent Team Profile ids regardless of registration status. Topic lineage, archival relationships, forks, or migrations should be recorded in a future relationship/history surface rather than by reusing a Project Manifest profile id. Alternative considered: allow inactive duplicate registrations. That creates ambiguous lookup semantics and introduces relationship vocabulary before the relationship model exists.

9. Update roadmap checkboxes as the final implementation step. The roadmap should change only after fixture validation, CLI validation, lint, typecheck, tests, research skill validation, and OpenSpec validation pass. Alternative considered: mark the roadmap first to show intent. The roadmap should reflect verified state, not aspiration.

## Risks / Trade-offs

- Fixture drift from generated `deepsci-org` package → Reuse the live built-in package for the main template validation test and keep custom fixture packages minimal, purpose-built, and documented.
- Validation becomes too strict for future templates → Keep hard-coded `deepsci-org` role expectations limited to built-in `deepsci-org`; custom templates should pass generic structural rules unless they claim the `deepsci-org` id.
- Profile write semantics disappoint users who expect registration → Emit a structured `registration_suggestion` object in JSON plus concise text guidance, and leave manifest mutation to an explicit future command.
- Use-case fixtures become pseudo-runtime records → Keep them in Project Config Directory shape only; do not include Workspace Runtime, Run status, Artifacts, Evidence Items, Gates, mailboxes, gateways, or Agent Team Instance facts.
- Profile lineage needs outlive registration state → Reject duplicate profile ids in Project Manifest and leave archival/fork/migration relationships to a future relationship record.

## Migration Plan

1. Add fixture Project files for positive UC-01, UC-02, UC-03, and UC-05 profiles plus minimal custom-template and negative fixture material.
2. Harden validators and CLI output while keeping existing command names and JSON envelope shape stable.
3. Replace or supplement generated-in-test fixture strings with fixture-file based tests.
4. Run `openspec validate --all`, `pixi run lint`, `pixi run typecheck`, `pixi run test`, and `pixi run validate-research-skills`.
5. Mark ROADMAP Milestone 2 and 3 checkboxes complete after the verification gate passes.

Rollback is straightforward because the change adds fixture files, validation checks, docs, and roadmap state. Removing the new fixtures and stricter checks returns the CLI to the previous first-pass behavior without touching Workspace Runtime or live agent state.

## Resolved Questions

- Profile-write registration guidance SHALL include a structured `registration_suggestion` object in JSON and concise text guidance in text output.
- Fixture Projects SHALL live under `tests/fixtures/projects/` for this milestone; docs may point to them as contributor/test fixtures, but `docs/examples/` is deferred.
- `team-templates validate` SHALL NOT expose a public `--no-harness` flag in this change.
- Duplicate Topic Agent Team Profile ids SHALL be rejected regardless of registration status; topic relationships and history belong in a separate future record.
- ROADMAP Milestone 2 and 3 checklist items SHALL be marked complete after the verification gate passes, while Milestone 4 and later live/runtime work remains incomplete.
