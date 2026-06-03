<script lang="ts">
  import { Toaster } from '$lib/components/ui/sonner/index.js';
  import './layout.css';
  import favicon from '$lib/assets/favicon.svg';

  let { children } = $props();
</script>

<svelte:head><link rel="icon" href={favicon} /></svelte:head>
{@render children()}
<Toaster position="bottom-left" richColors closeButton />
