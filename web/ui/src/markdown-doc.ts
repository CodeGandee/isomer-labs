import { gfmToMarkdown } from "mdast-util-gfm";
import { toMarkdown } from "mdast-util-to-markdown";
import { u } from "unist-builder";

type MdNode = {
  type: string;
  [key: string]: unknown;
};

export type JsonMarkdownPreview = {
  markdown: string;
  jsonText: string;
};

const HUMAN_KEYS = new Set(["title", "summary", "one_liner", "claim", "hypothesis", "rationale", "status", "family", "visibility"]);

export function buildJsonMarkdownPreview(value: unknown, options: { title?: string; maxDepth?: number } = {}): JsonMarkdownPreview {
  const normalized = normalizeJson(value);
  const children: MdNode[] = [];
  if (options.title) {
    children.push(heading(1, options.title));
  }
  children.push(...renderValue(undefined, normalized, 2, options.maxDepth ?? 6));
  const root = u("root", children);
  return {
    markdown: toMarkdown(root, { extensions: [gfmToMarkdown()] }).trim(),
    jsonText: JSON.stringify(normalized, null, 2),
  };
}

function renderValue(key: string | undefined, value: unknown, depth: number, maxDepth: number): MdNode[] {
  if (isPlainObject(value)) {
    const body = depth > maxDepth ? [jsonCode(value)] : renderObject(value, depth, maxDepth);
    return key ? [heading(depth, labelForKey(key)), ...body] : body;
  }
  if (Array.isArray(value)) {
    const body = depth > maxDepth ? [jsonCode(value)] : renderArray(value, depth, maxDepth);
    return key ? [heading(depth, labelForKey(key)), ...body] : body;
  }
  if (key) {
    return [paragraph([strong(labelForKey(key)), text(`: ${formatScalar(value)}`)])];
  }
  return [paragraph([text(formatScalar(value))])];
}

function renderObject(value: Record<string, unknown>, depth: number, maxDepth: number): MdNode[] {
  const entries = Object.entries(value);
  const contentEntries = entries.filter(([key]) => !isMetadataKey(key));
  const metadataEntries = entries.filter(([key]) => isMetadataKey(key));
  const children: MdNode[] = [];
  for (const [key, child] of contentEntries) {
    children.push(...renderValue(key, child, depth, maxDepth));
  }
  if (metadataEntries.length) {
    children.push(heading(depth, "Metadata"));
    for (const [key, child] of metadataEntries) {
      children.push(...renderValue(key, child, Math.min(depth + 1, 6), maxDepth));
    }
  }
  if (!children.length) {
    children.push(paragraph([text("No fields.")]));
  }
  return children;
}

function renderArray(value: unknown[], depth: number, maxDepth: number): MdNode[] {
  if (!value.length) {
    return [paragraph([text("No items.")])];
  }
  if (value.every(isScalar)) {
    return [list(value.map((item) => [paragraph([text(formatScalar(item))])]))];
  }
  const table = tableForArray(value);
  if (table) {
    return [table];
  }
  return value.flatMap((item, index) => [heading(Math.min(depth, 6), `Item ${index + 1}`), ...renderValue(undefined, item, Math.min(depth + 1, 6), maxDepth)]);
}

function tableForArray(value: unknown[]): MdNode | null {
  if (!value.every(isPlainObject)) {
    return null;
  }
  const rows = value as Record<string, unknown>[];
  const keys = Object.keys(rows[0] || {});
  if (!keys.length || rows.some((row) => !sameKeys(keys, Object.keys(row)) || keys.some((key) => !isScalar(row[key])))) {
    return null;
  }
  return u(
    "table",
    { align: keys.map(() => null) },
    [
      tableRow(keys.map((key) => tableCell(labelForKey(key)))),
      ...rows.map((row) => tableRow(keys.map((key) => tableCell(formatScalar(row[key]))))),
    ],
  );
}

function normalizeJson(value: unknown): unknown {
  if (Array.isArray(value)) {
    return value.map(normalizeJson);
  }
  if (isPlainObject(value)) {
    const normalized: Record<string, unknown> = {};
    for (const key of Object.keys(value).sort()) {
      normalized[key] = normalizeJson(value[key]);
    }
    return normalized;
  }
  return value;
}

function isMetadataKey(key: string): boolean {
  const normalized = key.toLowerCase();
  if (HUMAN_KEYS.has(normalized)) {
    return false;
  }
  return (
    normalized === "id" ||
    normalized.endsWith("_id") ||
    normalized.endsWith("_ids") ||
    normalized.includes("digest") ||
    normalized.includes("locator") ||
    normalized.includes("provenance") ||
    normalized.startsWith("source_") ||
    normalized.endsWith("_path") ||
    normalized === "path" ||
    normalized.endsWith("_at") ||
    normalized === "metadata"
  );
}

function isPlainObject(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === "object" && !Array.isArray(value);
}

function isScalar(value: unknown): boolean {
  return value === null || ["string", "number", "boolean"].includes(typeof value);
}

function sameKeys(left: string[], right: string[]): boolean {
  if (left.length !== right.length) {
    return false;
  }
  const sortedLeft = [...left].sort();
  const sortedRight = [...right].sort();
  return sortedLeft.every((key, index) => key === sortedRight[index]);
}

function labelForKey(key: string): string {
  return key
    .replace(/[_-]+/g, " ")
    .trim()
    .replace(/\b\w/g, (char) => char.toUpperCase());
}

function formatScalar(value: unknown): string {
  if (value === null) {
    return "null";
  }
  if (typeof value === "string") {
    return value;
  }
  return JSON.stringify(value);
}

function heading(depth: number, value: string): MdNode {
  return u("heading", { depth: Math.min(Math.max(depth, 1), 6) }, [text(value)]);
}

function paragraph(children: MdNode[]): MdNode {
  return u("paragraph", children);
}

function text(value: string): MdNode {
  return u("text", value);
}

function strong(value: string): MdNode {
  return u("strong", [text(value)]);
}

function list(items: MdNode[][]): MdNode {
  return u("list", { ordered: false }, items.map((children) => u("listItem", children)));
}

function tableRow(children: MdNode[]): MdNode {
  return u("tableRow", children);
}

function tableCell(value: string): MdNode {
  return u("tableCell", [text(value)]);
}

function jsonCode(value: unknown): MdNode {
  return u("code", { lang: "json", value: JSON.stringify(value, null, 2) });
}
