import { chromium } from "playwright";

const baseUrl = process.env.ISOMER_WEB_BASE_URL || "http://127.0.0.1:8765";
const topicId = process.env.ISOMER_WEB_TOPIC || "flash-attention-4-whitebox-runtime-model";
const openGraph = encodeURIComponent(`topic:${topicId}:graph:idea-lineage`);

const browser = await chromium.launch({ headless: true });
const page = await browser.newPage({ viewport: { width: 1440, height: 960 } });
const pageErrors = [];
const failedRequests = [];

page.on("pageerror", (error) => {
  pageErrors.push(String(error.stack || error.message || error));
});
page.on("requestfailed", (request) => {
  if (!request.url().includes("/api/events")) {
    failedRequests.push({ url: request.url(), failure: request.failure()?.errorText });
  }
});

await page.route("**/api/topics/**/ideas/**", async (route) => {
  await new Promise((resolve) => setTimeout(resolve, 450));
  await route.continue();
});

try {
  await page.goto(`${baseUrl}/?topic=${encodeURIComponent(topicId)}&graph=idea-lineage&open=${openGraph}&pw=${Date.now()}`, {
    waitUntil: "domcontentloaded",
    timeout: 60000,
  });
  await page.waitForSelector(".research-shell", { timeout: 30000 });
  await page.waitForSelector(".react-flow__node[data-id^='idea:']", { timeout: 30000 });
  await page.waitForTimeout(1500);

  const node = page.locator(".react-flow__node[data-id^='idea:']").first();
  const nodeBox = await node.boundingBox();
  if (!nodeBox) {
    throw new Error("No visible idea lineage node found");
  }
  await page.mouse.move(nodeBox.x + nodeBox.width / 2, nodeBox.y + nodeBox.height / 2);

  await page.waitForSelector(".idea-node-hover-card", { timeout: 15000 });
  await page.getByText("Loading preview").waitFor({ timeout: 5000 });

  await page.waitForFunction(
    () => {
      const card = document.querySelector(".idea-node-hover-card");
      return Boolean(card && card.querySelector(".markdown-view") && !card.textContent?.includes("Loading preview") && card.textContent.length > 200);
    },
    null,
    { timeout: 30000 },
  );

  const cardMetrics = await page.locator(".idea-node-hover-card").evaluate((card) => {
    const style = window.getComputedStyle(card);
    return {
      height: card.clientHeight,
      overflow: style.overflow,
      overflowY: style.overflowY,
      pointerEvents: style.pointerEvents,
      scrollHeight: card.scrollHeight,
      scrollTop: card.scrollTop,
      textLength: card.textContent?.length || 0,
    };
  });

  const lockedBoxBefore = await page.locator(".idea-node-hover-card").boundingBox();
  await page.mouse.move(nodeBox.x + 10, nodeBox.y + 10);
  await page.waitForTimeout(150);
  const lockedBoxAfter = await page.locator(".idea-node-hover-card").boundingBox();
  const positionLocked = Boolean(
    lockedBoxBefore &&
    lockedBoxAfter &&
    Math.abs(lockedBoxBefore.x - lockedBoxAfter.x) < 1 &&
    Math.abs(lockedBoxBefore.y - lockedBoxAfter.y) < 1,
  );

  const cardBox = await page.locator(".idea-node-hover-card").boundingBox();
  if (!cardBox) {
    throw new Error("Hover card disappeared before interaction check");
  }
  await page.mouse.move(cardBox.x + Math.min(cardBox.width - 12, 24), cardBox.y + Math.min(cardBox.height - 12, 24));
  await page.waitForTimeout(500);
  const retainedInPopup = await page.locator(".idea-node-hover-card").isVisible();

  await page.mouse.wheel(0, 220);
  await page.waitForTimeout(150);
  const scrollAfterWheel = await page.locator(".idea-node-hover-card").evaluate((card) => card.scrollTop);
  const scrollWorks = cardMetrics.scrollHeight <= cardMetrics.height || scrollAfterWheel > cardMetrics.scrollTop;

  await page.mouse.dblclick(nodeBox.x + nodeBox.width / 2, nodeBox.y + nodeBox.height / 2);
  await page.waitForSelector(".idea-detail-panel", { timeout: 30000 });
  await page.waitForTimeout(500);
  const tooltipClearedAfterOpen = (await page.locator(".idea-node-hover-card").count()) === 0;

  await page.evaluate(() => window.history.back());
  await page.waitForSelector(".react-flow__node[data-id^='idea:']", { timeout: 30000 });
  await page.waitForTimeout(800);
  const tooltipRestoredAfterBack = (await page.locator(".idea-node-hover-card").count()) > 0;
  const nodeAfterBack = page.locator(".react-flow__node[data-id^='idea:']").first();
  const nodeAfterBackBox = await nodeAfterBack.boundingBox();
  if (!nodeAfterBackBox) {
    throw new Error("No visible idea lineage node found after returning to graph");
  }
  await nodeAfterBack.dispatchEvent("pointerdown", {
    bubbles: true,
    pointerId: 21,
    pointerType: "touch",
    clientX: nodeAfterBackBox.x + nodeAfterBackBox.width / 2,
    clientY: nodeAfterBackBox.y + nodeAfterBackBox.height / 2,
  });
  await page.waitForSelector(".idea-node-hover-card", { timeout: 15000 });
  const touchLongPressOpened = await page.locator(".idea-node-hover-card").isVisible();
  await nodeAfterBack.dispatchEvent("pointerup", {
    bubbles: true,
    pointerId: 21,
    pointerType: "touch",
    clientX: nodeAfterBackBox.x + nodeAfterBackBox.width / 2,
    clientY: nodeAfterBackBox.y + nodeAfterBackBox.height / 2,
  });

  const result = {
    cardMetrics,
    positionLocked,
    retainedInPopup,
    scrollAfterWheel,
    scrollWorks,
    tooltipClearedAfterOpen,
    tooltipRestoredAfterBack,
    touchLongPressOpened,
    pageErrors,
    failedRequests,
  };
  console.log(JSON.stringify(result, null, 2));

  if (
    pageErrors.length ||
    failedRequests.length ||
    cardMetrics.pointerEvents === "none" ||
    !["auto", "scroll"].includes(cardMetrics.overflowY) && !["auto", "scroll"].includes(cardMetrics.overflow) ||
    cardMetrics.textLength <= 200 ||
    !positionLocked ||
    !retainedInPopup ||
    !scrollWorks ||
    !tooltipClearedAfterOpen ||
    tooltipRestoredAfterBack ||
    !touchLongPressOpened
  ) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}
