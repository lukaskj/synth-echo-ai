<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import { Badge } from '$lib/components/ui/badge/index.js';
	import { Separator } from '$lib/components/ui/separator/index.js';
	import CpuIcon from 'lucide-svelte/icons/cpu';
	import { PAGE_TITLE, REQUEST_STATUS_LABELS, UI_TEXT } from '$lib/tts/constants';
	import type { RequestStatus } from '$lib/tts/types';

	let {
		status,
		modelReady,
		isBusy,
		onLoadModel,
		onUnloadModel
	}: {
		status: RequestStatus;
		modelReady: boolean;
		isBusy: boolean;
		onLoadModel: () => void;
		onUnloadModel: () => void;
	} = $props();

	const statusLabel = $derived(REQUEST_STATUS_LABELS[status]);
</script>

<header class="border-border bg-background/80 sticky top-0 z-10 border-b backdrop-blur-sm">
	<div class="mx-auto flex max-w-7xl items-center gap-4 px-4 py-3">
		<!-- App title -->
		<div class="flex items-center gap-2">
			<div class="bg-primary/10 text-primary flex size-7 items-center justify-center rounded-md">
				<CpuIcon class="size-4" />
			</div>
			<h1 class="text-foreground text-sm font-semibold tracking-tight">{PAGE_TITLE}</h1>
		</div>

		<Separator orientation="vertical" class="h-5" />

		<!-- Status badges + buttons -->
		<div class="flex flex-1 items-center justify-between gap-3">
			<div class="flex items-center gap-2">
				<Badge variant="outline" class="gap-1.5 text-xs">
					<span class="text-muted-foreground">Status:</span>
					<span class="text-foreground font-medium">{statusLabel}</span>
				</Badge>
				<Badge
					variant="outline"
					class="gap-1.5 text-xs {modelReady
						? 'border-emerald-500/40 text-emerald-400'
						: 'border-amber-500/40 text-amber-400'}"
				>
					<span
						class="size-1.5 rounded-full {modelReady ? 'bg-emerald-400' : 'bg-amber-400'}"
					></span>
					Model: {modelReady ? UI_TEXT.modelLoaded : UI_TEXT.modelNotLoaded}
				</Badge>
			</div>

			<div class="flex items-center gap-2">
				<Button
					variant="outline"
					size="sm"
					onclick={onLoadModel}
					disabled={isBusy || modelReady}
				>
					{isBusy && status === 'loading-model' ? UI_TEXT.loadingShort : UI_TEXT.loadModel}
				</Button>
				<Button
					variant="outline"
					size="sm"
					onclick={onUnloadModel}
					disabled={isBusy || !modelReady}
					class="text-destructive border-destructive/40 hover:bg-destructive/10 hover:text-destructive"
				>
					{isBusy && status === 'unloading-model' ? UI_TEXT.unloadingShort : UI_TEXT.unloadModel}
				</Button>
			</div>
		</div>
	</div>
</header>
