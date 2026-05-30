import { json } from '@sveltejs/kit';

export const prerender = true;

const SAMPLE_RATE = 16_000;
const DURATION_SECONDS = 0.4;
const SAMPLE_COUNT = Math.floor(SAMPLE_RATE * DURATION_SECONDS);
const MOCK_AUDIO_URL = createMockAudioUrl();

function writeString(view: DataView, offset: number, value: string) {
	for (let index = 0; index < value.length; index += 1) {
		view.setUint8(offset + index, value.charCodeAt(index));
	}
}

function createMockAudioUrl() {
	const bytesPerSample = 2;
	const dataSize = SAMPLE_COUNT * bytesPerSample;
	const buffer = new ArrayBuffer(44 + dataSize);
	const view = new DataView(buffer);

	writeString(view, 0, 'RIFF');
	view.setUint32(4, 36 + dataSize, true);
	writeString(view, 8, 'WAVE');
	writeString(view, 12, 'fmt ');
	view.setUint32(16, 16, true);
	view.setUint16(20, 1, true);
	view.setUint16(22, 1, true);
	view.setUint32(24, SAMPLE_RATE, true);
	view.setUint32(28, SAMPLE_RATE * bytesPerSample, true);
	view.setUint16(32, bytesPerSample, true);
	view.setUint16(34, 16, true);
	writeString(view, 36, 'data');
	view.setUint32(40, dataSize, true);

	for (let index = 0; index < SAMPLE_COUNT; index += 1) {
		const time = index / SAMPLE_RATE;
		const attack = Math.min(index / (SAMPLE_RATE * 0.03), 1);
		const release = Math.min((SAMPLE_COUNT - index) / (SAMPLE_RATE * 0.08), 1);
		const envelope = Math.max(0, Math.min(attack, release));
		const sample = Math.sin(2 * Math.PI * 440 * time) * 0.18 * envelope;

		view.setInt16(44 + index * bytesPerSample, Math.round(sample * 0x7fff), true);
	}

	return `data:audio/wav;base64,${Buffer.from(new Uint8Array(buffer)).toString('base64')}`;
}

export function GET() {
	return json({
		audioUrl: MOCK_AUDIO_URL,
		message:
			'Mock audio preview ready. The endpoint returns a canned WAV file so the UI flow can be built and tested before real synthesis is added.',
		durationMs: Math.round(DURATION_SECONDS * 1000)
	});
}
