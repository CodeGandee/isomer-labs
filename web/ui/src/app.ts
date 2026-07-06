type JsonObject = Record<string, unknown>;

type Topic = {
  id: string;
  status?: string;
  topic_workspace_id?: string;
  topic_workspace_path?: string;
  topic_statement?: string | null;
};

type IndexedRecord = {
  record_id: string;
  record_kind?: string;
  status?: string;
  title?: string | null;
  summary?: string | null;
  profile?: string | null;
  updated_at?: string;
};

type DiagnosticSummary = {
  total?: number;
  by_code?: Array<{ severity?: string; code?: string; count?: number }>;
};

type IndexedFile = {
  path?: string;
  resolved_path?: string | null;
  file_role?: string;
  openable?: boolean;
  open_blocked_reason?: string | null;
};

type ViewportMode = "wide" | "medium" | "narrow";

const state: {
  topics: Topic[];
  selectedTopicId: string | null;
  selectedRecordId: string | null;
  exportView: string;
  viewportMode: ViewportMode;
} = {
  topics: [],
  selectedTopicId: null,
  selectedRecordId: null,
  exportView: "dashboard",
  viewportMode: "wide",
};

const $ = <T extends HTMLElement>(selector: string): T => {
  const element = document.querySelector<T>(selector);
  if (!element) {
    throw new Error(`Missing element: ${selector}`);
  }
  return element;
};

async function fetchJson<T = JsonObject>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  return (await response.json()) as T;
}

function text(value: unknown, fallback = ""): string {
  if (value === null || value === undefined || value === "") {
    return fallback;
  }
  return String(value);
}

