<script lang="ts">
  import Button from '$lib/tts/components/Button.svelte';
  import { UI_TEXT } from '$lib/tts/constants';
  import type { RequestStatus } from '$lib/tts/types';

  type Props = {
    statusLabel: string;
    modelReady: boolean;
    isBusy: boolean;
    status: RequestStatus;
    onLoadModel: () => void | Promise<void>;
    onUnloadModel: () => void | Promise<void>;
  };

  let { statusLabel, modelReady, isBusy, status, onLoadModel, onUnloadModel }: Props = $props();
</script>

<div class="flex flex-wrap items-center justify-end gap-2">
  <div class="rounded-md border border-slate-700 bg-slate-950/60 px-3 py-1 text-sm text-slate-300">
    {UI_TEXT.statusLabel}: {statusLabel}
  </div>
  <div
    class="rounded-md border px-3 py-1 text-sm {modelReady
      ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200'
      : 'border-amber-500/30 bg-amber-500/10 text-amber-200'}"
  >
    Model: {modelReady ? UI_TEXT.modelLoaded : UI_TEXT.modelNotLoaded}
  </div>
  <Button
    type="button"
    variant="secondary"
    size="small"
    class="px-4"
    onclick={onLoadModel}
    disabled={isBusy || modelReady}
  >
    {#if status === 'loading-model'}
      {UI_TEXT.loadingShort}
    {:else}
      {UI_TEXT.loadModel}
    {/if}
  </Button>
  <Button
    type="button"
    variant="danger"
    size="small"
    class="px-4"
    onclick={onUnloadModel}
    disabled={isBusy || !modelReady}
  >
    {#if status === 'unloading-model'}
      {UI_TEXT.unloadingShort}
    {:else}
      {UI_TEXT.unloadModel}
    {/if}
  </Button>
</div>
