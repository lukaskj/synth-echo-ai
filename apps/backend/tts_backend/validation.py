from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .constants import (
    CONVERSATION_VOICE_TYPES,
    DEFAULT_INSTRUCT,
    DEFAULT_LANG,
    DEFAULT_NUM_STEP,
    DEFAULT_SPEED,
    SUPPORTED_LANGUAGES,
)
from .schemas import (
    CloneRequest,
    CloneSettingCreateRequest,
    CloneSettingUpdateRequest,
    ConversationLineUpsertRequest,
    ConversationUpsertRequest,
    SynthesisRequest,
)


class RequestValidationError(ValueError):
    pass


def parse_synthesis_request(payload: dict[str, Any]) -> SynthesisRequest:
    text = _parse_required_string(payload.get("text"), "`text`")
    speed = _parse_positive_float(payload.get("speed", DEFAULT_SPEED), "`speed`", DEFAULT_SPEED)
    lang = _parse_lang(payload.get("lang", DEFAULT_LANG))

    instruct = payload.get("instruct", DEFAULT_INSTRUCT)
    if instruct is None:
        instruct = DEFAULT_INSTRUCT
    if not isinstance(instruct, str):
        raise RequestValidationError("`instruct` must be a string.")

    num_step = _parse_positive_int(payload.get("num_step", DEFAULT_NUM_STEP), "`num_step`", DEFAULT_NUM_STEP)

    return SynthesisRequest(
        text=text,
        speed=speed,
        lang=lang,
        instruct=instruct.strip(),
        num_step=num_step,
    )


def parse_clone_request(payload: Mapping[str, Any], ref_audio_path: str) -> CloneRequest:
    text = _parse_required_string(payload.get("text"), "`text`")
    ref_text = _parse_required_string(payload.get("ref_text"), "`ref_text`")
    speed = _parse_positive_float(payload.get("speed", DEFAULT_SPEED), "`speed`", DEFAULT_SPEED)
    lang = _parse_lang(payload.get("lang", DEFAULT_LANG))
    num_step = _parse_positive_int(payload.get("num_step", DEFAULT_NUM_STEP), "`num_step`", DEFAULT_NUM_STEP)

    return CloneRequest(
        text=text,
        ref_audio_path=ref_audio_path,
        ref_text=ref_text,
        speed=speed,
        lang=lang,
        num_step=num_step,
    )


def parse_clone_setting_create_request(
    payload: Mapping[str, Any],
    *,
    is_microphone_recording: bool = False,
) -> CloneSettingCreateRequest:
    name = _parse_required_string(payload.get("name"), "`name`")
    ref_text = _parse_required_string(payload.get("ref_text"), "`ref_text`")
    speed = _parse_positive_float(payload.get("speed", DEFAULT_SPEED), "`speed`", DEFAULT_SPEED)
    lang = _parse_lang(payload.get("lang", DEFAULT_LANG))
    num_step = _parse_positive_int(payload.get("num_step", DEFAULT_NUM_STEP), "`num_step`", DEFAULT_NUM_STEP)
    return CloneSettingCreateRequest(
        name=name,
        ref_text=ref_text,
        speed=speed,
        lang=lang,
        num_step=num_step,
        is_microphone_recording=is_microphone_recording,
    )


def parse_clone_setting_update_request(payload: Mapping[str, Any]) -> CloneSettingUpdateRequest:
    name = _parse_optional_string(payload.get("name"), "`name`")
    ref_text = _parse_optional_string(payload.get("ref_text"), "`ref_text`")
    speed = _parse_optional_positive_float(payload.get("speed"), "`speed`")
    lang = _parse_optional_lang(payload.get("lang"))
    num_step = _parse_optional_positive_int(payload.get("num_step"), "`num_step`")

    return CloneSettingUpdateRequest(
        name=name,
        ref_text=ref_text,
        speed=speed,
        lang=lang,
        num_step=num_step,
    )


def parse_conversation_request(payload: Mapping[str, Any]) -> ConversationUpsertRequest:
    name = _parse_required_string(payload.get("name"), "`name`")
    raw_lines = payload.get("lines", [])

    if not isinstance(raw_lines, list):
        raise RequestValidationError("`lines` must be an array.")

    lines = tuple(_parse_conversation_line_request(line, index) for index, line in enumerate(raw_lines))
    return ConversationUpsertRequest(name=name, lines=lines)


