import { QueryClient, QueryClientProvider, useQuery, useQueryClient } from "@tanstack/react-query";
import { createRootRoute, createRouter, RouterProvider } from "@tanstack/react-router";
import { createColumnHelper, flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import { Background, Controls, ReactFlow, ReactFlowProvider, useReactFlow, type Edge, type Node } from "@xyflow/react";
import { DockviewReact, type DockviewReadyEvent, type IDockviewPanelProps } from "dockview-react";
import Graphology from "graphology";
import mermaid from "mermaid";
import React, { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import ReactMarkdown from "react-markdown";
import rehypeKatex from "rehype-katex";
import remarkGfm from "remark-gfm";
import remarkMath from "remark-math";
import Sigma from "sigma";
import { Subscription } from "rxjs";
import { getProject, getRecordDetail, getRecordFacets, getRecordFiles, getRecordLineage, getRecordRender, getRecordSiblings, getRecords, getTopicGraph, getTopics, getViewerDescriptor, type GraphFilters } from "./api";
import { layoutFlowGraph, requestedRenderer, selectRenderer, toFlowEdges, toFlowNodes } from "./graph-utils";
import { manualRefresh$, topicInvalidations, workbenchCommands$ } from "./events";
import type { GraphScope, RecordSummary, Topic, TopicGraphView } from "./types";
import { filterRecords, viewerSurface } from "./view-model";
import "dockview/dist/styles/dockview.css";
import "@xyflow/react/dist/style.css";
import "katex/dist/katex.min.css";
import "./styles.css";

type SearchState = {
  topicId?: string;
  graphScope: GraphScope;
};

type PanelParams = {
  topicId: string;
  graphScope?: GraphScope;
  recordId?: string;
};

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5000,
      refetchOnWindowFocus: false,
    },
  },
});

const rootRoute = createRootRoute({
  component: Workbench,
});

const router = createRouter({ routeTree: rootRoute });

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router;
  }
}

export function RootApp() {
  return (
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  );
}

function Workbench() {
  const [urlState, setUrlState] = useUrlState();
  const [dockApi, setDockApi] = useState<unknown>(null);
  const queryClientValue = useQueryClient();
  const project = useQuery({ queryKey: ["project"], queryFn: getProject });
  const topics = useQuery({ queryKey: ["topics"], queryFn: getTopics });
  const topicList = topics.data?.topics || [];
  const selectedTopicId = urlState.topicId || topicList[0]?.id;
  const graphScope = urlState.graphScope;

  useEffect(() => {
    if (!urlState.topicId && selectedTopicId) {
      setUrlState({ topicId: selectedTopicId, graphScope });
    }
  }, [graphScope, selectedTopicId, setUrlState, urlState.topicId]);

  useEffect(() => {
    if (!selectedTopicId) {
      return undefined;
    }
    const subscription = topicInvalidations(selectedTopicId).subscribe((event) => {
      queryClientValue.invalidateQueries({
        predicate: (query) => {
          const key = query.queryKey;
          return Array.isArray(key) && key[0] === "topic" && key[1] === selectedTopicId && intersectsEvent(key, event.graph_scopes || []);
        },
      });
    });
    return () => subscription.unsubscribe();
  }, [queryClientValue, selectedTopicId]);

  useEffect(() => {
    if (!dockApi) {
      return undefined;
    }
    const subscription = workbenchCommands$.subscribe((command) => {
      const api = dockApi as { addPanel?: (options: unknown) => unknown; getPanel?: (id: string) => { api?: { setActive?: () => void } } | undefined };
      if (command.type === "open-record") {
        const panelId = `record-${command.recordId}`;
        const existing = api.getPanel?.(panelId);
        if (existing) {
          existing.api?.setActive?.();
          return;
        }
        api.addPanel?.({
          id: panelId,
          component: "recordDetail",
          title: command.recordId,
          params: { topicId: command.topicId, recordId: command.recordId },
        });
      }
      if (command.type === "open-graph") {
        setUrlState({ topicId: command.topicId, graphScope: command.graphScope });
      }
      if (command.type === "refresh-topic") {
        manualRefresh$.next({ topicId: command.topicId });
      }
    });
    return () => subscription.unsubscribe();
  }, [dockApi, setUrlState]);

  const onDockReady = useCallback(
    (event: DockviewReadyEvent) => {
      setDockApi(event.api);
      if (!selectedTopicId) {
        return;
      }
      const primaryComponent = graphScope === "idea-lineage" ? "ideaGraph" : "denseGraph";
      event.api.addPanel({
        id: `graph-${graphScope}`,
        component: primaryComponent,
        title: graphTitle(graphScope),
        params: { topicId: selectedTopicId, graphScope },
      });
      event.api.addPanel({
        id: "records",
        component: "records",
        title: "Records",
        params: { topicId: selectedTopicId },
      });
      event.api.addPanel({
        id: "diagnostics",
        component: "diagnostics",
        title: "Diagnostics",
        params: { topicId: selectedTopicId, graphScope },
      });
    },
    [graphScope, selectedTopicId],
  );

  return (
    <div className="research-shell">
      <aside className="sidebar">
        <header className="brand-row">
          <h1>Isomer</h1>
          <span>{project.data?.ok ? "ready" : "loading"}</span>
        </header>
        <div className="project-root">{String(project.data?.project?.root || "")}</div>
        <TopicList topics={topicList} selectedTopicId={selectedTopicId} onSelect={(topicId) => setUrlState({ topicId, graphScope })} />
      </aside>
      <main className="workbench">
        <div className="topbar">
          <div className="topic-heading">
            <span>Research Topic</span>
            <h2>{selectedTopicId || "Select a topic"}</h2>
          </div>
          <div className="toolbar">
            <GraphScopeButtons selected={graphScope} topicId={selectedTopicId} />
            <button type="button" onClick={() => selectedTopicId && manualRefresh$.next({ topicId: selectedTopicId })}>
              Refresh
            </button>
          </div>
        </div>
        {selectedTopicId ? (
          <div className="dock-host dockview-theme-light">
            <DockviewReact key={`${selectedTopicId}:${graphScope}`} components={dockComponents} onReady={onDockReady} />
          </div>
        ) : (
          <div className="empty-state">No topic selected.</div>
        )}
      </main>
    </div>
  );
}

