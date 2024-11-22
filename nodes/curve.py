import torch
import numpy as np
from PIL import Image
from ..hakuimg.curve import run


class CURVE:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
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
            images: Image.Image,
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
    ):
        images = images.squeeze().numpy()
        images = (images * 255).astype(np.uint8)
        images = Image.fromarray(images, 'RGB').convert('RGBA')

        curve_func = run(3)
        images = curve_func(
            images,
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

        images = np.array(images).astype(np.float32) / 255.0
        images = torch.from_numpy(images)[None,]

        return (images,)
