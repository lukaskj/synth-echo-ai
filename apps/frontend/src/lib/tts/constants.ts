import type {
  LanguageOption,
  RequestStatus,
  TtsFormState,
  TtsMode,
  VoiceCategoryOption
} from './types';

export const PAGE_TITLE = 'SynthEcho AI';
export const PAGE_DESCRIPTION = 'Generate speech with a Flask-backed OmniVoice synthesis workflow.';

export const DEFAULT_BACKEND_BASE_URL = 'http://127.0.0.1:5000';

export const API_PATHS = {
  load: '/api/v1/load',
  unload: '/api/v1/unload',
  synthesize: '/api/v1/synthesize',
  clone: '/api/v1/clone',
  saveCloneSetting: '/api/v1/settings/save-clone',
  saveCloneRecordingSetting: '/api/v1/settings/save-clone-recording',
  getCloneSettings: '/api/v1/settings/get-clones',
  getCloneSettingBase: '/api/v1/settings/get-clone',
  updateCloneSettingBase: '/api/v1/settings/update-clone',
  deleteCloneSettingBase: '/api/v1/settings/delete-clone'
} as const;

export const DEFAULT_FORM_STATE: TtsFormState = {
  inputText: '',
  cloneInputText: '',
  cloneSettingName: '',
  cloneRefText: '',
  lang: 'en',
  speed: 1.0,
  numStep: 32,
  cloneLang: 'en',
  cloneSpeed: 1.0,
  cloneNumStep: 32,
  selectedGender: 'male',
  selectedAccent: '',
  selectedPitch: '',
  selectedAge: '',
  selectedStyle: ''
};

export const REQUEST_STATUS_LABELS: Record<RequestStatus, string> = {
  idle: 'Ready',
  'loading-model': 'Loading model',
  'unloading-model': 'Releasing model',
  synthesizing: 'Synthesizing audio',
  cloning: 'Cloning voice',
  success: 'Audio ready',
  error: 'Request failed'
};

export const MODE_OPTIONS: { value: TtsMode; label: string; description: string }[] = [
  {
    value: 'synthesize',
    label: 'Text to speech',
    description: 'Generate a voice from text and instruct settings.'
  },
  {
    value: 'clone',
    label: 'Voice cloning',
    description: 'Generate speech from a reference voice sample.'
  }
];

export const LANGUAGES: LanguageOption[] = [
  { value: 'en', label: 'English' },
  { value: 'zh', label: 'Chinese' },
  { value: 'ja', label: 'Japanese' },
  { value: 'pt', label: 'Portuguese' },
  { value: 'es', label: 'Spanish' },
  { value: 'fr', label: 'French' },
  { value: 'de', label: 'German' },
  { value: 'it', label: 'Italian' },
  { value: 'ru', label: 'Russian' }
];

export const GENDER_OPTIONS: VoiceCategoryOption[] = [
  { value: '', label: 'Any', description: 'Leave gender unspecified.' },
  { value: 'female', label: 'Female', description: 'Use a female voice instruction.' },
  { value: 'male', label: 'Male', description: 'Use a male voice instruction.' }
];

export const ACCENT_OPTIONS: VoiceCategoryOption[] = [
  { value: '', label: 'Any', description: 'Do not bias toward an accent.' },
  { value: 'american accent', label: 'American', description: 'American accent' },
  { value: 'australian accent', label: 'Australian', description: 'Australian accent' },
  { value: 'british accent', label: 'British', description: 'British accent' },
  { value: 'canadian accent', label: 'Canadian', description: 'Canadian accent' },
  { value: 'chinese accent', label: 'Chinese', description: 'Chinese accent' },
  { value: 'indian accent', label: 'Indian', description: 'Indian accent' },
  { value: 'japanese accent', label: 'Japanese', description: 'Japanese accent' },
  { value: 'korean accent', label: 'Korean', description: 'Korean accent' },
  { value: 'portuguese accent', label: 'Portuguese', description: 'Portuguese accent' },
  { value: 'russian accent', label: 'Russian', description: 'Russian accent' }
];

export const PITCH_OPTIONS: VoiceCategoryOption[] = [
  { value: '', label: 'Any', description: 'Use the model default pitch range.' },
  { value: 'very low pitch', label: 'Very low', description: 'Very low pitch' },
  { value: 'low pitch', label: 'Low', description: 'Low pitch' },
  { value: 'moderate pitch', label: 'Moderate', description: 'Moderate pitch' },
  { value: 'high pitch', label: 'High', description: 'High pitch' },
  { value: 'very high pitch', label: 'Very high', description: 'Very high pitch' }
];

export const AGE_OPTIONS: VoiceCategoryOption[] = [
  { value: '', label: 'Any', description: 'Leave age unspecified.' },
  { value: 'child', label: 'Child', description: 'Child voice' },
  { value: 'teenager', label: 'Teenager', description: 'Teenage voice' },
  { value: 'young adult', label: 'Young adult', description: 'Young adult voice' },
  { value: 'middle-aged', label: 'Middle-aged', description: 'Middle-aged voice' },
  { value: 'elderly', label: 'Elderly', description: 'Elderly voice' }
];

export const STYLE_OPTIONS: VoiceCategoryOption[] = [
  { value: '', label: 'Normal', description: 'No extra style instruction.' },
  { value: 'whisper', label: 'Whisper', description: 'Soft whisper delivery' }
];

