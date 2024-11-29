import torch
import numpy as np
from PIL import Image
from ..hakuimg.blend import run, blend_methods


class BLENDIMAGE:
    @classmethod
    def INPUT_TYPES(cls):
        inputs = {
            "optional": {
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
                "bg_color": (
                    "COLOR",
                    {"default": "#FFFFFF"},
                ),
            },
        }
        for i in range(1, 6):
            # inputs["required"][f"image_{i}"] = ("IMAGE",)
            # inputs["required"][f"mask_{i}"] = ("MASK",)
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

    # def process_image(self, images_count, **kwargs):
    #     images = [kwargs[f"image_{i}"] for i in range(1, images_count + 1)]
    #     masks = [kwargs[f"mask_{i}"] for i in range(1, images_count + 1)]
    #     alphas = [kwargs[f"alpha_{i}"] for i in range(1, images_count + 1)]
    #     mask_blurs = [kwargs[f"mask_blur_{i}"] for i in range(1, images_count + 1)]
    #     mask_strengths = [
    #         kwargs[f"mask_strength_{i}"] for i in range(1, images_count + 1)
    #     ]
    #     modes = [kwargs[f"mode_{i}"] for i in range(1, images_count + 1)]

    def process_image(
        self,
        images_count: int,
        bg_color: str,
        image_1: Image.Image = None,
        image_2: Image.Image = None,
        image_3: Image.Image = None,
        image_4: Image.Image = None,
        image_5: Image.Image = None,
        mask_1: Image.Image = None,
        mask_2: Image.Image = None,
        mask_3: Image.Image = None,
        mask_4: Image.Image = None,
        mask_5: Image.Image = None,
        alpha_1: float = None,
        alpha_2: float = None,
        alpha_3: float = None,
        alpha_4: float = None,
        alpha_5: float = None,
        mask_blur_1: float = None,
        mask_blur_2: float = None,
        mask_blur_3: float = None,
        mask_blur_4: float = None,
        mask_blur_5: float = None,
        mask_strength_1: float = None,
        mask_strength_2: float = None,
        mask_strength_3: float = None,
        mask_strength_4: float = None,
        mask_strength_5: float = None,
        mode_1: str = None,
        mode_2: str = None,
        mode_3: str = None,
        mode_4: str = None,
        mode_5: str = None,
    ):
        # image
        if image_1 is not None:
            if mask_1 is None:
                raise Exception("image_1 input need mask_1 input, but missing")

            image_1 = image_1.squeeze().numpy()
            image_1 = (image_1 * 255).astype(np.uint8)
            image_1 = Image.fromarray(image_1, "RGB").convert("RGBA")

        if image_2 is not None:
            if mask_2 is None:
                raise Exception("image_2 input need mask_2 input, but missing")

            image_2 = image_2.squeeze().numpy()
            image_2 = (image_2 * 255).astype(np.uint8)
            image_2 = Image.fromarray(image_2, "RGB").convert("RGBA")

        if image_3 is not None:
            if mask_3 is None:
                raise Exception("image_3 input need mask_3 input, but missing")

            image_3 = image_3.squeeze().numpy()
            image_3 = (image_3 * 255).astype(np.uint8)
            image_3 = Image.fromarray(image_3, "RGB").convert("RGBA")

        if image_4 is not None:
            if mask_4 is None:
                raise Exception("image_4 input need mask_4 input, but missing")

            image_4 = image_4.squeeze().numpy()
            image_4 = (image_4 * 255).astype(np.uint8)
            image_4 = Image.fromarray(image_4, "RGB").convert("RGBA")

        if image_5 is not None:
            if mask_5 is None:
                raise Exception("image_5 input need mask_5 input, but missing")

            image_5 = image_5.squeeze().numpy()
            image_5 = (image_5 * 255).astype(np.uint8)
            image_5 = Image.fromarray(image_5, "RGB").convert("RGBA")

        # mask
        if mask_1 is not None:
            if image_1 is None:
                raise Exception("mask_1 input need image_1 input, but missing")

            mask_1 = mask_1.squeeze().numpy()
            mask_1 = (mask_1 * 255).astype(np.uint8)
            mask_1 = Image.fromarray(mask_1, "L")
            image_1 = {"image": image_1, "mask": mask_1}

        if mask_2 is not None:
            if image_2 is None:
                raise Exception("mask_2 input need image_2 input, but missing")

            mask_2 = mask_2.squeeze().numpy()
            mask_2 = (mask_2 * 255).astype(np.uint8)
            mask_2 = Image.fromarray(mask_2, "L")
            image_2 = {"image": image_2, "mask": mask_2}

        if mask_3 is not None:
            if image_3 is None:
                raise Exception("mask_3 input need image_3 input, but missing")

            mask_3 = mask_3.squeeze().numpy()
            mask_3 = (mask_3 * 255).astype(np.uint8)
            mask_3 = Image.fromarray(mask_3, "L")
            image_3 = {"image": image_3, "mask": mask_3}

        if mask_4 is not None:
            if image_4 is None:
                raise Exception("mask_4 input need image_4 input, but missing")

            mask_4 = mask_4.squeeze().numpy()
            mask_4 = (mask_4 * 255).astype(np.uint8)
            mask_4 = Image.fromarray(mask_4, "L")
            image_4 = {"image": image_4, "mask": mask_4}

        if mask_5 is not None:
            if image_5 is None:
                raise Exception("mask_5 input need image_5 input, but missing")

            mask_5 = mask_5.squeeze().numpy()
            mask_5 = (mask_5 * 255).astype(np.uint8)
            mask_5 = Image.fromarray(mask_5, "L")
            image_5 = {"image": image_5, "mask": mask_5}

        blend_func = run(5)
        bg = bg_color

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
            image_1,
            image_2,
            image_3,
            image_4,
            image_5,
        )

        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]

        return (image,)