function html(value: unknown, fallback = ""): string {
  return text(value, fallback)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function renderJson(value: unknown): string {
  return JSON.stringify(value, null, 2);
}

function setStatus(message: string): void {
  $("#status-line").textContent = message;
}

function renderDiagnostics(containerId: string, diagnostics: unknown, summary?: unknown): void {
  const container = $<HTMLElement>(containerId);
  if (!Array.isArray(diagnostics) || diagnostics.length === 0) {
    container.innerHTML = "";
    return;
  }
  const summaryData = summary as DiagnosticSummary | undefined;
  if (summaryData && Array.isArray(summaryData.by_code)) {
    const grouped = summaryData.by_code
      .map((item) => `<div class="diagnostic ${html(item.severity)}"><strong>${html(item.count)}</strong> ${html(item.code)} <span>${html(item.severity)}</span></div>`)
      .join("");
    const details = diagnostics
      .map((item) => {
        const diagnostic = item as JsonObject;
        return `<div class="diagnostic ${html(diagnostic.severity)}"><strong>${html(diagnostic.code)}</strong> ${html(diagnostic.message)}</div>`;
      })
      .join("");
    container.innerHTML = `<div class="diagnostic-summary">${grouped}</div><details><summary>Details</summary>${details}</details>`;
    return;
  }
  container.innerHTML = diagnostics
    .map((item) => {
      const diagnostic = item as JsonObject;
      return `<div class="diagnostic ${html(diagnostic.severity)}"><strong>${html(diagnostic.code)}</strong> ${html(diagnostic.message)}</div>`;
    })
    .join("");
}

async function loadProject(): Promise<void> {
  const project = await fetchJson<JsonObject>("/api/project");
  const projectData = project.project as JsonObject | null;
  $("#project-root").textContent = text(projectData?.root, "No Project");
  $("#project-meta").textContent = project.ok ? "ready" : "diagnostics available";
  renderDiagnostics("#project-diagnostics", project.diagnostics);
}

async function loadTopics(): Promise<void> {
  const payload = await fetchJson<{ topics: Topic[]; diagnostics?: unknown }>("/api/topics");
  state.topics = payload.topics || [];
  if (!state.selectedTopicId && state.topics.length > 0) {
    state.selectedTopicId = state.topics[0].id;
  }
  renderTopicList();
  if (state.selectedTopicId) {
    await selectTopic(state.selectedTopicId);
  }
  renderDiagnostics("#topic-diagnostics", payload.diagnostics);
}

function renderTopicList(): void {
  const list = $("#topic-list");
  list.innerHTML = state.topics
    .map((topic) => {
      const active = topic.id === state.selectedTopicId ? "active" : "";
      return `<button class="topic-button ${active}" data-topic="${topic.id}">
        <span>${html(topic.id)}</span>
        <small>${html(topic.status, "unknown")}</small>
      </button>`;
    })
    .join("");
  list.querySelectorAll<HTMLButtonElement>("[data-topic]").forEach((button) => {
    button.addEventListener("click", () => selectTopic(button.dataset.topic || ""));
  });
}

async function selectTopic(topicId: string): Promise<void> {
  state.selectedTopicId = topicId;
  state.selectedRecordId = null;
  renderTopicList();
  setStatus(`Topic ${topicId}`);
  await Promise.all([loadTopicSummary(topicId), loadRuntime(topicId), loadRecords(topicId), loadExport(topicId)]);
}

async function loadTopicSummary(topicId: string): Promise<void> {
  const payload = await fetchJson<JsonObject>(`/api/topics/${encodeURIComponent(topicId)}`);
  const context = payload.context as JsonObject | null;
  const actors = Array.isArray(payload.topic_actors) ? payload.topic_actors : [];
  $("#topic-title").textContent = topicId;
  $("#topic-path").textContent = text(context?.topic_workspace_path, "");
  $("#actor-count").textContent = `${actors.length}`;
  renderDiagnostics("#topic-diagnostics", payload.diagnostics);
}

async function loadRuntime(topicId: string): Promise<void> {
  const payload = await fetchJson<JsonObject>(`/api/topics/${encodeURIComponent(topicId)}/runtime`);
  const runtime = payload.runtime as JsonObject | null;
  const counts = (runtime?.counts || {}) as JsonObject;
  const selected = ["lifecycle_records", "structured_research_payloads", "research_record_index", "research_record_files", "research_record_metrics", "research_record_claims"];
  $("#runtime-counts").innerHTML = selected
    .map((key) => `<div><strong>${html(counts[key], "0")}</strong><span>${html(key.replaceAll("_", " "))}</span></div>`)
    .join("");
}

async function loadRecords(topicId: string): Promise<void> {
  const params = new URLSearchParams();
  const kind = $<HTMLInputElement>("#filter-kind").value.trim();
  const profile = $<HTMLInputElement>("#filter-profile").value.trim();
  const facet = $<HTMLSelectElement>("#filter-facet").value;
  if (kind) params.set("record_kind", kind);
  if (profile) params.set("profile", profile);
  if (facet) params.set("facet", facet);
  params.set("limit", "200");
  const payload = await fetchJson<{ records?: IndexedRecord[]; diagnostics?: unknown }>(
    `/api/topics/${encodeURIComponent(topicId)}/records?${params.toString()}`,
  );
  renderRecords(payload.records || []);
  renderDiagnostics("#record-diagnostics", payload.diagnostics);
}

function renderRecords(records: IndexedRecord[]): void {
  const body = $("#record-table-body");
  body.innerHTML = records
    .map((record) => {
      const title = text(record.title, record.record_id);
      return `<tr data-record="${record.record_id}">
        <td>${html(record.record_id)}</td>
        <td>${html(record.record_kind)}</td>
        <td>${html(record.status)}</td>
        <td><strong>${html(title)}</strong><span>${html(record.summary)}</span></td>
        <td>${html(record.profile)}</td>
        <td>${html(record.updated_at)}</td>
      </tr>`;
    })
    .join("");
  body.querySelectorAll<HTMLTableRowElement>("[data-record]").forEach((row) => {
    row.addEventListener("click", () => openRecord(row.dataset.record || ""));
    });
}

function renderFilesView(filesPayload: JsonObject): string {
  const files = Array.isArray(filesPayload.files) ? (filesPayload.files as IndexedFile[]) : [];
  if (files.length === 0) {
    return "No indexed files.";
  }
  return files
    .map((file) => {
      const status = file.openable ? "openable" : `not openable: ${text(file.open_blocked_reason, "unknown")}`;
      const locator = text(file.resolved_path, text(file.path, ""));
      return `${text(file.file_role, "file")} | ${status}\n${locator}`;
    })
    .join("\n\n");
}

async function loadExport(topicId: string): Promise<void> {
  const payload = await fetchJson<JsonObject>(`/api/topics/${encodeURIComponent(topicId)}/records/export?view=${state.exportView}`);
  const keys = ["nodes", "edges", "files", "ideas", "routes", "metrics", "claims", "facts"];
  $("#export-cards").innerHTML = keys
    .map((key) => {
      const value = payload[key];
      const count = Array.isArray(value) ? value.length : 0;
      return `<div><strong>${html(count)}</strong><span>${html(key)}</span></div>`;
    })
    .join("");
  renderDiagnostics("#export-diagnostics", payload.diagnostics, payload.diagnostic_summary);
}

async function openRecord(recordId: string): Promise<void> {
  if (!state.selectedTopicId) return;
  state.selectedRecordId = recordId;
  setStatus(`Record ${recordId}`);
  const topicId = encodeURIComponent(state.selectedTopicId);
  const id = encodeURIComponent(recordId);
  const [detail, render, lineage, files, facets] = await Promise.all([
    fetchJson<JsonObject>(`/api/topics/${topicId}/records/${id}?include_payload=true`),
    fetchJson<JsonObject>(`/api/topics/${topicId}/records/${id}/render`),
    fetchJson<JsonObject>(`/api/topics/${topicId}/records/${id}/lineage`),
    fetchJson<JsonObject>(`/api/topics/${topicId}/records/${id}/files`),
    fetchJson<JsonObject>(`/api/topics/${topicId}/records/${id}/facets`),
  ]);
  const record = detail.record as JsonObject | undefined;
  $("#detail-title").textContent = text(record?.id, recordId);
  const rendered = render.render as JsonObject | undefined;
  $("#rendered-markdown").textContent = text(rendered?.content, "No rendered Markdown available.");
  $("#payload-json").textContent = renderJson((detail.structured_payload as JsonObject | undefined)?.payload || detail);
  $("#lineage-json").textContent = renderJson(lineage);
  $("#files-json").textContent = renderFilesView(files);
  $("#facets-json").textContent = renderJson(facets);
}

async function runIndexAction(action: "validate" | "rebuild" | "cleanup"): Promise<void> {
  if (!state.selectedTopicId) return;
  const topicId = encodeURIComponent(state.selectedTopicId);
  let payload: JsonObject;
  if (action === "validate") {
    payload = await fetchJson<JsonObject>(`/api/topics/${topicId}/records/index/validate`);
  } else if (action === "rebuild") {
    payload = await fetchJson<JsonObject>(`/api/topics/${topicId}/records/index/rebuild`, {
      method: "POST",
      body: JSON.stringify({ dry_run: false }),
    });
  } else {
    payload = await fetchJson<JsonObject>(`/api/topics/${topicId}/records/index/cleanup`, {
      method: "POST",
      body: JSON.stringify({ stale_derived: true, orphaned: true, missing_files: true, apply: false }),
    });
  }
  $("#maintenance-output").textContent = renderJson(payload);
  if (action === "rebuild") {
    await Promise.all([loadRecords(state.selectedTopicId), loadExport(state.selectedTopicId), loadRuntime(state.selectedTopicId)]);
  }
}

function bindControls(): void {
  $("#refresh-button").addEventListener("click", () => {
    if (state.selectedTopicId) selectTopic(state.selectedTopicId);
  });
  $("#filter-button").addEventListener("click", () => {
    if (state.selectedTopicId) loadRecords(state.selectedTopicId);
  });
  $("#export-view").addEventListener("change", (event) => {
    state.exportView = (event.target as HTMLSelectElement).value;
    if (state.selectedTopicId) loadExport(state.selectedTopicId);
  });
  document.querySelectorAll<HTMLButtonElement>("[data-index-action]").forEach((button) => {
    button.addEventListener("click", () => runIndexAction(button.dataset.indexAction as "validate" | "rebuild" | "cleanup"));
  });
}

function viewportMode(width: number): ViewportMode {
  if (width < 760) {
    return "narrow";
  }
  if (width < 1180) {
    return "medium";
  }
  return "wide";
}

function applyViewportMode(): void {
  const mode = viewportMode(window.innerWidth);
  if (mode === state.viewportMode && document.documentElement.dataset.viewport === mode) {
    return;
  }
  state.viewportMode = mode;
  document.documentElement.dataset.viewport = mode;
}

function bindViewportReactivity(): void {
  let frame = 0;
  const schedule = () => {
    if (frame) {
      return;
    }
    frame = window.requestAnimationFrame(() => {
      frame = 0;
      applyViewportMode();
    });
  };
  applyViewportMode();
  window.addEventListener("resize", schedule);
  window.visualViewport?.addEventListener("resize", schedule);
}

async function main(): Promise<void> {
  bindViewportReactivity();
  bindControls();
  await loadProject();
  await loadTopics();
  setStatus("Ready");
}

main().catch((error) => {
  setStatus(`Error: ${error instanceof Error ? error.message : String(error)}`);
});
