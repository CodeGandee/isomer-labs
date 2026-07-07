import { chromium } from "playwright";

const baseUrl = process.env.ISOMER_WEB_BASE_URL || "http://127.0.0.1:8765";
const topicId = process.env.ISOMER_WEB_TOPIC || "flash-attention-4-whitebox-runtime-model";
const ideaId = process.env.ISOMER_WEB_IDEA || "idea-occupancy-correction";

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 960 } });
await context.grantPermissions(["clipboard-read", "clipboard-write"], { origin: new URL(baseUrl).origin });
const page = await context.newPage();
const consoleMessages = [];
const pageErrors = [];
const failedRequests = [];

page.on("console", (message) => {
  if (["error", "warning"].includes(message.type())) {
    consoleMessages.push({ type: message.type(), text: message.text() });
  }
});
page.on("pageerror", (error) => {
  pageErrors.push(String(error.stack || error.message || error));
});
page.on("requestfailed", (request) => {
  if (!request.url().includes("/api/events")) {
    failedRequests.push({ url: request.url(), failure: request.failure()?.errorText });
  }
});

try {
  const openItem = encodeURIComponent(`idea:${topicId}:${ideaId}`);
  await page.goto(`${baseUrl}/?topic=${encodeURIComponent(topicId)}&graph=idea-lineage&open=${openItem}&pw=${Date.now()}`, {
    waitUntil: "domcontentloaded",
    timeout: 60000,
  });
  await page.waitForSelector(".research-shell", { timeout: 30000 });
  await page.waitForSelector(".idea-detail-panel", { timeout: 45000 });
  await page.waitForSelector(".markdown-view", { timeout: 45000 });

  const title = await page.locator(".idea-detail-panel .detail-heading h3").first().innerText();
  const markdownText = await page.locator(".idea-detail-panel .markdown-view").first().innerText();
  const markdownTextLength = markdownText.length;
  const leakedFilterNotes = /filter[_\\s-]*notes/i.test(markdownText) || markdownText.includes("R7 rejected") || markdownText.includes("R8 deferred");
  await page.getByRole("button", { name: "View JSON" }).click({ timeout: 15000, force: true });
  await page.waitForSelector(".json-modal", { timeout: 30000 });
  const jsonTextLength = await page.locator(".json-modal-code").innerText().then((text) => text.length);
  await page.getByRole("button", { name: "Copy JSON" }).last().click({ timeout: 15000, force: true });
  await page.waitForTimeout(500);
  await page.getByRole("button", { name: "Close" }).click({ timeout: 15000, force: true });
  await page.getByRole("button", { name: "Copy Markdown" }).click({ timeout: 15000, force: true });
  await page.waitForTimeout(500);
  const copyStatusVisible = await page.locator(".copy-status").count();

  const result = {
    topicId,
    ideaId,
    title,
    markdownTextLength,
    leakedFilterNotes,
    jsonTextLength,
    copyStatusVisible,
    consoleMessages,
    pageErrors,
    failedRequests,
  };
  console.log(JSON.stringify(result, null, 2));

  if (pageErrors.length || failedRequests.length || leakedFilterNotes || markdownTextLength < 20 || jsonTextLength < 10 || copyStatusVisible < 1) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}
