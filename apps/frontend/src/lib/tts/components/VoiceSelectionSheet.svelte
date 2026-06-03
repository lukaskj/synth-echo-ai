<script lang="ts">
  import * as Sheet from '$lib/components/ui/sheet/index.js';
  import VoiceLibraryBrowser from './VoiceLibraryBrowser.svelte';
  import AddVoiceView from './AddVoiceView.svelte';
  import RecordVoiceView from './RecordVoiceView.svelte';
  import EditVoiceView from './EditVoiceView.svelte';
  import type { SavedCloneSetting, CloneView } from '$lib/tts/types';
  import { DEFAULT_FORM_STATE, UI_TEXT } from '$lib/tts/constants';

  let {
    open = $bindable(false),
    cloneView,
    isRecordMode,
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
    open?: boolean;
    cloneView: CloneView;
    isRecordMode: boolean;
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

  const sheetView: 'list' | 'add-upload' | 'add-record' | 'edit' = $derived(
    cloneView === 'create'
      ? isRecordMode
        ? 'add-record'
        : 'add-upload'
      : cloneView === 'selected'
        ? 'edit'
        : 'list'
  );
</script>

<Sheet.Root bind:open>
  <Sheet.Content side="right" class="flex w-full flex-col sm:max-w-md">
    <Sheet.Header class="pb-2">
      <Sheet.Title>
        {#if sheetView === 'list'}
          {UI_TEXT.voiceLibraryTitle}
        {:else if sheetView === 'add-upload'}
          {UI_TEXT.uploadVoiceTitle}
        {:else if sheetView === 'add-record'}
          {UI_TEXT.recordVoiceTitle}
        {:else}
          {UI_TEXT.editVoiceTitle}
        {/if}
      </Sheet.Title>
    </Sheet.Header>

    <div class="flex flex-1 flex-col overflow-hidden px-1">
      {#if sheetView === 'list'}
        <!-- Search + action buttons -->
        <VoiceLibraryBrowser
          {savedCloneSettings}
          {selectedCloneSettingId}
          {isCloneSettingsLoading}
          {hasLoadedCloneSettings}
          {cloneSettingsMessage}
          {cloneSettingsErrorMessage}
          {onSelectVoice}
          {onStartAddUpload}
          {onStartAddRecord}
          {onStartEditVoice}
          {onDeleteVoice}
          {onRefreshVoices}
        />
      {:else if sheetView === 'add-upload'}
        <AddVoiceView
          bind:cloneSettingName
          bind:cloneRefText
          bind:cloneLang
          bind:cloneSpeed
          bind:cloneNumStep
          {cloneRefAudioFile}
          {cloneRefAudioPreviewUrl}
          {cloneRefAudioInputKey}
          {isSavingCloneSetting}
          {canSaveCloneSetting}
          {cloneSettingsErrorMessage}
          onSave={onSaveCloneSetting}
          onBack={onBackToList}
          {onRefAudioChange}
        />
      {:else if sheetView === 'add-record'}
        <RecordVoiceView
          bind:cloneSettingName
          bind:cloneRefText
          bind:cloneLang
          bind:cloneSpeed
          bind:cloneNumStep
          {cloneRefAudioPreviewUrl}
          {cloneRefAudioIsMicrophoneRecording}
          {isRecordingCloneRefAudio}
          {recordingElapsedLabel}
          {microphoneStatusMessage}
          {microphoneStatusIsError}
          {isSpeechRecognitionSupported}
          {canRecordCloneRefAudio}
          {isSavingCloneSetting}
          {canSaveCloneSetting}
          {cloneSettingsErrorMessage}
          {mediaStream}
          onSave={onSaveCloneSetting}
          onBack={onBackToList}
          {onToggleRecording}
        />
      {:else if sheetView === 'edit'}
        <EditVoiceView
          {selectedCloneSetting}
          bind:cloneSettingName
          bind:cloneLang
          bind:cloneSpeed
          bind:cloneNumStep
          {isUpdatingCloneSetting}
          {isDeletingCloneSetting}
          {canUpdateCloneSetting}
          {canDeleteCloneSetting}
          {cloneSettingsErrorMessage}
          {cloneSettingsMessage}
          onUpdate={onUpdateCloneSetting}
          onDelete={onDeleteSelectedVoice}
          onBack={onBackToList}
        />
      {/if}
    </div>
  </Sheet.Content>
</Sheet.Root>
