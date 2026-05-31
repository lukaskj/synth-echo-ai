from __future__ import annotations

from typing import cast
from pathlib import Path

from flask import Flask
from flask_cors import CORS

from .constants import API_PREFIX
from .repositories.clone_settings_repository import CloneSettingsRepository
from .routes import create_api_blueprint
from .services.clone_settings_service import CloneSettingsService
from .services.model_service import ModelService
from .storage import AudioStorage


MODEL_SERVICE_EXTENSION_KEY = "tts_model_service"
CLONE_SETTINGS_SERVICE_EXTENSION_KEY = "clone_settings_service"


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)

    backend_root = Path(__file__).resolve().parents[1]
    model_service = ModelService()
    clone_settings_repository = CloneSettingsRepository(backend_root / "data" / "clone_settings.sqlite3")
    clone_settings_service = CloneSettingsService(clone_settings_repository)
    clone_settings_service.initialize()
    audio_storage = AudioStorage(backend_root, backend_root / "storage" / "clone_settings")

    app.extensions[MODEL_SERVICE_EXTENSION_KEY] = model_service
    app.extensions[CLONE_SETTINGS_SERVICE_EXTENSION_KEY] = clone_settings_service
    app.register_blueprint(
        create_api_blueprint(model_service, clone_settings_service, audio_storage),
        url_prefix=API_PREFIX,
    )
    return app


def get_model_service(app: Flask) -> ModelService:
    return cast(ModelService, app.extensions[MODEL_SERVICE_EXTENSION_KEY])


def get_clone_settings_service(app: Flask) -> CloneSettingsService:
    return cast(CloneSettingsService, app.extensions[CLONE_SETTINGS_SERVICE_EXTENSION_KEY])
