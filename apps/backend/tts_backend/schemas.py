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
