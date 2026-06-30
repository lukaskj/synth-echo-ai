import {
  getApiBaseUrl,
  getApiEndpoints,
  readErrorText,
  toBackendAssetUrl,
  toBackendRelativeAssetUrl
} from './helpers';
import type {
  AudioGenerationResponse,
  ApiMessageResponse,
  Conversation,
  ConversationLine,
  ConversationListResponse,
  ConversationMutation,
  ConversationResponse,
  SavedCloneSetting,
  SavedCloneSettingListResponse,
  SavedCloneSettingResponse
} from './types';

const apiBaseUrl = getApiBaseUrl();
const endpoints = getApiEndpoints(apiBaseUrl);

async function postJson(endpoint: string, payload: Record<string, unknown>) {
  const response = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(payload)
  });

  if (!response.ok) {
    throw new Error(readErrorText(await response.text()));
  }

  return response;
}

async function getJson<T>(endpoint: string) {
  const response = await fetch(endpoint);

  if (!response.ok) {
    throw new Error(readErrorText(await response.text()));
  }

  return (await response.json()) as T;
}

async function postForm(endpoint: string, payload: FormData) {
  const response = await fetch(endpoint, {
    method: 'POST',
    body: payload
  });

  if (!response.ok) {
    throw new Error(readErrorText(await response.text()));
  }

  return response;
}

async function deleteRequest(endpoint: string) {
  const response = await fetch(endpoint, {
    method: 'DELETE'
  });

  if (!response.ok) {
    throw new Error(readErrorText(await response.text()));
  }

  return response;
}

function normalizeCloneSetting(setting: SavedCloneSetting): SavedCloneSetting {
  return {
    ...setting,
    ref_audio_path: toBackendAssetUrl(apiBaseUrl, setting.ref_audio_path)
  };
}

function normalizeGeneratedAudioResponse(
  payload: AudioGenerationResponse
): AudioGenerationResponse {
  return {
    ...payload,
    audio_url: toBackendAssetUrl(apiBaseUrl, payload.audio_url)
  };
}

function normalizeConversationLine(line: ConversationLine): ConversationLine {
  return {
    ...line,
    audio_url: toBackendAssetUrl(apiBaseUrl, line.audio_url)
  };
}

function normalizeConversation(conversation: Conversation): Conversation {
  return {
    ...conversation,
    lines: conversation.lines.map(normalizeConversationLine)
  };
}

function serializeConversationPayload(payload: ConversationMutation): ConversationMutation {
  return {
    ...payload,
    lines: payload.lines.map((line) => {
      const serializedLine = { ...line };
      delete serializedLine.persisted_voice_type;

      return {
        ...serializedLine,
        audio_url: toBackendRelativeAssetUrl(apiBaseUrl, line.audio_url)
      };
    })
  };
}

export async function loadModel() {
  const response = await postJson(endpoints.load, {});
  return (await response.json()) as ApiMessageResponse;
}

export async function unloadModel() {
  const response = await postJson(endpoints.unload, {});
  return (await response.json()) as ApiMessageResponse;
}

export async function synthesizeAudio(payload: {
  text: string;
  lang: string;
  speed: number;
  num_step: number;
  instruct: string;
}) {
  const response = await postJson(endpoints.synthesize, payload);
  return normalizeGeneratedAudioResponse((await response.json()) as AudioGenerationResponse);
}

export async function cloneAudio(payload: {
  text: string;
  settingId: number;
  lang: string;
  speed: number;
  numStep: number;
}) {
  const formData = new FormData();
  formData.set('text', payload.text);
  formData.set('setting_id', `${payload.settingId}`);
  formData.set('lang', payload.lang);
  formData.set('speed', `${payload.speed}`);
  formData.set('num_step', `${payload.numStep}`);

  const response = await postForm(endpoints.clone, formData);
  return normalizeGeneratedAudioResponse((await response.json()) as AudioGenerationResponse);
}

export async function listConversations() {
  const payload = await getJson<ConversationListResponse>(endpoints.conversations);
  return payload.conversations.map(normalizeConversation);
}

export async function getConversation(conversationId: number) {
  const payload = await getJson<ConversationResponse>(endpoints.getConversation(conversationId));
  return normalizeConversation(payload.conversation);
}

export async function createConversation(payload: ConversationMutation) {
  const response = await postJson(endpoints.conversations, serializeConversationPayload(payload));
  const body = (await response.json()) as ConversationResponse;
  return {
    ...body,
    conversation: normalizeConversation(body.conversation)
  };
}

export async function updateConversation(conversationId: number, payload: ConversationMutation) {
  const response = await postJson(
    endpoints.updateConversation(conversationId),
    serializeConversationPayload(payload)
  );
  const body = (await response.json()) as ConversationResponse;
  return {
    ...body,
    conversation: normalizeConversation(body.conversation)
  };
}

export async function deleteConversation(conversationId: number) {
  const response = await deleteRequest(endpoints.deleteConversation(conversationId));
  return (await response.json()) as ApiMessageResponse;
}

export async function downloadConversationAudio(conversationId: number) {
  const response = await fetch(endpoints.downloadConversation(conversationId));

  if (!response.ok) {
    throw new Error(readErrorText(await response.text()));
  }

  const blob = await response.blob();
  const contentDisposition = response.headers.get('content-disposition') || '';
  const filenameMatch = contentDisposition.match(/filename="?([^";]+)"?/i);
  const fallbackDateString = new Date()
    .toISOString()
    .slice(0, 19)
    .replace('T', '_')
    .replace(/:/g, '-');

  return {
    blob,
    filename: filenameMatch?.[1] || `conversation-${fallbackDateString}-${conversationId}.zip`
  };
}

export async function listSavedCloneSettings() {
  const payload = await getJson<SavedCloneSettingListResponse>(endpoints.getCloneSettings);
  return payload.settings.map(normalizeCloneSetting);
}

export async function getSavedCloneSetting(settingId: number) {
  const payload = await getJson<SavedCloneSettingResponse>(endpoints.getCloneSetting(settingId));
  return normalizeCloneSetting(payload.setting);
}

export async function saveCloneSetting(payload: {
  name: string;
  refText: string;
  lang: string;
  speed: number;
  numStep: number;
  refAudio: File;
  isMicrophoneRecording: boolean;
}) {
  const formData = new FormData();
  formData.set('name', payload.name);
  formData.set('ref_text', payload.refText);
  formData.set('lang', payload.lang);
  formData.set('speed', `${payload.speed}`);
  formData.set('num_step', `${payload.numStep}`);
  formData.set('ref_audio', payload.refAudio);

  const endpoint = payload.isMicrophoneRecording
    ? endpoints.saveCloneRecordingSetting
    : endpoints.saveCloneSetting;

  const response = await postForm(endpoint, formData);
  return (await response.json()) as ApiMessageResponse;
}

export async function updateCloneSetting(payload: {
  settingId: number;
  name: string;
  lang: string;
  speed: number;
  numStep: number;
}) {
  const formData = new FormData();
  formData.set('name', payload.name);
  formData.set('lang', payload.lang);
  formData.set('speed', `${payload.speed}`);
  formData.set('num_step', `${payload.numStep}`);

  const response = await postForm(endpoints.updateCloneSetting(payload.settingId), formData);
  return (await response.json()) as ApiMessageResponse;
}

export async function deleteCloneSetting(settingId: number) {
  const response = await deleteRequest(endpoints.deleteCloneSetting(settingId));
  return (await response.json()) as ApiMessageResponse;
}
