<script lang="ts">
  import { page } from '$app/state';
  import ConversationDetailPage from '$lib/tts/components/ConversationDetailPage.svelte';
</script>

{#key page.params.conversationId}
  <ConversationDetailPage conversationId={page.params.conversationId ?? ''} />
{/key}
