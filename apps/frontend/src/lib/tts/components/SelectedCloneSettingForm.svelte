<script lang="ts">
	import { LANGUAGES, UI_TEXT } from '$lib/tts/constants';
	import type { SavedCloneSetting } from '$lib/tts/types';
	import AudioPreviewCard from './AudioPreviewCard.svelte';
	import Button from './Button.svelte';
	import RangeField from './RangeField.svelte';
	import SelectField from './SelectField.svelte';
	import TextInputField from './TextInputField.svelte';

	type Props = {
		cloneSettingName: string;
		cloneLang: string;
		cloneSpeed: number;
		cloneNumStep: number;
		selectedCloneSetting: SavedCloneSetting;
		canUpdateCloneSetting: boolean;
		canDeleteCloneSetting: boolean;
		isUpdatingCloneSetting: boolean;
		isDeletingCloneSetting: boolean;
		onBackToCloneSettingsList: () => void | Promise<void>;
		onUpdateSelectedCloneSetting: () => void | Promise<void>;
		onDeleteSelectedCloneSetting: () => void | Promise<void>;
	};

	let {
		cloneSettingName = $bindable(),
		cloneLang = $bindable(),
		cloneSpeed = $bindable(),
		cloneNumStep = $bindable(),
		selectedCloneSetting,
		canUpdateCloneSetting,
		canDeleteCloneSetting,
		isUpdatingCloneSetting,
		isDeletingCloneSetting,
		onBackToCloneSettingsList,
		onUpdateSelectedCloneSetting,
		onDeleteSelectedCloneSetting
	}: Props = $props();
</script>

<div class="space-y-4 rounded-lg border border-violet-500/20 bg-slate-900/70 p-4">
	<div class="my-1 flex items-center justify-between gap-0">
		<h4 class="text-base font-semibold text-white">{UI_TEXT.selectedCloneSettingTitle}</h4>
		<Button type="button" variant="secondary" size="small" class="px-4 rounded-lg" onclick={onBackToCloneSettingsList}>
			{UI_TEXT.back}
		</Button>
	</div>

	<div class="grid gap-3 sm:grid-cols-2">
		<TextInputField
			id="selected-setting-name"
			label={UI_TEXT.selectedCloneSettingName}
			placeholder={UI_TEXT.cloneSettingNamePlaceholder}
			inputClassName="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950/70 px-2 py-2 text-base text-slate-100 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-400/30"
			bind:value={cloneSettingName}
		/>
		<div>
			<SelectField id="selected-language-select" label={UI_TEXT.language} options={LANGUAGES} bind:value={cloneLang} />
		</div>
	</div>

	<AudioPreviewCard title={UI_TEXT.refAudioLabel} src={selectedCloneSetting.ref_audio_path} />

	<div class="grid gap-4 px-1">
		<RangeField
			id="selected-clone-speed-range"
			label={UI_TEXT.speed}
			displayValue={`${cloneSpeed.toFixed(1)}x`}
			min={0.5}
			max={2}
			step={0.1}
			bind:value={cloneSpeed}
		/>

		<RangeField
			id="selected-clone-step-range"
			label={UI_TEXT.diffusionSteps}
			displayValue={`${cloneNumStep}`}
			min={8}
			max={64}
			step={8}
			bind:value={cloneNumStep}
		/>
	</div>

	<div class="grid gap-3 sm:grid-cols-2">
		<Button type="button" variant="primary" size="medium" class="w-full" onclick={onUpdateSelectedCloneSetting} disabled={!canUpdateCloneSetting}>
			{isUpdatingCloneSetting ? UI_TEXT.updatingCloneSetting : UI_TEXT.selectedCloneSettingUpdate}
		</Button>
		<Button type="button" variant="danger" size="medium" class="w-full" onclick={onDeleteSelectedCloneSetting} disabled={!canDeleteCloneSetting}>
			{isDeletingCloneSetting ? UI_TEXT.deletingCloneSetting : UI_TEXT.selectedCloneSettingDelete}
		</Button>
	</div>
</div>