function TopicList({ topics, selectedTopicId, onSelect }: { topics: Topic[]; selectedTopicId?: string; onSelect: (topicId: string) => void }) {
  return (
    <nav className="topic-list">
      {topics.map((topic) => (
        <button className={topic.id === selectedTopicId ? "topic-button active" : "topic-button"} key={topic.id} type="button" onClick={() => onSelect(topic.id)}>
          <span>{topic.id}</span>
          <small>{topic.topic_statement || topic.status || "topic"}</small>
        </button>
      ))}
    </nav>
  );
}

function GraphScopeButtons({ selected, topicId }: { selected: GraphScope; topicId?: string }) {
  const scopes: GraphScope[] = ["idea-lineage", "artifact-overview", "experiment-records", "paper-revisions"];
  return (
    <div className="segmented">
      {scopes.map((scope) => (
        <button
          key={scope}
          className={scope === selected ? "selected" : ""}
          type="button"
          onClick={() => topicId && workbenchCommands$.next({ type: "open-graph", topicId, graphScope: scope })}
        >
          {scopeLabel(scope)}
        </button>
      ))}
    </div>
  );
}

const dockComponents = {
  ideaGraph: (props: IDockviewPanelProps<PanelParams>) => <IdeaGraphPanel {...props.params} />,
  denseGraph: (props: IDockviewPanelProps<PanelParams>) => <DenseGraphPanel topicId={props.params.topicId} graphScope={props.params.graphScope || "artifact-overview"} />,
  records: (props: IDockviewPanelProps<PanelParams>) => <RecordsPanel topicId={props.params.topicId} />,
  recordDetail: (props: IDockviewPanelProps<PanelParams>) => <RecordDetailPanel topicId={props.params.topicId} recordId={props.params.recordId || ""} />,
  diagnostics: (props: IDockviewPanelProps<PanelParams>) => <DiagnosticsPanel topicId={props.params.topicId} graphScope={props.params.graphScope || "idea-lineage"} />,
};

