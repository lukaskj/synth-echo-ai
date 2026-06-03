<script lang="ts">
  import * as Card from '$lib/components/ui/card/index.js';
  import { Button } from '$lib/components/ui/button/index.js';
  import { Badge } from '$lib/components/ui/badge/index.js';
  import type { Conversation } from '$lib/tts/types';
  import { UI_TEXT } from '$lib/tts/constants';
  import PlusIcon from 'lucide-svelte/icons/plus';
  import LoaderIcon from 'lucide-svelte/icons/loader';

  let {
    conversations,
    selectedConversationId,
    isLoadingConversations,
    onNewConversation,
    onOpenConversation
  }: {
    conversations: Conversation[];
    selectedConversationId: number | null;
    isLoadingConversations: boolean;
    onNewConversation: () => void | Promise<void>;
    onOpenConversation: (conversationId: number) => void | Promise<void>;
  } = $props();
</script>

<Card.Root class="h-fit">
  <Card.Header class="">
    <div class="flex items-center justify-between gap-3">
      <Card.Title class="text-sm font-semibold">{UI_TEXT.conversationSectionTitle}</Card.Title>
      <Button size="sm" class="gap-1.5" onclick={onNewConversation}>
        <PlusIcon class="size-3.5" />
        {UI_TEXT.conversationNewButton}
      </Button>
    </div>
  </Card.Header>
  <Card.Content class="space-y-3">
    {#if isLoadingConversations}
      <div class="text-muted-foreground flex items-center gap-2 text-sm">
        <LoaderIcon class="size-4 animate-spin" />
        {UI_TEXT.conversationSectionLoading}
      </div>
    {:else if conversations.length === 0}
      <p class="text-muted-foreground text-sm">{UI_TEXT.conversationSectionEmpty}</p>
    {:else}
      <div class="space-y-2">
        {#each conversations as conversation (conversation.id)}          
          <Button
            variant="outline"
            class={`h-auto w-full justify-start rounded-xl px-3 py-3 text-left transition-colors cursor-pointer ${selectedConversationId === conversation.id ? 'bg-primary/5 hover:bg-primary/10' : 'bg-muted/20 hover:bg-muted/35'}`}
            onclick={() => onOpenConversation(conversation.id)}
          >
            <div class="flex flex-row justify-between w-full">
              <p class="truncate text-sm font-medium">{conversation.name}</p>
              <Badge variant="outline" title={conversation.lines.length === 1 ? '1 line' : `${conversation.lines.length} lines`}>
                {conversation.lines.length === 1 ? '1 line' : `${conversation.lines.length} lines`}
              </Badge>
            </div>
          </Button>
        {/each}
      </div>
    {/if}
  </Card.Content>
</Card.Root>
