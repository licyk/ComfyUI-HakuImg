import torch
import numpy as np
from PIL import Image
from comfy_api.latest import IO
from ..effects.flip import run


class Flip(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="Flip",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("image"),
                IO.Combo.Input("axis", options=["horizontal", "vertical"]),
            ],
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(
        cls,
        image: torch.Tensor,
        axis: str,
    ) -> IO.NodeOutput:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, "RGB").convert("RGBA")

        image_pil = run(
            image_pil,
            axis,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return IO.NodeOutput(image_output)
