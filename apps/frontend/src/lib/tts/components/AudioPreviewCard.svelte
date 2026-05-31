<script lang="ts">
  import AudioPlayer from '$lib/tts/components/AudioPlayer.svelte';

  type Props = {
    title: string;
    src: string;
    preload?: 'auto' | 'metadata' | 'none';
    className?: string;
  };

  let { title, src, preload = 'none', className = '' }: Props = $props();
</script>

<div class={`rounded-lg border border-slate-800 bg-slate-900/80 p-3 ${className}`.trim()}>
  <p class="text-xs uppercase tracking-[0.18em] text-slate-500">{title}</p>
  <AudioPlayer {src} {preload} />
</div>
