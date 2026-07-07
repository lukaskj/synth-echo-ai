from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SynthesisRequest:
    text: str
    speed: float
    lang: str
    instruct: str
    num_step: int


@dataclass(frozen=True, slots=True)
class CloneRequest:
    text: str
    ref_audio_path: str
    ref_text: str
    speed: float
    lang: str
    num_step: int


@dataclass(frozen=True, slots=True)
class CloneSettingCreateRequest:
    name: str
    ref_text: str
    speed: float
    lang: str
    num_step: int
    is_microphone_recording: bool


@dataclass(frozen=True, slots=True)
class CloneSettingUpdateRequest:
    name: str | None = None
    ref_text: str | None = None
    speed: float | None = None
    lang: str | None = None
    num_step: int | None = None


@dataclass(frozen=True, slots=True)
class CloneSetting:
    id: int
    name: str
    ref_audio_path: str
    ref_text: str
    lang: str
    speed: float
    num_step: int
    is_microphone_recording: bool
    created_at: str


@dataclass(frozen=True, slots=True)
class ConversationLineUpsertRequest:
    position: int
    text: str
    voice_type: str
    clone_setting_id: int | None
    voice_label: str
    audio_url: str
    lang: str
    speed: float
    num_step: int
    instruct: str
    selected_gender: str
    selected_accent: str
    selected_pitch: str
    selected_age: str
    selected_style: str


@dataclass(frozen=True, slots=True)
class ConversationUpsertRequest:
    name: str
    lines: tuple[ConversationLineUpsertRequest, ...]


@dataclass(frozen=True, slots=True)
class ConversationLine:
    id: int
    conversation_id: int
    position: int
    text: str
    voice_type: str
    clone_setting_id: int | None
    voice_label: str
    audio_url: str
    lang: str
    speed: float
    num_step: int
    instruct: str
    selected_gender: str
    selected_accent: str
    selected_pitch: str
    selected_age: str
    selected_style: str
    created_at: str
    updated_at: str


@dataclass(frozen=True, slots=True)
class Conversation:
    id: int
    name: str
    lines: tuple[ConversationLine, ...]
    created_at: str
    updated_at: str
