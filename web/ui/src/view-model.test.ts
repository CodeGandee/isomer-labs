import { describe, expect, it } from "vitest";
import { filterRecords, viewerSurface } from "./view-model";

describe("view model helpers", () => {
  it("filters records by high-level visible fields", () => {
    const records = [
      { record_id: "run-one", record_kind: "run", title: "Runtime model", status: "active" },
      { record_id: "claim-one", record_kind: "research_claim", title: "Memory claim", status: "open" },
    ];
    expect(filterRecords(records, "runtime")).toHaveLength(1);
    expect(filterRecords(records, "research_claim")[0].record_id).toBe("claim-one");
  });

  it("selects detail viewer surfaces from descriptors", () => {
    expect(viewerSurface({ viewer_kind: "markdown", primary_content_url: "/render" })).toBe("markdown");
    expect(viewerSurface({ viewer_kind: "pdf", primary_content_url: "/file.pdf" })).toBe("pdf");
    expect(viewerSurface({ viewer_kind: "pdf", primary_content_url: null })).toBe("unknown");
    expect(viewerSurface({ viewer_kind: "json", primary_content_url: null })).toBe("json");
  });
});
