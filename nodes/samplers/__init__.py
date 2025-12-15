from .multigpu_sampler import KSamplerMultiGPU
from .debug_sampler import KSamplerMultiGPUDebug

NODE_CLASS_MAPPINGS = {
    "KSamplerMultiGPU": KSamplerMultiGPU,
    "KSamplerMultiGPUDebug": KSamplerMultiGPUDebug,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "KSamplerMultiGPU": "KSampler (MultiGPU)",
    "KSamplerMultiGPUDebug": "KSampler (MultiGPU Debug)",
}
