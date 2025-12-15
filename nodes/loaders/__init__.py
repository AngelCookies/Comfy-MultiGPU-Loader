from .multigpu_loader import (
    LoadCheckpointMultiGPU,
    LoadCheckpointMultiGPUDebug,
    LoadFluxCheckpointMultiGPU,
    LoadFluxCheckpointMultiGPUDebug,
)

NODE_CLASS_MAPPINGS = {
    "LoadCheckpointMultiGPU": LoadCheckpointMultiGPU,
    "LoadFluxCheckpointMultiGPU": LoadFluxCheckpointMultiGPU,
    "LoadCheckpointMultiGPUDebug": LoadCheckpointMultiGPUDebug,
    "LoadFluxCheckpointMultiGPUDebug": LoadFluxCheckpointMultiGPUDebug,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadCheckpointMultiGPU": "Load Checkpoint (MultiGPU)",
    "LoadFluxCheckpointMultiGPU": "Flux Loader (All-In-One)",
    "LoadCheckpointMultiGPUDebug": "Load Checkpoint (MultiGPU Debug)",
    "LoadFluxCheckpointMultiGPUDebug": "Flux Loader Debug (All-In-One)",
}
