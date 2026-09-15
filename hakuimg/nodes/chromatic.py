import torch
import numpy as np
from PIL import Image
from comfy_api.latest import IO
from ..effects.chromatic import run


class Chromatic(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="Chromatic",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("image"),
                IO.Float.Input("strength", default=1, min=0, max=3, step=0.01),
                IO.Boolean.Input("blur", default=False),
            ],
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(
        cls,
        image: torch.Tensor,
        strength: float,
        blur: bool,
    ) -> IO.NodeOutput:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, "RGB")

        image_pil = run(
            image_pil,
            strength,
            blur,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return IO.NodeOutput(image_output)
