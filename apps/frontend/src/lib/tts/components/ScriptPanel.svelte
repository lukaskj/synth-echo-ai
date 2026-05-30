<script lang="ts">
  import {UI_TEXT} from "$lib/tts/constants";
  import type {LastRequest, RequestStatus, TtsMode} from "$lib/tts/types";
  import AudioResultPanel from "./AudioResultPanel.svelte";
  import StatusToolbar from "./StatusToolbar.svelte";

  type Props = {
    mode: TtsMode;
    canSubmit: boolean;
    synthesizeInputText: string;
    cloneInputText: string;
    statusLabel: string;
    modelReady: boolean;
    isBusy: boolean;
    status: RequestStatus;
    audioUrl: string;
    errorMessage: string;
    responseMessage: string;
    lastRequest: LastRequest | null;
    onLoadModel: () => void | Promise<void>;
    onUnloadModel: () => void | Promise<void>;
  };

  let {
    mode,
    canSubmit,
    synthesizeInputText = $bindable(),
    cloneInputText = $bindable(),
    statusLabel,
    modelReady,
    isBusy,
    status,
    audioUrl,
    errorMessage,
    responseMessage,
    lastRequest,
    onLoadModel,
    onUnloadModel,
  }: Props = $props();

</script>

<section class="rounded-xl border border-slate-800 bg-slate-900/70 px-6 pt-4 pb-6 shadow-2xl shadow-slate-950/40 backdrop-blur">
  <div class="flex flex-col flex-wrap items-start justify-between gap-4">
    <div>
      <p class="text-sm font-medium uppercase tracking-[0.18em] text-slate-400">
        {mode === 'clone' ? UI_TEXT.cloneEyebrow : UI_TEXT.synthesisEyebrow}
      </p>
      <h2 class="mt-2 text-2xl font-semibold text-white">{mode === 'clone' ? UI_TEXT.cloneTitle : UI_TEXT.synthesisTitle}</h2>
    </div>

    <StatusToolbar {statusLabel} {modelReady} {isBusy} {status} {onLoadModel} {onUnloadModel} />
  </div>

  <label class="mt-3 block text-sm font-medium text-slate-200" for="tts-input">
    {mode === 'clone' ? UI_TEXT.cloneScriptLabel : UI_TEXT.scriptLabel}
  </label>
  {#if mode === 'clone'}
    <textarea
      id="tts-input"
      bind:value={cloneInputText}
      rows="7"
      placeholder={UI_TEXT.cloneScriptPlaceholder}
      class="mt-3 w-full rounded-lg border border-slate-700 bg-slate-950/70 px-4 py-3 text-base leading-7 text-slate-100 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-400/30"
    ></textarea>
  {:else}
    <textarea
      id="tts-input"
      bind:value={synthesizeInputText}
      rows="7"
      placeholder={UI_TEXT.scriptPlaceholder}
      class="mt-3 w-full rounded-lg border border-slate-700 bg-slate-950/70 px-4 py-3 text-base leading-7 text-slate-100 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-400/30"
    ></textarea>
  {/if}

  <button
    type="submit"
    disabled={!canSubmit}
    class="mt-4 inline-flex w-full items-center justify-center rounded-lg bg-violet-400 px-4 py-3 text-base font-semibold text-slate-950 transition hover:bg-violet-300 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-violet-300 disabled:cursor-not-allowed disabled:bg-slate-700 disabled:text-slate-300"
  >
    {#if status === 'synthesizing'}
      {UI_TEXT.synthesizing}
    {:else if status === 'cloning'}
      {UI_TEXT.cloning}
    {:else}
      {mode === 'clone' ? UI_TEXT.cloneVoice : UI_TEXT.generateSpeech}
    {/if}
  </button>

  <AudioResultPanel {status} {audioUrl} {errorMessage} {responseMessage} {lastRequest} />
</section>
