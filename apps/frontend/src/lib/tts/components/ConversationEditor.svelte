<script lang="ts">
  import { Badge } from '$lib/components/ui/badge/index.js';
  import { Button } from '$lib/components/ui/button/index.js';
  import * as Card from '$lib/components/ui/card/index.js';
  import { Input } from '$lib/components/ui/input/index.js';
  import { Label } from '$lib/components/ui/label/index.js';
  import AudioPlayer from '$lib/tts/components/AudioPlayer.svelte';
  import { UI_TEXT } from '$lib/tts/constants';
  import type { ConversationLineMutation } from '$lib/tts/types';
  import ArrowDownIcon from 'lucide-svelte/icons/arrow-down';
  import ArrowUpIcon from 'lucide-svelte/icons/arrow-up';
  import CheckIcon from 'lucide-svelte/icons/check';
  import LoaderIcon from 'lucide-svelte/icons/loader';
  import PencilLineIcon from 'lucide-svelte/icons/pencil-line';
  import PlayIcon from 'lucide-svelte/icons/play';
  import PlusIcon from 'lucide-svelte/icons/plus';
  import DownloadIcon from 'lucide-svelte/icons/download';
  import SquareIcon from 'lucide-svelte/icons/square';
  import Trash2Icon from 'lucide-svelte/icons/trash-2';
  import Wand from 'lucide-svelte/icons/wand-sparkles';

  let {
    selectedConversationId,
    conversationTitle,
    draftName,
    draftLines,
    selectedLineIndex,
    activeGeneratingConversationLineIndex = $bindable(null),
    playingLineIndex,
    playbackAudioSrc,
    playbackAudioElement = $bindable(null),
    isSavingConversation,
    isDownloadingConversation,
    onDraftNameChange,
    onSelectLine,
    onPlayConversation,
    onStopConversationPlayback,
    onDownloadConversation,
    onSaveConversation,
    onDeleteConversation,
    onMoveLine,
    onDeleteLine,
    onGenerateLine,
    onAddLine
  }: {
    selectedConversationId: number | null;
    conversationTitle: string;
    draftName: string;
    draftLines: ConversationLineMutation[];
    selectedLineIndex: number | null;
    activeGeneratingConversationLineIndex: number | null;
    playingLineIndex: number | null;
    playbackAudioSrc: string;
    playbackAudioElement?: HTMLAudioElement | null;
    isSavingConversation: boolean;
    isDownloadingConversation: boolean;
    onDraftNameChange: (value: string) => void;
    onSelectLine: (lineIndex: number) => void;
    onPlayConversation: () => void | Promise<void>;
    onStopConversationPlayback: () => void;
    onDownloadConversation: () => void | Promise<void>;
    onSaveConversation: () => void | Promise<void>;
    onDeleteConversation: () => void | Promise<void>;
    onMoveLine: (lineIndex: number, direction: -1 | 1) => void;
    onDeleteLine: (lineIndex: number) => void;
    onGenerateLine: (line: ConversationLineMutation) => void | Promise<void>;
    onAddLine: () => void;
  } = $props();

  const canPlayConversation = $derived(draftLines.some((line) => Boolean(line.audio_url)));
  const isConversationPlaying = $derived(playingLineIndex !== null);
  const canDownloadConversation = $derived(
    selectedConversationId !== null && draftLines.some((line) => Boolean(line.audio_url))
  );
</script>

