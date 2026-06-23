## 1. Operator Skillset Structure

- [x] 1.1 Create `skillset/operator/` with README documentation for Project Operator Session and Operator Agent skill installation.
- [x] 1.2 Move `isomer-rsch-project-aware` to `skillset/operator/isomer-admin-project-aware`.
- [x] 1.3 Move `isomer-rsch-service-request-route` to `skillset/operator/isomer-admin-service-request-route`.
- [x] 1.4 Move `isomer-rsch-template-inspect` to `skillset/operator/isomer-admin-template-inspect`.
- [x] 1.5 Move `isomer-rsch-topic-context-resolve` to `skillset/operator/isomer-admin-topic-context-resolve`.
- [x] 1.6 Move `isomer-rsch-placeholder-reconcile` to `skillset/operator/isomer-admin-placeholder-reconcile`.
- [x] 1.7 Move `isomer-rsch-topic-profile-draft` to `skillset/operator/isomer-admin-topic-profile-draft`.
- [x] 1.8 Move `isomer-rsch-profile-review-approval` to `skillset/operator/isomer-admin-profile-review-approval`.
- [x] 1.9 Move `isomer-rsch-profile-materialize` to `skillset/operator/isomer-admin-profile-materialize`.
- [x] 1.10 Move `isomer-rsch-team-launch-orchestrate` to `skillset/operator/isomer-admin-team-launch-orchestrate`.

## 2. Service Skill Boundary

- [x] 2.1 Move Topic Service Agent-only support from `isomer-rsch-topic-service-agent-support` to `skillset/service/isomer-srv-topic-service-agent-support`.
- [x] 2.2 Confirm `skillset/service/isomer-srv-env-setup` remains service-scoped and does not depend on operator admin naming.
- [x] 2.3 Update Topic Service Master required skill refs to use `isomer-admin-*` only for true operator-admin capabilities and `isomer-srv-*` for service support capabilities.

## 3. Skill Metadata and Content

- [x] 3.1 Update each moved operator skill's `SKILL.md` frontmatter `name` and in-body self-references to the new `isomer-admin-*` name.
- [x] 3.2 Update each moved operator skill's `agents/openai.yaml` display name and default prompt to the new `isomer-admin-*` name.
- [x] 3.3 Update the moved service skill's frontmatter, manifest, and self-references to its `isomer-srv-*` name.
- [x] 3.4 Review moved skill text so Project Operator Session, Operator Agent, Topic Service Agent, Service Team, Topic Team Specialization, and Agent Team Instance boundaries remain explicit.
- [x] 3.5 Remove old active operator skill folders from `skillset/research-paradigm/`.

## 4. Documentation and References

- [x] 4.1 Update `skillset/README.md` to document `skillset/operator/`, `skillset/research-paradigm/`, and `skillset/service/` naming conventions.
- [x] 4.2 Update `skillset/research-paradigm/README.md` so it lists only research-stage `isomer-rsch-*` skills and points operator/admin work to `skillset/operator/`.
- [x] 4.3 Update active OpenSpec docs, team docs, fixtures, tests, and profile material that reference moved skills by old `isomer-rsch-*` names.
- [x] 4.4 Run `rg` for every old operator skill name and resolve active references, leaving only historical provenance or archived text where appropriate.

## 5. Validation Updates

- [x] 5.1 Extend or add a validation harness for `skillset/operator/` that checks `isomer-admin-*` folder names, frontmatter names, manifests, prompts, and local references.
- [x] 5.2 Extend or add service skill validation for `skillset/service/` naming and local references.
- [x] 5.3 Keep `pixi run validate-research-skills` passing for `skillset/research-paradigm/` after moved operator skills are removed.
- [x] 5.4 Add a repository-level validation command or documented command sequence that validates research, operator, and service skillsets.
- [x] 5.5 Add tests or validation checks that fail on active references to migrated operator skills by old `isomer-rsch-*` names.

## 6. Verification

- [x] 6.1 Run `openspec validate rename-operator-skills-to-isomer-admin --strict`.
- [x] 6.2 Run `openspec validate --all`.
- [x] 6.3 Run the repository skill validation commands for research, operator, and service skillsets.
- [x] 6.4 Run `pixi run lint`.
- [x] 6.5 Run `pixi run typecheck`.
- [x] 6.6 Run `pixi run test`.
- [x] 6.7 Run the UC-01 manual harness or a focused topic-team instantiation smoke test to confirm renamed skill refs do not break packet-backed profile materialization.
- [x] 6.8 Run `git diff --check`.
