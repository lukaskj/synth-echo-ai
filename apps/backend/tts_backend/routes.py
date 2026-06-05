from __future__ import annotations

from http import HTTPStatus
from typing import Any

from flask import Blueprint, jsonify, request, send_file

from .schemas import CloneRequest, CloneSetting, CloneSettingUpdateRequest, Conversation, ConversationLine
from .services.clone_settings_service import (
    CloneSettingNotFoundError,
    CloneSettingsService,
    CloneSettingsServiceError,
)
from .services.conversation_service import (
    ConversationNotFoundError,
    ConversationService,
    ConversationServiceError,
)
from .services.generated_audio_service import GeneratedAudioService
from .services.model_service import (
    ModelLoadInProgressError,
    ModelNotLoadedError,
    ModelService,
    UnloadResult,
)
from .storage import AudioStorage, InvalidAudioUploadError
from .validation import (
    RequestValidationError,
    parse_clone_request,
    parse_clone_setting_create_request,
    parse_clone_setting_update_request,
    parse_conversation_request,
    parse_synthesis_request,
)


def create_api_blueprint(
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    conversation_service: ConversationService,
    audio_storage: AudioStorage,
    generated_audio_service: GeneratedAudioService,
) -> Blueprint:
    api = Blueprint("api", __name__)

    _register_hello_route(api)
    _register_generated_audio_route(api, model_service, generated_audio_service)
    _register_load_model_route(api, model_service)
    _register_unload_model_route(api, model_service)
    _register_synthesize_route(api, model_service, generated_audio_service)
    _register_clone_route(api, model_service, clone_settings_service, audio_storage, generated_audio_service)
    _register_list_conversations_route(api, model_service, conversation_service)
    _register_get_conversation_route(api, model_service, conversation_service)
    _register_create_conversation_route(api, model_service, conversation_service)
    _register_update_conversation_route(api, model_service, conversation_service, generated_audio_service)
    _register_delete_conversation_route(api, model_service, conversation_service, generated_audio_service)
    _register_save_clone_setting_route(api, model_service, clone_settings_service, audio_storage)
    _register_save_clone_recording_setting_route(api, model_service, clone_settings_service, audio_storage)
    _register_get_clone_setting_routes(api, model_service, clone_settings_service)
    _register_get_clone_setting_audio_route(api, model_service, clone_settings_service, audio_storage)
    _register_update_clone_setting_route(api, model_service, clone_settings_service)
    _register_delete_clone_setting_route(api, model_service, clone_settings_service, audio_storage)
    _register_get_clone_settings_route(api, model_service, clone_settings_service)

    return api


def _register_hello_route(api: Blueprint) -> None:
    @api.get("/hello")
    def hello_world() -> str:
        return _hello_world()


def _register_generated_audio_route(
    api: Blueprint,
    model_service: ModelService,
    generated_audio_service: GeneratedAudioService,
) -> None:
    @api.get("/generated-audio/<string:filename>")
    def get_generated_audio(filename: str):
        return _get_generated_audio(model_service, generated_audio_service, filename)


def _register_load_model_route(api: Blueprint, model_service: ModelService) -> None:
    @api.post("/load")
    def load_model():
        return _load_model(model_service)


def _register_unload_model_route(api: Blueprint, model_service: ModelService) -> None:
    @api.post("/unload")
    def unload_model():
        return _unload_model(model_service)


def _register_synthesize_route(
    api: Blueprint,
    model_service: ModelService,
    generated_audio_service: GeneratedAudioService,
) -> None:
    @api.post("/synthesize")
    def synthesize_speech():
        return _synthesize_speech(model_service, generated_audio_service)


def _register_clone_route(
    api: Blueprint,
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
    generated_audio_service: GeneratedAudioService,
) -> None:
    @api.post("/clone")
    def clone_voice():
        return _clone_voice(model_service, clone_settings_service, audio_storage, generated_audio_service)


def _register_list_conversations_route(
    api: Blueprint,
    model_service: ModelService,
    conversation_service: ConversationService,
) -> None:
    @api.get("/conversations")
    def list_conversations():
        return _list_conversations(model_service, conversation_service)


