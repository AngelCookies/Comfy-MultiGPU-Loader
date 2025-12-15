from .multigpu_vae import VAEDecodeMultiGPU
from .debug_vae import VAEDecodeMultiGPUDebug

NODE_CLASS_MAPPINGS = {
    "VAEDecodeMultiGPU": VAEDecodeMultiGPU,
    "VAEDecodeMultiGPUDebug": VAEDecodeMultiGPUDebug,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VAEDecodeMultiGPU": "VAE Decode (MultiGPU)",
    "VAEDecodeMultiGPUDebug": "VAE Decode (MultiGPU Debug)",
}
