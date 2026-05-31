# @lukaskj/omni-clone

Monorepo for an OmniVoice-based text-to-speech and voice cloning app with a SvelteKit frontend and Flask backend.

## Repo Layout

- `apps/frontend`: static SvelteKit app.
- `apps/backend`: Flask API and Python model integration.
- `scripts/back-setup.ts`: creates or refreshes the backend virtual environment and installs `requirements.txt`.
- `scripts/back-run.ts`: runs the backend with the venv Python.

## Quick Start

`bun install` must be run from the repo root. It also runs `bun run backend:setup`, so `python` must be available on `PATH`.

```bash
bun install
```

Run the backend and frontend in separate terminals:

```bash
bun run backend:dev
```

```bash
bun run frontend:dev
```

Frontend dev server: Vite default host/port.

Backend API base URL: `http://127.0.0.1:5000`

## Common Commands

### Frontend

```bash
bun run frontend:dev
bun run --cwd apps/frontend lint
bun run --cwd apps/frontend check
bun run --cwd apps/frontend build
bun run --cwd apps/frontend test:unit -- --run
```

Run a single frontend test file:

```bash
bun run --cwd apps/frontend test:unit -- --run path/to/spec.ts
```

### Backend

```bash
bun run backend:setup
bun run backend:dev
```

Lightweight backend verification from `apps/backend`:

```bash
python -m compileall app.py tts_backend
```

## Runtime Notes

- Frontend browser code calls Flask directly via `PUBLIC_BACKEND_BASE_URL`. If unset, it defaults to `http://127.0.0.1:5000`.
- Backend routes are mounted under `/api/v1`.
- Voice clone settings persist in `apps/backend/data/clone_settings.sqlite3` and uploaded reference audio persists in `apps/backend/storage/clone_settings/`.
- The backend currently hardcodes `MODEL_DEVICE_MAP = "cuda:0"` in `apps/backend/tts_backend/constants.py`, so CPU-only development will fail unless that is changed.

## More Detail

- Frontend details: [`apps/frontend/README.md`](apps/frontend/README.md)
- Backend details: [`apps/backend/README.md`](apps/backend/README.md)
