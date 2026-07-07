import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { StatusBadge } from "@/components/workbench-controls";
import type { GraphFilters } from "../../api";
import type { TopicGraphView } from "../../types";

export function GraphFiltersBar({ filters, onChange }: { filters: GraphFilters; onChange: (filters: GraphFilters) => void }) {
  return (
    <div className="filters">
      <Input aria-label="Search graph" placeholder="search" value={filters.search || ""} onChange={(event) => onChange({ ...filters, search: event.target.value })} />
      <Input aria-label="Status filter" placeholder="status" value={filters.status || ""} onChange={(event) => onChange({ ...filters, status: event.target.value })} />
      <Input aria-label="Relation filter" placeholder="relation" value={filters.relationKind || ""} onChange={(event) => onChange({ ...filters, relationKind: event.target.value })} />
      <label className="checkbox">
        <Checkbox aria-label="Show supporting records" checked={Boolean(filters.includeSecondary)} onCheckedChange={(checked) => onChange({ ...filters, includeSecondary: checked === true })} />
        Supporting Records
      </label>
    </div>
  );
}

export function GraphSummary({ graph, isLoading }: { graph?: TopicGraphView; isLoading: boolean }) {
  if (isLoading) {
    return <div className="status-line">Loading.</div>;
  }
  if (!graph) {
    return <div className="status-line">No graph data.</div>;
  }
  return (
    <div className="graph-summary">
      <StatusBadge>{graph.nodes.length} nodes</StatusBadge>
      <StatusBadge>{graph.edges.length} edges</StatusBadge>
      <StatusBadge>{graph.renderer_hint}</StatusBadge>
      {graph.paging?.truncated ? <StatusBadge tone="warning">truncated</StatusBadge> : null}
      {graph.error ? <StatusBadge tone="danger">{graph.error.code}</StatusBadge> : null}
    </div>
  );
}
