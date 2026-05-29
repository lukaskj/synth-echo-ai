# @lukaskj/omni-clone

Monorepo scaffold for a future TTS and voice cloning project using Electrobun for the desktop frontend and Flask for the backend API.

## Frontend

Install frontend dependencies:

```bash
bun install
```

Run the Electrobun app in watch mode:

```bash
bun run dev:frontend
```

## Backend

From `apps/backend/`, create the virtual environment:

```bash
python -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask server from `apps/backend/`:

```bash
python app.py
```

The backend listens on `http://127.0.0.1:5000` and exposes `GET /api/hello`, which returns `Hello, World!`.
