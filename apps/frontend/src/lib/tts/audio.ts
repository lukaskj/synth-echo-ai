import type {
  SpeechRecognitionConstructor,
  SpeechRecognitionErrorEvent,
  SpeechRecognitionEvent,
  SpeechRecognitionInstance
} from './types';

export function formatElapsedTime(value: number) {
  const totalSeconds = Math.max(0, Math.floor(value / 1000));
  const minutes = Math.floor(totalSeconds / 60)
    .toString()
    .padStart(2, '0');
  const seconds = (totalSeconds % 60).toString().padStart(2, '0');
  return `${minutes}:${seconds}`;
}

export function getSpeechRecognitionConstructor(): SpeechRecognitionConstructor | null {
  if (typeof window === 'undefined') {
    return null;
  }

  return window.SpeechRecognition ?? window.webkitSpeechRecognition ?? null;
}

export function getSpeechRecognitionLocale(language: string) {
  const locales: Record<string, string> = {
    en: 'en-US',
    zh: 'zh-CN',
    ja: 'ja-JP',
    pt: 'pt-BR',
    es: 'es-ES',
    fr: 'fr-FR',
    de: 'de-DE',
    it: 'it-IT',
    ru: 'ru-RU'
  };

  return locales[language] ?? language;
}

export function getPreferredRecordingMimeType() {
  if (typeof MediaRecorder === 'undefined') {
    return '';
  }

  const preferredTypes = [
    'audio/wav',
    'audio/ogg;codecs=opus',
    'audio/ogg',
    'audio/webm;codecs=opus',
    'audio/webm'
  ];
  return preferredTypes.find((type) => MediaRecorder.isTypeSupported(type)) ?? '';
}

export function getRecordedFileExtension(mimeType: string) {
  if (mimeType.includes('wav') || mimeType.includes('wave')) {
    return 'wav';
  }

  if (mimeType.includes('ogg')) {
    return 'ogg';
  }

  if (mimeType.includes('mp4')) {
    return 'm4a';
  }

  return 'webm';
}

export function buildTranscriptFromEvent(event: SpeechRecognitionEvent) {
  const segments: string[] = [];
  for (let index = 0; index < event.results.length; index += 1) {
    const result = event.results[index];
    const transcript = result?.[0]?.transcript?.trim();
    if (transcript) {
      segments.push(transcript);
    }
  }
  return segments.join(' ').trim();
}

function mixAudioBufferToMono(audioBuffer: AudioBuffer) {
  const monoSamples = new Float32Array(audioBuffer.length);
  for (let channelIndex = 0; channelIndex < audioBuffer.numberOfChannels; channelIndex += 1) {
    const channelSamples = audioBuffer.getChannelData(channelIndex);
    for (let sampleIndex = 0; sampleIndex < channelSamples.length; sampleIndex += 1) {
      monoSamples[sampleIndex] += channelSamples[sampleIndex] / audioBuffer.numberOfChannels;
    }
  }
  return monoSamples;
}

function encodeMono16BitPcmWav(samples: Float32Array, sampleRate: number) {
  const bytesPerSample = 2;
  const dataLength = samples.length * bytesPerSample;
  const buffer = new ArrayBuffer(44 + dataLength);
  const view = new DataView(buffer);

  view.setUint32(0, 0x52494646, false);
  view.setUint32(4, 36 + dataLength, true);
  view.setUint32(8, 0x57415645, false);
  view.setUint32(12, 0x666d7420, false);
  view.setUint32(16, 16, true);
  view.setUint16(20, 1, true);
  view.setUint16(22, 1, true);
  view.setUint32(24, sampleRate, true);
  view.setUint32(28, sampleRate * bytesPerSample, true);
  view.setUint16(32, bytesPerSample, true);
  view.setUint16(34, 16, true);
  view.setUint32(36, 0x64617461, false);
  view.setUint32(40, dataLength, true);

  let offset = 44;
  for (let index = 0; index < samples.length; index += 1) {
    const sample = Math.max(-1, Math.min(1, samples[index]));
    view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7fff, true);
    offset += bytesPerSample;
  }

  return buffer;
}

export async function convertRecordedBlobToWav(blob: Blob) {
  if (blob.type === 'audio/wav') {
    return blob;
  }

  if (typeof window === 'undefined') {
    throw new Error('Audio conversion is only available in the browser.');
  }

  const AudioContextConstructor =
    window.AudioContext ??
    (window as Window & { webkitAudioContext?: typeof AudioContext }).webkitAudioContext;
  if (!AudioContextConstructor) {
    throw new Error('AudioContext is not available.');
  }

  const audioContext = new AudioContextConstructor();
  try {
    const arrayBuffer = await blob.arrayBuffer();
    const audioBuffer = await audioContext.decodeAudioData(arrayBuffer.slice(0));
    const monoSamples = mixAudioBufferToMono(audioBuffer);
    const wavBuffer = encodeMono16BitPcmWav(monoSamples, audioBuffer.sampleRate);
    return new Blob([wavBuffer], { type: 'audio/wav' });
  } finally {
    await audioContext.close().catch(() => undefined);
  }
}

export function startSpeechRecognitionSession(options: {
  lang: string;
  onResult: (event: SpeechRecognitionEvent) => void;
  onError: (event: SpeechRecognitionErrorEvent) => void;
}): SpeechRecognitionInstance | null {
  const Recognition = getSpeechRecognitionConstructor();
  if (!Recognition) {
    return null;
  }

  const recognition = new Recognition();
  recognition.continuous = true;
  recognition.interimResults = true;
  recognition.lang = options.lang;
  recognition.onresult = options.onResult;
  recognition.onerror = options.onError;
  recognition.start();
  return recognition;
}
