# Backend

Flask API for OmniVoice model loading, synthesis, voice cloning, and saved clone settings.

## Preferred Commands

Run these from the repo root:

```bash
bun run backend:setup
bun run backend:dev
```

`bun run backend:setup` creates `apps/backend/.venv` if needed and installs `requirements.txt`. It requires `python` on `PATH`.

The dev server listens on `http://127.0.0.1:5000`.

## Direct Verification

From `apps/backend`:

```bash
python -m compileall app.py tts_backend
```

## Structure

- `app.py` creates the Flask app and registers shutdown handlers.
- `tts_backend/factory.py` wires the model service, clone settings service, storage, CORS, and API blueprint.
- `tts_backend/routes.py` contains the HTTP route behavior.
- `tts_backend/repositories/clone_settings_repository.py` owns SQLite schema creation and inline data migration.

## API Notes

- All routes are mounted under `/api/v1`.
- Health/demo route: `GET /api/v1/hello`
- Model lifecycle: `POST /api/v1/load`, `POST /api/v1/unload`
- Generation: `POST /api/v1/synthesize`, `POST /api/v1/clone`
- Saved clone setting endpoints live under `/api/v1/settings/*`.
- A second `/load` while the model is loading returns `409`.
- `/synthesize` and `/clone` also return `409` until the model is loaded.

## Persistence

- Clone settings database: `apps/backend/data/clone_settings.sqlite3`
- Uploaded reference audio: `apps/backend/storage/clone_settings/`

There is no standalone migration system. Schema creation and the current inline column/path migration both live in `tts_backend/repositories/clone_settings_repository.py`.

## Caveats

- `.env` files are not auto-loaded.
- `tts_backend/constants.py` hardcodes `MODEL_DEVICE_MAP = "cuda:0"`, so CPU-only development will fail unless that is changed.
