import { describe, expect, it } from "vitest";
import type { TopicGraphNode } from "../../types";
import { buildSteeringRequest, steeringTransitions } from "./steering";

const target = node("target", "unexplored", "closed");
const current = node("current", "exploring", "selected");

describe("idea steering confirmation", () => {
  it("sends exact replacement ids, expected states, and closure reasons", () => {
    const request = buildSteeringRequest({
      action: "explore_instead",
      target,
      replacements: [current],
      indexRevision: "qidx:before",
      actorRef: " actor:user ",
      idempotencyKey: "request-1",
      rationale: " Replace the current route. ",
      userPrompt: "Inspect the target.",
      reopenConfirmed: true,
      gatePolicy: "none",
      gateResolutionRef: "",
      dispositions: { current: "closed" },
      closureReasons: { current: "supersession" },
    });
    expect(request.target_idea_id).toBe("target");
    expect(request.replaced_idea_ids).toEqual(["current"]);
    expect(request.expected_states?.target.decision_state).toBe("closed");
    expect(request.replacement_dispositions).toEqual({ current: "closed" });
    expect(request.replacement_closure_reasons).toEqual({ current: "supersession" });
    expect(request.actor_ref).toBe("actor:user");
  });

  it("previews target and replacement transitions independently", () => {
    expect(steeringTransitions("explore_instead", target, [current], { current: "deferred" })).toEqual([
      "target: decision closed → open",
      "target: decision open → selected",
      "target: exploration unexplored → exploring",
      "current: decision selected → deferred",
    ]);
  });

  it("does not preview a decision change for alongside exploration of a selected idea", () => {
    const selected = node("selected", "unexplored", "selected");
    expect(steeringTransitions("explore", selected, [], {})).toEqual([
      "selected: exploration unexplored → exploring",
    ]);
  });
});

function node(ideaId: string, exploration: string, decision: string): TopicGraphNode {
  return {
    id: `idea:${ideaId}`,
    record_id: `record:${ideaId}`,
    material_kind: "idea",
    density_class: "sparse",
    title: ideaId,
    idea_id: ideaId,
    exploration_state: exploration,
    decision_state: decision,
    evidence_state: "unassessed",
    archive_state: "active",
    visibility: "primary",
  };
}