export const UI_TEXT = {
  synthesisEyebrow: 'Synthesis',
  synthesisTitle: 'Text to speech',
  cloneEyebrow: 'Voice cloning',
  cloneTitle: 'Clone a voice',
  configurationsEyebrow: 'Configurations',
  settingsTitle: 'Voice settings',
  cloneSettingsTitle: 'Clone settings',
  modeLabel: 'Mode',
  scriptLabel: 'Script',
  scriptPlaceholder: 'Write the text you want to synthesize...',
  cloneScriptLabel: 'Target text',
  cloneScriptPlaceholder: 'Write the text you want the cloned voice to speak...',
  refAudioLabel: 'Reference audio',
  recordRefAudioLabel: 'Record with microphone',
  startRecording: 'Start recording',
  stopRecording: 'Stop recording',
  recordingInProgress: 'Recording',
  recordingTimerLabel: 'Elapsed time',
  microphoneTranscriptLabel: 'Detected transcript',
  microphoneNotSupported: 'This browser does not support microphone recording.',
  speechRecognitionNotSupported:
    'Speech recognition is not supported in this browser. Enter the transcript manually.',
  microphoneAccessFailed: 'Unable to access your microphone.',
  recordingFailed: 'Unable to record audio from your microphone.',
  recordingTranscriptPending: 'Listening for speech and building the transcript...',
  recordingTranscriptReady: 'Transcript captured from your recording.',
  recordingTranscriptUnavailable: 'No transcript was captured. Enter the reference text manually.',
  microphoneRecordingBadge: 'Microphone recording',
  refTextLabel: 'Reference transcript',
  refTextPlaceholder: 'Paste the transcript that matches the uploaded reference audio...',
  cloneSettingNameLabel: 'Setting name',
  cloneSettingNamePlaceholder: 'My Voice Clone 1',
  saveCloneSetting: 'Save',
  savingCloneSetting: 'Saving setting...',
  savedCloneSettingsTitle: 'Saved clone settings',
  savedCloneSettingsDescription: 'Select a saved voice clone.',
  savedCloneSettingsEmpty: 'No saved clone settings yet.',
  refreshCloneSettings: 'Refresh',
  refreshingCloneSettings: 'Refreshing...',
  loadingSavedCloneSetting: 'Loading...',
  cloneSettingSavedSuccess: 'Clone setting saved successfully.',
  cloneSettingNameError: 'Enter a name before saving this clone setting.',
  savedCloneSettingsFailed: 'Unable to load saved clone settings.',
  saveCloneSettingFailed: 'Unable to save this clone setting.',
  updateCloneSettingFailed: 'Unable to update this clone setting.',
  deleteCloneSettingFailed: 'Unable to delete this clone setting.',
  cloneSettingUpdatedSuccess: 'Clone setting updated successfully.',
  cloneSettingDeletedSuccess: 'Clone setting deleted successfully.',
  createCloneSetting: 'Create new setting',
  cancelCreateCloneSetting: 'Back',
  back: 'Back',
  selectedCloneSettingTitle: 'Selected setting',
  selectedCloneSettingName: 'Name',
  selectedCloneSettingUpdate: 'Update setting',
  selectedCloneSettingDelete: 'Delete setting',
  updatingCloneSetting: 'Updating...',
  deletingCloneSetting: 'Deleting...',
  deleteCloneSettingConfirm: 'Delete this saved voice cloning setting?',
  useSavedCloneSetting: 'Use saved setting',
  referenceAudioPreview: 'Reference audio preview',
  createCloneSettingTitle: 'Create new setting',
  createCloneSettingDescription: 'Save a voice clone preset.',
  statusLabel: 'Status',
  deviceLabel: 'Device',
  modelLoaded: 'loaded',
  modelNotLoaded: 'not loaded',
  modelDeviceUnknown: 'unknown',
  loadModel: 'Load model',
  unloadModel: 'Unload model',
  loadingShort: 'Loading...',
  unloadingShort: 'Unloading...',
  language: 'Language',
  speed: 'Speed',
  diffusionSteps: 'Diffusion steps',
  gender: 'Gender',
  accent: 'Accent',
  pitch: 'Pitch',
  age: 'Age',
  style: 'Style',
  currentInstruct: 'Current instruct',
  noInstruction: 'No instruction selected.',
  generateSpeech: 'Generate speech',
  cloneVoice: 'Clone voice',
  synthesizing: 'Synthesizing...',
  cloning: 'Cloning...',
  generatedAudioTitle: 'Generated audio',
  generatedAudioDescription: 'Preview the generated clip.',
  generatingAudio: 'Generating audio...',
  inProgress: 'In progress',
  synthesisFailedTitle: 'Synthesis failed',
  noAudioYet: 'No audio generated yet. Load the model or submit text to start synthesis.',
  resultLanguage: 'Language',
  resultSpeed: 'Speed',
  resultSteps: 'Steps',
  resultMode: 'Mode',
  resultReferenceAudio: 'Reference audio',
  resultReferenceText: 'Reference text',
  synthesisComplete: 'Synthesis complete. Your generated audio is ready to preview.',
  cloneComplete: 'Voice cloning complete. Your generated audio is ready to preview.',
  modelLoadedSuccess: 'Model loaded successfully.',
  modelUnloadedSuccess: 'Model unloaded successfully.',
  enterTextError: 'Enter some text before generating audio.',
  enterReferenceTextError: 'Enter the transcript for the reference audio.',
  uploadReferenceAudioError: 'Upload a reference audio file before cloning.',
  selectCloneSettingError: 'Select a saved clone setting or create a new one first.',
  emptyErrorResponse: 'The server returned an empty error response.',
  genericRequestFailed: 'The request failed.',
  loadModelFailed: 'Failed to load the model.',
  unloadModelFailed: 'Failed to unload the model.',
  synthesizeFailed: 'Something went wrong while synthesizing the audio.',
  cloneFailed: 'Something went wrong while cloning the voice.'
} as const;
