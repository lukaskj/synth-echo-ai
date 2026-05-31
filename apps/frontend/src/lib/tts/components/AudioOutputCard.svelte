<script lang="ts">
	import * as Card from '$lib/components/ui/card/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import MusicIcon from 'lucide-svelte/icons/music';
	import AlertCircleIcon from 'lucide-svelte/icons/alert-circle';
	import CheckCircleIcon from 'lucide-svelte/icons/check-circle';
	import type { LastRequest, RequestStatus } from '$lib/tts/types';
	import { LANGUAGES, UI_TEXT } from '$lib/tts/constants';

	let {
		audioUrl = '',
		errorMessage = '',
		responseMessage = '',
		lastRequest = null,
		status
	}: {
		audioUrl?: string;
		errorMessage?: string;
		responseMessage?: string;
		lastRequest?: LastRequest | null;
		status: RequestStatus;
	} = $props();

	const isGenerating = $derived(status === 'synthesizing' || status === 'cloning');
</script>

<Card.Root>
	<Card.Header class="pb-3">
		<Card.Title class="flex items-center gap-2 text-sm font-semibold">
			<MusicIcon class="size-4" />
			{UI_TEXT.generatedAudioTitle}
		</Card.Title>
	</Card.Header>

	<Card.Content class="space-y-3">
		{#if isGenerating}
			<!-- Generating state -->
			<div class="flex items-center gap-2 py-3">
				<Badge variant="secondary" class="animate-pulse gap-1.5">
					<span class="bg-primary size-1.5 animate-pulse rounded-full"></span>
					{UI_TEXT.generatingAudio}
				</Badge>
			</div>

		{:else if errorMessage}
			<!-- Error state -->
			<div class="flex items-start gap-2 rounded-md border border-red-500/30 bg-red-500/10 px-3 py-2">
				<AlertCircleIcon class="mt-0.5 size-4 shrink-0 text-red-400" />
				<p class="text-sm text-red-400">{errorMessage}</p>
			</div>

		{:else if audioUrl}
			<!-- Success with audio -->
			{#if responseMessage}
				<div class="flex items-center gap-2">
					<CheckCircleIcon class="size-4 shrink-0 text-emerald-400" />
					<p class="text-sm text-emerald-400">{responseMessage}</p>
				</div>
			{/if}

			<audio
				controls
				src={audioUrl}
				class="w-full"
				preload="auto"
				aria-label="Generated audio"
				onclick={(e) => e.stopPropagation()}
				onkeydown={(e) => e.stopPropagation()}
			></audio>

			{#if lastRequest}
				<Separator />
				<div class="grid grid-cols-2 gap-x-4 gap-y-1.5 text-xs">
					<div class="text-muted-foreground">Mode</div>
					<div class="text-foreground capitalize">{lastRequest.mode}</div>

					<div class="text-muted-foreground">{UI_TEXT.resultLanguage}</div>
					<div class="text-foreground">{lastRequest.langLabel}</div>

					<div class="text-muted-foreground">{UI_TEXT.resultSpeed}</div>
					<div class="text-foreground tabular-nums">{lastRequest.speed.toFixed(1)}</div>

					<div class="text-muted-foreground">{UI_TEXT.resultSteps}</div>
					<div class="text-foreground tabular-nums">{lastRequest.numStep}</div>

					{#if lastRequest.refAudioName}
						<div class="text-muted-foreground">{UI_TEXT.resultReferenceAudio}</div>
						<div class="text-foreground truncate">{lastRequest.refAudioName}</div>
					{/if}

					{#if lastRequest.instruct}
						<div class="text-muted-foreground col-span-2">Instruct</div>
						<div class="text-foreground col-span-2 italic">{lastRequest.instruct}</div>
					{/if}
				</div>
			{/if}

		{:else if responseMessage}
			<!-- Response message only (e.g. model loaded) -->
			<div class="flex items-center gap-2">
				<CheckCircleIcon class="size-4 shrink-0 text-emerald-400" />
				<p class="text-sm text-emerald-400">{responseMessage}</p>
			</div>

		{:else}
			<!-- Idle state -->
			<p class="text-muted-foreground py-4 text-center text-sm">{UI_TEXT.noAudioYet}</p>
		{/if}
	</Card.Content>
</Card.Root>
