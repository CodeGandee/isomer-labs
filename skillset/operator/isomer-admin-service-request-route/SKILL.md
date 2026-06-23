---
name: isomer-admin-service-request-route
description: Route bounded Service Requests from a Project Operator Session or Operator Agent to topic-scoped Topic Service Agents.
---

# Isomer Service Request Routing

## Workflow

When this skill is invoked, execute the following steps in order.

1. Identify the requester as a Project Operator Session or Operator Agent and identify the selected Research Topic and Topic Workspace.
2. Define the Service Request scope, expected outputs, allowed file surfaces, validation obligations, approval posture, and provenance refs.
3. Select the Topic Service Agent or Topic Service Master that owns the requested support work.
4. Write or dispatch the bounded request using the project's supported Service Request, mailbox, or handoff surface.
5. Record the request ref, target service-agent ref, expected support Artifact refs, and return criteria for the operator.

If the user's task does not map cleanly to these steps, use your native planning tool to build a bounded Service Request from the requested support work, then execute it.

## Reference Routing

Read first:

- The selected Research Topic Config and Effective Topic Context.
- The Topic Service Agent or Topic Service Master profile material when available.

Read as needed:

- `docs/runtime-and-files.md` for runtime and workspace boundaries.
- The selected Domain Agent Team Template workspace contract when the request touches Agent Workspace setup.

## Entry Signals

- The operator needs topic-scoped help with environment readiness, template inspection, placeholder reconciliation, monitoring, diagnostics, or support Artifact writing.
- The task belongs to the Service Team rather than a research team member.

## Exit Criteria

- The Service Request scope and target Topic Service Agent are explicit.
- Expected outputs and validation obligations are listed.
- The operator knows how to detect completion, blocker, or failed service support.

## Guardrails

- Do not give Topic Service Agents authority over Research Claims, Gates, or team membership by default.
- Do not send credentials or live adapter state in the request body.
- Do not bypass generic Isomer validators after service output arrives.