{#snippet conversationPrimaryActions()}
  <Button
    variant="outline"
    class="gap-1.5"
    onclick={isConversationPlaying ? onStopConversationPlayback : onPlayConversation}
    disabled={!isConversationPlaying && !canPlayConversation}
    >
      {#if isConversationPlaying}
        <SquareIcon class="size-4" />
      {UI_TEXT.conversationStopPlayButton}
    {:else}
      <PlayIcon class="size-4" />
      {UI_TEXT.conversationPlayButton}
      {/if}
    </Button>
    {#if selectedConversationId !== null}
      <Button
        variant="outline"
        class="gap-1.5"
        onclick={onDownloadConversation}
        disabled={!canDownloadConversation || isDownloadingConversation}
      >
        {#if isDownloadingConversation}
          <LoaderIcon class="size-4 animate-spin" />
          {UI_TEXT.conversationDownloadingButton}
        {:else}
          <DownloadIcon class="size-4" />
          {UI_TEXT.conversationDownloadButton}
        {/if}
      </Button>
    {/if}
    <Button class="gap-1.5" onclick={onSaveConversation} disabled={isSavingConversation}>
      {#if isSavingConversation}
        <LoaderIcon class="size-4 animate-spin" />
    {:else}
      <CheckIcon class="size-4" />
    {/if}
    {UI_TEXT.conversationSaveButton}
  </Button>
{/snippet}

<Card.Root>
  <Card.Header class="pb-3">
    <div class="flex flex-wrap items-center justify-between gap-3">
      <div>
        <Card.Title class="text-lg font-semibold">{conversationTitle}</Card.Title>
        <Card.Description>
          {selectedConversationId === null
            ? UI_TEXT.conversationBuildDescription
            : UI_TEXT.conversationEditDescription}
        </Card.Description>
      </div>
      <div class="flex flex-wrap items-center gap-2">
        {@render conversationPrimaryActions()}
        {#if selectedConversationId !== null}
          <Button variant="ghost" class="gap-1.5 text-destructive" onclick={onDeleteConversation}>
            <Trash2Icon class="size-4" />
            {UI_TEXT.conversationDeleteButton}
          </Button>
        {/if}
      </div>
    </div>
  </Card.Header>
  <Card.Content class="space-y-4">
    <div class="space-y-2">
      <Label for="conversation-title">{UI_TEXT.conversationNameLabel}</Label>
      <Input
        id="conversation-title"
        type="text"
        value={draftName}
        class="h-10"
        placeholder={UI_TEXT.conversationNamePlaceholder}
        oninput={(event) => onDraftNameChange((event.currentTarget as HTMLInputElement).value)}
      />
    </div>

    <AudioPlayer
      bind:audioElement={playbackAudioElement}
      src={playbackAudioSrc}
      preload="auto"
      controls={false}
      className="hidden"
      ariaLabel={UI_TEXT.conversationPlaybackTitle}
    />

    <div class="space-y-3">
      {#each draftLines as line, index (line.position)}
        <Card.Root
          class={`gap-2 border border-accent pt-2 w-full ${selectedLineIndex === index ? 'border-secondary bg-primary/6' : ''}`}
          role="button"
          onclick={() => onSelectLine(index)}
        >
          <Card.Header class="">
            <Card.Title class="flex gap-2">
              <div class="flex flex-row justify-between w-full relative">
                {#if playingLineIndex === index}
                  <div class="w-full absolute flex flex-row justify-center">
                    <Badge variant="secondary" class="gap-1.5">
                      <PlayIcon class="size-3 animate-pulse" />
                      {UI_TEXT.conversationLinePlaying}
                    </Badge>
                  </div>
                {/if}
                <div class="flex items-center justify-start gap-1 relative">
                  <Button
                    variant="ghost"
                    size="sm"
                    class="gap-1.5 pl-0"
                    onclick={(event) => {
                      event.stopPropagation();
                      onSelectLine(index);
                    }}
                  >
                    <PencilLineIcon class="size-4" />
                    {UI_TEXT.conversationConfigureButton}
                  </Button>
                  <Badge variant="outline">{UI_TEXT.conversationLineLabel} {index + 1}</Badge>
                  <Badge variant="outline">{line.voice_label}</Badge>
                </div>
                <div class="flex items-end justify-end gap-0">
                  <Button
                    variant="ghost"
                    size="icon-sm"
                    aria-label={`Move line ${index + 1} up`}
                    onclick={(event) => {
                      event.stopPropagation();
                      onMoveLine(index, -1);
                    }}
                    disabled={index === 0}
                  >
                    <ArrowUpIcon class="size-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon-sm"
                    aria-label={`Move line ${index + 1} down`}
                    onclick={(event) => {
                      event.stopPropagation();
                      onMoveLine(index, 1);
                    }}
                    disabled={index === draftLines.length - 1}
                  >
                    <ArrowDownIcon class="size-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon-sm"
                    aria-label={`Delete line ${index + 1}`}
                    onclick={(event) => {
                      event.stopPropagation();
                      onDeleteLine(index);
                    }}
                  >
                    <Trash2Icon class="size-4" />
                  </Button>
                </div>
              </div>
            </Card.Title>
          </Card.Header>
          <Card.Content class="space-y-3 w-full">
            <div class="flex flex-row justify-between items-center w-full">
              <p class="text-sm leading-relaxed break-words text-wrap max-w-[85%]">
                {line.text || UI_TEXT.conversationLineEmpty}
              </p>
              <Button
                class="cursor-pointer "
                variant="outline"
                size="lg"
                title={line.audio_url
                  ? UI_TEXT.conversationLineRegenerate
                  : UI_TEXT.conversationLineGenerate}
                onclick={() => {
                  onSelectLine(index);
                  void onGenerateLine(line);
                }}
              >
                {#if activeGeneratingConversationLineIndex === index}
                  <LoaderIcon class="size-4 animate-spin" />
                {:else}
                  <Wand class="size-4" />
                {/if}
              </Button>
            </div>
            {#if line.audio_url}
              <div class="mt-3">
                <AudioPlayer
                  src={line.audio_url}
                  preload="metadata"
                  ariaLabel={`Conversation line ${index + 1} audio`}
                />
              </div>
            {/if}
          </Card.Content>
        </Card.Root>
      {/each}
    </div>

    <Button variant="outline" class="w-full gap-1.5" onclick={onAddLine}>
      <PlusIcon class="size-4" />
      {UI_TEXT.conversationAddLine}
    </Button>

    <div class="flex flex-wrap items-center justify-end gap-2">
      {@render conversationPrimaryActions()}
    </div>
  </Card.Content>
</Card.Root>
