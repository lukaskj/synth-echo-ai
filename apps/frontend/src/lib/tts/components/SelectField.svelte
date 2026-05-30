<script lang="ts">
	import type { SelectOption } from '$lib/tts/types';

	type Props = {
		id: string;
		label: string;
		options: SelectOption[];
		value: string;
	};

	let { id, label, options, value = $bindable() }: Props = $props();
</script>

<div>
	<label class="text-sm font-medium text-slate-200" for={id}>{label}</label>
	<select
		id={id}
		bind:value
		class="mt-1 w-full rounded-lg border border-slate-700 bg-slate-950/70 px-2 py-2 text-base text-slate-100 outline-none transition focus:border-violet-400 focus:ring-2 focus:ring-violet-400/30"
	>
		{#each options as option}
			<option value={option.value}>{option.label}</option>
		{/each}
	</select>
</div>
