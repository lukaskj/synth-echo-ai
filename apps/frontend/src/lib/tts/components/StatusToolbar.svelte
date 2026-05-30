<script lang="ts">
	import { UI_TEXT } from '$lib/tts/constants';
	import type { RequestStatus } from '$lib/tts/types';

	type Props = {
		statusLabel: string;
		modelReady: boolean;
		isBusy: boolean;
		status: RequestStatus;
		onLoadModel: () => void | Promise<void>;
		onUnloadModel: () => void | Promise<void>;
	};

	let { statusLabel, modelReady, isBusy, status, onLoadModel, onUnloadModel }: Props = $props();
</script>

<div class="flex flex-wrap items-center justify-end gap-2">
	<div class="rounded-md border border-slate-700 bg-slate-950/60 px-3 py-1 text-sm text-slate-300">
		{UI_TEXT.statusLabel}: {statusLabel}
	</div>
	<div class="rounded-md border px-3 py-1 text-sm {modelReady ? 'border-emerald-500/30 bg-emerald-500/10 text-emerald-200' : 'border-amber-500/30 bg-amber-500/10 text-amber-200'}">
		Model: {modelReady ? UI_TEXT.modelLoaded : UI_TEXT.modelNotLoaded}
	</div>
	<button
		type="button"
		onclick={onLoadModel}
		disabled={isBusy || modelReady}
		class="inline-flex items-center justify-center rounded-md border border-slate-700 bg-slate-950/70 px-4 py-2 text-sm font-semibold text-slate-100 transition hover:border-violet-400/50 hover:bg-slate-900 disabled:cursor-not-allowed disabled:border-slate-800 disabled:bg-slate-900 disabled:text-slate-500"
	>
		{#if status === 'loading-model'}
			{UI_TEXT.loadingShort}
		{:else}
			{UI_TEXT.loadModel}
		{/if}
	</button>
	<button
		type="button"
		onclick={onUnloadModel}
		disabled={isBusy || !modelReady}
		class="inline-flex items-center justify-center rounded-md border border-rose-500/30 bg-rose-500/10 px-4 py-2 text-sm font-semibold text-rose-100 transition hover:bg-rose-500/20 disabled:cursor-not-allowed disabled:border-slate-800 disabled:bg-slate-900 disabled:text-slate-500"
	>
		{#if status === 'unloading-model'}
			{UI_TEXT.unloadingShort}
		{:else}
			{UI_TEXT.unloadModel}
		{/if}
	</button>
</div>
