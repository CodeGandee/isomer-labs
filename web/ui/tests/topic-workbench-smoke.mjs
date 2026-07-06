import { chromium } from "playwright";

const baseUrl = process.env.ISOMER_WEB_BASE_URL || "http://127.0.0.1:8766";

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
const consoleMessages = [];
const pageErrors = [];
const failedRequests = [];
const apiResponses = [];

page.on("console", (message) => {
  if (["error", "warning"].includes(message.type())) {
    consoleMessages.push({ type: message.type(), text: message.text() });
  }
});
page.on("pageerror", (error) => {
  pageErrors.push(String(error.stack || error.message || error));
});
page.on("requestfailed", (request) => {
  const url = request.url();
  if (!url.includes("/api/events")) {
    failedRequests.push({ url, failure: request.failure()?.errorText });
  }
});
page.on("response", (response) => {
  const url = response.url();
  if (url.includes("/api/") || url.includes("/assets/")) {
    apiResponses.push({ url, status: response.status() });
  }
});

try {
  await page.goto(`${baseUrl}/?pw=${Date.now()}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForSelector(".research-shell", { timeout: 30000 });
  await page.waitForSelector(".explorer-tree", { timeout: 30000 });
  await page.waitForSelector('[data-testid^="explorer-row-topic:"]', { timeout: 30000 });
  const topicRow = page.locator('[data-testid^="explorer-row-topic:"]').first();
  const topicText = await topicRow.innerText();
  await topicRow.click();
  await page.waitForSelector(".dock-host", { timeout: 30000 });

  await page.locator(".explorer-row").filter({ hasText: "Idea Lineage" }).first().click({ timeout: 15000 });
  await page.locator(".dv-tab").filter({ hasText: "Idea Lineage Graph" }).first().click({ timeout: 15000 });
  await page.waitForSelector(".graph-summary", { timeout: 30000 });
  await page.waitForSelector(".react-flow__node", { timeout: 30000 });
  await page.waitForTimeout(3000);
  const historyLengthBeforeActiveNoop = await page.evaluate(() => window.history.length);
  await page.locator(".explorer-row").filter({ hasText: "Idea Lineage" }).first().click({ timeout: 15000 });
  await page.waitForTimeout(500);
  const historyLengthAfterActiveNoop = await page.evaluate(() => window.history.length);
  const activeOpenNoop = historyLengthAfterActiveNoop === historyLengthBeforeActiveNoop;
  const ideaSummary = await page.locator(".graph-summary").first().innerText();
  const reactFlowNodeCount = await page.locator(".react-flow__node").count();
  const supportingCheckbox = page.getByRole("checkbox", { name: "Show supporting records" }).first();
  const supportingInitiallyChecked = await supportingCheckbox.isChecked();
  const defaultRouteDecisionCount = await page.locator(".react-flow__node").filter({ hasText: "Route decision" }).count();
  await supportingCheckbox.check({ timeout: 15000 });
  await page.waitForTimeout(2500);
  const supportingSummary = await page.locator(".graph-summary").first().innerText();
  const supportingNodeCount = await page.locator(".react-flow__node").count();
  await supportingCheckbox.uncheck({ timeout: 15000 });
  await page.waitForTimeout(2500);
  const visibleNodeIndex = await page.evaluate(() => {
    const nodes = Array.from(document.querySelectorAll(".react-flow__node"));
    return nodes.findIndex((node) => {
      const rect = node.getBoundingClientRect();
      const hit = document.elementFromPoint(rect.x + rect.width / 2, rect.y + rect.height / 2);
      return hit === node || Boolean(hit?.closest?.(".react-flow__node"));
    });
  });
  if (visibleNodeIndex < 0) {
    throw new Error("No clickable React Flow node found");
  }
  const selectedNodeText = await page.locator(".react-flow__node").nth(visibleNodeIndex).innerText();
  await page.locator(".react-flow__node").nth(visibleNodeIndex).click({ timeout: 15000 });
  await page.waitForSelector(".detail-viewer", { timeout: 30000 });
  await page.waitForTimeout(2500);
  const detailTitle = await page.locator(".detail-heading h3").first().innerText();
  const detailBodyPresent = await page.locator(".detail-viewer").first().isVisible();
  const tabsAfterDetail = await page.locator(".dv-tab").count();
  const detailTabsBeforeBack = await page.locator(".dv-tab").filter({ hasText: detailTitle }).count();

  await page.evaluate(() => window.history.back());
  await page.waitForFunction(() => {
    const open = new URL(window.location.href).searchParams.get("open");
    return open === null || open.includes(":graph:");
  }, null, { timeout: 15000 });
  await page.waitForSelector(".graph-summary", { timeout: 30000 });
  await page.waitForTimeout(1200);
  const tabsAfterBrowserBack = await page.locator(".dv-tab").count();
  const detailTabsAfterBrowserBack = await page.locator(".dv-tab").filter({ hasText: detailTitle }).count();
  const browserBackClosedDetail = detailTabsBeforeBack > 0 && detailTabsAfterBrowserBack === 0 && tabsAfterBrowserBack < tabsAfterDetail;

  await page.evaluate(() => window.history.forward());
  await page.waitForFunction(() => new URL(window.location.href).searchParams.get("open")?.startsWith("record:"), null, { timeout: 15000 });
  await page.waitForSelector(".detail-viewer", { timeout: 30000 });
  await page.waitForTimeout(1200);
  const detailTitleAfterForward = await page.locator(".detail-heading h3").first().innerText();
  const detailTabsAfterBrowserForward = await page.locator(".dv-tab").filter({ hasText: detailTitle }).count();
  const browserForwardRestoredDetail = detailTitleAfterForward === detailTitle && detailTabsAfterBrowserForward > 0;

  const fileButtonCount = await page.locator(".file-row button").count();
  if (fileButtonCount > 0) {
    await page.locator(".file-row button").first().click({ timeout: 15000 });
    await page.waitForSelector(".dv-tab", { timeout: 30000 });
  }

  await page.locator(".explorer-row").filter({ hasText: "Artifact Overview" }).first().click({ timeout: 15000 });
  await page.waitForSelector(".dv-tab", { timeout: 30000 });
  await page.locator(".dv-tab").filter({ hasText: "Artifact Overview Graph" }).first().click({ timeout: 15000 });
  await page.waitForSelector(".sigma-frame, .flow-frame", { timeout: 60000 });
  await page.waitForTimeout(3500);
  const artifactSummary = await page.locator(".graph-summary").first().innerText();
  const artifactGraphRenderer = await page.evaluate(() => {
    if (document.querySelector(".sigma-frame")) {
      return "sigma";
    }
    if (document.querySelector(".flow-frame")) {
      return "react-flow";
    }
    return "none";
  });
  const artifactGraphFrameVisible = await page.locator(".sigma-frame, .flow-frame").first().isVisible();

  await page.getByRole("button", { name: "Refresh" }).click({ timeout: 15000 });
  await page.waitForTimeout(1000);
  const refreshStillVisible = await page.locator(".graph-summary").first().isVisible();

  await page.setViewportSize({ width: 390, height: 820 });
  await page.waitForTimeout(1200);
  const mobileOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 2);
  await page.setViewportSize({ width: 1024, height: 720 });
  await page.waitForTimeout(800);
  const resizedSummaryVisible = await page.locator(".graph-summary").first().isVisible();

  const apiFailures = apiResponses.filter((item) => item.status >= 400 && !item.url.includes("/api/events"));
  const fatalConsoleErrors = consoleMessages.filter((message) => message.type === "error" && !message.text.includes("ResizeObserver loop"));
  const result = {
    title: await page.title(),
    topicText: topicText.split("\n")[0],
    ideaSummary,
    reactFlowNodeCount,
    historyLengthBeforeActiveNoop,
    historyLengthAfterActiveNoop,
    activeOpenNoop,
    supportingInitiallyChecked,
    defaultRouteDecisionCount,
    supportingSummary,
    supportingNodeCount,
    selectedNodeText,
    detailTitle,
    detailBodyPresent,
    tabsAfterDetail,
    detailTabsBeforeBack,
    tabsAfterBrowserBack,
    detailTabsAfterBrowserBack,
    browserBackClosedDetail,
    detailTitleAfterForward,
    detailTabsAfterBrowserForward,
    browserForwardRestoredDetail,
    fileButtonCount,
    artifactSummary,
    artifactGraphRenderer,
    artifactGraphFrameVisible,
    refreshStillVisible,
    mobileOverflow,
    resizedSummaryVisible,
    consoleMessages,
    pageErrors,
    failedRequests,
    apiFailures,
    apiResponseCount: apiResponses.length,
  };
  console.log(JSON.stringify(result, null, 2));

  if (
    pageErrors.length ||
    failedRequests.length ||
    apiFailures.length ||
    fatalConsoleErrors.length ||
    mobileOverflow ||
    reactFlowNodeCount < 1 ||
    !activeOpenNoop ||
    supportingInitiallyChecked ||
    defaultRouteDecisionCount > 0 ||
    supportingNodeCount < reactFlowNodeCount ||
    !detailBodyPresent ||
    tabsAfterDetail < 2 ||
    !browserBackClosedDetail ||
    !browserForwardRestoredDetail ||
    artifactSummary.includes("missing") ||
    !artifactGraphFrameVisible ||
    !refreshStillVisible ||
    !resizedSummaryVisible
  ) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}
