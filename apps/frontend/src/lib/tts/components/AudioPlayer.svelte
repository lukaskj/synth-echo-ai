<script lang="ts">
  type Props = {
    src: string;
    preload?: 'auto' | 'metadata' | 'none';
  };

  let { src, preload = 'auto' }: Props = $props();

  function stopEventPropagation(event: Event) {
    event.stopPropagation();
  }
</script>

<audio
  controls
  {preload}
  {src}
  class="m-0 w-full py-3"
  onclick={stopEventPropagation}
  onkeydown={stopEventPropagation}
></audio>
