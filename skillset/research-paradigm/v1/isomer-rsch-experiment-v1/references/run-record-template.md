# Run Record

Use this template when creating or reviewing a durable Run record.

## Template

```md
# Run Record: <run_id>

## Identity

- run_id:
- Research Task:
- Research Inquiry Relationship:
- selected_route:
- comparator_reference:
- metric_contract:
- experiment_tier: auxiliary/dev or main/test

## Research Question

- question:
- null_hypothesis:
- alternative_hypothesis:
- strongest_alternative_hypothesis:

## Setup

- dataset_or_split:
- code_or_config_deltas:
- keep_unchanged_contract:
- seeds:
- environment_snapshot:
- resource_constraints:

## Execution

- Capability Binding:
- Execution Adapter:
- commands_or_adapter_calls:
- start_time:
- end_time:
- status:
- log_artifacts:
- output_artifacts:

## Results

- metric_rows:
- required_metric_keys_present:
- finite_metric_check:
- comparator_relation: better / worse / mixed / not_comparable
- comparability: high / medium / low

## Claim Validation

- Research Claim:
- metric_key:
- expected_direction:
- observed_result:
- verdict: supported / refuted / inconclusive
- caveats:

## Failure or Blocker

- failure_mode: none / implementation / evaluation / environment / direction / data_contract_mismatch / resource_exhausted / numeric_instability / external_dependency_blocked
- failure_layer:
- retry_or_route_rationale:

## Evaluation Summary

- takeaway:
- claim_update: strengthens / weakens / narrows / neutral
- comparator_relation:
- comparability:
- failure_mode:
- next_action:

## Provenance

- input Artifacts:
- generated Artifacts:
- Evidence Items:
- Provenance Records:
- unresolved TBD surfaces:
```

## Quality Rule

A Run record should make it easy for a later stage to answer what changed, how the Run can be reconstructed, what the result means, why it worked or failed, and what should happen next.
