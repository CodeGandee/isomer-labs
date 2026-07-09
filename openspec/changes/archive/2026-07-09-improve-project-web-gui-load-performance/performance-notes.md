## Performance Notes

Validation date: 2026-07-09.

## Build Output

`npm run build` now emits content-hashed asset names under `src/isomer_labs/web/static/assets`.

Key first-load assets after lazy boundaries:

- `index-DBj-2qfF.js`: 1,063.32 kB, gzip 295.42 kB
- `index-DuY2Vi6T.css`: 200.26 kB, gzip 24.01 kB
- `markdown-view-BNWMBVqz.js`: 409.49 kB, gzip 123.18 kB, loaded on demand
- `markdown-view-BYZTj3zW.css`: 29.29 kB, gzip 8.05 kB, loaded with Markdown
- `IdeaTimelinePanel-Cl9d4vbf.js`: 7.54 kB, gzip 2.96 kB, loaded on demand
- `IdeaLineagePanel-C8trxv8h.js`: 1,770.40 kB, gzip 532.21 kB, loaded on demand
- `mermaid.core-pD9FYNUz.js`: 584.27 kB, gzip 136.59 kB, loaded only when Mermaid rendering is needed

The previous measured first-load `app.js` was about 3.9 MB uncompressed. The normal shell entry is now about 1.06 MB uncompressed and about 295 kB over gzip.

## Normal Versus Debug Launch

Temporary normal launch:

```bash
pixi run isomer-cli project web serve --root /data/ssd1/huangzhe/code/isomer-labs --host 127.0.0.1 --port 8876 --no-browser
```

Representative normal asset response:

- `X-Isomer-Web-Cache-Mode: normal`
- `Cache-Control: public, max-age=31536000, immutable`
- `Content-Encoding: gzip`
- `Server-Timing: app;dur=10.0`
- `index-DBj-2qfF.js` encoded size: 294,044 bytes

Temporary debug launch:

```bash
pixi run isomer-cli project web serve --root /data/ssd1/huangzhe/code/isomer-labs --host 127.0.0.1 --port 8877 --no-browser --cache-mode debug
```

Representative debug asset/API response:

- `X-Isomer-Web-Cache-Mode: debug`
- `Cache-Control: no-store, no-cache, must-revalidate, max-age=0`
- `Pragma: no-cache`
- `Expires: 0`
- `Content-Encoding: gzip` for eligible assets
- `/api/health` reports `"cache_mode": "debug"`

## Playwright Smoke

Command:

```bash
ISOMER_WEB_BASE_URL=http://127.0.0.1:8876 npm run test:performance
```

Result:

- DOM content loaded: 773 ms
- Shell visible: 858 ms
- Budget: 12,000 ms
- Hashed assets observed: 2
- Immutable hashed assets: 2
- Gzip assets: 2
- API responses with `Server-Timing`: 3
- Failed requests: 0
- API failures: 0