function IdeaGraphPanel({ topicId, graphScope = "idea-lineage" }: PanelParams) {
  const [filters, setFilters] = useState<GraphFilters>({ includeSecondary: true });
  const graph = useQuery({
    queryKey: ["topic", topicId, "graph", graphScope, requestedRenderer(graphScope), filters],
    queryFn: () => getTopicGraph(topicId, graphScope, requestedRenderer(graphScope), filters),
    enabled: Boolean(topicId),
  });
  const [flowNodes, setFlowNodes] = useState<Node[]>([]);
  const flowEdges = useMemo(() => (graph.data ? toFlowEdges(graph.data) : []), [graph.data]);

  useEffect(() => {
    let subscription = new Subscription();
    if (graph.data) {
      const nodes = toFlowNodes(graph.data);
      layoutFlowGraph(nodes, flowEdges).then((layouted) => {
        if (!subscription.closed) {
          setFlowNodes(layouted);
        }
      });
    }
    return () => subscription.unsubscribe();
  }, [flowEdges, graph.data]);

  return (
    <section className="panel-body">
      <GraphFiltersBar filters={filters} onChange={setFilters} />
      {graph.data && selectRenderer(graphScope, graph.data.renderer_hint, graph.data.nodes.length) === "sigma" ? (
        <SigmaGraph graph={graph.data} />
      ) : (
        <ReactFlowProvider>
          <div className="flow-frame">
            <ReactFlow nodes={flowNodes} edges={flowEdges} fitView onNodeClick={(_event, node) => openRecordFromNode(topicId, graph.data, node.id)}>
              <FlowAutoFit edgeCount={flowEdges.length} nodeCount={flowNodes.length} />
              <Background />
              <Controls />
            </ReactFlow>
          </div>
        </ReactFlowProvider>
      )}
      <GraphSummary graph={graph.data} isLoading={graph.isLoading} />
    </section>
  );
}

function FlowAutoFit({ edgeCount, nodeCount }: { edgeCount: number; nodeCount: number }) {
  const { fitView } = useReactFlow();
  useEffect(() => {
    if (!nodeCount) {
      return undefined;
    }
    const fit = () => fitView({ padding: 0.2, duration: 0 });
    const animationFrame = window.requestAnimationFrame(fit);
    window.addEventListener("resize", fit);
    return () => {
      window.cancelAnimationFrame(animationFrame);
      window.removeEventListener("resize", fit);
    };
  }, [edgeCount, fitView, nodeCount]);
  return null;
}

function DenseGraphPanel({ topicId, graphScope }: { topicId: string; graphScope: GraphScope }) {
  const [filters, setFilters] = useState<GraphFilters>({ includeSecondary: true });
  const graph = useQuery({
    queryKey: ["topic", topicId, "graph", graphScope, "sigma", filters],
    queryFn: () => getTopicGraph(topicId, graphScope, "sigma", filters),
    enabled: Boolean(topicId),
  });
  return (
    <section className="panel-body">
      <GraphFiltersBar filters={filters} onChange={setFilters} />
      {graph.data ? <SigmaGraph graph={graph.data} /> : <div className="empty-state">Loading graph.</div>}
      <GraphSummary graph={graph.data} isLoading={graph.isLoading} />
    </section>
  );
}

function SigmaGraph({ graph }: { graph: TopicGraphView }) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  useEffect(() => {
    if (!containerRef.current) {
      return undefined;
    }
    const graphology = new Graphology({ multi: true });
    for (const node of graph.nodes) {
      graphology.addNode(node.id, {
        label: node.title,
        x: Math.random(),
        y: Math.random(),
        size: Number(node.renderer_hints?.size || 8),
        color: String(node.renderer_hints?.color || "#64748b"),
      });
    }
    for (const edge of graph.edges) {
      if (graphology.hasNode(edge.source) && graphology.hasNode(edge.target) && !graphology.hasEdge(edge.id)) {
        graphology.addEdgeWithKey(edge.id, edge.source, edge.target, { label: edge.relation_kind, color: "#94a3b8" });
      }
    }
    const renderer = new Sigma(graphology, containerRef.current, { allowInvalidContainer: true });
    renderer.on("clickNode", ({ node }) => openRecordFromNode(graph.topic_id, graph, node));
    return () => renderer.kill();
  }, [graph]);
  return <div className="sigma-frame" ref={containerRef} />;
}

