from typing import Any, Callable

from PIL import Image, ImageFilter, ImageColor
import numpy as np


def basic(target: np.ndarray, blend: np.ndarray, opacity: float) -> np.ndarray:
    return target * opacity + blend * (1 - opacity)


def blender(func: Callable[..., np.ndarray]) -> Callable[..., np.ndarray]:
    def blend(target: np.ndarray, blend: np.ndarray, opacity: float=1, *args: Any) -> np.ndarray:
        res = func(target, blend, *args)
        res = basic(res, blend, opacity)
        return np.clip(res, 0, 1)

    return blend


class Blend:
    @classmethod
    def method(cls, name: str) -> Callable[..., np.ndarray]:
        return getattr(cls, name)

    normal = basic

    @staticmethod
    @blender
    def darken(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return np.minimum(target, blend)

    @staticmethod
    @blender
    def multiply(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return target * blend

    @staticmethod
    @blender
    def color_burn(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return 1 - (1 - target) / blend

    @staticmethod
    @blender
    def linear_burn(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return target + blend - 1

    @staticmethod
    @blender
    def lighten(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return np.maximum(target, blend)

    @staticmethod
    @blender
    def screen(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return 1 - (1 - target) * (1 - blend)

    @staticmethod
    @blender
    def color_dodge(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return target / (1 - blend)

    @staticmethod
    @blender
    def linear_dodge(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return target + blend

    @staticmethod
    @blender
    def overlay(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return (target > 0.5) * (1 - (2 - 2 * target) * (1 - blend)) + (
            target <= 0.5
        ) * (2 * target * blend)

    @staticmethod
    @blender
    def soft_light(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return (blend > 0.5) * (1 - (1 - target) * (1 - (blend - 0.5))) + (
            blend <= 0.5
        ) * (target * (blend + 0.5))

    @staticmethod
    @blender
    def hard_light(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return (blend > 0.5) * (1 - (1 - target) * (2 - 2 * blend)) + (blend <= 0.5) * (
            2 * target * blend
        )

    @staticmethod
    @blender
    def vivid_light(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return (blend > 0.5) * (1 - (1 - target) / (2 * blend - 1)) + (blend <= 0.5) * (
            target / (1 - 2 * blend)
        )

    @staticmethod
    @blender
    def linear_light(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return (blend > 0.5) * (target + 2 * (blend - 0.5)) + (blend <= 0.5) * (
            target + 2 * blend
        )

    @staticmethod
    @blender
    def pin_light(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return (blend > 0.5) * np.maximum(target, 2 * (blend - 0.5)) + (
            blend <= 0.5
        ) * np.minimum(target, 2 * blend)

    @staticmethod
    @blender
    def difference(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return np.abs(target - blend)

    @staticmethod
    @blender
    def exclusion(target: np.ndarray, blend: np.ndarray, *args: Any) -> np.ndarray:
        return 0.5 - 2 * (target - 0.5) * (blend - 0.5)


blend_methods = [i for i in Blend.__dict__ if i[0] != "_" and i != "method"]


def run(layers: int) -> Callable[..., Image.Image]:
    def blend(bg: str, *args: Any) -> Image.Image:
        assert len(args) % 5 == 0
        chunks = [args[i * layers : i * layers + layers] for i in range(5)]
        h, w, c = np.array([i["image"] for i in chunks[-1] if i is not None][0]).shape
        base_img = np.array(
            Image.new(mode="RGB", size=(w, h), color=ImageColor.getcolor(bg, "RGB"))
        )
        base_img = base_img.astype(np.float64) / 255

        for alpha, mask_blur, mask_str, mode, img in reversed(list(zip(*chunks))):
            if img is None or img["image"] is None:
                continue
            img_now = img["image"].convert('RGB').resize((w, h))
            mask = img["mask"].convert('L')

            img_now = np.array(img_now).astype(np.float64) / 255
            mask = mask.resize((w, h)).filter(ImageFilter.GaussianBlur(mask_blur))
            mask = np.expand_dims(np.array(mask) * mask_str / 255, 2)

            img_now = Blend.normal(base_img, img_now, mask)
            base_img = Blend.method(mode)(img_now, base_img, alpha)
        base_img *= 255
        base_img = np.clip(base_img, 0, 255)

        return Image.fromarray(base_img.astype(np.uint8), mode="RGB")

    return blend
