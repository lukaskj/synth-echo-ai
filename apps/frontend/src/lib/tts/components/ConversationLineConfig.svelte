<script lang="ts">
  import * as Card from '$lib/components/ui/card/index.js';
  import { Textarea } from '$lib/components/ui/textarea/index.js';
  import AudioPlayer from '$lib/tts/components/AudioPlayer.svelte';
  import CloneSettings from '$lib/tts/components/CloneSettings.svelte';
  import GenerateAudioButton from '$lib/tts/components/GenerateAudioButton.svelte';
  import SynthesisSettings from '$lib/tts/components/SynthesisSettings.svelte';
  import VoiceSourceConfig from '$lib/tts/components/VoiceSourceConfig.svelte';
  import { UI_TEXT } from '$lib/tts/constants';
  import { buildInstruct } from '$lib/tts/helpers';
  import type {
    ConversationLineMutation,
    ConversationVoiceType,
    SavedCloneSetting
  } from '$lib/tts/types';
  import PanelLeftIcon from 'lucide-svelte/icons/panel-left';

  let {
    selectedLine,
    selectedLineIndex,
    activeGeneratingConversationLineIndex,
    savedCloneSettings,
    onUpdateVoiceType,
    onOpenVoiceLibrary,
    onGenerateLine
  }: {
    selectedLine: ConversationLineMutation | null;
    selectedLineIndex: number | null;
    activeGeneratingConversationLineIndex: number | null;
    savedCloneSettings: SavedCloneSetting[];
    onUpdateVoiceType: (voiceType: ConversationVoiceType) => void;
    onOpenVoiceLibrary: () => void;
    onGenerateLine: (line: ConversationLineMutation) => void | Promise<void>;
  } = $props();

  const selectedCloneSetting = $derived(
    selectedLine?.voice_type === 'clone'
      ? (savedCloneSettings.find((setting) => setting.id === selectedLine.clone_setting_id) ?? null)
      : null
  );
  const isSelectedLineGenerating = $derived(
    selectedLineIndex !== null && activeGeneratingConversationLineIndex === selectedLineIndex
  );

  let instruct = $derived(
    buildInstruct([
      selectedLine?.selected_gender || '',
      selectedLine?.selected_pitch || '',
      selectedLine?.selected_accent || '',
      selectedLine?.selected_age || '',
      selectedLine?.selected_style || ''
    ])
  );
</script>

<Card.Root class="h-fit">
  <Card.Header class="pb-3">
    <Card.Title class="flex items-center gap-2 text-sm font-semibold">
      <PanelLeftIcon class="size-4" />
      {UI_TEXT.conversationLineConfigTitle}
    </Card.Title>
  </Card.Header>
  <Card.Content>
    {#if selectedLine}
      <div class="space-y-4">
        <div class="space-y-2">
          <div class="text-sm font-medium">{UI_TEXT.conversationLineLabel} text</div>
          <Textarea
            bind:value={selectedLine.text}
            rows={4}
            class="min-h-[90px] resize-y"
            placeholder="Write what this line should say..."
          />
        </div>
        <VoiceSourceConfig
          value={selectedLine.voice_type}
          onValueChange={(value) => onUpdateVoiceType(value as ConversationVoiceType)}
          {savedCloneSettings}
          {selectedCloneSetting}
          {onOpenVoiceLibrary}
          noVoiceSelectedMessage={UI_TEXT.conversationNoVoiceSelected}
        >
          {#snippet cloneContent()}
            <CloneSettings
              bind:cloneLang={selectedLine.lang}
              bind:cloneSpeed={selectedLine.speed}
              bind:cloneNumStep={selectedLine.num_step}
            />
          {/snippet}
          {#snippet instructionContent()}
            <div class="space-y-3">
              <SynthesisSettings
                bind:lang={selectedLine.lang}
                bind:speed={selectedLine.speed}
                bind:numStep={selectedLine.num_step}
                bind:selectedGender={selectedLine.selected_gender}
                bind:selectedAccent={selectedLine.selected_accent}
                bind:selectedPitch={selectedLine.selected_pitch}
                bind:selectedAge={selectedLine.selected_age}
                bind:selectedStyle={selectedLine.selected_style}
                {instruct}
              />
              <div class="rounded-lg border border-dashed px-3 py-2 text-sm">
                <div class="text-muted-foreground mb-1 text-xs uppercase tracking-wide">
                  {UI_TEXT.currentInstruct}
                </div>
                <div>{instruct || UI_TEXT.noInstruction}</div>
              </div>
            </div>
          {/snippet}
        </VoiceSourceConfig>

        {#if selectedLine.audio_url}
          <div class="mb-4">
            <AudioPlayer
              src={selectedLine.audio_url}
              preload="metadata"
              ariaLabel="Selected conversation line audio"
            />
          </div>
        {/if}

        <GenerateAudioButton
          loading={isSelectedLineGenerating}
          isRegenerate={Boolean(selectedLine.audio_url)}
          size="default"
          className="w-full"
          onClick={() => {
            void onGenerateLine(selectedLine);
          }}
        />
      </div>
    {:else}
      <p class="text-muted-foreground text-sm">
        {UI_TEXT.conversationSelectLinePrompt}
      </p>
    {/if}
  </Card.Content>
</Card.Root>
