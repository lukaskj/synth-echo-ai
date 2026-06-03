<script lang="ts">
  import { Button, type ButtonSize, type ButtonVariant } from '$lib/components/ui/button/index.js';
  import RefreshCcwIcon from 'lucide-svelte/icons/refresh-ccw';
  import LoaderIcon from 'lucide-svelte/icons/loader';
  import { UI_TEXT } from '$lib/tts/constants';

  let {
    loading = false,
    isRegenerate = false,
    variant = 'default',
    size = 'sm',
    className = '',
    disabled = false,
    onClick
  }: {
    loading?: boolean;
    isRegenerate?: boolean;
    variant?: ButtonVariant;
    size?: ButtonSize;
    className?: string;
    disabled?: boolean;
    onClick: () => void | Promise<void>;
  } = $props();
</script>

<Button
  {variant}
  {size}
  class={className}
  disabled={disabled || loading}
  onclick={(event) => {
    event.stopPropagation();
    if (onClick) {
      void onClick();
    }
  }}
>
  {#if loading}
    <LoaderIcon class="size-4 animate-spin" />
  {:else}
    <RefreshCcwIcon class="size-4" />
  {/if}
  {isRegenerate ? UI_TEXT.conversationLineRegenerate : UI_TEXT.conversationLineGenerate}
</Button>
