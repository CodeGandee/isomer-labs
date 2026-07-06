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
  await page.waitForSelector(".topic-button", { timeout: 30000 });
  const topicText = await page.locator(".topic-button").first().innerText();
  await page.locator(".topic-button").first().click();
  await page.waitForSelector(".dock-host", { timeout: 30000 });

  await page.locator(".dv-tab").filter({ hasText: "Ideas Graph" }).first().click({ timeout: 15000 });
  await page.waitForSelector(".graph-summary", { timeout: 30000 });
  await page.waitForSelector(".react-flow__node", { timeout: 30000 });
  await page.waitForTimeout(3000);
  const ideaSummary = await page.locator(".graph-summary").first().innerText();
  const reactFlowNodeCount = await page.locator(".react-flow__node").count();
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

  await page.getByRole("button", { name: "Artifacts" }).click({ timeout: 15000 });
  await page.waitForSelector(".dv-tab", { timeout: 30000 });
  await page.locator(".dv-tab").filter({ hasText: "Artifacts Graph" }).first().click({ timeout: 15000 });
  await page.waitForSelector(".sigma-frame", { timeout: 30000 });
  await page.waitForTimeout(3500);
  const artifactSummary = await page.locator(".graph-summary").first().innerText();
  const sigmaFrameVisible = await page.locator(".sigma-frame").first().isVisible();

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
    selectedNodeText,
    detailTitle,
    detailBodyPresent,
    tabsAfterDetail,
    artifactSummary,
    sigmaFrameVisible,
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
    !detailBodyPresent ||
    tabsAfterDetail < 4 ||
    artifactSummary.includes("missing") ||
    !sigmaFrameVisible ||
    !refreshStillVisible ||
    !resizedSummaryVisible
  ) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}
