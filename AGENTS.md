# AGENTS.md

## Trust These Sources
- README files are partially stale. Trust `package.json`, `scripts/back-*.ts`, and `apps/frontend/{package.json,vite.config.ts,svelte.config.js}` over README command examples.
- Use Bun at the repo root. `bun install` is not frontend-only: root `postinstall` runs `bun run backend:setup`, so installs require `python` on `PATH` and will create/update `apps/backend/.venv`.

## Repo Shape
- Only `apps/frontend` is a Bun workspace package. The Flask backend in `apps/backend` is managed by root scripts, not workspace commands.
- Current integration is minimal: `apps/backend/app.py` only serves `GET /api/hello`, and the frontend does not currently call the backend.

## Frontend
- The real app entrypoints are `apps/frontend/src/routes/*`. It is SvelteKit 2 with `@sveltejs/adapter-static`, and `src/routes/+layout.ts` sets `prerender = true`; treat it as a fully static site unless you intentionally change deployment assumptions.
- `apps/frontend/svelte.config.js` forces Svelte 5 runes mode for app code. Follow rune syntax instead of legacy Svelte component APIs.
- Tailwind uses v4's Vite plugin plus `src/routes/layout.css`; there is no `tailwind.config.*`.
- Useful commands:
  - dev: `bun run frontend:dev`
  - typecheck: `bun run --cwd apps/frontend check`
  - build: `bun run --cwd apps/frontend build`
  - focused Node-side tests: `bun run --cwd apps/frontend test:unit -- --project server --run`
  - single test file: `bun run --cwd apps/frontend test:unit -- --run src/lib/vitest-examples/greet.spec.ts`
- Vitest is split in `apps/frontend/vite.config.ts`: `*.svelte.spec.ts` runs in the Playwright browser project, other specs run in Node. Full `test` / `test:unit` currently fails if Playwright browsers are not installed.
- Ignore root `frontend:start`; it points to a nonexistent `start` script. Use `bun run --cwd apps/frontend preview` after `build` for a production preview.
- No lint or formatter command is configured; `check` is the main automated frontend static verification.

## Backend
- Use root scripts instead of manually activating the venv:
  - setup/update deps: `bun run backend:setup`
  - run dev server: `bun run backend:dev`
- The live launcher is `scripts/back-run.ts`; `apps/backend/back-run.ts` is not referenced by root scripts.
- There is no backend test, lint, or typecheck config yet. Current verification is starting the server and checking `http://127.0.0.1:5000/api/hello`.
- An `apps/backend/.env` file may exist, but `requirements.txt` does not include `python-dotenv`; do not assume `.env` values are loaded automatically.

## Search Noise
- Exclude local/generated directories from searches and edits: `apps/backend/.venv/`, `apps/frontend/.svelte-kit/`, `apps/frontend/build/`, `node_modules/`.
