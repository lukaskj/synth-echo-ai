from __future__ import annotations

import gc
from threading import Lock
from typing import Any

from ..constants import MODEL_REPOSITORY
from ..schemas import CloneRequest, SynthesisRequest
from ..enums import ModelState, LoadResult, UnloadResult, Device
from ..config import Config


class ModelLoadInProgressError(RuntimeError):
    pass


class ModelNotLoadedError(RuntimeError):
    pass


class ModelService:
    def __init__(self) -> None:
        self._model: Any | None = None
        self._state = ModelState.UNLOADED
        self._device: Device | None = None
        self._lock = Lock()

    def get_state(self) -> ModelState:
        with self._lock:
            return self._state

    def get_device(self) -> Device | None:
        with self._lock:
            return self._device

    def load(self) -> LoadResult:
        with self._lock:
            if self._state is ModelState.LOADED:
                return LoadResult.ALREADY_LOADED

            if self._state is ModelState.LOADING:
                raise ModelLoadInProgressError("Model is still loading.")

            self._state = ModelState.LOADING

        try:
            model, device = self._create_model()
        except Exception:
            with self._lock:
                self._state = ModelState.UNLOADED
            raise

        with self._lock:
            self._model = model
            self._state = ModelState.LOADED
            self._device = device

        return LoadResult.LOADED

    def unload(self) -> UnloadResult:
        with self._lock:
            if self._state is ModelState.LOADING:
                return UnloadResult.LOADING

            if self._model is None:
                self._state = ModelState.UNLOADED
                self._device = None
                return UnloadResult.NOT_LOADED

            self._model = None
            self._state = ModelState.UNLOADED
            self._device = None

        gc.collect()
        self._clear_cache()
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
    def _create_model() -> tuple[Any, Device]:
        from omnivoice import OmniVoice

        device, dtype, model_device = Config.resolve_model_device_dtype()
        print(f"Loading model on {device} with dtype {dtype}...")

        model = OmniVoice.from_pretrained(
            MODEL_REPOSITORY,
            device_map=model_device,
            dtype=dtype,
        )
        return model, device

    @staticmethod
    def _clear_cache() -> None:
        try:
            import torch

            if torch.accelerator.is_available():
              torch.accelerator.memory.empty_cache()
              return

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
            if torch.backends.mps.is_available():
                torch.mps.empty_cache()
        except ImportError:
            pass
