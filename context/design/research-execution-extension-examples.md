# Research Execution Extension Examples

This note gives concise TOML examples for the provider-neutral Research Execution and Extension Contract. The examples show refs and expected shapes only; they do not define provider-specific command bodies, credentials, scheduler internals, command outputs, provider payloads, or runtime truth.

## Research Topic Config Example

Research Topic Config carries topic-level defaults and selected extension refs for one Research Topic.

```toml
schema_version = "0.1"
research_topic_id = "kernel-a-vs-b"

topic_statement = "Why is CUDA kernel A faster than kernel B?"
topic_statement_artifact_refs = ["artifact:topic-brief"]
measurable_objectives = [
  "Identify the dominant performance cause",
  "Validate the explanation with profiling evidence",
]

default_topic_agent_team_profile = "topic-profile:cuda-kernel-investigation"
default_execution_adapter = "execution-adapter:topic-default"
default_control_mode = "manual"

[defaults]
research_inquiry_id = "compute-utilization"
artifact_tracking = "selective"

[operation_extension_refs]
command_execution = "operation-extension:topic-command"
repository_inspection = "operation-extension:topic-repository-readonly"
package_management = "operation-extension:topic-package-management"
hpc_job = "operation-extension:topic-hpc-job"
figure_render = "operation-extension:topic-figure-render"
literature_search = "operation-extension:literature-search"
baseline_waiver = "operation-extension:baseline-waiver"
cost_privacy_gate = "operation-extension:cost-privacy-gate"
service_request = "operation-extension:service-request"
agent_launch = "operation-extension:agent-launch"

[capability_binding_refs]
default = "capability:topic-defaults"
experimenter = "capability:cuda-experimenter"
analyst = "capability:cuda-analyst"

[skill_binding_projection_refs]
default = "skill-binding:research-defaults"
experimenter = "skill-binding:cuda-experimenter"

[policy_refs]
scheduler = "scheduler-policy:manual-first"
cost_privacy_gate = "gate-policy:local-safe"
baseline_waiver = "baseline-waiver-policy:active-baseline-required"

[provider_binding_refs]
literature = "provider-binding:project-literature"

[artifact_format_defaults]
experiment_result = "artifact-format:cuda-kernel-profile"
analysis_report = "artifact-format:cuda-analysis-report"
literature_provider_result = "artifact-format:literature-search-batch"

[artifact_extensions]
enabled = ["artifact-extension:cuda-kernel-metadata"]
```

## Topic Agent Team Profile Example

Topic Agent Team Profile carries topic-specialized role, Workflow Stage, Capability Binding, Skill Binding projection, and policy availability. It does not become a running Agent Team Instance.

```toml
schema_version = "0.1"
id = "cuda-kernel-investigation"
research_topic_id = "kernel-a-vs-b"
domain_agent_team_template = "domain-team-template:ml-systems-research"

[coordination]
policy_ref = "coordination-policy:operator-mediated"
default_scheduler_policy_ref = "scheduler-policy:manual-first"

[[roles]]
id = "experimenter"
agent_profile_ref = "agent-profile:topic-experimenter"
capability_binding_refs = ["capability:cuda-experimenter"]
skill_binding_projection_ref = "skill-binding:cuda-experimenter"
allowed_operation_extension_refs = [
  "operation-extension:topic-command",
  "operation-extension:topic-package-management",
  "operation-extension:topic-hpc-job",
]

[[roles]]
id = "analyst"
agent_profile_ref = "agent-profile:topic-analyst"
capability_binding_refs = ["capability:cuda-analyst"]
skill_binding_projection_ref = "skill-binding:analysis-defaults"
allowed_operation_extension_refs = [
  "operation-extension:topic-repository-readonly",
  "operation-extension:topic-figure-render",
]

[[workflow_stages]]
id = "profile-kernels"
owner_role = "experimenter"
expected_artifact_kinds = ["experiment_plan", "experiment_result", "run_log"]
operation_extension_refs = ["operation-extension:topic-command", "operation-extension:topic-hpc-job"]
gate_policy_refs = ["gate-policy:local-safe"]

[[workflow_stages]]
id = "explain-performance"
owner_role = "analyst"
expected_artifact_kinds = ["analysis_report", "finding"]
operation_extension_refs = ["operation-extension:topic-repository-readonly", "operation-extension:topic-figure-render"]
gate_policy_refs = ["gate-policy:publication-facing-output"]
```

## Recording Notes

An Execution Adapter Command Request that consumes these refs stores selected refs, source metadata, expected inputs and outputs, expected Artifact kinds, Gate policy refs, scheduler policy refs, and Provenance obligations. Provider-specific command text, queue parameters, API payloads, credentials, live process ids, and command outputs stay in adapter-owned payload refs, credential backends, Workspace Runtime records, Artifacts, or Provenance Records according to the accepted specs.
