import torch
import numpy as np
from PIL import Image
from comfy_api.latest import IO
from ..effects.sketch import run


class Sketch(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="Sketch",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("image"),
                IO.Int.Input("kernel_size", default=0, min=0, max=25, step=1),
                IO.Float.Input("sigma", default=1.4, min=1, max=5, step=0.05),
                IO.Float.Input("k_sigma", default=1.6, min=1, max=5, step=0.05),
                IO.Float.Input("epsilon", default=-0.03, min=-0.2, max=0.2, step=0.005),
                IO.Float.Input("phi", default=10, min=1, max=50, step=1),
                IO.Float.Input("gamma", default=1.0, min=0.75, max=1, step=0.005),
                IO.Combo.Input("color_mode", options=["gray", "rgb"]),
                IO.Boolean.Input("scale", default=False),
            ],
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(
        cls,
        image: torch.Tensor,
        kernel_size: float,
        sigma: float,
        k_sigma: float,
        epsilon: float,
        phi: float,
        gamma: float,
        color_mode: str,
        scale: bool,
    ) -> IO.NodeOutput:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, "RGB").convert("RGBA")

        image_pil = run(
            image_pil,
            kernel_size,
            sigma,
            k_sigma,
            epsilon,
            phi,
            gamma,
            color_mode,
            scale,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return IO.NodeOutput(image_output)
