import { readFileSync } from "node:fs";
import { chromium } from "playwright";

const baseUrl = process.env.ISOMER_WEB_BASE_URL || "http://127.0.0.1:8766";
const topicId = process.env.ISOMER_WEB_TOPIC || "flash-attention-4-whitebox-runtime-model";
const fixture = JSON.parse(readFileSync(new URL("../../../tests/fixtures/research_idea_portfolio.json", import.meta.url), "utf8"));
const browser = await chromium.launch({ headless: true });
const errors = [];

try {
  const actual = await browser.newPage({ viewport: { width: 1440, height: 960 } });
  collectErrors(actual, errors, "actual");
  await actual.addInitScript(() => localStorage.clear());
  await openView(actual, "idea-lineage");
  await actual.waitForSelector(".idea-portfolio-controls", { timeout: 30000 });
  await waitForCount(actual, ".react-flow__node", 3);
  const graphControlsInitiallyOpen = await actual.locator(".idea-graph-controls").evaluate((element) => element.open);

  await selectPreset(actual, "all-proposed");
  await waitForCount(actual, ".react-flow__node", 5);
  const allProposedTitles = await actual.locator(".react-flow__node").allInnerTexts();
  await selectPreset(actual, "needs-classification");
  await waitForCount(actual, ".react-flow__node", 3);
  await selectPreset(actual, "selected");
  await waitForCount(actual, ".react-flow__node", 2);

  const stageNode = actual.locator(".react-flow__node").filter({ hasText: "Stage-pipeline white-box predictor" });
  const sassNode = actual.locator(".react-flow__node").filter({ hasText: "SASS-grounded interpretable runtime model" });
  await stageNode.click({ force: true });
  await sassNode.click({ force: true, modifiers: ["Control"] });
  await actual.getByRole("button", { name: "Explore Stage-pipeline white-box predictor instead" }).click();
  await actual.waitForSelector(".idea-steering-dialog", { timeout: 15000 });
  const steeringText = await actual.locator(".idea-steering-dialog").innerText();
  await actual.getByRole("button", { name: "Cancel" }).click();

  await actual.getByRole("button", { name: "Review decisions for Stage-pipeline white-box predictor" }).click();
  await actual.waitForSelector(".idea-decision-context", { timeout: 15000 });
  await actual.locator(".idea-decision-context").getByText("Pure roofline predictor", { exact: false }).waitFor({ timeout: 15000 });
  const decisionText = await actual.locator(".idea-decision-context").innerText();
  await actual.locator(".idea-decision-context").getByRole("button", { name: "Close" }).click();

  const traversalResponse = actual.waitForResponse((response) => response.url().includes("/ideas/traverse") && response.status() === 200, { timeout: 15000 });
  await actual.getByRole("button", { name: "Show descendants for Stage-pipeline white-box predictor" }).click();
  await traversalResponse;
  await actual.waitForSelector(".idea-traversal-banner", { timeout: 15000 });
  await waitForCount(actual, ".react-flow__node", 2);
  const traversalText = await actual.locator(".idea-traversal-banner").innerText();
  await actual.getByRole("button", { name: "Return to portfolio" }).click();

  const detail = await actual.evaluate(async ({ topic, idea }) => {
    const response = await fetch(`/api/topics/${encodeURIComponent(topic)}/ideas/${encodeURIComponent(idea)}?include_source_json=true`);
    return response.json();
  }, { topic: topicId, idea: "stage-pipeline-predictor" });
  const realizationPaths = detail.realizations.map((item) => item.source_json_path).filter(Boolean);

  await openView(actual, "idea-timeline");
  await actual.waitForSelector(".idea-timeline-panel", { timeout: 30000 });
  await waitForCount(actual, ".idea-timeline-row", 3);
  const timelineDefaultPreset = await actual.getByLabel("Idea portfolio preset").inputValue();
  await selectPreset(actual, "all-proposed");
  await waitForCount(actual, ".idea-timeline-row", 5);
  const timelineTitles = await actual.locator(".idea-timeline-row .timeline-title-cell strong").allInnerTexts();

  const kaojuOnly = await runFixturePortfolio(browser, fixture.kaoju_only, { current: 2, all: 4, marker: "Memory-traffic direction" }, errors, "kaoju-only");
  const mixed = await runFixturePortfolio(browser, fixture, { current: 3, all: 7, marker: "Static cost model" }, errors, "mixed");

  const result = {
    topicId,
    graphControlsInitiallyOpen,
    allProposedTitles,
    steeringText,
    decisionText,
    traversalText,
    realizationPaths,
    timelineDefaultPreset,
    timelineTitles,
    kaojuOnly,
    mixed,
    errors,
  };
  console.log(JSON.stringify(result, null, 2));
  const actualIdeasVisible = ["Pure roofline predictor", "Stage-pipeline white-box predictor", "Probabilistic occupancy predictor", "SASS-critical-path predictor"].every((title) => allProposedTitles.some((text) => text.includes(title)));
  const decisionComplete = decisionText.includes("Pure roofline predictor") && decisionText.includes("Probabilistic occupancy predictor") && decisionText.includes("SASS-critical-path predictor") && decisionText.includes("Requires SASS disassembly");
  const steeringComplete = steeringText.includes("Stage-pipeline white-box predictor") && steeringText.includes("SASS-grounded interpretable runtime model") && steeringText.includes("selected → deferred");
  const exactDetail = realizationPaths.includes("$.sections.raw_ideas[1]") && realizationPaths.includes("$.sections.serious_candidates[0]") && realizationPaths.includes("$.sections");
  if (errors.length || graphControlsInitiallyOpen || !actualIdeasVisible || !decisionComplete || !steeringComplete || !traversalText.includes("descendants") || !exactDetail || timelineDefaultPreset !== "current" || timelineTitles.length !== 5 || !kaojuOnly.ok || !mixed.ok) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}

