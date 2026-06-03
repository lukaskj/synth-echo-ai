<script lang="ts">
  import { page } from '$app/state';
  import { Button } from '$lib/components/ui/button/index.js';
  import { Badge } from '$lib/components/ui/badge/index.js';
  import { Separator } from '$lib/components/ui/separator/index.js';
  import CpuIcon from 'lucide-svelte/icons/cpu';
  import MessageSquareMoreIcon from 'lucide-svelte/icons/message-square-more';
  import Mic2Icon from 'lucide-svelte/icons/mic-2';
  import { PAGE_TITLE, REQUEST_STATUS_LABELS, UI_TEXT } from '$lib/tts/constants';
  import type { RequestStatus } from '$lib/tts/types';

  let {
    status,
    modelReady,
    modelDevice,
    isBusy,
    onLoadModel,
    onUnloadModel
  }: {
    status: RequestStatus;
    modelReady: boolean;
    modelDevice: string | null;
    isBusy: boolean;
    onLoadModel: () => void;
    onUnloadModel: () => void;
  } = $props();

  const statusLabel = $derived(REQUEST_STATUS_LABELS[status]);
  const navigationItems = [
    { href: '/', label: 'Voice Dashboard', icon: Mic2Icon },
    { href: '/conversation', label: 'Conversation', icon: MessageSquareMoreIcon }
  ];

  function isActiveNavigationItem(href: string) {
    return href === '/' ? page.url.pathname === '/' : page.url.pathname.startsWith(href);
  }
</script>

<header class="border-border bg-background/80 sticky top-0 z-10 border-b backdrop-blur-sm">
  <div class="mx-auto flex max-w-7xl flex-wrap items-center gap-4 px-4 py-3">
    <div class="flex items-center gap-2">
      <div class="bg-primary/10 text-primary flex size-7 items-center justify-center rounded-md">
        <CpuIcon class="size-4" />
      </div>
      <h1 class="text-foreground text-sm font-semibold tracking-tight">{PAGE_TITLE}</h1>
    </div>

    <Separator orientation="vertical" class="h-5" />

    <nav class="flex flex-1 flex-wrap items-center gap-2">
      {#each navigationItems as item (item.href)}
        {@const Icon = item.icon}
        <Button
          href={item.href}
          variant={isActiveNavigationItem(item.href) ? 'secondary' : 'ghost'}
          size="sm"
          class="gap-1.5"
        >
          <Icon class="size-3.5" />
          {item.label}
        </Button>
      {/each}
    </nav>

    <div class="flex flex-wrap items-center gap-2">
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
        <span class="size-1.5 rounded-full {modelReady ? 'bg-emerald-400' : 'bg-amber-400'}"></span>
        Model: {modelReady ? UI_TEXT.modelLoaded : UI_TEXT.modelNotLoaded}
      </Badge>
      <Badge variant="outline" class="gap-1.5 text-xs">
        <span class="text-muted-foreground">{UI_TEXT.deviceLabel}:</span>
        <span class="text-foreground font-medium">{modelDevice ?? UI_TEXT.modelDeviceUnknown}</span>
      </Badge>
      <Button variant="outline" size="sm" onclick={onLoadModel} disabled={isBusy || modelReady}>
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
</header>
