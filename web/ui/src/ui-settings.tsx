import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

export const DEFAULT_HOVER_PREVIEW_DELAY_MS = 1500;
export const MIN_HOVER_PREVIEW_DELAY_MS = 250;
export const MAX_HOVER_PREVIEW_DELAY_MS = 5000;
export const DEFAULT_IDEA_TIMELINE_PRIMARY_COLOR = "#e9f7ef";
export const DEFAULT_IDEA_TIMELINE_SUPPORTING_COLOR = "#fff7d6";

const HOVER_PREVIEW_DELAY_STORAGE_KEY = "isomer-web-hover-preview-delay-ms";
const IDEA_TIMELINE_ROW_COLORS_ENABLED_STORAGE_KEY = "isomer-web-idea-timeline-row-colors-enabled";
const IDEA_TIMELINE_PRIMARY_COLOR_STORAGE_KEY = "isomer-web-idea-timeline-primary-color";
const IDEA_TIMELINE_SUPPORTING_COLOR_STORAGE_KEY = "isomer-web-idea-timeline-supporting-color";

type GuiSettingsContextValue = {
  hoverPreviewDelayMs: number;
  ideaTimelinePrimaryColor: string;
  ideaTimelineRowColorsEnabled: boolean;
  ideaTimelineSupportingColor: string;
  refreshGuiSettings: () => void;
  setHoverPreviewDelayMs: (delayMs: number) => void;
  setIdeaTimelinePrimaryColor: (color: string) => void;
  setIdeaTimelineRowColorsEnabled: (enabled: boolean) => void;
  setIdeaTimelineSupportingColor: (color: string) => void;
};

const GuiSettingsContext = createContext<GuiSettingsContextValue>({
  hoverPreviewDelayMs: DEFAULT_HOVER_PREVIEW_DELAY_MS,
  ideaTimelinePrimaryColor: DEFAULT_IDEA_TIMELINE_PRIMARY_COLOR,
  ideaTimelineRowColorsEnabled: false,
  ideaTimelineSupportingColor: DEFAULT_IDEA_TIMELINE_SUPPORTING_COLOR,
  refreshGuiSettings: () => undefined,
  setHoverPreviewDelayMs: () => undefined,
  setIdeaTimelinePrimaryColor: () => undefined,
  setIdeaTimelineRowColorsEnabled: () => undefined,
  setIdeaTimelineSupportingColor: () => undefined,
});

export function GuiSettingsProvider({ children }: { children: React.ReactNode }) {
  const [hoverPreviewDelayMs, setHoverPreviewDelayMsState] = useState(() => readStoredHoverPreviewDelayMs());
  const [ideaTimelineRowColorsEnabled, setIdeaTimelineRowColorsEnabledState] = useState(() => readStoredIdeaTimelineRowColorsEnabled());
  const [ideaTimelinePrimaryColor, setIdeaTimelinePrimaryColorState] = useState(() => readStoredIdeaTimelinePrimaryColor());
  const [ideaTimelineSupportingColor, setIdeaTimelineSupportingColorState] = useState(() => readStoredIdeaTimelineSupportingColor());

  const setHoverPreviewDelayMs = useCallback((delayMs: number) => {
    const normalized = normalizeHoverPreviewDelayMs(delayMs);
    writeStoredHoverPreviewDelayMs(normalized);
    setHoverPreviewDelayMsState(normalized);
  }, []);
  const setIdeaTimelineRowColorsEnabled = useCallback((enabled: boolean) => {
    writeStoredIdeaTimelineRowColorsEnabled(enabled);
    setIdeaTimelineRowColorsEnabledState(enabled);
  }, []);
  const setIdeaTimelinePrimaryColor = useCallback((color: string) => {
    const normalized = normalizeHexColor(color, DEFAULT_IDEA_TIMELINE_PRIMARY_COLOR);
    writeStoredIdeaTimelinePrimaryColor(normalized);
    setIdeaTimelinePrimaryColorState(normalized);
  }, []);
  const setIdeaTimelineSupportingColor = useCallback((color: string) => {
    const normalized = normalizeHexColor(color, DEFAULT_IDEA_TIMELINE_SUPPORTING_COLOR);
    writeStoredIdeaTimelineSupportingColor(normalized);
    setIdeaTimelineSupportingColorState(normalized);
  }, []);

  const refreshGuiSettings = useCallback(() => {
    setHoverPreviewDelayMsState(readStoredHoverPreviewDelayMs());
    setIdeaTimelineRowColorsEnabledState(readStoredIdeaTimelineRowColorsEnabled());
    setIdeaTimelinePrimaryColorState(readStoredIdeaTimelinePrimaryColor());
    setIdeaTimelineSupportingColorState(readStoredIdeaTimelineSupportingColor());
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") {
      return undefined;
    }
    const handleStorage = (event: StorageEvent) => {
      if (
        event.key === HOVER_PREVIEW_DELAY_STORAGE_KEY ||
        event.key === IDEA_TIMELINE_ROW_COLORS_ENABLED_STORAGE_KEY ||
        event.key === IDEA_TIMELINE_PRIMARY_COLOR_STORAGE_KEY ||
        event.key === IDEA_TIMELINE_SUPPORTING_COLOR_STORAGE_KEY ||
        event.key === null
      ) {
        refreshGuiSettings();
      }
    };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, [refreshGuiSettings]);

  const value = useMemo(
    () => ({
      hoverPreviewDelayMs,
      ideaTimelinePrimaryColor,
      ideaTimelineRowColorsEnabled,
      ideaTimelineSupportingColor,
      refreshGuiSettings,
      setHoverPreviewDelayMs,
      setIdeaTimelinePrimaryColor,
      setIdeaTimelineRowColorsEnabled,
      setIdeaTimelineSupportingColor,
    }),
    [
      hoverPreviewDelayMs,
      ideaTimelinePrimaryColor,
      ideaTimelineRowColorsEnabled,
      ideaTimelineSupportingColor,
      refreshGuiSettings,
      setHoverPreviewDelayMs,
      setIdeaTimelinePrimaryColor,
      setIdeaTimelineRowColorsEnabled,
      setIdeaTimelineSupportingColor,
    ],
  );

  return <GuiSettingsContext.Provider value={value}>{children}</GuiSettingsContext.Provider>;
}

