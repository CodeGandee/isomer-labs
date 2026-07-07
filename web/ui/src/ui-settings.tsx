import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";

export const DEFAULT_HOVER_PREVIEW_DELAY_MS = 1500;
export const MIN_HOVER_PREVIEW_DELAY_MS = 250;
export const MAX_HOVER_PREVIEW_DELAY_MS = 5000;

const HOVER_PREVIEW_DELAY_STORAGE_KEY = "isomer-web-hover-preview-delay-ms";

type GuiSettingsContextValue = {
  hoverPreviewDelayMs: number;
  refreshGuiSettings: () => void;
  setHoverPreviewDelayMs: (delayMs: number) => void;
};

const GuiSettingsContext = createContext<GuiSettingsContextValue>({
  hoverPreviewDelayMs: DEFAULT_HOVER_PREVIEW_DELAY_MS,
  refreshGuiSettings: () => undefined,
  setHoverPreviewDelayMs: () => undefined,
});

export function GuiSettingsProvider({ children }: { children: React.ReactNode }) {
  const [hoverPreviewDelayMs, setHoverPreviewDelayMsState] = useState(() => readStoredHoverPreviewDelayMs());

  const setHoverPreviewDelayMs = useCallback((delayMs: number) => {
    const normalized = normalizeHoverPreviewDelayMs(delayMs);
    writeStoredHoverPreviewDelayMs(normalized);
    setHoverPreviewDelayMsState(normalized);
  }, []);

  const refreshGuiSettings = useCallback(() => {
    setHoverPreviewDelayMsState(readStoredHoverPreviewDelayMs());
  }, []);

  useEffect(() => {
    if (typeof window === "undefined") {
      return undefined;
    }
    const handleStorage = (event: StorageEvent) => {
      if (event.key === HOVER_PREVIEW_DELAY_STORAGE_KEY || event.key === null) {
        refreshGuiSettings();
      }
    };
    window.addEventListener("storage", handleStorage);
    return () => window.removeEventListener("storage", handleStorage);
  }, [refreshGuiSettings]);

  const value = useMemo(() => ({ hoverPreviewDelayMs, refreshGuiSettings, setHoverPreviewDelayMs }), [hoverPreviewDelayMs, refreshGuiSettings, setHoverPreviewDelayMs]);

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

export function normalizeHoverPreviewDelayMs(delayMs: number) {
  if (!Number.isFinite(delayMs)) {
    return DEFAULT_HOVER_PREVIEW_DELAY_MS;
  }
  return Math.min(MAX_HOVER_PREVIEW_DELAY_MS, Math.max(MIN_HOVER_PREVIEW_DELAY_MS, Math.round(delayMs)));
}

function storageForBrowser() {
  return typeof window === "undefined" ? undefined : window.localStorage;
}
