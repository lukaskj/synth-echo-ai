// See https://svelte.dev/docs/kit/types#app.d.ts
// for information about these interfaces
declare global {
	interface Window {
		SpeechRecognition?: import('$lib/tts/types').SpeechRecognitionConstructor;
		webkitSpeechRecognition?: import('$lib/tts/types').SpeechRecognitionConstructor;
	}

	namespace App {
		// interface Error {}
		// interface Locals {}
		// interface PageData {}
		// interface PageState {}
		// interface Platform {}
	}
}

export {};
