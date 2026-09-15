from typing import Any

import torch
import numpy as np
from PIL import Image
from ..effects.blend import run, blend_methods


class BLENDIMAGE:
    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        inputs: dict[str, dict[str, object]] = {
            "optional": {
                "bg_color": (
                    "INT",
                    {"default": 0xFFFFFF, "min": 0, "max": 0xFFFFFF, "step": 1},
                ),
                "image_1": ("IMAGE",),
                "mask_1": ("MASK",),
                "image_2": ("IMAGE",),
                "mask_2": ("MASK",),
                "image_3": ("IMAGE",),
                "mask_3": ("MASK",),
                "image_4": ("IMAGE",),
                "mask_4": ("MASK",),
                "image_5": ("IMAGE",),
                "mask_5": ("MASK",),
            },
            "required": {
                "images_count": (
                    "INT",
                    {"default": 2, "min": 1, "max": 5, "step": 1},
                ),
            },
        }
        for i in range(1, 6):
            inputs["required"][f"alpha_{i}"] = (
                "FLOAT",
                {"default": 1, "min": 0, "max": 1, "step": 0.01},
            )
            inputs["required"][f"mask_blur_{i}"] = (
                "FLOAT",
                {"default": 4, "min": 0, "max": 32, "step": 0.05},
            )
            inputs["required"][f"mask_strength_{i}"] = (
                "FLOAT",
                {"default": 1, "min": 0, "max": 1, "step": 0.01},
            )
            inputs["required"][f"mode_{i}"] = (
                blend_methods,
                {"default": blend_methods[0]},
            )

        return inputs

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "process_image"
    CATEGORY = "image/HakuImg"

    def process_image(
        self,
        images_count: int,
        bg_color: int = 0xFFFFFF,
        image_1: torch.Tensor | None = None,
        image_2: torch.Tensor | None = None,
        image_3: torch.Tensor | None = None,
        image_4: torch.Tensor | None = None,
        image_5: torch.Tensor | None = None,
        mask_1: torch.Tensor | None = None,
        mask_2: torch.Tensor | None = None,
        mask_3: torch.Tensor | None = None,
        mask_4: torch.Tensor | None = None,
        mask_5: torch.Tensor | None = None,
        alpha_1: float | None = None,
        alpha_2: float | None = None,
        alpha_3: float | None = None,
        alpha_4: float | None = None,
        alpha_5: float | None = None,
        mask_blur_1: float | None = None,
        mask_blur_2: float | None = None,
        mask_blur_3: float | None = None,
        mask_blur_4: float | None = None,
        mask_blur_5: float | None = None,
        mask_strength_1: float | None = None,
        mask_strength_2: float | None = None,
        mask_strength_3: float | None = None,
        mask_strength_4: float | None = None,
        mask_strength_5: float | None = None,
        mode_1: str | None = None,
        mode_2: str | None = None,
        mode_3: str | None = None,
        mode_4: str | None = None,
        mode_5: str | None = None,
    ) -> tuple[torch.Tensor]:
        def to_image_item(
            image: torch.Tensor | None, mask: torch.Tensor | None, name: str
        ) -> dict[str, Image.Image] | None:
            if image is None and mask is None:
                return None
            if image is None or mask is None:
                raise Exception(f"{name} input need matching {name} mask input, but missing")

            image_data = image.squeeze().numpy()
            image_data = (image_data * 255).astype(np.uint8)
            image_pil = Image.fromarray(image_data, "RGB").convert("RGBA")

            mask_data = mask.squeeze().numpy()
            mask_data = (mask_data * 255).astype(np.uint8)
            mask_pil = Image.fromarray(mask_data, "L")

            return {"image": image_pil, "mask": mask_pil}

        image_1_item = to_image_item(image_1, mask_1, "image_1")
        image_2_item = to_image_item(image_2, mask_2, "image_2")
        image_3_item = to_image_item(image_3, mask_3, "image_3")
        image_4_item = to_image_item(image_4, mask_4, "image_4")
        image_5_item = to_image_item(image_5, mask_5, "image_5")

        blend_func = run(5)
        bg = f"#{hex(bg_color)[2:].upper()}"

        image = blend_func(
            bg,
            alpha_1,
            alpha_2,
            alpha_3,
            alpha_4,
            alpha_5,
            mask_blur_1,
            mask_blur_2,
            mask_blur_3,
            mask_blur_4,
            mask_blur_5,
            mask_strength_1,
            mask_strength_2,
            mask_strength_3,
            mask_strength_4,
            mask_strength_5,
            mode_1,
            mode_2,
            mode_3,
            mode_4,
            mode_5,
            image_1_item,
            image_2_item,
            image_3_item,
            image_4_item,
            image_5_item,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
