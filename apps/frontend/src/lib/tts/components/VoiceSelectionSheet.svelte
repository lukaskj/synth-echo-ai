<script lang="ts">
	import * as Sheet from '$lib/components/ui/sheet/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { ScrollArea } from '$lib/components/ui/scroll-area/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import VoiceListItem from './VoiceListItem.svelte';
	import AddVoiceView from './AddVoiceView.svelte';
	import RecordVoiceView from './RecordVoiceView.svelte';
	import EditVoiceView from './EditVoiceView.svelte';
	import MicIcon from 'lucide-svelte/icons/mic';
	import UploadIcon from 'lucide-svelte/icons/upload';
	import RefreshCwIcon from 'lucide-svelte/icons/refresh-cw';
	import SearchIcon from 'lucide-svelte/icons/search';
	import XIcon from 'lucide-svelte/icons/x';
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

	let searchQuery = $state('');

	// Reset search when the sheet closes so it's clean on next open
	$effect(() => {
		if (!open) {
			searchQuery = '';
		}
	});

	const filteredVoices = $derived(
		searchQuery.trim()
			? savedCloneSettings.filter(
					(v) =>
						v.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
						v.lang.toLowerCase().includes(searchQuery.toLowerCase())
				)
			: savedCloneSettings
	);

	// Determine current sheet view from cloneView + isRecordMode
	const sheetView: 'list' | 'add-upload' | 'add-record' | 'edit' = $derived(
		cloneView === 'create' ? (isRecordMode ? 'add-record' : 'add-upload') :
		cloneView === 'selected' ? 'edit' :
		'list'
	);
</script>

<Sheet.Root bind:open>
	<Sheet.Content side="right" class="flex w-full flex-col sm:max-w-md">
		<Sheet.Header class="pb-2">
			<Sheet.Title>
				{#if sheetView === 'list'}
					Voice Library
				{:else if sheetView === 'add-upload'}
					Upload Voice
				{:else if sheetView === 'add-record'}
					Record Voice
				{:else}
					Edit Voice
				{/if}
			</Sheet.Title>
		</Sheet.Header>

		<div class="flex flex-1 flex-col overflow-hidden px-1">
			{#if sheetView === 'list'}
				<!-- Search + action buttons -->
				<div class="space-y-3 pb-3">
					<div class="relative">
						<SearchIcon
							class="text-muted-foreground absolute top-1/2 left-2.5 size-3.5 -translate-y-1/2"
						/>
						<Input
							bind:value={searchQuery}
							placeholder="Search voices..."
							class="pl-8 {searchQuery ? 'pr-8' : ''}"
						/>
						{#if searchQuery}
							<button
								type="button"
								class="text-muted-foreground hover:text-foreground absolute top-1/2 right-2.5 -translate-y-1/2"
								onclick={() => { searchQuery = ''; }}
								aria-label="Clear search"
							>
								<XIcon class="size-3.5" />
							</button>
						{/if}
					</div>
					<div class="flex gap-2">
						<Button
							variant="outline"
							class="flex-1 gap-1.5"
							onclick={onStartAddUpload}
							size="sm"
						>
							<UploadIcon class="size-3.5" />
							Upload Voice
						</Button>
						<Button
							variant="outline"
							class="flex-1 gap-1.5"
							onclick={onStartAddRecord}
							size="sm"
						>
							<MicIcon class="size-3.5" />
							Record Voice
						</Button>
						<Button
							variant="ghost"
							size="icon-sm"
							onclick={onRefreshVoices}
							disabled={isCloneSettingsLoading}
							aria-label="Refresh voice list"
						>
							<RefreshCwIcon class="size-3.5 {isCloneSettingsLoading ? 'animate-spin' : ''}" />
						</Button>
					</div>
				</div>

				<Separator class="mb-3" />

				<!-- Messages -->
				{#if cloneSettingsErrorMessage}
					<div class="mb-3 rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2 text-sm text-red-400">
						{cloneSettingsErrorMessage}
					</div>
				{/if}
				{#if cloneSettingsMessage}
					<div class="mb-3 rounded-md border border-emerald-500/30 bg-emerald-500/10 px-3 py-2 text-sm text-emerald-400">
						{cloneSettingsMessage}
					</div>
				{/if}

				<!-- Voice list -->
				<ScrollArea class="flex-1">
					{#if isCloneSettingsLoading && !hasLoadedCloneSettings}
						<div class="text-muted-foreground py-8 text-center text-sm">Loading voices...</div>
					{:else if filteredVoices.length === 0}
						<div class="text-muted-foreground py-8 text-center text-sm">
							{searchQuery ? 'No voices match your search.' : 'No voices saved yet. Add your first voice above.'}
						</div>
					{:else}
						<div class="space-y-2 pr-3">
							{#each filteredVoices as voice (voice.id)}
								<VoiceListItem
									{voice}
									isSelected={voice.id === selectedCloneSettingId}
									onSelect={onSelectVoice}
									onEdit={onStartEditVoice}
									onDelete={onDeleteVoice}
								/>
							{/each}
						</div>
					{/if}
				</ScrollArea>

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
