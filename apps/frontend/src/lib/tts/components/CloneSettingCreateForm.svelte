<script lang="ts">
  import { LANGUAGES, UI_TEXT } from '$lib/tts/constants';
  import AudioPreviewCard from './AudioPreviewCard.svelte';
  import Button from './Button.svelte';
  import RangeField from './RangeField.svelte';
  import SelectField from './SelectField.svelte';
  import TextInputField from './TextInputField.svelte';
  import TextareaField from './TextareaField.svelte';

  type Props = {
    cloneSettingName: string;
    cloneRefText: string;
    cloneRefAudioInputKey: number;
    cloneRefAudioName: string;
    cloneRefAudioIsMicrophoneRecording: boolean;
    cloneRefAudioPreviewUrl: string;
    isRecordingCloneRefAudio: boolean;
    recordingElapsedLabel: string;
    shouldShowSpeechRecognitionHint: boolean;
    shouldShowMicrophoneStatus: boolean;
    microphoneStatusMessage: string;
    microphoneStatusIsError: boolean;
    canRecordCloneRefAudio: boolean;
    cloneLang: string;
    cloneSpeed: number;
    cloneNumStep: number;
    canSaveCloneSetting: boolean;
    isSavingCloneSetting: boolean;
    onSaveCloneSetting: () => void | Promise<void>;
    onCancelCreateCloneSetting: () => void | Promise<void>;
    onToggleCloneRefRecording: () => void | Promise<void>;
    onRefAudioChange: (event: Event) => void;
  };

  let {
    cloneSettingName = $bindable(),
    cloneRefText = $bindable(),
    cloneRefAudioInputKey,
    cloneRefAudioName,
    cloneRefAudioIsMicrophoneRecording,
    cloneRefAudioPreviewUrl,
    isRecordingCloneRefAudio,
    recordingElapsedLabel,
    shouldShowSpeechRecognitionHint,
    shouldShowMicrophoneStatus,
    microphoneStatusMessage,
    microphoneStatusIsError,
    canRecordCloneRefAudio,
    cloneLang = $bindable(),
    cloneSpeed = $bindable(),
    cloneNumStep = $bindable(),
    canSaveCloneSetting,
    isSavingCloneSetting,
    onSaveCloneSetting,
    onCancelCreateCloneSetting,
    onToggleCloneRefRecording,
    onRefAudioChange
  }: Props = $props();
</script>

<div class="space-y-4 rounded-lg border border-emerald-500/20 bg-slate-900/70 p-4">
  <div>
    <h4 class="text-base font-semibold text-white">{UI_TEXT.createCloneSettingTitle}</h4>
    <p class="mt-1 text-sm leading-6 text-slate-400">{UI_TEXT.createCloneSettingDescription}</p>
  </div>

  <TextInputField
    id="clone-setting-name"
    label={UI_TEXT.cloneSettingNameLabel}
    placeholder={UI_TEXT.cloneSettingNamePlaceholder}
    bind:value={cloneSettingName}
  />

  <SelectField
    id="clone-language-select"
    label={UI_TEXT.language}
    options={LANGUAGES}
    bind:value={cloneLang}
  />

  <div class="grid gap-4 px-1">
    <RangeField
      id="clone-speed-range"
      label={UI_TEXT.speed}
      displayValue={`${cloneSpeed.toFixed(1)}x`}
      min={0.5}
      max={2}
      step={0.1}
      bind:value={cloneSpeed}
    />

    <RangeField
      id="clone-step-range"
      label={UI_TEXT.diffusionSteps}
      displayValue={`${cloneNumStep}`}
      min={8}
      max={64}
      step={8}
      bind:value={cloneNumStep}
    />
  </div>

  <div class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-slate-200" for="ref-audio"
        >{UI_TEXT.refAudioLabel}</label
      >
      <div class="mt-3 flex flex-wrap items-center gap-3">
        <Button
          type="button"
          variant={isRecordingCloneRefAudio ? 'danger' : 'primary'}
          size="small"
          onclick={onToggleCloneRefRecording}
          disabled={!canRecordCloneRefAudio}
        >
          {isRecordingCloneRefAudio ? UI_TEXT.stopRecording : UI_TEXT.startRecording}
        </Button>
        {#if isRecordingCloneRefAudio}
          <div
            class="inline-flex items-center gap-2 rounded-full border border-rose-500/30 bg-rose-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-rose-100"
          >
            <span class="h-2.5 w-2.5 rounded-full bg-rose-400"></span>
            <span>{UI_TEXT.recordingInProgress}</span>
            <span aria-label={UI_TEXT.recordingTimerLabel}>{recordingElapsedLabel}</span>
          </div>
        {/if}
      </div>
      {#if shouldShowMicrophoneStatus}
        <p
          class={`mt-3 text-sm leading-6 ${microphoneStatusIsError ? 'text-amber-200' : 'text-slate-400'}`}
        >
          {microphoneStatusMessage}
        </p>
      {/if}
      {#if shouldShowSpeechRecognitionHint}
        <p class="mt-3 text-sm leading-6 text-slate-400">{UI_TEXT.speechRecognitionNotSupported}</p>
      {/if}
      <div
        class="mt-3 rounded-lg border border-dashed border-slate-700 bg-slate-950/60 px-4 py-4 text-sm text-slate-300"
      >
        {#key cloneRefAudioInputKey}
          <input
            id="ref-audio"
            name="ref_audio"
            type="file"
            accept="audio/*"
            disabled={isRecordingCloneRefAudio}
            onchange={onRefAudioChange}
            class="block w-full cursor-pointer text-sm text-slate-200 file:mr-4 file:rounded-md file:border-0 file:bg-violet-400 file:px-3 file:py-2 file:font-semibold file:text-slate-950 hover:file:bg-violet-300"
          />
        {/key}
        {#if cloneRefAudioName}
          <div
            class="mt-3 flex flex-wrap items-center gap-2 text-xs uppercase tracking-[0.18em] text-slate-500"
          >
            <p>{cloneRefAudioName}</p>
            {#if cloneRefAudioIsMicrophoneRecording}
              <span
                class="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2 py-1 text-[10px] font-semibold text-emerald-100"
              >
                {UI_TEXT.microphoneRecordingBadge}
              </span>
            {/if}
          </div>
        {/if}
        {#if cloneRefAudioPreviewUrl}
          <AudioPreviewCard
            title={UI_TEXT.referenceAudioPreview}
            src={cloneRefAudioPreviewUrl}
            preload="metadata"
            className="mt-4"
          />
        {/if}
      </div>
    </div>

    <TextareaField
      id="ref-text"
      label={UI_TEXT.refTextLabel}
      rows={4}
      placeholder={UI_TEXT.refTextPlaceholder}
      bind:value={cloneRefText}
    />
  </div>

  <div class="flex flex-wrap gap-3">
    <Button
      type="button"
      variant="primary"
      size="medium"
      class="flex-1"
      onclick={onSaveCloneSetting}
      disabled={!canSaveCloneSetting}
    >
      {isSavingCloneSetting ? UI_TEXT.savingCloneSetting : UI_TEXT.saveCloneSetting}
    </Button>
    <Button type="button" variant="secondary" size="medium" onclick={onCancelCreateCloneSetting}>
      {UI_TEXT.back}
    </Button>
  </div>
</div>
