from __future__ import annotations

import atexit
import signal
from types import FrameType

from .services.model_service import ModelService


def register_shutdown_handlers(model_service: ModelService) -> None:
    def shutdown_cleanup() -> None:
        model_service.unload()

    def handle_shutdown_signal(_signum: int, _frame: FrameType | None) -> None:
        shutdown_cleanup()
        raise SystemExit(0)

    atexit.register(shutdown_cleanup)

    for signal_name in ("SIGINT", "SIGTERM"):
        if hasattr(signal, signal_name):
            try:
                signal.signal(getattr(signal, signal_name), handle_shutdown_signal)
            except ValueError:
                pass
