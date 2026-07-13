import { chromium } from "playwright";

const baseUrl = process.env.ISOMER_WEB_BASE_URL || "http://127.0.0.1:8766";
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const pageErrors = [];
page.on("pageerror", (error) => pageErrors.push(String(error)));

try {
  await page.goto(`${baseUrl}/?idea_graph_controls=${Date.now()}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForSelector(".research-shell", { timeout: 30000 });
  await page.waitForSelector('[data-testid^="explorer-row-topic:"]', { timeout: 30000 });
  const topicTestId = await page.locator('[data-testid^="explorer-row-topic:"]').first().getAttribute("data-testid");
  const topicId = topicTestId?.replace("explorer-row-topic:", "");
  if (!topicId) {
    throw new Error("No Research Topic id was available for the Idea Graph smoke test.");
  }
  const graphItemId = `topic:${topicId}:graph:idea-lineage`;
  await page.goto(`${baseUrl}/?topic=${encodeURIComponent(topicId)}&graph=idea-lineage&open=${encodeURIComponent(graphItemId)}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForSelector(".idea-graph-controls", { timeout: 30000 });
  await page.waitForSelector(".react-flow__node", { timeout: 30000 });

  const graphControlsVisible = await page.getByText("Graph Controls", { exact: true }).isVisible();
  const nodeCount = await page.locator(".react-flow__node").count();
  await page.locator(".react-flow__node").nth(0).click({ force: true });
  if (nodeCount > 1) {
    await page.locator(".react-flow__node").nth(1).click({ force: true, modifiers: ["Control"] });
  }
  const selectedCount = await page.locator(".react-flow__node.ui-selected").count();
  const selectionChips = await page.locator(".idea-graph-selection-chip").count();

  await page.getByLabel("Enable N-hop focus").check();
  await page.getByLabel("Focus hop radius").fill("1");
  const focusCounts = await page.locator(".idea-graph-counts").innerText();
  await page.getByLabel("Graph layout algorithm").selectOption("grid");
  await page.getByRole("button", { name: "Preview Layout" }).click();
  await page.getByRole("status").filter({ hasText: /Layout completed in/ }).waitFor({ timeout: 30000 });
  await page.getByLabel("Graph layout preset name").fill("Browser smoke grid");
  await page.getByRole("button", { name: "Save as New" }).click();
  const storedPreset = await page.evaluate(() => localStorage.getItem("isomer-web-idea-graph-layout-presets-v1"));

  await page.setViewportSize({ width: 390, height: 820 });
  await page.waitForTimeout(300);
  const responsiveControlsVisible = await page.locator(".idea-graph-controls").isVisible();
  const mobileOverflow = await page.evaluate(() => document.documentElement.scrollWidth > document.documentElement.clientWidth + 2);
  await page.setViewportSize({ width: 1280, height: 900 });

  const target = page.locator(".react-flow__node").first();
  await target.dblclick({ force: true });
  await page.waitForSelector(".idea-detail-panel, .detail-viewer", { timeout: 30000 });
  const detailOpened = await page.locator(".idea-detail-panel, .detail-viewer").first().isVisible();

  const result = { graphControlsVisible, nodeCount, selectedCount, selectionChips, focusCounts, storedPreset: Boolean(storedPreset?.includes("Browser smoke grid")), responsiveControlsVisible, mobileOverflow, detailOpened, pageErrors };
  console.log(JSON.stringify(result, null, 2));
  if (!graphControlsVisible || nodeCount < 1 || selectedCount < 1 || selectionChips !== selectedCount || !focusCounts.includes("Visible") || !storedPreset?.includes("Browser smoke grid") || !responsiveControlsVisible || mobileOverflow || !detailOpened || pageErrors.length) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}
