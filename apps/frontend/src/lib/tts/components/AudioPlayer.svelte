<script lang="ts">
  type Props = {
    src: string;
    preload?: 'auto' | 'metadata' | 'none';
    controls?: boolean;
    className?: string;
    ariaLabel?: string;
    audioElement?: HTMLAudioElement | null;
    onEnded?: (() => void) | undefined;
  };

  let {
    src,
    preload = 'auto',
    controls = true,
    className = 'm-0 w-full py-3',
    ariaLabel,
    audioElement = $bindable(null),
    onEnded
  }: Props = $props();

  function stopEventPropagation(event: Event) {
    event.stopPropagation();
  }
</script>

<audio
  bind:this={audioElement}
  {controls}
  {preload}
  {src}
  class={className}
  aria-label={ariaLabel}
  onclick={stopEventPropagation}
  onkeydown={stopEventPropagation}
  onended={onEnded}
></audio>
