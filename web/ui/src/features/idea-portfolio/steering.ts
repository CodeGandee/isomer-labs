import type { ResearchIdeaSteeringRequest, TopicGraphNode } from "../../types";

export const IDEA_CLOSURE_REASONS = [
  "rejection",
  "supersession",
  "duplication",
  "invalidation",
  "user_closure",
  "legacy_rejection",
  "legacy_supersession",
  "other",
] as const;

export function expectedIdeaStates(nodes: TopicGraphNode[]): Record<string, Record<string, string>> {
  return Object.fromEntries(nodes.filter((node) => node.idea_id).map((node) => [String(node.idea_id), {
    exploration_state: String(node.exploration_state || "unknown"),
    decision_state: String(node.decision_state || "unknown"),
    evidence_state: String(node.evidence_state || "unknown"),
    archive_state: String(node.archive_state || "active"),
    visibility: String(node.visibility || "primary"),
  }]));
}

export function buildSteeringRequest(options: {
  action: "explore" | "explore_instead";
  target: TopicGraphNode;
  replacements: TopicGraphNode[];
  indexRevision?: string | null;
  actorRef: string;
  idempotencyKey: string;
  rationale: string;
  userPrompt: string;
  reopenConfirmed: boolean;
  gatePolicy: "none" | "reopen" | "replace" | "all";
  gateResolutionRef: string;
  dispositions: Record<string, "deferred" | "closed">;
  closureReasons: Record<string, string>;
}): ResearchIdeaSteeringRequest {
  const affected = [options.target, ...options.replacements];
  return {
    action: options.action,
    target_idea_id: String(options.target.idea_id),
    actor_ref: options.actorRef.trim(),
    idempotency_key: options.idempotencyKey,
    expected_index_revision: options.indexRevision || undefined,
    expected_states: expectedIdeaStates(affected),
    replaced_idea_ids: options.action === "explore_instead" ? options.replacements.map((node) => String(node.idea_id)) : [],
    replacement_dispositions: options.action === "explore_instead" ? options.dispositions : {},
    replacement_closure_reasons: options.action === "explore_instead" ? options.closureReasons : {},
    rationale: options.rationale.trim() || undefined,
    user_prompt: options.userPrompt.trim() || undefined,
    reopen_confirmed: options.reopenConfirmed,
    gate_policy: options.gatePolicy,
    gate_resolution_ref: options.gateResolutionRef.trim() || undefined,
    dispatch: true,
  };
}

export function steeringTransitions(action: "explore" | "explore_instead", target: TopicGraphNode, replacements: TopicGraphNode[], dispositions: Record<string, "deferred" | "closed">): string[] {
  const targetLabel = target.display_key || target.idea_id;
  const explorationState = target.exploration_state || "unknown";
  const decisionState = target.decision_state || "unknown";
  const result: string[] = [];
  let effectiveDecisionState = decisionState;
  if (decisionState === "closed" || decisionState === "deferred") {
    result.push(`${targetLabel}: decision ${decisionState} → open`);
    effectiveDecisionState = "open";
  }
  if (action === "explore_instead" && effectiveDecisionState !== "selected") {
    result.push(`${targetLabel}: decision ${effectiveDecisionState} → selected`);
  }
  if (explorationState !== "exploring") {
    result.push(`${targetLabel}: exploration ${explorationState} → exploring`);
  }
  for (const replacement of replacements) {
    result.push(`${replacement.display_key || replacement.idea_id}: decision ${replacement.decision_state || "unknown"} → ${dispositions[String(replacement.idea_id)] || "deferred"}`);
  }
  return result;
}
