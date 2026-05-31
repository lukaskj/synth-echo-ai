<script lang="ts">
	import { MODE_OPTIONS, UI_TEXT } from '$lib/tts/constants';
	import type { CloneView, SavedCloneSetting, TtsMode } from '$lib/tts/types';
	import CloneSettingsPanel from './CloneSettingsPanel.svelte';
	import SelectField from './SelectField.svelte';
	import SynthesisSettingsForm from './SynthesisSettingsForm.svelte';

	type Props = {
		mode: TtsMode;
		cloneView: CloneView;
		cloneSettingName: string;
		cloneRefText: string;
		cloneRefAudioInputKey: number;
		cloneRefAudioName: string;
		cloneRefAudioIsMicrophoneRecording: boolean;
		isRecordingCloneRefAudio: boolean;
		recordingElapsedLabel: string;
		isSpeechRecognitionSupported: boolean;
		microphoneStatusMessage: string;
		microphoneStatusIsError: boolean;
		canRecordCloneRefAudio: boolean;
		synthesizeLang: string;
		synthesizeSpeed: number;
		synthesizeNumStep: number;
		cloneLang: string;
		cloneSpeed: number;
		cloneNumStep: number;
		selectedGender: string;
		selectedAccent: string;
		selectedPitch: string;
		selectedAge: string;
		selectedStyle: string;
		instruct: string;
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
		cloneRefAudioPreviewUrl: string;
	};

	let {
		mode = $bindable(),
		cloneView,
		cloneSettingName = $bindable(),
		cloneRefText = $bindable(),
		cloneRefAudioInputKey,
		cloneRefAudioName,
		cloneRefAudioIsMicrophoneRecording,
		isRecordingCloneRefAudio,
		recordingElapsedLabel,
		isSpeechRecognitionSupported,
		microphoneStatusMessage,
		microphoneStatusIsError,
		canRecordCloneRefAudio,
		synthesizeLang = $bindable(),
		synthesizeSpeed = $bindable(),
		synthesizeNumStep = $bindable(),
		cloneLang = $bindable(),
		cloneSpeed = $bindable(),
		cloneNumStep = $bindable(),
		selectedGender = $bindable(),
		selectedAccent = $bindable(),
		selectedPitch = $bindable(),
		selectedAge = $bindable(),
		selectedStyle = $bindable(),
		instruct,
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
		onToggleCloneRefRecording,
		cloneRefAudioPreviewUrl
	}: Props = $props();
</script>

<aside class="rounded-xl border border-slate-800 bg-slate-900/70 p-6 shadow-2xl shadow-slate-950/40 backdrop-blur">
	<p class="text-sm font-medium uppercase tracking-[0.18em] text-slate-400">
		{UI_TEXT.configurationsEyebrow}
	</p>
	<h2 class="mt-2 text-2xl font-semibold text-white">{mode === 'clone' ? UI_TEXT.cloneSettingsTitle : UI_TEXT.settingsTitle}</h2>

	<div class="mt-2 space-y-5">
		<SelectField id="mode-select" label={UI_TEXT.modeLabel} options={MODE_OPTIONS} bind:value={mode} />

		{#if mode === 'synthesize'}
			<SynthesisSettingsForm
				bind:synthesizeLang
				bind:synthesizeSpeed
				bind:synthesizeNumStep
				bind:selectedGender
				bind:selectedAccent
				bind:selectedPitch
				bind:selectedAge
				bind:selectedStyle
				{instruct}
			/>
		{:else}
			<CloneSettingsPanel
				{cloneView}
				bind:cloneSettingName
				bind:cloneRefText
				{cloneRefAudioInputKey}
				{cloneRefAudioName}
				{cloneRefAudioIsMicrophoneRecording}
				{cloneRefAudioPreviewUrl}
				{isRecordingCloneRefAudio}
				{recordingElapsedLabel}
				{isSpeechRecognitionSupported}
				{microphoneStatusMessage}
				{microphoneStatusIsError}
				{canRecordCloneRefAudio}
				bind:cloneLang
				bind:cloneSpeed
				bind:cloneNumStep
				{canSaveCloneSetting}
				{canUpdateCloneSetting}
				{canDeleteCloneSetting}
				{cloneSettingsErrorMessage}
				{cloneSettingsMessage}
				{isCloneSettingsLoading}
				{isLoadingSelectedCloneSetting}
				{isSavingCloneSetting}
				{isUpdatingCloneSetting}
				{isDeletingCloneSetting}
				{savedCloneSettings}
				{selectedCloneSetting}
				onRefreshCloneSettings={onRefreshCloneSettings}
				onBackToCloneSettingsList={onBackToCloneSettingsList}
				onStartCreateCloneSetting={onStartCreateCloneSetting}
				onCancelCreateCloneSetting={onCancelCreateCloneSetting}
				onSaveCloneSetting={onSaveCloneSetting}
				onUpdateSelectedCloneSetting={onUpdateSelectedCloneSetting}
				onSelectSavedCloneSetting={onSelectSavedCloneSetting}
				onDeleteSelectedCloneSetting={onDeleteSelectedCloneSetting}
				onDeleteSavedCloneSetting={onDeleteSavedCloneSetting}
				onRefAudioChange={onRefAudioChange}
				onToggleCloneRefRecording={onToggleCloneRefRecording}
			/>
		{/if}
	</div>
</aside>
