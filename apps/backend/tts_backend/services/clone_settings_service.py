from __future__ import annotations

import sqlite3

from ..repositories.clone_settings_repository import CloneSettingsRepository
from ..schemas import CloneSetting, CloneSettingCreateRequest, CloneSettingUpdateRequest


class CloneSettingNotFoundError(LookupError):
    pass


class CloneSettingsServiceError(RuntimeError):
    pass


class CloneSettingsService:
    def __init__(self, repository: CloneSettingsRepository) -> None:
        self._repository = repository

    def initialize(self) -> None:
        try:
            self._repository.initialize()
        except sqlite3.Error as exc:
            raise CloneSettingsServiceError("Failed to initialize clone settings.") from exc

    def create(self, request: CloneSettingCreateRequest, ref_audio_path: str) -> CloneSetting:
        try:
            setting_id = self._repository.create(request, ref_audio_path)
        except sqlite3.Error as exc:
            raise CloneSettingsServiceError("Failed to create clone setting.") from exc
        return self.get(setting_id)

    def get(self, setting_id: int) -> CloneSetting:
        try:
            setting = self._repository.get(setting_id)
        except sqlite3.Error as exc:
            raise CloneSettingsServiceError("Failed to load clone setting.") from exc

        if setting is None:
            raise CloneSettingNotFoundError(f"Clone setting {setting_id} was not found.")

        return setting

    def list(self) -> list[CloneSetting]:
        try:
            return self._repository.list()
        except sqlite3.Error as exc:
            raise CloneSettingsServiceError("Failed to load clone settings.") from exc

    def update(
        self,
        setting_id: int,
        request: CloneSettingUpdateRequest,
        ref_audio_path: str | None = None,
    ) -> CloneSetting:
        current = self.get(setting_id)

        next_name = request.name if request.name is not None else current.name
        next_ref_audio_path = ref_audio_path if ref_audio_path is not None else current.ref_audio_path
        next_ref_text = request.ref_text if request.ref_text is not None else current.ref_text
        next_lang = request.lang if request.lang is not None else current.lang
        next_speed = request.speed if request.speed is not None else current.speed
        next_num_step = request.num_step if request.num_step is not None else current.num_step
        next_is_microphone_recording = current.is_microphone_recording

        try:
            self._repository.update(
                CloneSetting(
                    id=setting_id,
                    name=next_name,
                    ref_audio_path=next_ref_audio_path,
                    ref_text=next_ref_text,
                    lang=next_lang,
                    speed=next_speed,
                    num_step=next_num_step,
                    is_microphone_recording=next_is_microphone_recording,
                    created_at=current.created_at,
                )
            )
        except sqlite3.Error as exc:
            raise CloneSettingsServiceError("Failed to update clone setting.") from exc

        return self.get(setting_id)

    def delete(self, setting_id: int) -> CloneSetting:
        setting = self.get(setting_id)

        try:
            self._repository.delete(setting_id)
        except sqlite3.Error as exc:
            raise CloneSettingsServiceError("Failed to delete clone setting.") from exc

        return setting
