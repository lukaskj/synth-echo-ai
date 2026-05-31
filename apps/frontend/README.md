# Frontend

Static SvelteKit frontend for the OmniVoice text-to-speech and voice cloning UI.

## Commands

Preferred from the repo root:

```bash
bun run frontend:dev
bun run --cwd apps/frontend lint
bun run --cwd apps/frontend check
bun run --cwd apps/frontend build
bun run --cwd apps/frontend format
bun run --cwd apps/frontend test:unit -- --run
```

Run a single test file:

```bash
bun run --cwd apps/frontend test:unit -- --run path/to/spec.ts
```

Preview the built app:

```bash
bun run --cwd apps/frontend preview
```

## Structure

- `src/routes/+page.svelte` is only a thin wrapper.
- The main app UI lives in `src/lib/tts/components/TtsWorkspace.svelte`.
- Frontend API calls are centralized in `src/lib/tts/api.ts`.
- API paths and shared UI constants live in `src/lib/tts/constants.ts`.
- URL and error helpers live in `src/lib/tts/helpers.ts`.

## Runtime Notes

- The app is intentionally static: `@sveltejs/adapter-static` is enabled and `src/routes/+layout.ts` sets `prerender = true`.
- `src/routes/api/mock-tts/+server.ts` is prerendered and returns canned audio for UI work when the Flask backend is unavailable.
- Svelte 5 runes mode is forced for app code in `svelte.config.js`.
- Browser requests go directly to Flask via `PUBLIC_BACKEND_BASE_URL`; the default is `http://127.0.0.1:5000`.
- Tailwind is configured through the Vite plugin and `src/routes/layout.css`; there is no `tailwind.config.*` file.

## Testing Notes

- Vitest is split by project in `vite.config.ts`.
- `*.svelte.{test,spec}.*` runs in Playwright/Chromium.
- Non-Svelte tests run in Node.
- Browser specs require Playwright browsers to be installed.
- Current tests under `src/lib/vitest-examples/` are starter examples, not meaningful app coverage.
