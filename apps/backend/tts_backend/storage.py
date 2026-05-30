from __future__ import annotations

import os
import tempfile
from pathlib import Path
from uuid import uuid4


ALLOWED_AUDIO_SUFFIXES = frozenset({".aac", ".flac", ".m4a", ".mp3", ".ogg", ".wav", ".webm"})


class InvalidAudioUploadError(ValueError):
    pass


class AudioStorage:
    def __init__(self, storage_dir: Path) -> None:
        self._storage_dir = storage_dir
        self._storage_dir.mkdir(parents=True, exist_ok=True)

    def save_persistent_upload(self, uploaded_file) -> str:
        suffix = self._get_valid_suffix(uploaded_file.filename)
        target_path = self._storage_dir / f"clone-setting-{uuid4().hex}{suffix}"
        uploaded_file.save(target_path)

        self._validate_non_empty_file(target_path)
        return str(target_path)

    def save_temporary_upload(self, uploaded_file) -> str:
        suffix = self._get_valid_suffix(uploaded_file.filename)
        file_descriptor, temp_path = tempfile.mkstemp(prefix="omnivoice-clone-", suffix=suffix)
        os.close(file_descriptor)
        uploaded_file.save(temp_path)
        self._validate_non_empty_file(Path(temp_path))
        return temp_path

    @staticmethod
    def delete_file(path: str) -> None:
        try:
            Path(path).unlink(missing_ok=True)
        except OSError:
            pass

    @staticmethod
    def _get_valid_suffix(filename: str | None) -> str:
        suffix = Path(filename or "").suffix.lower()
        if suffix not in ALLOWED_AUDIO_SUFFIXES:
            supported = ", ".join(sorted(ALLOWED_AUDIO_SUFFIXES))
            raise InvalidAudioUploadError(f"`ref_audio` must use one of these file types: {supported}.")
        return suffix

    @staticmethod
    def _validate_non_empty_file(path: Path) -> None:
        if path.stat().st_size > 0:
            return

        AudioStorage.delete_file(str(path))
        raise InvalidAudioUploadError("`ref_audio` must not be empty.")
