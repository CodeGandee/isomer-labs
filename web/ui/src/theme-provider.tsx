import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import {
  applyThemeMode,
  readStoredThemeMode,
  resolveThemeMode,
  subscribeToSystemTheme,
  writeStoredThemeMode,
  type ResolvedThemeMode,
  type ThemeMode,
} from "./theme-mode";

type ThemeContextValue = {
  themeMode: ThemeMode;
  resolvedThemeMode: ResolvedThemeMode;
  setThemeMode: (mode: ThemeMode) => void;
};

const ThemeContext = createContext<ThemeContextValue>({
  themeMode: "system",
  resolvedThemeMode: "light",
  setThemeMode: () => undefined,
});

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [themeMode, setThemeModeState] = useState<ThemeMode>(() => readStoredThemeMode());
  const [resolvedThemeMode, setResolvedThemeMode] = useState<ResolvedThemeMode>(() => resolveThemeMode(readStoredThemeMode()));

  const setThemeMode = useCallback((mode: ThemeMode) => {
    writeStoredThemeMode(mode);
    setThemeModeState(mode);
  }, []);

  useEffect(() => {
    const refreshTheme = () => setResolvedThemeMode(applyThemeMode(themeMode));
    refreshTheme();
    if (themeMode !== "system") {
      return undefined;
    }
    return subscribeToSystemTheme(refreshTheme);
  }, [themeMode]);

  const value = useMemo(() => ({ themeMode, resolvedThemeMode, setThemeMode }), [resolvedThemeMode, setThemeMode, themeMode]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useGuiTheme() {
  return useContext(ThemeContext);
}
