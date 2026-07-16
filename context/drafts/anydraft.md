The current classification model has three main fields:

   Field         Purpose                                         Allowed values
  ━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   family        Conceptual or methodological category           Free-form, such as interpretability, architecture, calibration, or
                                                                 cost-model
  ────────────  ──────────────────────────────────────────────  ───────────────────────────────────────────────────────────────────────
   status        Decision and lifecycle state                    raw, candidate, selected, active, deferred, rejected, supported,
                                                                 refuted, superseded, archived
  ────────────  ──────────────────────────────────────────────  ───────────────────────────────────────────────────────────────────────
   visibility    Whether it belongs in the default Idea Graph    primary, supporting, hidden

  Ideas also carry:

  - display_key: stable UI label such as I-1; not a classification.
  - aliases: source-local labels such as R1 or C3; not stable classifications.
  - generation_id: groups alternatives produced by the same idea-generation pass.
  - lineage_kind: classifies conceptual relationships as derived_from, selected_from, merged_from, follow_up_to, alternative_to, or
    subsumes.

  - metadata: arbitrary structured fields when a domain needs more classification dimensions.

  The important limitation is that family currently has no controlled vocabulary. Agents can assign inconsistent labels such as
  raw_ideas, serious_candidates, interpretability, or nearly anything else. Only status, visibility, and lineage kinds are validated.

  For the Flash Attention topic:

  - Canonical I-1 has family=interpretability, status=selected, and visibility=primary.
  - The legacy records use raw_ideas and serious_candidates as families, but those are payload section names rather than a coherent
    topic taxonomy.

  A better taxonomy for that topic could use stable families such as analytical-model, hardware-mechanism, calibration, execution-path,
  and validation, while leaving maturity and selection decisions in status.

---

The database contains 11 idea rows: 1 canonical idea and 10 legacy facets. The legacy rows include duplicates from two research
  passes.

   Name                                         Summary                                      Kind
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
   Stage-pipeline white-box predictor           Predict runtime as the maximum of Tensor     Legacy facet · serious_candidates
                                                Core, HBM, SFU, and sync stage times;
                                                label the saturating component and
                                                blocking path.
  ───────────────────────────────────────────  ───────────────────────────────────────────  ───────────────────────────────────────────
   Pure roofline predictor                      Runtime = max(FLOPs/TC_peak, bytes/          Legacy facet · raw_ideas
                                                HBM_bw)
  ───────────────────────────────────────────  ───────────────────────────────────────────  ───────────────────────────────────────────
   Stage-pipeline predictor                     Decompose into TMA, MMA, softmax, store      Legacy facet · raw_ideas
                                                and take the slowest stage plus pipeline
                                                overhead.
  ───────────────────────────────────────────  ───────────────────────────────────────────  ───────────────────────────────────────────
   Probabilistic occupancy predictor            Add occupancy, L2 hit-rate, and TMA          Legacy facet · raw_ideas
                                                latency distributions.
  ───────────────────────────────────────────  ───────────────────────────────────────────  ───────────────────────────────────────────
   SASS-critical-path predictor                 Build from disassembled SASS instruction     Legacy facet · raw_ideas
                                                latencies.
  ───────────────────────────────────────────  ───────────────────────────────────────────  ───────────────────────────────────────────
   Pure roofline predictor                      Runtime = max(FLOPs/TC_peak, bytes/          Legacy facet · raw_ideas (second pass)
                                                HBM_bw)
  ───────────────────────────────────────────  ───────────────────────────────────────────  ───────────────────────────────────────────
   Stage-pipeline predictor                     Decompose into TMA, MMA, softmax, store      Legacy facet · raw_ideas (second pass)
                                                and take the slowest stage plus pipeline
                                                overhead.
  ───────────────────────────────────────────  ───────────────────────────────────────────  ───────────────────────────────────────────
   Probabilistic occupancy predictor            Add occupancy, L2 hit-rate, and TMA          Legacy facet · raw_ideas (second pass)
                                                latency distributions.
  ───────────────────────────────────────────  ───────────────────────────────────────────  ───────────────────────────────────────────
   SASS-critical-path predictor                 Build from disassembled SASS instruction     Legacy facet · raw_ideas (second pass)
                                                latencies.
  ───────────────────────────────────────────  ───────────────────────────────────────────  ───────────────────────────────────────────
   Stage-pipeline white-box predictor           Predict runtime as the maximum of Tensor     Legacy facet · serious_candidates (second
                                                Core, HBM, SFU, and sync stage times;        pass)
                                                label the saturating component and
                                                blocking path.
  ───────────────────────────────────────────  ───────────────────────────────────────────  ───────────────────────────────────────────
   SASS-grounded interpretable runtime model    Replace fitted scaling and overhead          Canonical · interpretability · selected/
   for Flash Attention 4                        parameters with values derived               primary
                                                independently from SASS or compiler IR
                                                and targeted microbenchmarks. Map each
                                                dataflow node to an instruction class and
                                                predict the target kernel without
                                                executing it.

  Only the final row is currently eligible for the default canonical Idea Graph. The other ten rows represent four raw candidates and
  one serious candidate repeated across two research passes.

  ---

  our current classification of ideas is not ideal, it does not show what user wants to see in GUI, here is what user wonders when seeing GUI of idea graph:

  - what ideas have been proposed?
  - which ones are explored further?
  - which ones are not yet explored?
  - for the explored ones, which one is derived from which one?
  - which ideas are selected for further development?
  - which ideas are closed or deferred?

  user may want:
  - "I only want to see the ideas that are still open for exploration"
  - "Let me check all the ideas that are derived from a specific idea"
  - "Maybe some closed ideas are still worth looking at, let me see all the closed ideas and why"
  - "Why this idea was selected over the others, let me see all the ideas that were considered and the reasoning behind the selection"
  - "This idea is not good, I want to explore another idea, let me refer to the one I selected and tell the agent to explore it instead of the current one"
