<script lang="ts">
  import { Button } from '$lib/components/ui/button/index.js';
  import { Input } from '$lib/components/ui/input/index.js';
  import { Label } from '$lib/components/ui/label/index.js';
  import * as Select from '$lib/components/ui/select/index.js';
  import { Slider } from '$lib/components/ui/slider/index.js';
  import ArrowLeftIcon from 'lucide-svelte/icons/arrow-left';
  import type { SavedCloneSetting } from '$lib/tts/types';
  import { LANGUAGES, UI_TEXT } from '$lib/tts/constants';
  import AudioPlayer from '$lib/tts/components/AudioPlayer.svelte';

  let {
    selectedCloneSetting,
    cloneSettingName = $bindable(''),
    cloneLang = $bindable('en'),
    cloneSpeed = $bindable(1.0),
    cloneNumStep = $bindable(32),
    isUpdatingCloneSetting = false,
    isDeletingCloneSetting = false,
    canUpdateCloneSetting = false,
    canDeleteCloneSetting = false,
    cloneSettingsErrorMessage = '',
    cloneSettingsMessage = '',
    onUpdate,
    onDelete,
    onBack
  }: {
    selectedCloneSetting: SavedCloneSetting | null;
    cloneSettingName?: string;
    cloneLang?: string;
    cloneSpeed?: number;
    cloneNumStep?: number;
    isUpdatingCloneSetting?: boolean;
    isDeletingCloneSetting?: boolean;
    canUpdateCloneSetting?: boolean;
    canDeleteCloneSetting?: boolean;
    cloneSettingsErrorMessage?: string;
    cloneSettingsMessage?: string;
    onUpdate: () => void;
    onDelete: () => void;
    onBack: () => void;
  } = $props();
</script>

<div class="flex h-full flex-col">
  <!-- Header -->
  <div class="flex items-center gap-2 pb-4">
    <Button variant="ghost" size="icon-sm" onclick={onBack} aria-label="Back to voice list">
      <ArrowLeftIcon class="size-4" />
    </Button>
    <div>
      <h3 class="text-foreground text-sm font-semibold">Edit Voice</h3>
      <p class="text-muted-foreground text-xs">Update voice settings</p>
    </div>
  </div>

  <!-- Messages -->
  {#if cloneSettingsErrorMessage}
    <div
      class="mb-4 rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-400"
    >
      {cloneSettingsErrorMessage}
    </div>
  {/if}
  {#if cloneSettingsMessage}
    <div
      class="mb-4 rounded-md border border-emerald-500/30 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-400"
    >
      {cloneSettingsMessage}
    </div>
  {/if}

  <div class="flex-1 space-y-4 overflow-y-auto pb-4">
    <!-- Name -->
    <div class="space-y-1.5">
      <Label for="edit-voice-name">{UI_TEXT.cloneSettingNameLabel}</Label>
      <Input
        id="edit-voice-name"
        bind:value={cloneSettingName}
        placeholder={UI_TEXT.cloneSettingNamePlaceholder}
      />
    </div>

    <!-- Language -->
    <div class="space-y-1.5">
      <Label for="edit-voice-lang">{UI_TEXT.language}</Label>
      <Select.Root bind:value={cloneLang}>
        <Select.Trigger id="edit-voice-lang" class="w-full">
          {LANGUAGES.find((o) => o.value === cloneLang)?.label ?? 'Select language...'}
        </Select.Trigger>
        <Select.Content>
          {#each LANGUAGES as option (option.value)}
            <Select.Item value={option.value} label={option.label} />
          {/each}
        </Select.Content>
      </Select.Root>
    </div>

    <!-- Reference Audio (read-only preview) -->
    {#if selectedCloneSetting?.ref_audio_path}
      <div class="space-y-1.5">
        <Label>Reference Audio (read-only)</Label>
        <AudioPlayer src={selectedCloneSetting.ref_audio_path} preload="none" />
      </div>
    {/if}

    <!-- Reference text (read-only) -->
    {#if selectedCloneSetting?.ref_text}
      <div class="space-y-1.5">
        <Label>Reference Text (read-only)</Label>
        <p
          class="text-muted-foreground rounded-md border border-dashed border-zinc-700 bg-zinc-800/30 px-3 py-2 text-xs italic"
        >
          {selectedCloneSetting.ref_text}
        </p>
      </div>
    {/if}

    <!-- Speed -->
    <div class="space-y-2">
      <div class="flex items-center justify-between">
        <Label for="edit-voice-speed">{UI_TEXT.speed}</Label>
        <span class="text-muted-foreground text-xs tabular-nums">{cloneSpeed.toFixed(1)}</span>
      </div>
      <Slider
        id="edit-voice-speed"
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
        <Label for="edit-voice-steps">{UI_TEXT.diffusionSteps}</Label>
        <span class="text-muted-foreground text-xs tabular-nums">{cloneNumStep}</span>
      </div>
      <Slider
        id="edit-voice-steps"
        min={4}
        max={64}
        step={4}
        bind:value={cloneNumStep}
        class="w-full"
      />
    </div>
  </div>

  <!-- Action buttons -->
  <div class="border-border flex flex-col gap-2 border-t pt-4">
    <Button class="w-full" onclick={onUpdate} disabled={!canUpdateCloneSetting}>
      {isUpdatingCloneSetting ? UI_TEXT.updatingCloneSetting : UI_TEXT.selectedCloneSettingUpdate}
    </Button>
    <Button
      variant="destructive"
      class="w-full"
      onclick={onDelete}
      disabled={!canDeleteCloneSetting}
    >
      {isDeletingCloneSetting ? UI_TEXT.deletingCloneSetting : UI_TEXT.selectedCloneSettingDelete}
    </Button>
  </div>
</div>
