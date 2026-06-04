<script lang="ts">
  import { Button } from '$lib/components/ui/button/index.js';
  import { Input } from '$lib/components/ui/input/index.js';
  import { ScrollArea } from '$lib/components/ui/scroll-area/index.js';
  import { Separator } from '$lib/components/ui/separator/index.js';
  import VoiceListItem from './VoiceListItem.svelte';
  import MicIcon from 'lucide-svelte/icons/mic';
  import UploadIcon from 'lucide-svelte/icons/upload';
  import RefreshCwIcon from 'lucide-svelte/icons/refresh-cw';
  import SearchIcon from 'lucide-svelte/icons/search';
  import XIcon from 'lucide-svelte/icons/x';
  import type { SavedCloneSetting } from '$lib/tts/types';
  import { UI_TEXT } from '$lib/tts/constants';

  let {
    savedCloneSettings,
    selectedCloneSettingId,
    isCloneSettingsLoading,
    hasLoadedCloneSettings,
    cloneSettingsMessage,
    cloneSettingsErrorMessage,
    onSelectVoice,
    onStartAddUpload,
    onStartAddRecord,
    onStartEditVoice,
    onDeleteVoice,
    onRefreshVoices,
    listClass = 'flex-1',
    showCreateActions = true,
    showManagementActions = true
  }: {
    savedCloneSettings: SavedCloneSetting[];
    selectedCloneSettingId: number | null;
    isCloneSettingsLoading: boolean;
    hasLoadedCloneSettings: boolean;
    cloneSettingsMessage: string;
    cloneSettingsErrorMessage: string;
    onSelectVoice: (id: number) => void;
    onStartAddUpload?: () => void;
    onStartAddRecord?: () => void;
    onStartEditVoice?: (id: number) => void;
    onDeleteVoice?: (id: number) => void;
    onRefreshVoices: () => void;
    listClass?: string;
    showCreateActions?: boolean;
    showManagementActions?: boolean;
  } = $props();

  let searchQuery = $state('');

  const filteredVoices = $derived(
    searchQuery.trim()
      ? savedCloneSettings.filter(
          (voice) =>
            voice.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
            voice.lang.toLowerCase().includes(searchQuery.toLowerCase())
        )
      : savedCloneSettings
  );
</script>

<div class="space-y-3 pb-3">
  <div class="relative">
    <SearchIcon class="text-muted-foreground absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2" />
    <Input
      bind:value={searchQuery}
      placeholder={UI_TEXT.voiceLibrarySearchPlaceholder}
      class="pl-8 {searchQuery ? 'pr-8' : ''}"
    />
    {#if searchQuery}
      <Button
        variant="ghost"
        size="icon-xs"
        class="text-muted-foreground hover:text-foreground absolute top-1/2 right-1.5 -translate-y-1/2"
        onclick={() => {
          searchQuery = '';
        }}
        aria-label={UI_TEXT.clearVoiceSearch}
      >
        <XIcon class="size-3.5" />
      </Button>
    {/if}
  </div>

  <div class="flex gap-2">
    {#if showCreateActions}
      <Button variant="outline" class="flex-1 gap-1.5" onclick={onStartAddUpload} size="sm">
        <UploadIcon class="size-3.5" />
        {UI_TEXT.uploadVoice}
      </Button>
      <Button variant="outline" class="flex-1 gap-1.5" onclick={onStartAddRecord} size="sm">
        <MicIcon class="size-3.5" />
        {UI_TEXT.recordVoice}
      </Button>
    {/if}
    <Button
      variant="ghost"
      size="icon-sm"
      onclick={onRefreshVoices}
      disabled={isCloneSettingsLoading}
      aria-label={UI_TEXT.refreshVoiceListLabel}
    >
      <RefreshCwIcon class="size-3.5 {isCloneSettingsLoading ? 'animate-spin' : ''}" />
    </Button>
  </div>
</div>

<Separator class="mb-3" />

{#if cloneSettingsErrorMessage}
  <div
    class="mb-3 rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-400"
  >
    {cloneSettingsErrorMessage}
  </div>
{/if}
{#if cloneSettingsMessage}
  <div
    class="mb-3 rounded-md border border-emerald-500/30 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-400"
  >
    {cloneSettingsMessage}
  </div>
{/if}

<ScrollArea class={listClass}>
  {#if isCloneSettingsLoading && !hasLoadedCloneSettings}
    <div class="text-muted-foreground py-8 text-center text-sm">{UI_TEXT.loadingVoices}</div>
  {:else if filteredVoices.length === 0}
    <div class="text-muted-foreground py-8 text-center text-sm">
      {searchQuery
        ? UI_TEXT.noVoiceSearchResults
        : showCreateActions
          ? UI_TEXT.noVoicesSavedYet
          : UI_TEXT.noVoicesAvailable}
    </div>
  {:else}
    <div class="space-y-2 pr-3">
      {#each filteredVoices as voice (voice.id)}
        <VoiceListItem
          {voice}
          isSelected={voice.id === selectedCloneSettingId}
          onSelect={onSelectVoice}
          onEdit={onStartEditVoice}
          onDelete={onDeleteVoice}
          {showManagementActions}
        />
      {/each}
    </div>
  {/if}
</ScrollArea>
