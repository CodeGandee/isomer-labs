import { chromium } from "playwright";

const baseUrl = process.env.ISOMER_WEB_BASE_URL || "http://127.0.0.1:8765";
const shellBudgetMs = Number(process.env.ISOMER_WEB_SHELL_BUDGET_MS || 12000);

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 960 } });
const page = await context.newPage();
const client = await context.newCDPSession(page);
const failedRequests = [];
const responses = [];

page.on("requestfailed", (request) => {
  if (!request.url().includes("/api/events")) {
    failedRequests.push({ url: request.url(), failure: request.failure()?.errorText });
  }
});
page.on("response", (response) => {
  const url = response.url();
  if (url.includes("/assets/") || url.includes("/api/")) {
    responses.push({ url, status: response.status(), headers: response.headers() });
  }
});

try {
  await client.send("Network.enable");
  await client.send("Network.emulateNetworkConditions", {
    offline: false,
    latency: 80,
    downloadThroughput: 625000,
    uploadThroughput: 625000,
  });

  const startedAt = Date.now();
  await page.goto(`${baseUrl}/?perf=${startedAt}`, { waitUntil: "domcontentloaded", timeout: 60000 });
  const domContentLoadedMs = Date.now() - startedAt;
  await page.waitForSelector(".research-shell", { timeout: shellBudgetMs });
  const shellVisibleMs = Date.now() - startedAt;
  await page.waitForSelector(".explorer-tree", { timeout: 30000 });

  const resourceEntries = await page.evaluate(() =>
    performance.getEntriesByType("resource").map((entry) => ({
      name: entry.name,
      duration: Math.round(entry.duration),
      transferSize: entry.transferSize,
      encodedBodySize: entry.encodedBodySize,
      decodedBodySize: entry.decodedBodySize,
    })),
  );
  const jsAssets = responses.filter((item) => item.url.includes("/assets/") && item.url.endsWith(".js"));
  const cssAssets = responses.filter((item) => item.url.includes("/assets/") && item.url.endsWith(".css"));
  const hashedAssets = [...jsAssets, ...cssAssets].filter((item) => /\/assets\/.+-[A-Za-z0-9_-]{8,}\.(?:js|css)$/.test(new URL(item.url).pathname));
  const immutableAssets = hashedAssets.filter((item) => item.headers["cache-control"]?.includes("immutable"));
  const gzipAssets = [...jsAssets, ...cssAssets].filter((item) => item.headers["content-encoding"] === "gzip");
  const apiWithTiming = responses.filter((item) => item.url.includes("/api/") && item.headers["server-timing"]);
  const apiFailures = responses.filter((item) => item.url.includes("/api/") && item.status >= 400 && !item.url.includes("/api/events"));

  const result = {
    baseUrl,
    domContentLoadedMs,
    shellVisibleMs,
    shellBudgetMs,
    jsAssetCount: jsAssets.length,
    cssAssetCount: cssAssets.length,
    hashedAssetCount: hashedAssets.length,
    immutableAssetCount: immutableAssets.length,
    gzipAssetCount: gzipAssets.length,
    apiWithTimingCount: apiWithTiming.length,
    failedRequests,
    apiFailures,
    largestResources: resourceEntries
      .filter((entry) => entry.name.includes("/assets/"))
      .sort((left, right) => right.encodedBodySize - left.encodedBodySize)
      .slice(0, 8),
  };
  console.log(JSON.stringify(result, null, 2));

  if (
    failedRequests.length ||
    apiFailures.length ||
    shellVisibleMs > shellBudgetMs ||
    hashedAssets.length < 1 ||
    immutableAssets.length < hashedAssets.length ||
    gzipAssets.length < 1 ||
    apiWithTiming.length < 1
  ) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}
