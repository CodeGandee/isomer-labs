import { chromium } from "playwright";

const baseUrl = process.env.ISOMER_WEB_BASE_URL || "http://127.0.0.1:8765";
const topicId = process.env.ISOMER_WEB_TOPIC || "flash-attention-4-whitebox-runtime-model";
const recordId = process.env.ISOMER_WEB_RECORD || "artifact-PRE_IDEA_DRAFT-8335b2785c4d";
const sampleMarkdown = [
  "# Runtime Model",
  "",
  "A [record](https://example.com) with `inline code`.",
  "",
  "## Candidate Updates",
  "",
  "- Capture the main idea.",
  "- Keep details readable.",
  "",
  "> Keep this review human-readable.",
  "",
  "```python",
  "print('hello')",
  "```",
  "",
  "| Field | Value |",
  "| --- | --- |",
  "| Outcome | Better preview |",
].join("\n");

function px(value) {
  return Number.parseFloat(String(value).replace("px", ""));
}

function rgbParts(value) {
  return (String(value).match(/\d+(\.\d+)?/g) || []).slice(0, 3).map(Number);
}

function luminance(value) {
  const [r = 0, g = 0, b = 0] = rgbParts(value);
  return 0.2126 * r + 0.7152 * g + 0.0722 * b;
}

function isWhite(value) {
  const [r = 0, g = 0, b = 0] = rgbParts(value);
  return r >= 248 && g >= 248 && b >= 248;
}

function styleSnapshot(page, rootSelector) {
  return page.evaluate((rootSelectorValue) => {
    const root = document.querySelector(rootSelectorValue);
    if (!root) {
      throw new Error(`Missing ${rootSelectorValue}`);
    }
    const pick = (selector) => {
      const element = root.querySelector(selector);
      if (!element) {
        return null;
      }
      const style = window.getComputedStyle(element);
      return {
        backgroundColor: style.backgroundColor,
        borderBottomColor: style.borderBottomColor,
        borderBottomWidth: style.borderBottomWidth,
        borderLeftColor: style.borderLeftColor,
        borderLeftWidth: style.borderLeftWidth,
        color: style.color,
        fontFamily: style.fontFamily,
        fontSize: style.fontSize,
        fontWeight: style.fontWeight,
        lineHeight: style.lineHeight,
        marginBottom: style.marginBottom,
        padding: style.padding,
      };
    };
    const rootStyle = window.getComputedStyle(root);
    return {
      root: {
        backgroundColor: rootStyle.backgroundColor,
        color: rootStyle.color,
        fontFamily: rootStyle.fontFamily,
        fontSize: rootStyle.fontSize,
        lineHeight: rootStyle.lineHeight,
      },
      h1: pick("h1"),
      h2: pick("h2"),
      p: pick("p"),
      link: pick("a"),
      inlineCode: pick("p code"),
      blockquote: pick("blockquote"),
      pre: pick("pre"),
      table: pick("table"),
      cell: pick("td"),
      hr: pick("hr"),
    };
  }, rootSelector);
}

const browser = await chromium.launch({ headless: true });
const referencePage = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const appPage = await browser.newPage({ viewport: { width: 1440, height: 960 } });
const failures = [];

