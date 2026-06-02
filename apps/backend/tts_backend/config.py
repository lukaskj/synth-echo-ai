from .enums import Device

class Config:    
    @staticmethod
    def resolve_model_device_dtype() -> tuple[str, str, str]:
      import torch
      dtype = torch.float16
      device = Device.CPU
      model_device = "cpu"
      try:
          if torch.cuda.is_available():
              device = Device.CUDA
              dtype = torch.float32
              model_device = "cuda:0"
          if torch.backends.mps.is_available():
              device = Device.MPS
              dtype = torch.float32
              model_device = "mps"
      except ImportError:
          pass
      return device, dtype, model_device
