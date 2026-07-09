import { useQuery } from "@tanstack/react-query";
import { ArrowDown, ArrowUp, ArrowUpDown, RefreshCw } from "lucide-react";
import React, { useCallback, useMemo, useRef, useState } from "react";
import { getRecentErrors, getTopicGraph, type GraphFilters } from "../../api";
import { workbenchCommands$ } from "../../events";
import { GraphSummary } from "../graph/GraphPanels";
import { Checkbox } from "@/components/ui/checkbox";
import { Input } from "@/components/ui/input";
import { StatusBadge, ToolbarButton } from "@/components/workbench-controls";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { useGuiSettings } from "../../ui-settings";
import {
  buildIdeaTimelineRows,
  filterIdeaTimelineRows,
  sortIdeaTimelineRows,
  type IdeaTimelineRow,
  type IdeaTimelineSortDirection,
  type IdeaTimelineSortKey,
} from "./idea-timeline";

const ENTRY_COUNTS = ["25", "50", "100", "all"] as const;
type EntryCount = (typeof ENTRY_COUNTS)[number];

const COLUMN_LABELS: Record<IdeaTimelineSortKey, string> = {
  created_at: "Creation Time",
  display_key: "Key",
  title: "Idea Title",
  parents: "Parents",
  status: "Status",
};

