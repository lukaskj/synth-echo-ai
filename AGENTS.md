# AGENTS.md

## Trust Sources Of Truth
- `README.md`, `apps/frontend/README.md`, and `apps/backend/README.md` are maintained entry docs, but if they conflict with code or scripts, trust root `package.json`, `scripts/back-*.ts`, `apps/frontend/package.json`, `apps/frontend/{vite.config.ts,svelte.config.js,eslint.config.js}`, and backend code under `apps/backend/tts_backend/`.
- Run Bun from the repo root. `bun install` triggers `bun run backend:setup`, so it requires `python` on `PATH` and creates or refreshes `apps/backend/.venv`.
- When changes affect setup, commands, architecture, env behavior, or user-facing workflows, update the relevant README files in the same change.

## Repo Shape
- Repo = static SvelteKit frontend in `apps/frontend` plus Flask API in `apps/backend`.
- Only `apps/frontend` is a Bun workspace package. Manage backend tasks through the root scripts instead of treating `apps/backend` as a workspace package.
- `apps/frontend/src/routes/+page.svelte` is just a wrapper; the real UI lives in `apps/frontend/src/lib/tts/components/TtsWorkspace.svelte` and related code under `apps/frontend/src/lib/tts/`.
- Frontend API access is centralized in `apps/frontend/src/lib/tts/api.ts`; paths/constants live in `apps/frontend/src/lib/tts/constants.ts` and URL helpers in `apps/frontend/src/lib/tts/helpers.ts`.
- `apps/backend/app.py` is only the Flask boot entrypoint. Actual app wiring is in `apps/backend/tts_backend/factory.py`; route behavior is in `apps/backend/tts_backend/routes.py`.

## Commands
- Frontend dev: `bun run frontend:dev`
- Frontend lint: `bun run --cwd apps/frontend lint`
- Frontend typecheck: `bun run --cwd apps/frontend check`
- Frontend build: `bun run --cwd apps/frontend build`
- Frontend format: `bun run --cwd apps/frontend format`
- Frontend tests: `bun run --cwd apps/frontend test:unit -- --run`
- Single frontend test file: `bun run --cwd apps/frontend test:unit -- --run path/to/spec.ts`
- Backend venv/deps refresh: `bun run backend:setup`
- Backend dev server: `bun run backend:dev`
- Lightweight backend verification from `apps/backend`: `python -m compileall app.py tts_backend`
- Do not use `bun run frontend:start`; the root script points to a nonexistent `apps/frontend start` script.

## Frontend Gotchas
- Keep the frontend static unless you intentionally change deployment assumptions: `@sveltejs/adapter-static` is enabled, `src/routes/+layout.ts` sets `prerender = true`, and `svelte.config.js` prerenders `'/api/mock-tts'`.
- App code is forced into Svelte 5 runes mode in `apps/frontend/svelte.config.js`; do not introduce legacy Svelte APIs.
- Browser code talks directly to Flask via `PUBLIC_BACKEND_BASE_URL`; default is `http://127.0.0.1:5000`.
- Tailwind is configured through the Vite plugin plus `src/routes/layout.css`; there is no `tailwind.config.*`.
- `apps/frontend/src/routes/api/mock-tts/+server.ts` is a prerendered mock endpoint for UI work when the Flask backend is unavailable.
- Vitest is split by project in `vite.config.ts`: `*.svelte.{test,spec}.*` runs in Playwright/Chromium, non-Svelte tests run in Node. Browser specs need Playwright browsers installed.
- Current frontend tests are only starter examples under `apps/frontend/src/lib/vitest-examples/`; they are not meaningful app coverage.
- Pages should primarily compose components and manage page-level concerns.
- Extract distinct UI sections into separate components by default.
- Avoid large blocks inside page files.
- If a page contains multiple visual sections, create separate components for them.
- Favor separation of concerns, readability, and reusability over minimizing the number of files.

## Backend Gotchas
- Flask routes are mounted under `/api/v1`, not `/api`.
- Model state matters: a second `/load` while loading returns `409`, and `/synthesize` and `/clone` also return `409` until the model is loaded.
- Clone settings persist in `apps/backend/data/clone_settings.sqlite3`; uploaded reference audio persists in `apps/backend/storage/clone_settings/`.
- There is no migration system. Schema creation and the inline column/path migration live in `apps/backend/tts_backend/repositories/clone_settings_repository.py`.
- The backend does not auto-load `.env`; `python-dotenv` is not installed.
- `apps/backend/tts_backend/constants.py` hardcodes `MODEL_DEVICE_MAP = "cuda:0"`; CPU-only development fails unless that code is changed.

## Ignore
- Ignore `apps/backend/.venv/`, `apps/backend/data/`, `apps/backend/storage/`, `apps/frontend/.svelte-kit/`, `apps/frontend/build/`, `apps/frontend/dist/`, `apps/frontend/artifacts/`, and `node_modules/`.
