#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -f "$REPO_ROOT/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  source "$REPO_ROOT/.env"
  set +a
fi

KIMI_BASE_URL="${CLAUDE_KIMI_ANTHROPIC_BASE_URL:-https://api.kimi.com/coding/}"
KIMI_API_KEY="${CLAUDE_KIMI_ANTHROPIC_API_KEY:-}"
KIMI_MODEL="${CLAUDE_KIMI_MODEL:-kimi-for-coding}"
COMPACT_WINDOW="${CLAUDE_KIMI_AUTO_COMPACT_WINDOW:-262144}"

KIMI_API_KEY_TRIMMED="${KIMI_API_KEY//[[:space:]]/}"
if [ -z "$KIMI_API_KEY_TRIMMED" ] || [ "$KIMI_API_KEY" = "<your-kimi-api-key>" ]; then
  echo "CLAUDE_KIMI_ANTHROPIC_API_KEY is missing or empty." >&2
  echo "Copy .env.example to .env, fill CLAUDE_KIMI_ANTHROPIC_API_KEY with a real Kimi key, and keep .env uncommitted." >&2
  exit 2
fi

CLAUDE_BIN=""
for candidate in "$HOME"/.nvm/versions/node/*/bin/claude "$HOME"/.bun/bin/claude "$HOME"/.local/bin/claude; do
  if [ -x "$candidate" ]; then
    CLAUDE_BIN="$candidate"
    break
  fi
done
if [ -z "$CLAUDE_BIN" ]; then
  CLAUDE_BIN="$(command -v claude || true)"
fi
if [ -z "$CLAUDE_BIN" ]; then
  echo "claude binary not found" >&2
  exit 127
fi

FILTERED_ARGS=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --model|--permission-mode)
      shift
      [ "$#" -gt 0 ] && shift
      ;;
    --model=*|--permission-mode=*)
      shift
      ;;
    --help|-h|--version|-v)
      exec "$CLAUDE_BIN" "$@"
      ;;
    *)
      FILTERED_ARGS+=("$1")
      shift
      ;;
  esac
done

unset ANTHROPIC_AUTH_TOKEN CLAUDE_CODE_OAUTH_TOKEN ANTHROPIC_MODEL CLAUDE_MODEL TEST_KIMI_KEY
export ANTHROPIC_BASE_URL="$KIMI_BASE_URL"
export ANTHROPIC_API_KEY="$KIMI_API_KEY"
export CLAUDE_CODE_AUTO_COMPACT_WINDOW="$COMPACT_WINDOW"

exec "$CLAUDE_BIN" --dangerously-skip-permissions --model "$KIMI_MODEL" "${FILTERED_ARGS[@]}"
