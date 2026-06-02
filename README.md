# @lukaskj/omni-clone

Monorepo for an OmniVoice-based text-to-speech and voice cloning app with a static SvelteKit frontend and Flask backend.

## Quick Start

1. Install repo dependencies from the repo root:

```bash
bun install
```

`bun install` runs `bun run backend:setup`, so `python` must be on `PATH`. That step creates or refreshes `apps/backend/.venv` and installs `apps/backend/requirements.txt`.

2. Activate the backend virtual environment.

```powershell
# Windows
.\apps\backend\.venv\Scripts\Activate.ps1
```

```bash
# macOS/Linux
source ./apps/backend/.venv/bin/activate
```

3. Install PyTorch manually into the activated backend virtual environment.

`apps/backend/requirements.txt` does not install `torch` or `torchaudio`, so the backend will not load the model until you add them yourself.

Examples:

```bash
# CPU-only or Apple Silicon
pip install torch torchaudio

# NVIDIA GPU: use the wheel that matches your CUDA version
pip install torch==2.11.0+cu128 torchaudio==2.11.0+cu128 --extra-index-url https://download.pytorch.org/whl/cu128

# Intel Arc / XPU
pip install torch==2.11.0+cu128 torchaudio==2.11.0+cu128 --index-url https://pytorch-extension.intel.com/release-whl/stable/xpu/us/
```

See the [PyTorch install guide](https://pytorch.org/get-started/locally/) for the correct wheel for your hardware. The backend chooses the device in `apps/backend/tts_backend/config.py`: CUDA first, then MPS, then CPU.

4. Run the backend and frontend in separate terminals:

```bash
bun run backend:dev
```

```bash
bun run frontend:dev
```

Backend API base URL: `http://127.0.0.1:5000`

## Common Commands

```bash
bun run frontend:dev
bun run frontend lint
bun run frontend check
bun run frontend build
bun run frontend format
bun run frontend test:unit -- --run
bun run backend:setup
bun run backend:dev
```

Run a single frontend test file:

```bash
bun run --cwd apps/frontend test:unit -- --run path/to/spec.ts
```

Lightweight backend verification from `apps/backend`:

```bash
python -m compileall app.py tts_backend
```

## Repo Layout

- `apps/frontend`: static SvelteKit app.
- `apps/backend`: Flask API and Python model integration.
- `scripts/back-setup.ts`: creates or refreshes `apps/backend/.venv` and installs `requirements.txt`.
- `scripts/back-run.ts`: runs the backend with the venv Python.

## Runtime Notes

- Frontend browser code calls Flask directly via `PUBLIC_BACKEND_BASE_URL`. If unset, it defaults to `http://127.0.0.1:5000`.
- Backend routes are mounted under `/api/v1`.
- Voice clone settings persist in `apps/backend/data/clone_settings.sqlite3` and uploaded reference audio persists in `apps/backend/storage/clone_settings/`.

## More Detail

- Frontend details: [`apps/frontend/README.md`](apps/frontend/README.md)
- Backend details: [`apps/backend/README.md`](apps/backend/README.md)