export function IdeaTimelinePanel({ topicId }: { topicId: string }) {
  const [filters, setFilters] = useState<GraphFilters>({ includeSecondary: false });
  const [sortKey, setSortKey] = useState<IdeaTimelineSortKey>("created_at");
  const [sortDirection, setSortDirection] = useState<IdeaTimelineSortDirection>("asc");
  const [entryCount, setEntryCount] = useState<EntryCount>("50");
  const [selectedIdeaId, setSelectedIdeaId] = useState<string | null>(null);
  const [selectionWarning, setSelectionWarning] = useState<string | null>(null);
  const lastTapRef = useRef<{ ideaId: string; at: number } | null>(null);
  const { ideaTimelinePrimaryColor, ideaTimelineRowColorsEnabled, ideaTimelineSupportingColor } = useGuiSettings();

  const graph = useQuery({
    queryKey: ["topic", topicId, "graph", "idea-lineage", "timeline"],
    queryFn: () => getTopicGraph(topicId, "idea-lineage", "auto", { includeSecondary: true }),
    enabled: Boolean(topicId),
  });
  const recentErrors = useQuery({
    queryKey: ["topic", topicId, "recent-errors", "idea-timeline"],
    queryFn: () => getRecentErrors(topicId, 10),
    enabled: Boolean(topicId),
  });

  const rows = useMemo(() => {
    const built = graph.data ? buildIdeaTimelineRows(graph.data) : [];
    const filtered = filterIdeaTimelineRows(built, filters);
    return sortIdeaTimelineRows(filtered, sortKey, sortDirection);
  }, [filters, graph.data, sortDirection, sortKey]);
  const visibleRows = useMemo(() => (entryCount === "all" ? rows : rows.slice(0, Number(entryCount))), [entryCount, rows]);

  React.useEffect(() => {
    if (!selectedIdeaId || graph.isLoading) {
      return;
    }
    if (!rows.some((row) => row.ideaId === selectedIdeaId)) {
      setSelectionWarning(`Selection cleared: ${selectedIdeaId} is no longer visible.`);
      setSelectedIdeaId(null);
    }
  }, [graph.isLoading, rows, selectedIdeaId]);

  const onSort = useCallback((nextKey: IdeaTimelineSortKey) => {
    if (nextKey === sortKey) {
      setSortDirection((current) => (current === "asc" ? "desc" : "asc"));
      return;
    }
    setSortKey(nextKey);
    setSortDirection("asc");
  }, [sortKey]);

  const openIdea = useCallback((row: IdeaTimelineRow) => {
    workbenchCommands$.next({ type: "open-idea", topicId, ideaId: row.ideaId });
  }, [topicId]);

  const onRowPointerUp = useCallback((row: IdeaTimelineRow, event: React.PointerEvent<HTMLTableRowElement>) => {
    if (event.pointerType !== "touch") {
      return;
    }
    const now = Date.now();
    const lastTap = lastTapRef.current;
    lastTapRef.current = { ideaId: row.ideaId, at: now };
    if (lastTap?.ideaId === row.ideaId && now - lastTap.at < 420) {
      openIdea(row);
    }
  }, [openIdea]);

  const tableStyle = {
    "--idea-timeline-primary-row": ideaTimelinePrimaryColor,
    "--idea-timeline-supporting-row": ideaTimelineSupportingColor,
  } as React.CSSProperties;

  return (
    <section className="panel-body idea-timeline-panel">
      <div className="idea-timeline-toolbar">
        <TimelineFilters filters={filters} onChange={setFilters} />
        <div className="toolbar">
          <label className="inline-control">
            <span>Rows</span>
            <Select value={entryCount} onValueChange={(value) => setEntryCount(value as EntryCount)}>
              <SelectTrigger aria-label="Timeline Rows" className="rows-select">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {ENTRY_COUNTS.map((count) => (
                  <SelectItem key={count} value={count}>
                    {count === "all" ? "All" : count}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </label>
          <ToolbarButton type="button" onClick={() => void graph.refetch()}>
            <RefreshCw aria-hidden="true" />
            Refresh
          </ToolbarButton>
        </div>
      </div>
      <div className="idea-timeline-table-wrap" style={tableStyle}>
        <Table className={ideaTimelineRowColorsEnabled ? "idea-timeline-table colored-rows" : "idea-timeline-table"}>
          <TableHeader>
            <TableRow>
              <SortableHead column="created_at" sortKey={sortKey} sortDirection={sortDirection} onSort={onSort} />
              <SortableHead column="display_key" sortKey={sortKey} sortDirection={sortDirection} onSort={onSort} />
              <SortableHead column="title" sortKey={sortKey} sortDirection={sortDirection} onSort={onSort} />
              <SortableHead column="parents" sortKey={sortKey} sortDirection={sortDirection} onSort={onSort} />
              <SortableHead column="status" sortKey={sortKey} sortDirection={sortDirection} onSort={onSort} />
            </TableRow>
          </TableHeader>
          <TableBody>
            {visibleRows.map((row) => (
              <TableRow
                key={row.ideaId}
                className={`idea-timeline-row ${row.category} ${selectedIdeaId === row.ideaId ? "selected" : ""}`}
                tabIndex={0}
                onClick={() => {
                  setSelectedIdeaId(row.ideaId);
                  setSelectionWarning(null);
                }}
                onDoubleClick={() => openIdea(row)}
                onPointerUp={(event) => onRowPointerUp(row, event)}
              >
                <TableCell className="mono-cell">{row.createdAt || "unknown"}</TableCell>
                <TableCell className="key-cell">{row.displayKey}</TableCell>
                <TableCell>
                  <div className="timeline-title-cell">
                    <strong>{row.title}</strong>
                    {row.summary ? <span>{row.summary}</span> : null}
                  </div>
                </TableCell>
                <TableCell>{row.parents.length ? row.parents.map((parent) => parent.displayKey).join(", ") : ""}</TableCell>
                <TableCell>{row.status ? <StatusBadge>{row.status}</StatusBadge> : null}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
        {!graph.isLoading && visibleRows.length === 0 ? <div className="empty-state">No ideas match the current filters.</div> : null}
      </div>
      <div className="idea-timeline-footer">
        <GraphSummary graph={graph.data} isLoading={graph.isLoading} />
        <StatusBadge>{visibleRows.length} / {rows.length} rows</StatusBadge>
        {selectedIdeaId ? <StatusBadge tone="info">selected {selectedIdeaId}</StatusBadge> : null}
        {selectionWarning ? <StatusBadge tone="warning">{selectionWarning}</StatusBadge> : null}
        {(graph.data?.diagnostics || []).some((diagnostic) => diagnostic.severity === "warning" || diagnostic.severity === "error") ? <StatusBadge tone="warning">diagnostics available</StatusBadge> : null}
        {(recentErrors.data?.errors || []).length ? <StatusBadge tone="warning">{recentErrors.data?.errors.length} recent errors</StatusBadge> : null}
      </div>
    </section>
  );
}

function TimelineFilters({ filters, onChange }: { filters: GraphFilters; onChange: (filters: GraphFilters) => void }) {
  return (
    <div className="filters idea-timeline-filters">
      <Input
        aria-label="Search timeline"
        placeholder="search ideas"
        value={filters.search || ""}
        onChange={(event) => onChange({ ...filters, search: event.target.value })}
      />
      <label className="checkbox">
        <Checkbox aria-label="Show supporting records" checked={Boolean(filters.includeSecondary)} onCheckedChange={(checked) => onChange({ ...filters, includeSecondary: checked === true })} />
        Supporting Records
      </label>
    </div>
  );
}

function SortableHead({ column, sortKey, sortDirection, onSort }: { column: IdeaTimelineSortKey; sortKey: IdeaTimelineSortKey; sortDirection: IdeaTimelineSortDirection; onSort: (column: IdeaTimelineSortKey) => void }) {
  const active = column === sortKey;
  const Icon = active ? (sortDirection === "asc" ? ArrowUp : ArrowDown) : ArrowUpDown;
  return (
    <TableHead>
      <ToolbarButton type="button" className="table-sort-button" onClick={() => onSort(column)}>
        <Icon aria-hidden="true" />
        {COLUMN_LABELS[column]}
      </ToolbarButton>
    </TableHead>
  );
}
