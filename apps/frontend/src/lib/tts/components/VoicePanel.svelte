<script lang="ts">
  import * as Card from '$lib/components/ui/card/index.js';

  import MicIcon from 'lucide-svelte/icons/mic';
  import SlidersIcon from 'lucide-svelte/icons/sliders';
  import SynthesisSettings from './SynthesisSettings.svelte';
  import CloneSettings from './CloneSettings.svelte';
  import VoiceSourceConfig from './VoiceSourceConfig.svelte';
  import VoiceSelectionSheet from './VoiceSelectionSheet.svelte';
  import type { TtsMode, CloneView, SavedCloneSetting } from '$lib/tts/types';
  import { DEFAULT_FORM_STATE, UI_TEXT } from '$lib/tts/constants';

  let {
    mode = $bindable('synthesize'),
    cloneView,
    isRecordMode,
    isVoiceSheetOpen = $bindable(false),
    savedCloneSettings,
    selectedCloneSettingId,
    selectedCloneSetting,
    isCloneSettingsLoading,
    hasLoadedCloneSettings,
    isSavingCloneSetting,
    isUpdatingCloneSetting,
    isDeletingCloneSetting,
    canSaveCloneSetting,
    canUpdateCloneSetting,
    canDeleteCloneSetting,
    cloneSettingsMessage,
    cloneSettingsErrorMessage,
    cloneSettingName = $bindable(''),
    cloneRefText = $bindable(''),
    cloneLang = $bindable(DEFAULT_FORM_STATE.cloneLang),
    cloneSpeed = $bindable(DEFAULT_FORM_STATE.cloneSpeed),
    cloneNumStep = $bindable(DEFAULT_FORM_STATE.cloneNumStep),
    synthesizeLang = $bindable(DEFAULT_FORM_STATE.lang),
    synthesizeSpeed = $bindable(DEFAULT_FORM_STATE.speed),
    synthesizeNumStep = $bindable(DEFAULT_FORM_STATE.numStep),
    selectedGender = $bindable(DEFAULT_FORM_STATE.selectedGender),
    selectedAccent = $bindable(DEFAULT_FORM_STATE.selectedAccent),
    selectedPitch = $bindable(DEFAULT_FORM_STATE.selectedPitch),
    selectedAge = $bindable(DEFAULT_FORM_STATE.selectedAge),
    selectedStyle = $bindable(DEFAULT_FORM_STATE.selectedStyle),
    instruct,
    cloneRefAudioFile,
    cloneRefAudioPreviewUrl,
    cloneRefAudioInputKey,
    cloneRefAudioIsMicrophoneRecording,
    isRecordingCloneRefAudio,
    recordingElapsedLabel,
    microphoneStatusMessage,
    microphoneStatusIsError,
    isSpeechRecognitionSupported,
    canRecordCloneRefAudio,
    mediaStream,
    onSelectVoice,
    onStartAddUpload,
    onStartAddRecord,
    onStartEditVoice,
    onSaveCloneSetting,
    onUpdateCloneSetting,
    onDeleteVoice,
    onDeleteSelectedVoice,
    onBackToList,
    onRefreshVoices,
    onToggleRecording,
    onRefAudioChange
  }: {
    mode?: TtsMode;
    cloneView: CloneView;
    isRecordMode: boolean;
    isVoiceSheetOpen?: boolean;
    savedCloneSettings: SavedCloneSetting[];
    selectedCloneSettingId: number | null;
    selectedCloneSetting: SavedCloneSetting | null;
    isCloneSettingsLoading: boolean;
    hasLoadedCloneSettings: boolean;
    isSavingCloneSetting: boolean;
    isUpdatingCloneSetting: boolean;
    isDeletingCloneSetting: boolean;
    canSaveCloneSetting: boolean;
    canUpdateCloneSetting: boolean;
    canDeleteCloneSetting: boolean;
    cloneSettingsMessage: string;
    cloneSettingsErrorMessage: string;
    cloneSettingName?: string;
    cloneRefText?: string;
    cloneLang?: string;
    cloneSpeed?: number;
    cloneNumStep?: number;
    synthesizeLang?: string;
    synthesizeSpeed?: number;
    synthesizeNumStep?: number;
    selectedGender?: string;
    selectedAccent?: string;
    selectedPitch?: string;
    selectedAge?: string;
    selectedStyle?: string;
    instruct: string;
    cloneRefAudioFile: File | null;
    cloneRefAudioPreviewUrl: string;
    cloneRefAudioInputKey: number;
    cloneRefAudioIsMicrophoneRecording: boolean;
    isRecordingCloneRefAudio: boolean;
    recordingElapsedLabel: string;
    microphoneStatusMessage: string;
    microphoneStatusIsError: boolean;
    isSpeechRecognitionSupported: boolean;
    canRecordCloneRefAudio: boolean;
    mediaStream: MediaStream | null;
    onSelectVoice: (id: number) => void;
    onStartAddUpload: () => void;
    onStartAddRecord: () => void;
    onStartEditVoice: (id: number) => void;
    onSaveCloneSetting: () => void;
    onUpdateCloneSetting: () => void;
    onDeleteVoice: (id: number) => void;
    onDeleteSelectedVoice: () => void;
    onBackToList: () => void;
    onRefreshVoices: () => void;
    onToggleRecording: () => Promise<void>;
    onRefAudioChange: (event: Event) => void;
  } = $props();

  const isCloneMode = $derived(mode === 'clone');