def _register_get_conversation_route(
    api: Blueprint,
    model_service: ModelService,
    conversation_service: ConversationService,
) -> None:
    @api.get("/conversations/<int:conversation_id>")
    def get_conversation(conversation_id: int):
        return _get_conversation(model_service, conversation_service, conversation_id)


def _register_create_conversation_route(
    api: Blueprint,
    model_service: ModelService,
    conversation_service: ConversationService,
) -> None:
    @api.post("/conversations")
    def create_conversation():
        return _create_conversation(model_service, conversation_service)


def _register_update_conversation_route(
    api: Blueprint,
    model_service: ModelService,
    conversation_service: ConversationService,
    generated_audio_service: GeneratedAudioService,
) -> None:
    @api.post("/conversations/update/<int:conversation_id>")
    def update_conversation(conversation_id: int):
        return _update_conversation(
            model_service,
            conversation_service,
            generated_audio_service,
            conversation_id,
        )


def _register_delete_conversation_route(
    api: Blueprint,
    model_service: ModelService,
    conversation_service: ConversationService,
    generated_audio_service: GeneratedAudioService,
) -> None:
    @api.delete("/conversations/delete/<int:conversation_id>")
    def delete_conversation(conversation_id: int):
        return _delete_conversation(
            model_service,
            conversation_service,
            generated_audio_service,
            conversation_id,
        )


def _register_save_clone_setting_route(
    api: Blueprint,
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
) -> None:
    @api.post("/settings/save-clone")
    def save_clone_setting():
        return _save_clone_setting(model_service, clone_settings_service, audio_storage)


def _register_save_clone_recording_setting_route(
    api: Blueprint,
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
) -> None:
    @api.post("/settings/save-clone-recording")
    def save_clone_recording_setting():
        return _save_clone_recording_setting(model_service, clone_settings_service, audio_storage)


def _register_get_clone_setting_routes(
    api: Blueprint,
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
) -> None:
    @api.get("/settings/get-clone/<int:setting_id>")
    @api.get("/settings/get-clones/<int:setting_id>")
    def get_clone_setting(setting_id: int):
        return _get_clone_setting(model_service, clone_settings_service, setting_id)


def _register_get_clone_setting_audio_route(
    api: Blueprint,
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
) -> None:
    @api.get("/settings/get-clone-audio/<int:setting_id>")
    def get_clone_setting_audio(setting_id: int):
        return _get_clone_setting_audio(model_service, clone_settings_service, audio_storage, setting_id)


def _register_update_clone_setting_route(
    api: Blueprint,
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
) -> None:
    @api.post("/settings/update-clone/<int:setting_id>")
    def update_clone_setting(setting_id: int):
        return _update_clone_setting(model_service, clone_settings_service, setting_id)


def _register_delete_clone_setting_route(
    api: Blueprint,
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
) -> None:
    @api.delete("/settings/delete-clone/<int:setting_id>")
    def delete_clone_setting(setting_id: int):
        return _delete_clone_setting(model_service, clone_settings_service, audio_storage, setting_id)


def _register_get_clone_settings_route(
    api: Blueprint,
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
) -> None:
    @api.get("/settings/get-clones")
    def get_clone_settings():
        return _get_clone_settings(model_service, clone_settings_service)


def _hello_world() -> str:
    return "Hello, World!"


def _get_generated_audio(
    model_service: ModelService,
    generated_audio_service: GeneratedAudioService,
    filename: str,
):
    try:
        audio_path = generated_audio_service.resolve_filename(filename)
    except FileNotFoundError:
        return _json_error("Generated audio file not found.", model_service, HTTPStatus.NOT_FOUND)

    if not audio_path.is_file():
        return _json_error("Generated audio file not found.", model_service, HTTPStatus.NOT_FOUND)

    return send_file(audio_path, mimetype="audio/mpeg", as_attachment=False, download_name=audio_path.name)


