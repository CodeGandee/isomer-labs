# Outline Seeding Example

Use this reference when the idea stage is strong enough that the next serious step will likely become a paper-facing line.

## Goal

Before analysis begins, seed one lightweight but structured outline candidate so later experiments are not free-floating.

## Minimal seed

```json
{
  "title": "Evidence-First Outline Seed",
  "paper_view": {
    "paper_type": "full_empirical",
    "outline_maturity": "idea_seed",
    "working_title": "Evidence-First Outline Seed",
    "narrative_strategy": {
      "central_thesis": "The method should improve the target setting by repairing a specific evidence gap.",
      "central_insight": "The reusable lesson is still tentative and must be tested by the main result and follow-up analyses.",
      "reader_takeaway": "If the idea works, readers should learn when the repair is useful and where it fails."
    },
    "story_spine": {
      "problem": "The current baseline fails in a diagnosable regime.",
      "gap": "Existing evidence is not enough to explain or repair that regime.",
      "method": "A targeted repair is added.",
      "main_result": "To be filled by the main benchmark comparison.",
      "scope_limit": "The claim is limited until ablation and boundary checks are complete."
    },
    "core_claims": [
      {
        "claim_id": "C1",
        "claim": "The method improves the accepted target metric under the planned evaluation.",
        "scope": "Current benchmark, model, and baseline setting.",
        "evidence_needed": ["run-main-001"],
        "what_would_falsify_it": "No gain or a gain that disappears under the accepted comparison contract."
      }
    ],
    "method_abstraction": {
      "intuition": "The method should help because it targets the missing evidence rather than changing unrelated parts of the system.",
      "mechanism_steps": ["Identify the weak regime", "Apply the targeted repair", "Compare under the accepted metric contract"]
    },
    "evaluation_plan": {
      "setting": "Accepted benchmark and baseline comparison",
      "datasets_or_benchmarks": [],
      "baselines": [],
      "metrics": [],
      "controlled_factors": ["same data split", "same metric contract"]
    },
    "analysis_plan": [
      {
        "analysis_id": "A1",
        "title": "Component ablation",
        "analysis_role": "component ablation",
        "reviewer_question": "Is the gain caused by the proposed component?",
        "claim_links": ["C1"],
        "target_display": "Ablation table",
        "main_or_appendix": "main_text",
        "failure_interpretation": "If the gain remains, weaken the mechanism claim."
      }
    ],
    "evidence_grounding": {
      "observed_facts": [],
      "allowed_interpretations": [],
      "must_not_claim": ["Do not claim generality before robustness and boundary checks."],
      "evidence_gaps": ["main benchmark result", "ablation", "boundary analysis"]
    },
    "analysis_budget_waiver": "Idea seed: full 4-8 analysis plan should be expanded after the main result."
  },
  "research_questions": [
    "RQ1: Does the method outperform the accepted baseline?",
    "RQ2: Which component is responsible for the gain?",
    "RQ3: What boundary or failure regime matters most?"
  ],
  "experimental_designs": [
    "Main benchmark comparison",
    "Component ablation",
    "Boundary analysis"
  ],
  "sections": [
    {
      "section_id": "results-main",
      "title": "Main Results",
      "paper_role": "main_text",
      "claims": ["C1"],
      "required_items": ["run-main-001"]
    },
    {
      "section_id": "analysis-mechanism",
      "title": "Mechanism Analysis",
      "paper_role": "main_text",
      "claims": ["C2"],
      "required_items": ["AN-ABL-001"]
    },
    {
      "section_id": "analysis-boundary",
      "title": "Boundary Analysis",
      "paper_role": "appendix",
      "claims": ["C3"],
      "optional_items": ["AN-BND-001"]
    }
  ]
}
```

## When to seed the outline

- The idea already survived literature and feasibility checks.
- The likely paper contribution is clear enough to name `1-3` research questions.
- You can already anticipate the first main experiment and at least one likely follow-up analysis family.

## When not to seed the outline yet

- The task framing is still unstable.
- The idea frontier is still too wide.
- You still cannot say what the main claim would be if the route worked.
