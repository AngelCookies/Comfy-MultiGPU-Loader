## Comfy MultiGPU Loader
A set of ComfyUI nodes that shard SD/SDXL/Flux-style checkpoints across multiple GPUs using custom forwards.

### Solidarity
We stand with Ukraine. #standwithukraine.

### Not GGUF/Quantization
This project focuses on sharding native safetensors checkpoints across multiple GPUs. It does not provide GGUF loaders, quantization, or VRAM-reduction tooling like ComfyUI-GGUF. The goal here is to combine multiple GPUs to run large models, not to compress models for single-GPU fits.

### License
Licensed under GPL-3.0 (see LICENSE.md). Ethical use is encouraged, but GPL terms apply for compatibility with ComfyUI.

### Attribution
Developed by Stefan with assistance from AI tools (Claude by Anthropic, GPT-5 by OpenAI, Gemini by Google).

### Debug helpers
- *Load Checkpoint (MultiGPU) Debug*: `log_vram_snapshot` appends per-GPU VRAM readings (in GB) before and after sharding to the node status and `comfyui.log`.
- *KSampler (MultiGPU) Debug*: reports shard counts per device, flags GPUs without assigned blocks, logs live VRAM deltas and peak usage per GPU, and lists how many blocks each GPU executed during the last sampling pass.

### Installation
- Drop this repository into `ComfyUI/custom_nodes/Comfy-MultiGPU-Loader` (folder name can vary; ensure it contains this README and `nodes/`).
- Install requirements if needed: `pip install -r requirements.txt` (accelerate/torch are typically already present in ComfyUI environments).
- Restart ComfyUI. Nodes appear under `MultiGPU/Loaders`, `MultiGPU/Sampling`, `MultiGPU/VAE`, and `MultiGPU/Diagnostics`.

### How to use (and debug)
- Use the *Load Checkpoint (MultiGPU) Debug* or *Load Flux Checkpoint (MultiGPU) Debug* node to load your model; set `gpu_ids` (e.g., `0,1,2,3`) and optionally enable `log_vram_snapshot` for before/after VRAM numbers.
- Pair with *KSampler (MultiGPU) Debug* to see shard layout, per-GPU block counts, VRAM deltas, and peaks during sampling. Connect its `status` output to a display node to log details into `comfyui.log`.
- For production graphs without extra outputs, use the non-debug loader/sampler counterparts.

### Known issues
- Logging/diagnostics can under-report activity on later runs; ongoing investigation.
- Early-stage code other bugs may exist.

### Verified models
- Flux Dev Full Model fp32 (~22.17 GB) on multi-GPU.  
- 
### Needs Verifying models
- Flux Dev 2 (~60 GB) planned for validation when hardware/credits allow. 

### Tested hardware
- NVIDIA RTX 3070 (4x) via RunPod (multi-GPU sharding with Flux Dev Full Model fp32).

### Project goals
- Stable multi-GPU sharding for SD/SDXL/Flux checkpoints.
- Broader node coverage (samplers/VAEs/utility).
- Future: video workflows and additional node support.

### Future updates
- Fix outstanding bugs.  
- Expand support to more default ComfyUI nodes.  
- Explore video creation pipelines.  
- Harden logging/diagnostics.

Created: 15 Dec 2025  
Last updated: 15 Dec 2025

### Changelog
- 2025-12-15: Initial public-ready docs; added loader/sampler debug VRAM logging, shard usage counts, government-use ban in license.

### Current nodes
- Load Checkpoint (MultiGPU) / Debug  
- Load Flux Checkpoint (MultiGPU) / Debug — early/less tested; use debug node for diagnostics  
- KSampler (MultiGPU) / Debug  
- VAE Decode (MultiGPU) / Debug  
- GPU Status Display (+ Debug)

### Contributors
Humans: 
- Stefan (AngelCookies), code/research/testing  

AI: 
- Gemini (license help, research)
- GPT-5 / GPT-5-Codex-Max (license, code)
- Claude (original test nodes, research, fixes)

This project encourages AI coding tools with human oversight.

### Motivation and Why
High-end GPUs are expensive (e.g., RTX 5090 ~£2,500), and even large cards cap out on sequence length or render duration. Inspired by Ollama’s multi-GPU weight sharding, this project aims to combine multiple affordable GPUs to match or exceed a single large card without sacrificing quality. The first milestone is a stable workflow where all cards participate; next is broader node coverage so the setup is useful for real workloads, not just demos. Example goals: make 4×RTX 5060 8GB approximate a 5090 32GB, or 2×RTX 3090 24GB compete with a 6000 Ada 48GB.

Note on low-VRAM cards: the focus is 8, 12, 24 GB GPUs working together. While some of the techniques might help 4–6 GB cards, supporting very low-VRAM hardware for large models is not a target.

Note on interconnects: NVLink/SLI is not required; sharding runs over standard PCIe (e.g., tested on RTX 3070s without NVLink).

### Model assets used in testing
- SD/SDXL: use the checkpoint’s built-in CLIP/VAE, or point the loader to an external VAE if preferred.
- Flux: external text encoders `clip_l.safetensors` and `t5xxl_fp8_e4m3fn_scaled.safetensors`, plus VAE `ae.safetensors` placed in `models/text_encoders` and `models/vae`, then selected in the Flux loader.
