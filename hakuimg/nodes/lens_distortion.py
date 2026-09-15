import torch
import numpy as np
from PIL import Image
from comfy_api.latest import IO
from ..effects.lens_distortion import run


class LenDistortion(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="LenDistortion",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("image"),
                IO.Float.Input("lens_distortion_k1", default=0, min=-1, max=1, step=0.01),
                IO.Float.Input("lens_distortion_k2", default=0, min=-1, max=1, step=0.01),
            ],
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(
        cls,
        image: torch.Tensor,
        lens_distortion_k1: float,
        lens_distortion_k2: float,
    ) -> IO.NodeOutput:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, "RGB").convert("RGBA")

        image_pil = run(
            image_pil,
            lens_distortion_k1,
            lens_distortion_k2,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return IO.NodeOutput(image_output)
