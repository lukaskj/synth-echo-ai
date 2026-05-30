<script lang="ts">
  import AudioPlayer from '$lib/tts/components/AudioPlayer.svelte';
	import {
		ACCENT_OPTIONS,
		AGE_OPTIONS,
		GENDER_OPTIONS,
		LANGUAGES,
		MODE_OPTIONS,
		PITCH_OPTIONS,
		STYLE_OPTIONS,
		UI_TEXT
	} from '$lib/tts/constants';
	import type { CloneView, RequestStatus, SavedCloneSetting, TtsMode } from '$lib/tts/types';
	import RangeField from './RangeField.svelte';
	import SelectField from './SelectField.svelte';

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
		status: RequestStatus;
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
		status,
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

	let activeSpeed = $derived(mode === 'clone' ? cloneSpeed : synthesizeSpeed);
	let activeNumStep = $derived(mode === 'clone' ? cloneNumStep : synthesizeNumStep);

	function getLanguageLabel(value: string) {
		return LANGUAGES.find((option) => option.value === value)?.label ?? value;
	}
</script>

<aside class="rounded-xl border border-slate-800 bg-slate-900/70 p-6 shadow-2xl shadow-slate-950/40 backdrop-blur">
	<p class="text-sm font-medium uppercase tracking-[0.18em] text-slate-400">
		{UI_TEXT.configurationsEyebrow}
	</p>
	<h2 class="mt-2 text-2xl font-semibold text-white">{mode === 'clone' ? UI_TEXT.cloneSettingsTitle : UI_TEXT.settingsTitle}</h2>

	<div class="mt-2 space-y-5">
		<SelectField id="mode-select" label={UI_TEXT.modeLabel} options={MODE_OPTIONS} bind:value={mode} />

		{#if mode === 'synthesize'}
			<SelectField id="language-select" label={UI_TEXT.language} options={LANGUAGES} bind:value={synthesizeLang} />

			<div class="grid gap-4 sm:grid-cols-2">
				<SelectField id="gender-select" label={UI_TEXT.gender} options={GENDER_OPTIONS} bind:value={selectedGender} />
				<SelectField id="accent-select" label={UI_TEXT.accent} options={ACCENT_OPTIONS} bind:value={selectedAccent} />
				<SelectField id="pitch-select" label={UI_TEXT.pitch} options={PITCH_OPTIONS} bind:value={selectedPitch} />
				<SelectField id="age-select" label={UI_TEXT.age} options={AGE_OPTIONS} bind:value={selectedAge} />
				<div class="sm:col-span-2">
					<SelectField id="style-select" label={UI_TEXT.style} options={STYLE_OPTIONS} bind:value={selectedStyle} />
				</div>
			</div>

			<div class="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
				<p class="text-xs uppercase tracking-[0.18em] text-slate-500">{UI_TEXT.currentInstruct}</p>
				<p class="mt-3 text-base leading-7 text-slate-100">
					{#if instruct}
						{instruct}
					{:else}
						{UI_TEXT.noInstruction}
					{/if}
				</p>
			</div>

			<div class="grid gap-4 px-1">
				<RangeField
					id="speed-range"
					label={UI_TEXT.speed}
					displayValue={`${activeSpeed.toFixed(1)}x`}
					min={0.5}
					max={2}
					step={0.1}
					bind:value={synthesizeSpeed}
				/>

				<RangeField
					id="step-range"
					label={UI_TEXT.diffusionSteps}
					displayValue={`${activeNumStep}`}
					min={8}
					max={64}
					step={8}
					bind:value={synthesizeNumStep}
				/>
			</div>
		{:else}
			<div class="space-y-4 rounded-lg border border-slate-800 bg-slate-950/50 p-4">
				<div class="flex flex-wrap items-start justify-between gap-3">
					<div>
						<h3 class="text-base font-semibold text-white">{UI_TEXT.savedCloneSettingsTitle}</h3>
						<p class="mt-1 text-sm leading-6 text-slate-400">{UI_TEXT.savedCloneSettingsDescription}</p>
					</div>
					<div class="flex flex-wrap gap-2">
						{#if cloneView !== 'create'}
							<button
								type="button"
								onclick={onRefreshCloneSettings}
								disabled={isCloneSettingsLoading}
								class="inline-flex items-center justify-center rounded-md border border-slate-700 bg-slate-900 px-3 py-2 text-sm font-semibold text-slate-100 transition hover:border-violet-400/50 hover:bg-slate-950 disabled:cursor-not-allowed disabled:border-slate-800 disabled:text-slate-500"
							>
								{isCloneSettingsLoading ? UI_TEXT.refreshingCloneSettings : UI_TEXT.refreshCloneSettings}
							</button>
						{/if}
						{#if cloneView !== 'create'}
							<button
								type="button"
								onclick={onStartCreateCloneSetting}
								class="inline-flex items-center justify-center rounded-md border border-emerald-500/30 bg-emerald-500/10 px-3 py-2 text-sm font-semibold text-emerald-100 transition hover:bg-emerald-500/20"
							>
								{UI_TEXT.createCloneSetting}
							</button>
						{/if}
					</div>
				</div>

				{#if cloneSettingsErrorMessage}
					<div class="rounded-lg border border-rose-500/30 bg-rose-500/10 p-4 text-sm leading-6 text-rose-100" role="alert">
						{cloneSettingsErrorMessage}
					</div>
				{:else if cloneSettingsMessage}
					<div class="rounded-lg border border-emerald-500/30 bg-emerald-500/10 p-4 text-sm leading-6 text-emerald-100">
						{cloneSettingsMessage}
					</div>
				{/if}

				{#if cloneView === 'create'}
					<div class="space-y-4 rounded-lg border border-emerald-500/20 bg-slate-900/70 p-4">
						<div>
							<h4 class="text-base font-semibold text-white">{UI_TEXT.createCloneSettingTitle}</h4>
							<p class="mt-1 text-sm leading-6 text-slate-400">{UI_TEXT.createCloneSettingDescription}</p>
						</div>

						<div>
							<label class="block text-sm font-medium text-slate-200" for="clone-setting-name">{UI_TEXT.cloneSettingNameLabel}</label>
							<input
								id="clone-setting-name"
								bind:value={cloneSettingName}
								placeholder={UI_TEXT.cloneSettingNamePlaceholder}
								class="mt-3 w-full rounded-lg border border-slate-700 bg-slate-950/70 px-4 py-3 text-base text-slate-100 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-400/30"
							/>
						</div>

						<SelectField id="language-select" label={UI_TEXT.language} options={LANGUAGES} bind:value={cloneLang} />

						<div class="grid gap-4 px-1">
							<RangeField
								id="clone-speed-range"
								label={UI_TEXT.speed}
								displayValue={`${activeSpeed.toFixed(1)}x`}
								min={0.5}
								max={2}
								step={0.1}
								bind:value={cloneSpeed}
							/>

							<RangeField
								id="clone-step-range"
								label={UI_TEXT.diffusionSteps}
								displayValue={`${activeNumStep}`}
								min={8}
								max={64}
								step={8}
								bind:value={cloneNumStep}
							/>
						</div>

						<div class="space-y-4">
							<div>
								<label class="block text-sm font-medium text-slate-200" for="ref-audio">{UI_TEXT.refAudioLabel}</label>
								<div class="mt-3 flex flex-wrap items-center gap-3">
									<button
										type="button"
										onclick={onToggleCloneRefRecording}
										disabled={!canRecordCloneRefAudio}
										class="inline-flex items-center justify-center rounded-md border px-3 py-2 text-sm font-semibold transition disabled:cursor-not-allowed disabled:border-slate-800 disabled:bg-slate-900 disabled:text-slate-500 {isRecordingCloneRefAudio
											? 'border-rose-500/40 bg-rose-500/15 text-rose-100 hover:bg-rose-500/20'
											: 'border-violet-500/30 bg-violet-500/10 text-violet-100 hover:bg-violet-500/20'}"
									>
										{isRecordingCloneRefAudio ? UI_TEXT.stopRecording : UI_TEXT.startRecording}
									</button>
									{#if isRecordingCloneRefAudio}
										<div class="inline-flex items-center gap-2 rounded-full border border-rose-500/30 bg-rose-500/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.18em] text-rose-100">
											<span class="h-2.5 w-2.5 rounded-full bg-rose-400"></span>
											<span>{UI_TEXT.recordingInProgress}</span>
											<span aria-label={UI_TEXT.recordingTimerLabel}>{recordingElapsedLabel}</span>
										</div>
									{/if}
								</div>
								{#if microphoneStatusMessage}
									<p class={`mt-3 text-sm leading-6 ${microphoneStatusIsError ? 'text-amber-200' : 'text-slate-400'}`}>
										{microphoneStatusMessage}
									</p>
								{/if}
								{#if !isSpeechRecognitionSupported}
									<p class="mt-3 text-sm leading-6 text-slate-400">{UI_TEXT.speechRecognitionNotSupported}</p>
								{/if}
								<div class="mt-3 rounded-lg border border-dashed border-slate-700 bg-slate-950/60 px-4 py-4 text-sm text-slate-300">
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
										<div class="mt-3 flex flex-wrap items-center gap-2 text-xs uppercase tracking-[0.18em] text-slate-500">
											<p>{cloneRefAudioName}</p>
											{#if cloneRefAudioIsMicrophoneRecording}
												<span class="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-2 py-1 text-[10px] font-semibold text-emerald-100">
													{UI_TEXT.microphoneRecordingBadge}
												</span>
											{/if}
										</div>
									{/if}
									{#if cloneRefAudioPreviewUrl}
										<div class="mt-4 rounded-lg border border-slate-800 bg-slate-900/80 p-3">
											<p class="text-xs uppercase tracking-[0.18em] text-slate-500">{UI_TEXT.referenceAudioPreview}</p>
                       <AudioPlayer src={cloneRefAudioPreviewUrl} preload="metadata" />
										</div>
									{/if}
								</div>
							</div>

							<div>
								<label class="block text-sm font-medium text-slate-200" for="ref-text">{UI_TEXT.refTextLabel}</label>
								<textarea
									id="ref-text"
									bind:value={cloneRefText}
									rows="4"
									placeholder={UI_TEXT.refTextPlaceholder}
									class="mt-3 w-full rounded-lg border border-slate-700 bg-slate-950/70 px-4 py-3 text-base leading-7 text-slate-100 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-400/30"
								></textarea>
							</div>
						</div>

						<div class="flex flex-wrap gap-3">
							<button
								type="button"
								onclick={onSaveCloneSetting}
								disabled={!canSaveCloneSetting}
								class="inline-flex flex-1 items-center justify-center rounded-lg border border-emerald-500/30 bg-emerald-500/10 px-4 py-1 text-base font-semibold text-emerald-100 transition hover:bg-emerald-500/20 disabled:cursor-not-allowed disabled:border-slate-800 disabled:bg-slate-900 disabled:text-slate-500"
							>
								{isSavingCloneSetting ? UI_TEXT.savingCloneSetting : UI_TEXT.saveCloneSetting}
							</button>
							<button
								type="button"
								onclick={onCancelCreateCloneSetting}
								class="inline-flex items-center justify-center rounded-lg border border-slate-700 bg-slate-900 px-4 py-1 text-base font-semibold text-slate-100 transition hover:border-slate-600"
							>
								{UI_TEXT.back}
							</button>
						</div>
					</div>
				{:else if cloneView === 'selected' && selectedCloneSetting}
					<div class="space-y-4 rounded-lg border border-violet-500/20 bg-slate-900/70 p-4">
						<div class="flex items-center justify-between gap-0 my-1">
							<h4 class="text-base font-semibold text-white">{UI_TEXT.selectedCloneSettingTitle}</h4>
							<button
								type="button"
								onclick={onBackToCloneSettingsList}
								class="inline-flex items-center justify-center rounded-lg border border-slate-700 bg-slate-900 px-4 py-2 text-sm font-semibold text-slate-100 transition hover:border-slate-600"
							>
								{UI_TEXT.back}
							</button>
						</div>

					<div class="grid gap-3 sm:grid-cols-2">
						<div>
							<label class="text-sm font-medium text-slate-200" for="selected-setting-name">{UI_TEXT.selectedCloneSettingName}</label>
							<input
								id="selected-setting-name"
								bind:value={cloneSettingName}
								placeholder={UI_TEXT.cloneSettingNamePlaceholder}
								class="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950/70 px-2 py-2 text-base text-slate-100 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-400/30"
							/>
						</div>
						<div>
							<SelectField id="selected-language-select" label={UI_TEXT.language} options={LANGUAGES} bind:value={cloneLang} />
						</div>
					</div>

					<div class="rounded-lg border border-slate-800 bg-slate-950/60 p-3">
						<div class="m-0 grid gap-4">
							<!-- <div>
								<label class="block text-sm font-medium text-slate-200" for="selected-ref-text">{UI_TEXT.refTextLabel}</label>
								<textarea
									id="selected-ref-text"
									value={cloneRefText}
									rows="4"
									readonly
									class="mt-3 w-full rounded-lg border border-slate-800 bg-slate-950/80 px-4 py-3 text-base leading-7 text-slate-400 outline-none"
								></textarea>
							</div> -->
							<div>
								<p class="text-sm font-medium text-slate-200">{UI_TEXT.refAudioLabel}</p>
                <AudioPlayer src={selectedCloneSetting.ref_audio_path} preload="none" />
							</div>
						</div>
					</div>

						<div class="grid gap-4 px-1">
							<RangeField
								id="selected-clone-speed-range"
								label={UI_TEXT.speed}
								displayValue={`${activeSpeed.toFixed(1)}x`}
								min={0.5}
								max={2}
								step={0.1}
								bind:value={cloneSpeed}
							/>

							<RangeField
								id="selected-clone-step-range"
								label={UI_TEXT.diffusionSteps}
								displayValue={`${activeNumStep}`}
								min={8}
								max={64}
								step={8}
								bind:value={cloneNumStep}
							/>
						</div>

						<div class="grid gap-3 sm:grid-cols-2">
							<button
								type="button"
								onclick={onUpdateSelectedCloneSetting}
								disabled={!canUpdateCloneSetting}
								class="inline-flex w-full items-center justify-center rounded-lg border border-amber-500/30 bg-amber-500/10 px-4 py-1 text-base font-semibold text-amber-100 transition hover:bg-amber-500/20 disabled:cursor-not-allowed disabled:border-slate-800 disabled:bg-slate-900 disabled:text-slate-500"
							>
								{isUpdatingCloneSetting ? UI_TEXT.updatingCloneSetting : UI_TEXT.selectedCloneSettingUpdate}
							</button>
							<button
								type="button"
								onclick={onDeleteSelectedCloneSetting}
								disabled={!canDeleteCloneSetting}
								class="inline-flex w-full items-center justify-center rounded-lg border border-rose-500/30 bg-rose-500/10 px-4 py-1 text-base font-semibold text-rose-100 transition hover:bg-rose-500/20 disabled:cursor-not-allowed disabled:border-slate-800 disabled:bg-slate-900 disabled:text-slate-500"
							>
								{isDeletingCloneSetting ? UI_TEXT.deletingCloneSetting : UI_TEXT.selectedCloneSettingDelete}
							</button>
						</div>
					</div>
				{:else if savedCloneSettings.length > 0}
					<div class="grid gap-3">
						{#each savedCloneSettings as setting (setting.id)}
							<div class="rounded-lg border border-slate-800 bg-slate-900/70 px-2 py-2 transition hover:border-slate-700">
								<div class="flex items-start justify-between gap-3">
									<div>
										<p class="text-sm font-semibold text-white">{setting.name}</p>
										<p class="mt-2 text-sm text-slate-400">{getLanguageLabel(setting.lang)}</p>
									</div>
									<div class="flex items-center gap-2">
										<button
											type="button"
											onclick={() => onSelectSavedCloneSetting(setting.id)}
											class="inline-flex items-center justify-center rounded-lg border border-slate-700 bg-slate-950 px-3 py-2 text-xs font-semibold uppercase tracking-[0.18em] text-slate-200 transition hover:border-slate-600"
										>
											{isLoadingSelectedCloneSetting ? UI_TEXT.loadingSavedCloneSetting : UI_TEXT.useSavedCloneSetting}
										</button>
										<button
											type="button"
											onclick={() => onDeleteSavedCloneSetting(setting.id)}
											class="inline-flex h-9 w-9 items-center justify-center rounded-lg border border-rose-500/30 bg-rose-500/10 text-rose-100 transition hover:bg-rose-500/20"
											aria-label={`${UI_TEXT.selectedCloneSettingDelete}: ${setting.name}`}
											title={UI_TEXT.selectedCloneSettingDelete}
										>
											<svg viewBox="0 0 20 20" fill="currentColor" class="h-4 w-4" aria-hidden="true">
												<path
													fill-rule="evenodd"
													d="M8.5 2a1 1 0 00-.894.553L7.382 3H4a1 1 0 100 2h.293l.853 10.236A2 2 0 007.14 17h5.72a2 2 0 001.994-1.764L15.707 5H16a1 1 0 100-2h-3.382l-.224-.447A1 1 0 0011.5 2h-3zM8 7a1 1 0 012 0v6a1 1 0 11-2 0V7zm4-1a1 1 0 00-1 1v6a1 1 0 102 0V7a1 1 0 00-1-1z"
													clip-rule="evenodd"
												/>
											</svg>
										</button>
									</div>
								</div>
								<div class="mt-2">
									<p class="text-xs uppercase tracking-[0.18em] text-slate-500">{UI_TEXT.referenceAudioPreview}</p>
                  <AudioPlayer src={setting.ref_audio_path} preload="none" />
								</div>
							</div>
						{/each}
					</div>
				{:else if isCloneSettingsLoading}
					<div class="rounded-lg border border-dashed border-slate-700 bg-slate-900/50 p-4 text-sm leading-6 text-slate-400">
						{UI_TEXT.refreshingCloneSettings}
					</div>
				{:else}
					<div class="rounded-lg border border-dashed border-slate-700 bg-slate-900/50 p-4 text-sm leading-6 text-slate-400">
						{UI_TEXT.savedCloneSettingsEmpty}
					</div>
				{/if}
			</div>
		{/if}
	</div>
</aside>
