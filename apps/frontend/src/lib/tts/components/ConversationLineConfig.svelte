<script lang="ts">
  import { Button } from '$lib/components/ui/button/index.js';
  import * as Card from '$lib/components/ui/card/index.js';
  import { Label } from '$lib/components/ui/label/index.js';
  import * as Select from '$lib/components/ui/select/index.js';
  import { Textarea } from '$lib/components/ui/textarea/index.js';
  import AudioPlayer from '$lib/tts/components/AudioPlayer.svelte';
  import GenerateAudioButton from '$lib/tts/components/GenerateAudioButton.svelte';
  import SynthesisSettings from '$lib/tts/components/SynthesisSettings.svelte';
  import { LANGUAGES, UI_TEXT } from '$lib/tts/constants';
  import { buildInstruct } from '$lib/tts/helpers';
  import type {
    ConversationLineMutation,
    ConversationVoiceType,
    SavedCloneSetting
  } from '$lib/tts/types';
  import ChevronRightIcon from 'lucide-svelte/icons/chevron-right';
  import MicIcon from 'lucide-svelte/icons/mic';
  import PanelLeftIcon from 'lucide-svelte/icons/panel-left';
  import WandSparklesIcon from 'lucide-svelte/icons/wand-sparkles';

  const voiceTypeOptions: { value: ConversationVoiceType; label: string }[] = [
    { value: 'clone', label: 'Voice library' },
    { value: 'instruction', label: 'Voice instruction' }
  ];

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
  const selectedVoiceLangLabel = $derived(
    selectedCloneSetting
      ? (LANGUAGES.find((option) => option.value === selectedCloneSetting.lang)?.label ??
          selectedCloneSetting.lang.toUpperCase())
      : ''
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
  <Card.Header class="pb-1">
    <Card.Title class="flex items-center gap-2 text-sm font-semibold">
      <PanelLeftIcon class="size-4" />
      {UI_TEXT.conversationLineConfigTitle}
    </Card.Title>
  </Card.Header>
  <Card.Content>
    {#if selectedLine}
      <div class="space-y-4">
        <div class="space-y-2">
          <Label>{UI_TEXT.conversationLineLabel} text</Label>
          <Textarea
            bind:value={selectedLine.text}
            rows={8}
            class="min-h-[180px] resize-y"
            placeholder="Write what this line should say..."
          />
        </div>
        <div class="space-y-2">
          <Label>{UI_TEXT.conversationVoiceSourceLabel}</Label>
          <Select.Root
            value={selectedLine.voice_type}
            onValueChange={(value) => onUpdateVoiceType(value as ConversationVoiceType)}
          >
            <Select.Trigger>
              {voiceTypeOptions.find((option) => option.value === selectedLine.voice_type)?.label ??
                'Select source'}
            </Select.Trigger>
            <Select.Content>
              {#each voiceTypeOptions as option (option.value)}
                <Select.Item value={option.value} label={option.label} />
              {/each}
            </Select.Content>
          </Select.Root>
        </div>

        {#if selectedLine.voice_type === 'clone'}
          <div class="space-y-3">
            <Label>{UI_TEXT.voiceLibraryTitle}</Label>
            {#if selectedCloneSetting}
              <div class="bg-muted/40 flex items-center gap-3 rounded-lg px-3 py-2.5">
                <div
                  class="bg-primary/15 flex size-8 shrink-0 items-center justify-center rounded-full"
                >
                  <MicIcon class="text-primary size-4" />
                </div>
                <div class="min-w-0 flex-1">
                  <p class="text-foreground truncate text-sm font-medium">
                    {selectedCloneSetting.name}
                  </p>
                  <p class="text-muted-foreground text-xs">{selectedVoiceLangLabel}</p>
                </div>
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
                    {savedCloneSettings.length > 0
                      ? UI_TEXT.conversationNoVoiceSelected
                      : UI_TEXT.noVoicesAvailable}
                  </p>
                </div>
              </div>
            {/if}

            <div>
              <Button variant="outline" class="w-full gap-2" onclick={onOpenVoiceLibrary}>
                {UI_TEXT.selectVoiceButton}
                <ChevronRightIcon class="size-3.5" />
              </Button>
            </div>
          </div>
        {:else}
          <div class="space-y-3">
            <Label>{UI_TEXT.conversationVoiceInstructionLabel} aaa</Label>
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
            <!-- <div class="grid gap-3 sm:grid-cols-2">
              <div class="space-y-2">
                <Label>{UI_TEXT.gender}</Label>
                <Select.Root
                  value={selectedLine.selected_gender}
                  onValueChange={(value) => onUpdateInstructionField('selected_gender', value)}
                >
                  <Select.Trigger>
                    {GENDER_OPTIONS.find((option) => option.value === selectedLine.selected_gender)
                      ?.label ?? 'Select gender'}
                  </Select.Trigger>
                  <Select.Content>
                    {#each GENDER_OPTIONS as option (option.value)}
                      <Select.Item value={option.value} label={option.label} />
                    {/each}
                  </Select.Content>
                </Select.Root>
              </div>
              <div class="space-y-2">
                <Label>{UI_TEXT.accent}</Label>
                <Select.Root
                  value={selectedLine.selected_accent}
                  onValueChange={(value) => onUpdateInstructionField('selected_accent', value)}
                >
                  <Select.Trigger>
                    {ACCENT_OPTIONS.find((option) => option.value === selectedLine.selected_accent)
                      ?.label ?? 'Select accent'}
                  </Select.Trigger>
                  <Select.Content>
                    {#each ACCENT_OPTIONS as option (option.value)}
                      <Select.Item value={option.value} label={option.label} />
                    {/each}
                  </Select.Content>
                </Select.Root>
              </div>
              <div class="space-y-2">
                <Label>{UI_TEXT.pitch}</Label>
                <Select.Root
                  value={selectedLine.selected_pitch}
                  onValueChange={(value) => onUpdateInstructionField('selected_pitch', value)}
                >
                  <Select.Trigger>
                    {PITCH_OPTIONS.find((option) => option.value === selectedLine.selected_pitch)
                      ?.label ?? 'Select pitch'}
                  </Select.Trigger>
                  <Select.Content>
                    {#each PITCH_OPTIONS as option (option.value)}
                      <Select.Item value={option.value} label={option.label} />
                    {/each}
                  </Select.Content>
                </Select.Root>
              </div>
              <div class="space-y-2">
                <Label>{UI_TEXT.age}</Label>
                <Select.Root
                  value={selectedLine.selected_age}
                  onValueChange={(value) => onUpdateInstructionField('selected_age', value)}
                >
                  <Select.Trigger>
                    {AGE_OPTIONS.find((option) => option.value === selectedLine.selected_age)
                      ?.label ?? 'Select age'}
                  </Select.Trigger>
                  <Select.Content>
                    {#each AGE_OPTIONS as option (option.value)}
                      <Select.Item value={option.value} label={option.label} />
                    {/each}
                  </Select.Content>
                </Select.Root>
              </div>
              <div class="space-y-2 sm:col-span-2">
                <Label>{UI_TEXT.style}</Label>
                <Select.Root
                  value={selectedLine.selected_style}
                  onValueChange={(value) => onUpdateInstructionField('selected_style', value)}
                >
                  <Select.Trigger>
                    {STYLE_OPTIONS.find((option) => option.value === selectedLine.selected_style)
                      ?.label ?? 'Select style'}
                  </Select.Trigger>
                  <Select.Content>
                    {#each STYLE_OPTIONS as option (option.value)}
                      <Select.Item value={option.value} label={option.label} />
                    {/each}
                  </Select.Content>
                </Select.Root>
              </div>
            </div> -->
            <div class="rounded-lg border border-dashed px-3 py-2 text-sm">
              <div class="text-muted-foreground mb-1 text-xs uppercase tracking-wide">
                {UI_TEXT.currentInstruct}
              </div>
              <div>{selectedLine.instruct}</div>
            </div>
          </div>
        {/if}

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
