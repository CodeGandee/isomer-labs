# Paper Outline Template

Use this template when producing a detailed outline Artifact. Field names are implementation-facing labels for the outline, not manuscript prose.

```json
{
  "paper_view": {
    "paper_type": "full_empirical",
    "outline_maturity": "mature",
    "working_title": "Paper-native title",
    "narrative_strategy": {
      "central_thesis": "The one idea the paper wants readers to remember",
      "central_insight": "The reusable lesson suggested by the evidence",
      "reader_takeaway": "What another researcher can learn or reuse"
    },
    "insight_ladder": [
      {
        "level": "Observed fact to interpretation",
        "statement": "What this fact teaches",
        "evidence": ["evidence-item-id"],
        "claim_links": ["C1"],
        "risk": "What could make the interpretation too strong"
      }
    ],
    "story_spine": {
      "problem": "What scientific problem exists",
      "gap": "What prior or easy approach fails to address",
      "method": "What abstract method is introduced",
      "main_result": "What measured result supports the claim",
      "scope_limit": "Where the claim stops"
    },
    "positioning": {
      "closest_neighbor": "The closest existing method, baseline, or obvious alternative",
      "novelty_boundary": "Exactly what is new or reusable here",
      "not_claiming": ["Claims this paper does not make"]
    },
    "core_claims": [
      {
        "claim_id": "C1",
        "claim": "A scoped claim, not a section summary",
        "scope": "Dataset, model, setting, or regime boundary",
        "evidence_needed": ["evidence-item-id", "analysis-id"],
        "what_would_falsify_it": "A result pattern that would weaken the claim"
      }
    ],
    "method_abstraction": {
      "paper_name": "Method name if stable",
      "intuition": "Why the method should work",
      "mechanism_steps": ["Step 1", "Step 2", "Step 3"],
      "appendix_only_details": ["Exact local setup or reproducibility details"]
    },
    "evaluation_plan": {
      "setting": "Scientific evaluation setting",
      "datasets_or_benchmarks": [],
      "baselines": [],
      "metrics": [],
      "controlled_factors": []
    },
    "analysis_plan": [
      {
        "analysis_id": "A1",
        "title": "Component ablation",
        "analysis_role": "component ablation",
        "reviewer_question": "Does the claimed mechanism actually cause the gain",
        "claim_links": ["C1"],
        "target_display": "Main-text ablation table",
        "main_or_appendix": "main_text",
        "failure_interpretation": "How the claim should change if this fails"
      }
    ],
    "reviewer_objections": [
      {
        "objection": "Why a skeptical reviewer might reject or downgrade the paper",
        "answer_route": "analysis | writing | claim_downgrade | limitation",
        "linked_claims": ["C1"],
        "needed_evidence": ["analysis-id"]
      }
    ],
    "evidence_grounding": {
      "observed_facts": ["Facts directly visible in durable results"],
      "allowed_interpretations": ["Careful interpretations allowed by the facts"],
      "must_not_claim": ["Claims the paper must avoid"],
      "evidence_gaps": ["Missing checks or unresolved risks"]
    }
  },
  "evidence_view": {
    "claim_to_items": [],
    "sections": [],
    "unmapped_items": [],
    "appendix_reproducibility": []
  }
}
```

## Template Use

The template is not a requirement to use JSON. It captures the minimum durable ideas a mature outline should contain. A Markdown outline is valid if it preserves the same claims, evidence links, analysis roles, and boundary fields.
