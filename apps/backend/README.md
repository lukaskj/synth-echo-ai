# Backend

Flask API for OmniVoice model loading, synthesis, voice cloning, saved clone settings, and saved conversations.

## Preferred Commands

Run these from the repo root:

```bash
bun run backend:setup
bun run backend:dev
```

`bun run backend:setup` creates `apps/backend/.venv` if needed and installs `requirements.txt`. It requires `python` on `PATH`.

Activate the backend virtual environment before installing PyTorch:

```powershell
# Windows
.\apps\backend\.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source ./apps/backend/.venv/bin/activate
```

`requirements.txt` does not install `torch` or `torchaudio`, so install PyTorch manually into the activated backend virtual environment before `bun run backend:dev`.

Examples:

```bash
# CPU-only or Apple Silicon
pip install torch torchaudio

# NVIDIA GPU: use the wheel that matches your CUDA version
pip install torch==2.11.0+cu128 torchaudio==2.11.0+cu128 --extra-index-url https://download.pytorch.org/whl/cu128

# Intel Arc / XPU
pip install torch==2.11.0+cu128 torchaudio==2.11.0+cu128 --index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/
```

See the [PyTorch install guide](https://pytorch.org/get-started/locally/) for the correct wheel for your hardware. The backend chooses the device in `tts_backend/config.py`: CUDA first, then MPS, then CPU.

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
- Generated audio files are served from `GET /api/v1/generated-audio/<filename>`.
- Conversation endpoints live under `/api/v1/conversations*`.
- Saved clone setting endpoints live under `/api/v1/settings/*`.
- A second `/load` while the model is loading returns `409`.
- `/synthesize` and `/clone` also return `409` until the model is loaded.

## Persistence

- Clone settings and conversations database: `apps/backend/data/clone_settings.sqlite3`
- Uploaded reference audio: `apps/backend/storage/clone_settings/`
- Generated audio: `apps/backend/storage/generated_audio/`

There is no standalone migration system. Schema creation and the current inline column/path migration both live in `tts_backend/repositories/clone_settings_repository.py`.

## Caveats

- `.env` files are not auto-loaded.
- Device selection happens in `tts_backend/config.py`, not `constants.py`.
