<script lang="ts">
  type Props = {
    src: string;
    preload?: "auto" | "metadata" | "none";
  };

  let { src, preload = "auto" }: Props = $props();
</script>

<audio controls {preload} {src} class="m-0 py-3 w-full"></audio>
