from __future__ import annotations

import io
from typing import Any


def audio_to_mp3_buffer(audio: Any, sample_rate: int) -> io.BytesIO:
    import soundfile as sf

    buffer = io.BytesIO()
    sf.write(buffer, audio, sample_rate, format="MP3")
    buffer.seek(0)
    return buffer