function GraphFiltersBar({ filters, onChange }: { filters: GraphFilters; onChange: (filters: GraphFilters) => void }) {
  return (
    <div className="filters">
      <input aria-label="Search graph" placeholder="search" value={filters.search || ""} onChange={(event) => onChange({ ...filters, search: event.target.value })} />
      <input aria-label="Status filter" placeholder="status" value={filters.status || ""} onChange={(event) => onChange({ ...filters, status: event.target.value })} />
      <input aria-label="Relation filter" placeholder="relation" value={filters.relationKind || ""} onChange={(event) => onChange({ ...filters, relationKind: event.target.value })} />
      <label className="checkbox">
        <input type="checkbox" checked={Boolean(filters.includeSecondary)} onChange={(event) => onChange({ ...filters, includeSecondary: event.target.checked })} />
        secondary
      </label>
    </div>
  );
}

function RecordsPanel({ topicId }: { topicId: string }) {
  const [search, setSearch] = useState("");
  const [facet, setFacet] = useState("");
  const records = useQuery({
    queryKey: ["topic", topicId, "records", facet],
    queryFn: () => getRecords(topicId, { facet: facet || undefined, limit: 500 }),
    enabled: Boolean(topicId),
  });
  const filteredRecords = useMemo(() => filterRecords(records.data?.records || [], search), [records.data?.records, search]);
  const table = useRecordsTable(filteredRecords, topicId);
  return (
    <section className="panel-body">
      <div className="filters">
        <input aria-label="Search records" placeholder="search records" value={search} onChange={(event) => setSearch(event.target.value)} />
        <select aria-label="Facet" value={facet} onChange={(event) => setFacet(event.target.value)}>
          <option value="">all facets</option>
          <option value="ideas">ideas</option>
          <option value="routes">routes</option>
          <option value="metrics">metrics</option>
          <option value="claims">claims</option>
          <option value="facts">facts</option>
        </select>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            {table.getHeaderGroups().map((group) => (
              <tr key={group.id}>
                {group.headers.map((header) => (
                  <th key={header.id}>{flexRender(header.column.columnDef.header, header.getContext())}</th>
                ))}
              </tr>
            ))}
          </thead>
          <tbody>
            {table.getRowModel().rows.map((row) => (
              <tr key={row.id} onClick={() => workbenchCommands$.next({ type: "open-record", topicId, recordId: row.original.record_id })}>
                {row.getVisibleCells().map((cell) => (
                  <td key={cell.id}>{flexRender(cell.column.columnDef.cell, cell.getContext())}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function RecordDetailPanel({ topicId, recordId }: { topicId: string; recordId: string }) {
  const descriptor = useQuery({
    queryKey: ["topic", topicId, "record", recordId, "descriptor"],
    queryFn: () => getViewerDescriptor(topicId, recordId),
    enabled: Boolean(topicId && recordId),
  });
  const detail = useQuery({
    queryKey: ["topic", topicId, "record", recordId, "detail", descriptor.data?.viewer_kind === "json"],
    queryFn: () => getRecordDetail(topicId, recordId, descriptor.data?.viewer_kind === "json"),
    enabled: Boolean(descriptor.data?.ok),
  });
  const rendered = useQuery({
    queryKey: ["topic", topicId, "record", recordId, "render", "markdown"],
    queryFn: () => getRecordRender(topicId, recordId),
    enabled: descriptor.data?.viewer_kind === "markdown",
  });
  const lineage = useQuery({ queryKey: ["topic", topicId, "record", recordId, "lineage"], queryFn: () => getRecordLineage(topicId, recordId), enabled: Boolean(descriptor.data?.ok) });
  const siblings = useQuery({ queryKey: ["topic", topicId, "record", recordId, "siblings"], queryFn: () => getRecordSiblings(topicId, recordId), enabled: Boolean(descriptor.data?.ok) });
  const files = useQuery({ queryKey: ["topic", topicId, "record", recordId, "files"], queryFn: () => getRecordFiles(topicId, recordId), enabled: Boolean(descriptor.data?.ok) });
  const facets = useQuery({ queryKey: ["topic", topicId, "record", recordId, "facets"], queryFn: () => getRecordFacets(topicId, recordId), enabled: Boolean(descriptor.data?.ok) });
  return (
    <section className="panel-body detail-viewer">
      <div className="detail-heading">
        <h3>{descriptor.data?.title || recordId}</h3>
        <span>{descriptor.data?.viewer_kind || "loading"}</span>
      </div>
      <ViewerContent descriptor={descriptor.data} rendered={rendered.data} detail={detail.data} />
      <div className="detail-columns">
        <JsonBlock title="Lineage" value={{ lineage: lineage.data, siblings: siblings.data }} />
        <FilesBlock value={files.data} />
        <JsonBlock title="Facets" value={facets.data} />
      </div>
    </section>
  );
}

function ViewerContent({ descriptor, rendered, detail }: { descriptor: unknown; rendered: unknown; detail: unknown }) {
  const data = descriptor as { viewer_kind?: string; primary_content_url?: string | null; media_type?: string | null } | undefined;
  if (!data) {
    return <div className="empty-state">Loading record.</div>;
  }
  const surface = viewerSurface(data);
  if (surface === "pdf" && data.primary_content_url) {
    return <iframe className="pdf-frame" title="PDF viewer" src={data.primary_content_url} />;
  }
  if (surface === "image" && data.primary_content_url) {
    return <img className="image-viewer" alt="" src={data.primary_content_url} />;
  }
  if (surface === "markdown") {
    const content = String(((rendered as { render?: { content?: string } })?.render?.content) || "");
    return <MarkdownView content={content || "No rendered Markdown available."} />;
  }
  if (surface === "table") {
    return <JsonBlock title="Table" value={detail} />;
  }
  return <JsonBlock title={surface === "json" ? "JSON" : "Record"} value={detail} />;
}

function MarkdownView({ content }: { content: string }) {
  return (
    <div className="markdown-view">
      <ReactMarkdown
        remarkPlugins={[remarkGfm, remarkMath]}
        rehypePlugins={[rehypeKatex]}
        components={{
          code(props) {
            const className = props.className || "";
            const value = String(props.children || "");
            if (className.includes("language-mermaid")) {
              return <MermaidBlock chart={value} />;
            }
            return <code className={className}>{props.children}</code>;
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}

function MermaidBlock({ chart }: { chart: string }) {
  const [svg, setSvg] = useState("");
  useEffect(() => {
    let cancelled = false;
    mermaid.initialize({ startOnLoad: false, securityLevel: "strict" });
    mermaid.render(`mmd-${crypto.randomUUID()}`, chart).then((result) => {
      if (!cancelled) {
        setSvg(result.svg);
      }
    });
    return () => {
      cancelled = true;
    };
  }, [chart]);
  return <div className="mermaid" dangerouslySetInnerHTML={{ __html: svg }} />;
}

function DiagnosticsPanel({ topicId, graphScope }: { topicId: string; graphScope: GraphScope }) {
  const graph = useQuery({
    queryKey: ["topic", topicId, "graph", graphScope, "diagnostics"],
    queryFn: () => getTopicGraph(topicId, graphScope, requestedRenderer(graphScope), { includeSecondary: true }),
    enabled: Boolean(topicId),
  });
  return (
    <section className="panel-body">
      <GraphSummary graph={graph.data} isLoading={graph.isLoading} />
      <div className="diagnostics-list">
        {(graph.data?.diagnostics || []).map((diagnostic, index) => (
          <div className={`diagnostic ${diagnostic.severity || "info"}`} key={`${diagnostic.code}-${index}`}>
            <strong>{diagnostic.code || "diagnostic"}</strong>
            <span>{diagnostic.message || ""}</span>
          </div>
        ))}
        {(graph.data?.groups || []).flatMap((group) =>
          (group.diagnostics || []).map((diagnostic, index) => (
            <div className={`diagnostic ${diagnostic.severity || "info"}`} key={`${group.id}-${diagnostic.code}-${index}`}>
              <strong>{diagnostic.code || group.title}</strong>
              <span>{diagnostic.message || group.purpose || ""}</span>
            </div>
          )),
        )}
      </div>
    </section>
  );
}

function GraphSummary({ graph, isLoading }: { graph?: TopicGraphView; isLoading: boolean }) {
  if (isLoading) {
    return <div className="status-line">Loading.</div>;
  }
  if (!graph) {
    return <div className="status-line">No graph data.</div>;
  }
  return (
    <div className="graph-summary">
      <span>{graph.nodes.length} nodes</span>
      <span>{graph.edges.length} edges</span>
      <span>{graph.renderer_hint}</span>
      {graph.paging?.truncated ? <span>truncated</span> : null}
      {graph.error ? <span>{graph.error.code}</span> : null}
    </div>
  );
}

function JsonBlock({ title, value }: { title: string; value: unknown }) {
  return (
    <div className="json-block">
      <h4>{title}</h4>
      <pre>{JSON.stringify(value || {}, null, 2)}</pre>
    </div>
  );
}

function FilesBlock({ value }: { value: unknown }) {
  const files = ((value as { files?: Array<Record<string, unknown>> })?.files || []) as Array<Record<string, unknown>>;
  return (
    <div className="json-block">
      <h4>Files</h4>
      <div className="file-list">
        {files.map((file) => (
          <div className="file-row" key={String(file.id || file.path)}>
            <strong>{String(file.file_role || "file")}</strong>
            <span>{String(file.path || "")}</span>
            <small>{file.openable ? "openable" : `not openable: ${String(file.open_blocked_reason || "unknown")}`}</small>
          </div>
        ))}
      </div>
    </div>
  );
}

function useRecordsTable(records: RecordSummary[], topicId: string) {
  const columnHelper = createColumnHelper<RecordSummary>();
  const columns = useMemo(
    () => [
      columnHelper.accessor("record_id", { header: "Record", cell: (info) => <button type="button" className="link-button" onClick={() => workbenchCommands$.next({ type: "open-record", topicId, recordId: info.getValue() })}>{info.getValue()}</button> }),
      columnHelper.accessor("record_kind", { header: "Kind", cell: (info) => info.getValue() || "" }),
      columnHelper.accessor("status", { header: "Status", cell: (info) => info.getValue() || "" }),
      columnHelper.accessor("title", { header: "Title", cell: (info) => info.getValue() || "" }),
      columnHelper.accessor("summary", { header: "Summary", cell: (info) => info.getValue() || "" }),
      columnHelper.accessor("updated_at", { header: "Updated", cell: (info) => info.getValue() || "" }),
    ],
    [columnHelper, topicId],
  );
  return useReactTable({ data: records, columns, getCoreRowModel: getCoreRowModel() });
}

function openRecordFromNode(topicId: string, graph: TopicGraphView | undefined, nodeId: string) {
  const node = graph?.nodes.find((candidate) => candidate.id === nodeId);
  if (node) {
    workbenchCommands$.next({ type: "open-record", topicId, recordId: node.record_id });
  }
}

function graphTitle(scope: GraphScope): string {
  return `${scopeLabel(scope)} Graph`;
}

function scopeLabel(scope: GraphScope): string {
  return {
    "idea-lineage": "Ideas",
    "artifact-overview": "Artifacts",
    "experiment-records": "Experiments",
    "paper-revisions": "Papers",
  }[scope];
}

function useUrlState(): [SearchState, (next: SearchState) => void] {
  const read = useCallback((): SearchState => {
    const params = new URLSearchParams(window.location.search);
    const graph = params.get("graph");
    return {
      topicId: params.get("topic") || undefined,
      graphScope: isGraphScope(graph) ? graph : "idea-lineage",
    };
  }, []);
  const [state, setState] = useState(read);
  useEffect(() => {
    const onPopState = () => setState(read());
    window.addEventListener("popstate", onPopState);
    return () => window.removeEventListener("popstate", onPopState);
  }, [read]);
  const write = useCallback((next: SearchState) => {
    const params = new URLSearchParams();
    if (next.topicId) {
      params.set("topic", next.topicId);
    }
    params.set("graph", next.graphScope);
    window.history.replaceState(null, "", `/?${params.toString()}`);
    setState(next);
  }, []);
  return [state, write];
}

function isGraphScope(value: string | null): value is GraphScope {
  return value === "idea-lineage" || value === "artifact-overview" || value === "experiment-records" || value === "paper-revisions";
}

function intersectsEvent(queryKey: readonly unknown[], graphScopes: string[]) {
  if (graphScopes.length === 0) {
    return true;
  }
  return queryKey.some((part) => typeof part === "string" && graphScopes.includes(part));
}

export function mountApp(element: HTMLElement) {
  createRoot(element).render(
    <React.StrictMode>
      <RootApp />
    </React.StrictMode>,
  );
}
