"use strict";
const state = {
    topics: [],
    selectedTopicId: null,
    selectedRecordId: null,
    exportView: "dashboard",
    viewportMode: "wide",
};
const $ = (selector) => {
    const element = document.querySelector(selector);
    if (!element) {
        throw new Error(`Missing element: ${selector}`);
    }
    return element;
};
async function fetchJson(path, init) {
    const response = await fetch(path, {
        headers: { "Content-Type": "application/json" },
        ...init,
    });
    return (await response.json());
}
function text(value, fallback = "") {
    if (value === null || value === undefined || value === "") {
        return fallback;
    }
    return String(value);
}
function html(value, fallback = "") {
    return text(value, fallback)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}
function renderJson(value) {
    return JSON.stringify(value, null, 2);
}
function setStatus(message) {
    $("#status-line").textContent = message;
}
function renderDiagnostics(containerId, diagnostics, summary) {
    const container = $(containerId);
    if (!Array.isArray(diagnostics) || diagnostics.length === 0) {
        container.innerHTML = "";
        return;
    }
    const summaryData = summary;
    if (summaryData && Array.isArray(summaryData.by_code)) {
        const grouped = summaryData.by_code
            .map((item) => `<div class="diagnostic ${html(item.severity)}"><strong>${html(item.count)}</strong> ${html(item.code)} <span>${html(item.severity)}</span></div>`)
            .join("");
        const details = diagnostics
            .map((item) => {
            const diagnostic = item;
            return `<div class="diagnostic ${html(diagnostic.severity)}"><strong>${html(diagnostic.code)}</strong> ${html(diagnostic.message)}</div>`;
        })
            .join("");
        container.innerHTML = `<div class="diagnostic-summary">${grouped}</div><details><summary>Details</summary>${details}</details>`;
        return;
    }
    container.innerHTML = diagnostics
        .map((item) => {
        const diagnostic = item;
        return `<div class="diagnostic ${html(diagnostic.severity)}"><strong>${html(diagnostic.code)}</strong> ${html(diagnostic.message)}</div>`;
    })
        .join("");
}
async function loadProject() {
    const project = await fetchJson("/api/project");
    const projectData = project.project;
    $("#project-root").textContent = text(projectData?.root, "No Project");
    $("#project-meta").textContent = project.ok ? "ready" : "diagnostics available";
    renderDiagnostics("#project-diagnostics", project.diagnostics);
}
async function loadTopics() {
    const payload = await fetchJson("/api/topics");
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
function renderTopicList() {
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
    list.querySelectorAll("[data-topic]").forEach((button) => {
        button.addEventListener("click", () => selectTopic(button.dataset.topic || ""));
    });
}
async function selectTopic(topicId) {
    state.selectedTopicId = topicId;
    state.selectedRecordId = null;
    renderTopicList();
    setStatus(`Topic ${topicId}`);
    await Promise.all([loadTopicSummary(topicId), loadRuntime(topicId), loadRecords(topicId), loadExport(topicId)]);
}
async function loadTopicSummary(topicId) {
    const payload = await fetchJson(`/api/topics/${encodeURIComponent(topicId)}`);
    const context = payload.context;
    const actors = Array.isArray(payload.topic_actors) ? payload.topic_actors : [];
    $("#topic-title").textContent = topicId;
    $("#topic-path").textContent = text(context?.topic_workspace_path, "");
    $("#actor-count").textContent = `${actors.length}`;
    renderDiagnostics("#topic-diagnostics", payload.diagnostics);
}
async function loadRuntime(topicId) {
    const payload = await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/runtime`);
    const runtime = payload.runtime;
    const counts = (runtime?.counts || {});
    const selected = ["lifecycle_records", "structured_research_payloads", "research_record_index", "research_record_files", "research_record_metrics", "research_record_claims"];
    $("#runtime-counts").innerHTML = selected
        .map((key) => `<div><strong>${html(counts[key], "0")}</strong><span>${html(key.replaceAll("_", " "))}</span></div>`)
        .join("");
}
async function loadRecords(topicId) {
    const params = new URLSearchParams();
    const kind = $("#filter-kind").value.trim();
    const profile = $("#filter-profile").value.trim();
    const facet = $("#filter-facet").value;
    if (kind)
        params.set("record_kind", kind);
    if (profile)
        params.set("profile", profile);
    if (facet)
        params.set("facet", facet);
    params.set("limit", "200");
    const payload = await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records?${params.toString()}`);
    renderRecords(payload.records || []);
    renderDiagnostics("#record-diagnostics", payload.diagnostics);
}
function renderRecords(records) {
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
    body.querySelectorAll("[data-record]").forEach((row) => {
        row.addEventListener("click", () => openRecord(row.dataset.record || ""));
    });
}
function renderFilesView(filesPayload) {
    const files = Array.isArray(filesPayload.files) ? filesPayload.files : [];
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
async function loadExport(topicId) {
    const payload = await fetchJson(`/api/topics/${encodeURIComponent(topicId)}/records/export?view=${state.exportView}`);
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
async function openRecord(recordId) {
    if (!state.selectedTopicId)
        return;
    state.selectedRecordId = recordId;
    setStatus(`Record ${recordId}`);
    const topicId = encodeURIComponent(state.selectedTopicId);
    const id = encodeURIComponent(recordId);
    const [detail, render, lineage, siblings, files, facets] = await Promise.all([
        fetchJson(`/api/topics/${topicId}/records/${id}?include_payload=true`),
        fetchJson(`/api/topics/${topicId}/records/${id}/render`),
        fetchJson(`/api/topics/${topicId}/records/${id}/lineage`),
        fetchJson(`/api/topics/${topicId}/records/${id}/siblings`),
        fetchJson(`/api/topics/${topicId}/records/${id}/files`),
        fetchJson(`/api/topics/${topicId}/records/${id}/facets`),
    ]);
    const record = detail.record;
    $("#detail-title").textContent = text(record?.id, recordId);
    const rendered = render.render;
    $("#rendered-markdown").textContent = text(rendered?.content, "No rendered Markdown available.");
    $("#payload-json").textContent = renderJson(detail.structured_payload?.payload || detail);
    $("#lineage-json").textContent = renderJson({ lineage, siblings });
    $("#files-json").textContent = renderFilesView(files);
    $("#facets-json").textContent = renderJson(facets);
}
async function runIndexAction(action) {
    if (!state.selectedTopicId)
        return;
    const topicId = encodeURIComponent(state.selectedTopicId);
    let payload;
    if (action === "validate") {
        payload = await fetchJson(`/api/topics/${topicId}/records/index/validate`);
    }
    else if (action === "rebuild") {
        payload = await fetchJson(`/api/topics/${topicId}/records/index/rebuild`, {
            method: "POST",
            body: JSON.stringify({ dry_run: false }),
        });
    }
    else {
        payload = await fetchJson(`/api/topics/${topicId}/records/index/cleanup`, {
            method: "POST",
            body: JSON.stringify({ stale_derived: true, orphaned: true, missing_files: true, apply: false }),
        });
    }
    $("#maintenance-output").textContent = renderJson(payload);
    if (action === "rebuild") {
        await Promise.all([loadRecords(state.selectedTopicId), loadExport(state.selectedTopicId), loadRuntime(state.selectedTopicId)]);
    }
}
function bindControls() {
    $("#refresh-button").addEventListener("click", () => {
        if (state.selectedTopicId)
            selectTopic(state.selectedTopicId);
    });
    $("#filter-button").addEventListener("click", () => {
        if (state.selectedTopicId)
            loadRecords(state.selectedTopicId);
    });
    $("#export-view").addEventListener("change", (event) => {
        state.exportView = event.target.value;
        if (state.selectedTopicId)
            loadExport(state.selectedTopicId);
    });
    document.querySelectorAll("[data-index-action]").forEach((button) => {
        button.addEventListener("click", () => runIndexAction(button.dataset.indexAction));
    });
}
function viewportMode(width) {
    if (width < 760) {
        return "narrow";
    }
    if (width < 1180) {
        return "medium";
    }
    return "wide";
}
function applyViewportMode() {
    const mode = viewportMode(window.innerWidth);
    if (mode === state.viewportMode && document.documentElement.dataset.viewport === mode) {
        return;
    }
    state.viewportMode = mode;
    document.documentElement.dataset.viewport = mode;
}
function bindViewportReactivity() {
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
async function main() {
    bindViewportReactivity();
    bindControls();
    await loadProject();
    await loadTopics();
    setStatus("Ready");
}
main().catch((error) => {
    setStatus(`Error: ${error instanceof Error ? error.message : String(error)}`);
});
