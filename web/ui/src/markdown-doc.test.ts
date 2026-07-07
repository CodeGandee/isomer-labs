import { describe, expect, it } from "vitest";
import { buildJsonMarkdownPreview } from "./markdown-doc";

describe("JSON Markdown document builder", () => {
  it("maps nested JSON into headings, lists, tables, and secondary metadata", () => {
    const preview = buildJsonMarkdownPreview(
      {
        title: "Precision-only throughput",
        one_liner: "Model precision overhead separately.",
        sections: {
          claims: ["GPU timing is predictable", "Host launch overhead is separable"],
          measurements: [
            { name: "baseline", speedup: 1.2 },
            { name: "candidate", speedup: 1.5 },
          ],
        },
        source_record_id: "record-1",
        payload_digest: "sha256:abc",
      },
      { title: "Idea Preview" },
    );

    expect(preview.markdown).toContain("# Idea Preview");
    expect(preview.markdown).toContain("**One Liner**: Model precision overhead separately.");
    expect(preview.markdown).toContain("* GPU timing is predictable");
    expect(preview.markdown).toContain("| Name");
    expect(preview.markdown).toContain("Speedup |");
    expect(preview.markdown).toContain("## Metadata");
    expect(preview.markdown).toContain("Source Record Id");
    expect(preview.markdown).not.toContain('{"title"');
    expect(preview.jsonText).toContain('"payload_digest": "sha256:abc"');
  });

  it("falls back to structured sections for mixed arrays instead of malformed tables", () => {
    const preview = buildJsonMarkdownPreview({
      alternatives: [
        { name: "route A", metrics: { score: 1 } },
        "route B",
      ],
    });

    expect(preview.markdown).toContain("## Alternatives");
    expect(preview.markdown).toContain("## Item 1");
    expect(preview.markdown).toContain("## Item 2");
    expect(preview.markdown).not.toContain("| Name | Metrics |");
  });
});
