export function topicRelativeDisplayPath(
  value: unknown,
  options: { topicId?: string | null; topicWorkspacePath?: string | null } = {},
): string {
  if (typeof value !== "string" || value.length === 0) {
    return value == null ? "" : String(value);
  }

  const normalizedValue = normalizePath(value);
  const workspacePath = options.topicWorkspacePath ? normalizePath(options.topicWorkspacePath) : "";
  if (workspacePath) {
    const stripped = stripPrefix(normalizedValue, workspacePath);
    if (stripped !== null) {
      return stripped;
    }
  }

  const topicId = options.topicId || "";
  if (topicId) {
    const marker = `/topic-ws/${topicId}/`;
    const markerIndex = normalizedValue.indexOf(marker);
    if (markerIndex >= 0) {
      return normalizedValue.slice(markerIndex + marker.length);
    }
  }

  return value;
}

function normalizePath(value: string): string {
  return value.replaceAll("\\", "/").replace(/\/+$/, "");
}

function stripPrefix(value: string, prefix: string): string | null {
  if (value === prefix) {
    return ".";
  }
  const withSlash = `${prefix}/`;
  return value.startsWith(withSlash) ? value.slice(withSlash.length) : null;
}
