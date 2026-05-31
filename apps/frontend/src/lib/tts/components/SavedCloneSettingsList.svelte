<script lang="ts">
	import { LANGUAGES, UI_TEXT } from '$lib/tts/constants';
	import type { SavedCloneSetting } from '$lib/tts/types';
	import AudioPreviewCard from './AudioPreviewCard.svelte';
	import Button from './Button.svelte';

	type Props = {
		savedCloneSettings: SavedCloneSetting[];
		isLoadingSelectedCloneSetting: boolean;
		onSelectSavedCloneSetting: (settingId: number) => void | Promise<void>;
		onDeleteSavedCloneSetting: (settingId: number) => void | Promise<void>;
	};

	let {
		savedCloneSettings,
		isLoadingSelectedCloneSetting,
		onSelectSavedCloneSetting,
		onDeleteSavedCloneSetting
	}: Props = $props();

	function getLanguageLabel(value: string) {
		return LANGUAGES.find((option) => option.value === value)?.label ?? value;
	}

	function handleSavedCloneSettingKeydown(event: KeyboardEvent, settingId: number) {
		if (event.key !== 'Enter' && event.key !== ' ') {
			return;
		}

		event.preventDefault();
		onSelectSavedCloneSetting(settingId);
	}

	function handleSavedCloneSettingButtonClick(event: MouseEvent, settingId: number) {
		event.stopPropagation();
		onSelectSavedCloneSetting(settingId);
	}

	function handleSavedCloneSettingDeleteClick(event: MouseEvent, settingId: number) {
		event.stopPropagation();
		onDeleteSavedCloneSetting(settingId);
	}
</script>

<div class="grid gap-3">
	{#each savedCloneSettings as setting (setting.id)}
		<div
			class="cursor-pointer rounded-lg border border-slate-800 bg-slate-900/70 px-2 py-2 transition hover:border-slate-700"
			role="button"
			tabindex="0"
			onclick={() => onSelectSavedCloneSetting(setting.id)}
			onkeydown={(event) => handleSavedCloneSettingKeydown(event, setting.id)}
		>
			<div class="flex items-start justify-between gap-3">
				<div>
					<p class="text-sm font-semibold text-white">{setting.name}</p>
					<p class="mt-2 text-sm text-slate-400">{getLanguageLabel(setting.lang)}</p>
				</div>
			<div class="flex items-center gap-2">
					<Button
						type="button"
						variant="secondary"
						size="small"
						class="rounded-lg bg-slate-950 text-xs uppercase tracking-[0.18em]"
						onclick={(event) => handleSavedCloneSettingButtonClick(event, setting.id)}
					>
						{isLoadingSelectedCloneSetting ? UI_TEXT.loadingSavedCloneSetting : UI_TEXT.useSavedCloneSetting}
					</Button>
					<Button
						type="button"
						variant="danger"
						size="small"
						class="h-9 w-9 rounded-lg px-0"
						onclick={(event) => handleSavedCloneSettingDeleteClick(event, setting.id)}
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
					</Button>
				</div>
			</div>
			<AudioPreviewCard title={UI_TEXT.referenceAudioPreview} src={setting.ref_audio_path} className="mt-2" />
		</div>
	{/each}
</div>
