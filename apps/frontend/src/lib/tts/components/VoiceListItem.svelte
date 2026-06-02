<script lang="ts">
  import { Button } from '$lib/components/ui/button/index.js';
  import { Badge } from '$lib/components/ui/badge/index.js';
  import AudioPlayer from '$lib/tts/components/AudioPlayer.svelte';
  import MicIcon from 'lucide-svelte/icons/mic';
  import PencilIcon from 'lucide-svelte/icons/pencil';
  import Trash2Icon from 'lucide-svelte/icons/trash-2';
  import CheckIcon from 'lucide-svelte/icons/check';
  import VolumeIcon from 'lucide-svelte/icons/volume-2';
  import PauseIcon from 'lucide-svelte/icons/pause';
  import type { SavedCloneSetting } from '$lib/tts/types';
  import { LANGUAGES } from '$lib/tts/constants';

  let {
    voice,
    isSelected = false,
    onSelect,
    onEdit,
    onDelete
  }: {
    voice: SavedCloneSetting;
    isSelected?: boolean;
    onSelect: (id: number) => void;
    onEdit: (id: number) => void;
    onDelete: (id: number) => void;
  } = $props();

  let audioPlaying = $state(false);
  let audioRef = $state<HTMLAudioElement | null>(null);

  const langLabel = $derived(
    LANGUAGES.find((l) => l.value === voice.lang)?.label ?? voice.lang.toUpperCase()
  );

  function togglePreview(e: MouseEvent) {
    e.stopPropagation();
    if (!audioRef) return;
    if (audioPlaying) {
      audioRef.pause();
      audioRef.currentTime = 0;
      audioPlaying = false;
    } else {
      audioRef.play().catch(() => undefined);
      audioPlaying = true;
    }
  }

  function handleAudioEnded() {
    audioPlaying = false;
  }
</script>

<div
  class="group relative flex items-start gap-3 rounded-lg border p-3 transition-colors {isSelected
    ? 'border-primary/60 bg-primary/5'
    : 'border-border hover:border-border/80 hover:bg-muted/30 cursor-pointer'}"
  role="button"
  tabindex="0"
  onclick={() => onSelect(voice.id)}
  onkeydown={(e) => (e.key === 'Enter' || e.key === ' ') && onSelect(voice.id)}
  aria-pressed={isSelected}
>
  <!-- Mic icon indicator -->
  <div
    class="mt-0.5 flex size-8 shrink-0 items-center justify-center rounded-full {isSelected
      ? 'bg-primary/20'
      : 'bg-muted'}"
  >
    {#if isSelected}
      <CheckIcon class="text-primary size-4" />
    {:else}
      <MicIcon class="text-muted-foreground size-4" />
    {/if}
  </div>

  <!-- Voice info -->
  <div class="min-w-0 flex-1">
    <div class="flex items-center gap-2">
      <p class="text-foreground truncate text-sm font-medium">{voice.name}</p>
      {#if voice.is_microphone_recording}
        <Badge variant="secondary" class="h-4 shrink-0 px-1.5 py-0 text-xs">Recorded</Badge>
      {/if}
    </div>
    <p class="text-muted-foreground text-xs">{langLabel}</p>

    <!-- Reference text snippet -->
    {#if voice.ref_text}
      <p class="text-muted-foreground mt-1 truncate text-xs italic">
        "{voice.ref_text.slice(0, 60)}{voice.ref_text.length > 60 ? '...' : ''}"
      </p>
    {/if}
  </div>

  <!-- Actions -->
  <div class="flex shrink-0 items-center gap-1">
    <!-- Audio preview button -->
    {#if voice.ref_audio_path}
      <Button
        variant="ghost"
        size="icon-sm"
        onclick={togglePreview}
        aria-label={audioPlaying ? 'Pause preview' : 'Preview reference audio'}
        title={audioPlaying ? 'Pause preview' : 'Preview reference audio'}
      >
        {#if audioPlaying}
          <PauseIcon class="size-3.5 text-primary" />
        {:else}
          <VolumeIcon class="size-3.5" />
        {/if}
      </Button>
      <AudioPlayer
        bind:audioElement={audioRef}
        src={voice.ref_audio_path}
        preload="none"
        controls={false}
        className="hidden"
        onEnded={handleAudioEnded}
      />
    {/if}

    <!-- Edit button -->
    <Button
      variant="ghost"
      size="icon-sm"
      onclick={(e: MouseEvent) => {
        e.stopPropagation();
        onEdit(voice.id);
      }}
      aria-label="Edit voice"
      title="Edit voice"
    >
      <PencilIcon class="size-3.5" />
    </Button>

    <!-- Delete button -->
    <Button
      variant="ghost"
      size="icon-sm"
      class="text-destructive hover:text-destructive hover:bg-destructive/10"
      onclick={(e: MouseEvent) => {
        e.stopPropagation();
        onDelete(voice.id);
      }}
      aria-label="Delete voice"
      title="Delete voice"
    >
      <Trash2Icon class="size-3.5" />
    </Button>
  </div>
</div>
