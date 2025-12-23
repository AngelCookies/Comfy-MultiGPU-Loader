"""
Comfy MultiGPU Loader
Copyright (C) 2025 Stefan Felton-Glenn  <stefanfg@protonmail.com>

This program comes with ABSOLUTELY NO WARRANTY; see LICENSE for details.
This is free software, and you are welcome to redistribute it
under the terms of the GPL-3.0; see LICENSE.
"""

import torch

from ...utils import create_colored_image, get_available_gpus, validate_gpu_count


class HardwareValidatorMultiGPU:
    """
    Verifies available GPUs against minimum VRAM/count for heavy checkpoints.
    Use this ahead of the loaders and pipe the gpu_ids output into them.
    """

    CATEGORY = "MultiGPU/Safety"

    PROFILES = {
        "generic": {"min_total_gb": 0, "min_per_gpu_gb": 0, "min_gpus": 1, "notes": "No enforced limits."},
        "sdxl": {"min_total_gb": 24, "min_per_gpu_gb": 8, "min_gpus": 1, "notes": "Typical SDXL floor; adjust per rig."},
        "flux-dev": {"min_total_gb": 32, "min_per_gpu_gb": 10, "min_gpus": 2, "notes": "Flux dev FP16/FP8 style footprints."},
        "flux-dev2-fp32": {"min_total_gb": 64, "min_per_gpu_gb": 12, "min_gpus": 6, "notes": "Flux Dev 2 FP32 baseline; assumes 12GB-class GPUs."},
    }

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "profile": (
                    list(cls.PROFILES.keys()),
                    {"default": "flux-dev2-fp32", "tooltip": "Profile to validate against."},
                ),
                "num_gpus": ([1, 2, 3, 4, 5, 6, 7, 8, "Auto"], {"default": "Auto", "tooltip": "How many GPUs to check (Auto uses all available)."}),
            },
            "optional": {
                "gpu_ids": ("STRING", {"default": "0,1,2,3,4,5,6,7", "multiline": False, "tooltip": "Comma-separated GPU IDs to allow."}),
                "allow_overcommit": ("BOOLEAN", {"default": False, "tooltip": "If true, emit warning but still pass when below requirements."}),
                "status_image": ("BOOLEAN", {"default": True, "tooltip": "Return a colored status image when validation fails."}),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "BOOLEAN", "IMAGE")
    RETURN_NAMES = ("gpu_ids", "status", "ok", "status_image")
    FUNCTION = "validate"

    def validate(self, profile, num_gpus, gpu_ids="0,1,2,3,4,5,6,7", allow_overcommit=False, status_image=True):
        available_gpus = get_available_gpus()
        if not available_gpus:
            status = "❌ No CUDA GPUs available."
            img = create_colored_image([180, 70, 70], "No GPUs") if status_image else None
            return "", status, False, img

        try:
            requested_gpu_ids = [int(x.strip()) for x in gpu_ids.split(",") if x.strip() != ""]
            valid_gpu_ids = [gid for gid in requested_gpu_ids if gid in available_gpus]
        except Exception:
            valid_gpu_ids = available_gpus

        actual_num_gpus = validate_gpu_count(num_gpus, valid_gpu_ids)
        used_gpus = valid_gpu_ids[:actual_num_gpus]

        if not used_gpus:
            status = "❌ No valid GPU IDs after filtering."
            img = create_colored_image([180, 70, 70], "No GPUs") if status_image else None
            return "", status, False, img

        profile_limits = self.PROFILES.get(profile, self.PROFILES["generic"])

        per_gpu_info = []
        for gid in used_gpus:
            try:
                props = torch.cuda.get_device_properties(gid)
                total_gb = props.total_memory / (1024**3)
                name = props.name
            except Exception:
                total_gb = 0
                name = "Unknown"
            per_gpu_info.append({"id": gid, "vram_gb": total_gb, "name": name})

        total_vram_gb = sum(g["vram_gb"] for g in per_gpu_info)
        min_vram_gb = min(g["vram_gb"] for g in per_gpu_info)

        failures = []
        if total_vram_gb < profile_limits["min_total_gb"]:
            failures.append(f"Total VRAM {total_vram_gb:.1f}GB < required {profile_limits['min_total_gb']}GB")
        if len(used_gpus) < profile_limits["min_gpus"]:
            failures.append(f"Only {len(used_gpus)} GPU(s); need {profile_limits['min_gpus']}+")
        if min_vram_gb < profile_limits["min_per_gpu_gb"]:
            failures.append(f"At least one GPU below {profile_limits['min_per_gpu_gb']}GB (lowest={min_vram_gb:.1f}GB)")

        ok = len(failures) == 0 or allow_overcommit

        status_lines = []
        status_lines.append(f"Profile: {profile} — {profile_limits['notes']}")
        status_lines.append(f"GPUs checked: {used_gpus}")
        status_lines.append("Per-GPU VRAM:")
        for g in per_gpu_info:
            status_lines.append(f"  GPU {g['id']} ({g['name']}): {g['vram_gb']:.1f}GB")
        status_lines.append(f"Total VRAM: {total_vram_gb:.1f}GB across {len(used_gpus)} GPU(s)")

        if failures:
            prefix = "⚠️ " if allow_overcommit else "❌ "
            status_lines.append(prefix + " / ".join(failures))
        else:
            status_lines.append("✅ Requirements met.")

        status_str = "\n".join(status_lines)
        img = None
        if status_image and (failures and not allow_overcommit):
            img = create_colored_image([200, 110, 50], "Safety check failed")
        elif status_image:
            img = create_colored_image([70, 130, 180], "Safety check OK")

        gpu_id_str = ",".join(str(g) for g in used_gpus)
        return gpu_id_str, status_str, ok, img
