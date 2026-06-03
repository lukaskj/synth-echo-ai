from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from uuid import uuid4

from ..audio import audio_to_mp3_buffer


@dataclass(frozen=True, slots=True)
class GeneratedAudioAsset:
    url: str


class GeneratedAudioService:
    def __init__(self, storage_dir: Path, route_prefix: str) -> None:
        self._storage_dir = storage_dir.resolve()
        self._storage_dir.mkdir(parents=True, exist_ok=True)
        self._route_prefix = route_prefix.rstrip("/")

    def save(self, audio, sample_rate: int, *, prefix: str) -> GeneratedAudioAsset:
        target_path = self._storage_dir / f"{prefix}-{uuid4().hex}.mp3"
        mp3_buffer = audio_to_mp3_buffer(audio, sample_rate)
        target_path.write_bytes(mp3_buffer.getvalue())

        if target_path.stat().st_size == 0:
            target_path.unlink(missing_ok=True)
            raise RuntimeError("Generated audio file was empty.")

        return GeneratedAudioAsset(url=f"{self._route_prefix}/{target_path.name}")

    def resolve_filename(self, filename: str) -> Path:
        safe_filename = Path(filename).name
        if safe_filename != filename or not safe_filename.endswith(".mp3"):
            raise FileNotFoundError(filename)

        return self._storage_dir / safe_filename

    def delete_by_url(self, audio_url: str) -> None:
        filename = self._get_filename_from_url(audio_url)
        if filename is None:
            return

        try:
            self.resolve_filename(filename).unlink(missing_ok=True)
        except OSError:
            pass

    def _get_filename_from_url(self, audio_url: str) -> str | None:
        path = urlparse(audio_url).path
        prefix = f"{self._route_prefix}/"
        if not path.startswith(prefix):
            return None

        filename = path.removeprefix(prefix)
        return filename or None
