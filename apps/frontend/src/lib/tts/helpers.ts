import { API_PATHS, DEFAULT_BACKEND_BASE_URL, UI_TEXT } from './constants';
import type { ApiMessageResponse } from './types';

export function getApiBaseUrl() {
  return (import.meta.env.PUBLIC_BACKEND_BASE_URL || DEFAULT_BACKEND_BASE_URL).replace(/\/$/, '');
}

export function getApiEndpoints(apiBaseUrl: string) {
  return {
    load: `${apiBaseUrl}${API_PATHS.load}`,
    unload: `${apiBaseUrl}${API_PATHS.unload}`,
    synthesize: `${apiBaseUrl}${API_PATHS.synthesize}`,
    clone: `${apiBaseUrl}${API_PATHS.clone}`,
    conversations: `${apiBaseUrl}${API_PATHS.conversations}`,
    getConversation: (id: number) => `${apiBaseUrl}${API_PATHS.conversations}/${id}`,
    downloadConversation: (id: number) => `${apiBaseUrl}${API_PATHS.downloadConversationBase}/${id}/download`,
    saveCloneSetting: `${apiBaseUrl}${API_PATHS.saveCloneSetting}`,
    saveCloneRecordingSetting: `${apiBaseUrl}${API_PATHS.saveCloneRecordingSetting}`,
    getCloneSettings: `${apiBaseUrl}${API_PATHS.getCloneSettings}`,
    getCloneSetting: (id: number) => `${apiBaseUrl}${API_PATHS.getCloneSettingBase}/${id}`,
    updateConversation: (id: number) => `${apiBaseUrl}${API_PATHS.updateConversationBase}/${id}`,
    deleteConversation: (id: number) => `${apiBaseUrl}${API_PATHS.deleteConversationBase}/${id}`,
    updateCloneSetting: (id: number) => `${apiBaseUrl}${API_PATHS.updateCloneSettingBase}/${id}`,
    deleteCloneSetting: (id: number) => `${apiBaseUrl}${API_PATHS.deleteCloneSettingBase}/${id}`
  };
}

export function toBackendAssetUrl(apiBaseUrl: string, assetPath: string) {
  if (!assetPath) {
    return '';
  }

  if (/^https?:\/\//.test(assetPath)) {
    return assetPath;
  }

  return `${apiBaseUrl}${assetPath.startsWith('/') ? assetPath : `/${assetPath}`}`;
}

export function toBackendRelativeAssetUrl(apiBaseUrl: string, assetPath: string) {
  if (!assetPath) {
    return '';
  }

  if (!/^https?:\/\//.test(assetPath)) {
    return assetPath;
  }

  try {
    const baseUrl = new URL(apiBaseUrl);
    const parsedUrl = new URL(assetPath);
    if (parsedUrl.origin !== baseUrl.origin) {
      return assetPath;
    }

    return `${parsedUrl.pathname}${parsedUrl.search}${parsedUrl.hash}`;
  } catch {
    return assetPath;
  }
}

export function buildInstruct(parts: string[]) {
  return parts.filter((value) => value.length > 0).join(', ');
}

export function readErrorText(body: string) {
  if (!body) {
    return UI_TEXT.emptyErrorResponse;
  }

  try {
    const parsed = JSON.parse(body) as ApiMessageResponse;
    return parsed.error || parsed.message || UI_TEXT.genericRequestFailed;
  } catch {
    return body;
  }
}

export function revokeObjectUrl(url: string) {
  if (url.startsWith('blob:')) {
    URL.revokeObjectURL(url);
  }
}
