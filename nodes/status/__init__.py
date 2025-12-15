from .gpu_status import GPUStatusDisplay
from .debug_status import GPUStatusDisplayDebug

NODE_CLASS_MAPPINGS = {
    "GPUStatusDisplay": GPUStatusDisplay,
    "GPUStatusDisplayDebug": GPUStatusDisplayDebug,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GPUStatusDisplay": "GPU Status Display",
    "GPUStatusDisplayDebug": "GPU Status Display (Debug)",
}
