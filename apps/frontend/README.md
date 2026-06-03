# Frontend

Static SvelteKit frontend for the OmniVoice text-to-speech, voice cloning, and multi-voice conversation UI.

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
- The voice dashboard UI lives in `src/lib/tts/components/TtsWorkspace.svelte` and is served from `/`.
- The conversation routes are thin wrappers around `src/lib/tts/components/ConversationWorkspace.svelte` and are served from `/conversation` and `/conversation/[id]`.
- `ConversationWorkspace.svelte` owns conversation state/orchestration, while `ConversationSidebar.svelte`, `ConversationEditor.svelte`, and `ConversationLineConfig.svelte` render the main page sections.
- `VoiceLibraryBrowser.svelte` is the shared searchable voice-library list used by both the dashboard voice sheet and the conversation line configuration.
- Frontend API calls are centralized in `src/lib/tts/api.ts`.
- API paths and shared UI constants live in `src/lib/tts/constants.ts`.
- URL and error helpers live in `src/lib/tts/helpers.ts`.

## Runtime Notes

- The app is intentionally static: `@sveltejs/adapter-static` is enabled and `src/routes/+layout.ts` sets `prerender = true`.
- `svelte.config.js` uses `adapter-static({ fallback: '200.html' })` so route-parameter pages like `/conversation/[id]` still work on direct loads and refreshes in SPA-style static hosting.
- `src/routes/api/mock-tts/+server.ts` is prerendered and returns canned audio for UI work when the Flask backend is unavailable.
- Svelte 5 runes mode is forced for app code in `svelte.config.js`.
- Browser requests go directly to Flask via `PUBLIC_BACKEND_BASE_URL`; the default is `http://127.0.0.1:5000`.
- Audio generation endpoints now return saved audio URLs, and the conversation editor stores those URLs per line for later playback.
- Toast notifications use shadcn-svelte Sonner and are mounted in the bottom-left from `src/routes/+layout.svelte`.
- Tailwind is configured through the Vite plugin and `src/routes/layout.css`; there is no `tailwind.config.*` file.

## Testing Notes

- Vitest is split by project in `vite.config.ts`.
- `*.svelte.{test,spec}.*` runs in Playwright/Chromium.
- Non-Svelte tests run in Node.
- Browser specs require Playwright browsers to be installed.
- Current tests under `src/lib/vitest-examples/` are starter examples, not meaningful app coverage.
