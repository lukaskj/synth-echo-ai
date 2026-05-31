<script lang="ts">
	import * as Card from '$lib/components/ui/card/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import MicIcon from 'lucide-svelte/icons/mic';
	import ChevronRightIcon from 'lucide-svelte/icons/chevron-right';
	import SlidersIcon from 'lucide-svelte/icons/sliders';
	import WandSparklesIcon from 'lucide-svelte/icons/wand-sparkles';
	import SynthesisSettings from './SynthesisSettings.svelte';
	import CloneSettings from './CloneSettings.svelte';
	import VoiceSelectionSheet from './VoiceSelectionSheet.svelte';
	import type {
		TtsMode,
		CloneView,
		SavedCloneSetting,
		RequestStatus
	} from '$lib/tts/types';
	import { LANGUAGES, DEFAULT_FORM_STATE, UI_TEXT } from '$lib/tts/constants';

	let {
		mode,
		cloneView,
		isRecordMode,
		isVoiceSheetOpen = $bindable(false),
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
		mode: TtsMode;
		cloneView: CloneView;
		isRecordMode: boolean;
		isVoiceSheetOpen?: boolean;
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
	const selectedVoiceLangLabel = $derived(
		LANGUAGES.find((l) => l.value === selectedCloneSetting?.lang)?.label ??
			selectedCloneSetting?.lang?.toUpperCase() ??
			''
	);
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

		<Card.Content class="space-y-3">
			<!-- Current voice display -->
			{#if isCloneMode && selectedCloneSetting}
				<div class="bg-muted/40 flex items-center gap-3 rounded-lg px-3 py-2.5">
					<div class="bg-primary/15 flex size-8 shrink-0 items-center justify-center rounded-full">
						<MicIcon class="text-primary size-4" />
					</div>
					<div class="min-w-0 flex-1">
						<p class="text-foreground truncate text-sm font-medium">
							{selectedCloneSetting.name}
						</p>
						<p class="text-muted-foreground text-xs">{selectedVoiceLangLabel}</p>
					</div>
					<Badge variant="secondary" class="shrink-0 text-xs">Active</Badge>
				</div>
			{:else}
				<div class="bg-muted/20 flex items-center gap-3 rounded-lg border border-dashed border-zinc-700 px-3 py-2.5">
					<div class="bg-muted flex size-8 shrink-0 items-center justify-center rounded-full">
						<WandSparklesIcon class="text-muted-foreground size-4" />
					</div>
					<div class="min-w-0 flex-1">
						<p class="text-foreground text-sm font-medium">Synthesize mode</p>
						<p class="text-muted-foreground text-xs">No voice clone selected</p>
					</div>
				</div>
			{/if}

			<Button
				variant="outline"
				class="w-full gap-2"
				onclick={() => (isVoiceSheetOpen = true)}
			>
				{isCloneMode && selectedCloneSetting ? 'Change Voice' : 'Select Voice'}
				<ChevronRightIcon class="size-3.5" />
			</Button>
		</Card.Content>
	</Card.Root>

	<!-- Settings Card -->
	<Card.Root>
		<Card.Header class="pb-3">
			<Card.Title class="flex items-center gap-2 text-sm font-semibold">
				<SlidersIcon class="size-4" />
				{isCloneMode ? 'Clone Settings' : UI_TEXT.settingsTitle}
			</Card.Title>
		</Card.Header>
		<Card.Content>
			{#if isCloneMode}
				<CloneSettings
					bind:cloneLang
					bind:cloneSpeed
					bind:cloneNumStep
				/>
			{:else}
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
			{/if}
		</Card.Content>
	</Card.Root>
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
