<script lang="ts">
  import type { Snippet } from 'svelte';
  import { Badge } from '$lib/components/ui/badge/index.js';
  import { Button } from '$lib/components/ui/button/index.js';
  import * as Tabs from '$lib/components/ui/tabs/index.js';
  import { LANGUAGES, UI_TEXT } from '$lib/tts/constants';
  import type { SavedCloneSetting, VoiceSourceType } from '$lib/tts/types';
  import ChevronRightIcon from 'lucide-svelte/icons/chevron-right';
  import MicIcon from 'lucide-svelte/icons/mic';
  import WandSparklesIcon from 'lucide-svelte/icons/wand-sparkles';

  let {
    value,
    onValueChange,
    savedCloneSettings,
    selectedCloneSetting,
    onOpenVoiceLibrary,
    noVoiceSelectedMessage = UI_TEXT.conversationNoVoiceSelected,
    selectedVoiceBadgeLabel = '',
    cloneContent,
    instructionContent
  }: {
    value: VoiceSourceType;
    onValueChange: (value: VoiceSourceType) => void;
    savedCloneSettings: SavedCloneSetting[];
    selectedCloneSetting: SavedCloneSetting | null;
    onOpenVoiceLibrary: () => void;
    noVoiceSelectedMessage?: string;
    selectedVoiceBadgeLabel?: string;
    cloneContent?: Snippet;
    instructionContent?: Snippet;
  } = $props();

  const selectedVoiceLangLabel = $derived(
    selectedCloneSetting
      ? (LANGUAGES.find((option) => option.value === selectedCloneSetting.lang)?.label ??
          selectedCloneSetting.lang.toUpperCase())
      : ''
  );
</script>

<Tabs.Root {value} onValueChange={(nextValue) => onValueChange(nextValue as VoiceSourceType)}>
  <Tabs.List class="grid w-full grid-cols-2">
    <Tabs.Trigger value="clone">{UI_TEXT.voiceLibraryTitle}</Tabs.Trigger>
    <Tabs.Trigger value="instruction">{UI_TEXT.voiceInstructionTitle}</Tabs.Trigger>
  </Tabs.List>

  <Tabs.Content value="clone" class="space-y-3 pt-1">
    {#if selectedCloneSetting}
      <div class="bg-muted/40 flex items-center gap-3 rounded-lg px-3 py-2.5">
        <div class="bg-primary/15 flex size-8 shrink-0 items-center justify-center rounded-full">
          <MicIcon class="text-primary size-4" />
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-foreground truncate text-sm font-medium">{selectedCloneSetting.name}</p>
          <p class="text-muted-foreground text-xs">{selectedVoiceLangLabel}</p>
        </div>
        {#if selectedVoiceBadgeLabel}
          <Badge variant="secondary" class="shrink-0 text-xs">{selectedVoiceBadgeLabel}</Badge>
        {/if}
      </div>
    {:else}
      <div
        class="bg-muted/20 flex items-center gap-3 rounded-lg border border-dashed border-zinc-700 px-3 py-2.5"
      >
        <div class="bg-muted flex size-8 shrink-0 items-center justify-center rounded-full">
          <WandSparklesIcon class="text-muted-foreground size-4" />
        </div>
        <div class="min-w-0 flex-1">
          <p class="text-foreground text-sm font-medium">{UI_TEXT.voiceLibraryTitle}</p>
          <p class="text-muted-foreground text-xs">
            {savedCloneSettings.length > 0 ? noVoiceSelectedMessage : UI_TEXT.noVoicesAvailable}
          </p>
        </div>
      </div>
    {/if}

    {@render cloneContent?.()}

    <Button variant="outline" class="w-full gap-2" onclick={onOpenVoiceLibrary}>
      {UI_TEXT.selectVoiceButton}
      <ChevronRightIcon class="size-3.5" />
    </Button>
  </Tabs.Content>

  <Tabs.Content value="instruction" class="pt-1">
    {@render instructionContent?.()}
  </Tabs.Content>
</Tabs.Root>
