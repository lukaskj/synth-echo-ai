from .enums import Device


class Config:
    @staticmethod
    def resolve_model_device_dtype() -> tuple[str, str, str]:
        import torch

        try:
            if torch.cuda.is_available():
                return Device.CUDA, torch.float32, "cuda:0"
            elif torch.backends.mps.is_available():
                return Device.MPS, torch.float32, "mps"
        except ImportError:
            pass

        return Device.CPU, torch.float16, "cpu"
