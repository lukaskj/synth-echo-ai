<script lang="ts">
  import AudioPlayer from '$lib/tts/components/AudioPlayer.svelte';
  import NoticeBanner from '$lib/tts/components/NoticeBanner.svelte';
  import { UI_TEXT } from '$lib/tts/constants';
  import type { LastRequest, RequestStatus } from '$lib/tts/types';

  type Props = {
    status: RequestStatus;
    audioUrl: string;
    errorMessage: string;
    responseMessage: string;
    lastRequest: LastRequest | null;
  };

  let { status, audioUrl, errorMessage, responseMessage, lastRequest }: Props = $props();
</script>

<section class="mt-3 rounded-lg border border-slate-800 bg-slate-950/60 p-5" aria-live="polite">
  <div class="flex flex-wrap items-center justify-between gap-3">
    <div>
      <h3 class="text-lg font-semibold text-white">{UI_TEXT.generatedAudioTitle}</h3>
      <p class="mt-1 text-sm text-slate-400">{UI_TEXT.generatedAudioDescription}</p>
    </div>
    {#if status === 'synthesizing' || status === 'cloning'}
      <div
        class="flex items-center gap-2 rounded-md border border-violet-400/30 bg-violet-400/10 px-3 py-1 text-sm text-violet-200"
      >
        <span class="h-2.5 w-2.5 animate-pulse rounded-full bg-violet-300"></span>
        {UI_TEXT.inProgress}
      </div>
    {/if}
  </div>

  {#if status === 'synthesizing' || status === 'cloning'}
    <NoticeBanner tone="neutral" className="mt-5 p-5">{UI_TEXT.generatingAudio}</NoticeBanner>
  {:else if status === 'success' && audioUrl && lastRequest}
    <div class="mt-5 space-y-4">
      <p class="text-sm leading-6 text-slate-300">{responseMessage}</p>
      <AudioPlayer src={audioUrl} preload="none" />
      <div class="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">
        <div class="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
          <p class="text-xs uppercase tracking-[0.18em] text-slate-500">{UI_TEXT.resultMode}</p>
          <p class="mt-2 text-sm font-medium text-white">
            {lastRequest.mode === 'clone' ? UI_TEXT.cloneTitle : UI_TEXT.synthesisTitle}
          </p>
        </div>
        {#if lastRequest.mode === 'clone'}
          <div class="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
            <p class="text-xs uppercase tracking-[0.18em] text-slate-500">
              {UI_TEXT.resultReferenceAudio}
            </p>
            <p class="mt-2 text-sm font-medium text-white">{lastRequest.refAudioName || '-'}</p>
          </div>
        {/if}
        <div class="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
          <p class="text-xs uppercase tracking-[0.18em] text-slate-500">{UI_TEXT.resultLanguage}</p>
          <p class="mt-2 text-sm font-medium text-white">{lastRequest.langLabel}</p>
        </div>
        <div class="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
          <p class="text-xs uppercase tracking-[0.18em] text-slate-500">{UI_TEXT.resultSpeed}</p>
          <p class="mt-2 text-sm font-medium text-white">{lastRequest.speed.toFixed(1)}x</p>
        </div>
        <div class="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
          <p class="text-xs uppercase tracking-[0.18em] text-slate-500">{UI_TEXT.resultSteps}</p>
          <p class="mt-2 text-sm font-medium text-white">{lastRequest.numStep}</p>
        </div>
      </div>
      {#if lastRequest.mode === 'synthesize' && lastRequest.instruct !== undefined}
        <div class="rounded-lg border border-slate-800 bg-slate-900/70 p-4">
          <p class="text-xs uppercase tracking-[0.18em] text-slate-500">
            {UI_TEXT.currentInstruct}
          </p>
          <p class="mt-2 text-sm leading-6 text-white">
            {lastRequest.instruct || UI_TEXT.noInstruction}
          </p>
        </div>
      {/if}
    </div>
  {:else if status === 'error'}
    <NoticeBanner tone="error" className="mt-5 p-5" role="alert">
      <p class="font-semibold text-rose-50">{UI_TEXT.synthesisFailedTitle}</p>
      <p class="mt-2">{errorMessage}</p>
    </NoticeBanner>
  {:else if responseMessage}
    <NoticeBanner tone="success" className="mt-5 p-5">
      {responseMessage}
    </NoticeBanner>
  {:else}
    <NoticeBanner tone="muted" className="mt-5 p-5">
      {UI_TEXT.noAudioYet}
    </NoticeBanner>
  {/if}
</section>
