from __future__ import annotations

import gc
from enum import Enum
from threading import Lock
from typing import Any

from ..constants import MODEL_DEVICE_MAP, MODEL_REPOSITORY
from ..schemas import CloneRequest, SynthesisRequest


class ModelState(str, Enum):
    UNLOADED = "unloaded"
    LOADING = "loading"
    LOADED = "loaded"


class LoadResult(str, Enum):
    LOADED = "loaded"
    ALREADY_LOADED = "already_loaded"


class UnloadResult(str, Enum):
    UNLOADED = "unloaded"
    NOT_LOADED = "not_loaded"
    LOADING = "loading"


class ModelLoadInProgressError(RuntimeError):
    pass


class ModelNotLoadedError(RuntimeError):
    pass


class ModelService:
    def __init__(self) -> None:
        self._model: Any | None = None
        self._state = ModelState.UNLOADED
        self._lock = Lock()

    def get_state(self) -> ModelState:
        with self._lock:
            return self._state

    def load(self) -> LoadResult:
        with self._lock:
            if self._state is ModelState.LOADED:
                return LoadResult.ALREADY_LOADED

            if self._state is ModelState.LOADING:
                raise ModelLoadInProgressError("Model is still loading.")

            self._state = ModelState.LOADING

        try:
            model = self._create_model()
        except Exception:
            with self._lock:
                self._state = ModelState.UNLOADED
            raise

        with self._lock:
            self._model = model
            self._state = ModelState.LOADED

        return LoadResult.LOADED

    def unload(self) -> UnloadResult:
        with self._lock:
            if self._state is ModelState.LOADING:
                return UnloadResult.LOADING

            if self._model is None:
                self._state = ModelState.UNLOADED
                return UnloadResult.NOT_LOADED

            self._model = None
            self._state = ModelState.UNLOADED

        gc.collect()
        self._clear_cuda_cache()
        return UnloadResult.UNLOADED

    def synthesize(self, request: SynthesisRequest) -> tuple[Any, int]:
        with self._lock:
            if self._state is ModelState.LOADING:
                raise ModelLoadInProgressError("Model is still loading.")

            if self._model is None:
                raise ModelNotLoadedError("Model is not loaded.")

            audio = self._model.generate(
                text=request.text,
                language=request.lang,
                instruct=request.instruct,
                speed=request.speed,
                num_step=request.num_step,
            )
            return audio[0], self._model.sampling_rate

    def clone(self, request: CloneRequest) -> tuple[Any, int]:
        with self._lock:
            if self._state is ModelState.LOADING:
                raise ModelLoadInProgressError("Model is still loading.")

            if self._model is None:
                raise ModelNotLoadedError("Model is not loaded.")

            audio = self._model.generate(
                text=request.text,
                ref_audio=request.ref_audio_path,
                ref_text=request.ref_text,
                language=request.lang,
                speed=request.speed,
                num_step=request.num_step,
            )
            return audio[0], self._model.sampling_rate

    @staticmethod
    def _create_model() -> Any:
        import torch
        from omnivoice import OmniVoice

        return OmniVoice.from_pretrained(
            MODEL_REPOSITORY,
            device_map=MODEL_DEVICE_MAP,
            dtype=torch.float16,
        )

    @staticmethod
    def _clear_cuda_cache() -> None:
        try:
            import torch

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
        except ImportError:
            pass
