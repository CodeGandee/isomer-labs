import { describe, expect, it, vi } from "vitest";
import {
  DEFAULT_HOVER_PREVIEW_DELAY_MS,
  MIN_HOVER_PREVIEW_DELAY_MS,
  readStoredIdeaTimelinePrimaryColor,
  readStoredIdeaTimelineRowColorsEnabled,
  writeStoredIdeaTimelineRowColorsEnabled,
  writeStoredIdeaTimelineSupportingColor,
  readStoredHoverPreviewDelayMs,
  writeStoredHoverPreviewDelayMs,
} from "./ui-settings";

describe("GUI settings storage", () => {
  it("uses the 1.5 second default when no hover delay is stored", () => {
    const storage = storageWith(null);

    expect(readStoredHoverPreviewDelayMs(storage)).toBe(DEFAULT_HOVER_PREVIEW_DELAY_MS);
    expect(readStoredHoverPreviewDelayMs(storage)).toBe(1500);
  });

  it("reads the currently stored hover delay value", () => {
    const storage = storageWith("2250");

    expect(readStoredHoverPreviewDelayMs(storage)).toBe(2250);
  });

  it("normalizes hover delay values before writing", () => {
    const storage = storageWith(null);

    writeStoredHoverPreviewDelayMs(10, storage);

    expect(storage.setItem).toHaveBeenCalledWith("isomer-web-hover-preview-delay-ms", String(MIN_HOVER_PREVIEW_DELAY_MS));
  });

  it("defaults idea timeline row coloring off and stores the preference", () => {
    const emptyStorage = storageWith(null);
    expect(readStoredIdeaTimelineRowColorsEnabled(emptyStorage)).toBe(false);

    const storage = storageWith("false");

    expect(readStoredIdeaTimelineRowColorsEnabled(storage)).toBe(false);
    writeStoredIdeaTimelineRowColorsEnabled(true, storage);
    writeStoredIdeaTimelineSupportingColor("not-a-color", storage);

    expect(storage.setItem).toHaveBeenCalledWith("isomer-web-idea-timeline-row-colors-enabled", "true");
    expect(storage.setItem).toHaveBeenCalledWith("isomer-web-idea-timeline-supporting-color", "#fff7d6");
  });

  it("normalizes stored idea timeline colors", () => {
    const storage = storageWith("#CCFFCC");

    expect(readStoredIdeaTimelinePrimaryColor(storage)).toBe("#ccffcc");
  });
});

function storageWith(value: string | null) {
  return {
    getItem: vi.fn(() => value),
    setItem: vi.fn(),
  } as unknown as Storage;
}
