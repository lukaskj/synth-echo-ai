from __future__ import annotations

import os
import tempfile
from pathlib import Path
from uuid import uuid4


ALLOWED_AUDIO_SUFFIXES = frozenset({".aac", ".flac", ".m4a", ".mp3", ".ogg", ".wav", ".webm"})


class InvalidAudioUploadError(ValueError):
    pass


class AudioStorage:
    def __init__(self, base_dir: Path, storage_dir: Path) -> None:
        self._base_dir = base_dir.resolve()
        self._storage_dir = storage_dir.resolve()
        self._storage_dir.mkdir(parents=True, exist_ok=True)

    def save_persistent_upload(self, uploaded_file) -> str:
        suffix = self._get_valid_suffix(uploaded_file.filename)
        target_path = self._storage_dir / f"clone-setting-{uuid4().hex}{suffix}"
        uploaded_file.save(target_path)

        self._validate_non_empty_file(target_path)
        return self._to_relative_path(target_path)

    def save_temporary_upload(self, uploaded_file) -> str:
        suffix = self._get_valid_suffix(uploaded_file.filename)
        file_descriptor, temp_path = tempfile.mkstemp(prefix="omnivoice-clone-", suffix=suffix)
        os.close(file_descriptor)
        uploaded_file.save(temp_path)
        self._validate_non_empty_file(Path(temp_path))
        return temp_path

    def resolve_path(self, path: str) -> Path:
        candidate = Path(path)
        if candidate.is_absolute():
            if candidate.exists():
                return candidate

            remapped_path = self._try_remap_legacy_storage_path(path)
            return remapped_path if remapped_path is not None else candidate

        normalized_path = path.replace("\\", "/")
        while normalized_path.startswith("./"):
            normalized_path = normalized_path[2:]

        return (self._base_dir / normalized_path).resolve()

    def delete_file(self, path: str) -> None:
        try:
            self.resolve_path(path).unlink(missing_ok=True)
        except OSError:
            pass

    @staticmethod
    def _get_valid_suffix(filename: str | None) -> str:
        suffix = Path(filename or "").suffix.lower()
        if suffix not in ALLOWED_AUDIO_SUFFIXES:
            supported = ", ".join(sorted(ALLOWED_AUDIO_SUFFIXES))
            raise InvalidAudioUploadError(f"`ref_audio` must use one of these file types: {supported}.")
        return suffix

    def _validate_non_empty_file(self, path: Path) -> None:
        if path.stat().st_size > 0:
            return

        self.delete_file(str(path))
        raise InvalidAudioUploadError("`ref_audio` must not be empty.")

    def _to_relative_path(self, path: Path) -> str:
        return f"./{path.resolve().relative_to(self._base_dir).as_posix()}"

    def _try_remap_legacy_storage_path(self, path: str) -> Path | None:
        normalized_path = path.replace("\\", "/")
        marker = "/storage/clone_settings/"
        marker_index = normalized_path.lower().find(marker)
        if marker_index == -1:
            return None

        relative_storage_path = normalized_path[marker_index + 1 :]
        return (self._base_dir / relative_storage_path).resolve()
