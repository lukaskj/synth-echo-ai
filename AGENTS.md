# AGENTS.md

## Trust Code, Not Docs
- `README.md` and `apps/frontend/README.md` are stale/template content. Trust root `package.json`, `scripts/back-*.ts`, `apps/frontend/package.json`, `apps/frontend/{vite.config.ts,svelte.config.js}`, and backend code under `apps/backend/tts_backend/`.
- Run Bun from the repo root. `bun install` also runs `bun run backend:setup`, so it requires `python` on `PATH` and creates or updates `apps/backend/.venv`.

## Repo Shape
- Repo = static SvelteKit frontend in `apps/frontend` plus Flask API in `apps/backend`.
- Only `apps/frontend` is a Bun workspace package. Manage the backend through the root scripts, not as a workspace package.
- `apps/backend/app.py` only boots the app; the real backend wiring is in `apps/backend/tts_backend/factory.py` and `routes.py`.
- Frontend API paths live in `apps/frontend/src/lib/tts/constants.ts`; base URL and endpoint helpers live in `apps/frontend/src/lib/tts/helpers.ts`.

## Commands
- Frontend dev: `bun run frontend:dev`
- Frontend typecheck: `bun run --cwd apps/frontend check`
- Frontend build: `bun run --cwd apps/frontend build`
- Frontend tests: `bun run --cwd apps/frontend test:unit -- --run`
- Single frontend test file: `bun run --cwd apps/frontend test:unit -- --run path/to/spec.ts`
- Backend deps / venv refresh: `bun run backend:setup`
- Backend dev server: `bun run backend:dev`
- Lightweight backend verification from `apps/backend`: `python -m compileall app.py tts_backend`
- `bun run frontend:start` is broken: root `package.json` points to an `apps/frontend` `start` script that does not exist.

## Frontend Gotchas
- Keep the frontend static unless you intentionally change deployment assumptions: `@sveltejs/adapter-static` is enabled, `src/routes/+layout.ts` sets `prerender = true`, and `svelte.config.js` prerenders `'/api/mock-tts'`.
- App code is forced into Svelte 5 runes mode in `apps/frontend/svelte.config.js`; do not use legacy component APIs.
- Browser code calls Flask directly via `PUBLIC_BACKEND_BASE_URL`, default `http://127.0.0.1:5000`.
- Tailwind is configured through the Vite plugin and `src/routes/layout.css`; there is no `tailwind.config.*`.
- `apps/frontend/src/routes/api/mock-tts/+server.ts` is a prerendered mock endpoint for UI work without the Flask backend.
- Vitest is split by project: `*.svelte.{test,spec}.*` runs in Playwright/Chromium, non-Svelte tests run in Node. Browser specs need Playwright browsers installed.
- The only current frontend tests are starter examples under `apps/frontend/src/lib/vitest-examples/`; they are not meaningful app coverage.
- Prefer extending `apps/frontend/src/lib/tts/` instead of adding more logic to the already-large `apps/frontend/src/routes/+page.svelte`.

## Backend Gotchas
- Flask routes are mounted under `/api/v1`.
- Model state matters: a second load request while loading returns `409`, and synthesize/clone also return `409` until the model is loaded.
- Clone settings persist in `apps/backend/data/clone_settings.sqlite3`; reference audio persists in `apps/backend/storage/clone_settings/`.
- The clone-settings table and inline column migration live in `apps/backend/tts_backend/repositories/clone_settings_repository.py`; there is no migration system.
- The backend does not auto-load `.env`; `python-dotenv` is not installed.
- `apps/backend/tts_backend/constants.py` hardcodes `MODEL_DEVICE_MAP = "cuda:0"`; CPU-only work will fail unless that code is changed.

## Ignore
- Ignore `apps/backend/.venv/`, `apps/backend/data/`, `apps/backend/storage/`, `apps/frontend/.svelte-kit/`, `apps/frontend/build/`, and `node_modules/`.
