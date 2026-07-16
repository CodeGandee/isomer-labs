import type { IdeaDecisionContextResponse } from "../../types";
import { StatusBadge, ToolbarButton } from "@/components/workbench-controls";

export function IdeaDecisionContextPanel({ response, isLoading, error, onClose }: { response: IdeaDecisionContextResponse | undefined; isLoading: boolean; error: unknown; onClose: () => void }) {
  return (
    <aside className="idea-decision-context" aria-label="Idea decision history">
      <header>
        <div>
          <h3>Decision comparison and history</h3>
          <p>Recorded alternatives and reasoning only. Missing context remains explicit.</p>
        </div>
        <ToolbarButton type="button" onClick={onClose}>Close</ToolbarButton>
      </header>
      {isLoading ? <p>Loading decision context.</p> : null}
      {error ? <StatusBadge tone="warning">Decision context failed to load.</StatusBadge> : null}
      {response?.error ? <StatusBadge tone="warning">{response.error.message}</StatusBadge> : null}
      {response?.decisions.map((decision, index) => {
        const options = arrayOfRecords(decision.options);
        return (
          <section className="idea-decision-card" key={stringValue(decision.decision_record_id) || index}>
            <h4>{stringValue(decision.title) || stringValue(decision.decision_record_id) || `Decision ${index + 1}`}</h4>
            <DecisionFact label="Rationale" value={decision.rationale} />
            <DecisionFact label="Consequence" value={decision.consequence} />
            <DecisionFact label="Actor" value={decision.actor_ref} />
            <ReferenceList label="Consequences" value={decision.consequences} />
            <ReferenceList label="Actors" value={decision.actor_refs} />
            <DecisionFact label="Recorded" value={decision.decided_at || decision.created_at} />
            <StatusBadge tone={decision.option_set_complete === false ? "warning" : "info"}>
              {decision.option_set_complete === false ? "partial option set" : `${options.length} recorded options`}
            </StatusBadge>
            <div className="idea-decision-options">
              {options.map((option, optionIndex) => {
                const idea = recordValue(option.idea);
                const displayKey = stringValue(option.display_key) || stringValue(idea.display_key);
                const title = stringValue(option.title) || stringValue(idea.title) || stringValue(option.idea_id) || "Unknown option";
                return (
                  <article key={stringValue(option.idea_id) || optionIndex}>
                    <strong>{displayKey ? `${displayKey} ` : ""}{title}</strong>
                    <StatusBadge tone={stringValue(option.outcome) === "selected" ? "success" : "default"}>{stringValue(option.outcome) || "outcome unknown"}</StatusBadge>
                    <DecisionFact label="Rationale" value={option.rationale || option.transition_rationale} />
                    <DecisionFact label="Consequence" value={option.consequence} />
                    <DecisionFact label="Closure / deferral" value={option.reason_code || option.closure_reason} />
                    <DecisionFact label="Transition" value={option.transition_ref} />
                    <ReferenceList label="Evidence and result refs" value={option.supporting_refs || option.terminal_result_refs} />
                  </article>
                );
              })}
              {!options.length ? <p>No option membership was recorded for this historical decision.</p> : null}
            </div>
            <ReferenceList label="Supporting refs" value={decision.supporting_refs || decision.terminal_result_refs} />
          </section>
        );
      })}
      {response && !response.decisions.length ? <p>No Decision Record is linked to this idea.</p> : null}
      {response?.reopen_history?.length ? (
        <section className="idea-reopen-history">
          <h4>Reopen history</h4>
          <ul>
            {response.reopen_history.map((transition, index) => (
              <li key={stringValue(transition.id) || index}>
                {stringValue(transition.previous_value)} → {stringValue(transition.next_value)}
                {stringValue(transition.rationale) ? `: ${stringValue(transition.rationale)}` : ""}
              </li>
            ))}
          </ul>
        </section>
      ) : null}
      {(response?.diagnostics || []).map((diagnostic, index) => (
        <StatusBadge key={`${diagnostic.code || "diagnostic"}:${index}`} tone={diagnostic.severity === "error" || diagnostic.severity === "warning" ? "warning" : "default"}>
          {diagnostic.message || diagnostic.code || "Decision diagnostic"}
        </StatusBadge>
      ))}
    </aside>
  );
}

function DecisionFact({ label, value }: { label: string; value: unknown }) {
  const text = stringValue(value);
  return text ? <p><strong>{label}:</strong> {text}</p> : null;
}

function ReferenceList({ label, value }: { label: string; value: unknown }) {
  const refs = Array.isArray(value) ? value.map(String).filter(Boolean) : [];
  return refs.length ? <p><strong>{label}:</strong> {refs.join(", ")}</p> : null;
}

function arrayOfRecords(value: unknown): Array<Record<string, unknown>> {
  return Array.isArray(value) ? value.filter((item): item is Record<string, unknown> => Boolean(item) && typeof item === "object") : [];
}

function recordValue(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {};
}

function stringValue(value: unknown): string {
  return typeof value === "string" || typeof value === "number" ? String(value) : "";
}
