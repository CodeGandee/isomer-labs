import type { GraphFilters } from "../../api";
import type { TopicGraphEdge, TopicGraphNode, TopicGraphView } from "../../types";

export type IdeaTimelineSortKey = "created_at" | "display_key" | "title" | "parents" | "status";
export type IdeaTimelineSortDirection = "asc" | "desc";

export type IdeaTimelineParent = {
  ideaId: string;
  displayKey: string;
  title: string;
};

export type IdeaTimelineRow = {
  ideaId: string;
  nodeId: string;
  displayKey: string;
  title: string;
  summary: string;
  family: string;
  status: string;
  visibility: string;
  createdAt: string;
  updatedAt: string;
  aliases: string[];
  parents: IdeaTimelineParent[];
  relationKinds: string[];
  category: "primary" | "supporting";
};

export function buildIdeaTimelineRows(graph: TopicGraphView): IdeaTimelineRow[] {
  const nodeById = new Map(graph.nodes.map((node) => [node.id, node]));
  const parentEdges = new Map<string, TopicGraphEdge[]>();
  for (const edge of graph.edges) {
    parentEdges.set(edge.target, [...(parentEdges.get(edge.target) || []), edge]);
  }
  return graph.nodes
    .filter((node) => node.material_kind === "idea" && node.idea_id && node.visibility !== "hidden")
    .map((node) => {
      const parents = (parentEdges.get(node.id) || [])
        .map((edge) => parentFromEdge(edge, nodeById))
        .filter((parent): parent is IdeaTimelineParent => parent !== null)
        .sort((left, right) => left.displayKey.localeCompare(right.displayKey) || left.ideaId.localeCompare(right.ideaId));
      const source = node.source || {};
      return {
        ideaId: String(node.idea_id),
        nodeId: node.id,
        displayKey: String(node.display_key || source.display_key || node.idea_id),
        title: node.title || String(node.idea_id),
        summary: String(node.summary || ""),
        family: String(source.family || node.renderer_hints?.cluster || ""),
        status: String(node.status || ""),
        visibility: String(node.visibility || "primary"),
        createdAt: String(node.created_at || ""),
        updatedAt: String(node.updated_at || ""),
        aliases: Array.isArray(source.aliases) ? source.aliases.map(String) : [],
        parents,
        relationKinds: (parentEdges.get(node.id) || []).map((edge) => edge.lineage_kind || edge.relation_kind).filter(Boolean).map(String),
        category: node.visibility === "primary" || !node.visibility ? "primary" : "supporting",
      };
    });
}

export function filterIdeaTimelineRows(rows: IdeaTimelineRow[], filters: GraphFilters): IdeaTimelineRow[] {
  const search = normalizeSearch(filters.search || "");
  return rows.filter((row) => {
    if (search && !matchesTimelineSearch(row, search)) {
      return false;
    }
    return filters.includeSecondary || row.category === "primary";
  });
}

export function sortIdeaTimelineRows(rows: IdeaTimelineRow[], sortKey: IdeaTimelineSortKey, direction: IdeaTimelineSortDirection): IdeaTimelineRow[] {
  const multiplier = direction === "asc" ? 1 : -1;
  return [...rows]
    .map((row, index) => ({ row, index }))
    .sort((left, right) => {
      const primary = compareSortValue(sortValue(left.row, sortKey), sortValue(right.row, sortKey));
      if (primary !== 0) {
        return primary * multiplier;
      }
      return fallbackCompare(left.row, right.row) || left.index - right.index;
    })
    .map((item) => item.row);
}

function parentFromEdge(edge: TopicGraphEdge, nodeById: Map<string, TopicGraphNode>): IdeaTimelineParent | null {
  const node = nodeById.get(edge.source);
  if (!node || !node.idea_id) {
    return null;
  }
  return {
    ideaId: String(node.idea_id),
    displayKey: String(node.display_key || node.source?.display_key || node.idea_id),
    title: node.title || String(node.idea_id),
  };
}

function sortValue(row: IdeaTimelineRow, sortKey: IdeaTimelineSortKey): string {
  if (sortKey === "created_at") {
    return row.createdAt;
  }
  if (sortKey === "display_key") {
    return row.displayKey;
  }
  if (sortKey === "parents") {
    return row.parents.map((parent) => parent.displayKey || parent.ideaId).join(" ");
  }
  if (sortKey === "status") {
    return row.status;
  }
  return row.title;
}

function compareSortValue(left: string, right: string): number {
  return left.localeCompare(right, undefined, { numeric: true, sensitivity: "base" });
}

function fallbackCompare(left: IdeaTimelineRow, right: IdeaTimelineRow): number {
  return (
    compareSortValue(left.createdAt, right.createdAt) ||
    compareSortValue(left.updatedAt, right.updatedAt) ||
    compareSortValue(left.title, right.title) ||
    compareSortValue(left.ideaId, right.ideaId)
  );
}

function matchesTimelineSearch(row: IdeaTimelineRow, normalizedQuery: string): boolean {
  const fields = [
    row.createdAt,
    row.displayKey,
    row.title,
    row.summary,
    row.family,
    row.status,
    row.visibility,
    row.category,
    row.ideaId,
    row.updatedAt,
    ...row.aliases,
    ...row.relationKinds,
    ...row.parents.flatMap((parent) => [parent.displayKey, parent.title, parent.ideaId]),
  ];
  const haystack = normalizeSearch(fields.join(" "));
  return normalizedQuery.split(" ").filter(Boolean).every((token) => fuzzyIncludes(haystack, token));
}

function normalizeSearch(value: string): string {
  return value.toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function fuzzyIncludes(haystack: string, needle: string): boolean {
  if (!needle) {
    return true;
  }
  if (haystack.includes(needle)) {
    return true;
  }
  let position = 0;
  for (const char of haystack) {
    if (char === needle[position]) {
      position += 1;
      if (position === needle.length) {
        return true;
      }
    }
  }
  return false;
}
