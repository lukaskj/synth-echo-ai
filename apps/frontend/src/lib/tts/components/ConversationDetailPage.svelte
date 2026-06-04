<script lang="ts">
  import { goto } from '$app/navigation';
  import { resolve } from '$app/paths';
  import { Button } from '$lib/components/ui/button/index.js';
  import {
    cloneAudio,
    deleteCloneSetting,
    deleteConversation,
    getConversation,
    getSavedCloneSetting,
    listSavedCloneSettings,
    loadModel,
    saveCloneSetting,
    synthesizeAudio,
    unloadModel,
    updateCloneSetting,
    updateConversation
  } from '$lib/tts/api';
  import {
    buildTranscriptFromEvent,
    convertRecordedBlobToWav,
    formatElapsedTime,
    getPreferredRecordingMimeType,
    getRecordedFileExtension,
    getSpeechRecognitionConstructor,
    getSpeechRecognitionLocale
  } from '$lib/tts/audio';
  import ConversationEditor from '$lib/tts/components/ConversationEditor.svelte';
  import ConversationLineConfig from '$lib/tts/components/ConversationLineConfig.svelte';
  import VoiceSelectionSheet from '$lib/tts/components/VoiceSelectionSheet.svelte';
  import { DEFAULT_FORM_STATE, UI_TEXT } from '$lib/tts/constants';
  import { dashboardHeaderState } from '$lib/tts/dashboard-header-state.svelte';
  import { buildInstruct, revokeObjectUrl } from '$lib/tts/helpers';
  import type {
    CloneView,
    Conversation,
    ConversationLineMutation,
    ConversationVoiceType,
    RequestStatus,
    SavedCloneSetting,
    SpeechRecognitionErrorEvent,
    SpeechRecognitionEvent,
    SpeechRecognitionInstance
  } from '$lib/tts/types';
  import ArrowLeftIcon from 'lucide-svelte/icons/arrow-left';
  import LoaderIcon from 'lucide-svelte/icons/loader';
  import { onDestroy, tick } from 'svelte';
  import { toast } from 'svelte-sonner';

  let { conversationId }: { conversationId: string } = $props();

  let status = $state<RequestStatus>('idle');
  let modelReady = $state(false);
  let modelDevice = $state<string | null>(null);
  let cloneSettingsMessage = $state('');
  let cloneSettingsErrorMessage = $state('');

  let loadedConversation = $state<Conversation | null>(null);
  let savedCloneSettings = $state<SavedCloneSetting[]>([]);
  let isLoadingConversation = $state(false);
  let isLoadingVoices = $state(false);
  let hasAttemptedConversationLoad = $state(false);
  let hasLoadedVoices = $state(false);
  let conversationLoadErrorMessage = $state('');
  let isVoiceSheetOpen = $state(false);
  let cloneView = $state<CloneView>('list');
  let isRecordMode = $state(false);
  let cloneSettingName = $state(DEFAULT_FORM_STATE.cloneSettingName);
  let cloneRefText = $state(DEFAULT_FORM_STATE.cloneRefText);
  let cloneLang = $state(DEFAULT_FORM_STATE.cloneLang);
  let cloneSpeed = $state(DEFAULT_FORM_STATE.cloneSpeed);
  let cloneNumStep = $state(DEFAULT_FORM_STATE.cloneNumStep);
  let cloneRefAudioFile = $state<File | null>(null);
  let cloneRefAudioPreviewUrl = $state('');
  let cloneRefAudioInputKey = $state(0);
  let cloneRefAudioIsMicrophoneRecording = $state(false);
  let isSavingCloneSetting = $state(false);
  let isUpdatingCloneSetting = $state(false);
  let isLoadingSelectedCloneSetting = $state(false);
  let isDeletingCloneSetting = $state(false);
  let selectedCloneSettingId = $state<number | null>(null);
  let selectedCloneSetting = $state<SavedCloneSetting | null>(null);
  let isRecordingCloneRefAudio = $state(false);
  let microphoneStatusMessage = $state('');
  let microphoneStatusIsError = $state(false);
  let recordingStartedAt = $state<number | null>(null);
  let recordingElapsedMs = $state(0);
  let mediaStream = $state<MediaStream | null>(null);
  let isSavingConversation = $state(false);
  let draftName = $state('');
  let draftLines = $state<ConversationLineMutation[]>([]);
  let selectedLineIndex = $state<number | null>(null);
  let activeGeneratingConversationLineIndex = $state<number | null>(null);
  let playingLineIndex = $state<number | null>(null);
  let playbackAudioElement = $state<HTMLAudioElement | null>(null);
  let playbackAudioSrc = $state('');
  let playbackToken = 0;
  let playbackReadyResolver: (() => void) | null = null;
  let mediaRecorder: MediaRecorder | null = null;
  let speechRecognition: SpeechRecognitionInstance | null = null;
  let recordingChunks: Blob[] = [];
  let transcriptSegments: string[] = [];
  let transcriptFallback = '';
  let recognitionShouldRemainActive = false;
  let discardPendingRecording = false;

  let isBusy = $derived(
    status === 'loading-model' ||
      status === 'unloading-model' ||
      status === 'synthesizing' ||
      status === 'cloning'
  );
  let routeConversationId = $derived.by(() => {
    const parsedConversationId = Number(conversationId);
    return Number.isFinite(parsedConversationId) && parsedConversationId > 0
      ? parsedConversationId
      : null;
  });
  let selectedConversationId = $derived(loadedConversation?.id ?? routeConversationId);
  let canSaveCloneSetting = $derived(
    cloneSettingName.trim().length > 0 &&
      cloneRefText.trim().length > 0 &&
      cloneRefAudioFile !== null &&
      !isSavingCloneSetting &&
      !isBusy &&
      !isLoadingSelectedCloneSetting
  );
  let canUpdateCloneSetting = $derived(
    selectedCloneSetting !== null &&
      cloneSettingName.trim().length > 0 &&
      !isUpdatingCloneSetting &&
      !isDeletingCloneSetting &&
      !isBusy
  );
  let canDeleteCloneSetting = $derived(
    selectedCloneSetting !== null && !isDeletingCloneSetting && !isBusy
  );
  let recordingElapsedLabel = $derived(formatElapsedTime(recordingElapsedMs));
  let isSpeechRecognitionSupported = $derived(getSpeechRecognitionConstructor() !== null);
  let canRecordCloneRefAudio = $derived(
    !isSavingCloneSetting && !isBusy && typeof navigator !== 'undefined'
  );
  let selectedLine = $derived(
    selectedLineIndex === null ? null : (draftLines[selectedLineIndex] ?? null)
  );
  let conversationTitle = $derived(
    draftName.trim() || loadedConversation?.name || UI_TEXT.conversationTitleFallback
  );

  function resetCloneRefAudioPreview() {
    revokeObjectUrl(cloneRefAudioPreviewUrl);
    cloneRefAudioPreviewUrl = '';
  }

  function clearCloneRefAudioSelection() {
    resetCloneRefAudioPreview();
    cloneRefAudioFile = null;
    cloneRefAudioIsMicrophoneRecording = false;
    cloneRefAudioInputKey += 1;
  }

  function setMicrophoneStatus(message: string, isError = false) {
    microphoneStatusMessage = message;
    microphoneStatusIsError = isError;
  }

  function stopMediaStream() {
    for (const track of mediaStream?.getTracks() ?? []) {
      track.stop();
    }
    mediaStream = null;
  }

  function stopSpeechRecognition() {
    recognitionShouldRemainActive = false;
    try {
      speechRecognition?.stop();
    } catch {
      // Ignore browser stop races.
    }
    speechRecognition = null;
  }

  function resetRecordingState() {
    isRecordingCloneRefAudio = false;
    recordingStartedAt = null;
    recordingElapsedMs = 0;
    recordingChunks = [];
    transcriptSegments = [];
    transcriptFallback = '';
    mediaRecorder = null;
  }

  function startSpeechRecognition() {
    const Recognition = getSpeechRecognitionConstructor();
    if (!Recognition) {
      setMicrophoneStatus(UI_TEXT.speechRecognitionNotSupported, true);
      return;
    }

    const recognition = new Recognition();
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.lang = getSpeechRecognitionLocale(
      selectedLine?.lang ?? DEFAULT_FORM_STATE.cloneLang
    );
    recognitionShouldRemainActive = true;

    recognition.onresult = (event: SpeechRecognitionEvent) => {
      transcriptFallback = buildTranscriptFromEvent(event);
      transcriptSegments = [];

      for (let index = 0; index < event.results.length; index += 1) {
        const result = event.results[index];
        if (result?.isFinal) {
          const transcript = result[0]?.transcript?.trim();
          if (transcript) {
            transcriptSegments.push(transcript);
          }
        }
      }

      const nextTranscript = transcriptSegments.join(' ').trim() || transcriptFallback;
      if (nextTranscript) {
        cloneRefText = nextTranscript;
        setMicrophoneStatus(UI_TEXT.recordingTranscriptPending);
      }
    };

    recognition.onerror = (event: SpeechRecognitionErrorEvent) => {
      if (event.error === 'aborted' || event.error === 'no-speech') {
        return;
      }

      setMicrophoneStatus(UI_TEXT.speechRecognitionNotSupported, true);
    };

    recognition.onend = () => {
      if (!recognitionShouldRemainActive) return;
      try {
        recognition.start();
      } catch {
        recognitionShouldRemainActive = false;
      }
    };

    speechRecognition = recognition;
    recognition.start();
  }

  function finalizeRecording(blob: Blob, mimeType: string) {
    const effectiveMimeType = mimeType || blob.type || 'audio/webm';
    const extension = getRecordedFileExtension(effectiveMimeType);
    const file = new File([blob], `microphone-recording-${Date.now()}.${extension}`, {
      type: effectiveMimeType
    });

    clearCloneRefAudioSelection();
    cloneRefAudioFile = file;
    cloneRefAudioIsMicrophoneRecording = true;
    cloneRefAudioPreviewUrl = URL.createObjectURL(file);

    const capturedTranscript = transcriptSegments.join(' ').trim() || transcriptFallback.trim();
    if (capturedTranscript) {
      cloneRefText = capturedTranscript;
      setMicrophoneStatus(UI_TEXT.recordingTranscriptReady);
    } else if (isSpeechRecognitionSupported) {
      setMicrophoneStatus(UI_TEXT.recordingTranscriptUnavailable, true);
    }
  }

  async function finalizeRecordedBlob(blob: Blob, mimeType: string) {
    if (blob.size === 0) {
      setMicrophoneStatus(UI_TEXT.recordingFailed, true);
      return;
    }

    try {
      const wavBlob = await convertRecordedBlobToWav(blob);
      finalizeRecording(wavBlob, wavBlob.type || mimeType || 'audio/wav');
    } catch {
      setMicrophoneStatus(UI_TEXT.recordingFailed, true);
    }
  }

  async function startCloneRefRecording() {
    if (typeof navigator === 'undefined' || typeof MediaRecorder === 'undefined') {
      setMicrophoneStatus(UI_TEXT.microphoneNotSupported, true);
      return;
    }

    resetCloneRefAudioPreview();
    cloneRefAudioFile = null;
    cloneRefAudioIsMicrophoneRecording = false;
    recordingChunks = [];
    transcriptSegments = [];
    transcriptFallback = '';
    discardPendingRecording = false;
    setMicrophoneStatus('');

    let stream: MediaStream;
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    } catch {
      setMicrophoneStatus(UI_TEXT.microphoneAccessFailed, true);
      return;
    }

    mediaStream = stream;

    try {
      const mimeType = getPreferredRecordingMimeType();
      mediaRecorder = mimeType
        ? new MediaRecorder(stream, { mimeType })
        : new MediaRecorder(stream);
    } catch {
      stopMediaStream();
      setMicrophoneStatus(UI_TEXT.recordingFailed, true);
      return;
    }

    mediaRecorder.ondataavailable = (event: BlobEvent) => {
      if (event.data.size > 0) {
        recordingChunks.push(event.data);
      }
    };

    mediaRecorder.onerror = () => {
      setMicrophoneStatus(UI_TEXT.recordingFailed, true);
    };

    mediaRecorder.onstop = () => {
      const recorderMimeType =
        mediaRecorder?.mimeType || getPreferredRecordingMimeType() || 'audio/webm';
      const recordedBlob = new Blob(recordingChunks, { type: recorderMimeType });
      const shouldDiscard = discardPendingRecording;
      discardPendingRecording = false;
      stopMediaStream();
      stopSpeechRecognition();
      resetRecordingState();

      if (shouldDiscard) return;
      if (recordedBlob.size === 0) {
        setMicrophoneStatus(UI_TEXT.recordingFailed, true);
        return;
      }

      void finalizeRecordedBlob(recordedBlob, recorderMimeType);
    };

    mediaRecorder.start();
    isRecordingCloneRefAudio = true;
    recordingStartedAt = Date.now();
    recordingElapsedMs = 0;
    setMicrophoneStatus(
      isSpeechRecognitionSupported
        ? UI_TEXT.recordingTranscriptPending
        : UI_TEXT.speechRecognitionNotSupported,
      !isSpeechRecognitionSupported
    );
    startSpeechRecognition();
  }

  function stopCloneRefRecording() {
    if (!mediaRecorder || mediaRecorder.state === 'inactive') return;
    mediaRecorder.stop();
  }

  function discardCloneRefRecording() {
    discardPendingRecording = true;
    stopSpeechRecognition();
    if (mediaRecorder && mediaRecorder.state !== 'inactive') {
      mediaRecorder.stop();
      return;
    }

    stopMediaStream();
    resetRecordingState();
  }

  async function handleToggleCloneRefRecording() {
    if (isRecordingCloneRefAudio) {
      stopCloneRefRecording();
      return;
    }

    await startCloneRefRecording();
  }

  function resetCloneSettingForm() {
    cloneSettingName = DEFAULT_FORM_STATE.cloneSettingName;
    cloneRefText = DEFAULT_FORM_STATE.cloneRefText;
    cloneLang = DEFAULT_FORM_STATE.cloneLang;
    cloneSpeed = DEFAULT_FORM_STATE.cloneSpeed;
    cloneNumStep = DEFAULT_FORM_STATE.cloneNumStep;
  }

  function createInstructionLine(position: number): ConversationLineMutation {
    const instruct = buildInstruct([
      DEFAULT_FORM_STATE.selectedGender,
      DEFAULT_FORM_STATE.selectedPitch,
      DEFAULT_FORM_STATE.selectedAccent,
      DEFAULT_FORM_STATE.selectedAge,
      DEFAULT_FORM_STATE.selectedStyle
    ]);

    return {
      position,
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

  function createCloneLine(position: number): ConversationLineMutation {
    const setting = savedCloneSettings[0] ?? null;
    if (!setting) {
      return {
        position,
        text: '',
        voice_type: 'clone',
        clone_setting_id: null,
        voice_label: 'No saved voices',
        audio_url: '',
        lang: DEFAULT_FORM_STATE.cloneLang,
        speed: DEFAULT_FORM_STATE.cloneSpeed,
        num_step: DEFAULT_FORM_STATE.cloneNumStep,
        instruct: '',
        selected_gender: '',
        selected_accent: '',
        selected_pitch: '',
        selected_age: '',
        selected_style: ''
      };
    }

    return {
      position,
      text: '',
      voice_type: 'clone',
      clone_setting_id: setting.id,
      voice_label: setting.name,
      audio_url: '',
      lang: setting.lang,
      speed: setting.speed,
      num_step: setting.num_step,
      instruct: '',
      selected_gender: '',
      selected_accent: '',
      selected_pitch: '',
      selected_age: '',
      selected_style: ''
    };
  }

  function createNewLine(position: number): ConversationLineMutation {
    return savedCloneSettings.length > 0
      ? createCloneLine(position)
      : createInstructionLine(position);
  }

  function reindexDraftLines(lines: ConversationLineMutation[]) {
    return lines.map((line, index) => ({ ...line, position: index }));
  }

  function loadConversationIntoDraft(
    conversation: Conversation | null,
    nextSelectedLineIndex?: number | null
  ) {
    if (!conversation) {
      draftName = '';
      draftLines = [];
      selectedLineIndex = null;
      return;
    }

    draftName = conversation.name;
    draftLines = conversation.lines.map((line, index) => ({
      position: index,
      text: line.text,
      voice_type: line.voice_type,
      clone_setting_id: line.clone_setting_id,
      voice_label: line.voice_label,
      audio_url: line.audio_url,
      lang: line.lang,
      speed: line.speed,
      num_step: line.num_step,
      instruct: line.instruct,
      selected_gender: line.selected_gender,
      selected_accent: line.selected_accent,
      selected_pitch: line.selected_pitch,
      selected_age: line.selected_age,
      selected_style: line.selected_style
    }));
    selectedLineIndex =
      conversation.lines.length === 0
        ? null
        : Math.min(Math.max(nextSelectedLineIndex ?? 0, 0), conversation.lines.length - 1);
  }

  function refreshCurrentLineReference() {
    draftLines = [...draftLines];
  }

  function updateInstructionLine(line: ConversationLineMutation) {
    line.instruct = buildInstruct([
      line.selected_gender,
      line.selected_pitch,
      line.selected_accent,
      line.selected_age,
      line.selected_style
    ]);
    line.voice_label = line.instruct || 'Instruction voice';
    refreshCurrentLineReference();
  }

  function updateLineVoiceType(line: ConversationLineMutation, voiceType: ConversationVoiceType) {
    if (voiceType === 'clone') {
      const nextLine = createCloneLine(line.position);
      draftLines[line.position] = { ...nextLine, text: line.text };
    } else {
      const nextLine = createInstructionLine(line.position);
      draftLines[line.position] = { ...nextLine, text: line.text };
    }
    refreshCurrentLineReference();
  }

  function updateCloneSelection(line: ConversationLineMutation, settingId: string) {
    const setting = savedCloneSettings.find((item) => item.id === Number(settingId)) ?? null;
    if (!setting) return;
    line.clone_setting_id = setting.id;
    line.voice_label = setting.name;
    line.lang = setting.lang;
    line.speed = setting.speed;
    line.num_step = setting.num_step;
    refreshCurrentLineReference();
  }

  function updateSelectedLineVoiceType(voiceType: ConversationVoiceType) {
    if (!selectedLine) return;
    updateLineVoiceType(selectedLine, voiceType);
  }

  function addLine() {
    const insertIndex = draftLines.length;
    const nextLines = [...draftLines, createNewLine(insertIndex)];
    draftLines = reindexDraftLines(nextLines);
    selectedLineIndex = insertIndex;
  }

  function moveLine(lineIndex: number, direction: -1 | 1) {
    const nextIndex = lineIndex + direction;
    if (nextIndex < 0 || nextIndex >= draftLines.length) return;
    const nextLines = [...draftLines];
    const [line] = nextLines.splice(lineIndex, 1);
    nextLines.splice(nextIndex, 0, line);
    draftLines = reindexDraftLines(nextLines);
    selectedLineIndex = nextIndex;
  }

  function deleteLine(lineIndex: number) {
    if (!window.confirm(UI_TEXT.conversationDeleteLineConfirm)) return;
    const nextLines = draftLines.filter((_, index) => index !== lineIndex);
    draftLines = reindexDraftLines(nextLines.length > 0 ? nextLines : [createNewLine(0)]);
    selectedLineIndex = Math.min(lineIndex, draftLines.length - 1);
  }

  function stopConversationPlayback() {
    playbackToken += 1;
    playingLineIndex = null;
    playbackAudioSrc = '';
    playbackReadyResolver?.();
    playbackReadyResolver = null;
    if (!playbackAudioElement) return;
    playbackAudioElement.pause();
    playbackAudioElement.currentTime = 0;
  }

  async function waitForPlaybackAudioElement() {
    if (playbackAudioElement) {
      return playbackAudioElement;
    }

    await new Promise<void>((resolve) => {
      playbackReadyResolver = resolve;
    });

    if (!playbackAudioElement) {
      throw new Error(UI_TEXT.conversationPlaybackInitFailed);
    }

    return playbackAudioElement;
  }

  async function playWithAudioPlayer(src: string, token: number) {
    playbackAudioSrc = src;
    await tick();
    const audio = await waitForPlaybackAudioElement();
    if (token !== playbackToken) {
      return;
    }

    audio.currentTime = 0;
    audio.load();

    await new Promise<void>((resolve, reject) => {
      const handleEnded = () => {
        cleanup();
        resolve();
      };
      const handleError = () => {
        cleanup();
        reject(new Error(UI_TEXT.conversationPlaybackFailed));
      };
      const cleanup = () => {
        audio.removeEventListener('ended', handleEnded);
        audio.removeEventListener('error', handleError);
      };

      audio.addEventListener('ended', handleEnded);
      audio.addEventListener('error', handleError);
      void audio.play().catch((error) => {
        cleanup();
        reject(error);
      });
    });
  }

  async function playFullConversation() {
    if (draftLines.length === 0) return;
    stopConversationPlayback();
    const token = playbackToken;

    try {
      for (const [index, line] of draftLines.entries()) {
        if (token !== playbackToken) return;
        if (!line.audio_url) continue;

        playingLineIndex = index;
        await playWithAudioPlayer(line.audio_url, token);
      }
    } finally {
      if (token === playbackToken) {
        playingLineIndex = null;
        playbackAudioSrc = '';
      }
    }
  }

  async function handleSelectSavedCloneSetting(settingId: number) {
    cloneSettingsErrorMessage = '';
    cloneSettingsMessage = '';
    isLoadingSelectedCloneSetting = true;
    selectedCloneSettingId = settingId;

    try {
      const setting = await getSavedCloneSetting(settingId);
      selectedCloneSetting = setting;
      cloneSettingName = setting.name;
      cloneRefText = setting.ref_text;
      cloneLang = setting.lang;
      cloneSpeed = setting.speed;
      cloneNumStep = setting.num_step;
      if (selectedLine) {
        updateCloneSelection(selectedLine, `${setting.id}`);
      }
      cloneView = 'selected';
    } catch (error) {
      cloneSettingsErrorMessage =
        error instanceof Error ? error.message : UI_TEXT.savedCloneSettingsFailed;
    } finally {
      isLoadingSelectedCloneSetting = false;
    }
  }

  function handleSelectVoice(settingId: number) {
    void handleSelectSavedCloneSetting(settingId).then(() => {
      isVoiceSheetOpen = false;
    });
  }

  function handleStartAddUpload() {
    isRecordMode = false;
    cloneView = 'create';
    selectedCloneSettingId = null;
    selectedCloneSetting = null;
    resetCloneSettingForm();
    clearCloneRefAudioSelection();
    setMicrophoneStatus('');
    cloneSettingsMessage = '';
    cloneSettingsErrorMessage = '';
  }

  function handleStartAddRecord() {
    isRecordMode = true;
    cloneView = 'create';
    selectedCloneSettingId = null;
    selectedCloneSetting = null;
    resetCloneSettingForm();
    clearCloneRefAudioSelection();
    setMicrophoneStatus('');
    cloneSettingsMessage = '';
    cloneSettingsErrorMessage = '';
  }

  function handleStartEditVoice(settingId: number) {
    void handleSelectSavedCloneSetting(settingId);
  }

  function handleBackToList() {
    if (cloneView !== 'selected') {
      selectedCloneSettingId = null;
      selectedCloneSetting = null;
    }

    cloneView = 'list';
    cloneSettingsMessage = '';
    cloneSettingsErrorMessage = '';
    if (isRecordingCloneRefAudio) {
      discardCloneRefRecording();
    }
    isRecordMode = false;
  }

  async function handleSaveCloneSetting() {
    const trimmedName = cloneSettingName.trim();
    const trimmedRefText = cloneRefText.trim();
    cloneSettingsErrorMessage = '';
    cloneSettingsMessage = '';

    if (!trimmedName) {
      cloneSettingsErrorMessage = UI_TEXT.cloneSettingNameError;
      return;
    }
    if (!cloneRefAudioFile) {
      cloneSettingsErrorMessage = UI_TEXT.uploadReferenceAudioError;
      return;
    }
    if (!trimmedRefText) {
      cloneSettingsErrorMessage = UI_TEXT.enterReferenceTextError;
      return;
    }

    isSavingCloneSetting = true;
    try {
      const payload = await saveCloneSetting({
        name: trimmedName,
        refText: trimmedRefText,
        lang: cloneLang,
        speed: cloneSpeed,
        numStep: cloneNumStep,
        refAudio: cloneRefAudioFile,
        isMicrophoneRecording: cloneRefAudioIsMicrophoneRecording
      });
      cloneSettingsMessage = payload.message || UI_TEXT.cloneSettingSavedSuccess;
      clearCloneRefAudioSelection();
      setMicrophoneStatus('');
      await refreshVoices();
      if (typeof payload.id === 'number') {
        await handleSelectSavedCloneSetting(payload.id);
      }
      isVoiceSheetOpen = false;
    } catch (error) {
      cloneSettingsErrorMessage =
        error instanceof Error ? error.message : UI_TEXT.saveCloneSettingFailed;
    } finally {
      isSavingCloneSetting = false;
    }
  }

  async function handleUpdateSelectedCloneSetting() {
    if (!selectedCloneSetting) return;
    const activeCloneSetting = selectedCloneSetting;
    const trimmedName = cloneSettingName.trim();
    if (!trimmedName) {
      cloneSettingsErrorMessage = UI_TEXT.cloneSettingNameError;
      return;
    }

    isUpdatingCloneSetting = true;
    cloneSettingsMessage = '';
    cloneSettingsErrorMessage = '';
    try {
      await updateCloneSetting({
        settingId: selectedCloneSetting.id,
        name: trimmedName,
        lang: cloneLang,
        speed: cloneSpeed,
        numStep: cloneNumStep
      });
      selectedCloneSetting = {
        ...activeCloneSetting,
        name: trimmedName,
        lang: cloneLang,
        speed: cloneSpeed,
        num_step: cloneNumStep
      };
      cloneSettingName = trimmedName;
      savedCloneSettings = savedCloneSettings.map((setting) =>
        setting.id === activeCloneSetting.id
          ? {
              ...setting,
              name: trimmedName,
              lang: cloneLang,
              speed: cloneSpeed,
              num_step: cloneNumStep
            }
          : setting
      );
      cloneSettingsMessage = UI_TEXT.cloneSettingUpdatedSuccess;
      if (selectedLine?.clone_setting_id === activeCloneSetting.id) {
        selectedLine.voice_label = trimmedName;
        refreshCurrentLineReference();
      }
    } catch (error) {
      cloneSettingsErrorMessage =
        error instanceof Error ? error.message : UI_TEXT.updateCloneSettingFailed;
    } finally {
      isUpdatingCloneSetting = false;
    }
  }

  async function handleDeleteSavedCloneSetting(settingId: number) {
    const settingToDelete = savedCloneSettings.find((setting) => setting.id === settingId) ?? null;
    if (!settingToDelete) return;
    if (!window.confirm(UI_TEXT.deleteCloneSettingConfirm)) return;

    isDeletingCloneSetting = true;
    cloneSettingsErrorMessage = '';
    cloneSettingsMessage = '';
    try {
      await deleteCloneSetting(settingToDelete.id);
      savedCloneSettings = savedCloneSettings.filter(
        (setting) => setting.id !== settingToDelete.id
      );
      if (selectedCloneSettingId === settingToDelete.id) {
        selectedCloneSettingId = null;
        selectedCloneSetting = null;
        cloneView = 'list';
      }
      if (selectedLine?.clone_setting_id === settingToDelete.id) {
        selectedLine.clone_setting_id = null;
        selectedLine.voice_label = UI_TEXT.noVoicesAvailable;
        refreshCurrentLineReference();
      }
      cloneSettingsMessage = UI_TEXT.cloneSettingDeletedSuccess;
    } catch (error) {
      cloneSettingsErrorMessage =
        error instanceof Error ? error.message : UI_TEXT.deleteCloneSettingFailed;
    } finally {
      isDeletingCloneSetting = false;
    }
  }

  async function handleDeleteSelectedCloneSetting() {
    if (!selectedCloneSetting) return;
    await handleDeleteSavedCloneSetting(selectedCloneSetting.id);
  }

  function handleRefAudioChange(event: Event) {
    const input = event.currentTarget as HTMLInputElement;
    resetCloneRefAudioPreview();
    cloneRefAudioFile = input.files?.[0] ?? null;
    cloneRefAudioIsMicrophoneRecording = false;
    cloneRefAudioPreviewUrl = cloneRefAudioFile ? URL.createObjectURL(cloneRefAudioFile) : '';
    setMicrophoneStatus('');
  }

  async function ensureModelLoaded() {
    if (modelReady) return;
    status = 'loading-model';
    const payload = await loadModel();
    modelReady = true;
    modelDevice = payload.device ?? null;
    toast.success(payload.message || UI_TEXT.modelLoadedSuccess);
    status = 'idle';
  }

  async function handleLoadModel() {
    try {
      await ensureModelLoaded();
    } catch (error) {
      status = 'error';

      const errorMessage = error instanceof Error ? error.message : UI_TEXT.loadModelFailed;
      toast.error(errorMessage);
    }
  }

  async function handleUnloadModel() {
    status = 'unloading-model';
    try {
      const payload = await unloadModel();
      modelReady = false;
      modelDevice = payload.device ?? null;
      toast.success(payload.message || UI_TEXT.modelUnloadedSuccess);
      status = 'idle';
    } catch (error) {
      status = 'error';
      modelDevice = null;
      const errorMessage = error instanceof Error ? error.message : UI_TEXT.unloadModelFailed;
      toast.error(errorMessage);
    }
  }

  async function refreshConversation(nextSelectedLineIndex: number | null = selectedLineIndex) {
    if (routeConversationId === null) {
      conversationLoadErrorMessage = UI_TEXT.conversationDetailUnavailable;
      loadConversationIntoDraft(null);
      loadedConversation = null;
      return;
    }

    isLoadingConversation = true;
    conversationLoadErrorMessage = '';

    try {
      const conversation = await getConversation(routeConversationId);
      loadedConversation = conversation;
      loadConversationIntoDraft(conversation, nextSelectedLineIndex);
    } catch (error) {
      loadedConversation = null;
      loadConversationIntoDraft(null);

      const errorMessage = error instanceof Error ? error.message : UI_TEXT.conversationLoadFailed;
      conversationLoadErrorMessage = errorMessage;
      toast.error(errorMessage);
    } finally {
      isLoadingConversation = false;
    }
  }

  async function refreshVoices() {
    isLoadingVoices = true;
    try {
      savedCloneSettings = await listSavedCloneSettings();
      if (selectedCloneSettingId !== null) {
        selectedCloneSetting =
          savedCloneSettings.find((setting) => setting.id === selectedCloneSettingId) ?? null;
        if (selectedCloneSetting === null && cloneView === 'selected') {
          cloneView = 'list';
        }
      }
      hasLoadedVoices = true;
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : UI_TEXT.savedCloneSettingsFailed;
      toast.error(errorMessage);
    } finally {
      isLoadingVoices = false;
    }
  }

  async function persistDraftConversation() {
    if (routeConversationId === null) {
      return null;
    }

    const preservedLineIndex = selectedLineIndex;

    const response = await updateConversation(routeConversationId, {
      name: draftName.trim(),
      lines: reindexDraftLines(draftLines)
    });
    const savedConversation = response.conversation;
    loadedConversation = savedConversation;
    loadConversationIntoDraft(savedConversation, preservedLineIndex);
    return response;
  }

  async function generateLine(line: ConversationLineMutation) {
    if (!line) return;

    const lineIndex = draftLines.indexOf(line);

    const trimmedText = line.text.trim();
    if (!trimmedText) {
      toast.error(UI_TEXT.enterTextError);
      return;
    }

    activeGeneratingConversationLineIndex = lineIndex;

    try {
      await ensureModelLoaded();
      if (line.voice_type === 'clone') {
        if (line.clone_setting_id === null) {
          throw new Error(UI_TEXT.selectCloneSettingError);
        }

        status = 'cloning';
        const payload = await cloneAudio({
          text: trimmedText,
          settingId: line.clone_setting_id,
          lang: line.lang,
          speed: line.speed,
          numStep: line.num_step
        });
        line.audio_url = payload.audio_url;
        line.voice_label =
          savedCloneSettings.find((setting) => setting.id === line.clone_setting_id)?.name ??
          line.voice_label;
        await persistDraftConversation();
        toast.success(payload.message || UI_TEXT.cloneComplete);
      } else {
        updateInstructionLine(line);
        status = 'synthesizing';
        const payload = await synthesizeAudio({
          text: trimmedText,
          lang: line.lang,
          speed: line.speed,
          num_step: line.num_step,
          instruct: line.instruct
        });
        line.audio_url = payload.audio_url;
        await persistDraftConversation();
        toast.success(payload.message || UI_TEXT.synthesisComplete);
      }
      draftLines = [...draftLines];
      status = 'success';
    } catch (error) {
      status = 'error';
      const errorMessage =
        error instanceof Error ? error.message : UI_TEXT.conversationGenerateFailed;
      toast.error(errorMessage);
    } finally {
      activeGeneratingConversationLineIndex = null;
    }
  }

  async function saveCurrentConversation() {
    if (routeConversationId === null) {
      toast.error(UI_TEXT.conversationDetailUnavailable);
      return;
    }

    const trimmedName = draftName.trim();
    if (!trimmedName) {
      toast.error(UI_TEXT.conversationNameRequired);
      return;
    }

    if (draftLines.length === 0) {
      toast.error(UI_TEXT.conversationNeedsLine);
      return;
    }

    isSavingConversation = true;

    try {
      const payload = {
        name: trimmedName,
        lines: reindexDraftLines(draftLines)
      };
      const response = await updateConversation(routeConversationId, payload);
      const savedConversation = response.conversation;
      loadedConversation = savedConversation;
      loadConversationIntoDraft(savedConversation);
      toast.success(response.message || UI_TEXT.conversationSaved);
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : UI_TEXT.conversationSaveFailed;
      toast.error(errorMessage);
    } finally {
      isSavingConversation = false;
    }
  }

  async function deleteSelectedConversation() {
    if (routeConversationId === null || !loadedConversation) return;
    if (
      !window.confirm(UI_TEXT.conversationDeletePrompt.replace('{name}', loadedConversation.name))
    ) {
      return;
    }

    try {
      const response = await deleteConversation(routeConversationId);
      stopConversationPlayback();
      loadConversationIntoDraft(null);
      loadedConversation = null;
      toast.success(response.message || UI_TEXT.conversationDeleted);
      await goto(resolve('/conversation'), { replaceState: true, noScroll: true });
    } catch (error) {
      const errorMessage =
        error instanceof Error ? error.message : UI_TEXT.conversationDeleteFailed;
      toast.error(errorMessage);
    }
  }

  async function goBackToConversationList() {
    stopConversationPlayback();
    await goto(resolve('/conversation'), { noScroll: true });
  }

  $effect(() => {
    dashboardHeaderState.setState({
      status,
      modelReady,
      modelDevice,
      isBusy,
      onLoadModel: handleLoadModel,
      onUnloadModel: handleUnloadModel
    });
  });

  $effect(() => {
    if (playbackAudioElement && playbackReadyResolver) {
      playbackReadyResolver();
      playbackReadyResolver = null;
    }
  });

  $effect(() => {
    if (hasAttemptedConversationLoad || isLoadingConversation) {
      return;
    }

    hasAttemptedConversationLoad = true;

    if (routeConversationId === null) {
      conversationLoadErrorMessage = UI_TEXT.conversationDetailUnavailable;
      return;
    }

    void refreshConversation();
  });

  $effect(() => {
    if (!hasLoadedVoices && !isLoadingVoices) {
      void refreshVoices();
    }
  });

  $effect(() => {
    if (!isVoiceSheetOpen) {
      cloneView = 'list';
      cloneSettingsMessage = '';
      cloneSettingsErrorMessage = '';
    }
  });

  $effect(() => {
    if (!isVoiceSheetOpen || hasLoadedVoices || isLoadingVoices) return;
    void refreshVoices();
  });

  $effect(() => {
    if (!isRecordingCloneRefAudio || recordingStartedAt === null || typeof window === 'undefined') {
      return;
    }

    recordingElapsedMs = Date.now() - recordingStartedAt;
    const intervalId = window.setInterval(() => {
      recordingElapsedMs = recordingStartedAt === null ? 0 : Date.now() - recordingStartedAt;
    }, 250);

    return () => window.clearInterval(intervalId);
  });

  $effect(() => {
    const isInRecordView = isVoiceSheetOpen && cloneView === 'create' && isRecordMode;
    if (!isInRecordView && (isRecordingCloneRefAudio || mediaStream !== null)) {
      discardCloneRefRecording();
    }
  });

  onDestroy(() => {
    dashboardHeaderState.reset();
    stopConversationPlayback();
    resetCloneRefAudioPreview();
    discardCloneRefRecording();
    stopSpeechRecognition();
    stopMediaStream();
  });
</script>

<Button variant="outline" class="gap-2" onclick={goBackToConversationList}>
  <ArrowLeftIcon class="size-4" />
  {UI_TEXT.conversationBackButton}
</Button>

{#if isLoadingConversation}
  <div class="text-muted-foreground flex items-center gap-2 text-sm">
    <LoaderIcon class="size-4 animate-spin" />
    {UI_TEXT.conversationDetailLoading}
  </div>
{:else if conversationLoadErrorMessage}
  <div class="rounded-xl border border-dashed px-4 py-6 text-sm">
    {conversationLoadErrorMessage}
  </div>
{:else}
  <div class="grid gap-6 lg:grid-cols-[minmax(0,1fr)_360px]">
    <div class="space-y-4">
      <ConversationEditor
        {selectedConversationId}
        {conversationTitle}
        {draftName}
        {draftLines}
        {selectedLineIndex}
        {activeGeneratingConversationLineIndex}
        {playingLineIndex}
        {playbackAudioSrc}
        bind:playbackAudioElement
        {isSavingConversation}
        onDraftNameChange={(value) => (draftName = value)}
        onSelectLine={(lineIndex) => (selectedLineIndex = lineIndex)}
        onPlayConversation={playFullConversation}
        onStopConversationPlayback={stopConversationPlayback}
        onSaveConversation={saveCurrentConversation}
        onDeleteConversation={deleteSelectedConversation}
        onMoveLine={moveLine}
        onDeleteLine={deleteLine}
        onGenerateLine={generateLine}
        onAddLine={addLine}
      />
    </div>

    <ConversationLineConfig
      {selectedLine}
      {selectedLineIndex}
      {activeGeneratingConversationLineIndex}
      {savedCloneSettings}
      onUpdateVoiceType={updateSelectedLineVoiceType}
      onOpenVoiceLibrary={() => {
        cloneView = 'list';
        isRecordMode = false;
        cloneLang = selectedLine?.lang ?? DEFAULT_FORM_STATE.cloneLang;
        cloneSpeed = selectedLine?.speed ?? DEFAULT_FORM_STATE.cloneSpeed;
        cloneNumStep = selectedLine?.num_step ?? DEFAULT_FORM_STATE.cloneNumStep;
        selectedCloneSettingId = selectedLine?.clone_setting_id ?? null;
        selectedCloneSetting =
          savedCloneSettings.find((setting) => setting.id === selectedLine?.clone_setting_id) ??
          null;
        isVoiceSheetOpen = true;
      }}
      onGenerateLine={generateLine}
    />
  </div>
{/if}

<VoiceSelectionSheet
  bind:open={isVoiceSheetOpen}
  {cloneView}
  {isRecordMode}
  {savedCloneSettings}
  {selectedCloneSettingId}
  {selectedCloneSetting}
  isCloneSettingsLoading={isLoadingVoices}
  hasLoadedCloneSettings={hasLoadedVoices}
  {isSavingCloneSetting}
  {isUpdatingCloneSetting}
  {isDeletingCloneSetting}
  {canSaveCloneSetting}
  {canUpdateCloneSetting}
  {canDeleteCloneSetting}
  {cloneSettingsMessage}
  {cloneSettingsErrorMessage}
  bind:cloneSettingName
  bind:cloneRefText
  bind:cloneLang
  bind:cloneSpeed
  bind:cloneNumStep
  {cloneRefAudioFile}
  {cloneRefAudioPreviewUrl}
  {cloneRefAudioInputKey}
  {cloneRefAudioIsMicrophoneRecording}
  {isRecordingCloneRefAudio}
  {recordingElapsedLabel}
  {microphoneStatusMessage}
  {microphoneStatusIsError}
  {isSpeechRecognitionSupported}
  {canRecordCloneRefAudio}
  {mediaStream}
  onSelectVoice={handleSelectVoice}
  onStartAddUpload={handleStartAddUpload}
  onStartAddRecord={handleStartAddRecord}
  onStartEditVoice={handleStartEditVoice}
  onSaveCloneSetting={handleSaveCloneSetting}
  onUpdateCloneSetting={handleUpdateSelectedCloneSetting}
  onDeleteVoice={handleDeleteSavedCloneSetting}
  onDeleteSelectedVoice={handleDeleteSelectedCloneSetting}
  onBackToList={handleBackToList}
  onRefreshVoices={refreshVoices}
  onToggleRecording={handleToggleCloneRefRecording}
  onRefAudioChange={handleRefAudioChange}
/>
