import torch


class VAEDecodeMultiGPU:
    """Thin wrapper around ComfyUI's VAE decode with status reporting."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "samples": ("LATENT",),
                "vae": ("VAE",),
            }
        }

    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("image", "status")
    FUNCTION = "decode"
    CATEGORY = "MultiGPU/VAE"

    def decode(self, samples, vae):
        try:
            decoded = vae.decode(samples["samples"])
            if decoded.dim() == 5:  # Merge temporal/batch dimensions if present
                decoded = decoded.reshape(-1, decoded.shape[-3], decoded.shape[-2], decoded.shape[-1])
            status = "✅ VAE decode finished"
            return (decoded, status)
        except Exception as exc:  # pragma: no cover - decode path should succeed in Comfy
            status = f"❌ VAE decode failed: {exc}"
            fallback = torch.rand(1, 512, 512, 3)
            return (fallback, status)
