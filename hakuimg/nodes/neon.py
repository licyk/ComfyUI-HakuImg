import torch
import numpy as np
from PIL import Image
from comfy_api.latest import IO
from ..effects.neon import run


class Neon(IO.ComfyNode):
    @classmethod
    def define_schema(cls) -> IO.Schema:
        return IO.Schema(
            node_id="Glow",
            category="image/HakuImg",
            inputs=[
                IO.Image.Input("image"),
                IO.Combo.Input("glow_mode", options=["BS", "BMBL"]),
                IO.Int.Input("blur", default=16, min=2, max=128, step=1),
                IO.Float.Input("strength", default=1, min=0, max=1, step=0.01),
            ],
            outputs=[IO.Image.Output(display_name="image")],
        )

    @classmethod
    def execute(
        cls,
        image: torch.Tensor,
        blur: int,
        strength: float,
        glow_mode: str,
    ) -> IO.NodeOutput:
        image_tensor = image.squeeze().numpy()
        image_tensor = (image_tensor * 255).astype(np.uint8)
        image_pil = Image.fromarray(image_tensor, "RGB").convert("RGBA")

        image_pil = run(
            image_pil,
            blur,
            strength,
            glow_mode,
        )

        image_output = np.array(image_pil).astype(np.float32) / 255.0
        image_output = torch.from_numpy(image_output)[None,]

        return IO.NodeOutput(image_output)
