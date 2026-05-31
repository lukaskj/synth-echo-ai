<script lang="ts">
  import { Button } from '$lib/components/ui/button/index.js';
  import { Textarea } from '$lib/components/ui/textarea/index.js';
  import * as Card from '$lib/components/ui/card/index.js';
  import * as Select from '$lib/components/ui/select/index.js';
  import PlayIcon from 'lucide-svelte/icons/play';
  import LoaderIcon from 'lucide-svelte/icons/loader';
  import type { TtsMode, RequestStatus } from '$lib/tts/types';
  import { MODE_OPTIONS, UI_TEXT } from '$lib/tts/constants';

  let {
    mode = $bindable('synthesize'),
    synthesizeInputText = $bindable(''),
    cloneInputText = $bindable(''),
    status,
    canSubmit
  }: {
    mode?: TtsMode;
    synthesizeInputText?: string;
    cloneInputText?: string;
    status: RequestStatus;
    canSubmit: boolean;
  } = $props();

  const isBusy = $derived(
    status === 'synthesizing' || status === 'cloning' || status === 'loading-model'
  );
  const isCloneMode = $derived(mode === 'clone');
  const buttonLabel = $derived(
    status === 'synthesizing'
      ? UI_TEXT.synthesizing
      : status === 'cloning'
        ? UI_TEXT.cloning
        : status === 'loading-model'
          ? 'Loading model...'
          : isCloneMode
            ? UI_TEXT.cloneVoice
            : UI_TEXT.generateSpeech
  );
</script>

<Card.Root class="flex flex-col">
  <Card.Header class="pb-3">
    <div class="flex items-center justify-between gap-3">
      <Card.Title class="text-sm font-semibold">
        {isCloneMode ? UI_TEXT.cloneTitle : UI_TEXT.synthesisTitle}
      </Card.Title>
      <!-- Mode selector -->
      <Select.Root
        value={mode}
        onValueChange={(v) => {
          mode = v as TtsMode;
        }}
      >
        <Select.Trigger size="sm" class="w-fit min-w-36">
          {MODE_OPTIONS.find((o) => o.value === mode)?.label ?? 'Select mode...'}
        </Select.Trigger>
        <Select.Content>
          {#each MODE_OPTIONS as option (option.value)}
            <Select.Item value={option.value} label={option.label} />
          {/each}
        </Select.Content>
      </Select.Root>
    </div>
  </Card.Header>

  <Card.Content class="flex flex-1 flex-col gap-3">
    {#if isCloneMode}
      <Textarea
        id="script-input"
        bind:value={cloneInputText}
        placeholder={UI_TEXT.cloneScriptPlaceholder}
        rows={8}
        class="min-h-[180px] flex-1 resize-none"
      />
    {:else}
      <Textarea
        id="script-input"
        bind:value={synthesizeInputText}
        placeholder={UI_TEXT.scriptPlaceholder}
        rows={8}
        class="min-h-[180px] flex-1 resize-none"
      />
    {/if}

    <Button type="submit" disabled={!canSubmit} class="w-full gap-2" size="lg">
      {#if isBusy}
        <LoaderIcon class="size-4 animate-spin" />
      {:else}
        <PlayIcon class="size-4" />
      {/if}
      {buttonLabel}
    </Button>
  </Card.Content>
</Card.Root>
