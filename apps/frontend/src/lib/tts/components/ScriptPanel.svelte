<script lang="ts">
  import {UI_TEXT} from "$lib/tts/constants";
  import type {LastRequest, RequestStatus, TtsMode} from "$lib/tts/types";
  import AudioResultPanel from "./AudioResultPanel.svelte";
  import Button from './Button.svelte';
  import StatusToolbar from "./StatusToolbar.svelte";
  import TextareaField from './TextareaField.svelte';

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

  {#if mode === 'clone'}
    <TextareaField
      id="tts-input"
      bind:value={cloneInputText}
      label={UI_TEXT.cloneScriptLabel}
      className="mt-3"
      rows={7}
      placeholder={UI_TEXT.cloneScriptPlaceholder}
    />
  {:else}
    <TextareaField
      id="tts-input"
      bind:value={synthesizeInputText}
      label={UI_TEXT.scriptLabel}
      className="mt-3"
      rows={7}
      placeholder={UI_TEXT.scriptPlaceholder}
    />
  {/if}

  <Button type="submit" variant="primary" size="large" class="mt-4 w-full" disabled={!canSubmit}>
    {#if status === 'synthesizing'}
      {UI_TEXT.synthesizing}
    {:else if status === 'cloning'}
      {UI_TEXT.cloning}
    {:else}
      {mode === 'clone' ? UI_TEXT.cloneVoice : UI_TEXT.generateSpeech}
    {/if}
  </Button>

  <AudioResultPanel {status} {audioUrl} {errorMessage} {responseMessage} {lastRequest} />
</section>
