<script lang="ts">
	import DashboardHeader from './DashboardHeader.svelte';
	import TextInputCard from './TextInputCard.svelte';
	import AudioOutputCard from './AudioOutputCard.svelte';
	import VoicePanel from './VoicePanel.svelte';
	import type {
		TtsMode,
		CloneView,
		LastRequest,
		RequestStatus,
		SavedCloneSetting
	} from '$lib/tts/types';
	import { DEFAULT_FORM_STATE } from '$lib/tts/constants';

	let {
		// Mode
		mode = $bindable('synthesize'),

		// Input texts
		synthesizeInputText = $bindable(''),
		cloneInputText = $bindable(''),

		// Status
		status,
		modelReady,
		isBusy,

		// Audio output
		audioUrl,
		errorMessage,
		responseMessage,
		lastRequest,

		// Submit
		canSubmit,

		// Model controls
		onLoadModel,
		onUnloadModel,
		onSubmit,

		// Synthesis settings
		synthesizeLang = $bindable(DEFAULT_FORM_STATE.lang),
		synthesizeSpeed = $bindable(DEFAULT_FORM_STATE.speed),
		synthesizeNumStep = $bindable(DEFAULT_FORM_STATE.numStep),
		selectedGender = $bindable(DEFAULT_FORM_STATE.selectedGender),
		selectedAccent = $bindable(DEFAULT_FORM_STATE.selectedAccent),
		selectedPitch = $bindable(DEFAULT_FORM_STATE.selectedPitch),
		selectedAge = $bindable(DEFAULT_FORM_STATE.selectedAge),
		selectedStyle = $bindable(DEFAULT_FORM_STATE.selectedStyle),
		instruct,

		// Clone settings
		cloneView,
		isRecordMode,
		isVoiceSheetOpen = $bindable(false),
		cloneLang = $bindable(DEFAULT_FORM_STATE.cloneLang),
		cloneSpeed = $bindable(DEFAULT_FORM_STATE.cloneSpeed),
		cloneNumStep = $bindable(DEFAULT_FORM_STATE.cloneNumStep),
		cloneSettingName = $bindable(''),
		cloneRefText = $bindable(''),
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

		// Voice management state
		savedCloneSettings,
		selectedCloneSettingId,
		selectedCloneSetting,
		isCloneSettingsLoading,
		hasLoadedCloneSettings,
		isLoadingSelectedCloneSetting,
		isSavingCloneSetting,
		isUpdatingCloneSetting,
		isDeletingCloneSetting,
		canSaveCloneSetting,
		canUpdateCloneSetting,
		canDeleteCloneSetting,
		cloneSettingsMessage,
		cloneSettingsErrorMessage,

		// Voice management callbacks
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
		synthesizeInputText?: string;
		cloneInputText?: string;
		status: RequestStatus;
		modelReady: boolean;
		isBusy: boolean;
		audioUrl: string;
		errorMessage: string;
		responseMessage: string;
		lastRequest: LastRequest | null;
		canSubmit: boolean;
		onLoadModel: () => void;
		onUnloadModel: () => void;
		onSubmit: (event: SubmitEvent) => void;
		synthesizeLang?: string;
		synthesizeSpeed?: number;
		synthesizeNumStep?: number;
		selectedGender?: string;
		selectedAccent?: string;
		selectedPitch?: string;
		selectedAge?: string;
		selectedStyle?: string;
		instruct: string;
		cloneView: CloneView;
		isRecordMode: boolean;
		isVoiceSheetOpen?: boolean;
		cloneLang?: string;
		cloneSpeed?: number;
		cloneNumStep?: number;
		cloneSettingName?: string;
		cloneRefText?: string;
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
		savedCloneSettings: SavedCloneSetting[];
		selectedCloneSettingId: number | null;
		selectedCloneSetting: SavedCloneSetting | null;
		isCloneSettingsLoading: boolean;
		hasLoadedCloneSettings: boolean;
		isLoadingSelectedCloneSetting: boolean;
		isSavingCloneSetting: boolean;
		isUpdatingCloneSetting: boolean;
		isDeletingCloneSetting: boolean;
		canSaveCloneSetting: boolean;
		canUpdateCloneSetting: boolean;
		canDeleteCloneSetting: boolean;
		cloneSettingsMessage: string;
		cloneSettingsErrorMessage: string;
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
</script>

<div class="bg-background text-foreground min-h-screen">
	<DashboardHeader
		{status}
		{modelReady}
		{isBusy}
		{onLoadModel}
		{onUnloadModel}
	/>

	<main class="mx-auto max-w-7xl px-4 py-6">
		<form
			class="grid gap-6 lg:grid-cols-[minmax(0,1.5fr)_minmax(300px,1fr)]"
			onsubmit={onSubmit}
		>
			<!-- Left column: Text input + Audio output -->
			<div class="flex flex-col gap-4">
				<TextInputCard
					bind:mode
					bind:synthesizeInputText
					bind:cloneInputText
					{status}
					{canSubmit}
				/>

				<AudioOutputCard
					{audioUrl}
					{errorMessage}
					{responseMessage}
					{lastRequest}
					{status}
				/>
			</div>

			<!-- Right column: Voice panel + Settings -->
			<VoicePanel
				{mode}
				{cloneView}
				{isRecordMode}
				bind:isVoiceSheetOpen
				{savedCloneSettings}
				{selectedCloneSettingId}
				{selectedCloneSetting}
				{isCloneSettingsLoading}
				{hasLoadedCloneSettings}
				{isLoadingSelectedCloneSetting}
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
				bind:synthesizeLang
				bind:synthesizeSpeed
				bind:synthesizeNumStep
				bind:selectedGender
				bind:selectedAccent
				bind:selectedPitch
				bind:selectedAge
				bind:selectedStyle
				{instruct}
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
		</form>
	</main>
</div>
