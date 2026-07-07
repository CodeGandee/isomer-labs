import { chromium } from "playwright";

const baseUrl = process.env.ISOMER_WEB_BASE_URL || "http://127.0.0.1:8765";
const topicId = process.env.ISOMER_WEB_TOPIC || "flash-attention-4-whitebox-runtime-model";
const ideaId = process.env.ISOMER_WEB_IDEA || "idea-occupancy-correction";

const viewports = [
  { name: "desktop", width: 1440, height: 960 },
  { name: "tablet", width: 820, height: 1180 },
  { name: "iphone", width: 390, height: 844 },
  { name: "android", width: 412, height: 915 },
];

function closeEnough(left, right) {
  return Math.abs(left - right) <= 2;
}

async function noPageOverflow(page) {
  return page.evaluate(() => document.documentElement.scrollWidth <= document.documentElement.clientWidth + 2);
}

async function visibleControlBounds(page, selector) {
  return page.evaluate((selectorValue) => {
    const viewportWidth = document.documentElement.clientWidth;
    const viewportHeight = document.documentElement.clientHeight;
    return Array.from(document.querySelectorAll(selectorValue))
      .filter((element) => {
        const rect = element.getBoundingClientRect();
        const style = window.getComputedStyle(element);
        return rect.width > 0 && rect.height > 0 && style.visibility !== "hidden" && style.display !== "none";
      })
      .map((element) => {
        const rect = element.getBoundingClientRect();
        return {
          text: element.textContent?.trim() || element.getAttribute("aria-label") || element.tagName,
          inside:
            rect.left >= -1 &&
            rect.top >= -1 &&
            rect.right <= viewportWidth + 1 &&
            rect.bottom <= viewportHeight + 1,
        };
      });
  }, selector);
}

const browser = await chromium.launch({ headless: true });
const results = [];
const failures = [];

try {
  for (const viewport of viewports) {
    const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height } });
    const page = await context.newPage();
    const pageErrors = [];
    const failedRequests = [];
    page.on("pageerror", (error) => pageErrors.push(String(error.stack || error.message || error)));
    page.on("requestfailed", (request) => {
      if (!request.url().includes("/api/events")) {
        failedRequests.push({ url: request.url(), failure: request.failure()?.errorText });
      }
    });

    const openItem = encodeURIComponent(`idea:${topicId}:${ideaId}`);
    await page.goto(`${baseUrl}/?topic=${encodeURIComponent(topicId)}&graph=idea-lineage&open=${openItem}&pw=${Date.now()}`, {
      waitUntil: "domcontentloaded",
      timeout: 60000,
    });
    await page.waitForSelector(".research-shell", { timeout: 30000 });
    await page.waitForSelector(".dock-host", { timeout: 30000 });
    await page.waitForTimeout(800);

    const mobile = viewport.width <= 980;
    let mobileDrawerOpened = false;
    if (mobile) {
      await page.getByRole("button", { name: "Project" }).click({ timeout: 15000 });
      await page.waitForSelector(".mobile-explorer-sheet .explorer-tree", { timeout: 15000 });
      mobileDrawerOpened = await page.locator(".mobile-explorer-sheet .explorer-tree").first().isVisible();
      await page.keyboard.press("Escape");
      await page.waitForTimeout(250);
    } else {
      const sidebarVisible = await page.locator(".explorer-sidebar").first().isVisible();
      if (!sidebarVisible) {
        failures.push(`${viewport.name}: desktop sidebar is not visible`);
      }
    }

    await page.waitForSelector(".idea-detail-panel", { timeout: 30000 }).catch(() => {});
    const ideaDetailAvailable = await page.locator(".idea-detail-panel").first().isVisible().catch(() => false);
    let jsonModalStable = null;
    if (ideaDetailAvailable && (await page.getByRole("button", { name: "View JSON" }).first().isEnabled().catch(() => false))) {
      await page.getByRole("button", { name: "View JSON" }).first().click({ timeout: 15000 });
      await page.waitForSelector(".json-modal", { timeout: 15000 });
      await page.waitForTimeout(250);
      const initialModal = await page.locator(".json-modal").boundingBox();
      const initialTabs = await page.locator(".json-modal [role='tab']").evaluateAll((tabs) =>
        tabs.map((tab) => {
          const rect = tab.getBoundingClientRect();
          return { left: rect.left, top: rect.top, width: rect.width, height: rect.height };
        }),
      );
      const tabCount = await page.locator(".json-modal [role='tab']").count();
      for (let index = 0; index < tabCount; index += 1) {
        await page.locator(".json-modal [role='tab']").nth(index).click({ timeout: 15000 });
        await page.waitForTimeout(120);
      }
      const finalModal = await page.locator(".json-modal").boundingBox();
      const finalTabs = await page.locator(".json-modal [role='tab']").evaluateAll((tabs) =>
        tabs.map((tab) => {
          const rect = tab.getBoundingClientRect();
          return { left: rect.left, top: rect.top, width: rect.width, height: rect.height };
        }),
      );
      jsonModalStable =
        Boolean(initialModal && finalModal) &&
        closeEnough(initialModal.width, finalModal.width) &&
        closeEnough(initialModal.height, finalModal.height) &&
        initialTabs.length === finalTabs.length &&
        initialTabs.every((tab, index) => closeEnough(tab.left, finalTabs[index].left) && closeEnough(tab.top, finalTabs[index].top));
      await page.getByRole("button", { name: "Close" }).click({ timeout: 15000 });
    }

    await page.getByRole("button", { name: "Settings" }).click({ timeout: 15000 });
    await page.waitForSelector(".settings-panel", { timeout: 15000 });
    const settingsVisible = await page.locator(".settings-panel").first().isVisible();
    const overflowFree = await noPageOverflow(page);
    const controlsInside = await visibleControlBounds(page, ".topbar button, .settings-panel button, .settings-panel [role='combobox']");
    const allControlsInside = controlsInside.every((control) => control.inside);

    const result = {
      viewport,
      mobile,
      mobileDrawerOpened,
      ideaDetailAvailable,
      jsonModalStable,
      settingsVisible,
      overflowFree,
      allControlsInside,
      pageErrors,
      failedRequests,
    };
    results.push(result);

    if (pageErrors.length || failedRequests.length || !overflowFree || !allControlsInside || !settingsVisible || (mobile && !mobileDrawerOpened) || jsonModalStable === false) {
      failures.push(`${viewport.name}: ${JSON.stringify(result)}`);
    }
    await context.close();
  }

  console.log(JSON.stringify({ results, failures }, null, 2));
  if (failures.length) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}
