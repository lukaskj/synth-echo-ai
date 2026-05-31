<script lang="ts">
  import Button from '$lib/tts/components/Button.svelte';
  import { UI_TEXT } from '$lib/tts/constants';
  import type { CloneView, SavedCloneSetting } from '$lib/tts/types';
  import CloneSettingCreateForm from './CloneSettingCreateForm.svelte';
  import NoticeBanner from './NoticeBanner.svelte';
  import SavedCloneSettingsList from './SavedCloneSettingsList.svelte';
  import SelectedCloneSettingForm from './SelectedCloneSettingForm.svelte';

  type Props = {
    cloneView: CloneView;
    cloneSettingName: string;
    cloneRefText: string;
    cloneRefAudioInputKey: number;
    cloneRefAudioName: string;
    cloneRefAudioIsMicrophoneRecording: boolean;
    cloneRefAudioPreviewUrl: string;
    isRecordingCloneRefAudio: boolean;
    recordingElapsedLabel: string;
    isSpeechRecognitionSupported: boolean;
    microphoneStatusMessage: string;
    microphoneStatusIsError: boolean;
    canRecordCloneRefAudio: boolean;
    cloneLang: string;
    cloneSpeed: number;
    cloneNumStep: number;
    canSaveCloneSetting: boolean;
    canUpdateCloneSetting: boolean;
    canDeleteCloneSetting: boolean;
    cloneSettingsErrorMessage: string;
    cloneSettingsMessage: string;
    isCloneSettingsLoading: boolean;
    isLoadingSelectedCloneSetting: boolean;
    isSavingCloneSetting: boolean;
    isUpdatingCloneSetting: boolean;
    isDeletingCloneSetting: boolean;
    savedCloneSettings: SavedCloneSetting[];
    selectedCloneSetting: SavedCloneSetting | null;
    onRefreshCloneSettings: () => void | Promise<void>;
    onBackToCloneSettingsList: () => void | Promise<void>;
    onStartCreateCloneSetting: () => void | Promise<void>;
    onCancelCreateCloneSetting: () => void | Promise<void>;
    onSaveCloneSetting: () => void | Promise<void>;
    onUpdateSelectedCloneSetting: () => void | Promise<void>;
    onSelectSavedCloneSetting: (settingId: number) => void | Promise<void>;
    onDeleteSelectedCloneSetting: () => void | Promise<void>;
    onDeleteSavedCloneSetting: (settingId: number) => void | Promise<void>;
    onRefAudioChange: (event: Event) => void;
    onToggleCloneRefRecording: () => void | Promise<void>;
  };

  let {
    cloneView,
    cloneSettingName = $bindable(),
    cloneRefText = $bindable(),
    cloneRefAudioInputKey,
    cloneRefAudioName,
    cloneRefAudioIsMicrophoneRecording,
    cloneRefAudioPreviewUrl,
    isRecordingCloneRefAudio,
    recordingElapsedLabel,
    isSpeechRecognitionSupported,
    microphoneStatusMessage,
    microphoneStatusIsError,
    canRecordCloneRefAudio,
    cloneLang = $bindable(),
    cloneSpeed = $bindable(),
    cloneNumStep = $bindable(),
    canSaveCloneSetting,
    canUpdateCloneSetting,
    canDeleteCloneSetting,
    cloneSettingsErrorMessage,
    cloneSettingsMessage,
    isCloneSettingsLoading,
    isLoadingSelectedCloneSetting,
    isSavingCloneSetting,
    isUpdatingCloneSetting,
    isDeletingCloneSetting,
    savedCloneSettings,
    selectedCloneSetting,
    onRefreshCloneSettings,
    onBackToCloneSettingsList,
    onStartCreateCloneSetting,
    onCancelCreateCloneSetting,
    onSaveCloneSetting,
    onUpdateSelectedCloneSetting,
    onSelectSavedCloneSetting,
    onDeleteSelectedCloneSetting,
    onDeleteSavedCloneSetting,
    onRefAudioChange,
    onToggleCloneRefRecording
  }: Props = $props();

  let hasReferenceTranscript = $derived(cloneRefText.trim().length > 0);
  let shouldShowSpeechRecognitionHint = $derived(
    !isSpeechRecognitionSupported && !hasReferenceTranscript
  );
  let shouldShowMicrophoneStatus = $derived(
    Boolean(microphoneStatusMessage) && (!microphoneStatusIsError || !hasReferenceTranscript)
  );
