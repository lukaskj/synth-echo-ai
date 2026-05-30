import { getApiBaseUrl, getApiEndpoints, readErrorText, toBackendAssetUrl } from './helpers';
import type {
	ApiMessageResponse,
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
	return response.blob();
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
	return response.blob();
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
