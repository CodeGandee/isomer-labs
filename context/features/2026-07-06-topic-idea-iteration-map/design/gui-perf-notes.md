# GUI Performance Notes

## DeepScientist Lesson

DeepScientist uses React Flow (`@xyflow/react`) with Dagre layout for its quest graph canvases. It follows some React Flow performance guidance, but it still shows how a rich research graph can become slow when React Flow renders many DOM-heavy nodes, SVG edges, minimaps, hover cards, metric widgets, and polling-driven updates in one surface.

## Likely Bottlenecks

The graph nodes are rich cards, not simple glyphs. A node can include badges, branch metadata, memory summaries, metric blocks, handles, and SVG sparklines, so every graph update can touch a large DOM tree.

The frontend derives too much graph view state. It computes metrics, trends, branch insights, memory summaries, decision labels, layout state, selection state, and highlight state before rendering the graph.

Layout work runs in the viewer. Dagre layout and post-render collision repair use frontend state, measured node dimensions, and React Flow internals, which makes graph updates more expensive.

Polling can refresh several related datasets. A live run may poll graph, events, papers, memory, agents, decisions, PI Q&A, and branch insight data, so a visible canvas can keep rebuilding derived state.

The visual style is expensive at scale. Gradients, shadows, drop-shadows, filters, backdrop filters, SVG curves, and rich hover overlays add cost when many graph elements are mounted.

## React Flow Fit

Use React Flow for small and medium semantic DAGs where nodes are interactive cards. It is a good fit for focused idea lineage, selected-path inspection, local edit flows, and views where users need buttons, badges, handles, and rich per-node detail.

Do not use React Flow as the default renderer for large global artifact maps. For thousands of artifact nodes and relationship edges, prefer a GPU-backed renderer with simple glyph nodes and detail-on-selection.

Split graph visualization by artifact density and inspection depth. Sparse materials such as ideas, candidate hypotheses, decisions, and selected reasoning paths should stay in React Flow because users need deep inspection, comments, editing affordances, and readable relationship cards.

Dense materials such as experiment records, run outputs, paper revisions, generated figures, result summaries, and repeated logs should use Sigma.js for overview first. These artifact families can easily reach hundreds or thousands of nodes, so the default view should show structure, clusters, search, filtering, and selection, then open expanded detail in a separate tab or side panel.

## Large Graph Renderer

Use Sigma.js with Graphology as the first WebGL renderer for large artifact relationship maps. Keep the backend graph API renderer-neutral: return nodes, edges, types, labels, metrics, lineage fields, and display hints, not React Flow-specific objects.

Keep React Flow and Sigma.js as two views over the same graph model. React Flow should render detail mode; Sigma.js should render overview, search, filtering, clustering, and large-map exploration.

Do not force one renderer to cover every graph. The GUI should choose the renderer from graph scope, artifact type, and expected cardinality: React Flow for idea-level reasoning graphs; Sigma.js for experiment/paper/revision/log maps.

## Data and Update Policy

Fetch only for open, relevant tabs. Closed graph tabs must stop polling, SSE-triggered refetches, layout work, and renderer updates.

Use backend-derived read models for expensive graph projections. The frontend should not reconstruct lineage, generation groups, metrics, and event summaries from raw records when the backend can return a prepared view model.

Use live events as invalidation hints, not full refresh triggers. SSE should say what topic, artifact kind, graph scope, or index revision changed; TanStack Query should invalidate only mounted queries whose keys intersect the event.

## Rendering Policy

Start every graph in a cheap overview mode. Render simple glyphs, color, size, labels-on-demand, and selection highlights first; load rich node detail only when the user opens a detail tab or selects a node.

Avoid always-on minimaps, animated edges, per-node charts, large hover cards, and expensive CSS effects in large graph mode. Treat these as detail-mode features.

For React Flow views, keep node components memoized, callbacks stable, node and edge arrays structurally shared, and selected-node state separate from the whole nodes array.
