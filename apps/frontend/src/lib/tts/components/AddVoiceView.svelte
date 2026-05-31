<script lang="ts">
  import { Button } from '$lib/components/ui/button/index.js';
  import { Input } from '$lib/components/ui/input/index.js';
  import { Label } from '$lib/components/ui/label/index.js';
  import { Textarea } from '$lib/components/ui/textarea/index.js';
  import * as Select from '$lib/components/ui/select/index.js';
  import { Slider } from '$lib/components/ui/slider/index.js';
  import ArrowLeftIcon from 'lucide-svelte/icons/arrow-left';
  import UploadIcon from 'lucide-svelte/icons/upload';
  import { LANGUAGES, UI_TEXT, DEFAULT_FORM_STATE } from '$lib/tts/constants';

  let {
    cloneSettingName = $bindable(''),
    cloneRefText = $bindable(''),
    cloneLang = $bindable(DEFAULT_FORM_STATE.cloneLang),
    cloneSpeed = $bindable(DEFAULT_FORM_STATE.cloneSpeed),
    cloneNumStep = $bindable(DEFAULT_FORM_STATE.cloneNumStep),
    cloneRefAudioFile = null,
    cloneRefAudioPreviewUrl = '',
    cloneRefAudioInputKey = 0,
    isSavingCloneSetting = false,
    canSaveCloneSetting = false,
    cloneSettingsErrorMessage = '',
    onSave,
    onBack,
    onRefAudioChange
  }: {
    cloneSettingName?: string;
    cloneRefText?: string;
    cloneLang?: string;
    cloneSpeed?: number;
    cloneNumStep?: number;
    cloneRefAudioFile?: File | null;
    cloneRefAudioPreviewUrl?: string;
    cloneRefAudioInputKey?: number;
    isSavingCloneSetting?: boolean;
    canSaveCloneSetting?: boolean;
    cloneSettingsErrorMessage?: string;
    onSave: () => void;
    onBack: () => void;
    onRefAudioChange: (event: Event) => void;
  } = $props();
</script>

<div class="flex h-full flex-col">
  <!-- Header -->
  <div class="flex items-center gap-2 pb-4">
    <Button variant="ghost" size="icon-sm" onclick={onBack} aria-label="Back to voice list">
      <ArrowLeftIcon class="size-4" />
    </Button>
    <div>
      <h3 class="text-foreground text-sm font-semibold">Upload New Voice</h3>
      <p class="text-muted-foreground text-xs">Save a voice clone from a reference audio file</p>
    </div>
  </div>

  <!-- Error banner -->
  {#if cloneSettingsErrorMessage}
    <div
      class="mb-4 rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-400"
    >
      {cloneSettingsErrorMessage}
    </div>
  {/if}

  <!-- Form -->
  <div class="flex-1 space-y-4 overflow-y-auto pb-4">
    <!-- Name -->
    <div class="space-y-1.5">
      <Label for="add-voice-name">{UI_TEXT.cloneSettingNameLabel}</Label>
      <Input
        id="add-voice-name"
        bind:value={cloneSettingName}
        placeholder={UI_TEXT.cloneSettingNamePlaceholder}
      />
    </div>

    <!-- Language -->
    <div class="space-y-1.5">
      <Label for="add-voice-lang">{UI_TEXT.language}</Label>
      <Select.Root bind:value={cloneLang}>
        <Select.Trigger id="add-voice-lang" class="w-full">
          {LANGUAGES.find((o) => o.value === cloneLang)?.label ?? 'Select language...'}
        </Select.Trigger>
        <Select.Content>
          {#each LANGUAGES as option (option.value)}
            <Select.Item value={option.value} label={option.label} />
          {/each}
        </Select.Content>
      </Select.Root>
    </div>

    <!-- Reference Audio Upload -->
    <div class="space-y-1.5">
      <Label for="add-voice-audio">{UI_TEXT.refAudioLabel}</Label>
      <div class="rounded-md border border-dashed border-zinc-600 p-3">
        {#if cloneRefAudioPreviewUrl}
          <audio controls src={cloneRefAudioPreviewUrl} class="mb-2 w-full" preload="auto"> </audio>
        {/if}
        <label
          for="add-voice-audio"
          class="flex cursor-pointer flex-col items-center gap-1 py-2 text-center"
        >
          <UploadIcon class="text-muted-foreground size-5" />
          <span class="text-muted-foreground text-xs">
            {cloneRefAudioFile ? cloneRefAudioFile.name : 'Click to upload audio file'}
          </span>
          <span class="text-muted-foreground text-xs">(WAV, MP3, OGG)</span>
        </label>
        {#key cloneRefAudioInputKey}
          <input
            id="add-voice-audio"
            type="file"
            accept="audio/*"
            class="sr-only"
            onchange={onRefAudioChange}
          />
        {/key}
      </div>
    </div>

    <!-- Reference Text -->
    <div class="space-y-1.5">
      <Label for="add-voice-ref-text">{UI_TEXT.refTextLabel}</Label>
      <Textarea
        id="add-voice-ref-text"
        bind:value={cloneRefText}
        placeholder={UI_TEXT.refTextPlaceholder}
        rows={3}
      />
    </div>

    <!-- Speed -->
    <div class="space-y-2">
      <div class="flex items-center justify-between">
        <Label for="add-voice-speed">{UI_TEXT.speed}</Label>
        <span class="text-muted-foreground text-xs tabular-nums">{cloneSpeed.toFixed(1)}</span>
      </div>
      <Slider
        id="add-voice-speed"
        min={0.5}
        max={2.0}
        step={0.1}
        bind:value={cloneSpeed}
        class="w-full"
      />
    </div>

    <!-- Diffusion Steps -->
    <div class="space-y-2">
      <div class="flex items-center justify-between">
        <Label for="add-voice-steps">{UI_TEXT.diffusionSteps}</Label>
        <span class="text-muted-foreground text-xs tabular-nums">{cloneNumStep}</span>
      </div>
      <Slider
        id="add-voice-steps"
        min={4}
        max={64}
        step={4}
        bind:value={cloneNumStep}
        class="w-full"
      />
    </div>
  </div>

  <!-- Save button -->
  <div class="border-border border-t pt-4">
    <Button class="w-full" onclick={onSave} disabled={!canSaveCloneSetting}>
      {isSavingCloneSetting ? UI_TEXT.savingCloneSetting : UI_TEXT.saveCloneSetting}
    </Button>
  </div>
</div>
