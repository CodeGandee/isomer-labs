import { useMutation } from "@tanstack/react-query";
import { useMemo, useState } from "react";
import { steerIdea } from "../../api";
import type { TopicGraphNode } from "../../types";
import { Checkbox } from "@/components/ui/checkbox";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle } from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { StatusBadge, ToolbarButton } from "@/components/workbench-controls";
import { buildSteeringRequest, IDEA_CLOSURE_REASONS, steeringTransitions } from "./steering";

export function IdeaSteeringDialog({ topicId, action, target, replacements, indexRevision, onClose, onAccepted }: { topicId: string; action: "explore" | "explore_instead"; target: TopicGraphNode; replacements: TopicGraphNode[]; indexRevision?: string | null; onClose: () => void; onAccepted: () => void }) {
  const [actorRef, setActorRef] = useState("project-operator:user");
  const [rationale, setRationale] = useState("");
  const [userPrompt, setUserPrompt] = useState("");
  const [reopenConfirmed, setReopenConfirmed] = useState(false);
  const [gatePolicy, setGatePolicy] = useState<"none" | "reopen" | "replace" | "all">("none");
  const [gateResolutionRef, setGateResolutionRef] = useState("");
  const [dispositions, setDispositions] = useState<Record<string, "deferred" | "closed">>(() => Object.fromEntries(replacements.map((node) => [String(node.idea_id), "deferred"])));
  const [closureReasons, setClosureReasons] = useState<Record<string, string>>({});
  const [idempotencyKey] = useState(() => globalThis.crypto?.randomUUID?.() || `steer-${Date.now()}-${Math.random().toString(16).slice(2)}`);
  const transitions = useMemo(() => steeringTransitions(action, target, replacements, dispositions), [action, dispositions, replacements, target]);
  const mutation = useMutation({
    mutationFn: () => steerIdea(topicId, buildSteeringRequest({ action, target, replacements, indexRevision, actorRef, idempotencyKey, rationale, userPrompt, reopenConfirmed, gatePolicy, gateResolutionRef, dispositions, closureReasons })),
    onSuccess: (response) => {
      if (response.status === "accepted") {
        onAccepted();
      }
    },
  });
  const reopeningRequired = target.decision_state === "closed" || target.decision_state === "deferred";
  const missingClosureReason = replacements.some((node) => dispositions[String(node.idea_id)] === "closed" && !closureReasons[String(node.idea_id)]?.trim());
  const submitDisabled = mutation.isPending || !actorRef.trim() || !rationale.trim() || (action === "explore_instead" && !replacements.length) || missingClosureReason || (reopeningRequired && !reopenConfirmed);
  return (
    <Dialog open onOpenChange={(open) => !open && onClose()}>
      <DialogContent className="idea-steering-dialog" showCloseButton={false}>
        <DialogHeader>
          <DialogTitle>{action === "explore" ? "Explore this idea" : "Explore instead"}</DialogTitle>
          <DialogDescription>Confirm the exact canonical state changes before the Project Operator receives the research handoff.</DialogDescription>
        </DialogHeader>
        <section className="idea-steering-targets">
          <h4>Target</h4>
          <p><strong>{target.display_key || target.idea_id} {target.title}</strong></p>
          {action === "explore_instead" ? <h4>Ideas being replaced</h4> : null}
          {replacements.map((node) => (
            <div className="idea-steering-replacement" key={node.idea_id}>
              <span>{node.display_key || node.idea_id} {node.title}</span>
              <select aria-label={`Disposition for ${node.title}`} value={dispositions[String(node.idea_id)] || "deferred"} onChange={(event) => setDispositions((current) => ({ ...current, [String(node.idea_id)]: event.target.value as "deferred" | "closed" }))}>
                <option value="deferred">deferred</option>
                <option value="closed">closed</option>
              </select>
              {dispositions[String(node.idea_id)] === "closed" ? (
                <select aria-label={`Closure reason for ${node.title}`} value={closureReasons[String(node.idea_id)] || ""} onChange={(event) => setClosureReasons((current) => ({ ...current, [String(node.idea_id)]: event.target.value }))}>
                  <option value="">Choose closure reason</option>
                  {IDEA_CLOSURE_REASONS.map((reason) => <option key={reason} value={reason}>{reason}</option>)}
                </select>
              ) : null}
            </div>
          ))}
          <h4>Expected transitions</h4>
          <ul>{transitions.map((transition) => <li key={transition}>{transition}</li>)}</ul>
        </section>
        <label><span>Actor ref</span><Input aria-label="Steering actor ref" value={actorRef} onChange={(event) => setActorRef(event.target.value)} /></label>
        <label><span>Rationale</span><textarea aria-label="Steering rationale" value={rationale} onChange={(event) => setRationale(event.target.value)} /></label>
        <label><span>Research prompt</span><textarea aria-label="Steering research prompt" value={userPrompt} onChange={(event) => setUserPrompt(event.target.value)} /></label>
        {reopeningRequired ? (
          <label className="checkbox">
            <Checkbox checked={reopenConfirmed} onCheckedChange={(checked) => setReopenConfirmed(checked === true)} />
            Confirm reopening {target.decision_state} idea
          </label>
        ) : null}
        <label>
          <span>Gate policy</span>
          <select aria-label="Steering gate policy" value={gatePolicy} onChange={(event) => setGatePolicy(event.target.value as typeof gatePolicy)}>
            <option value="none">No extra Gate</option>
            <option value="reopen">Gate reopening</option>
            <option value="replace">Gate replacement</option>
            <option value="all">Gate all state changes</option>
          </select>
        </label>
        {gatePolicy !== "none" ? <Input aria-label="Gate resolution ref" placeholder="Gate resolution ref (leave blank to request review)" value={gateResolutionRef} onChange={(event) => setGateResolutionRef(event.target.value)} /> : null}
        {mutation.data ? (
          <div className="idea-steering-result" aria-live="polite">
            <StatusBadge tone={mutation.data.status === "accepted" ? "success" : mutation.data.status === "conflict" || mutation.data.status === "gate_required" ? "warning" : "default"}>{mutation.data.status}</StatusBadge>
            {mutation.data.dispatch_status ? <StatusBadge>dispatch {mutation.data.dispatch_status}</StatusBadge> : null}
            {mutation.data.canonical_accepted ? <p>The canonical steering decision and task are durable.</p> : null}
            <SteeringReference label="Decision" value={mutation.data.decision_record_ref} />
            <SteeringReference label="Research Inquiry" value={mutation.data.research_inquiry_ref} />
            <SteeringReference label="Research Task" value={mutation.data.research_task_ref} />
            <SteeringReference label="Handoff" value={mutation.data.handoff_ref} />
            <SteeringReference label="Retry" value={recordString(mutation.data.dispatch, "retry_ref")} />
            {mutation.data.error ? <p>{mutation.data.error.message}</p> : null}
            {mutation.data.status === "conflict" ? <p>The portfolio changed. Close this dialog, review the current ideas, and submit a new confirmation.</p> : null}
            {mutation.data.status === "gate_required" ? <p>A Gate resolution is required before this state change can be accepted.</p> : null}
            {mutation.data.diagnostics.map((diagnostic, index) => <p key={`${diagnostic.code || "diagnostic"}:${index}`}>{diagnostic.message || diagnostic.code}</p>)}
          </div>
        ) : null}
        {mutation.error ? <StatusBadge tone="warning">Steering request failed.</StatusBadge> : null}
        <DialogFooter>
          <ToolbarButton type="button" onClick={onClose}>{mutation.data?.status === "accepted" ? "Done" : "Cancel"}</ToolbarButton>
          <ToolbarButton type="button" disabled={submitDisabled || mutation.data?.status === "accepted"} onClick={() => mutation.mutate()}>{mutation.data?.status === "accepted" ? "Accepted" : "Confirm and route"}</ToolbarButton>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}

function SteeringReference({ label, value }: { label: string; value: string | null | undefined }) {
  return value ? <p><strong>{label}:</strong> {value}</p> : null;
}

function recordString(value: Record<string, unknown> | null | undefined, key: string): string | undefined {
  const item = value?.[key];
  return typeof item === "string" ? item : undefined;
}
