import { describe, expect, it } from "vitest";

import { topicRelativeDisplayPath } from "./display-path";

describe("topicRelativeDisplayPath", () => {
  it("strips paths under a topic workspace", () => {
    expect(
      topicRelativeDisplayPath(
        "/data/ssd1/huangzhe/code/isomer-labs/isomer-content/topic-ws/flash-attention-4-whitebox-runtime-model/intent/src/topic-overview.md",
        { topicId: "flash-attention-4-whitebox-runtime-model" },
      ),
    ).toBe("intent/src/topic-overview.md");
  });

  it("uses an explicit topic workspace path when available", () => {
    expect(
      topicRelativeDisplayPath("/tmp/custom-topic/records/artifacts/idea.json", {
        topicWorkspacePath: "/tmp/custom-topic",
      }),
    ).toBe("records/artifacts/idea.json");
  });

  it("keeps non-topic paths and json paths unchanged", () => {
    expect(topicRelativeDisplayPath("/tmp/outside/file.md", { topicId: "alpha" })).toBe("/tmp/outside/file.md");
    expect(topicRelativeDisplayPath("sections.raw_ideas[0]", { topicId: "alpha" })).toBe("sections.raw_ideas[0]");
  });
});