</script>

<div class="space-y-4 rounded-lg border border-slate-800 bg-slate-950/50 p-4">
  <div class="flex flex-wrap items-start justify-between gap-3">
    <div>
      <h3 class="text-base font-semibold text-white">{UI_TEXT.savedCloneSettingsTitle}</h3>
      <p class="mt-1 text-sm leading-6 text-slate-400">{UI_TEXT.savedCloneSettingsDescription}</p>
    </div>
    <div class="flex flex-wrap gap-2">
      {#if cloneView !== 'create'}
        <Button
          type="button"
          variant="secondary"
          size="small"
          onclick={onRefreshCloneSettings}
          disabled={isCloneSettingsLoading}
        >
          {isCloneSettingsLoading ? UI_TEXT.refreshingCloneSettings : UI_TEXT.refreshCloneSettings}
        </Button>
      {/if}
      {#if cloneView !== 'create'}
        <Button type="button" variant="primary" size="small" onclick={onStartCreateCloneSetting}>
          {UI_TEXT.createCloneSetting}
        </Button>
      {/if}
    </div>
  </div>

  {#if cloneSettingsErrorMessage}
    <NoticeBanner tone="error" className="p-4" role="alert"
      >{cloneSettingsErrorMessage}</NoticeBanner
    >
  {:else if cloneSettingsMessage}
    <NoticeBanner tone="success" className="p-4">{cloneSettingsMessage}</NoticeBanner>
  {/if}

  {#if cloneView === 'create'}
    <CloneSettingCreateForm
      bind:cloneSettingName
      bind:cloneRefText
      {cloneRefAudioInputKey}
      {cloneRefAudioName}
      {cloneRefAudioIsMicrophoneRecording}
      {cloneRefAudioPreviewUrl}
      {isRecordingCloneRefAudio}
      {recordingElapsedLabel}
      {shouldShowSpeechRecognitionHint}
      {shouldShowMicrophoneStatus}
      {microphoneStatusMessage}
      {microphoneStatusIsError}
      {canRecordCloneRefAudio}
      bind:cloneLang
      bind:cloneSpeed
      bind:cloneNumStep
      {canSaveCloneSetting}
      {isSavingCloneSetting}
      {onSaveCloneSetting}
      {onCancelCreateCloneSetting}
      {onToggleCloneRefRecording}
      {onRefAudioChange}
    />
  {:else if cloneView === 'selected' && selectedCloneSetting}
    <SelectedCloneSettingForm
      bind:cloneSettingName
      bind:cloneLang
      bind:cloneSpeed
      bind:cloneNumStep
      {selectedCloneSetting}
      {canUpdateCloneSetting}
      {canDeleteCloneSetting}
      {isUpdatingCloneSetting}
      {isDeletingCloneSetting}
      {onBackToCloneSettingsList}
      {onUpdateSelectedCloneSetting}
      {onDeleteSelectedCloneSetting}
    />
  {:else if savedCloneSettings.length > 0}
    <SavedCloneSettingsList
      {savedCloneSettings}
      {isLoadingSelectedCloneSetting}
      {onSelectSavedCloneSetting}
      {onDeleteSavedCloneSetting}
    />
  {:else if isCloneSettingsLoading}
    <NoticeBanner tone="muted" className="p-4">{UI_TEXT.refreshingCloneSettings}</NoticeBanner>
  {:else}
    <NoticeBanner tone="muted" className="p-4">{UI_TEXT.savedCloneSettingsEmpty}</NoticeBanner>
  {/if}
</div>
