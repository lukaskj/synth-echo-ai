<script lang="ts">
	import { onDestroy } from 'svelte';

	let {
		mediaStream = null,
		isRecording = false,
		class: className = ''
	}: {
		mediaStream?: MediaStream | null;
		isRecording?: boolean;
		class?: string;
	} = $props();

	let canvas = $state<HTMLCanvasElement | null>(null);
	let animationFrameId: number | null = null;
	let audioContext: AudioContext | null = null;
	let analyser: AnalyserNode | null = null;

	$effect(() => {
		cleanup();

		if (!mediaStream || !isRecording || !canvas) return;

		const ctx = canvas.getContext('2d');
		if (!ctx) return;

		const AudioContextCtor =
			window.AudioContext ??
			(window as Window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
		if (!AudioContextCtor) return;

		audioContext = new AudioContextCtor();
		analyser = audioContext.createAnalyser();
		analyser.fftSize = 128;
		analyser.smoothingTimeConstant = 0.8;

		const source = audioContext.createMediaStreamSource(mediaStream);
		source.connect(analyser);

		const bufferLength = analyser.frequencyBinCount;
		const dataArray = new Uint8Array(bufferLength);
		const barWidth = canvas.width / bufferLength;

		function draw() {
			animationFrameId = requestAnimationFrame(draw);
			if (!analyser || !canvas || !ctx) return;

			const width = canvas.width;
			const height = canvas.height;

			analyser.getByteFrequencyData(dataArray);

			ctx.clearRect(0, 0, width, height);

			let x = 0;
			for (let i = 0; i < bufferLength; i++) {
				const barHeight = ((dataArray[i] ?? 0) / 255) * height;
				const alpha = 0.5 + (barHeight / height) * 0.5;
				ctx.fillStyle = `rgba(147, 197, 253, ${alpha})`;
				ctx.fillRect(x, height - barHeight, barWidth - 1, barHeight);
				x += barWidth;
			}
		}

		draw();

		return () => cleanup();
	});

	function cleanup() {
		if (animationFrameId !== null) {
			cancelAnimationFrame(animationFrameId);
			animationFrameId = null;
		}
		if (audioContext) {
			audioContext.close().catch(() => undefined);
			audioContext = null;
		}
		analyser = null;

		if (canvas) {
			const ctx = canvas.getContext('2d');
			if (ctx) ctx.clearRect(0, 0, canvas.width, canvas.height);
		}
	}

	onDestroy(() => cleanup());
</script>

<div class="relative overflow-hidden rounded-md bg-zinc-800/60 {className}">
	<canvas
		bind:this={canvas}
		width={300}
		height={60}
		class="h-full w-full"
		aria-hidden="true"
	></canvas>
	{#if !isRecording}
		<div
			class="text-muted-foreground absolute inset-0 flex items-center justify-center text-xs"
			aria-hidden="true"
		>
			Start recording to see waveform
		</div>
	{/if}
</div>
