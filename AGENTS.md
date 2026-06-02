# AGENTS.md

## Sources Of Truth
- Prefer executable sources over prose: root `package.json`, `scripts/back-*.ts`, `apps/frontend/package.json`, `apps/frontend/{vite.config.ts,svelte.config.js,eslint.config.js}`, and backend code under `apps/backend/tts_backend/`.
- Run Bun from the repo root. `bun install` runs `bun run backend:setup`, so `python` must be on `PATH` and `apps/backend/.venv` will be created or refreshed.
- `bun run backend:setup` installs `apps/backend/requirements.txt` only. It does not install PyTorch, so keep the manual `torch` / `torchaudio` install step in the READMEs if setup changes.
- When setup, commands, env behavior, or app structure changes, update `README.md` and the relevant app README in the same change.

## Repo Shape
- Repo = static SvelteKit frontend in `apps/frontend` plus Flask API in `apps/backend`.
- Only `apps/frontend` is a Bun workspace package. Use the root backend scripts instead of treating `apps/backend` as a workspace package.
- `apps/frontend/src/routes/+page.svelte` is a thin wrapper; the real UI lives under `apps/frontend/src/lib/tts/`, with `components/TtsWorkspace.svelte` as the top-level feature component.
- Frontend HTTP calls are centralized in `apps/frontend/src/lib/tts/api.ts`; shared API paths/default backend URL live in `constants.ts`, and URL/error helpers live in `helpers.ts`.
- `apps/backend/app.py` only boots Flask. App wiring is in `apps/backend/tts_backend/factory.py`; route behavior is in `apps/backend/tts_backend/routes.py`.

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
- Keep the frontend static unless deployment assumptions are changing: `@sveltejs/adapter-static` is enabled, `src/routes/+layout.ts` sets `prerender = true`, and `svelte.config.js` prerenders `'/api/mock-tts'`.
- App code is forced into Svelte 5 runes mode in `apps/frontend/svelte.config.js`; do not introduce legacy Svelte APIs.
- Browser code talks directly to Flask via `PUBLIC_BACKEND_BASE_URL`; default is `http://127.0.0.1:5000`.
- `apps/frontend/src/routes/api/mock-tts/+server.ts` is the prerendered mock endpoint for UI work without the Flask backend.
- Tailwind is configured through `@tailwindcss/vite` plus `src/routes/layout.css`; there is no `tailwind.config.*`.
- Vitest is split in `vite.config.ts`: `*.svelte.{test,spec}.*` runs in Playwright/Chromium, everything else runs in Node. Browser specs need Playwright browsers installed.

## Backend Gotchas
- Flask routes are mounted under `/api/v1`, not `/api`.
- Model state matters: a second `/load` while loading returns `409`, and `/synthesize` / `/clone` return `409` until the model is loaded.
- Clone settings persist in `apps/backend/data/clone_settings.sqlite3`; uploaded reference audio persists in `apps/backend/storage/clone_settings/`.
- There is no standalone migration system. Schema creation and the inline column/path migration live in `apps/backend/tts_backend/repositories/clone_settings_repository.py`.
- The backend does not auto-load `.env` files.
- Device selection lives in `apps/backend/tts_backend/config.py`: CUDA first, then MPS, then CPU. Do not rely on the old hardcoded-device assumption.

## Runtime Artifacts
- Ignore `apps/backend/.venv/`, `apps/backend/data/`, `apps/backend/storage/`, `apps/frontend/.svelte-kit/`, `apps/frontend/build/`, `apps/frontend/dist/`, `apps/frontend/artifacts/`, and `node_modules/`.
