<script lang="ts">
	import * as Select from '$lib/components/ui/select/index.js';
	import { Label } from '$lib/components/ui/label/index.js';
	import { Slider } from '$lib/components/ui/slider/index.js';
	import { LANGUAGES, UI_TEXT } from '$lib/tts/constants';

	let {
		cloneLang = $bindable('en'),
		cloneSpeed = $bindable(1.0),
		cloneNumStep = $bindable(32)
	}: {
		cloneLang?: string;
		cloneSpeed?: number;
		cloneNumStep?: number;
	} = $props();
</script>

<div class="space-y-4">
	<!-- Language -->
	<div class="space-y-1.5">
		<Label for="clone-lang">{UI_TEXT.language}</Label>
		<Select.Root bind:value={cloneLang}>
			<Select.Trigger id="clone-lang" class="w-full">
				{LANGUAGES.find(o => o.value === cloneLang)?.label ?? 'Select language...'}
			</Select.Trigger>
			<Select.Content>
				{#each LANGUAGES as option}
					<Select.Item value={option.value} label={option.label} />
				{/each}
			</Select.Content>
		</Select.Root>
	</div>

	<!-- Speed -->
	<div class="space-y-2">
		<div class="flex items-center justify-between">
			<Label for="clone-speed">{UI_TEXT.speed}</Label>
			<span class="text-muted-foreground text-xs tabular-nums">{cloneSpeed.toFixed(1)}</span>
		</div>
		<Slider
			id="clone-speed"
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
			<Label for="clone-steps">{UI_TEXT.diffusionSteps}</Label>
			<span class="text-muted-foreground text-xs tabular-nums">{cloneNumStep}</span>
		</div>
		<Slider
			id="clone-steps"
			min={4}
			max={64}
			step={4}
			bind:value={cloneNumStep}
			class="w-full"
		/>
	</div>
</div>
