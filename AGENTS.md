# AGENTS.md

## Trust These
- Prefer executable sources: root `package.json`, `scripts/back-setup.ts`, `scripts/python.ts`, `apps/frontend/package.json`, `apps/frontend/{vite.config.ts,svelte.config.js,eslint.config.js}`, and backend code under `apps/backend/tts_backend/`.
- Current `README*` files are partly stale. They still mention `bun run frontend:dev`, `bun run backend:dev`, and `scripts/back-run.ts`, but those do not exist in the current repo.

## Commands
- Run Bun from the repo root.
- `bun install` runs `bun run backend:setup`; `python` must be on `PATH`.
- `bun run backend:setup` creates or refreshes `apps/backend/.venv` and installs only `apps/backend/requirements.txt`; it does not install `torch` or `torchaudio`.
- Frontend dev: `bun run frontend`
- Frontend lint: `bun run --cwd apps/frontend lint`
- Frontend typecheck: `bun run --cwd apps/frontend check`
- Frontend build: `bun run --cwd apps/frontend build`
- Frontend format: `bun run --cwd apps/frontend format`
- Frontend tests: `bun run --cwd apps/frontend test:unit -- --run`
- Single frontend test: `bun run --cwd apps/frontend test:unit -- --run path/to/spec.ts`
- Combined lint: `bun run lint:all`
- Backend dev: `bun run backend`
- Backend quick verify from `apps/backend`: `python -m compileall app.py tts_backend`

## Structure
- Only `apps/frontend` is a Bun workspace package. Treat `apps/backend` as a plain Python app driven by the root Bun scripts.
- Frontend route files are thin wrappers: `apps/frontend/src/routes/+page.svelte`, `apps/frontend/src/routes/conversation/+page.svelte`, and `apps/frontend/src/routes/conversation/[conversationId]/+page.svelte`. The real UI lives under `apps/frontend/src/lib/tts/components/`.
- Frontend HTTP calls are centralized in `apps/frontend/src/lib/tts/api.ts`; shared API paths and the default backend URL live in `constants.ts`; URL/error helpers live in `helpers.ts`.
- `apps/backend/app.py` only boots Flask. App wiring is in `apps/backend/tts_backend/factory.py`; request handling is in `apps/backend/tts_backend/routes.py`.

## Frontend
- The app is intentionally static: `@sveltejs/adapter-static` uses `fallback: '200.html'`, and `apps/frontend/src/routes/+layout.ts` sets `prerender = true`.
- `apps/frontend/src/routes/api/mock-tts/+server.ts` is prerendered and returns canned audio for UI work without Flask.
- App code is forced into Svelte 5 runes mode in `apps/frontend/svelte.config.js`; do not introduce legacy Svelte APIs.
- Tailwind is configured through `@tailwindcss/vite` and `apps/frontend/src/routes/layout.css`; there is no `tailwind.config.*`.
- Browser code talks directly to Flask via `PUBLIC_BACKEND_BASE_URL`; the default is `http://127.0.0.1:5000`.
- `apps/frontend/vite.config.ts` splits Vitest by file type: `*.svelte.{test,spec}.*` runs in Playwright/Chromium, everything else runs in Node.
- `apps/frontend/vite.config.ts` sets `expect: { requireAssertions: true }`; every test needs at least one assertion.
- Current frontend tests are only starter examples in `apps/frontend/src/lib/vitest-examples/`.

### Frontend Component Guidelines 
- Pages should primarily compose components and manage page-level concerns.
- Extract distinct UI sections into separate components by default.
- Avoid large blocks inside page files.
- If a page contains multiple visual sections, create separate components for them.
- Favor separation of concerns, readability, and reusability over minimizing the number of files.
- Use svelte-code-writer and svelte-core-bestpractices skills when creating or updating svelte components.

## Backend
- API routes are mounted under `/api/v1`, not `/api`.
- First `POST /api/v1/load` downloads `k2-fsa/OmniVoice`; it needs internet and can take several minutes.
- Model state is strict: a second `/load` while loading returns `409`; `/synthesize` and `/clone` return `409` until the model is loaded; `/unload` also returns `409` while loading.
- Generated audio is saved under `apps/backend/storage/generated_audio/`, and synth/clone endpoints return `audio_url` values instead of raw audio bytes.
- Clone settings and conversations share `apps/backend/data/clone_settings.sqlite3`; uploaded reference audio lives in `apps/backend/storage/clone_settings/`.
- There is no standalone migration system. Clone-setting schema/path migration lives in `apps/backend/tts_backend/repositories/clone_settings_repository.py`; conversation table creation lives in `apps/backend/tts_backend/repositories/conversation_repository.py`.
- `ref_audio` and `ref_text` are immutable after clone setting creation; `POST /settings/update-clone/<id>` rejects both with `400`.
- Device selection in `apps/backend/tts_backend/config.py` is CUDA -> MPS -> CPU.

## Artifacts
- Ignore `apps/backend/.venv/`, `apps/backend/data/`, `apps/backend/storage/`, `apps/frontend/.svelte-kit/`, `apps/frontend/build/`, `apps/frontend/dist/`, `apps/frontend/artifacts/`, and `node_modules/`.
- If you change setup, commands, or app structure, update `README.md` and the affected app README in the same change.
