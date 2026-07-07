export type RequestStatus =
  | 'idle'
  | 'loading-model'
  | 'unloading-model'
  | 'synthesizing'
  | 'cloning'
  | 'success'
  | 'error';

export type TtsMode = 'synthesize' | 'clone';

export type VoiceSourceType = 'clone' | 'instruction';

export type ConversationVoiceType = VoiceSourceType;

export type SelectOption = {
  value: string;
  label: string;
};

export type LanguageOption = SelectOption;

export type VoiceCategoryOption = SelectOption & {
  description: string;
};

export type LastRequest = {
  mode: TtsMode;
  text: string;
  langLabel: string;
  speed: number;
  numStep: number;
  instruct?: string;
  refText?: string;
  refAudioName?: string;
};

export type ApiMessageResponse = {
  message?: string;
  error?: string;
  id?: number;
  state?: string;
  device?: string | null;
};

export type AudioGenerationResponse = ApiMessageResponse & {
  audio_url: string;
};

export type SpeechRecognitionAlternative = {
  transcript: string;
  confidence?: number;
};

export type SpeechRecognitionResult = {
  isFinal: boolean;
  readonly length: number;
  [item: number]: SpeechRecognitionAlternative;
};

export type SpeechRecognitionResultList = {
  readonly length: number;
  [item: number]: SpeechRecognitionResult;
};

export type SpeechRecognitionEvent = Event & {
  readonly resultIndex: number;
  readonly results: SpeechRecognitionResultList;
};

export type SpeechRecognitionErrorEvent = Event & {
  error: string;
  message?: string;
};

export type SpeechRecognitionInstance = EventTarget & {
  continuous: boolean;
  interimResults: boolean;
  lang: string;
  onresult: ((event: SpeechRecognitionEvent) => void) | null;
  onerror: ((event: SpeechRecognitionErrorEvent) => void) | null;
  onend: (() => void) | null;
  start: () => void;
  stop: () => void;
  abort: () => void;
};

export type SpeechRecognitionConstructor = new () => SpeechRecognitionInstance;

export type SavedCloneSetting = {
  id: number;
  name: string;
  ref_audio_path: string;
  ref_text: string;
  lang: string;
  speed: number;
  num_step: number;
  is_microphone_recording: boolean;
  created_at: string;
};

export type CloneView = 'list' | 'selected' | 'create';

export type SavedCloneSettingListResponse = {
  settings: SavedCloneSetting[];
};

export type SavedCloneSettingResponse = {
  setting: SavedCloneSetting;
};

export type ConversationLine = {
  id: number;
  conversation_id: number;
  position: number;
  text: string;
  voice_type: ConversationVoiceType;
  clone_setting_id: number | null;
  voice_label: string;
  audio_url: string;
  lang: string;
  speed: number;
  num_step: number;
  instruct: string;
  selected_gender: string;
  selected_accent: string;
  selected_pitch: string;
  selected_age: string;
  selected_style: string;
  created_at: string;
  updated_at: string;
};

export type Conversation = {
  id: number;
  name: string;
  lines: ConversationLine[];
  created_at: string;
  updated_at: string;
};

export type ConversationLineMutation = {
  position: number;
  text: string;
  voice_type: ConversationVoiceType;
  persisted_voice_type?: ConversationVoiceType;
  clone_setting_id: number | null;
  voice_label: string;
  audio_url: string;
  lang: string;
  speed: number;
  num_step: number;
  instruct: string;
  selected_gender: string;
  selected_accent: string;
  selected_pitch: string;
  selected_age: string;
  selected_style: string;
};

export type ConversationMutation = {
  name: string;
  lines: ConversationLineMutation[];
};

export type ConversationListResponse = {
  conversations: Conversation[];
};

export type ConversationResponse = ApiMessageResponse & {
  conversation: Conversation;
};

export type TtsFormState = {
  inputText: string;
  cloneInputText: string;
  cloneSettingName: string;
  cloneRefText: string;
  lang: string;
  speed: number;
  numStep: number;
  cloneLang: string;
  cloneSpeed: number;
  cloneNumStep: number;
  selectedGender: string;
  selectedAccent: string;
  selectedPitch: string;
  selectedAge: string;
  selectedStyle: string;
};
