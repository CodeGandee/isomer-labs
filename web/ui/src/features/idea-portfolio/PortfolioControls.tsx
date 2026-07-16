import { IDEA_FACET_OPTIONS, IDEA_PORTFOLIO_PRESETS, type IdeaPortfolioViewState, visiblePortfolioCount } from "./idea-portfolio";
import type { TopicGraphView } from "../../types";
import { ToolbarButton } from "@/components/workbench-controls";

export function PortfolioControls({ graph, state, onChange }: { graph: TopicGraphView | undefined; state: IdeaPortfolioViewState; onChange: (state: IdeaPortfolioViewState) => void }) {
  const counts = visiblePortfolioCount(graph);
  const selectedPreset = IDEA_PORTFOLIO_PRESETS.find((preset) => preset.id === state.preset) || IDEA_PORTFOLIO_PRESETS[0];
  return (
    <section className="idea-portfolio-controls" aria-label="Idea portfolio filters">
      <label>
        <span>Portfolio</span>
        <select aria-label="Idea portfolio preset" value={state.preset} onChange={(event) => onChange({ ...state, preset: event.target.value as IdeaPortfolioViewState["preset"] })}>
          {IDEA_PORTFOLIO_PRESETS.map((preset) => <option key={preset.id} value={preset.id}>{preset.label}</option>)}
        </select>
      </label>
      <FacetSelect label="Exploration" value={state.explorationState} options={IDEA_FACET_OPTIONS.explorationState} onChange={(value) => onChange({ ...state, explorationState: value })} />
      <FacetSelect label="Decision" value={state.decisionState} options={IDEA_FACET_OPTIONS.decisionState} onChange={(value) => onChange({ ...state, decisionState: value })} />
      <FacetSelect label="Evidence" value={state.evidenceState} options={IDEA_FACET_OPTIONS.evidenceState} onChange={(value) => onChange({ ...state, evidenceState: value })} />
      <FacetSelect label="Archive" value={state.archiveState} options={IDEA_FACET_OPTIONS.archiveState} onChange={(value) => onChange({ ...state, archiveState: value })} />
      <FacetSelect label="Visibility" value={state.visibility} options={IDEA_FACET_OPTIONS.visibility} onChange={(value) => onChange({ ...state, visibility: value })} />
      <span className="idea-portfolio-count" aria-live="polite">{counts.visible} visible / {counts.source} source</span>
      <ToolbarButton type="button" onClick={() => onChange({ preset: "current" })}>Reset</ToolbarButton>
      <p className="idea-portfolio-predicate">{selectedPreset.description}</p>
      {state.preset === "needs-classification" ? <span className="idea-portfolio-warning">Unknown exploration, decision, or evidence state</span> : null}
      {graph?.topology_complete === false ? <span className="idea-portfolio-warning">Source is incomplete; refine filters or refresh with a larger bound.</span> : null}
    </section>
  );
}

function FacetSelect({ label, value, options, onChange }: { label: string; value: string | undefined; options: readonly string[]; onChange: (value: string | undefined) => void }) {
  return (
    <label>
      <span>{label}</span>
      <select aria-label={`${label} state`} value={value || ""} onChange={(event) => onChange(event.target.value || undefined)}>
        <option value="">Any</option>
        {options.map((option) => <option key={option} value={option}>{option}</option>)}
      </select>
    </label>
  );
}