try {
  await referencePage.goto("https://markdownlivepreview.com/", { waitUntil: "domcontentloaded", timeout: 60000 });
  await referencePage.locator("textarea").first().fill(sampleMarkdown);
  await referencePage.waitForFunction(
    () =>
      Array.from(document.querySelectorAll(".preview-pane, .preview, [class*='preview'], .column"))
        .filter((element) => element.textContent?.includes("Better preview"))
        .some((element) => {
          const h1 = element.querySelector("h1");
          return h1 && Number.parseFloat(window.getComputedStyle(h1).fontSize) >= 28;
        }),
    null,
    { timeout: 30000 },
  );
  const referenceRoot = await referencePage.evaluate(() => {
    const candidates = Array.from(document.querySelectorAll(".preview-pane, .preview, [class*='preview'], .column"));
    const match = candidates
      .filter((element) => element.textContent?.includes("Better preview") && element.querySelector("h1"))
      .sort((left, right) => {
        const leftH1 = left.querySelector("h1");
        const rightH1 = right.querySelector("h1");
        return Number.parseFloat(window.getComputedStyle(rightH1).fontSize) - Number.parseFloat(window.getComputedStyle(leftH1).fontSize);
      })[0];
    if (match) {
      match.id = "markdown-live-preview-reference";
      return "#markdown-live-preview-reference";
    }
    throw new Error("Could not find Markdown Live Preview output pane");
  });
  const reference = await styleSnapshot(referencePage, referenceRoot);

  const openItem = encodeURIComponent(`record:${topicId}:${recordId}`);
  await appPage.goto(`${baseUrl}/?topic=${encodeURIComponent(topicId)}&graph=idea-lineage&open=${openItem}&pw=${Date.now()}`, {
    waitUntil: "domcontentloaded",
    timeout: 60000,
  });
  await appPage.waitForSelector(".markdown-view", { timeout: 45000 });
  await appPage.waitForFunction(
    () => {
      const text = document.querySelector(".markdown-view")?.textContent || "";
      return text.length > 100 && !text.includes("Rendering Markdown.") && !text.includes("No rendered Markdown available.");
    },
    null,
    { timeout: 45000 },
  );
  const realRecord = await appPage.evaluate(() => {
    const markdown = document.querySelector(".markdown-view");
    const dockview = document.querySelector(".dv-dockview");
    if (!markdown) {
      throw new Error("Missing real Markdown preview");
    }
    const markdownStyle = window.getComputedStyle(markdown);
    const dockviewStyle = dockview ? window.getComputedStyle(dockview) : null;
    return {
      textLength: markdown.textContent?.length || 0,
      backgroundColor: markdownStyle.backgroundColor,
      color: markdownStyle.color,
      dockviewBackgroundColor: dockviewStyle?.backgroundColor || "",
      dockviewColor: dockviewStyle?.color || "",
    };
  });
  await appPage.screenshot({ path: "/tmp/isomer-markdown-preview-real.png", fullPage: false });

  await appPage.evaluate(() => {
    const host = document.createElement("main");
    host.id = "synthetic-markdown-preview";
    host.className = "markdown-view";
    host.innerHTML = `
      <h1>Runtime Model</h1>
      <p>A <a href="https://example.com">record</a> with <code>inline code</code>.</p>
      <h2>Candidate Updates</h2>
      <ul><li>Capture the main idea.</li><li>Keep details readable.</li></ul>
      <blockquote><p>Keep this review human-readable.</p></blockquote>
      <pre><code>print('hello')</code></pre>
      <table><thead><tr><th>Field</th><th>Value</th></tr></thead><tbody><tr><td>Outcome</td><td>Better preview</td></tr></tbody></table>
      <hr />
    `;
    document.body.replaceChildren(host);
    document.body.style.padding = "24px";
    document.body.style.background = "#f5f7f9";
  });
  const synthetic = await styleSnapshot(appPage, "#synthetic-markdown-preview");
  await appPage.screenshot({ path: "/tmp/isomer-markdown-preview-synthetic.png", fullPage: false });

  if (!isWhite(realRecord.backgroundColor)) {
    failures.push(`Real record Markdown background is not white: ${realRecord.backgroundColor}`);
  }
  if (luminance(realRecord.color) > 90) {
    failures.push(`Real record Markdown text is not dark enough: ${realRecord.color}`);
  }
  if (!isWhite(realRecord.dockviewBackgroundColor)) {
    failures.push(`Dockview content background is not light: ${realRecord.dockviewBackgroundColor}`);
  }
  if (realRecord.textLength < 100) {
    failures.push(`Real record Markdown did not render enough content: ${realRecord.textLength}`);
  }
  if (Math.abs(px(synthetic.h1?.fontSize) - px(reference.h1?.fontSize)) > 2) {
    failures.push(`H1 size diverges from Markdown Live Preview: app=${synthetic.h1?.fontSize}, reference=${reference.h1?.fontSize}`);
  }
  if (Math.abs(px(synthetic.p?.fontSize) - px(reference.p?.fontSize)) > 1) {
    failures.push(`Paragraph size diverges from Markdown Live Preview: app=${synthetic.p?.fontSize}, reference=${reference.p?.fontSize}`);
  }
  if (synthetic.link?.color !== "rgb(9, 105, 218)") {
    failures.push(`Link color is not GitHub-like blue: ${synthetic.link?.color}`);
  }
  if (synthetic.pre?.backgroundColor !== "rgb(246, 248, 250)") {
    failures.push(`Code block background is not GitHub-like gray: ${synthetic.pre?.backgroundColor}`);
  }
  if (!synthetic.blockquote?.borderLeftWidth || px(synthetic.blockquote.borderLeftWidth) < 3) {
    failures.push(`Blockquote lacks a readable left border: ${synthetic.blockquote?.borderLeftWidth}`);
  }
  if (synthetic.cell?.borderBottomColor !== "rgb(209, 217, 224)") {
    failures.push(`Table cell border is not GitHub-like gray: ${synthetic.cell?.borderBottomColor}`);
  }

  const result = {
    reference,
    realRecord,
    synthetic,
    screenshots: ["/tmp/isomer-markdown-preview-real.png", "/tmp/isomer-markdown-preview-synthetic.png"],
    failures,
  };
  console.log(JSON.stringify(result, null, 2));

  if (failures.length > 0) {
    process.exitCode = 1;
  }
} finally {
  await browser.close();
}
