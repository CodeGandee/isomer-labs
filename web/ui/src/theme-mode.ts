export type ThemeMode = "light" | "dark" | "system";
export type ResolvedThemeMode = "light" | "dark";

const THEME_STORAGE_KEY = "isomer-web-gui-theme";

export function readStoredThemeMode(storage: Storage | undefined = storageForBrowser()): ThemeMode {
  const stored = storage?.getItem(THEME_STORAGE_KEY);
  return isThemeMode(stored) ? stored : "system";
}

export function writeStoredThemeMode(mode: ThemeMode, storage: Storage | undefined = storageForBrowser()) {
  storage?.setItem(THEME_STORAGE_KEY, mode);
}

export function resolveThemeMode(mode: ThemeMode, media: Pick<MediaQueryList, "matches"> | undefined = systemDarkMedia()): ResolvedThemeMode {
  if (mode === "system") {
    return media?.matches ? "dark" : "light";
  }
  return mode;
}

export function applyThemeMode(mode: ThemeMode, root: HTMLElement | undefined = documentRoot()) {
  const resolved = resolveThemeMode(mode);
  root?.classList.toggle("dark", resolved === "dark");
  root?.setAttribute("data-theme", resolved);
  root?.setAttribute("data-theme-mode", mode);
  return resolved;
}

export function subscribeToSystemTheme(callback: () => void) {
  const media = systemDarkMedia();
  if (!media) {
    return () => undefined;
  }
  media.addEventListener("change", callback);
  return () => media.removeEventListener("change", callback);
}

function isThemeMode(value: string | null | undefined): value is ThemeMode {
  return value === "light" || value === "dark" || value === "system";
}

function storageForBrowser() {
  return typeof window === "undefined" ? undefined : window.localStorage;
}

function systemDarkMedia() {
  return typeof window === "undefined" ? undefined : window.matchMedia("(prefers-color-scheme: dark)");
}

function documentRoot() {
  return typeof document === "undefined" ? undefined : document.documentElement;
}
