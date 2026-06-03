<script lang="ts">
  import { onDestroy } from 'svelte';
  import {
    cloneAudio,
    deleteCloneSetting,
    getSavedCloneSetting,
    listSavedCloneSettings,
    loadModel,
    saveCloneSetting,
    synthesizeAudio,
    unloadModel,
    updateCloneSetting
  } from '$lib/tts/api';
  import {
    buildTranscriptFromEvent,
    convertRecordedBlobToWav,
    formatElapsedTime,
    getPreferredRecordingMimeType,
    getRecordedFileExtension,
    getSpeechRecognitionLocale,
    getSpeechRecognitionConstructor
  } from '$lib/tts/audio';
  import TtsDashboard from '$lib/tts/components/TtsDashboard.svelte';
  import {
    DEFAULT_FORM_STATE,
    LANGUAGES,
    PAGE_DESCRIPTION,
    PAGE_TITLE,
    UI_TEXT
  } from '$lib/tts/constants';
  import { buildInstruct, revokeObjectUrl } from '$lib/tts/helpers';
  import type {
    CloneView,
    LastRequest,
    RequestStatus,
    SavedCloneSetting,
    SpeechRecognitionErrorEvent,
    SpeechRecognitionEvent,
    SpeechRecognitionInstance,
    TtsMode
  } from '$lib/tts/types';

  let mode = $state<TtsMode>('synthesize');
  let cloneView = $state<CloneView>('list');
  let inputText = $state(DEFAULT_FORM_STATE.inputText);
  let cloneInputText = $state(DEFAULT_FORM_STATE.cloneInputText);

  let isVoiceSheetOpen = $state(false);
  let isRecordMode = $state(false);

  let cloneSettingName = $state(DEFAULT_FORM_STATE.cloneSettingName);
  let cloneRefText = $state(DEFAULT_FORM_STATE.cloneRefText);
  let cloneRefAudioFile = $state<File | null>(null);
  let cloneRefAudioPreviewUrl = $state('');
  let cloneRefAudioInputKey = $state(0);
  let cloneRefAudioIsMicrophoneRecording = $state(false);

  let isRecordingCloneRefAudio = $state(false);
  let microphoneStatusMessage = $state('');
  let microphoneStatusIsError = $state(false);
  let recordingStartedAt = $state<number | null>(null);
  let recordingElapsedMs = $state(0);
  let mediaStream = $state<MediaStream | null>(null);

  let lang = $state(DEFAULT_FORM_STATE.lang);
  let speed = $state(DEFAULT_FORM_STATE.speed);
  let numStep = $state(DEFAULT_FORM_STATE.numStep);
  let cloneLang = $state(DEFAULT_FORM_STATE.cloneLang);
  let cloneSpeed = $state(DEFAULT_FORM_STATE.cloneSpeed);
  let cloneNumStep = $state(DEFAULT_FORM_STATE.cloneNumStep);
  let selectedGender = $state(DEFAULT_FORM_STATE.selectedGender);
  let selectedAccent = $state(DEFAULT_FORM_STATE.selectedAccent);
  let selectedPitch = $state(DEFAULT_FORM_STATE.selectedPitch);
  let selectedAge = $state(DEFAULT_FORM_STATE.selectedAge);
  let selectedStyle = $state(DEFAULT_FORM_STATE.selectedStyle);

  let status = $state<RequestStatus>('idle');
  let audioUrl = $state('');
  let errorMessage = $state('');
  let responseMessage = $state('');
  let lastRequest = $state<LastRequest | null>(null);
  let modelReady = $state(false);
  let modelDevice = $state<string | null>(null);

  let cloneSettingsMessage = $state('');
  let cloneSettingsErrorMessage = $state('');
  let isCloneSettingsLoading = $state(false);
  let isSavingCloneSetting = $state(false);
  let isUpdatingCloneSetting = $state(false);
  let isLoadingSelectedCloneSetting = $state(false);
  let isDeletingCloneSetting = $state(false);
  let hasLoadedCloneSettings = $state(false);
  let savedCloneSettings = $state<SavedCloneSetting[]>([]);
  let selectedCloneSettingId = $state<number | null>(null);
  let selectedCloneSetting = $state<SavedCloneSetting | null>(null);

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
  let canSynthesize = $derived(inputText.trim().length > 0 && !isBusy);
  let canClone = $derived(
    cloneInputText.trim().length > 0 && mode === 'clone' && selectedCloneSetting !== null && !isBusy
  );
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
  let canSubmit = $derived(mode === 'clone' ? canClone : canSynthesize);
  let recordingElapsedLabel = $derived(formatElapsedTime(recordingElapsedMs));
  let isSpeechRecognitionSupported = $derived(getSpeechRecognitionConstructor() !== null);
  let canRecordCloneRefAudio = $derived(
    !isSavingCloneSetting && !isBusy && typeof navigator !== 'undefined'
  );
  let instruct = $derived(
    buildInstruct([selectedGender, selectedPitch, selectedAccent, selectedAge, selectedStyle])
  );

  function resetAudioPreview() {
    revokeObjectUrl(audioUrl);
    audioUrl = '';
  }

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
      // Ignore stop races from browser implementations.
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
    recognition.lang = getSpeechRecognitionLocale(cloneLang);
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

  onDestroy(() => {
    resetAudioPreview();
    resetCloneRefAudioPreview();
    discardCloneRefRecording();
    stopSpeechRecognition();
    stopMediaStream();
  });

  $effect(() => {
    if (mode !== 'clone' || hasLoadedCloneSettings || isCloneSettingsLoading) return;
    void refreshSavedCloneSettings();
  });

  $effect(() => {
    if (!isVoiceSheetOpen || hasLoadedCloneSettings || isCloneSettingsLoading) return;
    void refreshSavedCloneSettings();
  });

  $effect(() => {
    if (!isVoiceSheetOpen) {
      cloneView = 'list';
      cloneSettingsMessage = '';
      cloneSettingsErrorMessage = '';
    }
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

  async function ensureModelLoaded() {
    if (modelReady) return;
    status = 'loading-model';
    responseMessage = '';
    const payload = await loadModel();
    modelReady = true;
    modelDevice = payload.device ?? null;
    responseMessage = payload.message || UI_TEXT.modelLoadedSuccess;
    status = 'idle';
  }

  async function handleLoadModel() {
    errorMessage = '';
    try {
      await ensureModelLoaded();
    } catch (error) {
      status = 'error';
      errorMessage = error instanceof Error ? error.message : UI_TEXT.loadModelFailed;
    }
  }

  async function handleUnloadModel() {
    errorMessage = '';
    status = 'unloading-model';
    try {
      const payload = await unloadModel();
      modelReady = false;
      modelDevice = payload.device ?? null;
      responseMessage = payload.message || UI_TEXT.modelUnloadedSuccess;
      resetAudioPreview();
      lastRequest = null;
      status = 'idle';
    } catch (error) {
      status = 'error';
      modelDevice = null;
      errorMessage = error instanceof Error ? error.message : UI_TEXT.unloadModelFailed;
    }
  }

  async function handleSynthesize(event?: SubmitEvent) {
    event?.preventDefault();

    if (mode === 'clone') {
      await handleClone();
      return;
    }

    const trimmedText = inputText.trim();
    if (!trimmedText) {
      status = 'error';
      errorMessage = UI_TEXT.enterTextError;
      responseMessage = '';
      resetAudioPreview();
      lastRequest = null;
      return;
    }

    errorMessage = '';
    responseMessage = '';
    resetAudioPreview();
    lastRequest = null;

    try {
      await ensureModelLoaded();
      status = 'synthesizing';
      const payload = await synthesizeAudio({
        text: trimmedText,
        lang,
        speed,
        num_step: numStep,
        instruct
      });
      audioUrl = payload.audio_url;
      responseMessage = payload.message || UI_TEXT.synthesisComplete;
      lastRequest = {
        mode: 'synthesize',
        text: trimmedText,
        langLabel: LANGUAGES.find((o) => o.value === lang)?.label ?? 'Unknown',
        speed,
        numStep,
        instruct
      };
      status = 'success';
    } catch (error) {
      status = 'error';
      errorMessage = error instanceof Error ? error.message : UI_TEXT.synthesizeFailed;
    }
  }

  async function handleClone() {
    const trimmedText = cloneInputText.trim();
    if (!trimmedText) {
      status = 'error';
      errorMessage = UI_TEXT.enterTextError;
      responseMessage = '';
      resetAudioPreview();
      lastRequest = null;
      return;
    }

    if (!selectedCloneSetting) {
      status = 'error';
      errorMessage = UI_TEXT.selectCloneSettingError;
      responseMessage = '';
      resetAudioPreview();
      lastRequest = null;
      return;
    }

    const activeCloneSetting = selectedCloneSetting;
    errorMessage = '';
    responseMessage = '';
    cloneSettingsErrorMessage = '';
    cloneSettingsMessage = '';
    resetAudioPreview();
    lastRequest = null;

    try {
      await ensureModelLoaded();
      status = 'cloning';
      const payload = await cloneAudio({
        text: trimmedText,
        settingId: activeCloneSetting.id,
        lang: cloneLang,
        speed: cloneSpeed,
        numStep: cloneNumStep
      });
      audioUrl = payload.audio_url;
      responseMessage = payload.message || UI_TEXT.cloneComplete;
      lastRequest = {
        mode: 'clone',
        text: trimmedText,
        langLabel: LANGUAGES.find((o) => o.value === cloneLang)?.label ?? 'Unknown',
        speed: cloneSpeed,
        numStep: cloneNumStep,
        refText: activeCloneSetting.ref_text,
        refAudioName: activeCloneSetting.name
      };
      status = 'success';
    } catch (error) {
      status = 'error';
      errorMessage = error instanceof Error ? error.message : UI_TEXT.cloneFailed;
    }
  }

  function handleRefAudioChange(event: Event) {
    const input = event.currentTarget as HTMLInputElement;
    resetCloneRefAudioPreview();
    cloneRefAudioFile = input.files?.[0] ?? null;
    cloneRefAudioIsMicrophoneRecording = false;
    cloneRefAudioPreviewUrl = cloneRefAudioFile ? URL.createObjectURL(cloneRefAudioFile) : '';
    setMicrophoneStatus('');
  }

  async function refreshSavedCloneSettings() {
    isCloneSettingsLoading = true;
    cloneSettingsErrorMessage = '';
    try {
      savedCloneSettings = await listSavedCloneSettings();
      if (selectedCloneSettingId !== null) {
        const nextSelectedSetting =
          savedCloneSettings.find((s) => s.id === selectedCloneSettingId) ?? null;
        selectedCloneSetting = nextSelectedSetting;
        if (nextSelectedSetting === null && cloneView === 'selected') {
          cloneView = 'list';
        }
      }
      hasLoadedCloneSettings = true;
    } catch (error) {
      cloneSettingsErrorMessage =
        error instanceof Error ? error.message : UI_TEXT.savedCloneSettingsFailed;
    } finally {
      hasLoadedCloneSettings = true;
      isCloneSettingsLoading = false;
    }
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
      await refreshSavedCloneSettings();
      if (typeof payload.id === 'number') {
        await handleSelectSavedCloneSetting(payload.id);
      }
      mode = 'clone';
      isVoiceSheetOpen = false;
    } catch (error) {
      cloneSettingsErrorMessage =
        error instanceof Error ? error.message : UI_TEXT.saveCloneSettingFailed;
    } finally {
      isSavingCloneSetting = false;
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
      cloneView = 'selected';
    } catch (error) {
      cloneSettingsErrorMessage =
        error instanceof Error ? error.message : UI_TEXT.savedCloneSettingsFailed;
    } finally {
      isLoadingSelectedCloneSetting = false;
    }
  }

  function resetCloneSettingForm() {
    cloneSettingName = DEFAULT_FORM_STATE.cloneSettingName;
    cloneRefText = DEFAULT_FORM_STATE.cloneRefText;
    cloneLang = DEFAULT_FORM_STATE.cloneLang;
    cloneSpeed = DEFAULT_FORM_STATE.cloneSpeed;
    cloneNumStep = DEFAULT_FORM_STATE.cloneNumStep;
  }

  function handleSelectVoice(settingId: number) {
    void handleSelectSavedCloneSetting(settingId).then(() => {
      mode = 'clone';
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
      savedCloneSettings = savedCloneSettings.map((s) =>
        s.id === activeCloneSetting.id
          ? { ...s, name: trimmedName, lang: cloneLang, speed: cloneSpeed, num_step: cloneNumStep }
          : s
      );
      cloneSettingsMessage = UI_TEXT.cloneSettingUpdatedSuccess;
    } catch (error) {
      cloneSettingsErrorMessage =
        error instanceof Error ? error.message : UI_TEXT.updateCloneSettingFailed;
    } finally {
      isUpdatingCloneSetting = false;
    }
  }

  async function handleDeleteSelectedCloneSetting() {
    if (!selectedCloneSetting) return;
    await handleDeleteSavedCloneSetting(selectedCloneSetting.id);
  }

  async function handleDeleteSavedCloneSetting(settingId: number) {
    const settingToDelete = savedCloneSettings.find((s) => s.id === settingId) ?? null;
    if (!settingToDelete) return;
    if (!window.confirm(UI_TEXT.deleteCloneSettingConfirm)) return;

    isDeletingCloneSetting = true;
    cloneSettingsErrorMessage = '';
    cloneSettingsMessage = '';
    try {
      await deleteCloneSetting(settingToDelete.id);
      savedCloneSettings = savedCloneSettings.filter((s) => s.id !== settingToDelete.id);
      if (selectedCloneSettingId === settingToDelete.id) {
        selectedCloneSettingId = null;
        selectedCloneSetting = null;
        cloneView = 'list';
        mode = 'synthesize';
        resetCloneSettingForm();
        clearCloneRefAudioSelection();
        setMicrophoneStatus('');
      }
      cloneSettingsMessage = UI_TEXT.cloneSettingDeletedSuccess;
      cloneView = 'list';
    } catch (error) {
      cloneSettingsErrorMessage =
        error instanceof Error ? error.message : UI_TEXT.deleteCloneSettingFailed;
    } finally {
      isDeletingCloneSetting = false;
    }
  }
</script>

<svelte:head>
  <title>{PAGE_TITLE}</title>
  <meta name="description" content={PAGE_DESCRIPTION} />
</svelte:head>

<TtsDashboard
  bind:mode
  bind:synthesizeInputText={inputText}
  bind:cloneInputText
  {status}
  {modelReady}
  {modelDevice}
  {isBusy}
  {audioUrl}
  {errorMessage}
  {responseMessage}
  {lastRequest}
  {canSubmit}
  onLoadModel={handleLoadModel}
  onUnloadModel={handleUnloadModel}
  onSubmit={handleSynthesize}
  bind:synthesizeLang={lang}
  bind:synthesizeSpeed={speed}
  bind:synthesizeNumStep={numStep}
  bind:selectedGender
  bind:selectedAccent
  bind:selectedPitch
  bind:selectedAge
  bind:selectedStyle
  {instruct}
  {cloneView}
  {isRecordMode}
  bind:isVoiceSheetOpen
  bind:cloneLang
  bind:cloneSpeed
  bind:cloneNumStep
  bind:cloneSettingName
  bind:cloneRefText
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
  {savedCloneSettings}
  {selectedCloneSettingId}
  {selectedCloneSetting}
  {isCloneSettingsLoading}
  {hasLoadedCloneSettings}
  {isSavingCloneSetting}
  {isUpdatingCloneSetting}
  {isDeletingCloneSetting}
  {canSaveCloneSetting}
  {canUpdateCloneSetting}
  {canDeleteCloneSetting}
  {cloneSettingsMessage}
  {cloneSettingsErrorMessage}
  onSelectVoice={handleSelectVoice}
  onStartAddUpload={handleStartAddUpload}
  onStartAddRecord={handleStartAddRecord}
  onStartEditVoice={handleStartEditVoice}
  onSaveCloneSetting={handleSaveCloneSetting}
  onUpdateCloneSetting={handleUpdateSelectedCloneSetting}
  onDeleteVoice={handleDeleteSavedCloneSetting}
  onDeleteSelectedVoice={handleDeleteSelectedCloneSetting}
  onBackToList={handleBackToList}
  onRefreshVoices={refreshSavedCloneSettings}
  onToggleRecording={handleToggleCloneRefRecording}
  onRefAudioChange={handleRefAudioChange}
/>
