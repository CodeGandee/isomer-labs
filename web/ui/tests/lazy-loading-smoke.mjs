import { chromium } from "playwright";

const baseUrl = process.env.ISOMER_WEB_BASE_URL || "http://127.0.0.1:8766";
const topicId = process.env.ISOMER_WEB_TOPIC_ID || "flash-attention-4-whitebox-runtime-model";
const explorerBudgetMs = Number(process.env.ISOMER_WEB_EXPLORER_BUDGET_MS || 2000);
const graphBudgetMs = Number(process.env.ISOMER_WEB_GRAPH_BUDGET_MS || 5000);
const openableItemId = `topic:${topicId}:graph:idea-lineage`;

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
const requestedApiPaths = [];
const requestedAssetPaths = [];
const failedRequests = [];
const pageErrors = [];

page.on("request", (request) => {
  const url = new URL(request.url());
  if (url.pathname.startsWith("/api/")) {
    requestedApiPaths.push(`${url.pathname}${url.search}`);
  }
  if (url.pathname.startsWith("/assets/")) {
    requestedAssetPaths.push(url.pathname);
  }
});
page.on("requestfailed", (request) => {
  if (!request.url().includes("/api/events")) {
    failedRequests.push({ url: request.url(), failure: request.failure()?.errorText });
  }
});
page.on("pageerror", (error) => {
  pageErrors.push(String(error.stack || error.message || error));
});

try {
  const url = new URL(baseUrl);
  url.searchParams.set("topic", topicId);
  url.searchParams.set("graph", "idea-lineage");
  url.searchParams.set("open", openableItemId);
  url.searchParams.set("lazy", String(Date.now()));

  await page.goto(url.toString(), { waitUntil: "domcontentloaded", timeout: 60000 });
  const domContentLoadedAt = Date.now();
  await page.waitForSelector(".research-shell", { timeout: 5000 });
  const shellMs = Date.now() - domContentLoadedAt;
  await page.waitForSelector(".explorer-tree", { timeout: Math.max(5000, explorerBudgetMs) });
  const explorerMs = Date.now() - domContentLoadedAt;
  await page.waitForSelector(".graph-summary", { timeout: Math.max(10000, graphBudgetMs) });
  const graphSummaryMs = Date.now() - domContentLoadedAt;
  await page.waitForSelector(".react-flow__node", { timeout: 10000 });
  await page.waitForTimeout(250);

  const topicPrefix = `/api/topics/${encodeURIComponent(topicId)}`;
  const allowedApi = (path) =>
    path.startsWith("/api/explorer/project") ||
    path.startsWith("/api/openable/") ||
    path.startsWith("/api/events?") ||
    path.startsWith(`${topicPrefix}/graphs/idea-lineage`);
  const unexpectedApiPaths = requestedApiPaths.filter((path) => !allowedApi(path));
  const unopenedViewerAssetPaths = requestedAssetPaths.filter((path) =>
    /(?:markdown-view|mermaid|katex|pdf)/i.test(path),
  );
  const result = {
    baseUrl,
    topicId,
    shellMs,
    explorerMs,
    explorerBudgetMs,
    graphSummaryMs,
    graphBudgetMs,
    requestedApiPaths,
    requestedAssetPaths,
    unexpectedApiPaths,
    unopenedViewerAssetPaths,
    failedRequests,
    pageErrors,
  };
  console.log(JSON.stringify(result, null, 2));

  if (
    shellMs > explorerBudgetMs ||
    explorerMs > explorerBudgetMs ||
    graphSummaryMs > graphBudgetMs ||
    unexpectedApiPaths.length ||
    unopenedViewerAssetPaths.length ||
    failedRequests.length ||
    pageErrors.length
  ) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}