def _parse_conversation_line_request(payload: Any, default_position: int) -> ConversationLineUpsertRequest:
    if not isinstance(payload, Mapping):
        raise RequestValidationError("Each conversation line must be an object.")

    position = _parse_non_negative_int(payload.get("position"), "`position`", default_position)
    voice_type = _parse_conversation_voice_type(payload.get("voice_type", "instruction"))
    clone_setting_id = _parse_optional_positive_int(payload.get("clone_setting_id"), "`clone_setting_id`")
    text = _parse_flexible_string(payload.get("text"), "`text`")
    voice_label = _parse_flexible_string(
        payload.get("voice_label"),
        "`voice_label`",
        default="Saved voice" if voice_type == "clone" else "Instruction voice",
    )
    audio_url = _parse_flexible_string(payload.get("audio_url"), "`audio_url`")
    lang = _parse_lang(payload.get("lang", DEFAULT_LANG))
    speed = _parse_positive_float(payload.get("speed", DEFAULT_SPEED), "`speed`", DEFAULT_SPEED)
    num_step = _parse_positive_int(payload.get("num_step", DEFAULT_NUM_STEP), "`num_step`", DEFAULT_NUM_STEP)
    instruct = _parse_flexible_string(payload.get("instruct"), "`instruct`")
    selected_gender = _parse_flexible_string(payload.get("selected_gender"), "`selected_gender`")
    selected_accent = _parse_flexible_string(payload.get("selected_accent"), "`selected_accent`")
    selected_pitch = _parse_flexible_string(payload.get("selected_pitch"), "`selected_pitch`")
    selected_age = _parse_flexible_string(payload.get("selected_age"), "`selected_age`")
    selected_style = _parse_flexible_string(payload.get("selected_style"), "`selected_style`")

    return ConversationLineUpsertRequest(
        position=position,
        text=text,
        voice_type=voice_type,
        clone_setting_id=clone_setting_id,
        voice_label=voice_label,
        audio_url=audio_url,
        lang=lang,
        speed=speed,
        num_step=num_step,
        instruct=instruct,
        selected_gender=selected_gender,
        selected_accent=selected_accent,
        selected_pitch=selected_pitch,
        selected_age=selected_age,
        selected_style=selected_style,
    )


def _parse_required_string(value: Any, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RequestValidationError(f"{field_name} is required and must be a non-empty string.")
    return value.strip()


def _parse_optional_string(value: Any, field_name: str) -> str | None:
    if value is None or value == "":
        return None

    if not isinstance(value, str) or not value.strip():
        raise RequestValidationError(f"{field_name} must be a non-empty string.")

    return value.strip()


def _parse_flexible_string(value: Any, field_name: str, *, default: str = "") -> str:
    if value is None:
        return default

    if not isinstance(value, str):
        raise RequestValidationError(f"{field_name} must be a string.")

    return value.strip()


def _parse_positive_float(value: Any, field_name: str, default: float) -> float:
    if value in (None, ""):
        return default

    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError as exc:
            raise RequestValidationError(f"{field_name} must be a positive number.") from exc

    if isinstance(value, bool) or not isinstance(value, (int, float)) or value <= 0:
        raise RequestValidationError(f"{field_name} must be a positive number.")

    return float(value)


def _parse_optional_positive_float(value: Any, field_name: str) -> float | None:
    if value in (None, ""):
        return None

    return _parse_positive_float(value, field_name, DEFAULT_SPEED)


def _parse_non_negative_int(value: Any, field_name: str, default: int) -> int:
    if value in (None, ""):
        return default

    if isinstance(value, str):
        try:
            value = int(value)
        except ValueError as exc:
            raise RequestValidationError(f"{field_name} must be a non-negative integer.") from exc

    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise RequestValidationError(f"{field_name} must be a non-negative integer.")

    return value


def _parse_lang(value: Any) -> str:
    if value in (None, ""):
        return DEFAULT_LANG

    if not isinstance(value, str):
        supported = ", ".join(sorted(SUPPORTED_LANGUAGES))
        raise RequestValidationError(f"`lang` must be one of: {supported}.")

    lang = value.strip()
    if lang not in SUPPORTED_LANGUAGES:
        supported = ", ".join(sorted(SUPPORTED_LANGUAGES))
        raise RequestValidationError(f"`lang` must be one of: {supported}.")

    return lang


def _parse_optional_lang(value: Any) -> str | None:
    if value in (None, ""):
        return None

    return _parse_lang(value)


def _parse_positive_int(value: Any, field_name: str, default: int) -> int:
    if value in (None, ""):
        return default

    if isinstance(value, str):
        try:
            value = int(value)
        except ValueError as exc:
            raise RequestValidationError(f"{field_name} must be a positive integer.") from exc

    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise RequestValidationError(f"{field_name} must be a positive integer.")

    return value


def _parse_optional_positive_int(value: Any, field_name: str) -> int | None:
    if value in (None, ""):
        return None

    return _parse_positive_int(value, field_name, DEFAULT_NUM_STEP)


def _parse_conversation_voice_type(value: Any) -> str:
    if not isinstance(value, str):
        supported = ", ".join(sorted(CONVERSATION_VOICE_TYPES))
        raise RequestValidationError(f"`voice_type` must be one of: {supported}.")

    voice_type = value.strip()
    if voice_type not in CONVERSATION_VOICE_TYPES:
        supported = ", ".join(sorted(CONVERSATION_VOICE_TYPES))
        raise RequestValidationError(f"`voice_type` must be one of: {supported}.")

    return voice_type
