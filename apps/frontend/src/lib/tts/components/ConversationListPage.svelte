<script lang="ts">
  import { goto } from '$app/navigation';
  import { resolve } from '$app/paths';
  import { createConversation, listConversations } from '$lib/tts/api';
  import ConversationSidebar from '$lib/tts/components/ConversationSidebar.svelte';
  import { DEFAULT_FORM_STATE, UI_TEXT } from '$lib/tts/constants';
  import { buildInstruct } from '$lib/tts/helpers';
  import type { Conversation, ConversationLineMutation } from '$lib/tts/types';
  import { toast } from 'svelte-sonner';

  let conversations = $state<Conversation[]>([]);
  let isLoadingConversations = $state(false);
  let hasLoadedConversations = $state(false);
  let isCreatingConversation = $state(false);

  function createInitialConversationLine(): ConversationLineMutation {
    const instruct = buildInstruct([
      DEFAULT_FORM_STATE.selectedGender,
      DEFAULT_FORM_STATE.selectedPitch,
      DEFAULT_FORM_STATE.selectedAccent,
      DEFAULT_FORM_STATE.selectedAge,
      DEFAULT_FORM_STATE.selectedStyle
    ]);

    return {
      position: 0,
      text: '',
      voice_type: 'instruction',
      clone_setting_id: null,
      voice_label: instruct || 'Instruction voice',
      audio_url: '',
      lang: DEFAULT_FORM_STATE.lang,
      speed: DEFAULT_FORM_STATE.speed,
      num_step: DEFAULT_FORM_STATE.numStep,
      instruct,
      selected_gender: DEFAULT_FORM_STATE.selectedGender,
      selected_accent: DEFAULT_FORM_STATE.selectedAccent,
      selected_pitch: DEFAULT_FORM_STATE.selectedPitch,
      selected_age: DEFAULT_FORM_STATE.selectedAge,
      selected_style: DEFAULT_FORM_STATE.selectedStyle
    };
  }

  async function refreshConversations() {
    isLoadingConversations = true;

    try {
      conversations = await listConversations();
      hasLoadedConversations = true;
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : UI_TEXT.conversationLoadFailed;
      toast.error(errorMessage);
    } finally {
      isLoadingConversations = false;
    }
  }

  async function openConversation(conversationId: number) {
    await goto(resolve(`/conversation/${conversationId}`), { noScroll: true });
  }

  async function createNewConversation() {
    if (isCreatingConversation) return;

    isCreatingConversation = true;

    try {
      const response = await createConversation({
        name: UI_TEXT.conversationNewTitle,
        lines: [createInitialConversationLine()]
      });

      conversations = [response.conversation, ...conversations];

      await goto(resolve(`/conversation/${response.conversation.id}`), { noScroll: true });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : UI_TEXT.conversationCreateFailed;
      toast.error(errorMessage);
    } finally {
      isCreatingConversation = false;
    }
  }

  $effect(() => {
    if (!hasLoadedConversations && !isLoadingConversations) {
      void refreshConversations();
    }
  });
</script>

<ConversationSidebar
  {conversations}
  selectedConversationId={null}
  {isLoadingConversations}
  {isCreatingConversation}
  onNewConversation={createNewConversation}
  onOpenConversation={openConversation}
/>
