import torch
import numpy as np
from PIL import Image
from comfy_api.latest import IO
from ..effects.color import run


class Color(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="Color",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("image"),
                IO.Int.Input("temperature", default=0, min=-100, max=100, step=1),
                IO.Int.Input("hue", default=0, min=-90, max=90, step=1),
                IO.Int.Input("brightness", default=0, min=-100, max=100, step=1),
                IO.Int.Input("contrast", default=0, min=-100, max=100, step=1),
                IO.Int.Input("saturation", default=0, min=-100, max=100, step=1),
                IO.Float.Input("gamma", default=1, min=0.2, max=2.2, step=0.1),
                IO.Float.Input("exposure_offset", default=0, min=0, max=1, step=0.01),
                IO.Float.Input("vignette", default=0, min=0, max=1, step=0.01),
                IO.Float.Input("noise", default=0, min=0, max=1, step=0.01),
                IO.Float.Input("sharpness", default=0, min=0, max=1, step=0.01),
                IO.Float.Input("hdr", default=0, min=0, max=1, step=0.01),
            ],
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(
        cls,
        image: torch.Tensor,
        temperature: int,
        hue: int,
        brightness: int,
        contrast: int,
        saturation: int,
        gamma: float,
        exposure_offset: float,
        vignette: float,
        noise: float,
        sharpness: float,
        hdr: float,
    ) -> IO.NodeOutput:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, "RGB").convert("RGBA")

        image_pil = run(
            image_pil,
            brightness,
            contrast,
            saturation,
            temperature,
            hue,
            gamma,
            exposure_offset,
            hdr,
            noise,
            sharpness,
            vignette,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return IO.NodeOutput(image_output)
