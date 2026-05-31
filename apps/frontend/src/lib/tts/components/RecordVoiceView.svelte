<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Textarea } from '$lib/components/ui/textarea/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Slider } from '$lib/components/ui/slider/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import ArrowLeftIcon from 'lucide-svelte/icons/arrow-left';
	import MicIcon from 'lucide-svelte/icons/mic';
	import StopCircleIcon from 'lucide-svelte/icons/stop-circle';
	import WaveformVisualizer from './WaveformVisualizer.svelte';
	import { LANGUAGES, UI_TEXT, DEFAULT_FORM_STATE } from '$lib/tts/constants';

	let {
		cloneSettingName = $bindable(''),
		cloneRefText = $bindable(''),
		cloneLang = $bindable(DEFAULT_FORM_STATE.cloneLang),
		cloneSpeed = $bindable(DEFAULT_FORM_STATE.cloneSpeed),
		cloneNumStep = $bindable(DEFAULT_FORM_STATE.cloneNumStep),
		cloneRefAudioPreviewUrl = '',
		cloneRefAudioIsMicrophoneRecording = false,
		isRecordingCloneRefAudio = false,
		recordingElapsedLabel = '00:00',
		microphoneStatusMessage = '',
		microphoneStatusIsError = false,
		isSpeechRecognitionSupported = false,
		canRecordCloneRefAudio = false,
		isSavingCloneSetting = false,
		canSaveCloneSetting = false,
		cloneSettingsErrorMessage = '',
		mediaStream = null,
		onSave,
		onBack,
		onToggleRecording
	}: {
		cloneSettingName?: string;
		cloneRefText?: string;
		cloneLang?: string;
		cloneSpeed?: number;
		cloneNumStep?: number;
		cloneRefAudioPreviewUrl?: string;
		cloneRefAudioIsMicrophoneRecording?: boolean;
		isRecordingCloneRefAudio?: boolean;
		recordingElapsedLabel?: string;
		microphoneStatusMessage?: string;
		microphoneStatusIsError?: boolean;
		isSpeechRecognitionSupported?: boolean;
		canRecordCloneRefAudio?: boolean;
		isSavingCloneSetting?: boolean;
		canSaveCloneSetting?: boolean;
		cloneSettingsErrorMessage?: string;
		mediaStream?: MediaStream | null;
		onSave: () => void;
		onBack: () => void;
		onToggleRecording: () => Promise<void>;
	} = $props();
</script>

