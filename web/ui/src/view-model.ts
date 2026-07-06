import type { RecordSummary, ViewerDescriptor } from "./types";

export function filterRecords(records: RecordSummary[], search: string): RecordSummary[] {
  const haystack = search.toLowerCase().trim();
  if (!haystack) {
    return records;
  }
  return records.filter((record) =>
    [record.record_id, record.record_kind, record.status, record.title, record.summary, record.profile, record.producer, record.skill]
      .filter(Boolean)
      .join(" ")
      .toLowerCase()
      .includes(haystack),
  );
}

export function viewerSurface(descriptor: Partial<Pick<ViewerDescriptor, "viewer_kind" | "primary_content_url">> | undefined): "markdown" | "pdf" | "image" | "json" | "table" | "unknown" {
  if (!descriptor || !descriptor.viewer_kind) {
    return "unknown";
  }
  if (descriptor.viewer_kind === "pdf" && descriptor.primary_content_url) {
    return "pdf";
  }
  if (descriptor.viewer_kind === "image" && descriptor.primary_content_url) {
    return "image";
  }
  if (descriptor.viewer_kind === "markdown") {
    return "markdown";
  }
  if (descriptor.viewer_kind === "table") {
    return "table";
  }
  if (descriptor.viewer_kind === "json") {
    return "json";
  }
  return "unknown";
}
