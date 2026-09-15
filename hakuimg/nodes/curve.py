from typing import Any

import torch
import numpy as np
from PIL import Image

from ..effects.curve import run



class CURVE:
    @classmethod
    def INPUT_TYPES(cls) -> dict[str, Any]:
        return {
            "required": {
                "image": ("IMAGE",),
                "all_x_point_1": (
                    "INT", {
                        "default":63,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "all_y_point_1": (
                    "INT", {
                        "default":63,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "all_x_point_2": (
                    "INT", {
                        "default":127,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "all_y_point_2": (
                    "INT", {
                        "default":127,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "all_x_point_3": (
                    "INT", {
                        "default":191,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "all_y_point_3": (
                    "INT", {
                        "default":191,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "r_x_point_1": (
                    "INT", {
                        "default":63,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "r_y_point_1": (
                    "INT", {
                        "default":63,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "r_x_point_2": (
                    "INT", {
                        "default":127,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "r_y_point_2": (
                    "INT", {
                        "default":127,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "r_x_point_3": (
                    "INT", {
                        "default":191,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "r_y_point_3": (
                    "INT", {
                        "default":191,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "g_x_point_1": (
                    "INT", {
                        "default":63,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "g_y_point_1": (
                    "INT", {
                        "default":63,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "g_x_point_2": (
                    "INT", {
                        "default":127,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "g_y_point_2": (
                    "INT", {
                        "default":127,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "g_x_point_3": (
                    "INT", {
                        "default":191,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "g_y_point_3": (
                    "INT", {
                        "default":191,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "b_x_point_1": (
                    "INT", {
                        "default":63,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "b_y_point_1": (
                    "INT", {
                        "default":63,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "b_x_point_2": (
                    "INT", {
                        "default":127,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "b_y_point_2": (
                    "INT", {
                        "default":127,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "b_x_point_3": (
                    "INT", {
                        "default":191,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
                "b_y_point_3": (
                    "INT", {
                        "default":191,
                        "min": 0,
                        "max": 255,
                        "step": 1
                    }
                ),
            },
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("image",)
    FUNCTION = "process_image"
    CATEGORY = "image/HakuImg"


    def process_image(
            self,
            image: torch.Tensor,
            all_x_point_1: int,
            all_y_point_1: int,
            all_x_point_2: int,
            all_y_point_2: int,
            all_x_point_3: int,
            all_y_point_3: int,
            r_x_point_1: int,
            r_y_point_1: int,
            r_x_point_2: int,
            r_y_point_2: int,
            r_x_point_3: int,
            r_y_point_3: int,
            g_x_point_1: int,
            g_y_point_1: int,
            g_x_point_2: int,
            g_y_point_2: int,
            g_x_point_3: int,
            g_y_point_3: int,
            b_x_point_1: int,
            b_y_point_1: int,
            b_x_point_2: int,
            b_y_point_2: int,
            b_x_point_3: int,
            b_y_point_3: int,
    ) -> tuple[torch.Tensor]:
        image_array = image.squeeze().numpy()
        image_array = (image_array * 255).astype(np.uint8)

        pil_image = Image.fromarray(
            image_array,
            "RGB",
        ).convert("RGBA")

        curve_func = run(3)
        pil_image = curve_func(
            pil_image,
            all_x_point_1,
            all_y_point_1,
            all_x_point_2,
            all_y_point_2,
            all_x_point_3,
            all_y_point_3,
            r_x_point_1,
            r_y_point_1,
            r_x_point_2,
            r_y_point_2,
            r_x_point_3,
            r_y_point_3,
            g_x_point_1,
            g_y_point_1,
            g_x_point_2,
            g_y_point_2,
            g_x_point_3,
            g_y_point_3,
            b_x_point_1,
            b_y_point_1,
            b_x_point_2,
            b_y_point_2,
            b_x_point_3,
            b_y_point_3,
        )

        output_array = np.asarray(pil_image).astype(np.float32) / 255.0
        output_image = torch.from_numpy(output_array)[None,]

        return (output_image,)
