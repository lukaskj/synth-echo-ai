from __future__ import annotations

from typing import cast
from pathlib import Path

from flask import Flask
from flask_cors import CORS

from .constants import API_PREFIX
from .repositories.clone_settings_repository import CloneSettingsRepository
from .repositories.conversation_repository import ConversationRepository
from .routes import (
    AUDIO_STORAGE_EXTENSION_KEY,
    CLONE_SETTINGS_SERVICE_EXTENSION_KEY,
    CONVERSATION_SERVICE_EXTENSION_KEY,
    GENERATED_AUDIO_SERVICE_EXTENSION_KEY,
    MODEL_SERVICE_EXTENSION_KEY,
    create_api_blueprint,
)
from .services.clone_settings_service import CloneSettingsService
from .services.conversation_service import ConversationService
from .services.generated_audio_service import GeneratedAudioService
from .services.model_service import ModelService
from .storage import AudioStorage

def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    backend_root = Path(__file__).resolve().parents[1]
    model_service = ModelService()
    database_path = backend_root / "data" / "clone_settings.sqlite3"
    clone_settings_repository = CloneSettingsRepository(database_path)
    conversation_repository = ConversationRepository(database_path)
    clone_settings_service = CloneSettingsService(clone_settings_repository)
    conversation_service = ConversationService(conversation_repository)
    clone_settings_service.initialize()
    conversation_service.initialize()
    audio_storage = AudioStorage(backend_root, backend_root / "storage" / "clone_settings")
    generated_audio_service = GeneratedAudioService(
        backend_root / "storage" / "generated_audio",
        f"{API_PREFIX}/generated-audio",
    )

    app.extensions[MODEL_SERVICE_EXTENSION_KEY] = model_service
    app.extensions[CLONE_SETTINGS_SERVICE_EXTENSION_KEY] = clone_settings_service
    app.extensions[CONVERSATION_SERVICE_EXTENSION_KEY] = conversation_service
    app.extensions[AUDIO_STORAGE_EXTENSION_KEY] = audio_storage
    app.extensions[GENERATED_AUDIO_SERVICE_EXTENSION_KEY] = generated_audio_service
    app.register_blueprint(
        create_api_blueprint(),
        url_prefix=API_PREFIX,
    )
    return app


def get_model_service(app: Flask) -> ModelService:
    return cast(ModelService, app.extensions[MODEL_SERVICE_EXTENSION_KEY])


def get_clone_settings_service(app: Flask) -> CloneSettingsService:
    return cast(CloneSettingsService, app.extensions[CLONE_SETTINGS_SERVICE_EXTENSION_KEY])


def get_conversation_service(app: Flask) -> ConversationService:
    return cast(ConversationService, app.extensions[CONVERSATION_SERVICE_EXTENSION_KEY])