</script>

<div class="flex flex-col gap-4">
  <!-- Voice Selection Card -->
  <Card.Root>
    <Card.Header class="pb-3">
      <Card.Title class="flex items-center gap-2 text-sm font-semibold">
        <MicIcon class="size-4" />
        Voice
      </Card.Title>
    </Card.Header>

    <Card.Content>
      <VoiceSourceConfig
        value={isCloneMode ? 'clone' : 'instruction'}
        onValueChange={(value) => {
          mode = value === 'clone' ? 'clone' : 'synthesize';
        }}
        {savedCloneSettings}
        {selectedCloneSetting}
        onOpenVoiceLibrary={() => {
          isVoiceSheetOpen = true;
        }}
        noVoiceSelectedMessage={UI_TEXT.conversationNoVoiceSelected}
        selectedVoiceBadgeLabel="Active"
      >
        {#snippet instructionContent()}
          <SynthesisSettings
            bind:lang={synthesizeLang}
            bind:speed={synthesizeSpeed}
            bind:numStep={synthesizeNumStep}
            bind:selectedGender
            bind:selectedAccent
            bind:selectedPitch
            bind:selectedAge
            bind:selectedStyle
            {instruct}
          />
        {/snippet}
      </VoiceSourceConfig>
    </Card.Content>
  </Card.Root>

  {#if isCloneMode}
    <!-- Settings Card -->
    <Card.Root>
      <Card.Header class="pb-3">
        <Card.Title class="flex items-center gap-2 text-sm font-semibold">
          <SlidersIcon class="size-4" />
          Clone Settings
        </Card.Title>
      </Card.Header>
      <Card.Content>
        <CloneSettings bind:cloneLang bind:cloneSpeed bind:cloneNumStep />
      </Card.Content>
    </Card.Root>
  {/if}
</div>

<!-- Voice Selection Sheet (rendered here, uses portal) -->
<VoiceSelectionSheet
  bind:open={isVoiceSheetOpen}
  {cloneView}
  {isRecordMode}
  {savedCloneSettings}
  {selectedCloneSettingId}
  {selectedCloneSetting}
  {isCloneSettingsLoading}
  {hasLoadedCloneSettings}
  {isSavingCloneSetting}
  {isUpdatingCloneSetting}
  {isDeletingCloneSetting}
  {canSaveCloneSetting}
  {canUpdateCloneSetting}
  {canDeleteCloneSetting}
  {cloneSettingsMessage}
  {cloneSettingsErrorMessage}
  bind:cloneSettingName
  bind:cloneRefText
  bind:cloneLang
  bind:cloneSpeed
  bind:cloneNumStep
  {cloneRefAudioFile}
  {cloneRefAudioPreviewUrl}
  {cloneRefAudioInputKey}
  {cloneRefAudioIsMicrophoneRecording}
  {isRecordingCloneRefAudio}
  {recordingElapsedLabel}
  {microphoneStatusMessage}
  {microphoneStatusIsError}
  {isSpeechRecognitionSupported}
  {canRecordCloneRefAudio}
  {mediaStream}
  {onSelectVoice}
  {onStartAddUpload}
  {onStartAddRecord}
  {onStartEditVoice}
  {onSaveCloneSetting}
  {onUpdateCloneSetting}
  {onDeleteVoice}
  {onDeleteSelectedVoice}
  {onBackToList}
  {onRefreshVoices}
  {onToggleRecording}
  {onRefAudioChange}
/>
