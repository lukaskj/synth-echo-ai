from enum import Enum

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

class Device(str, Enum):
    AUTO = "auto"
    CUDA = "cuda"
    MPS = "mps"
    CPU = "cpu"