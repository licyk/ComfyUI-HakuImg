from __future__ import annotations

import numpy as np
import torch
from comfy_api.latest import IO
from PIL import Image

from ..effects.licyk_style import run

SEED_MAX = 0xFFFFFFFFFFFFFFFF


def _tensor_to_pil_images(image: torch.Tensor) -> list[Image.Image]:
    if image.ndim == 3:
        image = image.unsqueeze(0)
    if image.ndim != 4 or image.shape[-1] not in (3, 4):
        raise ValueError("Expected an IMAGE tensor with shape [B, H, W, 3/4]")

    image_array = image.detach().cpu().clamp(0, 1).numpy()
    mode = "RGBA" if image_array.shape[-1] == 4 else "RGB"
    return [
        Image.fromarray(
            np.clip(frame * 255, 0, 255).astype(np.uint8),
            mode=mode,
        )
        for frame in image_array
    ]


class LicykStyle(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="LicykStyle",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("image"),
                IO.Int.Input(
                    "seed",
                    default=0,
                    min=0,
                    max=SEED_MAX,
                    control_after_generate=True,
                ),
                IO.Float.Input("noise_strength", default=0.4, min=0, max=1, step=0.01),
                IO.Int.Input("noise_r", default=255, min=0, max=255, step=1),
                IO.Int.Input("noise_g", default=255, min=0, max=255, step=1),
                IO.Int.Input("noise_b", default=255, min=0, max=255, step=1),
                IO.Int.Input("offset_percentage", default=20, min=0, max=100, step=1),
                IO.Int.Input("opacity", default=128, min=0, max=255, step=1),
                IO.Float.Input("chromatic_strength", default=0.3, min=0, max=1, step=0.01),
                IO.Boolean.Input("chromatic_blur", default=False),
                IO.Float.Input("glow_strength", default=0, min=0, max=2, step=0.01),
                IO.Float.Input("glow_threshold", default=0.6, min=0, max=1, step=0.01),
                IO.Float.Input("glow_radius", default=3, min=0.5, max=10, step=0.1),
                IO.Int.Input("glow_r", default=255, min=0, max=255, step=1),
                IO.Int.Input("glow_g", default=240, min=0, max=255, step=1),
                IO.Int.Input("glow_b", default=220, min=0, max=255, step=1),
                IO.Float.Input("glow_soft_focus", default=0.3, min=0, max=1, step=0.01),
                IO.Float.Input("glow_edge_softness", default=0.2, min=0, max=1, step=0.01),
            ],
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    # ComfyUI's base class uses **kwargs, while node implementations expose
    # concrete parameters so the runtime can bind and document each input.
    # ty: ignore[invalid-method-override]
    def execute(
        cls,
        image: torch.Tensor,
        seed: int,
        noise_strength: float,
        noise_r: int,
        noise_g: int,
        noise_b: int,
        offset_percentage: int,
        opacity: int,
        chromatic_strength: float,
        chromatic_blur: bool,
        glow_strength: float = 0,
        glow_threshold: float = 0.6,
        glow_radius: float = 3,
        glow_r: int = 255,
        glow_g: int = 240,
        glow_b: int = 220,
        glow_soft_focus: float = 0.3,
        glow_edge_softness: float = 0.2,
    ) -> IO.NodeOutput:
        output_images: list[np.ndarray] = []
        for batch_index, pil_image in enumerate(_tensor_to_pil_images(image)):
            processed = run(
                image=pil_image,
                seed=(seed + batch_index) & SEED_MAX,
                noise_strength=noise_strength,
                noise_r=noise_r,
                noise_g=noise_g,
                noise_b=noise_b,
                offset_percentage=offset_percentage,
                opacity=opacity,
                chromatic_strength=chromatic_strength,
                chromatic_blur=chromatic_blur,
                glow_strength=glow_strength,
                glow_threshold=glow_threshold,
                glow_radius=glow_radius,
                glow_r=glow_r,
                glow_g=glow_g,
                glow_b=glow_b,
                glow_soft_focus=glow_soft_focus,
                glow_edge_softness=glow_edge_softness,
            )
            output_images.append(np.asarray(processed.convert("RGB"), dtype=np.float32) / 255.0)

        return IO.NodeOutput(torch.from_numpy(np.stack(output_images)))