def _load_model(model_service: ModelService):
    try:
        model_service.load()
    except ModelLoadInProgressError as exc:
        return _json_error(str(exc), model_service, HTTPStatus.CONFLICT)
    except Exception as exc:
        return _json_error("Failed to load model.", model_service, HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    message = "Model loaded successfully."
    return jsonify(_build_model_response(message, model_service)), HTTPStatus.OK


def _unload_model(model_service: ModelService):
    result = model_service.unload()

    if result is UnloadResult.LOADING:
        return _json_error("Model is still loading.", model_service, HTTPStatus.CONFLICT)

    message = "Model unloaded successfully." if result is UnloadResult.UNLOADED else "Model was not loaded."
    return jsonify(_build_model_response(message, model_service)), HTTPStatus.OK


def _synthesize_speech(
    model_service: ModelService,
    generated_audio_service: GeneratedAudioService,
):
    payload = _get_json_payload()

    try:
        synthesis_request = parse_synthesis_request(payload)
    except RequestValidationError as exc:
        return _json_error(
            "Invalid synthesis request.",
            model_service,
            HTTPStatus.BAD_REQUEST,
            str(exc),
        )

    try:
        audio, sample_rate = model_service.synthesize(synthesis_request)
        generated_audio = generated_audio_service.save(audio, sample_rate, prefix="synthesis")
    except ModelLoadInProgressError as exc:
        return _json_error(str(exc), model_service, HTTPStatus.CONFLICT)
    except ModelNotLoadedError:
        return _json_error("Model is not loaded. Call /load first.", model_service, HTTPStatus.CONFLICT)
    except Exception as exc:
        return _json_error("Synthesis failed.", model_service, HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    return jsonify({"message": "Synthesis complete.", "audio_url": generated_audio.url}), HTTPStatus.OK


def _clone_voice(
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
    generated_audio_service: GeneratedAudioService,
):
    setting_id = request.form.get("setting_id")
    temp_path: str | None = None

    try:
        if setting_id not in (None, ""):
            clone_request = _build_clone_request_from_saved_setting(
                request.form,
                clone_settings_service,
                audio_storage,
                setting_id,
            )
        else:
            ref_audio = request.files.get("ref_audio")
            if ref_audio is None or not ref_audio.filename:
                raise RequestValidationError("`ref_audio` is required and must be an uploaded audio file.")

            temp_path = audio_storage.save_temporary_upload(ref_audio)
            clone_request = parse_clone_request(request.form, temp_path)

        audio, sample_rate = model_service.clone(clone_request)
        generated_audio = generated_audio_service.save(audio, sample_rate, prefix="clone")
    except CloneSettingNotFoundError as exc:
        return _json_error("Clone setting not found.", model_service, HTTPStatus.NOT_FOUND, str(exc))
    except RequestValidationError as exc:
        return _json_error(
            "Invalid clone request.",
            model_service,
            HTTPStatus.BAD_REQUEST,
            str(exc),
        )
    except InvalidAudioUploadError as exc:
        return _json_error(
            "Invalid clone request.",
            model_service,
            HTTPStatus.BAD_REQUEST,
            str(exc),
        )
    except ModelLoadInProgressError as exc:
        return _json_error(str(exc), model_service, HTTPStatus.CONFLICT)
    except ModelNotLoadedError:
        return _json_error("Model is not loaded. Call /load first.", model_service, HTTPStatus.CONFLICT)
    except Exception as exc:
        return _json_error("Voice cloning failed.", model_service, HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))
    finally:
        if temp_path is not None:
            audio_storage.delete_file(temp_path)

    return jsonify({"message": "Voice cloning complete.", "audio_url": generated_audio.url}), HTTPStatus.OK


def _list_conversations(
    model_service: ModelService,
    conversation_service: ConversationService,
):
    try:
        conversations = conversation_service.list()
    except ConversationServiceError as exc:
        return _json_error("Failed to load conversations.", model_service, HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    return jsonify({"conversations": [_serialize_conversation(conversation) for conversation in conversations]}), HTTPStatus.OK


def _get_conversation(
    model_service: ModelService,
    conversation_service: ConversationService,
    conversation_id: int,
):
    try:
        conversation = conversation_service.get(conversation_id)
    except ConversationNotFoundError as exc:
        return _json_error("Conversation not found.", model_service, HTTPStatus.NOT_FOUND, str(exc))
    except ConversationServiceError as exc:
        return _json_error("Failed to load conversation.", model_service, HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    return jsonify({"conversation": _serialize_conversation(conversation)}), HTTPStatus.OK


def _create_conversation(model_service: ModelService, conversation_service: ConversationService):
    payload = _get_json_payload()

    try:
        conversation_request = parse_conversation_request(payload)
        conversation = conversation_service.create(conversation_request)
    except RequestValidationError as exc:
        return _json_error("Invalid conversation request.", model_service, HTTPStatus.BAD_REQUEST, str(exc))
    except ConversationServiceError as exc:
        return _json_error("Failed to create conversation.", model_service, HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    return (
        jsonify({"message": "Conversation created successfully.", "conversation": _serialize_conversation(conversation)}),
        HTTPStatus.CREATED,
    )


def _update_conversation(
    model_service: ModelService,
    conversation_service: ConversationService,
    generated_audio_service: GeneratedAudioService,
    conversation_id: int,
):
    payload = _get_json_payload()

    try:
        previous_conversation = conversation_service.get(conversation_id)
        conversation_request = parse_conversation_request(payload)
        conversation = conversation_service.update(conversation_id, conversation_request)
    except ConversationNotFoundError as exc:
        return _json_error("Conversation not found.", model_service, HTTPStatus.NOT_FOUND, str(exc))
    except RequestValidationError as exc:
        return _json_error("Invalid conversation request.", model_service, HTTPStatus.BAD_REQUEST, str(exc))
    except ConversationServiceError as exc:
        return _json_error("Failed to update conversation.", model_service, HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    previous_audio_urls = {line.audio_url for line in previous_conversation.lines if line.audio_url}
    next_audio_urls = {line.audio_url for line in conversation.lines if line.audio_url}
    for removed_audio_url in previous_audio_urls - next_audio_urls:
        generated_audio_service.delete_by_url(removed_audio_url)

    return jsonify({"message": "Conversation updated successfully.", "conversation": _serialize_conversation(conversation)}), HTTPStatus.OK


def _delete_conversation(
    model_service: ModelService,
    conversation_service: ConversationService,
    generated_audio_service: GeneratedAudioService,
    conversation_id: int,
):
    try:
        deleted_conversation = conversation_service.delete(conversation_id)
    except ConversationNotFoundError as exc:
        return _json_error("Conversation not found.", model_service, HTTPStatus.NOT_FOUND, str(exc))
    except ConversationServiceError as exc:
        return _json_error("Failed to delete conversation.", model_service, HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    for line in deleted_conversation.lines:
        generated_audio_service.delete_by_url(line.audio_url)

    return jsonify({"message": "Conversation deleted successfully.", "id": deleted_conversation.id}), HTTPStatus.OK


def _save_clone_setting(
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
):
    return _save_clone_setting_request(
        model_service,
        clone_settings_service,
        audio_storage,
        is_microphone_recording=False,
    )


def _save_clone_recording_setting(
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
):
    return _save_clone_setting_request(
        model_service,
        clone_settings_service,
        audio_storage,
        is_microphone_recording=True,
    )


def _get_clone_setting(
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    setting_id: int,
):
    try:
        setting = clone_settings_service.get(setting_id)
    except CloneSettingNotFoundError as exc:
        return _json_error("Clone setting not found.", model_service, HTTPStatus.NOT_FOUND, str(exc))
    except CloneSettingsServiceError as exc:
        return _json_error(
            "Failed to load clone setting.",
            model_service,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            str(exc),
        )

    return jsonify({"setting": _serialize_clone_setting(setting)}), HTTPStatus.OK


def _get_clone_setting_audio(
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
    setting_id: int,
):
    try:
        setting = clone_settings_service.get(setting_id)
    except CloneSettingNotFoundError as exc:
        return _json_error("Clone setting not found.", model_service, HTTPStatus.NOT_FOUND, str(exc))
    except CloneSettingsServiceError as exc:
        return _json_error(
            "Failed to load clone setting.",
            model_service,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            str(exc),
        )

    audio_path = audio_storage.resolve_path(setting.ref_audio_path)
    if not audio_path.is_file():
        return _json_error(
            "Clone setting reference audio not found.",
            model_service,
            HTTPStatus.NOT_FOUND,
            f"Missing file: {audio_path}",
        )

    return send_file(audio_path, as_attachment=False, download_name=audio_path.name)


def _update_clone_setting(
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    setting_id: int,
):
    ref_audio = request.files.get("ref_audio")
    if ref_audio is not None and ref_audio.filename:
        return _json_error(
            "Invalid clone setting update request.",
            model_service,
            HTTPStatus.BAD_REQUEST,
            "`ref_audio` cannot be updated after the setting is created.",
        )

    if request.form.get("ref_text") not in (None, ""):
        return _json_error(
            "Invalid clone setting update request.",
            model_service,
            HTTPStatus.BAD_REQUEST,
            "`ref_text` cannot be updated after the setting is created.",
        )

    try:
        clone_setting_request = parse_clone_setting_update_request(request.form)

        if _is_empty_clone_setting_update(clone_setting_request):
            raise RequestValidationError("Provide at least one field to update.")

        updated_setting = clone_settings_service.update(setting_id, clone_setting_request)
    except CloneSettingNotFoundError as exc:
        return _json_error("Clone setting not found.", model_service, HTTPStatus.NOT_FOUND, str(exc))
    except RequestValidationError as exc:
        return _json_error(
            "Invalid clone setting update request.",
            model_service,
            HTTPStatus.BAD_REQUEST,
            str(exc),
        )
    except CloneSettingsServiceError as exc:
        return _json_error(
            "Failed to update clone setting.",
            model_service,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            str(exc),
        )

    return jsonify({"message": "Clone setting updated successfully.", "id": updated_setting.id}), HTTPStatus.OK


def _delete_clone_setting(
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
    setting_id: int,
):
    try:
        deleted_setting = clone_settings_service.delete(setting_id)
    except CloneSettingNotFoundError as exc:
        return _json_error("Clone setting not found.", model_service, HTTPStatus.NOT_FOUND, str(exc))
    except CloneSettingsServiceError as exc:
        return _json_error(
            "Failed to delete clone setting.",
            model_service,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            str(exc),
        )

    audio_storage.delete_file(deleted_setting.ref_audio_path)
    return jsonify({"message": "Clone setting deleted successfully.", "id": deleted_setting.id}), HTTPStatus.OK


def _get_clone_settings(model_service: ModelService, clone_settings_service: CloneSettingsService):
    try:
        settings = clone_settings_service.list()
    except CloneSettingsServiceError as exc:
        return _json_error(
            "Failed to load clone settings.",
            model_service,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            str(exc),
        )

    return jsonify({"settings": [_serialize_clone_setting(setting) for setting in settings]}), HTTPStatus.OK


def _get_json_payload() -> dict[str, Any]:
    payload = request.get_json(silent=True)
    return payload if isinstance(payload, dict) else {}


def _save_clone_setting_request(
    model_service: ModelService,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
    *,
    is_microphone_recording: bool,
):
    ref_audio = request.files.get("ref_audio")
    if ref_audio is None or not ref_audio.filename:
        return _json_error(
            "Invalid clone setting request.",
            model_service,
            HTTPStatus.BAD_REQUEST,
            "`ref_audio` is required and must be an uploaded audio file.",
        )

    stored_audio_path: str | None = None

    try:
        clone_setting_request = parse_clone_setting_create_request(
            request.form,
            is_microphone_recording=is_microphone_recording,
        )
        stored_audio_path = audio_storage.save_persistent_upload(ref_audio)
        setting = clone_settings_service.create(clone_setting_request, stored_audio_path)
    except RequestValidationError as exc:
        return _json_error(
            "Invalid clone setting request.",
            model_service,
            HTTPStatus.BAD_REQUEST,
            str(exc),
        )
    except InvalidAudioUploadError as exc:
        return _json_error(
            "Invalid clone setting request.",
            model_service,
            HTTPStatus.BAD_REQUEST,
            str(exc),
        )
    except CloneSettingsServiceError as exc:
        if stored_audio_path is not None:
            audio_storage.delete_file(stored_audio_path)
        return _json_error(
            "Failed to save clone setting.",
            model_service,
            HTTPStatus.INTERNAL_SERVER_ERROR,
            str(exc),
        )

    return jsonify({"message": "Clone setting saved successfully.", "id": setting.id}), HTTPStatus.CREATED


def _is_empty_clone_setting_update(request_data: CloneSettingUpdateRequest) -> bool:
    return (
        request_data.name is None
        and request_data.lang is None
        and request_data.speed is None
        and request_data.num_step is None
    )


def _serialize_clone_setting(setting: CloneSetting) -> dict[str, Any]:
    return {
        "id": setting.id,
        "name": setting.name,
        "ref_audio_path": f"/api/v1/settings/get-clone-audio/{setting.id}",
        "ref_text": setting.ref_text,
        "lang": setting.lang,
        "speed": setting.speed,
        "num_step": setting.num_step,
        "is_microphone_recording": setting.is_microphone_recording,
        "created_at": setting.created_at,
    }


def _serialize_conversation(conversation: Conversation) -> dict[str, Any]:
    return {
        "id": conversation.id,
        "name": conversation.name,
        "lines": [_serialize_conversation_line(line) for line in conversation.lines],
        "created_at": conversation.created_at,
        "updated_at": conversation.updated_at,
    }


def _serialize_conversation_line(line: ConversationLine) -> dict[str, Any]:
    return {
        "id": line.id,
        "conversation_id": line.conversation_id,
        "position": line.position,
        "text": line.text,
        "voice_type": line.voice_type,
        "clone_setting_id": line.clone_setting_id,
        "voice_label": line.voice_label,
        "audio_url": line.audio_url,
        "lang": line.lang,
        "speed": line.speed,
        "num_step": line.num_step,
        "instruct": line.instruct,
        "selected_gender": line.selected_gender,
        "selected_accent": line.selected_accent,
        "selected_pitch": line.selected_pitch,
        "selected_age": line.selected_age,
        "selected_style": line.selected_style,
        "created_at": line.created_at,
        "updated_at": line.updated_at,
    }


def _build_clone_request_from_saved_setting(
    payload: Any,
    clone_settings_service: CloneSettingsService,
    audio_storage: AudioStorage,
    setting_id: str,
) -> CloneRequest:
    try:
        parsed_setting_id = int(setting_id)
    except ValueError as exc:
        raise RequestValidationError("`setting_id` must be a valid integer.") from exc

    setting = clone_settings_service.get(parsed_setting_id)
    text = payload.get("text")

    if not isinstance(text, str) or not text.strip():
        raise RequestValidationError("`text` is required and must be a non-empty string.")

    clone_setting_update = parse_clone_setting_update_request(payload)
    speed = clone_setting_update.speed if clone_setting_update.speed is not None else setting.speed
    num_step = clone_setting_update.num_step if clone_setting_update.num_step is not None else setting.num_step
    lang = clone_setting_update.lang if clone_setting_update.lang is not None else setting.lang

    return CloneRequest(
        text=text.strip(),
        ref_audio_path=str(audio_storage.resolve_path(setting.ref_audio_path)),
        ref_text=setting.ref_text,
        speed=speed,
        lang=lang,
        num_step=num_step,
    )


def _json_error(message: str, model_service: ModelService, status: HTTPStatus, error: str | None = None):
    response = _build_model_response(message, model_service)
    if error is not None:
        response["error"] = error
    return jsonify(response), status


def _build_model_response(message: str, model_service: ModelService) -> dict[str, str | None]:
    device = model_service.get_device()
    return {
        "message": message,
        "state": model_service.get_state().value,
        "device": device.value if device is not None else None,
    }