export function useGuiSettings() {
  return useContext(GuiSettingsContext);
}

export function readStoredHoverPreviewDelayMs(storage: Storage | undefined = storageForBrowser()) {
  const stored = storage?.getItem(HOVER_PREVIEW_DELAY_STORAGE_KEY);
  if (stored === null || stored === undefined || !stored.trim()) {
    return DEFAULT_HOVER_PREVIEW_DELAY_MS;
  }
  return normalizeHoverPreviewDelayMs(Number(stored));
}

export function writeStoredHoverPreviewDelayMs(delayMs: number, storage: Storage | undefined = storageForBrowser()) {
  storage?.setItem(HOVER_PREVIEW_DELAY_STORAGE_KEY, String(normalizeHoverPreviewDelayMs(delayMs)));
}

export function readStoredIdeaTimelineRowColorsEnabled(storage: Storage | undefined = storageForBrowser()) {
  return storage?.getItem(IDEA_TIMELINE_ROW_COLORS_ENABLED_STORAGE_KEY) === "true";
}

export function writeStoredIdeaTimelineRowColorsEnabled(enabled: boolean, storage: Storage | undefined = storageForBrowser()) {
  storage?.setItem(IDEA_TIMELINE_ROW_COLORS_ENABLED_STORAGE_KEY, enabled ? "true" : "false");
}

export function readStoredIdeaTimelinePrimaryColor(storage: Storage | undefined = storageForBrowser()) {
  return normalizeHexColor(storage?.getItem(IDEA_TIMELINE_PRIMARY_COLOR_STORAGE_KEY), DEFAULT_IDEA_TIMELINE_PRIMARY_COLOR);
}

export function writeStoredIdeaTimelinePrimaryColor(color: string, storage: Storage | undefined = storageForBrowser()) {
  storage?.setItem(IDEA_TIMELINE_PRIMARY_COLOR_STORAGE_KEY, normalizeHexColor(color, DEFAULT_IDEA_TIMELINE_PRIMARY_COLOR));
}

export function readStoredIdeaTimelineSupportingColor(storage: Storage | undefined = storageForBrowser()) {
  return normalizeHexColor(storage?.getItem(IDEA_TIMELINE_SUPPORTING_COLOR_STORAGE_KEY), DEFAULT_IDEA_TIMELINE_SUPPORTING_COLOR);
}

export function writeStoredIdeaTimelineSupportingColor(color: string, storage: Storage | undefined = storageForBrowser()) {
  storage?.setItem(IDEA_TIMELINE_SUPPORTING_COLOR_STORAGE_KEY, normalizeHexColor(color, DEFAULT_IDEA_TIMELINE_SUPPORTING_COLOR));
}

export function normalizeHoverPreviewDelayMs(delayMs: number) {
  if (!Number.isFinite(delayMs)) {
    return DEFAULT_HOVER_PREVIEW_DELAY_MS;
  }
  return Math.min(MAX_HOVER_PREVIEW_DELAY_MS, Math.max(MIN_HOVER_PREVIEW_DELAY_MS, Math.round(delayMs)));
}

export function normalizeHexColor(color: string | null | undefined, fallback: string) {
  const value = String(color || "").trim();
  return /^#[0-9a-fA-F]{6}$/.test(value) ? value.toLowerCase() : fallback;
}

function storageForBrowser() {
  return typeof window === "undefined" ? undefined : window.localStorage;
}