<div class="flex h-full flex-col">
	<!-- Header -->
	<div class="flex items-center gap-2 pb-4">
		<Button variant="ghost" size="icon-sm" onclick={onBack} aria-label="Back to voice list">
			<ArrowLeftIcon class="size-4" />
		</Button>
		<div>
			<h3 class="text-foreground text-sm font-semibold">Record New Voice</h3>
			<p class="text-muted-foreground text-xs">Record a reference voice sample with your microphone</p>
		</div>
	</div>

	<!-- Error banner -->
	{#if cloneSettingsErrorMessage}
		<div class="mb-4 rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-400">
			{cloneSettingsErrorMessage}
		</div>
	{/if}

	<div class="flex-1 space-y-4 overflow-y-auto pb-4">
		<!-- Name -->
		<div class="space-y-1.5">
			<Label for="rec-voice-name">{UI_TEXT.cloneSettingNameLabel}</Label>
			<Input
				id="rec-voice-name"
				bind:value={cloneSettingName}
				placeholder={UI_TEXT.cloneSettingNamePlaceholder}
			/>
		</div>

		<!-- Language -->
		<div class="space-y-1.5">
			<Label for="rec-voice-lang">{UI_TEXT.language}</Label>
		<Select.Root bind:value={cloneLang}>
			<Select.Trigger id="rec-voice-lang" class="w-full">
				{LANGUAGES.find(o => o.value === cloneLang)?.label ?? 'Select language...'}
				</Select.Trigger>
				<Select.Content>
					{#each LANGUAGES as option}
						<Select.Item value={option.value} label={option.label} />
					{/each}
				</Select.Content>
			</Select.Root>
		</div>

		<!-- Recording section -->
		<div class="space-y-3">
			<Label>{UI_TEXT.recordRefAudioLabel}</Label>

			<!-- Waveform visualizer -->
			<WaveformVisualizer
				{mediaStream}
				isRecording={isRecordingCloneRefAudio}
				class="h-14 w-full"
			/>

			<!-- Recording controls -->
			<div class="flex items-center gap-3">
				<Button
					variant={isRecordingCloneRefAudio ? 'destructive' : 'default'}
					onclick={onToggleRecording}
					disabled={!canRecordCloneRefAudio && !isRecordingCloneRefAudio}
					class="flex-1"
				>
					{#if isRecordingCloneRefAudio}
						<StopCircleIcon class="mr-2 size-4" />
						{UI_TEXT.stopRecording}
					{:else}
						<MicIcon class="mr-2 size-4" />
						{UI_TEXT.startRecording}
					{/if}
				</Button>

				{#if isRecordingCloneRefAudio}
					<Badge variant="destructive" class="shrink-0 animate-pulse">
						● {recordingElapsedLabel}
					</Badge>
				{/if}
			</div>

			<!-- Microphone status -->
			{#if microphoneStatusMessage}
				<p
					class="text-xs {microphoneStatusIsError
						? 'text-destructive'
						: 'text-muted-foreground'}"
				>
					{microphoneStatusMessage}
				</p>
			{/if}
		</div>

		<!-- Audio preview after recording -->
		{#if cloneRefAudioPreviewUrl && cloneRefAudioIsMicrophoneRecording}
			<div class="space-y-1.5">
				<Label>Recording Preview</Label>
				<audio controls src={cloneRefAudioPreviewUrl} class="w-full" preload="auto"></audio>
			</div>
		{/if}

		<!-- Reference text (auto-filled by speech recognition) -->
		<div class="space-y-1.5">
			<div class="flex items-center justify-between">
				<Label for="rec-voice-ref-text">{UI_TEXT.refTextLabel}</Label>
				{#if isSpeechRecognitionSupported}
					<span class="text-muted-foreground text-xs">Auto-transcribed</span>
				{/if}
			</div>
			<Textarea
				id="rec-voice-ref-text"
				bind:value={cloneRefText}
				placeholder={isSpeechRecognitionSupported
					? 'Will be filled automatically as you speak...'
					: UI_TEXT.refTextPlaceholder}
				rows={3}
			/>
		</div>

		<!-- Speed -->
		<div class="space-y-2">
			<div class="flex items-center justify-between">
				<Label for="rec-voice-speed">{UI_TEXT.speed}</Label>
				<span class="text-muted-foreground text-xs tabular-nums">{cloneSpeed.toFixed(1)}</span>
			</div>
		<Slider
			id="rec-voice-speed"
			min={0.5}
			max={2.0}
			step={0.1}
			bind:value={cloneSpeed}
			class="w-full"
		/>
		</div>

		<!-- Diffusion Steps -->
		<div class="space-y-2">
			<div class="flex items-center justify-between">
				<Label for="rec-voice-steps">{UI_TEXT.diffusionSteps}</Label>
				<span class="text-muted-foreground text-xs tabular-nums">{cloneNumStep}</span>
			</div>
		<Slider
			id="rec-voice-steps"
			min={4}
			max={64}
			step={4}
			bind:value={cloneNumStep}
			class="w-full"
		/>
		</div>
	</div>

	<!-- Save button -->
	<div class="border-border border-t pt-4">
		<Button
			class="w-full"
			onclick={onSave}
			disabled={!canSaveCloneSetting}
		>
			{isSavingCloneSetting ? UI_TEXT.savingCloneSetting : UI_TEXT.saveCloneSetting}
		</Button>
	</div>
</div>