async function runFixturePortfolio(browserInstance, dataset, expected, errorsOut, label) {
  const page = await browserInstance.newPage({ viewport: { width: 1280, height: 900 } });
  collectErrors(page, errorsOut, label);
  await page.addInitScript(() => localStorage.clear());
  const graphPayload = fixtureGraph(dataset);
  await page.route(`**/api/topics/${topicId}/graphs/idea-lineage*`, async (route) => {
    await route.fulfill({ status: 200, contentType: "application/json", body: JSON.stringify(graphPayload) });
  });
  await openView(page, "idea-lineage");
  await page.waitForSelector(".idea-portfolio-controls", { timeout: 30000 });
  await waitForCount(page, ".react-flow__node", expected.current);
  await selectPreset(page, "all-proposed");
  await waitForCount(page, ".react-flow__node", expected.all);
  const graphText = (await page.locator(".react-flow__node").allInnerTexts()).join("\n");
  await openView(page, "idea-timeline");
  await page.waitForSelector(".idea-timeline-panel", { timeout: 30000 });
  await selectPreset(page, "all-proposed");
  await waitForCount(page, ".idea-timeline-row", expected.all);
  const timelineText = (await page.locator(".idea-timeline-row").allInnerTexts()).join("\n");
  await page.close();
  return { ok: graphText.includes(expected.marker) && timelineText.includes(expected.marker), graphCount: expected.all, timelineCount: expected.all, marker: expected.marker };
}

function fixtureGraph(dataset) {
  const visibleIdeas = dataset.canonical_ideas.filter((idea) => idea.visibility !== "hidden");
  const nodeIds = new Set(visibleIdeas.map((idea) => idea.idea_id));
  const realizations = dataset.canonical_idea_realizations || [];
  const transitions = dataset.canonical_idea_transitions || [];
  const options = dataset.canonical_idea_decision_options || [];
  const nodes = visibleIdeas.map((idea) => {
    const latest = realizations.find((item) => item.idea_id === idea.idea_id && item.latest) || null;
    return {
      ...idea,
      id: `idea:${idea.idea_id}`,
      record_id: latest?.record_id || `record:${idea.idea_id}`,
      material_kind: "idea",
      density_class: "sparse",
      backend_selected: idea.decision_state === "selected",
      needs_classification: ["exploration_state", "decision_state", "evidence_state"].filter((facet) => idea[facet] === "unknown"),
      transition_refs: transitions.filter((item) => item.idea_id === idea.idea_id).map((item) => item.id),
      decision_record_ids: [...new Set([...transitions, ...options].filter((item) => item.idea_id === idea.idea_id && item.decision_record_id).map((item) => item.decision_record_id))],
      generation_ids: [],
      decision_summary: { current_decision_state: idea.decision_state },
      steering_eligibility: { eligible: idea.archive_state === "active" && idea.visibility !== "hidden", reopening_required: idea.decision_state === "closed" || idea.decision_state === "deferred" },
      source: { latest_realization: latest },
      detail_refs: { idea_detail: `/api/topics/${topicId}/ideas/${idea.idea_id}` },
    };
  });
  const edges = (dataset.canonical_idea_edges || []).filter((edge) => nodeIds.has(edge.parent_idea_id) && nodeIds.has(edge.child_idea_id)).map((edge) => ({
    ...edge,
    source: `idea:${edge.parent_idea_id}`,
    target: `idea:${edge.child_idea_id}`,
    relation_kind: edge.lineage_kind,
    canonical: true,
  }));
  return {
    ok: true,
    mutated: false,
    topic_id: topicId,
    topic_workspace_id: topicId,
    graph_scope: "idea-lineage",
    renderer_hint: "react-flow-detail",
    index_revision: dataset.index_revision,
    generated_at: "2026-07-17T00:00:00Z",
    nodes,
    edges,
    groups: [],
    facets: {},
    portfolio: { source_counts: { ideas: dataset.canonical_ideas.length, edges: edges.length }, visible_counts: { ideas: nodes.length, edges: edges.length }, source_topology_complete: true },
    topology_complete: true,
    total_node_count: nodes.length,
    total_edge_count: edges.length,
    source_node_count: dataset.canonical_ideas.length,
    source_edge_count: edges.length,
    visible_node_count: nodes.length,
    visible_edge_count: edges.length,
    diagnostics: [],
  };
}

async function openView(page, scope) {
  const open = `topic:${topicId}:graph:${scope}`;
  await page.goto(`${baseUrl}/?topic=${encodeURIComponent(topicId)}&graph=${scope}&open=${encodeURIComponent(open)}&portfolio_smoke=${Date.now()}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForSelector(".research-shell", { timeout: 30000 });
}

async function selectPreset(page, preset) {
  await page.getByLabel("Idea portfolio preset").selectOption(preset);
}

async function waitForCount(page, selector, expected) {
  await page.waitForFunction(({ css, count }) => document.querySelectorAll(css).length === count, { css: selector, count: expected }, { timeout: 30000 });
}

function collectErrors(page, target, label) {
  page.on("pageerror", (error) => target.push({ label, kind: "pageerror", message: String(error.stack || error) }));
  page.on("requestfailed", (request) => {
    if (!request.url().includes("/api/events")) {
      target.push({ label, kind: "requestfailed", message: `${request.url()}: ${request.failure()?.errorText}` });
    }
  });
}
